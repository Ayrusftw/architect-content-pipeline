#!/usr/bin/env python3.11
"""
generate-cover.py — ComfyUI Cloud cover image generator.

Uses Nano Banana 2 (Gemini Flash Image) via ComfyUI Cloud API.
Uploads a reference image, submits a workflow, captures output via WebSocket.

Setup:
  1. Copy .env.example to .env and add your COMFYUI_API_KEY
  2. Add your reference image path below
  3. Edit POSITIVE_PROMPT and SYSTEM_PROMPT for your character/style
  4. Run: python3.11 generate-cover.py

Credit: @ayrus_ftw — An Architect Learning AI
"""

import requests, os, json, asyncio, uuid
import websockets
from dotenv import load_dotenv

load_dotenv()

key      = os.getenv("COMFYUI_API_KEY")
BASE_URL = "https://cloud.comfy.org"
WS_URL   = "wss://cloud.comfy.org/ws"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  CONTROL PANEL — edit everything in this section
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REFERENCE_IMAGE = "reference.jpg"        # your character reference image
OUTPUT_PATH     = "outputs/cover.png"    # where the output is saved

# The main prompt — describe what you want to generate
POSITIVE_PROMPT = """
Editorial poster. Cream background (#F5F0E8). Portrait 4:5.
Small hook word in the top-left corner — understated, not dominating.
Wide shot: anime character (curly dark hair, beard, dark jacket) small in the lower centre,
surrounded by giant floating architectural elements filling the space.
Character looking upward with a sense of wonder and scale.
Match the character face and hair from the reference image exactly.
Lots of breathing room. Floating elements fill most of the poster.
No masthead. One line of small dark navy text at the very bottom.
"""

# System prompt — constraints and style rules
SYSTEM_PROMPT = """
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
"""

# Model settings
MODEL                  = "Nano Banana 2 (Gemini 3.1 Flash Image)"
SEED                   = 43              # change this to explore variations
CONTROL_AFTER_GENERATE = "fixed"         # "fixed" | "randomize" | "increment"
ASPECT_RATIO           = "auto"
RESOLUTION             = "2K"
RESPONSE_MODALITIES    = "IMAGE"
THINKING_LEVEL         = "MINIMAL"

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def upload_image(image_path):
    print(f"Uploading {image_path}...")
    with open(image_path, "rb") as f:
        resp = requests.post(
            f"{BASE_URL}/api/upload/image",
            headers={"X-API-Key": key},
            files={"image": (os.path.basename(image_path), f, "image/jpeg")}
        )
    name = resp.json().get("name")
    print(f"  Uploaded as: {name}")
    return name


def build_workflow(uploaded_filename):
    return {
        "9":  {"inputs": {"filename_prefix": "cover", "images": ["23", 0]},
               "class_type": "SaveImage"},
        "16": {"inputs": {"image": uploaded_filename},
               "class_type": "LoadImage"},
        "23": {"inputs": {
                   "prompt":               POSITIVE_PROMPT,
                   "system_prompt":        SYSTEM_PROMPT,
                   "model":                MODEL,
                   "seed":                 SEED,
                   "control_after_generate": CONTROL_AFTER_GENERATE,
                   "aspect_ratio":         ASPECT_RATIO,
                   "resolution":           RESOLUTION,
                   "response_modalities":  RESPONSE_MODALITIES,
                   "thinking_level":       THINKING_LEVEL,
                   "images": ["16", 0]
               },
               "class_type": "GeminiNanoBanana2"}
    }


async def run_workflow(workflow):
    client_id = str(uuid.uuid4())
    resp = requests.post(
        f"{BASE_URL}/api/prompt",
        headers={"X-API-Key": key, "Content-Type": "application/json"},
        json={"prompt": workflow, "client_id": client_id,
              "extra_data": {"api_key_comfy_org": key}}
    )
    prompt_id = resp.json().get("prompt_id")
    print(f"  Job submitted: {prompt_id}")

    async with websockets.connect(f"{WS_URL}?clientId={client_id}&token={key}") as ws:
        print("  Waiting for result...")
        while True:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=120)
                if isinstance(msg, bytes):
                    continue
                data = json.loads(msg)

                if data.get("type") == "executed":
                    for img in data.get("data", {}).get("output", {}).get("images", []):
                        fname = img.get("filename")
                        if fname:
                            dl = requests.get(
                                f"{BASE_URL}/api/view",
                                headers={"X-API-Key": key},
                                params={"filename": fname, "subfolder": img.get("subfolder", ""),
                                        "type": img.get("type", "output")},
                                allow_redirects=True
                            )
                            if dl.status_code == 200:
                                os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
                                with open(OUTPUT_PATH, "wb") as f:
                                    f.write(dl.content)
                                print(f"  Saved → {OUTPUT_PATH}")
                                return True

                elif data.get("type") == "execution_error":
                    print(f"  Error: {data.get('data', {})}")
                    return False

            except asyncio.TimeoutError:
                print("  Timed out.")
                return False
    return False


async def main():
    print(f"\n{'─'*50}")
    print(f"  Model:   {MODEL}")
    print(f"  Seed:    {SEED}  ({CONTROL_AFTER_GENERATE})")
    print(f"  Output:  {OUTPUT_PATH}")
    print(f"{'─'*50}\n")

    uploaded = upload_image(REFERENCE_IMAGE)
    if not uploaded:
        print("Upload failed — check your API key and reference image path.")
        return

    success = await run_workflow(build_workflow(uploaded))
    print("\nDone." if success else "\nFailed — try a different seed or check your prompt.")


if __name__ == "__main__":
    asyncio.run(main())
