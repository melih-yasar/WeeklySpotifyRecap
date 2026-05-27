from datetime import datetime, timedelta, timezone

import requests

from config import LASTFM_API_KEY, LASTFM_BASE_URL, LASTFM_HEADERS, LASTFM_USERNAME


def lastfm_get(params):
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
    return lastfm_get({
        "method": "user.getrecenttracks",
        "user": LASTFM_USERNAME,
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "limit": limit,
        "page": page,
    })


def get_all_tracks_last_7_days():
    now_utc = datetime.now(timezone.utc)
    week_ago = now_utc - timedelta(days=7)

    all_tracks = []
    page = 1

    while True:
        data = get_recent_tracks_page(page=page, limit=200)
        tracks = data.get("recenttracks", {}).get("track", [])

        if isinstance(tracks, dict):
            tracks = [tracks]

        if not tracks:
            break

        stop_paging = False

        for track in tracks:
            date_info = track.get("date")

            if not date_info or "uts" not in date_info:
                continue

            played_at = datetime.fromtimestamp(
                int(date_info["uts"]),
                tz=timezone.utc,
            )

            if played_at >= week_ago:
                all_tracks.append({
                    "artist": track.get("artist", {}).get("#text", "Unknown Artist").strip(),
                    "title": track.get("name", "Unknown Track").strip(),
                    "album": track.get("album", {}).get("#text", "Unknown Album").strip() or "Unknown Album",
                    "played_at": played_at,
                })
            else:
                stop_paging = True
                break

        if stop_paging:
            break

        total_pages = int(
            data.get("recenttracks", {})
            .get("@attr", {})
            .get("totalPages", "1")
        )

        if page >= total_pages:
            break

        page += 1

    return all_tracks
