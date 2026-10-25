import { cp, mkdir, readdir, readFile, rm, writeFile, lstat } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const out = path.join(root, 'dist');
await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });
const publicManifest = JSON.parse(await readFile(path.join(root, 'public-artifacts.json'), 'utf8'));
if (publicManifest.schema_version !== 1) throw new Error('Invalid public artifact manifest version');
const destinations = new Set();
for (const [key, prefix] of [['website_files', 'site/'], ['document_files', '']]) {
  const files = publicManifest[key];
  if (!Array.isArray(files) || JSON.stringify(files) !== JSON.stringify([...new Set(files)].sort())) throw new Error('Public paths must be sorted and unique');
  for (const relative of files) {
    if (typeof relative !== 'string' || relative.includes('\\') || relative.startsWith('/') || relative.split('/').some(part => !part || part === '..' || part.startsWith('.') || ['internal','private','handoffs','runs','node_modules','__pycache__'].includes(part.toLowerCase()) || part.toLowerCase().includes('private'))) throw new Error('Unsafe/private public artifact path');
    if (prefix && !relative.startsWith(prefix)) throw new Error('Website source must originate in site/');
    const target = prefix ? relative.slice(prefix.length) : relative;
    if (destinations.has(target)) throw new Error('Public artifact destination collision');
    destinations.add(target);
    let source = root;
    for (const component of relative.split('/')) {
      source = path.join(source, component);
      if ((await lstat(source)).isSymbolicLink()) throw new Error('Public artifact symlinks are not allowed');
    }
    await mkdir(path.dirname(path.join(out, target)), { recursive: true });
    await cp(source, path.join(out, target));
  }
}
await mkdir(path.join(out, 'downloads'), { recursive: true });
await mkdir(path.join(out, 'archive'), { recursive: true });
for (const file of ['The_Garden_Original.html', 'The_Garden_v0.1_retrospective.html', 'Original_Concept_Experiment.md']) {
  await cp(path.join(root, 'archive', file), path.join(out, 'archive', file));
}
execFileSync('python3', ['scripts/package_release.py', '--toolkit-only'], { cwd: root, stdio: 'inherit' });
const revision = execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim();
await writeFile(path.join(out, 'health.json'), JSON.stringify({ status: 'ok', project: 'garden', version: '0.4.0', source_revision: revision, research_status: 'pre-pilot_no_results', inference_enabled: false }, null, 2) + '\n');
await writeFile(path.join(out, 'robots.txt'), 'User-agent: *\nAllow: /\nSitemap: https://garden.icarus.onl/sitemap.xml\n');
const pages = publicManifest.website_files.filter(f => /^site\/[^/]+\.html$/.test(f)).map(f => f.slice(5)).filter(f => f !== '404.html').sort();
await writeFile(path.join(out, 'sitemap.xml'), '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + pages.map(p => `  <url><loc>https://garden.icarus.onl/${p === 'index.html' ? '' : p}</loc></url>`).join('\n') + '\n</urlset>\n');
const hashes = {};
async function walk(dir, prefix = '') {
  for (const entry of (await readdir(dir, { withFileTypes: true })).sort((a,b) => a.name.localeCompare(b.name, 'en'))) {
    const key = prefix + entry.name;
    if (entry.isDirectory()) await walk(path.join(dir, entry.name), key + '/');
    else hashes[key] = createHash('sha256').update(await readFile(path.join(dir, entry.name))).digest('hex');
  }
}
await walk(out);
await writeFile(path.join(out, 'artifact-manifest.json'), JSON.stringify({ schema_version: 1, source_revision: revision, files: hashes }, null, 2) + '\n');
console.log(`Built ${Object.keys(hashes).length} public files from ${revision.slice(0, 12)}.`);
