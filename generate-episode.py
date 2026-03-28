#!/usr/bin/env python3.11
"""
generate-episode.py — PIL slide starter template.

Creates Instagram carousel slides (1856×2304) using the Anton + Playfair Display
font system. Re-stamps NB Pro backgrounds with text, or builds pure PIL slides
from scratch.

Slide types:
  - Illustrated  — NB Pro background + gradient overlay + text at y=1650
  - Dark text    — Pure PIL dark background, statement/insight slides
  - Cream CTA    — Pure PIL cream background, CTA and onboarding slides

Usage:
  1. Copy this file and rename it for your episode
  2. Fill in SLIDES_SRC, SLIDES_OUT, FOOTER_TEXT
  3. Write a make_XX() function for each slide
  4. Run: python3.11 generate-episode.py

Credit: @ayrus_ftw — An Architect Learning AI
"""

import os, sys, subprocess
sys.path.insert(0, os.path.dirname(__file__))
from ayrus_fonts import headline, emphasis, body
from PIL import Image, ImageDraw, ImageFilter

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CONFIG — edit per episode
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SLIDES_SRC  = "slides/backgrounds"    # folder with NB Pro background PNGs
SLIDES_OUT  = "slides/final"          # output folder
COVER_PATH  = "cover.png"             # your episode cover (used in onboarding slide)

os.makedirs(SLIDES_OUT, exist_ok=True)

FOOTER_TEXT = "YOUR SERIES NAME  ·  EP. 00"   # update per episode

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


W, H         = 1856, 2304
CREAM        = (245, 240, 232)
NAVY         = (26, 35, 64)
AMBER        = (217, 119, 6)      # #D97706
GRAY         = (160, 160, 160)
DARK         = (30, 30, 30)
WHITE        = (241, 241, 240)
FOOTER_Y     = H - 110
FOOTER_STRIP = H - 140


# ─── HELPERS ──────────────────────────────────────────────────────────────────

def dark_footer(d):
    d.text((80, FOOTER_Y), FOOTER_TEXT, font=body(28), fill=GRAY)

def cream_footer(d):
    d.text((80, FOOTER_Y), FOOTER_TEXT, font=body(28), fill=GRAY)


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


# ─── SLIDE TYPES ──────────────────────────────────────────────────────────────

def make_illustrated(num, headline_lines, emphasis_word, body_lines,
                     h_size=120, e_size=96, b_size=36):
    """
    Re-stamps an NB Pro background PNG with new text.

    - Erases baked-in text at bottom (last 400px)
    - Applies gradient overlay — full image stays visible
    - Fixed text position at y=1650 for consistency across all slides
    """
    src   = f"{SLIDES_SRC}/slide-{num:02d}.png"
    img   = Image.open(src).convert("RGB")
    d_pre = ImageDraw.Draw(img)
    d_pre.rectangle([(0, H - 400), (W, H)], fill=(15, 15, 15))   # erase old text
    img   = bottom_overlay(img, strength=220)
    d     = ImageDraw.Draw(img)

    y = 1650    # fixed — same position on every illustrated slide
    for line in headline_lines:
        d.text((80, y), line, font=headline(h_size), fill=WHITE)
        y += h_size + 10
    y += 8
    d.text((80, y), emphasis_word, font=emphasis(e_size), fill=AMBER)
    y += e_size + 14
    for line in body_lines:
        d.text((80, y), line, font=body(b_size), fill=GRAY)
        y += b_size + 8

    dark_footer(d)
    out = f"{SLIDES_OUT}/slide-{num:02d}.png"
    img.save(out, "PNG")
    return out


def make_dark(num, headline_lines, emphasis_word, body_lines,
              h_size=120, e_size=96, b_size=44):
    """
    Pure PIL dark slide — for insight/statement slides with no background image.
    Amber top and bottom bars. Text starts at y=900.
    """
    img = Image.new("RGB", (W, H), DARK)
    d   = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=AMBER)

    y = 900
    for line in headline_lines:
        d.text((80, y), line, font=headline(h_size), fill=WHITE)
        y += h_size + 16
    y += 16
    d.text((80, y), emphasis_word, font=emphasis(e_size), fill=AMBER)
    y += e_size + 20
    for line in body_lines:
        d.text((80, y), line, font=body(b_size), fill=GRAY)
        y += b_size + 12

    d.rectangle([0, H - 8, W, H], fill=AMBER)
    dark_footer(d)
    out = f"{SLIDES_OUT}/slide-{num:02d}.png"
    img.save(out, "PNG")
    return out


