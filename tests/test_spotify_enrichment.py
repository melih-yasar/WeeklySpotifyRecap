import unittest
from unittest.mock import patch

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
from weekly_spotify_recap.spotify_enrichment import enrich_summary_with_spotify


def sample_recap_summary():
    return {
        "total_scrobbles": 4,
        "top_artists": [("Artist A", 3), ("Artist B", 1)],
        "top_tracks": [(("Artist A", "Song A"), 3), (("Artist B", "Song B"), 1)],
        "top_albums": [(("Artist A", "Album A"), 3)],
        "busiest_day": ("Monday", 4),
        "favorite_hour": 9,
        "latest_track": {"artist": "Artist A", "title": "Song A", "album": "Album A"},
        "raw_tracks": [
            {"artist": "Artist A", "title": "Song A", "album": "Album A"},
            {"artist": "Artist B", "title": "Song B", "album": "Album B"},
        ],
    }


class SpotifyEnrichmentTests(unittest.TestCase):
    def test_enrich_summary_with_spotify_builds_sections(self):
        with patch("weekly_spotify_recap.spotify_enrichment.find_spotify_track", return_value={
            "spotify_url": "https://track",
            "album_cover_url": "https://cover",
        }):
            with patch("weekly_spotify_recap.spotify_enrichment.find_spotify_album", return_value={
                "spotify_url": "https://album",
                "image_url": "https://album-cover",
            }):
                with patch("weekly_spotify_recap.spotify_enrichment.find_spotify_artist", return_value={
                    "spotify_url": "https://artist",
                    "image_url": "https://artist-image",
                }):
                    enriched = enrich_summary_with_spotify(sample_recap_summary())

        self.assertEqual(enriched["hero"]["cover_url"], "https://cover")
        self.assertEqual(enriched["artists"][0]["image_url"], "https://artist-image")
        self.assertEqual(enriched["tracks"][0]["spotify_url"], "https://track")
        self.assertEqual(enriched["albums"][0]["cover_url"], "https://album-cover")


if __name__ == "__main__":
    unittest.main()


