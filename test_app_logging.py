import tempfile
import unittest
from datetime import datetime
from pathlib import Path

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
from weekly_spotify_recap import app_logging


class AppLoggingTests(unittest.TestCase):
    def test_configure_logging_writes_expected_levels_to_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_file = Path(tmp) / "weekly_spotify_recap.log"
            app_logging.configure_logging(log_file)

            try:
                app_logging.LOGGER.info("info test")
                app_logging.LOGGER.warning("warning test")
                app_logging.LOGGER.error("error test")

                for handler in app_logging.LOGGER.handlers:
                    handler.flush()

                content = log_file.read_text(encoding="utf-8")
            finally:
                for handler in list(app_logging.LOGGER.handlers):
                    if (
                        hasattr(handler, "baseFilename")
                        and Path(handler.baseFilename) == log_file
                    ):
                        app_logging.LOGGER.removeHandler(handler)
                        handler.close()

        self.assertIn("INFO", content)
        self.assertIn("info test", content)
        self.assertIn("WARNING", content)
        self.assertIn("warning test", content)
        self.assertIn("ERROR", content)
        self.assertIn("error test", content)

    def test_logging_helpers_write_expected_messages(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_file = Path(tmp) / "weekly_spotify_recap.log"
            app_logging.configure_logging(log_file)

            try:
                app_logging.log_summary_built({"total_scrobbles": 4, "top_tracks": [1, 2]})
                app_logging.log_playlist_ready({
                    "id": "playlist-id",
                    "name": "Weekly Spotify Recap",
                    "track_count": 2,
                    "cover_uploaded": True,
                })
                app_logging.log_email_sent("recipient@example.com", "https://playlist")
                app_logging.log_run_started()
                app_logging.log_run_finished("SUCCESS")

                for handler in app_logging.LOGGER.handlers:
                    handler.flush()

                content = log_file.read_text(encoding="utf-8")
            finally:
                for handler in list(app_logging.LOGGER.handlers):
                    if (
                        hasattr(handler, "baseFilename")
                        and Path(handler.baseFilename) == log_file
                    ):
                        app_logging.LOGGER.removeHandler(handler)
                        handler.close()

        self.assertIn("Built weekly summary", content)
        self.assertIn("Spotify playlist ready", content)
        self.assertIn("Weekly Spotify recap sent", content)
        self.assertIn("Weekly Spotify Recap run started", content)
        self.assertIn("status=SUCCESS", content)

    def test_remove_old_log_entries_keeps_only_recent_entries(self):
        with tempfile.TemporaryDirectory() as tmp:
            log_file = Path(tmp) / "weekly_spotify_recap.log"
            log_file.write_text(
                "2026-06-10 09:00:00 | INFO    | old entry\n"
                "old traceback line\n"
                "2026-06-15 09:00:00 | INFO    | recent entry\n",
                encoding="utf-8",
            )

            app_logging.remove_old_log_entries(
                log_file,
                retention_days=7,
                now=datetime(2026, 6, 19, 9, 0, 0),
            )

            content = log_file.read_text(encoding="utf-8")

        self.assertNotIn("old entry", content)
        self.assertNotIn("old traceback line", content)
        self.assertIn("recent entry", content)


if __name__ == "__main__":
    unittest.main()

