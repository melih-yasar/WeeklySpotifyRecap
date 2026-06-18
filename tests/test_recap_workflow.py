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
from weekly_spotify_recap import recap_workflow


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
        "hero": {"cover_url": "https://example.com/cover.jpg"},
        "artists": [],
        "tracks": [],
        "albums": [],
    }


class RecapWorkflowTests(unittest.TestCase):
    def test_run_recap_runs_full_happy_path_with_mocks(self):
        playlist = {
            "id": "playlist-id",
            "name": "Weekly Spotify Recap",
            "url": "https://playlist",
            "track_count": 2,
        }

        with patch("weekly_spotify_recap.lastfm_client.get_all_tracks_last_7_days", return_value=[{"track": "data"}]):
            with patch("weekly_spotify_recap.recap_summary.build_summary", return_value=sample_recap_summary()):
                with patch("weekly_spotify_recap.spotify_enrichment.enrich_summary_with_spotify", return_value=sample_enriched()):
                    with patch("weekly_spotify_recap.spotify_playlist.create_or_update_weekly_playlist", return_value=playlist):
                        with patch("weekly_spotify_recap.recap_email_builder.build_html_email", return_value="<html></html>"):
                            with patch("weekly_spotify_recap.email_sender.send_email") as send:
                                recap_workflow.run_recap()

        send.assert_called_once_with("<html></html>")

    def test_run_recap_stops_when_no_tracks_found(self):
        with patch("weekly_spotify_recap.lastfm_client.get_all_tracks_last_7_days", return_value=[]):
            with patch("weekly_spotify_recap.email_sender.send_email") as send:
                with patch.object(recap_workflow.LOGGER, "warning") as warning_log:
                    recap_workflow.run_recap()

        send.assert_not_called()
        warning_log.assert_called_with("No scrobbles found in the last 7 days.")


if __name__ == "__main__":
    unittest.main()

