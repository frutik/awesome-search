---
name: awesome-search-kg-hubs
description: Audit hub notes in the Awesome Search Obsidian vault — rank notes by inbound link count and compare against existing Topics/ notes. Surfaces mismatches where high-traffic concepts lack a proper topic page. Use for periodic graph structure reviews.
---

# Awesome Search KG — Hub Audit

Use this skill to identify the true hub notes in the vault by inbound link count, then compare them against the existing `Awesome Search/Topics/` notes. A mismatch — where a concept note has more inbound links than its topic page — is a restructuring signal.

## When to use

- After a significant batch of new articles have been processed
- When the Topics/ folder feels out of sync with the actual content
- Periodically (e.g. monthly) as part of graph health maintenance

## Vault Access

**Always use the Obsidian MCP server for all vault operations** — never access the vault directly via the filesystem (no Read/Write/Bash file tools). The MCP server is the only sanctioned way to read, search, create, and edit notes.

## Workflow

### 1. Count inbound links for all notes

For every note in `Awesome Search/`, count how many other notes contain a `[[wikilink]]` pointing to it.

Focus on:
- `Awesome Search/Concepts/` — these are the most likely hubs
- `Awesome Search/Topics/` — these should be hubs but sometimes aren't
- `Awesome Search/People/` — high-link people may need richer notes

### 2. Produce the top-N ranking

Output the top 20 notes by inbound link count:

```
HUB RANKING — Awesome Search KG
================================
Rank | Note                        | Folder    | Inbound Links
-----|-----------------------------|-----------|--------------
  1  | Hybrid Search               | Concepts  | 34
  2  | BM25                        | Concepts  | 28
  3  | Search Evaluation           | Concepts  | 25
  ...
```

### 3. Compare against Topics/

For each top-ranked concept, check:
- Does a corresponding `Topics/` note exist?
- If yes: does the topic note have fewer inbound links than the concept? (mismatch)
- If no: should one be created?

Flag mismatches:

```
MISMATCH REPORT
===============
- "Hybrid Search" (Concepts, 34 links) > "E-commerce Search" (Topics, 12 links)
  → Consider elevating Hybrid Search to a Topic note

- "LLM as Judge" (Concepts, 18 links) — no Topic note exists
  → Candidate for new Topic: "LLM-Based Evaluation"
```

### 4. Flag under-linked Topics

Also check the reverse: existing `Topics/` notes with very few inbound links (< 3). These may be:
- Correctly low-traffic niche topics (OK)
- Topics that haven't been linked from articles yet (needs linking)
- Topics that are redundant with a concept note (consider merging)

### 5. Recommendations

For each mismatch or gap, produce one of:
- **Elevate**: promote a concept note to a topic note (or create a new topic note)
- **Link**: existing topic note just needs more article links added to it
- **Merge**: topic and concept overlap significantly — consolidate
- **Monitor**: not actionable yet but worth watching

Do not make changes automatically — present recommendations for user approval.
