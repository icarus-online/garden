#!/usr/bin/env python3
"""Validate a local release and atomically activate it. No network or container actions."""
import argparse
import fcntl
import gzip
import io
import hashlib
import json
import os
import re
import shutil
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

MAX_ARCHIVE = 64 * 1024 * 1024
MAX_CONTENT = 128 * 1024 * 1024
MAX_FILE = 16 * 1024 * 1024
MAX_ENTRIES = 5000
PUBLIC_SUFFIXES = {'.html','.css','.js','.json','.txt','.xml','.svg','.png','.jpg','.jpeg','.webp','.ico','.woff','.woff2','.ttf','.md','.zip','.pdf'}
FORBIDDEN_COMPONENTS = {'runs','node_modules','deploy','scripts','tests','__pycache__'}

class InvalidRelease(ValueError):
    pass

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read_json(path):
    def unique(items):
        obj = {}
        for key, value in items:
            if key in obj:
                raise InvalidRelease('Duplicate JSON keys')
            obj[key] = value
        return obj
    return json.loads(path.read_bytes(), object_pairs_hook=unique)

def safe_name(name):
    path = PurePosixPath(name)
    if (not name or '\\' in name or '\x00' in name or path.is_absolute()
        or any(part in ('','.','..') for part in name.rstrip('/').split('/'))
        or any(part.startswith('.') or part in FORBIDDEN_COMPONENTS or 'PRIVATE' in part for part in path.parts)):
        raise InvalidRelease(f'Unsafe or private archive path: {name!r}')
    return path.as_posix()

def verify_release(path, revision):
    manifest = read_json(path / 'artifact-manifest.json')
    if manifest.get('schema_version') != 1 or manifest.get('source_revision') != revision or not isinstance(manifest.get('files'), dict):
        raise InvalidRelease('Artifact manifest identity mismatch')
    files = manifest['files']
    if not {'index.html','404.html','health.json','assets/garden.js','assets/garden.css'} <= set(files):
        raise InvalidRelease('Required public files missing')
    actual = {p.relative_to(path).as_posix() for p in path.rglob('*') if p.is_file()}
    if actual != set(files) | {'artifact-manifest.json'}:
        raise InvalidRelease('Public artifact inventory mismatch')
    for name, expected in files.items():
        safe_name(name)
        target = path / name
        if target.is_symlink() or not target.resolve().is_relative_to(path.resolve()) or digest(target.read_bytes()) != expected:
            raise InvalidRelease(f'Public file hash/path mismatch: {name}')
    health = read_json(path / 'health.json')
    if (health.get('project') != 'garden' or health.get('status') != 'ok'
        or health.get('source_revision') != revision or health.get('research_status') != 'pre-pilot_no_results'
        or health.get('inference_enabled') is not False):
        raise InvalidRelease('Health identity/research status mismatch')
    return digest((path / 'artifact-manifest.json').read_bytes())

