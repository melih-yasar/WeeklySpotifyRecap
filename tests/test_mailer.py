import unittest
from unittest.mock import Mock, patch

import test_support  # noqa: F401
from weekly_spotify_recap.mailer import send_email


class MailerTests(unittest.TestCase):
    def test_send_email_logs_in_and_sends_message(self):
        server = Mock()
        context = Mock()
        context.__enter__ = Mock(return_value=server)
        context.__exit__ = Mock(return_value=None)

        with patch("weekly_spotify_recap.mailer.smtplib.SMTP_SSL", return_value=context) as smtp:
            send_email("<html>recap</html>")

        smtp.assert_called_once_with("smtp.gmail.com", 465)
        server.login.assert_called_once()
        server.send_message.assert_called_once()
        message = server.send_message.call_args.args[0]
        self.assertEqual(message["Subject"], "Your Weekly Music Recap")


if __name__ == "__main__":
    unittest.main()
