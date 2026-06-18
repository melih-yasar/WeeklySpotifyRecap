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
from weekly_spotify_recap import spotify_playlist


def sample_recap_summary():
    return {
        "top_tracks": [(("Artist A", "Song A"), 3), (("Artist B", "Song B"), 1)],
    }


class SpotifyPlaylistTests(unittest.TestCase):
    def test_get_top_track_uris_deduplicates_tracks(self):
        summary = {
            "top_tracks": [
                (("Artist A", "Song A"), 3),
                (("Artist B", "Song B"), 2),
                (("Artist A", "Song A"), 1),
            ]
        }

        def fake_track(_artist, title):
            return {"uri": f"spotify:track:{title[-1]}"}

        with patch("weekly_spotify_recap.spotify_playlist.find_spotify_track", side_effect=fake_track):
            uris = spotify_playlist.get_top_track_uris(summary)

        self.assertEqual(uris, ["spotify:track:A", "spotify:track:B"])

    def test_create_or_update_raises_when_no_spotify_tracks_found(self):
        summary = {"top_tracks": [(("Artist A", "Song A"), 1)]}

        with patch("weekly_spotify_recap.spotify_playlist.find_spotify_track", return_value=None):
            with self.assertRaises(RuntimeError):
                spotify_playlist.create_or_update_weekly_playlist(summary)

    def test_create_or_update_updates_playlist(self):
        with patch("weekly_spotify_recap.spotify_playlist.get_top_track_uris", return_value=["spotify:track:1"]):
            with patch("weekly_spotify_recap.spotify_playlist.get_playlist", return_value={
                "id": "playlist-id",
                "name": "Weekly Spotify Recap",
                "external_urls": {"spotify": "https://playlist"},
            }):
                with patch("weekly_spotify_recap.spotify_playlist.replace_playlist_tracks") as replace:
                    with patch("weekly_spotify_recap.spotify_playlist.upload_cover_if_available", return_value=True):
                        result = spotify_playlist.create_or_update_weekly_playlist(sample_recap_summary())

        replace.assert_called_once_with("playlist-id", ["spotify:track:1"])
        self.assertEqual(result["track_count"], 1)
        self.assertTrue(result["cover_uploaded"])

    def test_upload_cover_if_available_returns_false_when_missing(self):
        with patch("weekly_spotify_recap.spotify_playlist.PLAYLIST_COVER_PATH", "missing.jpg"):
            self.assertFalse(spotify_playlist.upload_cover_if_available("playlist-id"))


if __name__ == "__main__":
    unittest.main()


