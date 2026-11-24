#!/usr/bin/env python3
"""Seventeen Syllables of Debugging.

The entry is one haiku about debugging, in the strict 5-7-5 shape:

    Cursor blinks at three
    one red line hides in the log
    I wrote it myself

The picture at the centre is concrete: a cursor blinking at 3 a.m.
and a single red line hiding in the log. The last line turns the poem
— the bug was never the machine's; the debugger wrote it himself.

Writes the haiku to /output/entry.txt. Stdlib only, no network.
"""

import os

HAIKU = """Cursor blinks at three
one red line hides in the log
I wrote it myself"""

# The gate allows 1 to 200 characters.
MAX_CHARS = 200

# Syllable counts, line by line: 5, 7, 5.
SYLLABLES = (5, 7, 5)


def count_syllables(line: str) -> int:
    """Count syllables the way a reader would say the line aloud.

    A syllable is a run of vowel letters (a, e, i, o, u, y when it
    sounds like a vowel). A silent trailing 'e' after a consonant
    does not add one. Good enough for these three short lines, and
    checked against the hand-counted shape below.
    """
    vowels = "aeiou"
    total = 0
    for word in line.lower().split():
        word = word.strip(".,;:!?")
        in_vowel = False
        syllables = 0
        for ch in word:
            if ch in vowels or (ch == "y" and not in_vowel):
                if not in_vowel:
                    syllables += 1
                in_vowel = True
            else:
                in_vowel = False
        if word.endswith("e") and syllables > 1 and word[-2] not in vowels:
            syllables -= 1
        elif word.endswith("es") and syllables > 1 and word[-3] not in vowels:
            syllables -= 1
        total += max(syllables, 1)
    return total


def entry_text() -> str:
    """Return the haiku, checked against the bounty's own rules."""
    text = HAIKU.strip()
    assert text, "the entry must not be empty"
    assert len(text) <= MAX_CHARS, "the entry must fit the 200 character gate"
    lines = text.split("\n")
    assert len(lines) == 3, "a haiku is three lines"
    for line, expected in zip(lines, SYLLABLES):
        got = count_syllables(line)
        assert got == expected, f"line {line!r} has {got} syllables, need {expected}"
    return text


def main() -> None:
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(entry_text() + "\n")


if __name__ == "__main__":
    main()
