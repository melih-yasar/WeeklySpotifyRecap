import sys


# This lets Python find the project files inside the src folder.
sys.path.append("src")

from weekly_spotify_recap.cli import run


run()
