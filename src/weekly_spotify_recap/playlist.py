import base64
from pathlib import Path

from .config import PLAYLIST_COVER_PATH, SPOTIFY_PLAYLIST_ID, SPOTIFY_PLAYLIST_NAME
from .spotify import (
    get_exact_spotify_track,
    spotify_user_request,
    upload_playlist_cover_image,
)


def create_or_update_weekly_playlist(summary):
    track_uris = get_top_track_uris(summary)

    if not track_uris:
        raise RuntimeError("No Spotify tracks found for the weekly playlist.")

    playlist = (
        get_playlist(SPOTIFY_PLAYLIST_ID)
        if SPOTIFY_PLAYLIST_ID
        else create_playlist(SPOTIFY_PLAYLIST_NAME)
    )

    playlist_id = playlist["id"]
    replace_playlist_tracks(playlist_id, track_uris)
    cover_uploaded = upload_cover_if_available(playlist_id)

    return {
        "id": playlist_id,
        "name": playlist.get("name", SPOTIFY_PLAYLIST_NAME),
        "url": playlist.get("external_urls", {}).get("spotify", ""),
        "track_count": len(track_uris),
        "cover_uploaded": cover_uploaded,
    }


def get_top_track_uris(summary, limit=20):
    uris = []
    seen = set()

    for (artist, title), _plays in summary["top_tracks"][:limit]:
        track_info = get_exact_spotify_track(artist, title)
        uri = (track_info or {}).get("uri")

        if uri and uri not in seen:
            uris.append(uri)
            seen.add(uri)

    return uris


def get_playlist(playlist_id):
    return spotify_user_request("GET", f"/playlists/{playlist_id}")


def create_playlist(name):
    return spotify_user_request(
        "POST",
        "/me/playlists",
        json={
            "name": name,
            "description": "Automatically generated weekly listening recap.",
            "public": False,
        },
    )


def replace_playlist_tracks(playlist_id, track_uris):
    spotify_user_request(
        "PUT",
        f"/playlists/{playlist_id}/items",
        json={"uris": track_uris},
    )


def upload_cover_if_available(playlist_id):
    cover_path = Path(PLAYLIST_COVER_PATH)

    if not cover_path.exists():
        return False

    image_base64 = base64.b64encode(cover_path.read_bytes()).decode("ascii")
    upload_playlist_cover_image(playlist_id, image_base64)
    return True
