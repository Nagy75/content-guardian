# Content Guardian

Content Guardian is an initial, privacy-first MVP for helping families reduce inappropriate movie content. It includes:

- A Chrome/Firefox WebExtension that filters visible captions and can skip configured time ranges.
- A local desktop CLI that creates a filtered copy of a video from subtitles and optional skip intervals.

> **Important limitations:** A browser extension cannot reliably inspect or modify DRM-protected streams, and detecting sexual scenes automatically requires a carefully evaluated ML model. This MVP does not claim to detect scenes automatically. It supports subtitle filtering and parent-configured scene intervals. Always preview the output and supervise children.

## Repository layout

- `extension/` — browser extension source (Manifest V3).
- `desktop/` — Python CLI using FFmpeg.
- `config/blocked-words.example.json` — example word list and skip intervals.

## Browser extension quick start

1. Open `chrome://extensions` (Chrome/Edge) or `about:debugging` (Firefox).
2. Enable developer mode.
3. Choose **Load unpacked** and select `extension/`.
4. Open the extension settings and configure blocked words and time intervals.

The extension filters HTML5 `<track kind="subtitles">` cues and common caption elements. Streaming services may use DRM, canvas, shadow DOM, or custom caption rendering, which the extension cannot always access.

## Desktop quick start

Requirements: Python 3.10+ and FFmpeg available on `PATH`.

```bash
python -m venv .venv
. .venv/bin/activate       # Windows: .venv\\Scripts\\activate
python -m pip install -e desktop
python -m content_guardian.cli input.mp4 --output filtered.mp4 --words config/blocked-words.example.json
```

For a manually reviewed scene interval:

```bash
python -m content_guardian.cli input.mp4 --output filtered.mp4 \
  --skip 00:12:10-00:13:05 --skip 00:48:00-00:49:30
```

The desktop MVP mutes detected profanity in subtitle-aligned windows and removes configured intervals. Keep the original file; it never overwrites the input.

## Safety and privacy

Processing is local by default. Do not upload children’s viewing data or recordings without informed consent. Word lists and timestamps are only starting points: languages, context, and ratings differ, so parents should review results.

## Roadmap

- Subtitle-file import for more players and formats.
- Parent PIN and local profiles.
- Better accessibility and audit logs stored only on the device.
- Optional, opt-in scene-analysis plugin with transparent confidence and human review.
- Automated tests for caption filtering and interval parsing.
