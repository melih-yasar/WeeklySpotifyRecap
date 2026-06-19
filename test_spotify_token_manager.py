import unittest
from unittest.mock import Mock, patch

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
from weekly_spotify_recap import spotify_token_manager


class SpotifyAuthTests(unittest.TestCase):
    def setUp(self):
        spotify_token_manager._spotify_app_token_cache = None
        spotify_token_manager._spotify_user_token_cache = None

    def test_get_spotify_app_token_caches_access_token(self):
        response = Mock()
        response.json.return_value = {"access_token": "app-token"}

        with patch("weekly_spotify_recap.spotify_token_manager.requests.post", return_value=response) as post:
            self.assertEqual(spotify_token_manager.get_spotify_app_token(), "app-token")
            self.assertEqual(spotify_token_manager.get_spotify_app_token(), "app-token")

        self.assertEqual(post.call_count, 1)

    def test_get_spotify_user_token_requires_refresh_token(self):
        with patch("weekly_spotify_recap.spotify_token_manager.SPOTIFY_REFRESH_TOKEN", ""):
            with self.assertRaises(RuntimeError):
                spotify_token_manager.get_spotify_user_token()


if __name__ == "__main__":
    unittest.main()


