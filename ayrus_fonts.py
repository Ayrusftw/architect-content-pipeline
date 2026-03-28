"""
Shared font loader for all PIL episode scripts.

Font system (ep-10 onwards):
  - HEADLINE : Anton Regular       — bold caps, fills 50–70% of slide
  - EMPHASIS : Playfair Display Bold Italic — italic script emphasis word
  - BODY     : Playfair Display Italic      — supporting body text
  - MONO     : SF Mono / Menlo              — terminal/code slides only

Usage:
    from fonts import headline, emphasis, body, mono
    d.text((x, y), "THE HARDEST PART", font=headline(120), fill=WHITE)
    d.text((x, y), "posting...",       font=emphasis(96),  fill=AMBER)
    d.text((x, y), "body text",        font=body(48),      fill=GRAY)
"""

import os
from PIL import ImageFont

_BASE = os.path.join(os.path.dirname(__file__), "..", "context", "fonts")

_ANTON           = os.path.join(_BASE, "Anton-Regular.ttf")
_PLAYFAIR_BOLD_I = os.path.join(_BASE, "PlayfairDisplay-BoldItalic.ttf")
_PLAYFAIR_I      = os.path.join(_BASE, "PlayfairDisplay-Italic.ttf")


def headline(size: int) -> ImageFont.FreeTypeFont:
    """Anton Regular — bold caps headline."""
    return ImageFont.truetype(_ANTON, size)


def emphasis(size: int) -> ImageFont.FreeTypeFont:
    """Playfair Display Bold Italic — italic emphasis word."""
    return ImageFont.truetype(_PLAYFAIR_BOLD_I, size)


def body(size: int) -> ImageFont.FreeTypeFont:
    """Playfair Display Italic — body / subtext."""
    return ImageFont.truetype(_PLAYFAIR_I, size)


def mono(size: int) -> ImageFont.FreeTypeFont:
    """SF Mono / Menlo — terminal and code slides only."""
    for p in ["/System/Library/Fonts/Menlo.ttc", "/System/Library/Fonts/SFNSMono.ttf"]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()
