"""Add Spotify images and links to the weekly summary."""

from .helpers import find_album_for_track
from .spotify_lookup import (
    find_spotify_album,
    find_spotify_artist,
    find_spotify_track,
)


def enrich_summary_with_spotify(summary):
    """Build all Spotify-enriched sections used by the email."""
    return {
        "hero": _enrich_latest_track(summary["latest_track"]),
        "artists": [
            _enrich_artist(artist, plays)
            for artist, plays in summary["top_artists"][:3]
        ],
        "tracks": [
            _enrich_track(summary, artist, title, plays)
            for (artist, title), plays in summary["top_tracks"][:5]
        ],
        "albums": [
            _enrich_album(artist, album, plays)
            for (artist, album), plays in summary["top_albums"][:5]
        ],
    }


def _enrich_latest_track(latest):
    """Build Spotify data for the latest-listen hero section."""
    if not latest:
        return None

    track_info = find_spotify_track(latest["artist"], latest["title"]) or {}
    album_info = find_spotify_album(latest["artist"], latest["album"]) or {}

    return {
        "artist": latest["artist"],
        "title": latest["title"],
        "album": latest["album"],
        "cover_url": track_info.get("album_cover_url") or album_info.get("image_url"),
        "spotify_url": track_info.get("spotify_url") or album_info.get("spotify_url"),
    }


def _enrich_artist(artist, plays):
    """Build Spotify data for one top artist card."""
    artist_info = find_spotify_artist(artist) or {}
    return {
        "artist": artist,
        "plays": plays,
        "image_url": artist_info.get("image_url"),
        "spotify_url": artist_info.get("spotify_url"),
    }


def _enrich_track(summary, artist, title, plays):
    """Build Spotify data for one top track row."""
    album_name = find_album_for_track(summary, artist, title)
    track_info = find_spotify_track(artist, title) or {}
    album_info = find_spotify_album(artist, album_name) or {}

    return {
        "artist": artist,
        "title": title,
        "album": album_name,
        "plays": plays,
        "cover_url": track_info.get("album_cover_url") or album_info.get("image_url"),
        "spotify_url": track_info.get("spotify_url"),
    }


def _enrich_album(artist, album, plays):
    """Build Spotify data for one top album row."""
    album_info = find_spotify_album(artist, album) or {}
    return {
        "artist": artist,
        "album": album,
        "plays": plays,
        "cover_url": album_info.get("image_url"),
        "spotify_url": album_info.get("spotify_url"),
    }
