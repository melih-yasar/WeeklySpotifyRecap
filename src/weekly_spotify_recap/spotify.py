import base64
import json as json_module

import requests

from .config import (
    SPOTIFY_API_BASE,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_CLIENT_SECRET,
    SPOTIFY_REFRESH_TOKEN,
    SPOTIFY_TOKEN_URL,
)
from .helpers import exact_name_match, relaxed_album_match

_spotify_app_token_cache = None
_spotify_user_token_cache = None


def get_spotify_app_token():
    global _spotify_app_token_cache

    if _spotify_app_token_cache:
        return _spotify_app_token_cache

    raw = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth = base64.b64encode(raw.encode()).decode()

    response = requests.post(
        SPOTIFY_TOKEN_URL,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
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
        raise RuntimeError(
            "Missing SPOTIFY_REFRESH_TOKEN. Add a Spotify refresh token to "
            "your .env file before creating or updating playlists."
        )

    raw = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth = base64.b64encode(raw.encode()).decode()

    response = requests.post(
        SPOTIFY_TOKEN_URL,
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "refresh_token",
            "refresh_token": SPOTIFY_REFRESH_TOKEN,
        },
        timeout=20,
    )

    response.raise_for_status()

    _spotify_user_token_cache = response.json()["access_token"]
    return _spotify_user_token_cache


def spotify_get(path, params=None):
    token = get_spotify_app_token()

    response = requests.get(
        f"{SPOTIFY_API_BASE}{path}",
        headers={"Authorization": f"Bearer {token}"},
        params=params,
        timeout=20,
    )

    response.raise_for_status()
    return response.json()


def spotify_user_request(method, path, json=None, params=None, data=None, content_type=None):
    token = get_spotify_user_token()
    headers = {"Authorization": f"Bearer {token}"}

    if content_type:
        headers["Content-Type"] = content_type

    response = requests.request(
        method,
        f"{SPOTIFY_API_BASE}{path}",
        headers=headers,
        json=json,
        params=params,
        data=data,
        timeout=20,
    )

    if response.status_code == 403:
        try:
            message = response.json().get("error", {}).get("message", response.text)
        except ValueError:
            message = response.text

        raise RuntimeError(
            "Spotify refused the playlist request. Check that your Spotify "
            "developer app has your account added under User Management and "
            f"that the token has playlist scopes. Spotify said: {message}"
        )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        details = response.text
        try:
            details = json_module.dumps(response.json())
        except ValueError:
            pass

        raise RuntimeError(f"Spotify API request failed: {details}") from error

    if response.content:
        return response.json()

    return {}


def upload_playlist_cover_image(playlist_id, image_base64):
    spotify_user_request(
        "PUT",
        f"/playlists/{playlist_id}/images",
        data=image_base64,
        content_type="image/jpeg",
    )


def spotify_search(query, item_type, limit=10):
    return spotify_get(
        "/search",
        params={
            "q": query,
            "type": item_type,
            "limit": limit,
        },
    )


def get_exact_spotify_artist(artist_name):
    try:
        data = spotify_search(f'artist:"{artist_name}"', "artist", limit=10)
        items = data.get("artists", {}).get("items", [])

        for item in items:
            if exact_name_match(item.get("name", ""), artist_name):
                images = item.get("images", [])
                return {
                    "name": item.get("name"),
                    "image_url": images[0]["url"] if images else None,
                    "spotify_url": item.get("external_urls", {}).get("spotify"),
                }

    except Exception:
        pass

    return None


def get_exact_spotify_album(artist_name, album_name):
    try:
        data = spotify_search(
            f'album:"{album_name}" artist:"{artist_name}"',
            "album",
            limit=10,
        )

        items = data.get("albums", {}).get("items", [])

        exact_match = _find_album_match(items, artist_name, album_name, exact_name_match)
        if exact_match:
            return exact_match

        relaxed_match = _find_album_match(items, artist_name, album_name, relaxed_album_match)
        if relaxed_match:
            return relaxed_match

        artist_match = _find_album_by_artist(items, artist_name)
        if artist_match:
            return artist_match

        if items:
            return _album_result(items[0])

    except Exception:
        pass

    return None


def get_exact_spotify_track(artist_name, track_name):
    try:
        data = spotify_search(
            f'track:"{track_name}" artist:"{artist_name}"',
            "track",
            limit=10,
        )

        items = data.get("tracks", {}).get("items", [])

        for item in items:
            item_artist_names = [
                artist.get("name", "")
                for artist in item.get("artists", [])
            ]

            if exact_name_match(item.get("name", ""), track_name) and any(
                exact_name_match(artist, artist_name)
                for artist in item_artist_names
            ):
                album = item.get("album", {})
                images = album.get("images", [])

                return {
                    "name": item.get("name"),
                    "uri": item.get("uri"),
                    "spotify_url": item.get("external_urls", {}).get("spotify"),
                    "album_cover_url": images[0]["url"] if images else None,
                    "album_name": album.get("name"),
                }

    except Exception:
        pass

    return None


def _find_album_match(items, artist_name, album_name, name_matcher):
    for item in items:
        item_artist_names = [
            artist.get("name", "")
            for artist in item.get("artists", [])
        ]

        if name_matcher(item.get("name", ""), album_name) and any(
            exact_name_match(artist, artist_name)
            for artist in item_artist_names
        ):
            return _album_result(item)

    return None


def _find_album_by_artist(items, artist_name):
    for item in items:
        item_artist_names = [
            artist.get("name", "")
            for artist in item.get("artists", [])
        ]

        if any(
            exact_name_match(artist, artist_name)
            for artist in item_artist_names
        ):
            return _album_result(item)

    return None


def _album_result(item):
    images = item.get("images", [])
    return {
        "name": item.get("name"),
        "image_url": images[0]["url"] if images else None,
        "spotify_url": item.get("external_urls", {}).get("spotify"),
    }
