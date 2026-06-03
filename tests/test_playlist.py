import unittest
from unittest.mock import patch

import test_support
from weekly_spotify_recap import playlist


class PlaylistTests(unittest.TestCase):
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

        with patch("weekly_spotify_recap.playlist.find_spotify_track", side_effect=fake_track):
            uris = playlist.get_top_track_uris(summary)

        self.assertEqual(uris, ["spotify:track:A", "spotify:track:B"])

    def test_create_or_update_raises_when_no_spotify_tracks_found(self):
        summary = {"top_tracks": [(("Artist A", "Song A"), 1)]}

        with patch("weekly_spotify_recap.playlist.find_spotify_track", return_value=None):
            with self.assertRaises(RuntimeError):
                playlist.create_or_update_weekly_playlist(summary)

    def test_create_or_update_updates_playlist(self):
        with patch("weekly_spotify_recap.playlist.get_top_track_uris", return_value=["spotify:track:1"]):
            with patch("weekly_spotify_recap.playlist.get_playlist", return_value={
                "id": "playlist-id",
                "name": "Weekly Spotify Recap",
                "external_urls": {"spotify": "https://playlist"},
            }):
                with patch("weekly_spotify_recap.playlist.replace_playlist_tracks") as replace:
                    with patch("weekly_spotify_recap.playlist.upload_cover_if_available", return_value=True):
                        result = playlist.create_or_update_weekly_playlist(test_support.sample_summary())

        replace.assert_called_once_with("playlist-id", ["spotify:track:1"])
        self.assertEqual(result["track_count"], 1)
        self.assertTrue(result["cover_uploaded"])

    def test_upload_cover_if_available_returns_false_when_missing(self):
        with patch("weekly_spotify_recap.playlist.PLAYLIST_COVER_PATH", "missing.jpg"):
            self.assertFalse(playlist.upload_cover_if_available("playlist-id"))


if __name__ == "__main__":
    unittest.main()
