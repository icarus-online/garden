import { readFile, readdir, stat } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import path from 'node:path';
const root = path.resolve(import.meta.dirname, '..');
const out = path.join(root, 'dist');
const errors = [];
const assert = (ok, message) => { if (!ok) errors.push(message); };
const pages = (await readdir(out)).filter(f => f.endsWith('.html'));
for (const name of pages) {
  const html = await readFile(path.join(out, name), 'utf8');
  assert(/<html[^>]+lang="en"/.test(html), `${name}: language`);
  assert(/name="viewport"/.test(html), `${name}: viewport`);
  assert(/<title>[^<]+<\/title>/.test(html), `${name}: title`);
  assert(name === '404.html' || /rel="canonical"[^>]+https:\/\/garden\.icarus\.onl\//.test(html), `${name}: canonical`);
  assert((html.match(/<h1\b/g) || []).length === 1, `${name}: exactly one h1`);
  assert(/<main\b/.test(html), `${name}: main landmark`);
  assert(/class="skip(?:-link)?"/.test(html), `${name}: skip link`);
  assert(!/<script(?![^>]+src=)[^>]*>/.test(html), `${name}: inline script violates CSP`);
  assert(!/\s(?:on\w+|style)\s*=/.test(html), `${name}: inline style/handler violates CSP`);
  assert(!/(?:src|href)="https?:\/\/[^" ]+\.(?:js|css|woff2?)\b/.test(html), `${name}: remote dependency`);
  for (const match of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
    const href = match[1];
    if (/^(?:https?:|mailto:|data:|blob:)/.test(href)) continue;
    const [url, fragment] = href.split('#');
    const clean = url.split('?')[0];
    const target = path.join(out, clean === '/' ? 'index.html' : clean.replace(/^\//, '') || name);
    try {
      assert((await stat(target)).isFile(), `${name}: file link ${href}`);
      if (fragment && target.endsWith('.html')) {
        const other = await readFile(target, 'utf8');
        assert(other.includes(`id="${fragment}"`), `${name}: fragment ${href}`);
      }
    } catch { errors.push(`${name}: missing ${href}`); }
  }
}
const manifest = JSON.parse(await readFile(path.join(out, 'artifact-manifest.json'), 'utf8'));
for (const [name, hash] of Object.entries(manifest.files)) {
  assert(createHash('sha256').update(await readFile(path.join(out, name))).digest('hex') === hash, `Hash mismatch: ${name}`);
}
const originalCorpus = JSON.parse(await readFile(path.join(root, 'methods/corpus_manifest.json'), 'utf8'));
assert(Boolean(originalCorpus), 'Corpus manifest required');
const css = await readFile(path.join(out, 'assets/garden.css'), 'utf8');
assert(css.includes('prefers-reduced-motion'), 'Reduced-motion style required');
assert(css.includes(':focus-visible'), 'Visible keyboard focus required');
const forbidden = [/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/, /\b(?:ghp|github_pat|sk_live|sk_test)_[A-Za-z0-9_]{12,}\b/, /\b(?:AKIA|ASIA)[A-Z0-9]{16}\b/, /controlled-evidence:\/\//, /\/home\/icarus\//];
async function scan(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) await scan(file);
    else if (/\.(html|css|js|md|json|txt|xml|svg)$/.test(entry.name)) {
      const text = await readFile(file, 'utf8');
      assert(!forbidden.some(p => p.test(text)), `Public output sensitive-data pattern: ${path.relative(out, file)}`);
      if (entry.name.endsWith('.md')) {
        const prose = text.replace(/```[\s\S]*?```/g, '');
        for (const match of prose.matchAll(/\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)/g)) {
          const href = match[1];
          if (/^(?:[a-z][a-z0-9+.-]*:|#)/i.test(href)) continue;
          const clean = decodeURIComponent(href.split(/[?#]/)[0]);
          const target = clean.startsWith('/') ? path.resolve(out, '.' + clean) : path.resolve(path.dirname(file), clean);
          assert(target.startsWith(out + path.sep), `${path.relative(out, file)}: link escapes public output ${href}`);
          try { assert((await stat(target)).isFile(), `${path.relative(out, file)}: file link ${href}`); }
          catch { errors.push(`${path.relative(out, file)}: missing ${href}`); }
        }
      }
    }
  }
}
await scan(out);
if (errors.length) { console.error(errors.join('\n')); process.exitCode = 1; }
else console.log(`Validated ${pages.length} pages, local links, metadata, ${Object.keys(manifest.files).length} hashes, CSP compatibility, accessibility hooks and public-data exclusions.`);
