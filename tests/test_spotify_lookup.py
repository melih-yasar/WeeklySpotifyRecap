import unittest
from unittest.mock import patch

import test_support  # noqa: F401
from weekly_spotify_recap import spotify_lookup


class SpotifyLookupTests(unittest.TestCase):
    def test_find_spotify_track_returns_matching_track(self):
        data = {
            "tracks": {
                "items": [{
                    "name": "Song A",
                    "uri": "spotify:track:1",
                    "external_urls": {"spotify": "https://track"},
                    "artists": [{"name": "Artist A"}],
                    "album": {"name": "Album A", "images": [{"url": "https://cover"}]},
                }]
            }
        }

        with patch("weekly_spotify_recap.spotify_lookup.spotify_search", return_value=data):
            track = spotify_lookup.find_spotify_track("artist a", "song a")

        self.assertEqual(track["uri"], "spotify:track:1")
        self.assertEqual(track["album_cover_url"], "https://cover")

    def test_find_spotify_track_returns_none_without_match(self):
        data = {"tracks": {"items": [{"name": "Other", "artists": []}]}}

        with patch("weekly_spotify_recap.spotify_lookup.spotify_search", return_value=data):
            track = spotify_lookup.find_spotify_track("Artist A", "Song A")

        self.assertIsNone(track)


if __name__ == "__main__":
    unittest.main()
