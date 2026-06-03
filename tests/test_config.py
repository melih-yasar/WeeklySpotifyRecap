import importlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import test_support
from weekly_spotify_recap import config


class ConfigTests(unittest.TestCase):
    def tearDown(self):
        test_support.apply_test_env()

    def test_required_env_returns_existing_value(self):
        os.environ["SAMPLE_ENV"] = "value"
        self.assertEqual(config.required_env("SAMPLE_ENV"), "value")

    def test_required_env_raises_for_missing_value(self):
        os.environ.pop("MISSING_ENV", None)
        with self.assertRaises(RuntimeError):
            config.required_env("MISSING_ENV")

    def test_load_dotenv_reads_key_value_pairs(self):
        with tempfile.TemporaryDirectory() as tmp:
            env_file = Path(tmp) / ".env"
            env_file.write_text("NEW_KEY='new-value'\n# ignored\nBROKEN\n", encoding="utf-8")
            os.environ.pop("NEW_KEY", None)

            with patch.object(config.Path, "cwd", return_value=Path(tmp)):
                config.load_dotenv()

        self.assertEqual(os.environ["NEW_KEY"], "new-value")

    def test_config_module_imports_with_test_environment(self):
        reloaded = importlib.reload(config)
        self.assertEqual(reloaded.LASTFM_API_KEY, test_support.TEST_ENV["LASTFM_API_KEY"])


if __name__ == "__main__":
    unittest.main()
