# Weekly Spotify Recap

## 1. Introduction

Weekly Spotify Recap is a Python automation project for module M122E. The
project automates a weekly music recap workflow that would otherwise require
checking listening history, calculating statistics manually, creating a Spotify
playlist, and writing an email summary by hand.

The script collects the last 7 days of listening data from Last.fm, calculates
weekly music statistics, enriches the result with Spotify images and links,
creates or updates a Spotify playlist with the top songs, and sends the recap as
a Spotify-style HTML email.

The main benefit is a clear personal overview of weekly listening habits with
less manual work. The generated email shows the most important results in one
place and includes a direct link to the weekly playlist.

## 2. Project Scope

The first complete version focuses on one user and one weekly automation
workflow:

1. Load configuration and secrets from `.env`.
2. Fetch recent tracks from the Last.fm API.
3. Keep only tracks from the last 7 days.
4. Calculate top artists, top songs, top albums, total scrobbles, estimated
   listening time, busiest day, peak listening hour, and latest listen.
5. Search Spotify for matching artists, albums, tracks, cover images, and links.
6. Create or update a private Spotify playlist with the weekly top songs.
7. Upload a custom playlist cover if the configured image exists.
8. Build a Spotify-inspired HTML email.
9. Send the email with Gmail SMTP.
10. Handle common API, runtime, and SMTP errors with readable console messages.

Out of scope: database storage, multi-user support, a web app, Apple Music or
other music platforms, and production-level monitoring.

## 3. Requirements

### Functional Requirements

| Priority | Requirement | Status |
| --- | --- | --- |
| Must | Collect weekly listening data automatically. | Implemented in `src/weekly_spotify_recap/lastfm.py`. |
| Must | Use only the last 7 days of listening history. | Implemented with UTC timestamp filtering in `get_all_tracks_last_7_days()`. |
| Must | Identify top songs, albums, and artists of the week. | Implemented in `src/weekly_spotify_recap/summary.py`. |
| Must | Calculate overall listening statistics. | Implemented: total scrobbles, estimated hours, busiest day, favorite hour, latest track. |
| Must | Create or update a Spotify playlist with the top songs. | Implemented in `src/weekly_spotify_recap/playlist.py`. |
| Must | Send an email summary with recap results and playlist link. | Implemented in `src/weekly_spotify_recap/email_html.py` and `mailer.py`. |
| Must | Use environment variables for API keys, credentials, and settings. | Implemented in `src/weekly_spotify_recap/config.py` and `.env.example`. |
| Must | Provide `requirements.txt` for pip dependencies. | Implemented with `requests>=2.31.0`. |
| Should | Use an email design inspired by Spotify. | Implemented with dark layout, green highlights, rankings, cards, and playlist button. |
| Should | Show rankings and listening time clearly. | Implemented in the HTML email and summary data. |
| Should | Display the playlist link clearly. | Implemented with the "Open your weekly playlist" email button. |
| Should | Handle API and email errors properly. | Implemented in `run()` with readable messages for network/API, runtime, and SMTP login errors. |
| Could | Include album covers and artist images in the email. | Implemented through Spotify enrichment. |
| Could | Add clickable Spotify links for songs, albums, and artists. | Implemented where Spotify returns matching URLs. |
| Could | Upload a custom playlist image. | Implemented when `PLAYLIST_COVER_PATH` points to an existing image. |
| Could | Save past weekly recaps for comparison. | Not implemented. |
| Won't | Add database integration. | Out of scope. |
| Won't | Support multiple music platforms such as Apple Music. | Out of scope. |
| Won't | Build a web app or mobile app. | Out of scope. |

### Non-Functional Requirements

| Area | Requirement | Status |
| --- | --- | --- |
| Usability | The app must be easy to run from PowerShell and Windows Task Scheduler. | Documented in this README. |
| Security | Secrets must not be hard-coded or committed. | `.env` is used locally and should stay ignored by git. |
| Maintainability | Code should be split into clear modules. | Implemented with separate modules for config, APIs, summary, playlist, email, and helpers. |
| Testability | External APIs and SMTP should be testable without real requests. | Implemented with unit tests and mocks. |
| Reliability | Common external service failures should not crash with unclear tracebacks. | Network/API, runtime, and SMTP authentication errors are handled in `main.py`. |
| Performance | The script should finish quickly for normal weekly use. | Last.fm pages are loaded only until tracks older than 7 days are reached; API calls use 20 second timeouts. |
| Portability | Setup should work on a normal Windows development machine. | Uses Python, pip, `.env`, and PowerShell commands. |

