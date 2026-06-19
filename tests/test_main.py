import smtplib
import unittest
from unittest.mock import patch

import requests
import os
import sys
from pathlib import Path


SRC = Path(__file__).resolve().parents[1] / "src"

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
from weekly_spotify_recap import main


class MainTests(unittest.TestCase):
    def test_main_calls_recap_workflow(self):
        with patch("weekly_spotify_recap.main.run_recap") as run_recap:
            main.main()

        run_recap.assert_called_once_with()

    def test_run_handles_network_error(self):
        with patch("weekly_spotify_recap.main.configure_logging"):
            with patch("weekly_spotify_recap.main.main", side_effect=requests.exceptions.RequestException("offline")):
                with patch("builtins.print") as print_call:
                    with patch.object(main.LOGGER, "error") as error_log:
                        main.run()

        self.assertIn("Network/API error:", print_call.call_args.args[0])
        error_log.assert_called_once()

    def test_run_handles_smtp_authentication_error(self):
        with patch("weekly_spotify_recap.main.configure_logging"):
            with patch("weekly_spotify_recap.main.main", side_effect=smtplib.SMTPAuthenticationError(535, b"bad")):
                with patch("builtins.print") as print_call:
                    with patch.object(main.LOGGER, "error") as error_log:
                        main.run()

        self.assertIn("SMTP login failed", print_call.call_args.args[0])
        error_log.assert_called_once()


if __name__ == "__main__":
    unittest.main()

