import importlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import os
import sys
from pathlib import Path


SRC = Path(__file__).resolve().parent / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

TEST_ENV = {
    "LASTFM_API_KEY": "test-lastfm-key",
    "LASTFM_USERNAME": "test-user",
    "SPOTIFY_CLIENT_ID": "test-client-id",
    "SPOTIFY_CLIENT_SECRET": "test-client-secret",
    "SPOTIFY_REFRESH_TOKEN": "test-refresh-token",
    "SPOTIFY_PLAYLIST_ID": "test-playlist-id",
    "SPOTIFY_PLAYLIST_NAME": "Weekly Spotify Recap",
    "GMAIL_ADDRESS": "sender@example.com",
    "GMAIL_APP_PASSWORD": "test-app-password",
    "RECIPIENT_EMAIL": "recipient@example.com",
    "PLAYLIST_URL": "https://open.spotify.com/playlist/test",
    "PLAYLIST_COVER_PATH": "assets/playlist-cover.jpg",
}

for key, value in TEST_ENV.items():
    os.environ[key] = value
from weekly_spotify_recap import config


def apply_test_env():
    for key, value in TEST_ENV.items():
        os.environ[key] = value


class ConfigTests(unittest.TestCase):
    def tearDown(self):
        apply_test_env()

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
        self.assertEqual(reloaded.LASTFM_API_KEY, TEST_ENV["LASTFM_API_KEY"])


if __name__ == "__main__":
    unittest.main()


