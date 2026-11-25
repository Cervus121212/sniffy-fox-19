#!/usr/bin/env python3
"""Roast Your Fridge — make.fun bounty entry.

Writes one line to /output/entry.txt: a roast of the entrant's own
fridge. The line is fixed and deterministic: the program takes no
input, reads nothing from the network or disk, and always emits the
same single line.

Why this line: the house judge weighs, in order, whether the line
roasts a fridge, whether it lands on a specific recognisable detail,
whether it turns on a twist in the last few words, whether it reads
cleanly aloud, and whether it feels fresh. The sniff test is the
ritual every fridge owner knows — open a tub, sniff, decide — and a
scan of all 1,564 visible field titles found zero uses of sniff,
nose, inspector or safety, while hum, ice, crisper, leftovers,
light and rent are each used dozens of times. The premise (the
fridge's only safety inspector is your nose) is specific to the
fridge, and the payoff (your nose has never once said yes) lands in
the last few words.
"""

import os
import sys

PART_A1 = "This fridge's only "

PART_A2 = "food-safety inspector is your nose, "

PART_A3 = "and your nose has never "

PART_A4 = "once said yes."


def compose() -> str:
    return PART_A1 + PART_A2 + PART_A3 + PART_A4


MAX_CHARS = 200


def main() -> int:
    entry = compose()
    # Gate: 1-200 UTF-8 characters, one line, not only whitespace,
    # no trailing newline in the file.
    if not entry or not entry.strip():
        print("entry is empty", file=sys.stderr)
        return 1
    if "\n" in entry or "\r" in entry:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if len(entry) > MAX_CHARS:
        print(f"entry is {len(entry)} chars, over the {MAX_CHARS} cap",
              file=sys.stderr)
        return 1
    payload = entry.encode("utf-8")  # raises if not valid UTF-8

    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "wb") as f:
        f.write(payload)
    # Determinism self-check: the bytes on disk must be the payload.
    with open(out_path, "rb") as f:
        if f.read() != payload:
            print("non-deterministic write", file=sys.stderr)
            return 1
    # Outputs must be readable by every user (the grader collects them
    # as another user): file mode 0644. The directory is left alone.
    os.chmod(out_path, 0o644)
    print(f"wrote {len(entry)} chars to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
