#!/usr/bin/env python3
"""Create a dated handoff brief with pre-filled template sections.

Creates .zcode/handoffs/<date>-<topic>.md under the project root (or
an explicit --target). Refuses to overwrite a non-empty file unless
--force is given.

Exit codes:
  0 = created (or overwrote with --force)
  3 = refused: target exists and is non-empty (use --force to overwrite)
  4 = bad arguments (no topic, bad date, etc.)

Stdlib only, cross-OS.
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

SLUG_RE = re.compile(r"[^a-z0-9-]+")


def slugify(topic):
    s = topic.strip().lower()
    s = SLUG_RE.sub("-", s).strip("-")
    return s[:60]


def default_target(root, topic, date):
    return Path(root) / ".zcode" / "handoffs" / "{}-{}.md".format(date, slugify(topic))


def template(args, date, topic, goal):
    lines = [
        "# Handoff: {0}".format(topic),
        "",
        "Date: {0}".format(date),
        "Source session: {0}".format(args.source_session or "unknown"),
        "",
        "## Goal",
        "",
        "{0}".format(goal or "TODO: fill from the user's original request, verbatim"),
        "",
        "## Decisions made",
        "",
        "| Decision | Reason | Evidence |",
        "| --- | --- | --- |",
        "| (none recorded yet) | | |",
        "",
        "## Invariants / constraints",
        "",
        "- (none found; say so rather than guess)",
        "",
        "## File map",
        "",
        "| File | What was done | State |",
        "| --- | --- | --- |",
        "| | | |",
        "",
        "## Current state",
        "",
        "What runs, what does not, and the command that shows it:",
        "",
        "- (fill with observed output, trimmed)",
        "",
        "## Next steps",
        "",
        "1. (first step, ending at a verifiable state)",
        "",
        "## Open questions",
        "",
        "- (everything without a pointer lands here)",
        "",
        "## Update log",
        "",
        "- {0}: created".format(date),
        "",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="Create a dated handoff brief with template sections "
                    "pre-filled under .zcode/handoffs/.")
    ap.add_argument("--topic", required=True,
                    help="Short topic; used in the filename.")
    ap.add_argument("--goal", default="",
                    help="One-sentence goal of the session, pre-filled.")
    ap.add_argument("--date", default=None,
                    help="YYYY-MM-DD (default: today).")
    ap.add_argument("--root", default=".",
                    help="Project root (default: current dir).")
    ap.add_argument("--target", default=None,
                    help="Explicit target path, overriding the default.")
    ap.add_argument("--source-session", default=None,
                    help="Identifier of the session that produced this brief.")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite an existing non-empty file.")
    args = ap.parse_args()

    if args.date:
        try:
            datetime.datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("error: --date must be YYYY-MM-DD", file=sys.stderr)
            return 4
    else:
        args.date = datetime.date.today().isoformat()

    root = Path(args.root)
    if not root.is_dir():
        print("error: project root not found: {0}".format(args.root),
              file=sys.stderr)
        return 4

    if args.target:
        target = Path(args.target)
        if not target.is_absolute():
            target = root / target
    else:
        target = default_target(root, args.topic, args.date)

    if target.exists() and target.stat().st_size > 0 and not args.force:
        print("refused: {0} exists and is non-empty; "
              "pass --force to overwrite, or use --target for a new file "
              "(a refresh should update this file in place instead)"
              .format(target), file=sys.stderr)
        return 3

    target.parent.mkdir(parents=True, exist_ok=True)
    text = template(args, args.date, args.topic, args.goal)
    target.write_text(text, encoding="utf-8")
    print("created: {0}".format(target))
    return 0


if __name__ == "__main__":
    sys.exit(main())
