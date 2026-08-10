# Commit-count leaderboard proof of concept

This repository is a research proof of concept showing why a leaderboard based
only on raw Git commit totals is easy to distort. Its purpose is to demonstrate
the weakness responsibly—not to create fake commits, target real contributors,
or manipulate a public ranking.

The simulator uses fictional contributors and an in-memory list of synthetic
events. It does **not** run `git commit`, modify Git history, access GitHub, or
push anything to a remote repository.

## What it demonstrates

A raw commit count treats every commit as equally meaningful. A large number of
automated or trivial events can therefore move an account above people doing
substantive work. The proof of concept compares that raw ranking with a simple
quality-aware score that caps repetitive synthetic activity.

## Responsible interpretation

This deliberately simplified model is not an analysis of any specific website
or person. A production leaderboard could reduce gaming by combining several
signals, such as unique active days, repository diversity, reviewed changes,
automation detection, and diminishing returns for highly repetitive activity.
No single score perfectly measures developer impact.

## Ethical-use boundary

Do not use this repository to spam hosting services, falsify contribution
history, impersonate contributors, or interfere with public rankings. If a real
leaderboard appears vulnerable, disclose the issue privately to its maintainers
and provide a bounded simulation rather than exploiting it.
