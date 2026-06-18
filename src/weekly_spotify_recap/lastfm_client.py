"""Collect weekly listening data from the Last.fm API."""

from datetime import datetime, timedelta, timezone

import requests

from .config import LASTFM_API_KEY, LASTFM_BASE_URL, LASTFM_HEADERS, LASTFM_USERNAME


def lastfm_get(params):
    """Send a Last.fm API request and return the JSON response."""
    response = requests.get(
        LASTFM_BASE_URL,
        params=params,
        headers=LASTFM_HEADERS,
        timeout=20,
    )

    response.raise_for_status()
    data = response.json()

    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(
            f"Last.fm API error {data['error']}: "
            f"{data.get('message', 'Unknown error')}"
        )

    return data


def get_recent_tracks_page(page=1, limit=200):
    """Request one page of recent tracks from Last.fm."""
    return lastfm_get({
        "method": "user.getrecenttracks",
        "user": LASTFM_USERNAME,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit,
        "page": page,
    })


def track_from_lastfm(track):
    """Convert one Last.fm track item into the app's track format."""
    date_info = track.get("date")

    if not date_info or "uts" not in date_info:
        return None

    return {
        "artist": track.get("artist", {}).get("#text", "Unknown Artist").strip(),
        "title": track.get("name", "Unknown Track").strip(),
        "album": track.get("album", {}).get("#text", "").strip() or "Unknown Album",
        "played_at": datetime.fromtimestamp(int(date_info["uts"]), tz=timezone.utc),
    }


def tracks_from_page(data):
    """Return the track list from a Last.fm page response."""
    tracks = data.get("recenttracks", {}).get("track", [])
    return [tracks] if isinstance(tracks, dict) else tracks


def total_pages(data):
    """Return how many result pages Last.fm says are available."""
    attr = data.get("recenttracks", {}).get("@attr", {})
    return int(attr.get("totalPages", "1"))


def add_recent_tracks(tracks, all_tracks, week_ago):
    """Add tracks newer than week_ago and stop when older tracks begin."""
    for track in tracks:
        item = track_from_lastfm(track)

        if not item:
            continue

        if item["played_at"] < week_ago:
            return False

        all_tracks.append(item)

    return True


def get_all_tracks_last_7_days():
    """Collect all Last.fm tracks played in the last 7 days."""
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    all_tracks = []
    page = 1

    while True:
        data = get_recent_tracks_page(page=page, limit=200)
        tracks = tracks_from_page(data)

        if not tracks or not add_recent_tracks(tracks, all_tracks, week_ago):
            break

        if page >= total_pages(data):
            break

        page += 1

    return all_tracks

