from .helpers import exact_name_match, relaxed_album_match
from .spotify_api import spotify_search


def find_spotify_artist(artist_name):
    data = spotify_search(f'artist:"{artist_name}"', "artist", limit=10)

    for item in data.get("artists", {}).get("items", []):
        if exact_name_match(item.get("name", ""), artist_name):
            return {
                "name": item.get("name"),
                "image_url": first_image(item),
                "spotify_url": item.get("external_urls", {}).get("spotify"),
            }

    return None


def find_spotify_album(artist_name, album_name):
    data = spotify_search(
        f'album:"{album_name}" artist:"{artist_name}"',
        "album",
        limit=10,
    )
    items = data.get("albums", {}).get("items", [])

    for matcher in (exact_name_match, relaxed_album_match):
        album = find_album(items, artist_name, album_name, matcher)
        if album:
            return album

    for item in items:
        if has_artist(item, artist_name):
            return album_result(item)

    return album_result(items[0]) if items else None


def find_spotify_track(artist_name, track_name):
    data = spotify_search(
        f'track:"{track_name}" artist:"{artist_name}"',
        "track",
        limit=10,
    )

    for item in data.get("tracks", {}).get("items", []):
        if track_matches(item, artist_name, track_name):
            return track_result(item)

    return None


def find_album(items, artist_name, album_name, name_matcher):
    for item in items:
        if name_matcher(item.get("name", ""), album_name) and has_artist(item, artist_name):
            return album_result(item)

    return None


def track_matches(item, artist_name, track_name):
    return exact_name_match(item.get("name", ""), track_name) and has_artist(item, artist_name)


def has_artist(item, artist_name):
    return any(
        exact_name_match(artist.get("name", ""), artist_name)
        for artist in item.get("artists", [])
    )


def track_result(item):
    album = item.get("album", {})

    return {
        "name": item.get("name"),
        "uri": item.get("uri"),
        "spotify_url": item.get("external_urls", {}).get("spotify"),
        "album_cover_url": first_image(album),
        "album_name": album.get("name"),
    }


def album_result(item):
    return {
        "name": item.get("name"),
        "image_url": first_image(item),
        "spotify_url": item.get("external_urls", {}).get("spotify"),
    }


def first_image(item):
    images = item.get("images", [])
    return images[0]["url"] if images else None
