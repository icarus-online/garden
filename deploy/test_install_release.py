import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('installer',Path(__file__).with_name('install_release.py'))
installer=importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)
REV='a'*40

def h(data): return hashlib.sha256(data).hexdigest()

class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)
        self.root=self.path/'deployment'
    def tearDown(self): self.temp.cleanup()
    def artifact(self,extra=None,revision=REV,alter_health=False):
        files={'index.html':b'The Garden','404.html':b'Not found','assets/garden.js':b'void 0;', 'assets/garden.css':b'body{}',
            'health.json':json.dumps({'status':'ok','project':'garden','source_revision':revision,'research_status':'pre-pilot_no_results','inference_enabled':alter_health}).encode()}
        manifest={'schema_version':1,'source_revision':revision,'files':{name:h(data) for name,data in files.items()}}
        files['artifact-manifest.json']=json.dumps(manifest).encode()
        stream=io.BytesIO()
        with tarfile.open(fileobj=stream,mode='w:gz') as tar:
            for name,data in files.items():
                item=tarfile.TarInfo(name);item.size=len(data);tar.addfile(item,io.BytesIO(data))
            if extra:
                info,payload=extra
                tar.addfile(info,io.BytesIO(payload) if payload else None)
        data=stream.getvalue()
        archive=self.path/'release.tar.gz';archive.write_bytes(data)
        release={'source_revision':revision,'sha256':h(data),'bytes':len(data)}
        manifest_path=self.path/'manifest.json';manifest_path.write_text(json.dumps(release))
        return archive,manifest_path,h(manifest_path.read_bytes()),revision,self.root
    def test_valid_atomic_install_preserves_previous_release(self):
        first=installer.install(*self.artifact())
        self.assertEqual((self.root/'current').readlink().as_posix(),first['current'])
        self.assertEqual(installer.verify_release(self.root/'current',REV),first['artifact_manifest_sha256'])
        second=installer.install(*self.artifact(revision='b'*40))
        self.assertEqual(second['previous'],first['current'])
        self.assertTrue((self.root/first['current']/'index.html').is_file())
        self.assertFalse(any((self.root/'releases').glob('.stage-*')))
    def test_hash_failure_never_creates_root(self):
        args=list(self.artifact());args[2]='0'*64
        with self.assertRaises(installer.InvalidRelease): installer.install(*args)
        self.assertFalse(self.root.exists())
    def test_bad_health_does_not_replace_current(self):
        first=installer.install(*self.artifact())
        with self.assertRaises(installer.InvalidRelease): installer.install(*self.artifact(revision='b'*40,alter_health=True))
        self.assertEqual((self.root/'current').readlink().as_posix(),first['current'])
    def test_traversal_links_duplicates_private_and_oversize_rejected(self):
        for attack in ('traversal','absolute','symlink','hardlink','duplicate','private','source','oversize'):
            with self.subTest(attack=attack):
                names={'traversal':'../escape.txt','absolute':'/escape.txt','symlink':'link.txt','hardlink':'hard.txt','duplicate':'index.html','private':'runs/private.json','source':'application.py','oversize':'large.txt'}
                info=tarfile.TarInfo(names[attack]);payload=b'x'
                if attack in ('symlink','hardlink'):
                    info.type=tarfile.SYMTYPE if attack=='symlink' else tarfile.LNKTYPE
                    info.linkname='../outside';payload=None
                elif attack=='oversize':
                    # Reduce the limit instead of allocating a giant fixture.
                    info.size=2;payload=b'xx'
                else: info.size=len(payload)
                args=self.artifact((info,payload))
                original=installer.MAX_FILE
                if attack=='oversize': installer.MAX_FILE=1
                try:
                    with self.assertRaises(installer.InvalidRelease): installer.install(*args)
                finally: installer.MAX_FILE=original
                self.assertFalse((self.root/'current').exists())
    def test_expanded_archive_bound_precedes_tar_metadata_parsing(self):
        args=self.artifact()
        original=installer.MAX_CONTENT
        installer.MAX_CONTENT=100
        try:
            with self.assertRaisesRegex(installer.InvalidRelease, 'Expanded archive'):
                installer.install(*args)
        finally:
            installer.MAX_CONTENT=original
        self.assertFalse(self.root.exists())
    def test_existing_release_refused(self):
        args=self.artifact();installer.install(*args)
        with self.assertRaises(installer.InvalidRelease):installer.install(*args)

if __name__=='__main__': unittest.main()
