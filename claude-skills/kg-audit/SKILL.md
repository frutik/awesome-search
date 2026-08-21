---
name: kg-audit
description: Run a fast, script-based quality audit of the Awesome Search Obsidian vault in one pass — frontmatter completeness, orphans, hub/topic coverage, disconnected clusters, duplicate articles (same source processed twice), and broken wikilinks. Use for periodic KG health checks, or when kg-frontmatter/kg-orphans/kg-hubs/kg-clusters would otherwise mean four separate full-vault scans. Triggers on "audit notes", "audit the vault", "kg health check", or `/kg-audit`.
---

# Awesome Search KG — Consolidated Audit

Runs `scripts/kg_audit.py` once over the whole vault and turns its output into
the same reports `kg-frontmatter`, `kg-orphans`, `kg-hubs`, and `kg-clusters`
produce individually, plus two checks those skills don't cover: duplicate
articles and unresolved wikilinks. One read of every note instead of four.

## Vault access — deliberate exception

Every other kg-* skill mandates the Obsidian MCP server and forbids raw
filesystem tools. This skill is the one deliberate exception: at ~800+ notes,
reading each file through MCP round-trips four separate times (once per
audit) is too slow to run routinely. `kg_audit.py` reads the vault directly
from disk with Python — **read-only, it writes nothing**. If findings lead to
fixes, make those fixes through the Obsidian MCP server or the relevant kg-*
skill, not by hand-editing files this script touched.

## When to use

- Periodic KG health checks ("audit notes", "audit the vault")
- Before/after a large batch of `kg-writer` or `kg-note-writing` runs, to
  catch systemic issues (not just per-note ones)
- Instead of running `kg-frontmatter` + `kg-orphans` + `kg-hubs` +
  `kg-clusters` back to back

## Workflow

### 1. Run the script

```sh
python3 claude-skills/kg-audit/scripts/kg_audit.py
```

Optional flags: `--vault PATH` (default: `obsidian/vault/Awesome Search` under
the repo root), `--output PATH` (default: `.scratchpad/kg_audit_result.json`,
already gitignored — never commit this file).

The script prints a one-line summary and writes full detail as JSON. Read
that JSON to build the reports below — do not re-derive the underlying data
by hand.

### 2. Duplicate articles/videos (report first — usually the highest-value finding)

`duplicate_sources` in the JSON groups Articles/Videos by their `source`/`url`
frontmatter field. Any group with 2+ notes is the *same real-world article*
processed into separate notes — often with different titles entirely (not
just an appended "1"), different summaries, and split inbound links.

```
DUPLICATE SOURCE REPORT
========================
- <source URL> (N notes)
    - Note A
    - Note B
```

For each group, read both notes and recommend which is the richer/canonical
one. Do not merge or delete anything without the user's confirmation — this
is a judgment call (which framing/summary is better), not mechanical.

### 3. Frontmatter audit

Use `fm_violations` (by folder) and `fm_violation_count`. Report violations
**grouped by pattern**, not as a flat per-note list — with 800+ notes, most
violations cluster into a handful of systemic causes (e.g. "every note in
folder X is missing field Y", "type value uses hyphens vault-wide but the
spec says underscore"). Call those out explicitly rather than listing every
note; only enumerate individual notes for violations that don't fit a
pattern. Cross-reference `duplicate_sources` — a lot of "missing concepts"
violations are usually the thinner half of a duplicate pair.

Field requirements by type are defined in `kg_audit.py`'s `REQUIRED_BY_TYPE` /
`FOLDER_TO_TYPE` — keep those in sync with `kg-note-writing`'s Supported
Entities table (the source of truth) if the vault's conventions change.

### 4. Orphans

Use `orphans` (by folder) and `orphan_count`. Same triage as `kg-orphans`:
for each orphan, read it and classify as **Integrate** (suggest 2-3
wikilinks), **Stub** (flag for expansion/deletion), or **Noise** (flag for
deletion). Do not delete anything — only suggest and let the user confirm.

### 5. Hub ranking and Topics coverage

Use `hub_data` (top 30 by inbound links) and `hub_topic_check` (naive
word-overlap match against `Topics/` titles — treat `candidate_topic_match:
null` as "no obvious topic page," not proof one is needed; verify by reading
before recommending). Also check `low_linked_topics` (<3 inbound) — flag
as **Monitor** (legitimately niche), **Link** (needs more inbound links), or
**Merge** (redundant with a concept note).

### 6. Clusters

Use `components` (connected components with ≥3 notes) and `total_components`.
If there's essentially one giant component plus a few singletons, the graph
is healthy — say so plainly rather than manufacturing cluster analysis where
none is needed. If there are genuinely multiple components of meaningful
size, read each and suggest bridge links the way `kg-clusters` does.

### 7. Unresolved wikilinks (bonus, not in the other four skills)

Use `path_style_unresolved_links` (links written with a vault-relative path
that doesn't match the actual filename — often the direct symptom of a
duplicate-article rename) and `plain_unresolved_links` (bare titles with no
matching note). For the latter, distinguish:
- naming inconsistencies (a `/` in a link where the real note uses `-`,
  case differences, singular/plural) — these are broken links to fix
- genuine gaps (a person/concept mentioned but never given a note) — normal
  in a growing KG, not urgent, don't manufacture urgency

Ignore obvious regex false positives (bracket-like syntax inside fenced code
blocks that isn't really a wikilink).

### 8. Summary

Close with a short priority-ordered action list, duplicates and any
one-root-cause bugs first, cosmetic/low-value findings last.

## Notes

- If `kg_audit.py`'s note-type field table ever drifts from
  `kg-note-writing`'s, fix it there first, then mirror the change here (same
  rule `kg-frontmatter` follows).
- This skill only reports. Fixing frontmatter, merging duplicates, adding
  links, etc. still goes through MCP-backed edits (or hand off to
  `kg-frontmatter`/`kg-orphans`/`kg-hubs`/`kg-clusters`/`kg-note-writing` for
  the actual write).