## 4. Project Plan

The project follows the waterfall model required by the assignment. The
maintenance phase is out of scope.

| Phase | Main work | Result |
| --- | --- | --- |
| Requirements Analysis | Define the automation goal, benefits, involved systems, and MoSCoW requirements. | Project proposal in `documents/M122E_ProjectProposal_Melih.pdf`. |
| Design | Plan modules, data flow, API interactions, email layout, local deployment, and diagrams. | Activity diagram and component/deployment diagram in `documents/`. |
| Implementation | Build Last.fm loading, summary calculation, Spotify authentication/search/playlist handling, HTML email generation, and Gmail sending. | Working Python script in `src/weekly_spotify_recap/`. |
| Integration and Testing | Test normal flow, empty data, API errors, SMTP errors, playlist behavior, and formatting helpers. | Unit tests in `tests/` and test protocol in `docs/testing-protocol.md`. |
| Deployment | Prepare local configuration and optional Windows Task Scheduler execution. | Script can be run manually or scheduled weekly. |
| Documentation | Document purpose, requirements, design, setup, usage, tests, and limitations. | Final README plus supporting docs and diagrams. |

## 5. Design

The app uses a simple controller-and-components structure. The entry point is
`src/weekly_spotify_recap/main.py`, which coordinates the complete workflow.
Specialized modules handle each separate responsibility.

### Workflow

1. `main.py` starts the run.
2. `config.py` loads `.env` values and checks required variables.
3. `lastfm.py` requests recent Last.fm scrobbles and filters them to the last 7
   days.
4. `summary.py` calculates all weekly statistics.
5. `enrichment.py` uses Spotify lookup helpers to collect image and link data.
6. `playlist.py` creates or updates the Spotify playlist and uploads the cover
   image when available.
7. `email_html.py` builds the final HTML email.
8. `mailer.py` sends the email through Gmail SMTP.
9. `main.py` prints a success message or a readable error message.

### Source Files

| File | Purpose |
| --- | --- |
| `src/weekly_spotify_recap/main.py` | Entry point and high-level workflow controller. |
| `src/weekly_spotify_recap/config.py` | Loads `.env` and exposes shared settings. |
| `src/weekly_spotify_recap/lastfm.py` | Collects recent listening history from Last.fm. |
| `src/weekly_spotify_recap/summary.py` | Calculates recap statistics and rankings. |
| `src/weekly_spotify_recap/enrichment.py` | Builds Spotify-enriched sections for the email. |
| `src/weekly_spotify_recap/spotify_auth.py` | Creates and caches Spotify access tokens. |
| `src/weekly_spotify_recap/spotify_api.py` | Sends low-level Spotify API requests. |
| `src/weekly_spotify_recap/spotify_lookup.py` | Finds matching Spotify artists, albums, and tracks. |
| `src/weekly_spotify_recap/playlist.py` | Creates or updates the weekly playlist. |
| `src/weekly_spotify_recap/email_html.py` | Builds the Spotify-style HTML email. |
| `src/weekly_spotify_recap/mailer.py` | Sends the HTML email through Gmail SMTP. |
| `src/weekly_spotify_recap/helpers.py` | Contains reusable matching and formatting helpers. |
| `scripts/get-spotify-refresh-token.py` | Helper script for creating a Spotify refresh token. |

### External Systems

| System | Used for | Module |
| --- | --- | --- |
| Last.fm API | Reads recent listening history. | `lastfm.py` |
| Spotify Accounts API | Creates app and user access tokens. | `spotify_auth.py` |
| Spotify Web API | Searches metadata, creates/updates playlists, uploads cover image. | `spotify_api.py`, `spotify_lookup.py`, `playlist.py` |
| Gmail SMTP | Sends the weekly recap email. | `mailer.py` |
| Local filesystem | Reads `.env`, requirements, playlist cover image, and source files. | `config.py`, `playlist.py` |
| Windows Task Scheduler | Optional weekly automation trigger. | External Windows setup |
| GitHub | Backup and final project repository. | Repository hosting |

### UML Design Documents

The design documents required by the assignment are stored in `documents/`:

| Document | Purpose |
| --- | --- |
| `documents/detailed-activity-diagram.png` | Detailed UML activity diagram for the script workflow, including decisions and error paths. |
| `documents/detailed-activity-diagram.drawio` | Editable source for the activity diagram. |
| `documents/component-and-deployment-diagram.png` | UML component/deployment diagram showing the Windows PC, Python runtime, local filesystem, scheduler, APIs, and SMTP interaction. |
| `documents/component-and-deployment-diagram.drawio` | Editable source for the component/deployment diagram. |
| `documents/M122E_ProjectProposal_Melih.pdf` | Project proposal context and original scope. |

