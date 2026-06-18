import unittest
from unittest.mock import Mock, patch

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
from weekly_spotify_recap import spotify_api_client


class SpotifyApiTests(unittest.TestCase):
    def test_spotify_request_raises_clear_error_for_403(self):
        response = Mock(status_code=403, text="Forbidden")
        response.json.return_value = {"error": {"message": "Forbidden"}}

        with patch("weekly_spotify_recap.spotify_api_client.get_spotify_user_token", return_value="token"):
            with patch("weekly_spotify_recap.spotify_api_client.requests.request", return_value=response):
                with self.assertRaises(RuntimeError):
                    spotify_api_client.spotify_request("PUT", "/playlists/id/items")

    def test_spotify_request_wraps_http_error_details(self):
        response = Mock(status_code=400, text="Bad request")
        response.json.side_effect = ValueError()
        response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        with patch("weekly_spotify_recap.spotify_api_client.get_spotify_user_token", return_value="token"):
            with patch("weekly_spotify_recap.spotify_api_client.requests.request", return_value=response):
                with self.assertRaises(RuntimeError):
                    spotify_api_client.spotify_request("GET", "/bad")

    def test_upload_playlist_cover_uses_image_endpoint(self):
        with patch("weekly_spotify_recap.spotify_api_client.spotify_request") as request:
            spotify_api_client.upload_playlist_cover_image("playlist-id", "base64")

        request.assert_called_once_with(
            "PUT",
            "/playlists/playlist-id/images",
            data="base64",
            content_type="image/jpeg",
        )


if __name__ == "__main__":
    unittest.main()


