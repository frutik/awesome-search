---
name: kg-mail-list
description: Turn one week's Awesome Search History entries into a plain, self-contained HTML email digest at mails/<year>.<week>.html in the repo root. Plain language, no statistics (no note counts, no totals) — just the substance of what changed that week, with wikilinks converted to links to the published site. Triggers on `/kg-mail-list [<year>.<week>]` or "write this week's email" / "write the mailing-list digest".
---

# Awesome Search KG — Mail Writer

Turns one week's `History/<year>.<week>.md` entries into a single HTML file
for email, in plain language, with no statistics — just what changed and why
it matters, in the same voice the History entries are already written in.

This is a **published artifact, not a vault note** — like `kg-readme-writer`'s
README.md. Vault conventions (approval, History entries, kg-reviewer) do not
apply to the output file itself, and it is written directly with the Write
tool, never inside `obsidian/vault/`.

## When to use

- `/kg-mail-list [<year>.<week>]`
- "write this week's email", "write the mailing-list digest"
- No week given → use the current ISO week (`date +%G.%V`).

## Output

- `mails/<year>.<week>.html` at the **repo root** (e.g. `mails/2026.34.html`,
  zero-padded week number, matching the History file's own naming). Create
  the `mails/` folder if it doesn't exist yet.
- One file per week. Re-running for a week that already has a file
  overwrites it (the source History file is the only truth to reflect).

## Source

Read `Awesome Search/History/<year>.<week>.md` via the **Obsidian MCP
server** — never raw filesystem tools against the vault. If that week file
doesn't exist, say so and stop; do not fabricate content or substitute a
different week.

## What goes in

Every entry in that week's file, in the order it appears in the file (newest
first):

- The entry's **title** — the text between the date and the parenthetical
  count (e.g. "Allegro's LLM-Judge Relevance Framework") — with the count
  itself dropped (see below).
- The **prose paragraph**, unedited — this is the actual content and already
  written in plain, subject-first, mailing-list language per
  `kg-history`.
- The **Corrections** bullets, if the entry has any — these are content
  (what a note said before vs. now), not statistics.
- The typed **New**/**Updated** line(s) (Articles/Videos/Concepts/Topics/
  People/Companies/Tools/Case Studies/Datasets/Conferences/Updated), rendered
  as a short list of linked note names so a reader can click through to the
  published site.

## What stays out (no statistics)

Never include: the `(N new, M updated)` count from any heading, any per-week
or cross-week total (note counts, cumulative counts, "Nth" claims), or any
other number describing the batch rather than the material. If it quantifies
the work instead of describing what changed, it doesn't belong in the email —
this mirrors `kg-history`'s own ban on totals and tallies (hard
rule 8), extended here to the heading count too, since a mail reader has even
less use for bookkeeping than a vault reader does.

## Link conversion

Same rule as `kg-readme-writer`: every `[[wikilink]]` becomes a vanilla
`<a href="...">` pointing at the published site,
`https://frutik.github.io/awesome-search/`:

- Resolve the wikilink target to the matching `.md` file (by filename stem)
  under `obsidian/vault/`; a path-style target like
  `[[Awesome Search/Topics/Foo]]` resolves against the vault root.
- Build the URL from the note's path relative to
  `obsidian/vault/Awesome Search/`, without the `.md` extension, slugified
  the way Quartz does: in each path segment, replace whitespace with `-`,
  then `&` → `-and-`, then `%` → `-percent`, and delete `?`/`#`. Everything
  else stays as-is.
- `[[Note|alias]]` uses `alias` as the link text.
- If a wikilink target doesn't resolve to a note file, keep the display text
  as plain text — never emit a broken link — and report the unresolved name
  in your summary.

## HTML structure

Self-contained, minimal, valid HTML — no external stylesheets, scripts,
fonts, or images; this is meant to render correctly as a standalone email
attachment/preview with no network access. Inline the (small) CSS.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Awesome Search — <date range from the week file's header, e.g. "Aug 17 – Aug 23, 2026"></title>
<style>
  body { font-family: Georgia, serif; max-width: 640px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; color: #1a1a1a; }
  h1 { font-size: 1.4rem; margin-bottom: 0; }
  .dateline { color: #555; margin-top: 0.25rem; }
  article { margin: 2rem 0; }
  h2 { font-size: 1.15rem; }
  a { color: #0b5fa5; }
  hr { border: none; border-top: 1px solid #ddd; margin: 2rem 0; }
</style>
</head>
<body>
<h1>Awesome Search</h1>
<p class="dateline"><date range></p>

<article>
  <h2><entry title, no count></h2>
  <p><entry paragraph, wikilinks converted to links></p>
  <!-- only if Corrections present -->
  <p><strong>Corrections</strong></p>
  <ul><li>...</li></ul>
  <!-- typed New/Updated lines, only the ones present in this entry -->
  <p><strong>New</strong>: <a href="...">Note</a>, <a href="...">Note</a></p>
  <p><strong>Updated</strong>: <a href="...">Note</a>, <a href="...">Note</a></p>
</article>
<hr>
<!-- repeat per entry, in file order -->

</body>
</html>
```

One `<article>` per History entry — multiple entries on the same date each
get their own `<article>`, per History's "one entry = one coherent edit"
rule. Drop the trailing `<hr>` after the last entry.

## Procedure

1. Determine the target week: the argument if given, else the current ISO
   week (`date +%G.%V`).
2. Read `Awesome Search/History/<year>.<week>.md` via MCP. If it doesn't
   exist, report that and stop.
3. Extract the date range from the file's `# History — <year> week <WW>
   (<range>)` header line.
4. Split the file into entries (each starts with `## YYYY-MM-DD — ...`,
   separated by `---` when there is more than one).
5. For each entry, extract: title (count stripped), paragraph, Corrections
   bullets (if any), and the typed New/Updated line(s) — resolving every
   `[[wikilink]]` to a site URL per the conversion rule above.
6. Render the HTML per the structure above, entries in the file's own order.
7. Create `mails/` at the repo root if missing; write
   `mails/<year>.<week>.html` with the Write tool (this output is outside the
   vault, so MCP does not apply to it).
8. Report: which week was written, how many entries it contains, and any
   unresolved wikilinks.
