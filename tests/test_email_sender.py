import unittest
from unittest.mock import Mock, patch

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
from weekly_spotify_recap.email_sender import send_email


class EmailSenderTests(unittest.TestCase):
    def test_send_email_logs_in_and_sends_message(self):
        server = Mock()
        context = Mock()
        context.__enter__ = Mock(return_value=server)
        context.__exit__ = Mock(return_value=None)

        with patch("weekly_spotify_recap.email_sender.smtplib.SMTP_SSL", return_value=context) as smtp:
            send_email("<html>recap</html>")

        smtp.assert_called_once_with("smtp.gmail.com", 465)
        server.login.assert_called_once()
        server.send_message.assert_called_once()
        message = server.send_message.call_args.args[0]
        self.assertEqual(message["Subject"], "Your Weekly Music Recap")


if __name__ == "__main__":
    unittest.main()


