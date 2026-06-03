import requests

from .config import SPOTIFY_API_BASE
from .spotify_auth import get_spotify_app_token, get_spotify_user_token


def spotify_get(path, params=None):
    response = requests.get(
        f"{SPOTIFY_API_BASE}{path}",
        headers={"Authorization": f"Bearer {get_spotify_app_token()}"},
        params=params,
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def spotify_request(method, path, json=None, params=None, data=None, content_type=None):
    headers = {"Authorization": f"Bearer {get_spotify_user_token()}"}

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
    return handle_user_response(response)


def spotify_search(query, item_type, limit=10):
    return spotify_get(
        "/search",
        params={"q": query, "type": item_type, "limit": limit},
    )


def upload_playlist_cover_image(playlist_id, image_base64):
    spotify_request(
        "PUT",
        f"/playlists/{playlist_id}/images",
        data=image_base64,
        content_type="image/jpeg",
    )


def handle_user_response(response):
    if response.status_code == 403:
        raise RuntimeError(f"Spotify refused the playlist request: {spotify_error(response)}")

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise RuntimeError(f"Spotify API request failed: {spotify_error(response)}") from error

    return response.json() if response.content else {}


def spotify_error(response):
    try:
        data = response.json()
    except ValueError:
        return response.text

    return data.get("error", {}).get("message", response.text)
