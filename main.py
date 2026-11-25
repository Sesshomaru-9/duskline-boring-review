#!/usr/bin/env python3
"""Duskline Boring Review — one funny, true line reviewing the most boring
everyday object we could name: the lint roller.

The entry is a single line, at most 200 characters, written to
$MAKEFUN_OUTPUT_DIR/entry.txt. The program is deterministic (the same line
every run), uses only the Python 3.13 standard library, and never writes
anywhere except $MAKEFUN_OUTPUT_DIR.
"""

import os
import sys

# The entry: a lint roller is genuinely boring and everyday, and the joke
# comes from how it really behaves — it peels other people's lint and hair
# off their clothes, and the moment its own sheet is dirty it is thrown
# away. The turn ("fired the moment it gets dirty") lands early and the
# last words ("everyone else's mess") sharpen it.
ENTRY = (
    "The lint roller: fired the moment it gets dirty, "
    "after a lifetime of cleaning up everyone else's mess."
)

MAX_CHARS = 200
MIN_CHARS = 1


def _validate_entry(text):
    """Gate matching the kit's sealed scorer: UTF-8 text of 1 to 200
    characters, not only whitespace, on a single line, with no control
    characters and no more than 200 bytes on disk."""
    if not isinstance(text, str):
        return False
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        return False
    if not text.strip():
        return False
    if "\n" in text or "\r" in text:
        return False
    # Control characters (tab, bell, escapes, ...) must not sneak into a
    # one-line review, and the written file must itself fit the 200-byte
    # bound even if a future edit swaps in multi-byte characters.
    if any(ord(ch) < 0x20 for ch in text):
        return False
    try:
        encoded = text.encode("utf-8")
    except UnicodeEncodeError:
        return False
    if not (MIN_CHARS <= len(encoded) <= MAX_CHARS):
        return False
    return True


def _resolve_output_dir():
    """Return the output directory from MAKEFUN_OUTPUT_DIR, or None.

    The program writes only here — never into the repo or anywhere else.
    """
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return None
    return out_dir


def main():
    if not _validate_entry(ENTRY):
        print("entry failed validation", file=sys.stderr)
        return 1

    out_dir = _resolve_output_dir()
    if out_dir is None:
        return 1

    try:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "entry.txt")
        with open(out_path, "w", encoding="utf-8", newline="") as f:
            f.write(ENTRY)
    except OSError as exc:
        # Never crash if the output dir is unwritable: warn and exit 0.
        print(f"warning: could not write entry.txt: {exc}", file=sys.stderr)
        return 0

    # Read-back verification: what landed on disk must be exactly the entry.
    try:
        with open(out_path, "r", encoding="utf-8") as f:
            written = f.read()
    except OSError as exc:
        print(f"warning: could not read back entry.txt: {exc}", file=sys.stderr)
        return 0
    if written != ENTRY or not _validate_entry(written):
        print("warning: read-back verification failed", file=sys.stderr)
        return 0

    print(f"wrote entry.txt ({len(ENTRY)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
