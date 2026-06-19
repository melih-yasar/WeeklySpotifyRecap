"""Logging setup for the Weekly Spotify Recap app."""

import logging
from datetime import datetime, timedelta
from pathlib import Path


LOGGER = logging.getLogger("weekly_spotify_recap")
LOG_FILE = Path.cwd() / "logs" / "weekly_spotify_recap.log"
LOG_RETENTION_DAYS = 7
RUN_SEPARATOR = "=" * 72


def configure_logging(log_file=LOG_FILE):
    """Configure file logging for normal runs and errors."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    remove_old_log_entries(log_file)
    LOGGER.setLevel(logging.INFO)
    LOGGER.propagate = False

    if _has_file_handler(log_file):
        return

    handler = logging.FileHandler(log_file, encoding="utf-8")
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(message)s"
    ))
    LOGGER.addHandler(handler)


def remove_old_log_entries(log_file, retention_days=LOG_RETENTION_DAYS, now=None):
    """Remove log entries older than the retention period."""
    if not log_file.exists():
        return

    now = now or datetime.now()
    cutoff = now - timedelta(days=retention_days)
    lines = log_file.read_text(encoding="utf-8").splitlines(keepends=True)
    kept_lines = []
    keep_current_entry = True

    for line in lines:
        timestamp = _line_timestamp(line)

        if timestamp:
            keep_current_entry = timestamp >= cutoff

        if keep_current_entry:
            kept_lines.append(line)

    if kept_lines != lines:
        log_file.write_text("".join(kept_lines), encoding="utf-8")


def _line_timestamp(line):
    """Return the timestamp at the start of a log line, if present."""
    try:
        return datetime.strptime(line[:19], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None


def _has_file_handler(log_file):
    """Return True when the logger already writes to the given file."""
    return any(
        isinstance(handler, logging.FileHandler)
        and Path(handler.baseFilename) == log_file
        for handler in LOGGER.handlers
    )


def log_run_started():
    """Log a clear separator at the beginning of each app run."""
    LOGGER.info(RUN_SEPARATOR)
    LOGGER.info("Weekly Spotify Recap run started")


def log_run_finished(status):
    """Log a clear status at the end of each app run."""
    LOGGER.info("Weekly Spotify Recap run finished. status=%s", status)
    LOGGER.info(RUN_SEPARATOR)


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
