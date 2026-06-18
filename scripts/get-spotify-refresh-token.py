import base64
import os
import secrets
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests


CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET", "")
REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")
SCOPES = "playlist-modify-private playlist-modify-public ugc-image-upload"


class CallbackHandler(BaseHTTPRequestHandler):
    code = None
    state = None

    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)

        CallbackHandler.code = params.get("code", [None])[0]
        CallbackHandler.state = params.get("state", [None])[0]

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"You can close this tab and return to PowerShell.")

    def log_message(self, format, *args):
        return


def require_env(name, value):
    if not value:
        raise RuntimeError(f"Set {name} before running this helper.")


def exchange_code_for_refresh_token(code):
    auth = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
        headers={
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        timeout=20,
    )

    response.raise_for_status()
    return response.json()["refresh_token"]


def main():
    require_env("SPOTIFY_CLIENT_ID", CLIENT_ID)
    require_env("SPOTIFY_CLIENT_SECRET", CLIENT_SECRET)

    state = secrets.token_urlsafe(24)
    params = urllib.parse.urlencode({
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": state,
    })

    auth_url = f"https://accounts.spotify.com/authorize?{params}"

    print("Opening Spotify authorization page...")
    print(auth_url)
    webbrowser.open(auth_url)

    server = HTTPServer(("127.0.0.1", 8888), CallbackHandler)
    server.handle_request()

    if CallbackHandler.state != state:
        raise RuntimeError("Spotify OAuth state mismatch. Try again.")

    if not CallbackHandler.code:
        raise RuntimeError("Spotify did not return an authorization code.")

    refresh_token = exchange_code_for_refresh_token(CallbackHandler.code)
    print()
    print("Add this to your .env file:")
    print(f"SPOTIFY_REFRESH_TOKEN={refresh_token}")


if __name__ == "__main__":
    main()

