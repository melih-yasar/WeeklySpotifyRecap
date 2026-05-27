import os


LASTFM_API_KEY = os.environ["LASTFM_API_KEY"]
LASTFM_USERNAME = os.environ["LASTFM_USERNAME"]

SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]

GMAIL_ADDRESS = os.environ["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]

PLAYLIST_URL = os.environ.get("PLAYLIST_URL", "")

LASTFM_BASE_URL = "https://ws.audioscrobbler.com/2.0/"
LASTFM_HEADERS = {"User-Agent": "M122E-WeeklyRecap/1.0"}

SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE = "https://api.spotify.com/v1"
