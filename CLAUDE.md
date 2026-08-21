# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Not a software project — a curated knowledge graph about search and information
retrieval, authored as an Obsidian vault and published as a static site. There is no
application code, no test suite, and no package manager here.

- `obsidian/vault/Awesome Search/` — the actual content: an Obsidian vault of
  interlinked Markdown notes (Concepts, Topics, People, Companies, Tools,
  Conferences, Case Studies, Datasets, Articles, Videos, History).
- `docs/` — generated static site output (built by Quartz, published via GitHub
  Pages). Never hand-edit; it's overwritten by `build-web.sh`.
- `README.md` — a published mirror of the vault's table of contents
  (`global_toc.md`) plus links to recent History entries. Kept in sync by the
  `kg-readme-writer` skill, not written by hand.
- `mails/` — generated per-week HTML email digests of the History log, one
  `<year>.<week>.html` file per week. Written by the `kg-mail-list` skill,
  never hand-edited.
- `claude-skills/` — the Claude Code skills that do essentially all the writing
  work in this repo (see below). `install-claude-skill.sh` copies them to
  `~/.claude/skills`.
- `.claude/agents/` — `kg-writer` (writes/enriches vault notes) and
  `kg-reviewer` (audits what kg-writer just did; never writes).

## Build / publish

```sh
sh build-web.sh   # cd quartz && npx quartz build --output ../docs --directory ../obsidian/vault/Awesome\ Search
                   # then python3 fix-folder-pages.py docs, then docs/History.html -> docs/index.html
sh release.sh      # build-web.sh, then commit+push obsidian/ and docs/
```

`quartz` is a sibling checkout, gitignored, not part of this repo — `build-web.sh`
assumes it already exists locally. `fix-folder-pages.py` is a required
post-processing step, not optional cleanup: when a note shares a name with a
sibling folder (`Concepts.md` next to `Concepts/`), Quartz emits that note a
second time as the folder's `index.html` but only fixes the asset paths for the
deeper location — links inside stay anchored to the shallower original and
resolve one level too deep once served from the folder URL. The script
re-anchors `href`/`src` targets that start with `./`. See the script's
docstring for the full mechanism.

There is a link-check GitHub Action (`.github/workflows/awesome-search-actions.yml`,
manually triggered) that runs `markdown-link-check` over the repo.

## Editing the knowledge graph

Content work happens through the skills in `claude-skills/`, not ad hoc edits —
each encodes vault conventions that are easy to violate by hand (frontmatter
shape, dense mutual `[[wikilinks]]`, canonical entity names, the History log
format). Skim `claude-skills/README.md` for the full list and invocation
triggers; the core ones:

- **`kg-article-processing`** — the fetch stage for a single article/video
  URL/note: fetch → detect paywall → save the Article/Video source note. Does
  not extract entities or write other notes itself; hands off to
  `kg-note-writing` once the source note is saved. Always uses the Obsidian
  MCP server for vault reads/writes — **never** raw filesystem tools (Read/
  Write/Bash) against `obsidian/vault/`.
- **`kg-note-writing`** — extracts entities (concepts, topics, people,
  companies, tools, case studies) → normalizes → creates/updates notes →
  cross-links. Entered either via `kg-article-processing`'s handoff (grounded
  in the fetched source text) or directly for a note synthesized from notes
  already in the vault with no new source — e.g. "write a topic note pulling
  together what we have on X" — grounded in those existing notes instead.
  Hands off to `awesome-search-knowledge-graph` once notes are written.
- **`awesome-search-knowledge-graph`** — the graph-wide maintenance pass, run
  after any batch of note changes (from `kg-note-writing`, `kg-writer`, or a
  manual edit): update `global_toc.md` and the `HOME.md`/`index.md` mirror
  invariant → write a History entry → spawn `kg-reviewer` to audit → apply its
  findings. Not itself a content-writing skill.
- **`kg-readme-writer`** — syncs root `README.md` from vault state
  (`global_toc.md` + latest History weeks), converting `[[wikilinks]]` to
  plain Markdown links pointed at the published site
  (`https://frutik.github.io/awesome-search/...`), using Quartz's slugging
  rules (whitespace → `-`, `&` → `-and-`, `%` → `-percent`, drop `?`/`#`).
  Edits in place; never regenerates from scratch; `README.md` lives at the
  repo root, not inside the vault.
- **`kg-history`** — writes the dated entry in
  `Awesome Search/History/<year>.<week>.md` after every content batch: one
  subject-first paragraph (60–120 words, mailing-list voice, no deliberation,
  no running totals, never says "vault"/"the graph"), a `(N new, M updated)`
  count, ≤3 Corrections bullets. `History.md` stays a pure newest-first index
  of week-file links.
- **`kg-mail-list`** — compiles one week's History entries
  into a plain-language HTML digest at `mails/<year>.<week>.html`: the prose
  paragraphs and Corrections as written, wikilinks converted to site links
  (same slugging as `kg-readme-writer`), but with every count/statistic
  (`(N new, M updated)`, totals) stripped — not a vault-writing skill.
- **`kg-frontmatter` / `-orphans` / `-hubs` / `-clusters`** —
  quality audits, run in that order: missing frontmatter → orphan notes (zero
  in/out links) → hub/topic-coverage mismatches → disconnected clusters.
- **`kg-audit`** — the same four checks plus duplicate-source articles and
  unresolved wikilinks, in one pass via `claude-skills/kg-audit/scripts/
  kg_audit.py`. The one deliberate exception to the MCP-only rule above: at
  800+ notes it reads the vault straight off disk (read-only) instead of
  four separate MCP-backed scans. Prefer this over running the four
  individually.
- **`awesome-search-tutor`** — read-only Q&A over the published content, not a
  vault-writing skill.

### Vault conventions worth knowing without opening a skill file

- Note folders: `Concepts/`, `Topics/`, `People/`, `Companies/`, `Tools/`,
  `Conferences/`, `Case Studies/`, `Datasets/`, `Articles/`, `Videos/`.
- Frontmatter always has `type:` (`concept`/`topic`/`person`/`company`/`tool`/
  `conference`/`article`/`video`) plus type-specific fields (`aliases`,
  `website`/`repo`/`blog`, `related_concepts`, `source`, etc. — full table in
  `claude-skills/kg-note-writing/SKILL.md`).
- Grounding is mandatory and invisible: every specific claim (number, date,
  quote, name, affiliation, "X invented Y") must trace to the source; nothing
  is filled from memory, and no meta-markers about grounding are left in the
  note.
- `global_toc.md` indexes every non-article, non-video-source note; `HOME.md`
  and `index.md` must always be byte-identical.

## Other top-level lists

`PAPERS.md`, `QUOTES.md`, `TALKS.md`, `UNDERFUNDED_SEARCH_TEAMS.md` are
standalone curated lists, separate from the Obsidian vault/KG pipeline above —
edit them directly as plain Markdown.
