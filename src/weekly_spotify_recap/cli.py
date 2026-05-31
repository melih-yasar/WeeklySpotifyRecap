import logging
import smtplib
from pathlib import Path

import requests


def setup_logging():
    log_dir = Path.cwd() / "logs"
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        filename=log_dir / "weekly_spotify_recap.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def main():
    logging.info("Weekly Spotify recap started.")

    from .config import RECIPIENT_EMAIL
    from .email_html import build_html_email
    from .enrichment import enrich_summary_with_spotify
    from .lastfm import get_all_tracks_last_7_days
    from .mailer import send_email
    from .outputs import append_run_history, save_html_preview, save_text_summary
    from .playlist import create_or_update_weekly_playlist
    from .summary import build_summary

    print("Loading Last.fm data...")
    tracks = get_all_tracks_last_7_days()

    if not tracks:
        print("No scrobbles found in the last 7 days.")
        logging.info("No scrobbles found in the last 7 days.")
        return

    print("Building summary...")
    summary = build_summary(tracks)

    print("Loading Spotify images and links...")
    enriched = enrich_summary_with_spotify(summary)

    print("Creating/updating Spotify playlist...")
    playlist = create_or_update_weekly_playlist(summary)
    print(
        f"Playlist ready: {playlist['name']} "
        f"({playlist['track_count']} tracks)"
    )

    print("Building email...")
    html = build_html_email(summary, enriched, playlist_url=playlist["url"])

    preview_path = save_html_preview(html)
    summary_path = save_text_summary(summary, playlist)
    print(f"Saved HTML preview: {preview_path}")
    print(f"Saved text summary: {summary_path}")

    print("Sending email...")
    send_email(html)

    history_path = append_run_history(summary, playlist, RECIPIENT_EMAIL)

    print("Done.")
    print(f"Sent to: {RECIPIENT_EMAIL}")
    print(f"Run history updated: {history_path}")
    logging.info(
        "Weekly Spotify recap sent to %s. Playlist=%s tracks=%s cover_uploaded=%s",
        RECIPIENT_EMAIL,
        playlist["id"],
        playlist["track_count"],
        playlist["cover_uploaded"],
    )


def run():
    setup_logging()

    try:
        main()

    except requests.exceptions.RequestException as e:
        logging.exception("Network/API error")
        print("Network/API error:", e)

    except RuntimeError as e:
        logging.exception("Runtime error")
        print("Runtime error:", e)

    except smtplib.SMTPAuthenticationError:
        logging.exception("SMTP login failed")
        print("SMTP login failed. Check Gmail address and app password.")

    except Exception as e:
        logging.exception("Unexpected error")
        print("Unexpected error:", e)


if __name__ == "__main__":
    run()
