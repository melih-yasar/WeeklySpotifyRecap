import unittest
from unittest.mock import Mock, patch

import test_support  # noqa: F401
from weekly_spotify_recap import spotify_auth


class SpotifyAuthTests(unittest.TestCase):
    def setUp(self):
        spotify_auth._spotify_app_token_cache = None
        spotify_auth._spotify_user_token_cache = None

    def test_get_spotify_app_token_caches_access_token(self):
        response = Mock()
        response.json.return_value = {"access_token": "app-token"}

        with patch("weekly_spotify_recap.spotify_auth.requests.post", return_value=response) as post:
            self.assertEqual(spotify_auth.get_spotify_app_token(), "app-token")
            self.assertEqual(spotify_auth.get_spotify_app_token(), "app-token")

        self.assertEqual(post.call_count, 1)

    def test_get_spotify_user_token_requires_refresh_token(self):
        with patch("weekly_spotify_recap.spotify_auth.SPOTIFY_REFRESH_TOKEN", ""):
            with self.assertRaises(RuntimeError):
                spotify_auth.get_spotify_user_token()


if __name__ == "__main__":
    unittest.main()