### Technical Choices

- Python was chosen because the assignment requires automation with a scripting
  language and Python has simple libraries for HTTP requests, SMTP, and testing.
- The script is split into modules instead of one large file to improve
  readability and make unit tests easier.
- Environment variables are used for secrets and account-specific settings.
- `requests` is used for Last.fm and Spotify HTTP APIs.
- Built-in `smtplib` and `email` modules are used for Gmail SMTP.
- Built-in `unittest` and `unittest.mock` are used so tests can run without real
  Last.fm, Spotify, or Gmail calls.
- A local helper script is used for Spotify OAuth because a refresh token is
  needed for playlist modification and image upload permissions.

## 6. Folder Structure

```text
WeeklySpotifyRecap/
|-- assets/
|   `-- playlist-cover.jpg
|-- docs/
|   |-- setup.md
|   `-- testing-protocol.md
|-- documents/
|   |-- M122E_ProjectProposal_Melih.pdf
|   |-- component-and-deployment-diagram.drawio
|   |-- component-and-deployment-diagram.png
|   |-- detailed-activity-diagram.drawio
|   `-- detailed-activity-diagram.png
|-- logs/
|   `-- weekly_spotify_recap.log
|-- scripts/
|   `-- get-spotify-refresh-token.py
|-- src/
|   `-- weekly_spotify_recap/
|       |-- config.py
|       |-- email_html.py
|       |-- enrichment.py
|       |-- helpers.py
|       |-- lastfm.py
|       |-- mailer.py
|       |-- main.py
|       |-- playlist.py
|       |-- spotify_api.py
|       |-- spotify_auth.py
|       |-- spotify_lookup.py
|       `-- summary.py
|-- tests/
|   `-- test_*.py
|-- .env.example
|-- requirements.txt
`-- README.md
```

## 7. Installation

These instructions assume a Windows machine with PowerShell.

### 7.1 Install Python

Install Python 3.11 or newer from:

```text
https://www.python.org/downloads/
```

During installation, enable **Add Python to PATH**.

Check the installation:

```powershell
py --version
```

### 7.2 Clone the Project

```powershell
cd C:\repos
git clone <your-repository-url>
cd WeeklySpotifyRecap
```

### 7.3 Create a Virtual Environment

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

### 7.4 Create `.env`

Copy the example file:

```powershell
Copy-Item .env.example .env
```

Fill in the values:

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

Do not commit `.env` to git.

## 8. API And Account Setup

### 8.0 Visual Setup Overview

Official setup links:

| Topic | Official link | Use |
| --- | --- | --- |
| Python | [Python downloads](https://www.python.org/downloads/) | Install Python for running the script and tests. |
| Last.fm API | [Last.fm API](https://www.last.fm/api) | Create the API account and get `LASTFM_API_KEY`. |
| Spotify Developer Dashboard | [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) | Create the Spotify app and copy client credentials. |
| Spotify authorization code flow | [Authorization code flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow) | Understand the refresh-token login flow. |
| Spotify scopes | [Spotify scopes](https://developer.spotify.com/documentation/web-api/concepts/scopes) | Check playlist and image-upload permissions. |
| Google app passwords | [Google app passwords](https://support.google.com/accounts/answer/185833) | Create the Gmail app password. |
| Gmail SMTP settings | [Gmail SMTP settings](https://support.google.com/mail/answer/7126229) | Check Gmail SMTP access and settings. |
| Windows Task Scheduler | [Task Scheduler documentation](https://learn.microsoft.com/windows/win32/taskschd/task-scheduler-start-page) | Learn how Windows scheduled tasks work. |

### 8.1 Last.fm API

1. Go to `https://www.last.fm/api`.
2. Log in with your Last.fm account.
3. Create an API account.
4. Copy the API key.
5. Add it to `.env` as `LASTFM_API_KEY`.
6. Add your Last.fm username as `LASTFM_USERNAME`.

The app uses Last.fm because Spotify does not provide a simple personal play
history endpoint for this type of weekly recap.

### 8.2 Spotify Developer App

1. Go to `https://developer.spotify.com/dashboard`.
2. Log in with your Spotify account.
3. Create a new app.
4. Add this redirect URI exactly:

```text
http://127.0.0.1:8888/callback
```

