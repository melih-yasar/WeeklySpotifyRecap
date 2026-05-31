# Project Structure

This project uses a small `src`-based Python layout so the application code,
documentation, helper scripts, and generated files stay separate.

## Folders

```text
assets/
```

Static assets that belong in the repository. The playlist cover image is stored
here so the app can upload it to Spotify.

```text
docs/
```

Project documentation. Start with `setup.md` for installation and API setup.

```text
examples/
```

Example generated artifacts for GitHub visitors. `email-preview.html` shows what
the recap email looks like without requiring API keys.

```text
scripts/
```

One-time or helper scripts. `get-spotify-refresh-token.py` is used to create the
Spotify refresh token for playlist updates and cover uploads.

```text
src/weekly_spotify_recap/
```

Main application package.

```text
logs/
output/
```

Generated at runtime. These folders are ignored by Git because they contain
local run logs, email previews, text summaries, and run history files.

## Main Application Files

- `cli.py`: Coordinates the weekly recap run
- `config.py`: Loads `.env` values
- `lastfm.py`: Fetches Last.fm listening history
- `summary.py`: Calculates recap statistics
- `spotify.py`: Handles Spotify API requests
- `playlist.py`: Creates or updates the Spotify playlist
- `enrichment.py`: Adds Spotify images and links to recap data
- `email_html.py`: Builds the HTML email
- `mailer.py`: Sends the email through Gmail SMTP
- `outputs.py`: Saves preview, summary, and run history files
