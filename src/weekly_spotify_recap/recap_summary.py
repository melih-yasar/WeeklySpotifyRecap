"""Build recap statistics from collected listening data."""

from collections import Counter


def build_summary(tracks):
    """Build the full weekly summary used by the email and playlist."""
    artist_counter, track_counter, album_counter = music_counters(tracks)
    day_counter, hour_counter = time_counters(tracks)

    return {
        "total_scrobbles": len(tracks),
        "top_artists": artist_counter.most_common(5),
        "top_tracks": track_counter.most_common(10),
        "top_albums": album_counter.most_common(5),
        "busiest_day": most_common_day(day_counter),
        "favorite_hour": favorite_hour(hour_counter),
        "latest_track": latest_track(tracks),
        "raw_tracks": tracks,
    }


def music_counters(tracks):
    """Count artists, tracks, and albums."""
    artist_counter = Counter()
    track_counter = Counter()
    album_counter = Counter()

    for track in tracks:
        artist_counter[track["artist"]] += 1
        track_counter[(track["artist"], track["title"])] += 1
        album_counter[(track["artist"], track["album"])] += 1

    return artist_counter, track_counter, album_counter


def time_counters(tracks):
    """Count listening activity by weekday and hour."""
    day_counter = Counter()
    hour_counter = Counter()

    for track in tracks:
        day_counter[track["played_at"].strftime("%A")] += 1
        hour_counter[track["played_at"].hour] += 1

    return day_counter, hour_counter


def latest_track(tracks):
    """Return the most recently played track."""
    return max(tracks, key=lambda track: track["played_at"], default=None)


def most_common_day(day_counter):
    """Return the day with the highest number of plays."""
    return day_counter.most_common(1)[0] if day_counter else ("Unknown", 0)


def favorite_hour(hour_counter):
    """Return the hour with the highest number of plays."""
    return hour_counter.most_common(1)[0][0] if hour_counter else None

