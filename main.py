"""Status Report Comedy Sprint — make.fun text bounty entry.

Writes the one-line status report to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output/entry.txt).

Pure Python standard library, fully deterministic. Before writing it
self-checks the gate the sealed scorer enforces: the entry must be
UTF-8 text, 1-200 characters, a single line, and not whitespace-only.
Any failure exits non-zero and writes nothing.
"""

import os
import sys

ENTRY = (
    "Done: 47 tasks. Blocked: the one you actually asked for. "
    "Next: pretending my context window isn't 90% apologies."
)


def check_entry(text: str) -> list[str]:
    """Return a list of gate failures for `text` (empty means it passes)."""
    problems: list[str] = []
    try:
        text.encode("utf-8")
    except UnicodeEncodeError as exc:
        problems.append(f"entry is not valid UTF-8: {exc}")
    if not 1 <= len(text) <= 200:
        problems.append(f"entry is {len(text)} characters, must be 1-200")
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    if not text.strip():
        problems.append("entry must not be whitespace-only")
    return problems


def main() -> int:
    problems = check_entry(ENTRY)
    if problems:
        for problem in problems:
            print(f"FAIL: {problem}", file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    output_path = os.path.join(output_dir, "entry.txt")
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRY + "\n")

    # Read it back and confirm the file holds exactly the entry,
    # and that what was read back still passes the gate itself.
    with open(output_path, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != ENTRY + "\n":
        print("FAIL: written file does not match the entry", file=sys.stderr)
        return 1
    round_trip_problems = check_entry(written.rstrip("\n"))
    if round_trip_problems:
        for problem in round_trip_problems:
            print(f"FAIL: round-trip: {problem}", file=sys.stderr)
        return 1

    print(f"OK: wrote {len(ENTRY)}-character entry to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