5. Select Spotify Web API access.
6. Copy the client ID and client secret.
7. Add them to `.env` as `SPOTIFY_CLIENT_ID` and
   `SPOTIFY_CLIENT_SECRET`.

### 8.3 Spotify Refresh Token

The playlist feature needs a refresh token with playlist and image-upload
permissions.

Run this from the project root:

```powershell
$env:SPOTIFY_CLIENT_ID="your-client-id"
$env:SPOTIFY_CLIENT_SECRET="your-client-secret"
py scripts/get-spotify-refresh-token.py
```

The script opens a Spotify login page. After approval, it prints:

```env
SPOTIFY_REFRESH_TOKEN=...
```

Copy that line into `.env`.

### 8.4 Spotify Playlist Settings

`SPOTIFY_PLAYLIST_ID` is optional.

- If it is empty, the app creates a new private playlist.
- If it is set, the app updates that existing playlist.

For repeated weekly updates, copy the playlist ID from Spotify and save it in
`.env`. The playlist ID is the long ID in the Spotify playlist URL.

`PLAYLIST_COVER_PATH` is optional. If the file exists, the app uploads it as the
playlist cover image.

### 8.5 Gmail SMTP

The email is sent with Gmail SMTP. Use an app password, not your normal Gmail
password.

1. Open `https://myaccount.google.com/security`.
2. Enable 2-Step Verification.
3. Open `https://myaccount.google.com/apppasswords`.
4. Create an app password for this project.
5. Add the values to `.env`:

```env
GMAIL_ADDRESS=your-gmail-address@gmail.com
GMAIL_APP_PASSWORD=your-16-digit-app-password
RECIPIENT_EMAIL=receiver@example.com
```

## 9. Running The App

Run the script from the project root:

```powershell
.\.venv\Scripts\python.exe src\weekly_spotify_recap\main.py
```

Expected console flow:

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

If no Last.fm scrobbles are found in the last 7 days, the app stops after
printing:

```text
No scrobbles found in the last 7 days.
```

## 10. Windows Task Scheduler Setup

Task Scheduler is optional, but it fits the project goal because the recap should
run automatically every week.

### 10.1 Create The Task

1. Open Windows Start Menu.
2. Search for **Task Scheduler**.
3. Click **Create Basic Task**.
4. Name it `Weekly Spotify Recap`.
5. Choose **Weekly**.
6. Choose a day and time, for example Monday at 09:00.
7. Choose **Start a program**.

### 10.2 Program Settings

Use values like these, adjusted to your local project path:

```text
Program/script:
C:\repos\WeeklySpotifyRecap\.venv\Scripts\python.exe

Add arguments:
src\weekly_spotify_recap\main.py

Start in:
C:\repos\WeeklySpotifyRecap
```

### 10.3 Test The Task

1. Right-click the task.
2. Click **Run**.
3. Check your email inbox.
4. Check the Spotify playlist.
5. If something fails, run the script manually in PowerShell to see the error
   message.

## 11. Testing

The automated tests use Python `unittest`. They mock external services, so they
do not call the real Last.fm API, Spotify API, or Gmail SMTP server.

Run all tests:

```powershell
$env:PYTHONPATH="src"
py -m unittest discover -s tests -p "test_*.py" -v
```

Latest local test execution:

```text
Ran 34 tests

OK
```

The latest test run was executed on 17.06.2026 with the command above.

### Test Protocol

| ID | Area | Test file | Main criteria | Result |
| --- | --- | --- | --- | --- |
| TC-01 | Main workflow | `tests/test_app_main.py` | Happy path calls Last.fm loading, summary, Spotify enrichment, playlist update, and email sending. | Passed |
| TC-02 | Empty listening history | `tests/test_app_main.py` | App stops cleanly when no weekly tracks are found. | Passed |
| TC-03 | Network/API error handling | `tests/test_app_main.py` | Network errors are caught and printed clearly. | Passed |
| TC-04 | SMTP authentication error | `tests/test_app_main.py` | SMTP login errors are caught and explained. | Passed |
| TC-05 | Configuration | `tests/test_config.py` | `.env` values load correctly and missing required values raise clear errors. | Passed |
| TC-06 | HTML email | `tests/test_email_html.py` | Email contains main sections and hides playlist button when no URL exists. | Passed |
| TC-07 | Spotify enrichment | `tests/test_enrichment.py` | Hero, artist, track, and album sections are built from Spotify lookup data. | Passed |
| TC-08 | Helpers | `tests/test_helpers.py` | Name normalization, album matching, album lookup, and listening-hour estimation work. | Passed |
| TC-09 | Last.fm API | `tests/test_lastfm.py` | Requests are built correctly, API errors are handled, and old tracks are filtered. | Passed |
| TC-10 | Mailer | `tests/test_mailer.py` | Gmail SMTP login and message sending are called correctly. | Passed |
| TC-11 | Playlist | `tests/test_playlist.py` | Playlist update, track URI deduplication, missing matches, and cover upload behavior are tested. | Passed |
| TC-12 | Spotify API | `tests/test_spotify_api.py` | Spotify request errors and image upload endpoint are handled. | Passed |
| TC-13 | Spotify auth | `tests/test_spotify_auth.py` | App/user token caching and missing refresh token behavior are tested. | Passed |
| TC-14 | Spotify lookup | `tests/test_spotify_lookup.py` | Track search returns matching tracks and rejects non-matches. | Passed |
| TC-15 | Summary | `tests/test_summary.py` | Weekly counts and empty input behavior are correct. | Passed |

