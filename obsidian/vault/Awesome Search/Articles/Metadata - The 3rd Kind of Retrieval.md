---
created: 2026-05-16
title: "Metadata: The 3rd Kind of Retrieval"
source: "https://softwaredoug.com/blog/2026/04/21/metadata-the-3rd-kind-of-retrieval"
author: "[[Doug Turnbull]]"
published: 2026-04-21
tags: [metadata-retrieval, attribute-search, explainable-ranking, ecommerce-search, query-understanding]
---

# Metadata: The 3rd Kind of Retrieval

**Author:** [[Doug Turnbull]]

## Summary

Search discussions focus on lexical vs. embedding retrieval. But there's a third retrieval philosophy that's often overlooked: **metadata retrieval** — ranking based on structured attribute matching. With LLMs, it's now easier than ever to extract attributes from queries and implement this approach.

## The Three Kinds of Retrieval

1. **Lexical** — term matching (BM25)
2. **Embedding** — semantic similarity
3. **Metadata** — structured attribute matching

## How Metadata Retrieval Works

A query like `"crimson suede couch"` can be parsed into structured attributes:

| Color | Material | Category |
|---|---|---|
| Red | Leather > Suede | Furniture > Living Room > Couches |

Products are then ranked by how closely their attributes match the specification:

| Product | Color | Material | Category | Rank |
|---|---|---|---|---|
| Red suede sofa | Red | Suede | Furniture > Living Room > Couches | 1st |
| Pink barbie recliner | Pink | Imitation leather | Recliners | 2nd |
| Mr. Beast neon desk | Green | Wood | Office > Desks | Excluded |

Each attribute has its own similarity function (e.g., color similarity uses primary/secondary color relationships).

## Why Metadata Retrieval Matters

### Explainable Ranking
Metadata retrieval produces **ranking you can have a conversation about**:
- "Would imitation leather be acceptable for a suede search?"
- "Should ankle-length leggings rank above calf-length?"

This turns ranking from an abstract black-box into something testable and stakeholder-communicable.

### Testable Without Extensive User Evals
Attribute-based ranking can be unit-tested:
- "These tangential financial reports may show below earnings reports, but it must be about company XYZ"
- "Show ankle-length first, then calf-length, exclude knee-length"

You don't need user behavior data to discover what's broken — stakeholders can tell you directly.

### LLMs Make It Easy Now
Query-to-attribute extraction used to require extensive NLP research. LLMs now make it straightforward — classifying queries and content into attributes without specialized models.

## Connection to Agentic Search

Doug notes a link to [[Agentic Search]] — with metadata retrieval, many semantic-seeming problems become solvable through attribute-based approaches, without needing dense embeddings. This may reduce the reliance on sophisticated retrieval in certain domains.

## Related Concepts

- [[Query Understanding]] — attribute extraction from queries
- [[Faceted Search]] — similar attribute-based filtering
- [[Search Governance]] — metadata policies can be expressed as governance rules
- [[Search Intent]] — attribute matching maps to deterministic intent
- [[Semantic Search]] — metadata retrieval as an alternative to embedding-based semantic search

## Related Articles

- [[Why Ecommerce Search Needs Governance and How It Improves Retrieval]]
- [[Deconstructing E-Commerce Search - The 12 Query Types]]

## People

- [[Doug Turnbull]]
