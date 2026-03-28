# ComfyUI Cloud Setup

Credit: @ayrus_ftw — An Architect Learning AI

---

## What is ComfyUI Cloud?

ComfyUI Cloud (cloud.comfy.org) is the hosted version of ComfyUI — you run image generation workflows via API without installing anything locally. This pipeline uses the **Nano Banana 2** model (powered by Gemini Flash Image).

---

## Step 1 — Create an account

Go to [cloud.comfy.org](https://cloud.comfy.org) and sign up.

---

## Step 2 — Get your API key

1. Log in to ComfyUI Cloud
2. Go to **Settings → API Keys**
3. Create a new key
4. Copy it — you'll only see it once

---

## Step 3 — Add credits

Image generation costs credits. Add a small amount to start (a few dollars covers many generations).

Go to **Settings → Billing** to add credits.

---

## Step 4 — Add your API key to .env

In the root of this project, copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Open `.env` and paste your key:

```
COMFYUI_API_KEY=your_actual_key_here
```

**Never commit `.env` to GitHub.** It's already in `.gitignore`.

---

## Step 5 — Test the connection

Run the cover generator with a test image:

```bash
python3.11 generate-cover.py
```

If it works, you'll see:
```
Uploading reference.jpg...
  Uploaded as: reference.jpg
  Job submitted: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  Waiting for result...
  Saved → outputs/cover.png
Done.
```

---

## Troubleshooting

| Error | Fix |
|---|---|
| `401 Unauthorized` | Check your API key in `.env` |
| `authentication method not allowed` | Make sure `extra_data: {"api_key_comfy_org": key}` is in the request body — not just the header |
| `Timed out` | The model took too long — run again, it usually works on the second attempt |
| Image saved but looks wrong | Adjust your prompt or try a different seed |

---

## Cost

Nano Banana 2 at 2K resolution costs roughly $0.02–0.05 per image depending on complexity and thinking level. MINIMAL thinking level is the cheapest and works well for this style.