Additional test details are documented in `docs/testing-protocol.md`.

## 12. Evidence

Project evidence is stored in the repository:

| Evidence | Location |
| --- | --- |
| Project proposal | `documents/M122E_ProjectProposal_Melih.pdf` |
| Activity diagram | `documents/detailed-activity-diagram.png` |
| Component/deployment diagram | `documents/component-and-deployment-diagram.png` |
| Test protocol | `docs/testing-protocol.md` |
| Setup guide | `docs/setup.md` |
| Local run log | `logs/weekly_spotify_recap.log` |

The local run log contains evidence of a successful email and playlist run from
03.06.2026.

## 13. Troubleshooting

Official help pages:

| Problem area | Official link |
| --- | --- |
| Last.fm API key or API response problems | [Last.fm API](https://www.last.fm/api) |
| Spotify developer app setup | [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) |
| Spotify authorization and refresh token flow | [Authorization code flow](https://developer.spotify.com/documentation/web-api/tutorials/code-flow) |
| Spotify permissions/scopes | [Spotify scopes](https://developer.spotify.com/documentation/web-api/concepts/scopes) |
| Gmail app password problems | [Google app passwords](https://support.google.com/accounts/answer/185833) |
| Gmail SMTP settings | [Gmail SMTP settings](https://support.google.com/mail/answer/7126229) |
| Windows Task Scheduler setup | [Task Scheduler documentation](https://learn.microsoft.com/windows/win32/taskschd/task-scheduler-start-page) |
| Python installation | [Python downloads](https://www.python.org/downloads/) |

### Missing Environment Variable

If the app prints a message like:

```text
Missing required environment variable: LASTFM_API_KEY
```

Check that `.env` exists in the project root and contains the required value.

### Last.fm Or Spotify Request Fails

Check:

- Internet connection is available.
- API keys and client credentials are correct.
- Last.fm username is spelled correctly.
- Spotify refresh token exists and was created with the required scopes.

### Spotify Playlist Cannot Be Updated

Check:

- `SPOTIFY_REFRESH_TOKEN` is set.
- The Spotify app has the redirect URI `http://127.0.0.1:8888/callback`.
- The refresh token was created with playlist permissions.
- `SPOTIFY_PLAYLIST_ID` belongs to the same Spotify user.

### Gmail Does Not Send

Check:

- Gmail 2-Step Verification is enabled.
- `GMAIL_APP_PASSWORD` is an app password, not the normal account password.
- `GMAIL_ADDRESS` and `RECIPIENT_EMAIL` are correct.

### Task Scheduler Does Not Run

Check:

- **Program/script** points to `.venv\Scripts\python.exe`.
- **Add arguments** is `src\weekly_spotify_recap\main.py`.
- **Start in** is the project root.
- The Windows user running the task can access the project folder.
- The computer is awake at the scheduled time.

## 14. Security Notes

These values are private and must not be committed:

- Last.fm API key
- Spotify client secret
- Spotify refresh token
- Gmail app password
- Email addresses in `.env`

The repository includes `.env.example` only as a template. The real `.env` file
should stay local.

## 15. Limitations

- Listening data depends on Last.fm scrobbling. If tracks are not scrobbled, the
  app cannot include them.
- Spotify search can fail to match some tracks, albums, or artists if names
  differ between Last.fm and Spotify.
- Estimated listening time uses an average song length of 3.5 minutes, not exact
  track durations.
- The project is designed for one local user, not multiple accounts.
- Past recap history is not stored in a database.

## 16. Disclaimer

This project is a school automation project for module M122E. It is intended for
learning and personal use, not production use.
