import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class PreprovisionedCredentialsContractTests(unittest.TestCase):
    def test_distribution_declares_no_runtime_secret_requirement(self):
        content = (ROOT / 'distribution.yaml').read_text()
        self.assertNotIn('env_requires:', content)
        self.assertIn('se aprovisionan antes de instalar', content)

    def test_onboarding_never_starts_credential_setup(self):
        content = (ROOT / 'skills/bizbrain-onboarding/SKILL.md').read_text()
        self.assertIn('bloqueado por aprovisionamiento', content)
        self.assertIn('no dirijas OAuth', content)
        self.assertIn('no solicites ni configures API keys', content)

    def test_connection_skill_operates_only_preprovisioned_connections(self):
        content = (ROOT / 'skills/composio-tenant-connections/SKILL.md').read_text()
        self.assertIn('conexiones ya aprovisionadas', content)
        self.assertIn('No lo uses para iniciar OAuth', content)
        self.assertIn('No inicies OAuth ni pidas secretos', content)


if __name__ == '__main__':
    unittest.main()
