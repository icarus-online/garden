import { cp, mkdir, readdir, readFile, rm, writeFile } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import path from 'node:path';

const root = path.resolve(import.meta.dirname, '..');
const out = path.join(root, 'dist');
await rm(out, { recursive: true, force: true });
await mkdir(out, { recursive: true });
await cp(path.join(root, 'site'), out, { recursive: true });
for (const dir of ['docs', 'materials', 'methods']) {
  await mkdir(path.join(out, dir), { recursive: true });
  for (const file of await readdir(path.join(root, dir), { withFileTypes: true })) {
    if (file.isFile() && /\.(md|json)$/.test(file.name)) {
      await cp(path.join(root, dir, file.name), path.join(out, dir, file.name));
    }
  }
}
await mkdir(path.join(out, 'research', 'configs'), { recursive: true });
await cp(path.join(root, 'research', 'configs'), path.join(out, 'research', 'configs'), { recursive: true });
await mkdir(path.join(out, 'downloads'), { recursive: true });
await mkdir(path.join(out, 'archive'), { recursive: true });
for (const file of ['The_Garden_Original.html', 'The_Garden_v0.1_retrospective.html', 'Original_Concept_Experiment.md']) {
  await cp(path.join(root, 'archive', file), path.join(out, 'archive', file));
}
execFileSync('python3', ['scripts/package_release.py', '--toolkit-only'], { cwd: root, stdio: 'inherit' });
execFileSync('git', ['archive', '--format=zip', '--output=dist/downloads/garden-original-v0.3.zip', '5f242997cc802707baaf7568cc7fdc6e0649cbab'], { cwd: root });
const revision = execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim();
await writeFile(path.join(out, 'health.json'), JSON.stringify({ status: 'ok', project: 'garden', version: '0.4.0', source_revision: revision, research_status: 'pre-pilot_no_results', inference_enabled: false }, null, 2) + '\n');
await writeFile(path.join(out, 'robots.txt'), 'User-agent: *\nAllow: /\nSitemap: https://garden.icarus.onl/sitemap.xml\n');
const pages = (await readdir(path.join(root, 'site'))).filter(f => f.endsWith('.html') && f !== '404.html').sort();
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
