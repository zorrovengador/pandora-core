"""No live profiles, credentials, network or Composio commands are used."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1] / 'skills/google-workspace-composio-policy/scripts'

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / (name + '.py'))
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

route = load('route_policy')
soul = load('sync_soul')
ID = ('tenant-qa', 'account-qa')


class RouteTests(unittest.TestCase):
    def test_cli_priority(self):
        self.assertEqual(route.choose_route('usable', ID, 'usable', ('wrong', 'wrong'))[0], 'cli')

    def test_allowed_fallback(self):
        for status in route.ALLOWED_FALLBACK:
            with self.subTest(status=status):
                self.assertEqual(route.choose_route(status, ID, 'usable', ID)[0], 'mcp')

    def test_auth_and_policy_never_fallback(self):
        for status in (*route.BLOCKED, 'unknown', None):
            with self.subTest(status=status):
                self.assertIsNone(route.choose_route(status, ID, 'usable', ID)[0])

    def test_mcp_must_be_live_and_same_tenant_account(self):
        for status, identity in [(None, ID), ('configured', ID), ('usable', None),
                                 ('usable', ('other-tenant', ID[1])),
                                 ('usable', (ID[0], 'other-account'))]:
            with self.subTest(status=status, identity=identity):
                self.assertIsNone(route.choose_route('executable_absent', ID, status, identity)[0])
        self.assertIsNone(route.choose_route('usable', None)[0])


class SoulTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='soul-qa-')
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / 'instance'
        self.home.mkdir()
        self.target = self.home / 'SOUL.md'
        self.original = 'Persona Pandora\n# Libre: texto ajeno 🐈\n'
        self.target.write_text(self.original)
        env = patch.dict(os.environ, {'HERMES_HOME': str(self.home), 'HERMES_PROFILE': 'qa'}, clear=False)
        env.start()
        self.addCleanup(env.stop)

    def test_idempotent_preserves_and_backups_with_readback(self):
        changed, backup = soul.sync(self.home, 'qa')
        self.assertTrue(changed)
        self.assertEqual(backup.read_text(), self.original)
        result = self.target.read_text()
        self.assertTrue(result.startswith(self.original))
        self.assertEqual(result.count(soul.START), 1)
        self.assertEqual(result.count(soul.END), 1)
        stamp = self.target.stat().st_mtime_ns
        self.assertEqual(soul.sync(self.home, 'qa'), (False, None))
        self.assertEqual(self.target.stat().st_mtime_ns, stamp)
        self.assertEqual(list(self.home.glob('SOUL.md.backup-*')), [backup])
        self.assertEqual(self.target.read_text(), result)
        # Update a previous bounded block, retaining unrelated text exactly.
        self.target.write_text(self.original + soul.START + '\nold rule\n' + soul.END + '\nAFTER\n')
        changed, second_backup = soul.sync(self.home, 'qa')
        self.assertTrue(changed)
        self.assertEqual(second_backup.read_text(), self.original + soul.START + '\nold rule\n' + soul.END + '\nAFTER\n')
        self.assertEqual(self.target.read_text(), self.original + soul.BLOCK + '\nAFTER\n')

    def test_mismatch_or_corruption_blocks_without_write(self):
        for profile in ('other', ''):
            with self.assertRaises(ValueError):
                soul.sync(self.home, profile)
        with patch.dict(os.environ, {'HERMES_HOME': str(self.home / 'other')}):
            with self.assertRaises(ValueError):
                soul.sync(self.home, 'qa')
        self.target.write_text(self.original + soul.START + '\n' + soul.START + '\n' + soul.END)
        with self.assertRaises(ValueError):
            soul.sync(self.home, 'qa')
        self.assertFalse(list(self.home.glob('SOUL.md.backup-*')))

    def test_symlink_and_missing_identity_block(self):
        self.target.unlink()
        outside = Path(self.temp.name) / 'outside'
        outside.write_text(self.original)
        self.target.symlink_to(outside)
        with self.assertRaises(ValueError):
            soul.sync(self.home, 'qa')
        self.assertEqual(outside.read_text(), self.original)
        with patch.dict(os.environ, {'HERMES_PROFILE': ''}):
            with self.assertRaises(ValueError):
                soul.sync(self.home, 'qa')

    def test_post_write_readback_is_executed(self):
        real = Path.read_bytes
        calls = []
        def observed(path):
            calls.append(str(path))
            return real(path)
        with patch.object(Path, 'read_bytes', observed):
            soul.sync(self.home, 'qa')
        self.assertGreaterEqual(calls.count(str(self.target)), 3)


if __name__ == '__main__':
    unittest.main()
