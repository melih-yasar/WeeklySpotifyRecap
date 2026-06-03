# Testing Protocol

Date: 03.06.2026

Project: Weekly Spotify Recap

Testing type: White-box unit testing with Python `unittest`

## Test Setup

Run all tests with:

```powershell
$env:PYTHONPATH="src"
py -m unittest discover -s tests -p "test_*.py" -v
```

The tests use fake environment variables and mocks. They do not call Last.fm,
Spotify, or Gmail.

## MoSCoW Scope Used For Testing

The tests focus on the documented project proposal:

- Must: collect weekly listening data, identify top songs/albums/artists,
  calculate listening statistics, create a top-songs playlist, and send an
  email recap with the playlist link.
- Should: use a Spotify-inspired email design, show rankings and listening
  time, display the playlist link clearly, and handle API/email errors.
- Could: include images and clickable Spotify links.
- Extra kept by request: upload a custom Spotify playlist image.

## Test Coverage By Module

| Module | Test file | Main criteria |
| --- | --- | --- |
| `main.py` | `tests/test_app_main.py` | Happy path, no-track edge case, network error, SMTP error |
| `config.py` | `tests/test_config.py` | Required env values, missing env error, `.env` parsing |
| `email_html.py` | `tests/test_email_html.py` | Email sections and playlist button behavior |
| `enrichment.py` | `tests/test_enrichment.py` | Spotify image/link enrichment |
| `helpers.py` | `tests/test_helpers.py` | Name matching and listening estimate |
| `lastfm.py` | `tests/test_lastfm.py` | Last.fm success, API error, weekly filtering |
| `mailer.py` | `tests/test_mailer.py` | SMTP login and email sending |
| `playlist.py` | `tests/test_playlist.py` | Playlist update, track URI selection, cover upload |
| `spotify_auth.py` | `tests/test_spotify_auth.py` | Token caching and missing refresh token |
| `spotify_api.py` | `tests/test_spotify_api.py` | API error handling and cover upload endpoint |
| `spotify_lookup.py` | `tests/test_spotify_lookup.py` | Spotify track matching |
| `summary.py` | `tests/test_summary.py` | Recap counts and empty input edge case |

## Latest Test Result

```text
Ran 35 tests

OK
```
