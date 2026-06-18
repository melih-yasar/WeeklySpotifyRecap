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
from weekly_spotify_recap.recap_email_builder import build_html_email


def sample_recap_summary():
    return {
        "total_scrobbles": 4,
        "top_artists": [("Artist A", 3), ("Artist B", 1)],
        "top_tracks": [(("Artist A", "Song A"), 3), (("Artist B", "Song B"), 1)],
        "top_albums": [(("Artist A", "Album A"), 3)],
        "busiest_day": ("Monday", 4),
        "favorite_hour": 9,
        "latest_track": {"artist": "Artist A", "title": "Song A", "album": "Album A"},
        "raw_tracks": [{"artist": "Artist A", "title": "Song A", "album": "Album A"}],
    }


def sample_enriched():
    return {
        "hero": {
            "artist": "Artist A",
            "title": "Song A",
            "album": "Album A",
            "cover_url": "https://example.com/cover.jpg",
            "spotify_url": "https://open.spotify.com/track/test",
        },
        "artists": [{
            "artist": "Artist A",
            "plays": 3,
            "image_url": "https://example.com/artist.jpg",
            "spotify_url": "https://open.spotify.com/artist/test",
        }],
        "tracks": [{
            "artist": "Artist A",
            "title": "Song A",
            "album": "Album A",
            "plays": 3,
            "cover_url": "https://example.com/cover.jpg",
            "spotify_url": "https://open.spotify.com/track/test",
        }],
        "albums": [{
            "artist": "Artist A",
            "album": "Album A",
            "plays": 3,
            "cover_url": "https://example.com/album.jpg",
            "spotify_url": "https://open.spotify.com/album/test",
        }],
    }


class EmailHtmlTests(unittest.TestCase):
    def test_build_html_email_contains_main_sections(self):
        html = build_html_email(
            sample_recap_summary(),
            sample_enriched(),
            playlist_url="https://open.spotify.com/playlist/test",
        )

        self.assertIn("Weekly listening recap", html)
        self.assertIn("Top artists", html)
        self.assertIn("Top tracks", html)
        self.assertIn("Top albums", html)
        self.assertIn("https://open.spotify.com/playlist/test", html)

    def test_build_html_email_hides_playlist_button_without_url(self):
        with unittest.mock.patch("weekly_spotify_recap.recap_email_builder.PLAYLIST_URL", ""):
            html = build_html_email(
                sample_recap_summary(),
                sample_enriched(),
                playlist_url="",
            )

        self.assertNotIn("Open your weekly playlist", html)


if __name__ == "__main__":
    unittest.main()


