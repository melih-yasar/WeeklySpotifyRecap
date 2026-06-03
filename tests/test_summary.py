from datetime import datetime, timezone
import unittest

import test_support  # noqa: F401
from weekly_spotify_recap.summary import build_summary


class SummaryTests(unittest.TestCase):
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
