---
name: youtube-transcribe
description: Transcribe a YouTube video to clean plain text. Triggers on a YouTube URL with a request to transcribe/get the transcript/text of a video, or `/youtube-transcribe <url>`. Produces a cleaned transcript plus video metadata (title, channel, upload date, URL) ready to hand off to the article/KG processing workflow.
---

# YouTube → Text Transcription

Turn a YouTube video into clean plain text so it can be fed into the normal
`kg-article-processing` workflow.

## When to use

- The user gives a YouTube URL and asks to transcribe it, "get the text", "get the transcript", or "process this video".
- `/youtube-transcribe <url>`

This skill only produces text + metadata. It does **not** create vault notes — hand the
result off to the `kg-article-processing` skill (which, per [[video_notes_convention]],
puts video content in `Awesome Search/Videos/` with `type: video`, not `Articles/`).

## Tooling (verified available on this machine)

- `yt-dlp` — downloads captions and audio. **Primary path** — no transcription model needed when captions exist.
  - If YouTube answers "Sign in to confirm you're not a bot", add
    `--cookies-from-browser chrome`. Cookie decryption needs macOS keychain access, so
    the command must run **without the sandbox** (expect a permission prompt).
  - If metadata/caption calls then fail with "Requested format is not available"
    (JS challenge), add `--ignore-no-formats-error` — formats are irrelevant for
    captions and `--print` metadata.
- `ffmpeg` — audio extraction (fallback path only).
- `whisper` is **not** installed. The fallback path needs it; see step 3.

Work in the scratchpad directory, not the vault or `/tmp`.

## Workflow

### 1. Fetch metadata

```bash
yt-dlp --skip-download --print "%(title)s\n%(uploader)s\n%(upload_date)s\n%(webpage_url)s\n%(duration_string)s" "<URL>"
```

Capture: **title**, **channel/uploader** (→ author), **upload_date** YYYYMMDD (→ published),
**canonical URL** (→ source), duration. Keep these — the downstream note needs them.

### 1a. Fetch official chapters (always)

Always also try to extract the video's official chapters (creator-defined or
YouTube-extracted):

```bash
yt-dlp --skip-download --print "%(chapters)s" "<URL>"
```

- Output is a Python-style list of `{start_time, end_time, title}` dicts, or `NA`/empty
  when the video has none.
- Include the chapter list (as `MM:SS  Title` lines) in the handoff under a
  `## Chapters` heading so the KG note can turn them into a clickable **Key Moments**
  table (`https://www.youtube.com/watch?v=<ID>&t=<start>s` links).
- Official chapters are often coarse or cover only part of the video (a lone
  `<Untitled Chapter 1>` counts as none). When they're missing or thin, derive finer
  key moments from the `.vtt` cue timestamps: locate anchor phrases of each section in
  the caption cues and record their start times.

### 2. Primary path — extract captions (fast, preferred)

Most videos have manual or auto-generated captions. Prefer manual (`--write-subs`) over
auto (`--write-auto-subs`); convert to a stable format and clean.

```bash
cd "<scratchpad>"
yt-dlp --skip-download \
  --write-subs --write-auto-subs \
  --sub-langs "en,en-orig" --sub-format vtt \
  --convert-subs vtt \
  -o "cap.%(ext)s" "<URL>"
```

**Do not** use a wildcard like `--sub-langs "en.*"` — it matches every machine-translated
`en-XX` track (en-ar, en-bn, …), which downloads dozens of files and trips YouTube's
`HTTP 429 Too Many Requests` rate limit. List exact codes: `en` (and `en-orig` for the
original track of a dubbed video). To see what a video actually offers, run
`yt-dlp --list-subs --skip-download "<URL>"` first.

Then clean the `.vtt` into deduplicated prose with the bundled script:

```bash
python3 ~/.claude/skills/youtube-transcribe/scripts/vtt2text.py cap.en.vtt > transcript.txt
```

Notes:
- If both a manual `cap.en.vtt` and an auto-generated file appear, prefer the manual one
  (human captions have punctuation and casing). Use `--list-subs` to tell them apart.
- For non-English videos, pass the exact language code (e.g. `--sub-langs "ru,ru-orig"`).
  If the user wants English from a foreign video, try `--sub-langs "en"` for a translated
  track; if none exists, fall back to the original language.
- Inspect `transcript.txt` — captions lack punctuation/casing but are fully usable for KG extraction.

### 3. Fallback path — no captions available

If step 2 yields no `.vtt` (or an empty transcript), the video has no captions. `whisper` is not
installed, so **stop and tell the user** rather than silently failing. Offer:

- **Install a transcriber** (one-time), e.g. `pipx install openai-whisper` or `brew install whisper-cpp` / `uv tool install mlx-whisper` (Apple Silicon, fastest). Then:
  ```bash
  yt-dlp -x --audio-format mp3 -o "audio.%(ext)s" "<URL>"
  whisper audio.mp3 --model small --output_format txt --output_dir .   # or: mlx_whisper audio.mp3
  ```
- Or the user pastes any transcript they already have.

Don't assume a transcriber exists — verify with `which` before invoking, and don't download
large models without asking.

### 4. Assemble the handoff

Produce a small text/markdown block the article workflow can consume directly:

```markdown
---
title: "<title>"
type: video
source: <canonical URL>
author: "<channel/uploader>"
published: <YYYY-MM-DD>
tags: [video]
---

# <title>

<cleaned transcript text>
```

Keep this handoff in the **scratchpad only** — do **not** store the raw transcript in the
vault (no `raw_articles/` copy, and never paste the full transcript into a vault note).
The transcript is working material: the KG workflow reads it from the scratchpad, distills
it into the `Videos/` note (summary, key moments, entities), and the raw text is discarded
with the scratchpad. If a staging copy was ever written to the vault, delete it once
processing is done.

Then offer to run the `kg-article-processing` skill on the scratchpad handoff
to create the `Videos/` note — it hands off to `kg-note-writing` from there to
extract entities and cross-link.

## Guardrails

- Only transcribe videos the user explicitly provides. Don't batch-crawl channels/playlists unless asked.
- Downloading full audio is bandwidth-heavy — only do it on the fallback path, and prefer captions.
- Report honestly when captions are missing or a language track isn't available; don't fabricate transcript text.
