import base64

import requests

from .config import (
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REFRESH_TOKEN,
    SPOTIFY_TOKEN_URL,
)

_spotify_app_token_cache = None
_spotify_user_token_cache = None


def get_spotify_app_token():
    global _spotify_app_token_cache

    if _spotify_app_token_cache:
        return _spotify_app_token_cache

    response = requests.post(
        SPOTIFY_TOKEN_URL,
        headers=basic_auth_headers(),
        data={"grant_type": "client_credentials"},
        timeout=20,
    )
    response.raise_for_status()

    _spotify_app_token_cache = response.json()["access_token"]
    return _spotify_app_token_cache


def get_spotify_user_token():
    global _spotify_user_token_cache

    if _spotify_user_token_cache:
        return _spotify_user_token_cache

    if not SPOTIFY_REFRESH_TOKEN:
        raise RuntimeError("Missing SPOTIFY_REFRESH_TOKEN. Add it to your .env file.")

    response = requests.post(
        SPOTIFY_TOKEN_URL,
        headers=basic_auth_headers(),
        data={"grant_type": "refresh_token", "refresh_token": SPOTIFY_REFRESH_TOKEN},
        timeout=20,
    )
    response.raise_for_status()

    _spotify_user_token_cache = response.json()["access_token"]
    return _spotify_user_token_cache


def basic_auth_headers():
    raw = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth = base64.b64encode(raw.encode()).decode()

    return {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
