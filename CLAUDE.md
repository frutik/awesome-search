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

- **`awesome-search-knowledge-graph`** — the main ingestion pipeline: fetch an
  article/video/URL → extract entities (concepts, topics, people, companies,
  tools, case studies) → create/update notes → cross-link → update
  `global_toc.md` and `HOME.md`/`index.md` invariants → write a History entry
  → spawn `kg-reviewer` to audit → apply its findings. Always uses the Obsidian
  MCP server for vault reads/writes — **never** raw filesystem tools (Read/
  Write/Bash) against `obsidian/vault/`.
- **`kg-readme-writer`** — syncs root `README.md` from vault state
  (`global_toc.md` + latest History weeks), converting `[[wikilinks]]` to
  plain Markdown links pointed at the published site
  (`https://frutik.github.io/awesome-search/...`), using Quartz's slugging
  rules (whitespace → `-`, `&` → `-and-`, `%` → `-percent`, drop `?`/`#`).
  Edits in place; never regenerates from scratch; `README.md` lives at the
  repo root, not inside the vault.
- **`awesome-search-kg-history`** — writes the dated entry in
  `Awesome Search/History/<year>.<week>.md` after every content batch: one
  subject-first paragraph (60–120 words, mailing-list voice, no deliberation,
  no running totals, never says "vault"/"the graph"), a `(N new, M updated)`
  count, ≤3 Corrections bullets. `History.md` stays a pure newest-first index
  of week-file links.
- **`awesome-search-kg-frontmatter` / `-orphans` / `-hubs` / `-clusters`** —
  quality audits, run in that order: missing frontmatter → orphan notes (zero
  in/out links) → hub/topic-coverage mismatches → disconnected clusters.
- **`awesome-search-tutor`** — read-only Q&A over the published content, not a
  vault-writing skill.

### Vault conventions worth knowing without opening a skill file

- Note folders: `Concepts/`, `Topics/`, `People/`, `Companies/`, `Tools/`,
  `Conferences/`, `Case Studies/`, `Datasets/`, `Articles/`, `Videos/`.
- Frontmatter always has `type:` (`concept`/`topic`/`person`/`company`/`tool`/
  `conference`/`article`/`video`) plus type-specific fields (`aliases`,
  `website`/`repo`/`blog`, `related_concepts`, `source`, etc. — full table in
  `claude-skills/awesome-search-knowledge-graph/SKILL.md`).
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
