# Character Prompt Guide

The prompts that took 20+ iterations to get right — distilled into a reusable structure.

Credit: @ayrus_ftw — An Architect Learning AI

---

## The Character Reference

Your character needs a **locked reference image**. This is the single most important thing.

- Use a photo of yourself, or an illustration you've already generated and locked
- Resize to ~1024px before uploading to ComfyUI Cloud
- Use the same reference image for every single episode — never swap it out
- The seed locks the face. The reference locks the identity.

---

## Positive Prompt Structure

```
[Style] [Background] [Format]
[Hook word placement]
[Shot type]: [character description] [position] [surrounding elements]
[Character match instruction — reference image]
[Negative space / breathing room note]
[Text instructions — minimal, series name only]
[Color accent] [Text color]
```

### Example — Wide shot, cream background

```
Editorial newspaper concept poster. Cream background (#F5F0E8). Portrait 4:5.
Small [HOOK WORD] in the top-left corner — understated, not dominating.
Wide shot: anime character (curly dark hair, beard, dark jacket) small in the lower centre,
surrounded by giant floating [YOUR SCENE ELEMENTS] filling the space.
Character [EMOTION/ACTION — e.g. "looking upward with wonder"].
Match the character face and hair from the reference image exactly.
Lots of breathing room. Floating elements fill most of the poster.
No masthead. One line of small dark navy text at the very bottom:
"[YOUR SERIES NAME]"
[ACCENT COLOR] accent. [TEXT COLOR] text.
```

### Swap these per episode

| Variable | Examples |
|---|---|
| `[HOOK WORD]` | LOST · FOUND · BUILT · ERROR · CONNECTED · FIRST |
| `[YOUR SCENE ELEMENTS]` | architectural blueprints · code fragments · error logs · glowing nodes |
| `[EMOTION/ACTION]` | looking upward with wonder · leaning forward with focus · arms open |

---

## System Prompt Structure

```
You are an expert editorial poster and graphic design engine.
Always produce a complete graphic design poster image.
Style: editorial newspaper concept — bold magazine cover with surreal illustration.

Key rules:
- Cream/beige background (#F5F0E8) — NOT white, NOT dark
- Anime-style character — cel-shaded, clean lines
- CRITICAL: Match the character's face, hair, and skin tone from the reference image exactly
- Wide shot — character small in lower portion, surrounded by giant floating elements
- Minimal text — series name at bottom only
- Portrait format 4:5. Lots of negative space.

Avoid: dark backgrounds, photorealism, cluttered layouts, neon colors.
```

---

## Seeds

Seeds control variation. Same prompt + same seed = same result every time.

**How to find your seed:**
1. Set `CONTROL_AFTER_GENERATE = "randomize"` and generate 5–10 images
2. Note the seed from any output you like
3. Lock it: `CONTROL_AFTER_GENERATE = "fixed"`, `SEED = your_number`

Once you find a seed where the character looks right — **lock it and never change it**.

---

## Model Settings

| Setting | Recommended | Notes |
|---|---|---|
| Model | Nano Banana 2 (Gemini 3.1 Flash Image) | The one that produces consistent character results |
| Resolution | 2K | Good quality without excessive cost |
| Thinking level | MINIMAL | Faster + cheaper — sufficient for this style |
| Aspect ratio | auto | Let the model decide based on prompt |

---

## Tips

- **Don't over-describe the character.** "Curly dark hair, beard, dark jacket" is enough. Over-describing causes drift.
- **The hook word is small.** It's a label, not a headline. Keep it 4–6 characters, top-left, understated.
- **One scene idea per episode.** Blueprints for architecture. Code fragments for scripting. Keep it direct.
- **Run 3 seeds before you commit.** The first one is rarely the best.
