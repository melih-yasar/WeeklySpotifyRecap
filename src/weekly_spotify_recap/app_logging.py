"""Logging setup for the Weekly Spotify Recap app."""

import logging
from pathlib import Path


LOGGER = logging.getLogger("weekly_spotify_recap")
LOG_FILE = Path.cwd() / "logs" / "weekly_spotify_recap.log"


def configure_logging(log_file=LOG_FILE):
    """Configure file logging for normal runs and errors."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    LOGGER.setLevel(logging.INFO)
    LOGGER.propagate = False

    if _has_file_handler(log_file):
        return

    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)s %(message)s"
    ))
    LOGGER.addHandler(handler)


def _has_file_handler(log_file):
    """Return True when the logger already writes to the given file."""
    return any(
        isinstance(handler, logging.FileHandler)
        and Path(handler.baseFilename) == log_file
        for handler in LOGGER.handlers
    )


def log_summary_built(summary):
    """Log the most important summary result values."""
    LOGGER.info(
        "Built weekly summary. total_scrobbles=%s top_tracks=%s",
        summary["total_scrobbles"],
        len(summary["top_tracks"]),
    )


def log_playlist_ready(playlist):
    """Log the playlist result values."""
    LOGGER.info(
        "Spotify playlist ready. id=%s name=%s tracks=%s cover_uploaded=%s",
        playlist.get("id", ""),
        playlist.get("name", ""),
        playlist.get("track_count", 0),
        playlist.get("cover_uploaded", False),
    )


def log_email_sent(recipient, playlist_url):
    """Log the successful email delivery target."""
    LOGGER.info(
        "Weekly Spotify recap sent. recipient=%s playlist_url=%s",
        recipient,
        playlist_url,
    )
