"""Load environment variables and shared configuration values."""

import os
from pathlib import Path


def load_dotenv():
    """Load key-value pairs from a local .env file into environment variables."""
    env_path = Path.cwd() / ".env"

    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def required_env(name):
    """Return a required environment variable or raise a clear error."""
    value = os.environ.get(name)

    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name}. "
            "Add it to your .env file or set it in PowerShell before running."
        )

    return value


load_dotenv()

LASTFM_API_KEY = required_env("LASTFM_API_KEY")
LASTFM_USERNAME = required_env("LASTFM_USERNAME")

SPOTIFY_CLIENT_ID = required_env("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = required_env("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REFRESH_TOKEN = os.environ.get("SPOTIFY_REFRESH_TOKEN", "")
SPOTIFY_PLAYLIST_ID = os.environ.get("SPOTIFY_PLAYLIST_ID", "")
SPOTIFY_PLAYLIST_NAME = os.environ.get(
    "SPOTIFY_PLAYLIST_NAME",
    "Weekly Spotify Recap",
)

GMAIL_ADDRESS = required_env("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = required_env("GMAIL_APP_PASSWORD")
RECIPIENT_EMAIL = required_env("RECIPIENT_EMAIL")

PLAYLIST_URL = os.environ.get("PLAYLIST_URL", "")
PLAYLIST_COVER_PATH = os.environ.get(
    "PLAYLIST_COVER_PATH",
    "assets/playlist-cover.jpg",
)

LASTFM_BASE_URL = "https://ws.audioscrobbler.com/2.0/"
LASTFM_HEADERS = {"User-Agent": "M122E-WeeklyRecap/1.0"}

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"
