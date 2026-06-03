import unittest
from unittest.mock import patch

import test_support
from weekly_spotify_recap.enrichment import enrich_summary_with_spotify


class EnrichmentTests(unittest.TestCase):
    def test_enrich_summary_with_spotify_builds_sections(self):
        with patch("weekly_spotify_recap.enrichment.find_spotify_track", return_value={
            "spotify_url": "https://track",
            "album_cover_url": "https://cover",
        }):
            with patch("weekly_spotify_recap.enrichment.find_spotify_album", return_value={
                "spotify_url": "https://album",
                "image_url": "https://album-cover",
            }):
                with patch("weekly_spotify_recap.enrichment.find_spotify_artist", return_value={
                    "spotify_url": "https://artist",
                    "image_url": "https://artist-image",
                }):
                    enriched = enrich_summary_with_spotify(test_support.sample_summary())

        self.assertEqual(enriched["hero"]["cover_url"], "https://cover")
        self.assertEqual(enriched["artists"][0]["image_url"], "https://artist-image")
        self.assertEqual(enriched["tracks"][0]["spotify_url"], "https://track")
        self.assertEqual(enriched["albums"][0]["cover_url"], "https://album-cover")


if __name__ == "__main__":
    unittest.main()
