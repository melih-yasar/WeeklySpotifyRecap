from .config import PLAYLIST_URL
from .helpers import estimate_listening_hours


def print_console_summary(summary, enriched):
    top_artist = (
        summary["top_artists"][0][0]
        if summary["top_artists"]
        else "No data"
    )

    top_track = (
        summary["top_tracks"][0][0][1]
        if summary["top_tracks"]
        else "No data"
    )

    top_track_artist = (
        summary["top_tracks"][0][0][0]
        if summary["top_tracks"]
        else "No data"
    )

    busiest_day, busiest_day_plays = summary["busiest_day"]

    favorite_hour = (
        f"{summary['favorite_hour']:02d}:00"
        if summary["favorite_hour"] is not None
        else "Unknown"
    )

    listening_hours = estimate_listening_hours(summary["total_scrobbles"])

    print()
    print("=" * 44)
    print("WEEKLY LISTENING RECAP")
    print("=" * 44)

    print()
    print("Overview")
    print("-" * 44)
    print(f"Total plays:              {summary['total_scrobbles']}")
    print(f"Estimated listening time: {listening_hours}h")
    print(f"Peak listening time:      {favorite_hour}")
    print(f"Busiest day:              {busiest_day} ({busiest_day_plays} plays)")

    print()
    print("Highlights")
    print("-" * 44)
    print(f"Top artist:          {top_artist}")
    print(f"Most replayed track: {top_track} by {top_track_artist}")

    if summary["latest_track"]:
        latest = summary["latest_track"]
        print(
            f"Latest listen:       {latest['title']} by {latest['artist']} "
            f"({latest['album']})"
        )

    print()
    print("Top Artists")
    print("-" * 44)

    for index, (artist, plays) in enumerate(summary["top_artists"], start=1):
        spotify_url = None

        for item in enriched["artists"]:
            if item["artist"] == artist:
                spotify_url = item.get("spotify_url")
                break

        print(f"{index}. {artist} - {plays} plays")

        if spotify_url:
            print(f"   Spotify: {spotify_url}")

    print()
    print("Top Tracks")
    print("-" * 44)

    for index, item in enumerate(enriched["tracks"], start=1):
        print(
            f"{index}. {item['title']} - {item['artist']} "
            f"({item['plays']} plays)"
        )

        if item.get("album"):
            print(f"   Album: {item['album']}")

        if item.get("spotify_url"):
            print(f"   Spotify: {item['spotify_url']}")

    print()
    print("Top Albums")
    print("-" * 44)

    for index, item in enumerate(enriched["albums"], start=1):
        print(
            f"{index}. {item['album']} - {item['artist']} "
            f"({item['plays']} plays)"
        )

        if item.get("spotify_url"):
            print(f"   Spotify: {item['spotify_url']}")

    if enriched["hero"]:
        print()
        print("Latest Listen Info")
        print("-" * 44)
        print(f"Track:  {enriched['hero'].get('title')}")
        print(f"Artist: {enriched['hero'].get('artist')}")
        print(f"Album:  {enriched['hero'].get('album')}")

        if enriched["hero"].get("spotify_url"):
            print(f"Spotify: {enriched['hero'].get('spotify_url')}")

        if enriched["hero"].get("cover_url"):
            print(f"Cover:   {enriched['hero'].get('cover_url')}")

    if PLAYLIST_URL:
        print()
        print("Playlist")
        print("-" * 44)
        print(PLAYLIST_URL)

    print()
    print("=" * 44)
    print("Done.")
    print("=" * 44)
