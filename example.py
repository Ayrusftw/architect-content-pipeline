#!/usr/bin/env python3.11
"""
example.py — Run this first. No ComfyUI needed.

Takes the included sample background and stamps text on it
using the full font system. Shows you exactly how the pipeline works.

Run:
    python3.11 example.py

Output: sample/output.png  (opens automatically)

Once this works, open generate-episode.py and start building your own.

Credit: @ayrus_ftw — An Architect Learning AI
"""

import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from ayrus_fonts import headline, emphasis, body
from PIL import Image, ImageDraw, ImageFilter

W, H         = 1856, 2304
AMBER        = (217, 119, 6)
GRAY         = (160, 160, 160)
WHITE        = (241, 241, 240)
FOOTER_Y     = H - 110
FOOTER_TEXT  = "YOUR SERIES NAME  ·  EP. 00"

INPUT  = "sample/background.png"
OUTPUT = "sample/output.png"


def bottom_overlay(img, strength=220):
    """Quadratic gradient — transparent at top, near-black at bottom."""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d  = ImageDraw.Draw(ov)
    for i in range(H):
        alpha = int(strength * (i / H) ** 2)
        d.line([(0, i), (W, i)], fill=(0, 0, 0, alpha))
    base = img.convert("RGBA")
    base.alpha_composite(ov)
    return base.convert("RGB")


def main():
    print("\n──────────────────────────────────────")
    print("  Example — PIL Slide from NB Pro background")
    print("──────────────────────────────────────\n")

    # ── Load the background ──────────────────────────────────────
    img   = Image.open(INPUT).convert("RGB")

    # Erase any baked-in text at the bottom of the sample background
    d_pre = ImageDraw.Draw(img)
    d_pre.rectangle([(0, H - 400), (W, H)], fill=(15, 15, 15))

    # Apply gradient — full image stays visible, bottom darkens
    img   = bottom_overlay(img, strength=220)
    d     = ImageDraw.Draw(img)

    # ── Stamp your text ─────────────────────────────────────────
    # Edit these three lines to try your own content:

    HEADLINE_LINES = ["YOUR HEADLINE", "GOES HERE."]   # Anton — ALL CAPS, white
    EMPHASIS_WORD  = "your emphasis."                  # Playfair Bold Italic — amber
    BODY_LINES     = ["Supporting body text goes here.",
                      "One or two lines is enough."]   # Playfair Italic — gray

    # Fixed position — same on every slide
    y = 1650
    for line in HEADLINE_LINES:
        d.text((80, y), line, font=headline(120), fill=WHITE)
        y += 130
    y += 8
    d.text((80, y), EMPHASIS_WORD, font=emphasis(96), fill=AMBER)
    y += 110
    for line in BODY_LINES:
        d.text((80, y), line, font=body(36), fill=GRAY)
        y += 44

    # Footer — always at the same position
    d.text((80, FOOTER_Y), FOOTER_TEXT, font=body(28), fill=GRAY)

    # ── Save and open ────────────────────────────────────────────
    os.makedirs("sample", exist_ok=True)
    img.save(OUTPUT, "PNG")
    print(f"  Output → {OUTPUT}")
    subprocess.Popen(["open", OUTPUT])
    print("\n  ✓ Done. Edit HEADLINE_LINES, EMPHASIS_WORD, and BODY_LINES")
    print("    to try your own text, then run again.\n")


main()
