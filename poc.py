"""Simulate commit-count inflation without creating Git commits."""

from __future__ import annotations

import argparse
from dataclasses import dataclass


@dataclass(frozen=True)
class Contributor:
    name: str
    substantive_events: int
    synthetic_events: int = 0

    @property
    def raw_count(self) -> int:
        return self.substantive_events + self.synthetic_events

    @property
    def quality_aware_score(self) -> int:
        """Give repetitive activity sharply diminishing influence."""
        synthetic_credit = min(self.synthetic_events, 25)
        return self.substantive_events + synthetic_credit


def rankings(contributors: list[Contributor], score: str) -> list[Contributor]:
    if score == "raw":
        key = lambda contributor: contributor.raw_count
    elif score == "quality":
        key = lambda contributor: contributor.quality_aware_score
    else:
        raise ValueError(f"unknown score: {score}")
    return sorted(contributors, key=key, reverse=True)


def render(title: str, contributors: list[Contributor], score: str) -> str:
    lines = [title, "=" * len(title)]
    for position, contributor in enumerate(rankings(contributors, score), 1):
        value = (
            contributor.raw_count
            if score == "raw"
            else contributor.quality_aware_score
        )
        lines.append(f"{position:>2}. {contributor.name:<20} {value:>8,}")
    return "\n".join(lines)


def simulate(synthetic_events: int) -> list[Contributor]:
    if synthetic_events < 0:
        raise ValueError("synthetic events cannot be negative")
    return [
        Contributor("Asha (fictional)", 12_400),
        Contributor("Baraka (fictional)", 9_750),
        Contributor("Neema (fictional)", 7_100),
        Contributor("POC account", 3, synthetic_events),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Model leaderboard inflation without touching Git history."
    )
    parser.add_argument(
        "--synthetic-events",
        type=int,
        default=45_000,
        help="in-memory event count to model (default: 45000)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        contributors = simulate(args.synthetic_events)
    except ValueError as error:
        raise SystemExit(str(error)) from error

    print(render("Raw commit-count ranking", contributors, "raw"))
    print()
    print(render("Quality-aware ranking", contributors, "quality"))
    print(
        "\nSimulation only: no repositories, commits, or remote services were changed."
    )


if __name__ == "__main__":
    main()
