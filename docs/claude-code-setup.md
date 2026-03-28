# Claude Code Setup

Claude Code is the AI coding assistant that wrote every script in this pipeline. You describe what you need — it writes the Python. You run it.

Credit: @ayrus_ftw — An Architect Learning AI

---

## What is Claude Code?

Claude Code is Anthropic's CLI tool that runs inside your terminal. It can read your files, write code, run scripts, and iterate based on your feedback — all in plain language.

This pipeline was built entirely inside VS Code using Claude Code. No prior Python experience required to get started.

---

## Step 1 — Install Node.js

Claude Code requires Node.js 18+. Check if you have it:

```bash
node --version
```

If not, download from [nodejs.org](https://nodejs.org).

---

## Step 2 — Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

Verify:

```bash
claude --version
```

---

## Step 3 — Get an Anthropic API key

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Go to **API Keys** and create a new key
4. Copy it

---

## Step 4 — Connect your API key

Run Claude Code for the first time:

```bash
claude
```

It will prompt you to enter your API key. Paste it in. It's stored securely on your machine.

---

## Step 5 — Open your project folder

```bash
cd path/to/your/project
claude
```

Claude Code starts inside your project directory and can read all your files.

---

## How to use it for this pipeline

You don't need to write Python. Just describe what you want:

**Generating a cover:**
```
Write a script that generates an Instagram cover image using ComfyUI Cloud.
The image should be 1856×2304. Use my reference image at reference.jpg.
Save the output to outputs/cover.png.
```

**Adding a new slide:**
```
Add a make_03() function to generate-episode.py.
It should use make_illustrated() with:
- Headline: "THREE MONTHS IN."
- Emphasis: "still learning."
- Body: "But building something."
```

**Fixing an error:**
Just paste the error message and Claude Code will diagnose and fix it.

---

## Tips

- **Work in small steps.** Ask for one thing at a time. Review it. Then ask for the next.
- **Run the script after every change.** Don't accumulate 10 changes before testing.
- **Describe the output, not the code.** Say "I want a slide that looks like X" — not "write a PIL function that does Y".
- **Paste errors directly.** If something fails, copy the terminal output and paste it in. Claude Code will fix it.
- **Ask it to explain.** "Explain what this function does" works. Understanding the code helps you adapt it.

---

## Cost

Claude Code uses the Anthropic API. A typical session building or iterating on a script costs cents, not dollars. Monitor usage at [console.anthropic.com](https://console.anthropic.com).
