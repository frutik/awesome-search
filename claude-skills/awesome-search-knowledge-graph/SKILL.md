---
name: awesome-search-knowledge-graph
description: Apply the Awesome Search KG maintenance pass after any batch of vault note changes — write the History log entry, run the kg-reviewer audit and apply its findings, keep global_toc.md indexing every non-article note, and keep index.md byte-identical to HOME.md. Invoked at the end of kg-note-writing (which itself may be entered directly, or via kg-article-processing's fetch stage), and by any other skill or agent that creates/edits vault notes; can also be run standalone to repair these invariants after manual edits.
---

# Awesome Search Knowledge Graph — Maintenance

This skill does not write article/entity content itself — see
**kg-article-processing** (fetching a source) and **kg-note-writing** (entity
extraction and note authoring). This skill keeps the graph's structural
invariants true after any batch of note changes, regardless of what produced
them (kg-note-writing, the `kg-writer` subagent, a frontmatter fix, a manual
edit).

## Vault Access

**Always use the Obsidian MCP server for all vault operations** — never
access the vault directly via the filesystem (no Read/Write/Bash file tools).
The MCP server is the only sanctioned way to read, search, create, and edit
notes.

## Invariant: the History log records every batch

After every batch that creates or modifies content notes, write one dated
entry to the current weekly log `Awesome Search/History/<year>.<week>.md` by
invoking the **kg-history** skill
(`claude-skills/kg-history/SKILL.md`). It fixes the entry
format (one subject-first paragraph in mailing-list voice, typed link lines,
≤3 Corrections bullets), creates the week file when missing, and keeps
`History.md` as a pure index of links to week files (newest on top — never
inline entries). Write the entry from the batch's own context — what the
vault now covers and what was corrected, never a diff summary and never the
deliberation behind the choices. Do this after the notes are written, before
the review pass below.

## Review pass

After the History entry is written, spawn the `kg-reviewer` subagent with the
list of notes just created or modified. Apply its ⚠️ findings (fix grounding,
broken links, frontmatter), then continue to the invariants below before
reporting completion.

## Invariant: global_toc.md tracks every non-article note

`global_toc.md` (at the vault root) is a categorized table of contents of
**every note except articles** — it indexes Concepts, Topics, People, Tools,
Companies, Case Studies, Videos, Conferences, and Datasets, but never notes in
`Awesome Search/Articles/`, `Clippings/`, or `raw_articles/`. (Videos are the
one non-article *source* note type that still gets indexed here — under a
dedicated `## Videos` section.)

Whenever a batch **creates or renames** a non-article note (Concept, Topic,
Person, Company, Tool, Case Study, Video, Conference, Dataset), add or update
its `[[wikilink]]` in `global_toc.md` as part of the same pass:

- Place each note under its category section, and within Concepts/Topics/Tools under the most fitting thematic sub-heading (create a new sub-heading only if none fits).
- Keep entries alphabetical within a group; People are grouped by the first letter of the name.
- Use an explicit full-path wikilink (e.g. `[[Awesome Search/Topics/A-B Testing for Search|A-B Testing for Search]]`) only when the same basename exists in more than one folder; otherwise a plain `[[Note Name]]` is fine.
- Update the counts line in the header to match.

Do this before the index.md mirroring step below. If `global_toc.md` does not exist, create it by indexing the full vault.

## Invariant: index.md mirrors HOME.md

As the final step of the maintenance pass (or any operation that modifies
`HOME.md`), read the current content of `HOME.md` and overwrite `index.md`
with that exact content. These two files must always be identical. Do this as
the final step before reporting completion.
