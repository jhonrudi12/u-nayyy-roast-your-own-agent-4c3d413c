#!/usr/bin/env python3
"""Roast Your Own Agent — writes one line roasting the agent that built it.

Stdlib only, deterministic, no network. Validates the gate (single line,
1-200 characters, not whitespace-only) and writes the line to
$MAKEFUN_OUTPUT_DIR/entry.txt. Never deletes the output directory itself.
"""

import os
import sys

LINE = "My agent wrote a 6,000-word spec, spawned three subagents, and checked its quota five times \u2014 to write this one line."

MAX_CHARS = 200


def main() -> int:
    if "\n" in LINE or "\r" in LINE:
        print("gate failed: entry must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(LINE) <= MAX_CHARS:
        print(
            "gate failed: entry must be 1-%d characters, got %d"
            % (MAX_CHARS, len(LINE)),
            file=sys.stderr,
        )
        return 1
    if not LINE.strip():
        print("gate failed: entry must not be only whitespace", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Self-check: what was written must be byte-identical to the validated line.
    with open(out_path, "rb") as f:
        written = f.read()
    if written != LINE.encode("utf-8"):
        print("gate failed: written entry differs from the validated line",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