def install(archive, manifest_path, manifest_sha256, revision, root):
    archive, manifest_path, root = Path(archive), Path(manifest_path), Path(root)
    if not re.fullmatch('[a-f0-9]{40}', revision) or not re.fullmatch('[a-f0-9]{64}', manifest_sha256):
        raise InvalidRelease('Full lowercase Git revision and SHA-256 are required')
    if manifest_path.stat().st_size > 16384 or digest(manifest_path.read_bytes()) != manifest_sha256:
        raise InvalidRelease('Release manifest checksum mismatch')
    manifest = read_json(manifest_path)
    if set(manifest) != {'source_revision','sha256','bytes'} or manifest['source_revision'] != revision:
        raise InvalidRelease('Release manifest revision/fields mismatch')
    if type(manifest['bytes']) is not int or not 0 < manifest['bytes'] <= MAX_ARCHIVE or archive.stat().st_size != manifest['bytes']:
        raise InvalidRelease('Archive size mismatch or limit exceeded')
    archive_data = archive.read_bytes()
    if digest(archive_data) != manifest['sha256']:
        raise InvalidRelease('Archive checksum mismatch')
    # Bound decompression before tarfile parses hidden GNU/PAX metadata.
    with gzip.GzipFile(fileobj=io.BytesIO(archive_data)) as compressed:
        tar_bytes = compressed.read(MAX_CONTENT + 1)
    if len(tar_bytes) > MAX_CONTENT:
        raise InvalidRelease('Expanded archive size limit exceeded')
    if root.is_symlink():
        raise InvalidRelease('Deployment root cannot be a symlink')
    root.mkdir(parents=True, exist_ok=True, mode=0o755)
    releases = root / 'releases'
    if releases.is_symlink():
        raise InvalidRelease('Releases directory cannot be a symlink')
    releases.mkdir(exist_ok=True, mode=0o755)
    with (root / '.install.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        current = root / 'current'
        if current.exists() and not current.is_symlink():
            raise InvalidRelease('Current must be absent or a symlink')
        previous = os.readlink(current) if current.is_symlink() else None
        if previous is not None and (not previous.startswith('releases/') or not current.resolve().is_relative_to(releases.resolve())):
            raise InvalidRelease('Current symlink points outside releases')
        name = revision[:12] + '-' + manifest['sha256'][:16]
        destination = releases / name
        if destination.exists() or destination.is_symlink():
            raise InvalidRelease('Release already exists; preserve it and use the documented rollback procedure')
        stage = Path(tempfile.mkdtemp(prefix='.stage-',dir=releases))
        next_link = root / ('.current-' + name)
        try:
            total, seen = 0, set()
            # Consume the exact verified bytes; never reopen a replaceable archive.
            with tarfile.open(fileobj=io.BytesIO(tar_bytes), mode='r|') as tar:
                for index, member in enumerate(tar, 1):
                    if index > MAX_ENTRIES:
                        raise InvalidRelease('Too many archive entries')
                    relative = safe_name(member.name)
                    if relative in seen:
                        raise InvalidRelease('Duplicate archive path')
                    seen.add(relative)
                    target = stage / relative
                    if member.isdir():
                        target.mkdir(parents=True, exist_ok=True, mode=0o755)
                        continue
                    if not member.isfile() or member.issparse() or member.pax_headers:
                        raise InvalidRelease('Only ordinary files/directories allowed; links and extended metadata rejected')
                    if target.suffix.lower() not in PUBLIC_SUFFIXES:
                        raise InvalidRelease(f'Non-public file type: {relative}')
                    total += member.size
                    if member.size < 0 or member.size > MAX_FILE or total > MAX_CONTENT:
                        raise InvalidRelease('Expanded content size limit exceeded')
                    target.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
                    stream = tar.extractfile(member)
                    if stream is None:
                        raise InvalidRelease('Missing tar file stream')
                    with target.open('xb') as output:
                        remaining = member.size
                        while remaining:
                            chunk = stream.read(min(remaining, 1024 * 1024))
                            if not chunk:
                                raise InvalidRelease('Truncated tar entry')
                            output.write(chunk)
                            remaining -= len(chunk)
                        output.flush()
                        os.fsync(output.fileno())
                    target.chmod(0o644)
            artifact_sha = verify_release(stage, revision)
            stage.chmod(0o755)
            stage.rename(destination)
            receipt = {'release':name,'source_revision':revision,'archive_sha256':manifest['sha256'],
                'release_manifest_sha256':manifest_sha256,'artifact_manifest_sha256':artifact_sha,'previous':previous,
                'current':'releases/' + name}
            receipt_dir = root / '.deployment-records'
            receipt_dir.mkdir(exist_ok=True, mode=0o700)
            receipt_path = receipt_dir / (name + '.json')
            receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
            receipt_path.chmod(0o600)
            next_link.symlink_to('releases/' + name)
            os.replace(next_link, current)
            directory_fd = os.open(root, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
            return receipt
        finally:
            if stage.exists():
                shutil.rmtree(stage)
            if next_link.is_symlink():
                next_link.unlink()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--archive',type=Path,required=True)
    parser.add_argument('--manifest',type=Path,required=True)
    parser.add_argument('--manifest-sha256',required=True)
    parser.add_argument('--revision',required=True)
    parser.add_argument('--root',type=Path,default=Path('/opt/garden'))
    args=parser.parse_args()
    try:
        result=install(args.archive,args.manifest,args.manifest_sha256,args.revision,args.root)
    except (InvalidRelease,OSError,ValueError,EOFError,tarfile.TarError) as error:
        parser.exit(2,f'Release refused: {error}\n')
    print(json.dumps(result,indent=2))

if __name__ == '__main__':
    main()
