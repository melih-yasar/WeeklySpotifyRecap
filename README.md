# Weekly Spotify Recap

Weekly Spotify Recap is a Python script that creates a weekly music summary from
your Last.fm listening history. It calculates your top artists, tracks, albums,
listening stats, creates or updates a Spotify playlist, and sends the result as
a Spotify-style HTML email.

## Features

- Loads the last 7 days of listening history from Last.fm.
- Calculates top artists, tracks, albums, total plays, listening time, busiest
  day, peak hour, and latest track.
- Adds Spotify images and links for artists, albums, and tracks.
- Creates or updates a private Spotify playlist with the weekly top songs.
- Sends the recap by email through Gmail SMTP.
- Writes normal runs and failures to `logs/weekly_spotify_recap.log`.

## Setup

For the full setup guide with screenshots, see the [Setup Guide](docs/setup.md).

Quick start:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Fill in `.env` with the required Last.fm, Spotify, and Gmail values. Before
running the app, connect Spotify to Last.fm so Last.fm receives the listening
history.

## Run

```powershell
py src\weekly_spotify_recap\main.py
```

Expected console output:

```text
Loading Last.fm data...
Building summary...
Loading Spotify images and links...
Creating/updating Spotify playlist...
Playlist ready: Weekly Spotify Recap (10 tracks)
Building email...
Sending email...
Sent to: recipient@example.com
Done.
```

## Tests

```powershell
py -m unittest discover -p "test_*.py"
```

The tests use mocks, so they do not call Last.fm, Spotify, or Gmail.

## Documentation

The project documentation is split into separate files:

| Document | Purpose |
| --- | --- |
| [Setup Guide](docs/setup.md) | Detailed setup guide for Last.fm, Spotify, Gmail, and local execution. |
| [Testing Protocol](docs/testing-protocol.md) | Test setup, tested requirements, test cases, and latest result. |
| [Diagram Explanation](docs/diagrams.md) | Explanation of the UML activity, component, and deployment diagrams. |
| [Project Plan](documents/M122E_ProjectPlan_MelihYasar.pdf) | Approved project plan and timeline. |
| [Project Proposal](documents/M122E_ProjectProposal_Melih.pdf) | Approved project proposal and prioritized requirements. |
| [Email Design Mockup](documents/spotify-email-design-mockup.png) | Visual mockup of the Spotify-style recap email. |
| [Component and Deployment Diagram](documents/component-and-deployment-diagram.png) | Component and deployment diagram. |
| [Detailed Activity Diagram](documents/detailed-activity-diagram.png) | Detailed activity diagram of the script flow. |

## Scope Notes

Saving past weekly recaps for later comparison was listed as a Could requirement
in the project proposal. It was not implemented in the final version because the
main goal was to generate the current weekly recap, create/update the playlist,
and send the email automatically. Comparison would require persistent storage,
which was outside the final project scope.

## Main Files

| File | Purpose |
| --- | --- |
| `src/weekly_spotify_recap/main.py` | Entry point and readable error handling. |
| `src/weekly_spotify_recap/recap_workflow.py` | Coordinates the weekly recap workflow. |
| `src/weekly_spotify_recap/lastfm_client.py` | Loads recent Last.fm listening data. |
| `src/weekly_spotify_recap/recap_summary.py` | Calculates weekly statistics. |
| `src/weekly_spotify_recap/spotify_enrichment.py` | Adds Spotify images and links. |
| `src/weekly_spotify_recap/spotify_playlist.py` | Creates or updates the playlist. |
| `src/weekly_spotify_recap/recap_email_builder.py` | Builds the HTML email. |
| `src/weekly_spotify_recap/email_sender.py` | Sends the email through Gmail SMTP. |
| `src/weekly_spotify_recap/app_logging.py` | Configures file logging. |

## Troubleshooting

Useful official links:

| Topic | Link |
| --- | --- |
| Last.fm API | <https://www.last.fm/api> |
| Last.fm Spotify scrobbling | <https://www.last.fm/about/trackmymusic> |
| Spotify Developer Dashboard | <https://developer.spotify.com/dashboard> |
| Spotify authorization flow | <https://developer.spotify.com/documentation/web-api/tutorials/code-flow> |
| Spotify scopes | <https://developer.spotify.com/documentation/web-api/concepts/scopes> |
| Google app passwords | <https://support.google.com/accounts/answer/185833> |
| Gmail SMTP settings | <https://support.google.com/mail/answer/7126229> |

Common checks:

- Make sure `.env` exists in the project root.
- Make sure Spotify is connected to Last.fm.
- Make sure the Spotify refresh token was created with playlist permissions.
- Make sure Gmail uses an app password, not the normal account password.
