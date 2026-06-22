---
title: "Compositional Queries"
aliases: ["compositional queries", "compositional query", "boolean attribute queries", "set queries"]
tags:
  - concept
  - information-retrieval
  - faceted-search
  - embeddings
---

# Compositional Queries

Queries that **combine multiple attributes with logical operators** — AND, OR, NOT — rather than asking about a single condition. Example: *"comedies **AND** British **BUT NOT** romances"*. They are the everyday shape of **[[Faceted Search|faceted browsing]]** and structured recommendation, where users stack and negate filters.

## Why They're Hard for Vector Embeddings

Dot-product [[Dense Embeddings|vector embeddings]] score one item against one query direction. They have no native notion of **set membership**, so AND/OR/NOT don't compose cleanly — combining or negating attributes in vector space is an approximation that degrades as more conditions are added, and especially at larger retrieval-set sizes.

## The Set-Theoretic / Box Approach

[[Set-Theoretic Embeddings]] — and concretely [[Box Embedding|box embeddings]] (*"learnable Venn diagrams"*) — map the logical operators onto **region operations**:

| Query operator | Set / region operation |
|---|---|
| AND | intersection (overlap volume) |
| OR | union |
| NOT | complement |

This makes compositional matching a geometric, first-class operation. See [[Answering Compositional Queries with Set-Theoretic Embeddings]] for evidence that boxes beat vectors on exactly these queries.

## Related Concepts
- [[Faceted Search]] — the UX where compositional attribute queries dominate
- [[Set-Theoretic Embeddings]] — embeddings that support these operators
- [[Box Embedding]] — concrete representation answering AND/OR/NOT
- [[Compositional Embeddings]] — composing meaning via set operations
- [[Dense Embeddings]] — point vectors that struggle with composition

## Articles
- [[Answering Compositional Queries with Set-Theoretic Embeddings]] — [[Shib Sankar Dasgupta]] et al.; boxes vs. vectors on compositional queries
