from datetime import datetime
from pathlib import Path

from .helpers import estimate_listening_hours


def output_dir():
    path = Path.cwd() / "output"
    path.mkdir(exist_ok=True)
    return path


def save_html_preview(html):
    path = output_dir() / "weekly_recap_preview.html"
    path.write_text(html, encoding="utf-8")
    return path


def save_text_summary(summary, playlist):
    path = output_dir() / "weekly_summary.txt"
    top_artist = summary["top_artists"][0][0] if summary["top_artists"] else "No data"
    top_track = summary["top_tracks"][0][0] if summary["top_tracks"] else ("No data", "No data")

    content = f"""Weekly Spotify Recap Summary
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

Total plays: {summary["total_scrobbles"]}
Estimated listening time: {estimate_listening_hours(summary["total_scrobbles"])} hours
Top artist: {top_artist}
Top track: {top_track[1]} by {top_track[0]}
Busiest day: {summary["busiest_day"][0]} ({summary["busiest_day"][1]} plays)
Favorite listening hour: {summary["favorite_hour"]}:00

Playlist: {playlist["name"]}
Playlist URL: {playlist["url"]}
Playlist tracks: {playlist["track_count"]}
"""

    path.write_text(content, encoding="utf-8")
    return path


def append_run_history(summary, playlist, recipient_email):
    path = output_dir() / "run_history.csv"
    new_file = not path.exists()
    line = ",".join([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        recipient_email,
        str(summary["total_scrobbles"]),
        str(playlist["track_count"]),
        playlist["id"],
        playlist["url"],
    ])

    with path.open("a", encoding="utf-8") as file:
        if new_file:
            file.write("run_at,recipient,total_scrobbles,playlist_tracks,playlist_id,playlist_url\n")
        file.write(line + "\n")

    return path
