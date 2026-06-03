import unittest

import test_support
from weekly_spotify_recap.email_html import build_html_email


class EmailHtmlTests(unittest.TestCase):
    def test_build_html_email_contains_main_sections(self):
        html = build_html_email(
            test_support.sample_summary(),
            test_support.sample_enriched(),
            playlist_url="https://open.spotify.com/playlist/test",
        )

        self.assertIn("Weekly listening recap", html)
        self.assertIn("Top artists", html)
        self.assertIn("Top tracks", html)
        self.assertIn("Top albums", html)
        self.assertIn("https://open.spotify.com/playlist/test", html)

    def test_build_html_email_hides_playlist_button_without_url(self):
        with unittest.mock.patch("weekly_spotify_recap.email_html.PLAYLIST_URL", ""):
            html = build_html_email(
                test_support.sample_summary(),
                test_support.sample_enriched(),
                playlist_url="",
            )

        self.assertNotIn("Open your weekly playlist", html)


if __name__ == "__main__":
    unittest.main()
