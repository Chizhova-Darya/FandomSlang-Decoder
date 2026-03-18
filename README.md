[README.md](https://github.com/user-attachments/files/26086299/README.md)
# FandomSlang Decoder

FandomSlang Decoder is a small web app that translates niche fandom slang, memes, ship names and in‑jokes into clear, plain English for newcomers.

It is aimed at casual viewers entering anime / TV / games fandoms and at content moderators who need quick explanations of slang-heavy text.

## Features

- **Fandom presets**: choose from General Internet, Anime/Manga, K‑pop, Marvel/MCU, Star Wars, Gaming, and Western TV/Streaming. Each preset guides the model toward relevant slang (e.g., `isekai`, `stan`).
- **Batch mode**: paste up to **three short texts** at once (e.g., a Discord snippet), and decode them together.
- **Plain‑English decoding**: each text is rewritten in accessible English while keeping the original sentiment where possible.
- **Inline glossary**: slang and references are listed under each result, with hover tooltips on each term (`title` attribute) for quick lookup.
- **Copy / share helpers**: one‑click copy of the decoded text, or a share‑ready blurb (`Decoded via FandomSlang Decoder: …`).
- **Dark mode**: a toggle in the header switches between light and dark themes, remembered per‑browser.
- **Session‑only usage history**: the last 5 decodes are stored in `localStorage` and shown in a “Recent decodes” panel. History never leaves the browser.

## Tech stack

- **Backend**: Python, Flask.
- **AI**: OpenAI Chat Completions API (configurable model, defaults to `gpt-4.1-mini`).
- **Frontend**: Jinja2 templates, modern CSS for the UI, and a small vanilla JavaScript file for:
  - Dark mode toggle and persistence.
  - Copy‑to‑clipboard buttons.
  - `localStorage`‑based usage history.

## Getting started

### 1. Install dependencies

Create and activate a virtual environment (optional but recommended), then install requirements:

```bash
cd fandomslang-decoder
pip install -r requirements.txt
```

### 2. Configure environment variables

Set your OpenAI API key in the environment:

```bash
# PowerShell example
$env:OPENAI_API_KEY = "sk-...your-key..."
```

Optional environment variables:

- `FANDOMSLANG_MODEL` – override the default model name if desired.
- `FANDOMSLANG_SECRET_KEY` – Flask secret key for sessions and CSRF protection (defaults to a simple dev key).

### 3. Run the app

You can run it directly with Python:

```bash
python app.py
```

Then open `http://127.0.0.1:5000/` in your browser.

Alternatively, using Flask’s CLI:

```bash
set FLASK_APP=app:app  # or $env:FLASK_APP = "app:app" in PowerShell
flask run
```

## How it works

### Presets

`presets.py` defines a small set of `FandomPreset` objects (Anime, K‑pop, Marvel, Star Wars, Gaming, General Internet, Western TV). Each preset includes:

- A human‑readable label.
- A short description of the fandom context.
- Prompt hints listing representative slang and concepts for that space.

The chosen preset is passed into the OpenAI prompt so the model knows which kind of slang to expect.

### OpenAI interaction

`ai_client.decode_slang`:

- Accepts up to three input texts and a fandom key.
- Builds a **system message** describing FandomSlang Decoder’s purpose and the selected fandom context.
- Builds a **user message** that:
  - Includes the array of texts.
  - Describes the desired behaviour (plain‑English decoding plus glossary).
  - Shows a JSON **response schema example**.
- Calls the Chat Completions API and parses the JSON into a list of `DecodedItem` objects:
  - `original`: original text.
  - `decoded`: plain‑English explanation.
  - `glossary`: list of `{ term, definition }`.
- If strict JSON parsing fails, it falls back to extracting the first JSON object or returning the raw content as a single decoded item.

### Flask routes and templates

- `GET /`
  - Renders `index.html` with:
    - Fandom dropdown.
    - Three textareas for batch mode.
    - Empty results and history area.

- `POST /decode`
  - Reads up to three text fields (`text1`, `text2`, `text3`) and the `fandom` preset.
  - Calls `decode_slang`.
  - Renders `index.html` with the decoded items and any error message.

The `index.html` template:

- Shows each decoded item with:
  - Original text.
  - Plain‑English decoded text.
  - A glossary list where each slang term is a hoverable tooltip.
- Provides **Copy decoded text** and **Copy share blurb** buttons per item.
- Exposes the fandom key and original/decoded text as `data-` attributes so the frontend script can build the session history.

### Frontend behaviour

`static/js/main.js` is a small vanilla JS helper that:

- **Dark mode**
  - Uses a checkbox in the header.
  - Toggles a `dark` class on `<body>`.
  - Stores the preference in `localStorage` so it persists across reloads.

- **Copy / share**
  - Copies the decoded text or a share message to the clipboard using `navigator.clipboard` when available.
  - Falls back to a hidden `<textarea>` + `document.execCommand("copy")` when needed.

- **Usage history**
  - After each decode, reads the newly rendered result cards and adds them to a `fandomslang_history` array in `localStorage`.
  - Keeps only the **five most recent** entries.
  - Renders the history list into the “Recent decodes” sidebar.

## Notes and limitations

- The app relies on the OpenAI API, so:
  - You must have a valid API key with sufficient quota.
  - Responses can vary slightly between calls.
- The decoder aims to neutralise or soften offensive slang, but you may still see rough language if present in the input.
- History is **per browser** and **per device**, using `localStorage` only. Clearing site data or switching browsers will reset it.

## Manual testing checklist

When running locally, you can quickly test the core flows:

- Single decode:
  - Choose “General Internet”.
  - Paste: `This arc slaps, mid-tier villain with insane rizz.` and click **Decode**.
  - Verify a clear English explanation and a glossary entry for “slaps”, “mid-tier”, and “rizz”.
- Batch mode:
  - Fill `Text 1`, `Text 2`, and `Text 3` with short fandom messages and decode them all at once.
- Presets:
  - Try “Anime / Manga” with `peak isekai MC, plot is kinda mid but the OP goes hard`.
  - Try “K‑pop” with `the comeback stage destroyed me, my bias wrecked me this era`.
- Dark mode:
  - Toggle the switch; verify colours update and the choice sticks after a reload.
- Copy / share:
  - Click **Copy decoded text** and paste into a text editor.
  - Click **Copy share blurb** and verify the prefix `Decoded via FandomSlang Decoder` appears.
- History:
  - Perform several decodes, then confirm that the “Recent decodes” panel shows up to the last five entries only.

