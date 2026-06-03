# Weekly Spotify Recap

This is my M122 automation project. It collects my Last.fm listening history for
the last 7 days, creates a weekly Spotify playlist from the top songs, and sends
the recap as an HTML email.

The goal is simple: collect music data automatically and show the weekly result
in an email.

## What It Does

- Fetches the last 7 days of Last.fm listening data
- Calculates top artists, top songs, top albums, listening time, busiest day, and peak hour
- Enriches the email with Spotify links and cover images
- Creates or updates a Spotify playlist with the weekly top songs
- Uploads a custom playlist image
- Sends the recap by email

## Project Structure

```text
WeeklySpotifyRecap/
|-- assets/                 # Playlist image
|-- scripts/                # Helper scripts
|-- tests/                  # Unit tests
|-- src/weekly_spotify_recap/
|   |-- main.py             # Run this file
|   |-- config.py           # Environment variables
|   |-- lastfm.py           # Collects Last.fm data
|   |-- summary.py          # Calculates recap stats
|   |-- enrichment.py       # Adds Spotify images and links
|   |-- playlist.py         # Creates/updates the Spotify playlist
|   |-- spotify_auth.py     # Spotify token handling
|   |-- spotify_api.py      # Spotify requests
|   |-- spotify_lookup.py   # Finds songs, albums, and artists on Spotify
|   |-- email_html.py       # Builds the HTML email
|   |-- mailer.py           # Sends the email
|   `-- helpers.py          # Small helper functions
|-- .env.example
`-- requirements.txt
```

## Documentation

- [Setup Guide](docs/setup.md)
- [Testing Protocol](docs/testing-protocol.md)

## Run

```powershell
py src\weekly_spotify_recap\main.py
```

## Tests

```powershell
$env:PYTHONPATH="src"
py -m unittest discover -s tests -p "test_*.py"
```
