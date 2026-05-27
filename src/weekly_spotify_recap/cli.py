import smtplib

import requests


def main():
    from .config import RECIPIENT_EMAIL
    from .email_html import build_html_email
    from .enrichment import enrich_summary_with_spotify
    from .lastfm import get_all_tracks_last_7_days
    from .mailer import send_email
    from .summary import build_summary

    print("Loading Last.fm data...")
    tracks = get_all_tracks_last_7_days()

    if not tracks:
        print("No scrobbles found in the last 7 days.")
        return

    print("Building summary...")
    summary = build_summary(tracks)

    print("Loading Spotify images and links...")
    enriched = enrich_summary_with_spotify(summary)

    print("Building email...")
    html = build_html_email(summary, enriched)

    print("Sending email...")
    send_email(html)

    print("Done.")
    print(f"Sent to: {RECIPIENT_EMAIL}")


def run():
    try:
        main()

    except requests.exceptions.RequestException as e:
        print("Network/API error:", e)

    except RuntimeError as e:
        print("Runtime error:", e)

    except smtplib.SMTPAuthenticationError:
        print("SMTP login failed. Check Gmail address and app password.")

    except Exception as e:
        print("Unexpected error:", e)


if __name__ == "__main__":
    run()
