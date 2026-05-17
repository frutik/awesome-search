---
name: awesome-search-kg-clusters
description: Find disconnected clusters in the Awesome Search Obsidian vault — groups of notes that are internally linked but isolated from the rest of the graph. Identify semantic overlap between clusters and suggest bridge links. Use for deep graph connectivity audits.
---

# Awesome Search KG — Cluster & Bridge Audit

Use this skill to find groups of notes that form isolated islands — internally connected but with no links to the rest of the vault. Then identify semantic overlap between clusters and suggest specific bridge links.

## When to use

- When the graph view shows distinct isolated clouds of notes
- After importing or processing a new domain of articles
- Periodically to surface cross-domain connections that were missed

## Workflow

### 1. Identify clusters

Group notes into clusters based on wikilink connectivity:
- Two notes are in the same cluster if you can reach one from the other by following wikilinks (in either direction)
- A cluster is "isolated" if it has fewer than 3 outbound links to notes outside the cluster

List all clusters with size ≥ 3 notes:

```
CLUSTER REPORT
==============
Cluster A (12 notes): centred on Hybrid Search, BM25, SPLADE
  External links: 8
  
Cluster B (7 notes): centred on Agentic Search, SIRA, RAG  
  External links: 2  ← potentially isolated

Cluster C (4 notes): centred on Autocomplete, Mirror Mirror article
  External links: 1  ← isolated
```

### 2. Analyse isolated clusters

For each cluster with few external links, read the notes and summarise:
- What is this cluster about?
- What other clusters or topics does it semantically overlap with?

### 3. Suggest bridge links

For each pair of semantically overlapping but disconnected clusters, suggest specific wikilinks that would connect them:

```
BRIDGE SUGGESTIONS
==================
Cluster B (Agentic Search) ↔ Cluster A (Hybrid Search)
  Suggested links:
  - In "Agentic Search.md": add [[Hybrid Search]] (agentic systems use hybrid retrieval)
  - In "SIRA.md": add [[Retrieval Pipeline]] (already in Cluster A)
  
Cluster C (Autocomplete) ↔ main graph
  Suggested links:
  - In "Autocomplete.md": add [[Query Understanding]] (natural parent concept)
  - In "Topics/Autocomplete and Autosuggest.md": add [[Search Intent]]
```

### 4. Identify existing bridge notes

Find notes that already bridge multiple clusters (high betweenness centrality):
- These are structurally the most valuable notes in the vault
- Flag them so they can be kept rich and well-maintained

```
BRIDGE NOTES (already connecting clusters)
==========================================
- "Retrieval Pipeline" — bridges Agentic, Hybrid, and RAG clusters
- "Search Evaluation" — bridges Metrics, A/B Testing, and LLM Judge clusters
```

### 5. Apply bridges (if requested)

Add the suggested wikilinks to the relevant notes. Only add links that are semantically justified — do not create links purely to improve graph connectivity scores.
