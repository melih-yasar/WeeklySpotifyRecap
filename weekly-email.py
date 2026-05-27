from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

sys.path.insert(0, str(SRC))

from weekly_spotify_recap.cli import run  # noqa: E402


if __name__ == "__main__":
    run()
