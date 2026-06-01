---
type: article
title: "Your Obsidian Vault Is a Knowledge Graph. Here's How to Make It Think (quickly)."
source: "https://medium.com/graph-praxis/your-obsidian-vault-is-a-knowledge-graph-heres-how-to-make-it-think-quickly-1487614a7682"
author:
  - "[[Alexander Shereshevsky]]"
published: 2026-04-11
created: 2026-05-17
tags: [article, obsidian, knowledge-graph, claude-code, graph-analysis, medium]
concepts:
  - "[[Knowledge Graph Search]]"
  - "[[Graph Centrality]]"
  - "[[Orphan Notes]]"
  - "[[Bridge Notes]]"
  - "[[Cluster Analysis]]"
topics:
  - "[[Fun and Philosophy]]"
---

# Your Obsidian Vault Is a Knowledge Graph. Here's How to Make It Think (quickly).

**Author:** [[Alexander Shereshevsky]] ([Graph Praxis](https://medium.com/graph-praxis))
**Source:** https://medium.com/graph-praxis/your-obsidian-vault-is-a-knowledge-graph-heres-how-to-make-it-think-quickly-1487614a7682

> *Following the yes LLM Wiki / no LLM Wiki debate, I want to share my experience from the last five years of building a second brain in Obsidian. Connecting it to Claude Code showed me what I'd been leaving on the table.*

---

## Summary

A practitioner account of connecting Claude Code to a 5,000-note Obsidian vault. The core insight: a vault maps onto a codebase almost perfectly (notes = source files, wikilinks = imports, folders = directories, frontmatter = config), so Claude Code can navigate it with the same fluency it uses for software projects. The article focuses on two things: how to configure the integration via `CLAUDE.md`, and what graph-quality analysis becomes possible once you have it.

---

## The Core Insight

Most Obsidian-AI integration guides start with plugins and configuration. They miss the fundamental point: Claude Code was built to navigate codebases — read files, follow references, make targeted edits, execute multi-step plans. An Obsidian vault maps onto this almost perfectly:

| Codebase | Obsidian Vault |
|---|---|
| Source files | Markdown notes |
| Import statements | Wikilinks |
| Directory structure | Folder hierarchy |
| Configuration | YAML frontmatter |

The simplest integration:

```bash
cd ~/my-vault
claude
```

No plugins, no servers, no configuration. Claude Code can now read every note, create files, edit content, and search with regex.

---

## CLAUDE.md: Onboarding Documentation for Claude

When `claude` runs in a directory, it automatically reads `CLAUDE.md`. Think of it as onboarding docs for a new hire who forgets everything between sessions.

Example structure:

```markdown
# Vault Context
[description of vault purpose and scope]

## Structure
- Projects/ - active client and personal work
- Areas/   - ongoing domains
- Resources/ - reference material, book notes, papers
- Archive/  - completed work (still searchable, not active)
- _attachments/ - images and PDFs (NEVER modify)
- _templates/   - Obsidian templates (NEVER modify)
- _ai-drafts/   - staging area for AI-generated content

## Conventions
- Internal links: always [[wikilinks]], never bare URLs
- Tags: hierarchical #domain/topic format
- MOCs: prefixed "MOC - " (Maps of Content)
- Source notes: must include `source:` in frontmatter

## Rules
- NEVER modify _attachments/, _templates/, or .obsidian/
- NEVER delete notes without explicit confirmation
- Always include YAML frontmatter: date, tags, aliases
- When synthesizing, use ONLY content from vault notes
- Output drafts to _ai-drafts/ — never directly into vault

## Active Context (update before each session)
- Working on: [current project]
- Open questions: [current unknowns]
- Recent focus: [relevant folders]
```

**Three non-obvious practices:**

1. **Keep Active Context fresh.** Stale context sends Claude down yesterday's priorities. Ask Claude to append a session log at the end of each session for continuity.
2. **Reference, don't inline.** Keep interests and project context in separate notes; CLAUDE.md just references them. Avoids burning tokens on irrelevant context.
3. **Include negative instructions.** "Never modify `_templates/`" is more effective than hoping Claude figures it out.

---

## The Knowledge Graph Structure

Every Obsidian vault is an implicit graph database:

- **Nodes** = notes
- **Edges** = wikilinks (directed: A → B, but Obsidian backlinks make navigation bidirectional)
- **Subgraphs** = tags
- **Node attributes** = frontmatter properties

Obsidian's Graph View shows this structure — but it's passive. It can't tell you which notes are hubs, can't identify clusters that should be connected but aren't. That's where Claude Code fills the gap.

---

## Graph Metrics That Actually Matter

### 1. Centrality Ranking

Identifies true hub notes — concepts that connect to the most other concepts. Actual hubs often don't match "official" MOCs.

Example using TurboVault MCP:

```
get_centrality_ranking(limit=5)

1. Feedback Loops          - 38 connections (bridges 3 domains)
2. MOC - Distributed Systems - 34 connections
3. Bayesian Reasoning      - 29 connections (bridges 3 clusters)
4. Second-Order Effects    - 26 connections
5. Margin of Safety        - 24 connections
```

A hub with 38 connections that has no corresponding topic/MOC note is a restructuring signal.

### 2. Orphan Detection

Finds notes with zero incoming **and** outgoing links — ideas captured but never connected. Common after migrations or rapid note-taking.

> In a 5,000-note vault: 340 orphans found. Some worth integrating; most were archive candidates.

### 3. Cluster Analysis

Reveals natural groupings and, crucially, **which clusters are disconnected from each other**. Disconnected clusters with obvious conceptual overlap represent missed integration opportunities.

> Investing notes and systems thinking notes were two separate islands despite strong conceptual overlap — an integration opportunity missed for years.

### 4. Bridge Note Identification

Finds the rare notes that already connect otherwise isolated clusters. These are structurally the most valuable notes in the vault — the ones that do cross-domain synthesis.

---

## Related Concepts

- [[Knowledge Graph Search]]
- [[Search Architecture]]

## People

- [[Alexander Shereshevsky]] — author; 5 years of Obsidian practice, Claude Code integration
