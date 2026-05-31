# Setup

## 1. Create a virtual environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```powershell
pip install -r requirements.txt
```

## 3. Configure credentials

Copy `.env.example` to `.env` and fill in your own values.

`.env.example` is kept in Git because it documents which environment variables the app needs without exposing real API keys. The real `.env` file is ignored by Git.

Required values:

```env
LASTFM_API_KEY=
LASTFM_USERNAME=
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
SPOTIFY_REFRESH_TOKEN=
SPOTIFY_PLAYLIST_ID=
SPOTIFY_PLAYLIST_NAME=Weekly Spotify Recap
PLAYLIST_COVER_PATH=assets/playlist-cover.jpg
GMAIL_ADDRESS=
GMAIL_APP_PASSWORD=
RECIPIENT_EMAIL=
PLAYLIST_URL=
```

`SPOTIFY_REFRESH_TOKEN` is required so the app can create or update your Spotify
playlist. `SPOTIFY_PLAYLIST_ID` is optional. If it is empty, the app creates a
private playlist named with `SPOTIFY_PLAYLIST_NAME` and prints the playlist link.
After the first run, add that playlist ID to `.env` if you want every later run
to update the same playlist.

`PLAYLIST_URL` is optional fallback text for the email button. During a normal
run, the app uses the playlist URL returned by Spotify.

`PLAYLIST_COVER_PATH` is optional. If the file exists, the app uploads it as the
Spotify playlist cover on every run.

## 4. Get a Spotify refresh token

In your Spotify developer app, add this redirect URI:

```text
http://127.0.0.1:8888/callback
```

Then run:

```powershell
$env:SPOTIFY_CLIENT_ID="your-client-id"
$env:SPOTIFY_CLIENT_SECRET="your-client-secret"
py scripts/get-spotify-refresh-token.py
```

Log in to Spotify, approve the playlist and image-upload permissions, then copy
the printed `SPOTIFY_REFRESH_TOKEN=...` line into `.env`.

## 5. Run and send the recap email

```powershell
$env:PYTHONPATH="src"
py -m weekly_spotify_recap
```

Errors are saved to `logs/weekly_spotify_recap.log`.
The latest HTML preview and text summary are saved in the `output` folder.
