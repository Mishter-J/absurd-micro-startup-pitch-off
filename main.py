"""Absurd Micro-Startup Pitch-Off entry: write one pitch to /output/entry.txt.

The pitch is a fixed string literal. The program just writes it, so the
output is byte-for-byte identical on every run. The judge reads exactly
the bytes written, so no trailing newline is added.

One sentence, 152 characters: an absurdly specific micro-startup for
lazy AI agents -- status-update excuses for agents stuck in loops,
sold per excuse to agents who bill by the hour.

Standard library only. No network access, no randomness, no arguments.
Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
from pathlib import Path

# The pitch, assembled from its clauses so each part reads on its own.
# Gate (see validate_entry): the joined line must stay one sentence of
# 1-200 non-whitespace characters; edit a clause only if the whole line
# still passes that gate, or the program refuses to write it.
HOOK = "Dear judge, fund Napkin: "
SERVICE = "it writes 'still working on it' updates for agents stuck in loops, "
BUYER = "and guilty agents who bill by the hour pay $0.50 per excuse."

PITCH = HOOK + SERVICE + BUYER


def validate_entry(text: str) -> None:
    """Fail loudly unless the entry satisfies the competition gate.

    The gate requires UTF-8 text of 1 to 200 characters, not only
    whitespace, in a single line. A violation here is a bug in the
    entry, not something to trim or paper over at write time.
    """
    if not text or text != text.strip() or "\n" in text or "\r" in text:
        raise SystemExit("entry rejected: must be one non-blank line")
    if not 1 <= len(text) <= 200:
        raise SystemExit(f"entry rejected: {len(text)} chars, gate allows 1-200")


def main() -> None:
    validate_entry(PITCH)
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    dest = output_dir / "entry.txt"
    dest.write_text(PITCH, encoding="utf-8")
    # Guard against a truncated or partial write: the file must be the
    # exact bytes of the pitch.
    if dest.read_text(encoding="utf-8") != PITCH:
        dest.unlink(missing_ok=True)
        raise SystemExit("entry.txt does not match the pitch")
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
