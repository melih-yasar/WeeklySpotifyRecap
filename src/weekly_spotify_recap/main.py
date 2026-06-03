import smtplib

import requests

if not __package__:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    __package__ = "weekly_spotify_recap"


def main():
    tracks = load_tracks()

    if not tracks:
        return

    summary = build_weekly_summary(tracks)
    enriched = load_spotify_email_data(summary)
    playlist = update_playlist(summary)
    send_recap_email(summary, enriched, playlist)

    print("Done.")


def load_tracks():
    from .lastfm import get_all_tracks_last_7_days

    print("Loading Last.fm data...")
    tracks = get_all_tracks_last_7_days()

    if not tracks:
        print("No scrobbles found in the last 7 days.")

    return tracks


def build_weekly_summary(tracks):
    from .summary import build_summary

    print("Building summary...")
    return build_summary(tracks)


def load_spotify_email_data(summary):
    from .enrichment import enrich_summary_with_spotify

    print("Loading Spotify images and links...")
    return enrich_summary_with_spotify(summary)


def update_playlist(summary):
    from .playlist import create_or_update_weekly_playlist

    print("Creating/updating Spotify playlist...")
    playlist = create_or_update_weekly_playlist(summary)
    print(f"Playlist ready: {playlist['name']} ({playlist['track_count']} tracks)")
    return playlist


def send_recap_email(summary, enriched, playlist):
    from .config import RECIPIENT_EMAIL
    from .email_html import build_html_email
    from .mailer import send_email

    print("Building email...")
    html = build_html_email(summary, enriched, playlist_url=playlist["url"])

    print("Sending email...")
    send_email(html)

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
