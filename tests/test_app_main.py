import smtplib
import unittest
from unittest.mock import patch

import requests
import test_support  # noqa: F401
from weekly_spotify_recap import main


class MainFlowTests(unittest.TestCase):
    def test_main_runs_full_happy_path_with_mocks(self):
        playlist = {
            "id": "playlist-id",
            "name": "Weekly Spotify Recap",
            "url": "https://playlist",
            "track_count": 2,
        }

        with patch("weekly_spotify_recap.lastfm.get_all_tracks_last_7_days", return_value=[{"track": "data"}]):
            with patch("weekly_spotify_recap.summary.build_summary", return_value=test_support.sample_summary()):
                with patch("weekly_spotify_recap.enrichment.enrich_summary_with_spotify", return_value=test_support.sample_enriched()):
                    with patch("weekly_spotify_recap.playlist.create_or_update_weekly_playlist", return_value=playlist):
                        with patch("weekly_spotify_recap.email_html.build_html_email", return_value="<html></html>"):
                            with patch("weekly_spotify_recap.mailer.send_email") as send:
                                main.main()

        send.assert_called_once_with("<html></html>")

    def test_main_stops_when_no_tracks_found(self):
        with patch("weekly_spotify_recap.lastfm.get_all_tracks_last_7_days", return_value=[]):
            with patch("weekly_spotify_recap.mailer.send_email") as send:
                main.main()

        send.assert_not_called()

    def test_run_handles_network_error(self):
        with patch("weekly_spotify_recap.main.main", side_effect=requests.exceptions.RequestException("offline")):
            with patch("builtins.print") as print_call:
                main.run()

        self.assertIn("Network/API error:", print_call.call_args.args[0])

    def test_run_handles_smtp_authentication_error(self):
        with patch("weekly_spotify_recap.main.main", side_effect=smtplib.SMTPAuthenticationError(535, b"bad")):
            with patch("builtins.print") as print_call:
                main.run()

        self.assertIn("SMTP login failed", print_call.call_args.args[0])


if __name__ == "__main__":
    unittest.main()
