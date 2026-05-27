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
GMAIL_ADDRESS=
GMAIL_APP_PASSWORD=
RECIPIENT_EMAIL=
PLAYLIST_URL=
```

## 4. Run and send the recap email

```powershell
$env:PYTHONPATH="src"
py -m weekly_spotify_recap
```
