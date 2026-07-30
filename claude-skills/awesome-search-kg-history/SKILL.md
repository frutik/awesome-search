---
name: awesome-search-kg-history
description: Write the dated history entry after any Awesome Search KG batch (new notes, enrichment, corrections). Entries go into weekly History/<year>.<week>.md files; History.md is only an index of links to them. Enforces a fixed entry format. Invoke at the end of every batch, before kg-reviewer.
---

# Awesome Search KG — History Entry

Writes one dated entry after a batch of vault work. The entry is written from
**session context** — the decisions, corrections, and dead ends of the run just
finished — never reconstructed from diffs. If a kg-writer subagent did the work,
write the entry from its report.

History is a *log*, not an essay collection. Terse, factual, scoped.

## Scope: one entry = one coherent edit

An entry describes a **single consistent unit of work**: one source (article,
video, series), one correction, or one cluster built around one theme. If the
session did unrelated things — e.g. processed an article *and* fixed an
unrelated stub — write **separate entries**, one per unit, each with its own
heading and counts. Never merge unrelated work into one entry to save space,
and never pad one unit's entry with another unit's details.

## File layout

- `Awesome Search/History/<year>.<week>.md` — the actual log, one file per
  **ISO week**, zero-padded week number (e.g. `2026.31.md`). Entries newest
  first, separated by `---`. Header:

  ```markdown
  ---
  tags:
    - meta
    - history
  ---
  # History — <year> week <WW> (<Mon d – Sun d, year>)

  Newest first.
  ```

- `Awesome Search/History.md` — **index only**, never entries. One line per
  week file, newest on top:

  ```markdown
  - [[2026.31]] — Jul 27 – Aug 2, 2026 (11 entries)
  ```

- `Awesome Search/History/History Stats.md` — the approximate note-count
  table; append a row only if the batch warrants it (optional).

## Entry format (fixed)

```markdown
## YYYY-MM-DD — <Title, ≤10 words> (N new, M updated)

<ONE prose paragraph, 2–4 sentences, ≤80 words. What was processed and from
where (source/author/series), and the one thing a future reader needs to know.
Plain statements of fact — no scene-setting, no rhetorical build-up.>

**Decisions** (optional, only if the run made non-obvious calls)
- <≤3 bullets, one line each: corrections, ungrounded claims removed, renames,
  aliasing calls, deliberate omissions — with the [[note]] they live in.>

**New** — [[Note]] (≤8-word gloss) · [[Note]] · …
**Updated** — [[Note]] (reason, only when not obvious) · [[Note]] · …
```

## Hard rules

1. **Newest first.** Prepend under the week file's intro, separated from the
   previous entry by `---`.
2. **Heading count is always `(N new, M updated)`.** No `(~14 notes)`,
   no `(0 notes, 1 correction)` — a correction-only run is `(0 new, 3 updated)`.
3. **One paragraph, ≤80 words.** Never more. No `### ` subheadings, no tables,
   no block quotes, no formulas, no bold inline part-markers (`**Part one**`, …).
   If the material deserves that much prose, it belongs in the notes themselves —
   link to them.
4. **No chattiness.** Cut narrative framing ("The vault had exactly one…",
   "which makes X worth revisiting"), findings retold from the source, quotes,
   metrics, and lessons — those live in the notes. The log answers *what
   changed and why*, not *what the article says*. If a sentence would survive
   in the note itself, it doesn't belong here.
5. **Decisions go in the Decisions bullets**, not woven into paragraphs. Max 3.
   This is where the richness lives: what got corrected, what didn't ground,
   what was deliberately left out. If a decision needs more than a line, put the
   detail in the affected note and link it.
6. **Typed New line(s).** If the batch spans multiple note types, split into
   typed lines in this order: **Articles** / **Videos** / **Concepts** /
   **Topics** / **People** / **Companies** / **Tools** / **Case Studies** /
   **Datasets** / **Conferences** — each replacing the single **New** line. Glosses ≤8 words, only where the
   title alone is opaque.
7. **Updated line lists content notes only.** Never `[[global_toc]]`,
   `[[Index]]`, `[[index]]`, MOC/section files, or History itself — index
   maintenance is an invariant of every run and logging it is noise.
8. **Every wikilink must resolve** to an existing note (same names/aliases used
   in the batch).
9. Multiple entries on the same date (or for the same session) are fine and
   expected when work was unrelated — one entry per coherent edit, each
   distinguished by title.

## Procedure

1. Collect from the session: what was created, what was updated, which decisions
   were made. **Split the work into coherent units** (one source / one
   correction / one cluster) — each unit gets its own entry. Per unit, compute
   N (files created) and M (content notes modified, excluding index/TOC/MOC
   files).
2. Determine the current ISO year and week for today's date
   (`date +%G.%V` gives it directly, e.g. `2026.31`).
3. If `History/<year>.<week>.md` does not exist: create it with the header
   above, and prepend its index line to the link list in `History.md`
   (newest on top).
4. Draft each entry inside the template. Check every hard rule above.
5. Prepend the entries to the week file, below its intro. Use the Obsidian MCP
   server (disk edit only if the REST API is down, per vault conventions).
6. Refresh the entry count on this week's line in `History.md`.
7. Report the entry heading(s) and paragraph word count(s) in your summary.

kg-reviewer verifies the newest entry against this format after every batch.
