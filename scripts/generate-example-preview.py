from datetime import datetime, timezone
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from weekly_spotify_recap.email_html import build_html_email
from weekly_spotify_recap.summary import build_summary


def main():
    tracks = [
        _track("The Weeknd", "Blinding Lights", "After Hours", 9),
        _track("The Weeknd", "Blinding Lights", "After Hours", 8),
        _track("Dua Lipa", "Levitating", "Future Nostalgia", 7),
        _track("Dua Lipa", "Levitating", "Future Nostalgia", 6),
        _track("Daft Punk", "Instant Crush", "Random Access Memories", 5),
        _track("Arctic Monkeys", "505", "Favourite Worst Nightmare", 4),
        _track("Tame Impala", "The Less I Know The Better", "Currents", 3),
        _track("Billie Eilish", "bad guy", "WHEN WE ALL FALL ASLEEP", 2),
        _track("Frank Ocean", "Pink + White", "Blonde", 1),
    ]

    summary = build_summary(tracks)
    enriched = {
        "hero": {
            "artist": "The Weeknd",
            "title": "Blinding Lights",
            "album": "After Hours",
            "cover_url": "https://i.scdn.co/image/ab67616d0000b273ef6e5f173afca6f8a3c5fb38",
            "spotify_url": "https://open.spotify.com/track/0VjIjW4GlUZAMYd2vXMi3b",
        },
        "artists": [
            {
                "artist": "The Weeknd",
                "plays": 17,
                "image_url": "https://i.scdn.co/image/ab6761610000e5eb9e528993a2820267b97f6aae",
                "spotify_url": "https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpatF05PJ",
            },
            {
                "artist": "Dua Lipa",
                "plays": 13,
                "image_url": "https://i.scdn.co/image/ab6761610000e5eb66d5ae4a8b88f2b62d151cda",
                "spotify_url": "https://open.spotify.com/artist/6M2wZ9GZgrQXHCFfjv46we",
            },
            {
                "artist": "Daft Punk",
                "plays": 5,
                "image_url": "https://i.scdn.co/image/ab6761610000e5eba7bfd7835b5c1eee0c95fa6e",
                "spotify_url": "https://open.spotify.com/artist/4tZwfgrHOc3mvqYlEYSvVi",
            },
        ],
        "tracks": [
            _enriched_track("The Weeknd", "Blinding Lights", "After Hours", 17, "https://i.scdn.co/image/ab67616d0000b273ef6e5f173afca6f8a3c5fb38"),
            _enriched_track("Dua Lipa", "Levitating", "Future Nostalgia", 13, "https://i.scdn.co/image/ab67616d0000b273bd26ede1ae69327010d49946"),
            _enriched_track("Daft Punk", "Instant Crush", "Random Access Memories", 5, "https://i.scdn.co/image/ab67616d0000b2731d5cf960a92bb8b03fc2be7f"),
            _enriched_track("Arctic Monkeys", "505", "Favourite Worst Nightmare", 4, "https://i.scdn.co/image/ab67616d0000b2730c8ac83035e9588e8ad34b90"),
            _enriched_track("Tame Impala", "The Less I Know The Better", "Currents", 3, "https://i.scdn.co/image/ab67616d0000b2739e1cfc756886ac782e363d79"),
        ],
        "albums": [
            _enriched_album("The Weeknd", "After Hours", 17, "https://i.scdn.co/image/ab67616d0000b273ef6e5f173afca6f8a3c5fb38"),
            _enriched_album("Dua Lipa", "Future Nostalgia", 13, "https://i.scdn.co/image/ab67616d0000b273bd26ede1ae69327010d49946"),
            _enriched_album("Daft Punk", "Random Access Memories", 5, "https://i.scdn.co/image/ab67616d0000b2731d5cf960a92bb8b03fc2be7f"),
        ],
    }

    html = build_html_email(
        summary,
        enriched,
        playlist_url="https://open.spotify.com/playlist/example",
    )

    output_path = ROOT / "examples" / "email-preview.html"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(html, encoding="utf-8")
    print(output_path)


def _track(artist, title, album, hour):
    return {
        "artist": artist,
        "title": title,
        "album": album,
        "played_at": datetime(2026, 5, 31, hour, 0, tzinfo=timezone.utc),
    }


def _enriched_track(artist, title, album, plays, cover_url):
    return {
        "artist": artist,
        "title": title,
        "album": album,
        "plays": plays,
        "cover_url": cover_url,
        "spotify_url": "https://open.spotify.com/",
    }


def _enriched_album(artist, album, plays, cover_url):
    return {
        "artist": artist,
        "album": album,
        "plays": plays,
        "cover_url": cover_url,
        "spotify_url": "https://open.spotify.com/",
    }


if __name__ == "__main__":
    main()
