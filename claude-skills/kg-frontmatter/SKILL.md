---
name: kg-frontmatter
description: Audit all notes in the Awesome Search Obsidian vault for missing or incomplete frontmatter. Reports violations by folder and optionally auto-fixes notes where values can be inferred from content. Use for KG consistency checks.
---

# Awesome Search KG — Frontmatter Audit

Use this skill to check all notes for required frontmatter fields and fix missing values where they can be inferred from content.

## When to use

- After processing a batch of new articles
- When notes feel inconsistently structured
- Before running other KG quality skills (clean frontmatter makes other checks more reliable)

## Required fields by note type

Every note type requires the baseline `type`, `tags`, `created` (per
`kg-note-writing`'s Note Structure). This table adds the fields specific to
each type, from `kg-note-writing`'s Supported Entities table — that table is
the source of truth for the field set; update it there first if the vault's
frontmatter conventions change, then mirror the change here.

| Type | Required beyond `type`/`tags`/`created` |
|---|---|
| `article` | `source`, `author`, `concepts` |
| `video` | `speaker`, `url`, `concepts` |
| `concept` | — |
| `topic` | `related_concepts` |
| `person` | — |
| `company` | `website` (if known) |
| `tool` | `website` or `repo` (if known) |
| `conference` | `website` (if known), `organizer` (if known) |
| `case_study` | `companies`, `related_concepts`, `source` |
| `dataset` | `website` or `repo` (if known), `related_concepts` |

## Vault Access

**Always use the Obsidian MCP server for all vault operations** — never access the vault directly via the filesystem (no Read/Write/Bash file tools). The MCP server is the only sanctioned way to read, search, create, and edit notes.

## Workflow

### 1. Scan all notes

Check every note in `Awesome Search/` — across every folder (Articles,
Videos, Concepts, Topics, People, Companies, Tools, Conferences, Case
Studies, Datasets) — against the required-fields table above:
- Missing `type` field
- Missing `created` field
- Missing `tags` field
- Missing any type-specific required field listed above (`source`/`author` for
  articles, `speaker`/`url` for videos, `related_concepts` for topics/case
  studies/datasets, `companies` for case studies, etc.)
- Notes with `type: article` but no `author`

### 2. Report violations by folder

```
FRONTMATTER AUDIT REPORT
========================
Articles/ — N notes, N violations:
  Missing `source`:  [list of note names]
  Missing `author`:  [list]
  Missing `concepts`: [list]

Concepts/ — N notes, N violations:
  Missing `type`:    [list]
  Missing `created`: [list]

People/ — N notes, N violations:
  ...

Total violations: N across N notes
```

### 3. Auto-fix where possible

For each violation, attempt to infer the missing value from note content:

- `type`: infer from folder (`Articles/` → `article`, `Concepts/` → `concept`, etc.)
- `created`: use file creation date if available, otherwise `2026-05-17`
- `tags`: infer from folder and note content
- `author`: look for `**Author:**` or `**Source:**` lines in the note body
- `source`: look for URLs in the note body

Ask for confirmation before writing, or auto-fix if the user has approved batch mode.

### 4. Flag un-inferable violations

For fields that cannot be reliably inferred (e.g. `concepts` for an article with no entity extraction yet), flag the note for manual review:

```
NEEDS MANUAL REVIEW
===================
- Articles/Some Article.md — missing `concepts` (no entity extraction done)
- People/Some Person.md — missing `website` (could not find URL in note)
```

### 5. Summary

```
FIX SUMMARY
===========
Auto-fixed: N fields across N notes
Flagged for manual review: N notes
No action needed: N notes
```

## Notes

- Run this skill before `kg-orphans` — orphan detection is more reliable with consistent `type` fields
- Notes in `Clippings/` and `raw_articles/` are exempt — they are pre-processing staging areas, not KG notes
