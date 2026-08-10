"""POC: edit a tracked file and create one local git commit with a given message."""

from __future__ import annotations

import argparse
import datetime
import subprocess
from pathlib import Path

LOG_FILE = Path("poc_log.txt")


def append_entry(message: str, index: int) -> None:
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    with LOG_FILE.open("a", encoding="utf-8") as handle:
        handle.write(f"{timestamp} {message} ({index})\n")


def commit(message: str) -> None:
    subprocess.run(["git", "add", str(LOG_FILE)], check=True)
    subprocess.run(["git", "commit", "-m", message], check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append a line to a file and commit it with the given message, n times."
    )
    parser.add_argument("message", help="commit message to use")
    parser.add_argument(
        "-n", "--count", type=int, default=1, help="number of commits to create (default: 1)"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.count < 1:
        raise SystemExit("count must be at least 1")

    for i in range(1, args.count + 1):
        append_entry(args.message, i)
        commit(f"{args.message} {i}")
        print(f"Committed {i}/{args.count}: {args.message!r}")


if __name__ == "__main__":
    main()
