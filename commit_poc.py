"""POC: edit a tracked file and create one local git commit with a given message."""

from __future__ import annotations

import argparse
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor

# git mutates shared repo state (the index, HEAD, .git/index.lock), so the
# actual commit must stay serialized even though the worker threads run
# concurrently. This does not make the git calls themselves faster.
GIT_LOCK = threading.Lock()


def commit(message: str) -> None:
    with GIT_LOCK:
        subprocess.run(
            ["git", "commit", "--allow-empty", "--no-verify", "--no-gpg-sign", "-m", message],
            check=True,
        )


def do_one(message: str, index: int, total: int) -> None:
    commit(f"{message} {index}")
    print(f"Committed {index}/{total}: {message!r}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append a line to a file and commit it with the given message, n times."
    )
    parser.add_argument("message", help="commit message to use")
    parser.add_argument(
        "-n", "--count", type=int, default=1, help="number of commits to create (default: 1)"
    )
    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=1,
        help="worker threads (default: 1); git commits are still serialized internally",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.count < 1:
        raise SystemExit("count must be at least 1")
    if args.threads < 1:
        raise SystemExit("threads must be at least 1")

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [
            executor.submit(do_one, args.message, i, args.count)
            for i in range(1, args.count + 1)
        ]
        for future in futures:
            future.result()


if __name__ == "__main__":
    main()
