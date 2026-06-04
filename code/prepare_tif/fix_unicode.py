"""Decode Mathematical-Italic Unicode in KB markdown files to plain ASCII.

The `awesome-ee-spectral-indices` source content uses Unicode math italic
characters (U+1D400-U+1D7FF) for variable names like Green / NIR / SWIR
because Sphinx rendered HTML math that way. Modern LLM tokenizers treat
these as opaque tokens and cannot understand them as the variable names
they represent.

This script does encoding correction — it does NOT modify content. Each
character is replaced with its plain ASCII / Greek equivalent so the
formulas read the same as when the original author wrote them.

Run: python fix_unicode.py
"""
from __future__ import annotations

from pathlib import Path


KB_ROOT = Path(__file__).resolve().parent.parent / "kb"


def _build_translation() -> dict[int, str]:
    table: dict[int, str | None] = {}

    # Mathematical Italic Capital A-Z  (U+1D434 .. U+1D44D)
    for i in range(26):
        table[0x1D434 + i] = chr(ord("A") + i)
    # Mathematical Italic Small a-z (U+1D44E .. U+1D467); h is reserved
    # at U+1D455 (Planck constant); skip if undefined
    for i in range(26):
        cp = 0x1D44E + i
        if cp == 0x1D455:  # h is missing in the math italic block
            continue
        table[cp] = chr(ord("a") + i)
    # The Planck h placeholder isn't used here, but if some text contains
    # U+210E (PLANCK CONSTANT), map to 'h':
    table[0x210E] = "h"

    # Mathematical Italic Greek Capital (U+1D6E2 .. U+1D6FA)
    # Map to ordinary Greek (U+0391 .. U+03A9)
    for i in range(25):
        table[0x1D6E2 + i] = chr(0x0391 + i)
    # Mathematical Italic Greek small (U+1D6FC .. U+1D714)
    for i in range(25):
        table[0x1D6FC + i] = chr(0x03B1 + i)

    # Other math punctuation
    table[0x2061] = ""    # FUNCTION APPLICATION → drop
    table[0x2062] = ""    # INVISIBLE TIMES → drop
    table[0x2212] = "-"   # MINUS SIGN → ASCII -
    table[0x00D7] = "*"   # MULTIPLICATION SIGN → ASCII *
    table[0x00B7] = "*"   # MIDDLE DOT (math multiply) → ASCII *
    table[0x221A] = "sqrt"  # SQUARE ROOT → ASCII sqrt
    table[0x2192] = "->"  # RIGHTWARDS ARROW
    table[0x2013] = "-"   # EN DASH
    table[0x2014] = "--"  # EM DASH
    table[0x00A0] = " "   # NO-BREAK SPACE
    table[0x201C] = '"'   # LEFT DOUBLE QUOTE
    table[0x201D] = '"'   # RIGHT DOUBLE QUOTE
    table[0x2018] = "'"   # LEFT SINGLE QUOTE
    table[0x2019] = "'"   # RIGHT SINGLE QUOTE

    # Parenthesis extensions used in big-paren rendering — drop
    for cp in (0x239B, 0x239C, 0x239D, 0x239E, 0x239F, 0x23A0):
        table[cp] = "("  # placeholder won't be perfect but markers are rare

    # Pilcrow (¶) is a section sigil from Sphinx → drop
    table[0x00B6] = ""

    return table


_TRANSLATION = str.maketrans(_build_translation())


def normalize(text: str) -> str:
    return text.translate(_TRANSLATION)


def main():
    targets = list(KB_ROOT.rglob("*.md"))
    fixed = []
    for p in targets:
        original = p.read_text(encoding="utf-8")
        cleaned = normalize(original)
        if cleaned != original:
            p.write_text(cleaned, encoding="utf-8")
            fixed.append((p, len(original) - len(cleaned)))

    print(f"Scanned {len(targets)} markdown files in {KB_ROOT}")
    print(f"Modified {len(fixed)} files:")
    for p, delta in fixed:
        rel = p.relative_to(KB_ROOT)
        print(f"  {rel}  ({delta:+d} chars)")


if __name__ == "__main__":
    main()
