import requests

from console_output import print_console_summary
from enrichment import enrich_summary_with_spotify
from lastfm import get_all_tracks_last_7_days
from summary import build_summary


def main():
    print("Loading Last.fm data...")
    tracks = get_all_tracks_last_7_days()

    if not tracks:
        print("No scrobbles found in the last 7 days.")
        return

    print("Building summary...")
    summary = build_summary(tracks)

    print("Loading Spotify links...")
    enriched = enrich_summary_with_spotify(summary)

    print_console_summary(summary, enriched)


if __name__ == "__main__":
    try:
        main()

    except requests.exceptions.RequestException as e:
        print("Network/API error:", e)

    except RuntimeError as e:
        print("Runtime error:", e)

    except Exception as e:
        print("Unexpected error:", e)
