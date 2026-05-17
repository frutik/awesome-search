---
name: awesome-search-kg-frontmatter
description: Audit all notes in the Awesome Search Obsidian vault for missing or incomplete frontmatter. Reports violations by folder and optionally auto-fixes notes where values can be inferred from content. Use for KG consistency checks.
---

# Awesome Search KG — Frontmatter Audit

Use this skill to check all notes for required frontmatter fields and fix missing values where they can be inferred from content.

## When to use

- After processing a batch of new articles
- When notes feel inconsistently structured
- Before running other KG quality skills (clean frontmatter makes other checks more reliable)

## Required fields by note type

| Type | Required fields |
|---|---|
| `article` | `type`, `title`, `source`, `author`, `created`, `tags`, `concepts` |
| `concept` | `type`, `tags`, `created` |
| `topic` | `type`, `tags`, `related_concepts`, `created` |
| `person` | `type`, `tags`, `created` |
| `company` | `type`, `tags`, `created`, `website` (if known) |
| `tool` | `type`, `tags`, `created`, `website` or `repo` (if known) |

## Vault Access

**Always use the Obsidian MCP server for all vault operations** — never access the vault directly via the filesystem (no Read/Write/Bash file tools). The MCP server is the only sanctioned way to read, search, create, and edit notes.

## Workflow

### 1. Scan all notes

Check every note in `Awesome Search/` for:
- Missing `type` field
- Missing `created` field
- Missing `source` field (articles only)
- Missing `tags` field
- Missing `concepts` or `related_concepts` (articles and topics)
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

- Run this skill before `awesome-search-kg-orphans` — orphan detection is more reliable with consistent `type` fields
- Notes in `Clippings/` and `raw_articles/` are exempt — they are pre-processing staging areas, not KG notes
