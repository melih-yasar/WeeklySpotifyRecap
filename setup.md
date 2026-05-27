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
PLAYLIST_URL=
```

## 4. Load environment variables

PowerShell does not automatically load `.env` files. Set the values in your shell before running the app:

```powershell
$env:LASTFM_API_KEY="your-lastfm-api-key"
$env:LASTFM_USERNAME="your-lastfm-username"
$env:SPOTIFY_CLIENT_ID="your-spotify-client-id"
$env:SPOTIFY_CLIENT_SECRET="your-spotify-client-secret"
$env:PLAYLIST_URL="your-playlist-url"
```

## 5. Run the recap

```powershell
$env:PYTHONPATH="src"
py -m weekly_spotify_recap
```