def make_cta(num, big_text, sub_text, body_lines, question, next_ep):
    """
    Cream CTA slide — for episode end + engagement question.
    """
    img = Image.new("RGB", (W, H), CREAM)
    d   = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=NAVY)
    d.text((80, 60), FOOTER_TEXT, font=body(34), fill=GRAY)
    d.line([(80, 116), (W - 80, 116)], fill=NAVY, width=2)

    y = 240
    d.text((80, y), big_text,  font=headline(80), fill=NAVY);       y += 96
    d.text((80, y), sub_text,  font=emphasis(70), fill=(50,70,140)); y += 100
    d.rectangle([80, y, W - 80, y + 4], fill=AMBER);                y += 40
    for line in body_lines:
        d.text((80, y), line, font=body(52), fill=NAVY);             y += 70
    y += 20
    d.rectangle([80, y, W - 80, y + 200], fill=NAVY)
    d.text((120, y + 30),  question,      font=body(44),     fill=WHITE)
    d.text((120, y + 144), "Drop it below.", font=emphasis(44), fill=AMBER)
    y += 260
    d.rectangle([80, y, W - 80, y + 3], fill=GRAY); y += 40
    d.text((80, y), next_ep, font=headline(56), fill=NAVY)

    d.rectangle([0, H - 8, W, H], fill=NAVY)
    cream_footer(d)
    out = f"{SLIDES_OUT}/slide-{num:02d}.png"
    img.save(out, "PNG")
    return out


def make_onboarding(num):
    """
    Cream onboarding slide — always the last slide.
    'Most AI content shows you the result. This shows you the part before that.'
    Optionally pastes a rotated cover thumbnail if COVER_PATH exists.
    """
    img = Image.new("RGB", (W, H), CREAM)
    d   = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 8], fill=NAVY)
    d.text((80, 60), FOOTER_TEXT, font=body(34), fill=GRAY)
    d.line([(80, 116), (W - 80, 116)], fill=NAVY, width=2)

    y = 240
    d.text((80, y), "MOST AI CONTENT",        font=headline(90), fill=NAVY);           y += 106
    d.text((80, y), "shows you the result.",  font=emphasis(70), fill=(50, 70, 140));  y += 110
    d.rectangle([80, y, 500, y + 6], fill=AMBER); y += 50
    d.text((80, y), "This shows you",  font=body(72), fill=NAVY); y += 100
    d.text((80, y), "the part",        font=body(72), fill=NAVY); y += 100
    d.text((80, y), "before that.",    font=emphasis(72), fill=AMBER); y += 140
    d.rectangle([80, y, W - 80, y + 3], fill=GRAY); y += 50
    d.text((80, y), "I'm an architect.",                     font=headline(56), fill=NAVY); y += 80
    d.text((80, y), "Start from Ep. 00 for the full story.", font=body(48),    fill=GRAY)

    # Optional: paste cover thumbnail top-right
    try:
        cover     = Image.open(COVER_PATH).convert("RGB")
        tw        = 500; th = int(tw * cover.height / cover.width)
        cover     = cover.resize((tw, th), Image.LANCZOS)
        cover_rot = cover.rotate(-5, expand=True, resample=Image.BICUBIC)
        shadow    = Image.new("RGBA", cover_rot.size, (0, 0, 0, 0))
        sd        = ImageDraw.Draw(shadow)
        sd.rectangle([0, 0, cover_rot.width, cover_rot.height], fill=(0, 0, 0, 80))
        shadow    = shadow.filter(ImageFilter.GaussianBlur(22))
        tx = W - 80 - cover_rot.width - 10; ty = 240
        img.paste(shadow.convert("RGB"), (tx + 18, ty + 18), mask=shadow.split()[3])
        img.paste(cover_rot, (tx, ty))
    except Exception:
        pass

    d.rectangle([0, H - 8, W, H], fill=NAVY)
    cream_footer(d)
    out = f"{SLIDES_OUT}/slide-{num:02d}.png"
    img.save(out, "PNG")
    return out


# ─── YOUR SLIDES ──────────────────────────────────────────────────────────────
# Uncomment and adapt each function for your episode.
# Delete the ones you don't need.

def make_02():
    return make_illustrated(2,
        ["YOUR HEADLINE HERE"],         # ALL CAPS, Anton
        "emphasis word.",               # italic, amber, Playfair
        ["Supporting body line."])      # gray, small, Playfair


# def make_03():
#     return make_illustrated(3,
#         ["HEADLINE LINE ONE", "LINE TWO"],
#         "emphasis word.",
#         ["Body line one.", "Body line two."])


# def make_last_minus_one():
#     return make_cta(
#         num       = 8,
#         big_text  = "YOUR HOOK HERE",
#         sub_text  = "your emphasis.",
#         body_lines= ["Body line one.", "Body line two."],
#         question  = "Your engagement question here?",
#         next_ep   = "→ Ep. XX: what comes next."
#     )


# def make_last():
#     return make_onboarding(9)


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print(f"\n{'─'*55}\n  Episode PIL Slides\n{'─'*55}\n")
    makers = [
        ("02", make_02),
        # ("03", make_03),
        # add your slides here in order
    ]
    for num, fn in makers:
        out = fn()
        print(f"  Slide {num} → {out}")
        subprocess.Popen(["open", out])
    print(f"\n{'─'*55}\n  Done → {SLIDES_OUT}/\n{'─'*55}\n")

main()
