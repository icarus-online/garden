"""Regression checks for the public site and downloadable source boundary."""
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.package_release import toolkit
from scripts.public_artifacts import public_files, validate_output, GENERATED


class PublicArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'source'
        self.root.mkdir()
        self.manifest = json.loads((ROOT / 'public-artifacts.json').read_text())
        for name in set().union(*(set(self.manifest[key]) for key in ('website_files', 'document_files', 'toolkit_files'))):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / name, target)
        self.write_manifest()

    def tearDown(self):
        self.temp.cleanup()

    def write_manifest(self):
        (self.root / 'public-artifacts.json').write_text(json.dumps(self.manifest))

    def output(self):
        out = self.root / 'dist'
        for key in ('website_files', 'document_files'):
            for source in public_files(self.root, key):
                name = source.relative_to(self.root / 'site' if key == 'website_files' else self.root)
                destination = out / name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
        for name in GENERATED - {'downloads/garden-toolkit.zip'}:
            target = out / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('public fixture')
        toolkit(self.root)
        return out

    def test_public_toolkit_is_exact_and_deterministic(self):
        toolkit(self.root)
        target = self.root / 'dist/downloads/garden-toolkit.zip'
        original = target.read_bytes()
        toolkit(self.root)
        self.assertEqual(original, target.read_bytes())
        with zipfile.ZipFile(target) as archive:
            self.assertEqual(set(archive.namelist()), set(self.manifest['toolkit_files']))
            self.assertTrue(all('internal' not in name.split('/') and 'handoffs' not in name.split('/') and 'PRIVATE' not in name for name in archive.namelist()))

    def test_new_documents_configs_runs_and_allocations_are_not_automatically_published(self):
        for name in ('docs/Future_Notes.md', 'docs/internal/DO_NOT_PUBLISH.md',
                     'docs/handoffs/continuation.md', 'research/configs/operator.json',
                     'methods/actual-allocations.csv', 'runs/trace.json', 'site/private-notes.json'):
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('synthetic private boundary sentinel')
        toolkit(self.root)
        with zipfile.ZipFile(self.root / 'dist/downloads/garden-toolkit.zip') as archive:
            self.assertEqual(set(archive.namelist()), set(self.manifest['toolkit_files']))
        self.assertEqual(set(p.relative_to(self.root).as_posix() for p in public_files(self.root, 'document_files')), set(self.manifest['document_files']))

    def test_private_traversal_duplicate_and_missing_allowlist_entries_fail_closed(self):
        original = list(self.manifest['toolkit_files'])
        for name in ('docs/internal/notes.md', 'docs/handoffs/note.md', 'runs/example.json',
                     'methods/allocations_PRIVATE.csv', '../outside.md', '/outside.md', 'missing.md'):
            with self.subTest(path=name):
                self.manifest['toolkit_files'] = sorted(original + [name])
                self.write_manifest()
                with self.assertRaises(ValueError):
                    public_files(self.root, 'toolkit_files')
        self.manifest['toolkit_files'] = sorted(original + [original[0]])
        self.write_manifest()
        with self.assertRaises(ValueError):
            public_files(self.root, 'toolkit_files')

    def test_approved_source_cannot_be_replaced_with_a_symlink(self):
        source = self.root / 'materials/Philosophy.md'
        source.unlink()
        source.symlink_to(self.root / 'materials/Philosophy.seed.md')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            public_files(self.root, 'toolkit_files')

    def test_output_and_embedded_zip_reject_unlisted_files(self):
        output = self.output()
        validate_output(self.root)
        unwanted = output / 'docs/internal/new-note.md'
        unwanted.parent.mkdir(parents=True)
        unwanted.write_text('synthetic boundary sentinel')
        with self.assertRaisesRegex(ValueError, 'output'):
            validate_output(self.root)
        unwanted.unlink()
        with zipfile.ZipFile(output / 'downloads/garden-toolkit.zip', 'a') as archive:
            archive.writestr('docs/internal/new-note.md', 'synthetic boundary sentinel')
        with self.assertRaisesRegex(ValueError, 'toolkit'):
            validate_output(self.root)

    def test_toolkit_member_bytes_must_match_selected_public_source(self):
        output = self.output()
        target = output / 'downloads/garden-toolkit.zip'
        with zipfile.ZipFile(target) as archive:
            content = {name: archive.read(name) for name in archive.namelist()}
        content['README.md'] = b'altered fixture'
        with zipfile.ZipFile(target, 'w') as archive:
            for name, data in content.items():
                archive.writestr(name, data)
        with self.assertRaisesRegex(ValueError, 'hash'):
            validate_output(self.root)


if __name__ == '__main__':
    unittest.main()
