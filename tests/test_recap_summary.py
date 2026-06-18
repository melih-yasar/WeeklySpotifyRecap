from datetime import datetime, timezone
import unittest

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
from weekly_spotify_recap.recap_summary import build_summary


class RecapSummaryTests(unittest.TestCase):
    def test_build_summary_counts_weekly_statistics(self):
        played_at = datetime(2026, 6, 1, 9, tzinfo=timezone.utc)
        tracks = [
            {"artist": "A", "title": "Song 1", "album": "Album 1", "played_at": played_at},
            {"artist": "A", "title": "Song 1", "album": "Album 1", "played_at": played_at},
            {"artist": "B", "title": "Song 2", "album": "Album 2", "played_at": played_at},
        ]

        summary = build_summary(tracks)

        self.assertEqual(summary["total_scrobbles"], 3)
        self.assertEqual(summary["top_artists"][0], ("A", 2))
        self.assertEqual(summary["top_tracks"][0], (("A", "Song 1"), 2))
        self.assertEqual(summary["favorite_hour"], 9)

    def test_build_summary_handles_empty_tracks(self):
        summary = build_summary([])

        self.assertEqual(summary["total_scrobbles"], 0)
        self.assertEqual(summary["busiest_day"], ("Unknown", 0))
        self.assertIsNone(summary["favorite_hour"])
        self.assertIsNone(summary["latest_track"])


if __name__ == "__main__":
    unittest.main()


