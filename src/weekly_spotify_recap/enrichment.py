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
        "hero": build_hero(summary["latest_track"]),
        "artists": build_artist_cards(summary),
        "tracks": build_track_cards(summary),
        "albums": build_album_cards(summary),
    }


def build_hero(latest):
    """Build the latest-listen hero section data."""
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


def build_artist_cards(summary):
    """Build Spotify data for the top artist cards."""
    return [
        artist_card(artist, plays)
        for artist, plays in summary["top_artists"][:3]
    ]


def artist_card(artist, plays):
    """Build one top artist card."""
    artist_info = find_spotify_artist(artist) or {}
    return {
        "artist": artist,
        "plays": plays,
        "image_url": artist_info.get("image_url"),
        "spotify_url": artist_info.get("spotify_url"),
    }


def build_track_cards(summary):
    """Build Spotify data for the top track rows."""
    return [
        track_card(summary, artist, title, plays)
        for (artist, title), plays in summary["top_tracks"][:5]
    ]


def track_card(summary, artist, title, plays):
    """Build one top track row with album cover data."""
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


def build_album_cards(summary):
    """Build Spotify data for the top album rows."""
    return [
        album_card(artist, album, plays)
        for (artist, album), plays in summary["top_albums"][:5]
    ]


def album_card(artist, album, plays):
    """Build one top album row."""
    album_info = find_spotify_album(artist, album) or {}
    return {
        "artist": artist,
        "album": album,
        "plays": plays,
        "cover_url": album_info.get("image_url"),
        "spotify_url": album_info.get("spotify_url"),
    }
