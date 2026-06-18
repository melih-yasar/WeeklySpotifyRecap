"""Main program flow for the Weekly Spotify Recap app."""

import smtplib
from pathlib import Path

import requests

if not __package__:
    import sys

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    __package__ = "weekly_spotify_recap"


from .app_logging import (
    LOGGER,
    configure_logging,
)
from .recap_workflow import run_recap


def main():
    """Run the complete recap workflow."""
    run_recap()


def run():
    """Run the app and print readable messages for important errors."""
    configure_logging()

    try:
        main()

    except requests.exceptions.RequestException as e:
        LOGGER.error("Network/API error while running weekly recap.", exc_info=True)
        print("Network/API error:", e)

    except RuntimeError as e:
        LOGGER.error("Runtime error while running weekly recap.", exc_info=True)
        print("Runtime error:", e)

    except smtplib.SMTPAuthenticationError:
        LOGGER.error("SMTP login failed while sending weekly recap.", exc_info=True)
        print("SMTP login failed. Check Gmail address and app password.")

    except Exception as e:
        LOGGER.exception("Unexpected error while running weekly recap.")
        print("Unexpected error:", e)


if __name__ == "__main__":
    run()

