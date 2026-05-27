# WeeklySpotifyRecap
A Python-based email automation project that generates a weekly Spotify listening recap and sends it to users, including highlights such as top songs, favorite artists, and listening insights.

## Setup

Install the project and its dependencies:

```bash
pip install -e .
```

Copy `.env.example` to `.env` and fill in your Last.fm and Spotify credentials. Then export those values into your shell before running the recap.

Run the console recap:

```bash
weekly-spotify-recap
```

You can also run it as a module:

```bash
python -m weekly_spotify_recap
```
