from datetime import datetime, timedelta, timezone
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
from weekly_spotify_recap import lastfm_client


class LastFmClientTests(unittest.TestCase):
    def test_lastfm_get_returns_json_happy_path(self):
        response = Mock()
        response.json.return_value = {"recenttracks": {"track": []}}

        with patch("weekly_spotify_recap.lastfm_client.requests.get", return_value=response):
            data = lastfm_client.lastfm_get({"method": "test"})

        self.assertIn("recenttracks", data)
        response.raise_for_status.assert_called_once_with()

    def test_lastfm_get_raises_for_api_error_body(self):
        response = Mock()
        response.json.return_value = {"error": 6, "message": "Invalid parameters"}

        with patch("weekly_spotify_recap.lastfm_client.requests.get", return_value=response):
            with self.assertRaises(RuntimeError):
                lastfm_client.lastfm_get({"method": "test"})

    def test_get_recent_tracks_page_builds_lastfm_params(self):
        with patch("weekly_spotify_recap.lastfm_client.lastfm_get", return_value={}) as call:
            lastfm_client.get_recent_tracks_page(page=2, limit=50)

        params = call.call_args.args[0]
        self.assertEqual(params["method"], "user.getrecenttracks")
        self.assertEqual(params["page"], 2)
        self.assertEqual(params["limit"], 50)

    def test_get_all_tracks_last_7_days_filters_old_tracks(self):
        now = datetime.now(timezone.utc)
        fresh = int((now - timedelta(days=1)).timestamp())
        old = int((now - timedelta(days=10)).timestamp())
        page = {
            "recenttracks": {
                "track": [
                    {
                        "artist": {"#text": " Artist A "},
                        "name": " Song A ",
                        "album": {"#text": ""},
                        "date": {"uts": str(fresh)},
                    },
                    {
                        "artist": {"#text": "Old Artist"},
                        "name": "Old Song",
                        "album": {"#text": "Old Album"},
                        "date": {"uts": str(old)},
                    },
                ],
                "@attr": {"totalPages": "1"},
            }
        }

        with patch("weekly_spotify_recap.lastfm_client.get_recent_tracks_page", return_value=page):
            tracks = lastfm_client.get_all_tracks_last_7_days()

        self.assertEqual(len(tracks), 1)
        self.assertEqual(tracks[0]["artist"], "Artist A")
        self.assertEqual(tracks[0]["album"], "Unknown Album")


if __name__ == "__main__":
    unittest.main()


