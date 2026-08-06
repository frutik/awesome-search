---
name: awesome-search-kg-history
description: Write the dated history entry after any Awesome Search KG batch (new notes, enrichment, corrections). Entries go into weekly History/<year>.<week>.md files; History.md is only an index of links to them. Enforces a fixed entry format. Invoke at the end of every batch, before kg-reviewer.
---

# Awesome Search KG — History Entry

Writes one dated entry after a batch of work, from **session context** — what
the batch changed — never reconstructed from diffs. If a kg-writer subagent did
the work, write the entry from its report.

An entry is a **short announcement of what is now covered**, in the voice of a
mailing-list digest: someone who never opens the notes should still learn
something from the paragraph, and someone who wants more should know which note
to open.

The subject is the **finished change**, not the work that produced it. Facts
that were corrected are part of the change and belong in the entry — say what
was wrong and what it says now. Deliberation is not: never write what was
weighed, what alternatives were considered and rejected, what was deliberately
left unwritten, or why option 1 beat option 2. The process is over; only the
result is news.

The reader is already inside the knowledge base, so it is never named. Write
what happened to the material — *added*, *extended*, *corrected*, *now covers* —
and let the notes speak for where it lives.

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

`Awesome Search/History/History Stats.md` is a frozen artifact — a running
note-count table kept until 2026-07-27. Never append to it; running totals are
banned (hard rule 8).

## Entry format (fixed)

```markdown
## YYYY-MM-DD — <Title, ≤10 words> (N new, M updated)

<ONE prose paragraph, 3–5 sentences, 60–120 words, subject-first. Open on the
substance — the problem the material addresses or the claim it makes — then what
was added or extended to cover it, linking the notes inline. Close with sourcing
(author, series, paper) and any caveat a reader would be misled without
(paywalled stub, author-reported figures). Written for someone who will not
open the notes.>

**Corrections** (only when this batch changed something already written)
- <≤3 bullets, one line each: what was wrong → what it says now, in [[note]].>

**New** — [[Note]] (≤8-word gloss) · [[Note]] · …
**Updated** — [[Note]] (reason, only when not obvious) · [[Note]] · …
```

## Hard rules

1. **Newest first.** Prepend under the week file's intro, separated from the
   previous entry by `---`.
2. **Heading count is always `(N new, M updated)`.** No `(~14 notes)`,
   no `(0 notes, 1 correction)` — a correction-only run is `(0 new, 3 updated)`.
3. **One paragraph, 60–120 words.** Never more. No `### ` subheadings, no
   tables, no block quotes, no formulas, no bold inline part-markers
   (`**Part one**`, …). If the material deserves more prose than that, it belongs
   in the notes themselves — link to them.
4. **Subject first, bookkeeping never.** Open on what the material is about, not
   on the state of the graph — not "X was scattered across…", "there was no note
   owning…", "built out the Y side of the graph". Coverage gaps are the *reason*
   for the work, not the news; if a gap matters to a reader, it is because of
   what now fills it.
5. **Never write "vault", "this vault", "the graph", "the knowledge base".**
   The reader is looking at it. Say what happened to the material instead:
   *added*, *extended*, *corrected*, *reworked*, *now covers*, *now hands off
   to*. "A note on tenant skew was added" — not "the vault gained a note on
   tenant skew".
6. **Substance is welcome, retelling is not.** Carry the shape of the material —
   the tension, the ladder of options, the counter-intuitive result — in enough
   detail to be worth reading. Do not reproduce the notes: no walkthrough of
   every section, no stacked metrics, no quotes. One or two concrete figures are
   fine when they *are* the point.
7. **No deliberation, ever.** Nothing about options weighed, alternatives
   rejected, naming or filing calls, what was left unwritten, what a search
   turned up, or how sources were reconciled. The reader cannot see the roads
   not taken and does not need to. Ban phrases: "rather than", "instead of
   creating", "opted to", "left … as", "no note exists so".
8. **No totals, no tallies.** Never a running or cumulative count — not "now at
   ~660 notes", not "the 12th case study", not "one of only three notes on…".
   The `(N new, M updated)` heading count is per-entry and is the only count
   that appears anywhere.
9. **Corrections are content, not process.** A `**Corrections**` bullet appears
   only when this batch changed a claim written earlier, and states the
   correction itself: what the note said, what it says now, where. Max 3. Not
   "verified figures against the PDF" — instead "[[Note]] attributed the 30%
   uplift to the vendor's post; it is the paper's baseline-of-1 reference".
   Renames, re-filings, and deleted drafts are not corrections; omit them.
