---
name: awesome-search-kg-orphans
description: Find orphan notes in the Awesome Search Obsidian vault — notes with no wikilinks in or out — and suggest or apply connections to existing notes. Use when running a graph health audit or when the KG feels sparse.
---

# Awesome Search KG — Orphan Finder

Use this skill to find and fix orphan notes: notes with zero inbound and zero outbound wikilinks. Orphans are captured ideas that were never connected to the knowledge graph.

## When to use

- Periodic KG quality audits
- After a batch of new articles have been processed
- When the graph feels fragmented or underlinked

## Workflow

### 1. Find orphans

Scan all notes in `Awesome Search/` for files that contain no `[[wikilinks]]` in their body AND have no other notes linking to them.

Check each folder:
- `Awesome Search/Articles/`
- `Awesome Search/Concepts/`
- `Awesome Search/People/`
- `Awesome Search/Companies/`
- `Awesome Search/Topics/`

A note is an orphan if:
- Its body contains zero `[[...]]` wikilinks, AND
- No other note in the vault contains a `[[NoteTitle]]` reference to it

### 2. Report

Output a table grouped by folder:

```
ORPHAN REPORT — Awesome Search KG
==================================
Articles (N orphans):
  - Note Title
  - ...

Concepts (N orphans):
  - ...

People (N orphans):
  - ...

Total: N orphans
```

### 3. Triage each orphan

For each orphan, read its content and determine:

- **Integrate**: note has real content worth connecting → suggest 2-3 specific wikilinks to add
- **Stub**: note is nearly empty → flag for expansion or deletion
- **Noise**: Medium/web clipping residue with no useful content → flag for deletion

### 4. Fix (if requested)

For orphans classified as **Integrate**:
- Add wikilinks to existing related notes in the body
- Add the orphan as a link in the most relevant related note's "Related" section

Do NOT delete any notes — only suggest deletion candidates and let the user confirm.

### 5. Report results

```
ORPHAN FIX SUMMARY
==================
Integrated: N notes (links added)
Flagged for expansion: N stubs
Flagged for deletion: N noise notes
Skipped: N (could not determine connections)
```

## Notes

- Only add wikilinks that are genuinely meaningful — do not create links just to eliminate orphan status
- An orphan concept note that is truly standalone is better left as-is than linked incorrectly
- Run `awesome-search-kg-hubs` after fixing orphans to check if any newly linked notes become unexpected hubs
