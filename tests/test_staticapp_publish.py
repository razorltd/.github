"""Exercise the exact publisher embedded in the reusable workflow."""
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import yaml

ROOT = Path(__file__).resolve().parents[1]
workflow = yaml.safe_load((ROOT / '.github/workflows/publish-static-site.yml').read_text())
script = next(s['run'] for s in workflow['jobs']['publish']['steps'] if s.get('id') == 'publish')
code = script.split("python3 - <<'PY'\n", 1)[1].rsplit('\nPY', 1)[0]
namespace = {'__name__': 'publisher_test'}
exec(compile(code, 'embedded_publisher', 'exec'), namespace)
publish, validate = namespace['publish'], namespace['validate']


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'sites'
        self.root.mkdir()
        self.source = Path(self.temp.name) / 'artifact'
        self.source.mkdir()
        (self.source / 'index.html').write_text('first')

    def deploy(self, run=100, attempt=1):
        return publish(self.source, self.root, 'pilot', run, attempt, 'abc123')

    def require_symlinks(self):
        probe = Path(self.temp.name) / 'probe'
        try:
            probe.symlink_to(self.source, target_is_directory=True)
            probe.unlink()
        except OSError:
            self.skipTest('Host cannot create symlinks; Linux CI runs this test')

    def test_rejects_missing_index_and_hidden_files(self):
        (self.source / 'index.html').unlink()
        with self.assertRaises(ValueError): validate(self.source)
        (self.source / 'index.html').write_text('ok')
        (self.source / '.env').write_text('private')
        with self.assertRaises(ValueError): validate(self.source)

    def test_rejects_site_path_traversal(self):
        with self.assertRaises(ValueError):
            publish(self.source, self.root, '../other', 1, 1, 'abc')
        self.assertEqual(list(self.root.iterdir()), [])

    def test_rejects_artifact_symlink(self):
        self.require_symlinks()
        (self.source / 'escape').symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError): validate(self.source)

    def test_switch_preserves_old_release_and_blocks_stale_runs(self):
        self.require_symlinks()
        self.deploy()
        (self.source / 'index.html').write_text('second')
        self.deploy(101)
        self.assertEqual((self.root / 'pilot/current/index.html').read_text(), 'second')
        self.assertEqual((self.root / 'pilot/releases/100-1/index.html').read_text(), 'first')
        with self.assertRaises(ValueError): self.deploy(100)
        with self.assertRaises(ValueError): self.deploy(101)
        self.deploy(101, 2)

    def test_failed_copy_keeps_current_and_cleans_staging(self):
        self.require_symlinks()
        self.deploy()
        original = shutil.copytree
        def fail(source, target):
            original(source, target)
            raise OSError('simulated storage failure')
        with patch.object(namespace['shutil'], 'copytree', side_effect=fail):
            with self.assertRaises(OSError): self.deploy(101)
        self.assertEqual((self.root / 'pilot/current/index.html').read_text(), 'first')
        self.assertEqual(list((self.root / 'pilot/releases').glob('.staging-*')), [])

    def test_external_current_pointer_rejected(self):
        self.require_symlinks()
        directory = self.root / 'pilot'
        directory.mkdir()
        (directory / 'current').symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(ValueError): self.deploy()


if __name__ == '__main__':
    unittest.main()
