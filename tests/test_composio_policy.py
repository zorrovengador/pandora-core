"""Regression tests; integration cases use the installed Hermes distribution API.
Run: PYTHONPATH=/path/to/hermes /path/to/hermes/.venv/bin/python -m unittest discover -s tests -v
All profiles and tenant fixtures stay in temporary directories, never live profiles.
"""
import copy
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path('skills/google-workspace-composio-policy')
spec = importlib.util.spec_from_file_location('route_diagnose', ROOT / SKILL / 'scripts/diagnose.py')
diag = importlib.util.module_from_spec(spec)
spec.loader.exec_module(diag)
NOW = datetime(2026, 1, 1, tzinfo=timezone.utc)


def fixture(route='connector'):
    return {'schema_version': 1, 'instance_id': 'qa-instance',
            'composio_account_id': 'qa-account', 'composio_project_id': 'qa-project',
            'google_account': 'qa@example.invalid', 'route': route,
            'services': {'drive': {'connection_id': 'qa-connection',
              'google_account': 'qa@example.invalid', 'status': 'verified_read',
              'verified_at': NOW.isoformat(), 'evidence_ref': 'qa-synthetic-fixture'}}}


class DiagnosticTests(unittest.TestCase):
    def check(self, record, route=None, cli=False, service='drive', instance='qa-instance'):
        return diag.diagnose(record, instance, service, now=NOW, cli_present=cli)

    def test_connector_without_cli(self):
        out = self.check(fixture())
        self.assertEqual(out['status'], 'recent_recorded_evidence')
        self.assertFalse(out['live_verified'])

    def test_mcp_without_cli(self):
        self.assertEqual(self.check(fixture('mcp'))['status'], 'recent_recorded_evidence')

    def test_cli_independent_of_mcp(self):
        self.assertEqual(self.check(fixture('cli'), cli=True)['status'], 'recent_recorded_evidence')
        self.assertEqual(self.check(fixture('cli'))['reason'], 'selected_cli_missing')

    def test_absent_is_pending_not_unavailable(self):
        self.assertEqual(self.check(None)['status'], 'pending')

    def test_unverified_services_pending(self):
        self.assertEqual(self.check(fixture(), service='gmail')['status'], 'pending')

    def test_wrong_instance(self):
        self.assertEqual(self.check(fixture(), instance='other')['reason'], 'instance_mismatch')

    def test_wrong_google_account(self):
        record = fixture()
        record['services']['drive']['google_account'] = 'other@example.invalid'
        self.assertEqual(self.check(record)['reason'], 'google_account_mismatch')

    def test_stale_future_naive_bad_time(self):
        for at in [(NOW-timedelta(days=2)).isoformat(), (NOW+timedelta(seconds=1)).isoformat(),
                   '2026-01-01T00:00:00', None, 'not-time']:
            record = fixture()
            record['services']['drive']['verified_at'] = at
            self.assertEqual(self.check(record)['status'], 'pending')

    def test_no_secret_fields_or_echo(self):
        record = fixture()
        record['token'] = 'synthetic-test-only'
        out = self.check(record)
        self.assertEqual(out['reason'], 'record_schema_invalid')
        self.assertNotIn('synthetic-test-only', json.dumps(out))

    def test_malformed_route_and_service(self):
        for route in ['google-direct', [], None]:
            record = fixture()
            record['route'] = route
            self.assertEqual(self.check(record)['status'], 'pending')
        record = fixture()
        record['services']['unknown'] = {}
        self.assertEqual(self.check(record)['status'], 'pending')

    def test_no_evidence_or_connection(self):
        for key in ['connection_id', 'evidence_ref']:
            record = fixture()
            record['services']['drive'][key] = ''
            self.assertEqual(self.check(record)['status'], 'pending')


class DistributionTests(unittest.TestCase):
    def setUp(self):
        from hermes_cli import profile_distribution as distribution
        self.distribution = distribution
        self.tmp = tempfile.TemporaryDirectory(prefix='pandora-core-test-')
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.source = self.base / 'source'
        shutil.copytree(ROOT, self.source, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        # Isolate the REAL install/update API's profile-root resolver.
        self.root_patch = patch('hermes_cli.profiles._get_profiles_root', return_value=self.base/'profiles')
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def install(self):
        plan = self.distribution.install_distribution(str(self.source), name='policy-qa')
        self.assertTrue(plan.target_dir.is_relative_to(self.base))
        return plan.target_dir

    def test_fresh_install_full_policy_no_auth(self):
        target = self.install()
        for file in ['SKILL.md', 'scripts/diagnose.py', 'references/route-record.md']:
            self.assertTrue((target/SKILL/file).is_file())
        self.assertIn('exclusivamente por Composio', (target/'SOUL.md').read_text())
        self.assertTrue((target/'config.yaml').is_file())
        for name in ['.env', 'auth.json', 'integrations/composio-google.json', 'mcp.json']:
            self.assertFalse((target/name).exists(), name)

    def test_upgrade_from_previous_version_preserves_tenant(self):
        # Simulate v1.0.0 payload from before this component existed.
        shutil.rmtree(self.source/SKILL)
        manifest = self.source/'distribution.yaml'
        manifest.write_text(manifest.read_text().replace('version: 1.1.0', 'version: 1.0.0').replace('  - config.yaml', '  - mcp.json'))
        target = self.install()
        self.assertFalse((target/SKILL).exists())
        tenant = {
          '.env': 'QA_SENTINEL=synthetic-only\n',
          'auth.json': '{"qa":"synthetic-only"}',
          'config.yaml': '_config_version: 33\n# tenant override\n',
          'mcp.json': '{"mcpServers":{"tenant_owned":{"command":"qa-placeholder"}}}',
          'integrations/composio-google.json': json.dumps(fixture('cli')),
          'memories/MEMORY.md': 'QA memory', 'sessions/qa.jsonl': '{}\n',
          'cron/jobs.json': '{"jobs": []}', 'skills/tenant-extra/SKILL.md': '# tenant skill',
          'workspace/qa.txt': 'QA workspace', 'state.db': 'QA sentinel, not sqlite'
        }
        for name, text in tenant.items():
            path = target/name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        shutil.copytree(ROOT/SKILL, self.source/SKILL)
        manifest.write_text((ROOT/'distribution.yaml').read_text())
        for _ in range(2):  # upgrade and idempotent re-run
            plan = self.distribution.update_distribution('policy-qa')
            self.assertEqual(plan.manifest.version, '1.1.0')
            self.assertTrue((target/SKILL/'scripts/diagnose.py').exists())
            for name, text in tenant.items():
                self.assertEqual((target/name).read_text(), text, name)


if __name__ == '__main__':
    unittest.main()
