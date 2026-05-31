# Weekly Spotify Recap

A Python automation project that creates a weekly music recap from Last.fm
listening history, enriches it with Spotify data, updates a Spotify playlist,
and sends the recap by email.

## Features

- Fetches the last 7 days of Last.fm scrobbles
- Calculates top artists, tracks, albums, listening time, busiest day, and peak hour
- Enriches the recap with Spotify links and cover images
- Creates or updates a Spotify playlist with the top weekly songs
- Uploads a custom playlist cover
- Sends a styled HTML email recap
- Saves a local HTML preview, text summary, run history, and error log

## Project Structure

```text
WeeklySpotifyRecap/
├── assets/                 # Static project assets, including playlist cover
├── docs/                   # Setup and project documentation
├── scripts/                # Helper scripts, e.g. Spotify refresh token setup
├── src/weekly_spotify_recap/
│   ├── cli.py              # Main application flow
│   ├── config.py           # Environment variable loading
│   ├── lastfm.py           # Last.fm API access
│   ├── spotify.py          # Spotify API access
│   ├── playlist.py         # Spotify playlist update logic
│   ├── summary.py          # Weekly recap calculations
│   ├── enrichment.py       # Spotify image/link enrichment
│   ├── email_html.py       # HTML email template
│   ├── mailer.py           # Gmail SMTP sending
│   └── outputs.py          # Local preview, summary, and run history files
├── .env.example            # Example environment variables
├── requirements.txt        # Python dependencies
└── weekly-email.py         # Simple launcher script
```

## Documentation

- [Setup Guide](docs/setup.md)
- [Project Structure](docs/project-structure.md)
- [Example Email Preview](examples/email-preview.html)

## Quick Run

```powershell
$env:PYTHONPATH="src"
py -m weekly_spotify_recap
```