10. **Typed New line(s).** If the batch spans multiple note types, split into
    typed lines in this order: **Articles** / **Videos** / **Concepts** /
    **Topics** / **People** / **Companies** / **Tools** / **Case Studies** /
    **Datasets** / **Conferences** — each replacing the single **New** line.
    Glosses ≤8 words, only where the title alone is opaque.
11. **Updated line lists content notes only.** Never `[[global_toc]]`,
    `[[Index]]`, `[[index]]`, MOC/section files, or History itself — index
    maintenance is an invariant of every run and logging it is noise.
12. **Every wikilink must resolve** to an existing note (same names/aliases used
    in the batch).
13. **Anything named that has a note is linked.** Every concept, person, company,
    tool, engine, dataset, or source mentioned anywhere in an entry — paragraph
    included, not just the New/Updated lines — is a wikilink on first mention.
    Never `Elasticsearch, Vespa, Algolia, Qdrant` as bare prose when those notes
    exist. Check before writing rather than assuming; alias the link to keep the
    sentence readable (`[[Uber Eats - Scaling Search for Food Delivery|Uber Eats]]`).
    If a named thing has no note, it stays plain text — do not invent a link, and
    do not create the note just to satisfy this rule. When linking every member
    of a long list would bloat the paragraph, name fewer of them and link those,
    or count them ("nine engines") instead of listing.
14. Multiple entries on the same date (or for the same session) are fine and
    expected when work was unrelated — one entry per coherent edit, each
    distinguished by title.

## Worked example

Same batch, written both ways.

**Don't** — opens on the graph, then lists the run's reasoning:

> Multi-tenancy was scattered across [[Sharding]], [[Extreme Search Systems]]
> and [[Bonsai - Designing Search for a Relational Database]] with no note owning
> it. Written from vendor documentation (Elastic, Lucidworks, Vespa, Algolia,
> Meilisearch, Pinecone, Qdrant, Weaviate, Milvus) and structured as an isolation
> ladder plus a per-engine mechanism table, covering schema, routing, tenant skew,
> corpus statistics, filtered ANN, operations and access control.
>
> **Decisions**
> - Left Meilisearch as plain text in [[Multi-Tenancy in Search]] — no Tool note
>   exists and a single mechanism mention did not warrant creating one.
> - Linked [[Vespa]] (company) for streaming mode; the vault has no Vespa tool note.

**Do** — opens on the subject, links inline, ends on sourcing:

> Serving thousands of customers from one search cluster is a ladder of isolation
> choices — a tenant field on every document, a routing key, an index per tenant,
> a cluster per tenant — trading operational cost against blast radius at each
> rung. [[Multi-Tenancy in Search]] climbs that ladder and maps where nine engines
> put each rung, then covers what breaks in between: tenants skewed a thousand to
> one in size, corpus statistics that let one tenant's vocabulary distort another's
> relevance, and filtered ANN that degrades as the filter gets more selective.
> Sourced from vendor documentation. [[Sharding]] and [[Extreme Search Systems]]
> now hand off to it.

The second is longer in prose and shorter in total, and a reader who never opens
a note still leaves knowing what tenant skew is.

## Procedure

1. Collect from the session: what was created, what was updated, and any claim
   written earlier that this batch corrected. **Split the work into
   coherent units** (one source / one correction / one cluster) — each unit gets
   its own entry. Per unit, compute N (files created) and M (content notes
   modified, excluding index/TOC/MOC files).
2. Determine the current ISO year and week for today's date
   (`date +%G.%V` gives it directly, e.g. `2026.31`).
3. If `History/<year>.<week>.md` does not exist: create it with the header
   above, and prepend its index line to the link list in `History.md`
   (newest on top).
4. Draft each entry inside the template. Then reread the paragraph as a
   subscriber seeing this material for the first time: if the first sentence is
   about the graph rather than the subject, or if any clause describes a choice
   being made rather than a thing that is now true, rewrite it. Check every hard
   rule above.
5. Prepend the entries to the week file, below its intro. Use the Obsidian MCP
   server (disk edit only if the REST API is down, per vault conventions).
6. Refresh the entry count on this week's line in `History.md`.
7. Report the entry heading(s) and paragraph word count(s) in your summary.

kg-reviewer verifies the newest entry against this format after every batch.
