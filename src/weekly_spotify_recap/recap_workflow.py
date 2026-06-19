"""Weekly recap workflow orchestration."""

from .app_logging import (
    LOGGER,
    configure_logging,
    log_run_finished,
    log_run_started,
    log_email_sent,
    log_playlist_ready,
    log_summary_built,
)


def run_recap():
    """Run the complete recap workflow."""
    from .config import RECIPIENT_EMAIL
    from .recap_email_builder import build_html_email
    from .spotify_enrichment import enrich_summary_with_spotify
    from .lastfm_client import get_all_tracks_last_7_days
    from .email_sender import send_email
    from .spotify_playlist import create_or_update_weekly_playlist
    from .recap_summary import build_summary

    configure_logging()
    log_run_started()

    print("Loading Last.fm data...")
    tracks = get_all_tracks_last_7_days()
    LOGGER.info("Loaded %s tracks from Last.fm.", len(tracks))

    if not tracks:
        LOGGER.warning("No scrobbles found in the last 7 days.")
        print("No scrobbles found in the last 7 days.")
        log_run_finished("NO_DATA")
        return

    print("Building summary...")
    summary = build_summary(tracks)
    log_summary_built(summary)

    print("Loading Spotify images and links...")
    enriched = enrich_summary_with_spotify(summary)
    LOGGER.info("Loaded Spotify images and links for the email.")

    print("Creating/updating Spotify playlist...")
    playlist = create_or_update_weekly_playlist(summary)
    log_playlist_ready(playlist)
    print(f"Playlist ready: {playlist['name']} ({playlist['track_count']} tracks)")

    print("Building email...")
    html = build_html_email(summary, enriched, playlist_url=playlist["url"])

    print("Sending email...")
    send_email(html)

    log_email_sent(RECIPIENT_EMAIL, playlist["url"])
    print(f"Sent to: {RECIPIENT_EMAIL}")

    log_run_finished("SUCCESS")
    print("Done.")
