# Architect Content Pipeline

The three-tool pipeline behind **An Architect Learning AI** — nine episodes of Instagram content, built with code.

**ComfyUI Cloud** generates the illustrated scenes.
**PIL** stamps the typography.
**Claude Code** wrote all the scripts.

Built and documented by [@ayrus_ftw](https://www.instagram.com/ayrus_ftw/)

---

## What's in here

| File | What it does |
|---|---|
| `generate-cover.py` | Generates episode cover images via ComfyUI Cloud + Nano Banana 2 |
| `generate-episode.py` | PIL starter template — stamps NB Pro backgrounds with Anton + Playfair text |
| `ayrus_fonts.py` | Shared font loader — Anton (headline) + Playfair Display (emphasis + body) |
| `fonts/` | Anton Regular + Playfair Display Bold Italic + Italic TTF files |
| `docs/prompts.md` | The character prompt structure + seed guide |
| `docs/comfyui-setup.md` | ComfyUI Cloud account + API key setup |
| `docs/claude-code-setup.md` | Step-by-step Claude Code installation and usage |

---

## Quick start

### 1. Clone and install dependencies

```bash
git clone https://github.com/yourusername/architect-content-pipeline
cd architect-content-pipeline
pip install -r requirements.txt
```

### 2. Add your API key

```bash
cp .env.example .env
```

Open `.env` and add your ComfyUI Cloud API key. See [docs/comfyui-setup.md](docs/comfyui-setup.md) for how to get one.

### 3. Try the example first (no ComfyUI needed)

A sample NB Pro background is included. Run this to see the full text-stamping pipeline immediately:

```bash
python3.11 example.py
```

Output opens at `sample/output.png`. Edit `HEADLINE_LINES`, `EMPHASIS_WORD`, and `BODY_LINES` in the script to try your own text.

### 4. Generate a cover image

Add your reference image as `reference.jpg`, then:

```bash
python3.11 generate-cover.py
```

Output saved to `outputs/cover.png`.

### 4. Create carousel slides

Copy `generate-episode.py` and rename it for your episode. Edit the `make_XX()` functions with your text. Run it:

```bash
python3.11 generate-episode.py
```

---

## The font system

All slides use two fonts:

| Role | Font | Style |
|---|---|---|
| Headline | **Anton Regular** | ALL CAPS, white, large |
| Emphasis word | **Playfair Display Bold Italic** | Italic, amber `#D97706` |
| Body text | **Playfair Display Italic** | Italic, gray |

```python
from ayrus_fonts import headline, emphasis, body

d.text((80, y), "YOUR HEADLINE", font=headline(120), fill=WHITE)
d.text((80, y), "emphasis word.", font=emphasis(96),  fill=AMBER)
d.text((80, y), "body text",      font=body(44),      fill=GRAY)
```

---

## Slide types

### Illustrated — NB Pro background + text overlay

```python
make_illustrated(
    num           = 2,
    headline_lines= ["YOUR HEADLINE HERE"],
    emphasis_word = "emphasis word.",
    body_lines    = ["Supporting body line."]
)
```

Full scene visible. Gradient darkens the bottom third. Text anchored at y=1650 on every slide — consistent position.

### Dark — pure PIL statement slide

```python
make_dark(
    num           = 3,
    headline_lines= ["THE INSIGHT", "IN CAPS."],
    emphasis_word = "the pivot.",
    body_lines    = ["One line of context.", "Maybe two."]
)
```

Dark background. Amber top and bottom bars. Text vertically centred.

### CTA — cream engagement slide

```python
make_cta(
    num       = 8,
    big_text  = "WHAT COMES NEXT",
    sub_text  = "the teaser.",
    body_lines= ["One line.", "Two lines."],
    question  = "What would you build with this?",
    next_ep   = "→ Ep. 02: the first error."
)
```

### Onboarding — always the last slide

```python
make_onboarding(num=9)
```

"Most AI content shows you the result. This shows you the part before that." Standard template — doesn't change between episodes.

---

## The three tools

### ComfyUI Cloud

Generates the illustrated background images. Nano Banana 2 model. Character reference image uploaded per job.

→ [docs/comfyui-setup.md](docs/comfyui-setup.md)

### PIL (Pillow)

Stamps typography on the generated backgrounds. Handles dark and cream pure-PIL slides from scratch.

→ `generate-episode.py`

### Claude Code

The AI coding assistant that wrote every script in this pipeline. You describe what you want — it writes the Python.

→ [docs/claude-code-setup.md](docs/claude-code-setup.md)

---

## Canvas size

All slides are **1856 × 2304 px** (4:5 portrait — Instagram standard).

---

## Credits

Built by [@ayrus_ftw](https://www.instagram.com/ayrus_ftw/) — An Architect Learning AI.
Follow the series on Instagram for the full story, episode by episode.
