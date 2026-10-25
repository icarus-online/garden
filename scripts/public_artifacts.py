"""Explicit public-artifact boundary; no directory or extension-based discovery."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import zipfile

KEYS = {'schema_version', 'website_files', 'document_files', 'toolkit_files'}
PRIVATE_COMPONENTS = {'internal', 'private', 'handoffs', 'runs', 'node_modules', '__pycache__'}
GENERATED = {'downloads/garden-toolkit.zip',
             'archive/The_Garden_Original.html', 'archive/The_Garden_v0.1_retrospective.html',
             'archive/Original_Concept_Experiment.md', 'health.json', 'robots.txt', 'sitemap.xml',
             'artifact-manifest.json'}


def public_files(root, key):
    root = Path(root).resolve()
    manifest = json.loads((root / 'public-artifacts.json').read_text())
    if set(manifest) != KEYS or manifest['schema_version'] != 1:
        raise ValueError('Invalid public-artifact manifest fields/version')
    for field in KEYS - {'schema_version'}:
        entries = manifest[field]
        if (not isinstance(entries, list) or any(not isinstance(item, str) for item in entries)
                or entries != sorted(set(entries))):
            raise ValueError('Public-artifact lists must be sorted, unique explicit paths')
        for entry in entries:
            path = PurePosixPath(entry)
            if (not entry or '\\' in entry or path.is_absolute()
                    or any(part in {'', '.', '..'} for part in entry.split('/'))
                    or any(part.startswith('.') or part.lower() in PRIVATE_COMPONENTS
                           or 'private' in part.lower() for part in path.parts)):
                raise ValueError('Unsafe/private path in public-artifact manifest')
            candidate = root
            for part in path.parts:
                candidate /= part
                if candidate.is_symlink():
                    raise ValueError('Public artifacts cannot follow symlinks')
            if not candidate.is_file() or not candidate.resolve().is_relative_to(root):
                raise ValueError('Missing or outside public-artifact source')
            if field == 'website_files' and not entry.startswith('site/'):
                raise ValueError('Website artifacts must originate in site/')
            if field == 'document_files' and entry.startswith('site/'):
                raise ValueError('Documents must not shadow website paths')
    return [root / entry for entry in manifest[key]]


def validate_output(root, output=None):
    root = Path(root).resolve()
    output = Path(output or root / 'dist')
    expected = {p.relative_to(root / 'site').as_posix() for p in public_files(root, 'website_files')}
    expected.update(p.relative_to(root).as_posix() for p in public_files(root, 'document_files'))
    expected.update(GENERATED)
    actual = {p.relative_to(output).as_posix() for p in output.rglob('*') if p.is_file()}
    if actual != expected:
        raise ValueError('Public output differs from explicit artifact inventory')
    expected_toolkit = {p.relative_to(root).as_posix(): p for p in public_files(root, 'toolkit_files')}
    with zipfile.ZipFile(output / 'downloads/garden-toolkit.zip') as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) != set(expected_toolkit):
            raise ValueError('Public toolkit differs from explicit artifact inventory')
        for name, source in expected_toolkit.items():
            if hashlib.sha256(archive.read(name)).digest() != hashlib.sha256(source.read_bytes()).digest():
                raise ValueError('Public toolkit source hash mismatch')
    return {'public_files': len(actual), 'toolkit_files': len(expected_toolkit)}


if __name__ == '__main__':
    root = Path(__file__).resolve().parents[1]
    counts = validate_output(root)
    print(f"Explicit public boundary passed: {counts['public_files']} files, {counts['toolkit_files']} toolkit entries; no unlisted source.")
