import unittest
from unittest.mock import Mock, patch

import requests
import test_support  # noqa: F401
from weekly_spotify_recap import spotify_api


class SpotifyApiTests(unittest.TestCase):
    def test_spotify_request_raises_clear_error_for_403(self):
        response = Mock(status_code=403, text="Forbidden")
        response.json.return_value = {"error": {"message": "Forbidden"}}

        with patch("weekly_spotify_recap.spotify_api.get_spotify_user_token", return_value="token"):
            with patch("weekly_spotify_recap.spotify_api.requests.request", return_value=response):
                with self.assertRaises(RuntimeError):
                    spotify_api.spotify_request("PUT", "/playlists/id/items")

    def test_spotify_request_wraps_http_error_details(self):
        response = Mock(status_code=400, text="Bad request")
        response.json.side_effect = ValueError()
        response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        with patch("weekly_spotify_recap.spotify_api.get_spotify_user_token", return_value="token"):
            with patch("weekly_spotify_recap.spotify_api.requests.request", return_value=response):
                with self.assertRaises(RuntimeError):
                    spotify_api.spotify_request("GET", "/bad")

    def test_upload_playlist_cover_uses_image_endpoint(self):
        with patch("weekly_spotify_recap.spotify_api.spotify_request") as request:
            spotify_api.upload_playlist_cover_image("playlist-id", "base64")

        request.assert_called_once_with(
            "PUT",
            "/playlists/playlist-id/images",
            data="base64",
            content_type="image/jpeg",
        )


if __name__ == "__main__":
    unittest.main()
