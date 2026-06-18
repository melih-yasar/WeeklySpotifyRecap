"""Small helper functions used by multiple project modules."""


def normalize_name(value: str) -> str:
    """Normalize a name by keeping only lowercase letters and numbers."""
    return "".join(ch.lower() for ch in value if ch.isalnum())


def exact_name_match(a: str, b: str) -> bool:
    """Compare two names after normalization."""
    return normalize_name(a) == normalize_name(b)


def estimate_listening_hours(total_scrobbles):
    """Estimate listening time with an average song length of 3.5 minutes."""
    return round(total_scrobbles * 3.5 / 60, 1)


def roman_to_normalized_number(text: str) -> str:
    """Replace common Roman numerals in album names with normal numbers."""
    replacements = {
        " viii ": " 8 ",
        " vii ": " 7 ",
        " vi ": " 6 ",
        " iv ": " 4 ",
        " v ": " 5 ",
        " iii ": " 3 ",
        " ii ": " 2 ",
        " i ": " 1 ",
    }

    s = f" {text.lower()} "
    for roman, number in replacements.items():
        s = s.replace(roman, number)

    return " ".join(s.split())


def relaxed_album_match(a: str, b: str) -> bool:
    """Compare album names while also accepting simple Roman numerals."""
    a_norm = normalize_name(roman_to_normalized_number(a))
    b_norm = normalize_name(roman_to_normalized_number(b))
    return a_norm == b_norm


def find_album_for_track(summary, artist, title):
    """Find the album name for a track inside the raw summary data."""
    for track in summary["raw_tracks"]:
        if track["artist"] == artist and track["title"] == title:
            return track["album"]

    return "Unknown Album"

