---
name: kg-article-processing
description: Fetch a single article or video/transcript source, detect paywalls, and save it as the Awesome Search Article/Video note — the fetch stage of KG ingestion. Triggers on an article URL to fetch and process, or a title/name of an article/video already in the vault (Clippings/, raw_articles/, or an unprocessed Awesome Search/Articles or Videos note) that hasn't been fully processed yet. Hands off to kg-note-writing for entity extraction and cross-linking — for a note authored by synthesizing existing vault notes with no new source (e.g. a topic page), use kg-note-writing directly instead.
---

# KG Article Processing

Use this skill when the user asks to process a single article or video into
the knowledge graph. Triggers include:

- A URL to a new article to fetch and process
- A title or name of an article already in the vault (e.g. in `Clippings/`,
  `raw_articles/`, or `Awesome Search/Articles/`) that hasn't been fully
  processed yet

If there is no new source to fetch — e.g. a request to write or enrich a
Topic/Concept note by pulling together notes already in the vault — this
skill doesn't apply; use **kg-note-writing** directly instead.

## Vault Structure

- `Awesome Search/Articles/` — one note per processed article
- `Awesome Search/Videos/` — one note per processed talk/video (type: video); the video/transcript equivalent of an article. Conference talks, tutorials, recorded presentations.

(The rest of the vault's note folders — Concepts, Topics, People, Companies,
Tools, Conferences, Case Studies, Datasets — are owned by `kg-note-writing`.)

## Vault Access

**Always use the Obsidian MCP server for all vault operations** — never
access the vault directly via the filesystem (no Read/Write/Bash file tools).
The MCP server is the only sanctioned way to read, search, create, and edit
notes.

## Workflow

### 1. Fetch the source

Branch on source type first — the fetch mechanism is different for each:

- **Article** (a webpage URL, or a title referring to an existing
  `Clippings/`/`raw_articles/`/`Articles/` note not yet processed): fetch the
  full content with WebFetch. No confirmation needed.
- **Video/talk** (a YouTube URL, or a title referring to an existing
  `Videos/` note not yet processed): WebFetch cannot pull a transcript off a
  video page. Invoke the **youtube-transcribe** skill first — it downloads
  captions (falling back to audio transcription only if none exist) and
  produces cleaned transcript text plus metadata (title, channel, upload
  date, canonical URL) in the scratchpad. Treat that transcript as "the
  fetched content" for every step below — do not call WebFetch on a video
  URL.

### 1a. Detect paywall (articles only — skip for video sources)

**Paywalled means the source is gated for a reader — member-only,
subscriber-only, or behind a login.** It is a property of the source, not of
how much text this session happened to obtain. A member-only Medium post is
paywalled whether it was fetched, pasted in, or supplied as a PDF export. Do
not reason about whether the flag is "accurate" given full access; do not
propose alternative fields. Treat this section as settled.

**Paywall signals** (any one → paywalled):
- An explicit gate: "Member-only story", "Subscribe to read", "Sign in to continue", "This content is for subscribers", "Create a free account to read"
- Fetched text is significantly shorter than expected for an article (< ~300 words of body content)
- Content is cut off mid-sentence or ends with a subscription/login prompt
- Only a lede or first few paragraphs are present with no further detail
- The user says it is paywalled, or supplies the text by a route that implies a gate (PDF, export, copy-paste of a member-only post)

**If paywalled — the note is a short summary of key ideas with links to the
details. Never a restatement of the article.**

1. Add `paywall: true` to the frontmatter, and `paywalled` to `tags`.
2. Open the body with:
   ```
   > [!warning] Paywall
   > <Publisher> member-only post. Key ideas only below; details are in the original.
   > <URL>
   ```
3. One or two sentences on what the piece is and whose it is, then a
   `## Key ideas` list. One bullet per idea, each bolded lead-in plus the
   claim, and each pointing at whichever vault note carries the detail
   (`[[Jev]]`, `[[TypeSafe]]`, the topic note). Roughly 300–500 words total.
4. **No reproduction.** No block quotes of the article's prose, no
   paragraph-by-paragraph walkthrough, no section mirroring the source's
   structure. Findings, numbers and named entities are facts and belong in the
   note; the author's sentences do not. This applies equally to every other
   note that cites the source — People, Company, Topic — so paraphrase there
   too.
5. Hand off entities, concepts, and links to kg-note-writing as normal.
6. If the text was only partially visible, say so in the callout
   ("Summary based on publicly visible content only") and tell kg-note-writing
   to apply extra grounding caution. If the full text was available, the
   summary is simply complete — the flag and the length limit are unchanged.

**If not paywalled** — proceed normally.

### 2. Save the article note
Save to `Awesome Search/Articles/<Title>.md` using the standard note structure
and frontmatter fields defined in **kg-note-writing**'s SKILL.md.

For a video/talk (per the branch in step 1), save the source note to
`Awesome Search/Videos/<Title>.md` with `type: video` instead — otherwise it
follows the same workflow as an article. Conferences and recurring events
mentioned in the source get their own `Awesome Search/Conferences/<Name>.md`
note with `type: conference` (created by kg-note-writing during the handoff
below, since Conferences is one of its folders).

## Handing off

Fetching and saving the source note is only the first stage. Once the
Article/Video note is saved, invoke the **kg-note-writing** skill, passing it
the fetched text (and the paywall/thin-source caveat if applicable), to
extract entities, create/update the surrounding Concept/Person/Company/Tool/
Topic/Case-Study/Conference notes, and cross-link everything back to the
source note. That skill in turn triggers the `awesome-search-knowledge-graph`
maintenance pass. Do not consider the batch done until both have run.
