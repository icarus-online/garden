"""Deterministic public toolkit and deployment artifacts; never include runs/secrets."""
from pathlib import Path
import argparse
import gzip
import hashlib
import io
import json
import subprocess
import tarfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def toolkit():
    files = [ROOT / 'README.md', ROOT / 'AGENTS.md']
    for directory in ['research', 'materials', 'methods', 'docs', 'tests']:
        files += [p for p in (ROOT / directory).rglob('*')
                  if p.is_file() and p.suffix in {'.py', '.json', '.md', '.csv'}
                  and '__pycache__' not in p.parts]
    files += [ROOT / 'scripts' / name for name in ['make_allocations.py', 'freeze_corpora.py']]
    destination = ROOT / 'dist/downloads/garden-toolkit.zip'
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in sorted(set(files)):
            if not p.exists():
                continue
            info = zipfile.ZipInfo(p.relative_to(ROOT).as_posix(), (2026, 10, 19, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes())


def release():
    dirty = subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True)
    if dirty:
        raise SystemExit('Release packaging requires a clean committed checkout.')
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    health = json.loads((ROOT / 'dist/health.json').read_text())
    if health['source_revision'] != revision:
        raise SystemExit('Build revision does not match source; rebuild first.')
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode='w') as tar:
        for file in sorted((ROOT / 'dist').rglob('*')):
            if not file.is_file():
                continue
            data = file.read_bytes()
            info = tarfile.TarInfo(file.relative_to(ROOT / 'dist').as_posix())
            info.size = len(data)
            info.mode = 0o644
            info.mtime = 0
            tar.addfile(info, io.BytesIO(data))
    compressed = gzip.compress(buffer.getvalue(), mtime=0)
    out = ROOT / '.release'
    out.mkdir(exist_ok=True)
    artifact = out / 'garden.tar.gz'
    artifact.write_bytes(compressed)
    manifest = {'source_revision': revision, 'sha256': hashlib.sha256(compressed).hexdigest(), 'bytes': len(compressed)}
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(manifest))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--toolkit-only', action='store_true')
    args = parser.parse_args()
    toolkit() if args.toolkit_only else release()
