import http from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import path from 'node:path';
const root = path.resolve(import.meta.dirname, '../dist');
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.svg': 'image/svg+xml', '.json': 'application/json', '.md': 'text/plain; charset=utf-8', '.txt': 'text/plain', '.xml': 'application/xml', '.zip': 'application/zip' };
const csp = "default-src 'none'; base-uri 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'none'";
const port = Number(process.env.PORT || 4178);
http.createServer(async (req, res) => {
  const headers = { 'Content-Security-Policy': csp, 'X-Content-Type-Options': 'nosniff', 'Referrer-Policy': 'no-referrer', 'Permissions-Policy': 'camera=(), microphone=(), geolocation=(), payment=()', 'Cache-Control': 'public, max-age=0, must-revalidate' };
  if (!['GET', 'HEAD'].includes(req.method)) { res.writeHead(405, { ...headers, Allow: 'GET, HEAD' }); res.end(); return; }
  try {
    const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    let file = path.resolve(root, '.' + pathname);
    if (!file.startsWith(root + path.sep) && file !== root) throw Error('Invalid path');
    if (pathname.split('/').some(p => p.startsWith('.'))) throw Error('Private path');
    if ((await stat(file)).isDirectory()) file = path.join(file, 'index.html');
    const data = await readFile(file);
    res.writeHead(200, { ...headers, 'Content-Type': types[path.extname(file)] || 'application/octet-stream', 'Content-Length': data.length });
    res.end(req.method === 'HEAD' ? undefined : data);
  } catch {
    const data = await readFile(path.join(root, '404.html')).catch(() => Buffer.from('Not found'));
    res.writeHead(404, { ...headers, 'Cache-Control': 'no-store', 'Content-Type': 'text/html; charset=utf-8' });
    res.end(req.method === 'HEAD' ? undefined : data);
  }
}).listen(port, '127.0.0.1', () => console.log(`Garden preview: http://127.0.0.1:${port}`));
