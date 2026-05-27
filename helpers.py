def normalize_name(value: str) -> str:
    return "".join(ch.lower() for ch in value if ch.isalnum())


def exact_name_match(a: str, b: str) -> bool:
    return normalize_name(a) == normalize_name(b)


def estimate_listening_hours(total_scrobbles):
    return round(total_scrobbles * 3.5 / 60, 1)


def roman_to_normalized_number(text: str) -> str:
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
    a_norm = normalize_name(roman_to_normalized_number(a))
    b_norm = normalize_name(roman_to_normalized_number(b))
    return a_norm == b_norm


def find_album_for_track(summary, artist, title):
    for track in summary["raw_tracks"]:
        if track["artist"] == artist and track["title"] == title:
            return track["album"]

    return "Unknown Album"
