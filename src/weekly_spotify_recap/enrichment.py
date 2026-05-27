from .helpers import find_album_for_track
from .spotify import (
    get_exact_spotify_album,
    get_exact_spotify_artist,
    get_exact_spotify_track,
)


def enrich_summary_with_spotify(summary):
    enriched = {
        "hero": None,
        "artists": [],
        "tracks": [],
        "albums": [],
    }

    if summary["latest_track"]:
        latest = summary["latest_track"]

        track_info = get_exact_spotify_track(
            latest["artist"],
            latest["title"],
        )

        album_info = get_exact_spotify_album(
            latest["artist"],
            latest["album"],
        )

        enriched["hero"] = {
            "artist": latest["artist"],
            "title": latest["title"],
            "album": latest["album"],
            "cover_url": (
                (track_info or {}).get("album_cover_url")
                or (album_info or {}).get("image_url")
            ),
            "spotify_url": (
                (track_info or {}).get("spotify_url")
                or (album_info or {}).get("spotify_url")
            ),
        }

    for artist, plays in summary["top_artists"][:3]:
        artist_info = get_exact_spotify_artist(artist)

        enriched["artists"].append({
            "artist": artist,
            "plays": plays,
            "image_url": (artist_info or {}).get("image_url"),
            "spotify_url": (artist_info or {}).get("spotify_url"),
        })

    for (artist, title), plays in summary["top_tracks"][:5]:
        album_name = find_album_for_track(summary, artist, title)

        track_info = get_exact_spotify_track(artist, title)
        album_info = get_exact_spotify_album(artist, album_name)

        enriched["tracks"].append({
            "artist": artist,
            "title": title,
            "album": album_name,
            "plays": plays,
            "cover_url": (
                (track_info or {}).get("album_cover_url")
                or (album_info or {}).get("image_url")
            ),
            "spotify_url": (track_info or {}).get("spotify_url"),
        })

    for (artist, album), plays in summary["top_albums"][:5]:
        album_info = get_exact_spotify_album(artist, album)

        enriched["albums"].append({
            "artist": artist,
            "album": album,
            "plays": plays,
            "cover_url": (album_info or {}).get("image_url"),
            "spotify_url": (album_info or {}).get("spotify_url"),
        })

    return enriched
