from collections import Counter


def build_summary(tracks):
    artist_counter = Counter()
    track_counter = Counter()
    album_counter = Counter()
    day_counter = Counter()
    hour_counter = Counter()

    for track in tracks:
        artist_counter[track["artist"]] += 1
        track_counter[(track["artist"], track["title"])] += 1
        album_counter[(track["artist"], track["album"])] += 1
        day_counter[track["played_at"].strftime("%A")] += 1
        hour_counter[track["played_at"].hour] += 1

    latest_track = (
        sorted(tracks, key=lambda x: x["played_at"], reverse=True)[0]
        if tracks
        else None
    )

    busiest_day = (
        day_counter.most_common(1)[0]
        if day_counter
        else ("Unknown", 0)
    )

    favorite_hour = (
        hour_counter.most_common(1)[0][0]
        if hour_counter
        else None
    )

    return {
        "total_scrobbles": len(tracks),
        "top_artists": artist_counter.most_common(5),
        "top_tracks": track_counter.most_common(10),
        "top_albums": album_counter.most_common(5),
        "busiest_day": busiest_day,
        "favorite_hour": favorite_hour,
        "latest_track": latest_track,
        "raw_tracks": tracks,
    }
