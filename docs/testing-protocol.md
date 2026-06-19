# Testing Protocol

Date: 03.06.2026

Project: Weekly Spotify Recap

Testing type: White-box unit testing with Python `unittest`

## Test Setup

Run all tests with:

```powershell
$env:PYTHONPATH="src"
py -m unittest discover -p "test_*.py" -v
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
| `app_logging.py` | `test_app_logging.py` | Log file creation and logging helper messages |
| `main.py` | `test_main.py` | Entry point call, network error, SMTP error |
| `config.py` | `test_config.py` | Required env values, missing env error, `.env` parsing |
| `email_sender.py` | `test_email_sender.py` | SMTP login and email sending |
| `lastfm_client.py` | `test_lastfm_client.py` | Last.fm success, API error, weekly filtering |
| `music_helpers.py` | `test_music_helpers.py` | Name matching and listening estimate |
| `recap_email_builder.py` | `test_recap_email_builder.py` | Email sections and playlist button behavior |
| `recap_summary.py` | `test_recap_summary.py` | Recap counts and empty input edge case |
| `recap_workflow.py` | `test_recap_workflow.py` | Happy path and no-track edge case |
| `spotify_api_client.py` | `test_spotify_api_client.py` | API error handling and cover upload endpoint |
| `spotify_enrichment.py` | `test_spotify_enrichment.py` | Spotify image/link enrichment |
| `spotify_playlist.py` | `test_spotify_playlist.py` | Playlist update, track URI selection, cover upload |
| `spotify_search.py` | `test_spotify_search.py` | Spotify track matching |
| `spotify_token_manager.py` | `test_spotify_token_manager.py` | Token caching and missing refresh token |

## Latest Test Result

```text
Ran 40 tests

OK
```
