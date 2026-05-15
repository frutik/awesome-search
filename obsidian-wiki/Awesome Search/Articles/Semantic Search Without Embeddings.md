---
title: "Semantic Search Without Embeddings"
source: "https://softwaredoug.com/blog/2026/01/08/semantic-search-without-embeddings"
author: "[[Doug Turnbull]]"
published: 2026-01-08
tags: [semantic-search, taxonomy, BM25, query-understanding, embeddings]
---

# Semantic Search Without Embeddings

**Author:** [[Doug Turnbull]]

## Reframing Semantic Search

Semantic search requires three things (not two):

1. **Representation** — a shared space for queries and content
2. **Similarity function** — how near/far items are
3. **Match criteria** *(often forgotten)* — whether an item qualifies as a match at all

Embeddings excel at 1 and 2, but poorly at 3. There's no "magic threshold" — a similarity of 0.8 doesn't mean "match" across all domains and query types.

## Taxonomy-Based Alternative

A **managed taxonomy** (hierarchical vocabulary) solves all three:

- **Representation**: category tree (e.g., `Baby & Kids / Toddler & Kids Playroom / Indoor Play / Rocking Horses`)
- **Similarity**: direct match > sibling > cousin > grandparent
- **Match criteria**: include direct node + parent; exclude grandparent/cousin if desired

Example path: `Baby & Kids / Toddler & Kids Playroom / Indoor Play / Rocking Horses / Novelty Rocking Horses`

## BM25 + Hierarchical Tokenizer

The taxonomy similarity function can be implemented in a *standard BM25 index* using a hierarchical tokenizer that produces all ancestor paths:

```
In:  hierarchical_tokenizer("Baby & Kids / ... / Rocking Horses")
Out: ['Baby & Kids',
      'Baby & Kids / Toddler & Kids Playroom',
      'Baby & Kids / Toddler & Kids Playroom / Indoor Play',
      'Baby & Kids / Toddler & Kids Playroom / Indoor Play / Rocking Horses']
```

**Why BM25 naturally gives the right ranking**: root nodes have high document frequency (common → low score); leaf nodes have low document frequency (rare → high score). Specific matches bubble up automatically.

## LLMs + Taxonomies

LLMs supercharge taxonomy maintenance:
- Given a taxonomy, LLMs can classify products/queries cheaply and accurately
- Can "hallucinate" plausible category paths for a query as a form of HyDE-style retrieval
- Makes the historically expensive management of taxonomies approachable

Sweet spot for embeddings: *building classifiers into taxonomies* — not direct retrieval. Use embeddings to find the best taxonomy node, then search within that node.

## Tradeoffs vs. Embeddings

| | Taxonomy | Embeddings |
|---|---|---|
| Explainability | High (user vocabulary) | Low (black box) |
| Cold start | Works if category exists | Random garbage without training data |
| Exact constraints | Excellent | Poor |
| Maintenance | Labor-intensive (but LLMs help now) | Data-hungry |
| Fuzzy/semantic | Limited (vocabulary-dependent) | Excellent |

## Key Insight

> "Don't apologize for living with a more organized, approach to semantic search."

Embeddings are the wrong lens for problems requiring exacting, precise matching. Taxonomies + LLM classifiers can serve as a powerful, interpretable semantic layer.

## Related Concepts

- [[Semantic Search]]
- [[BM25]]
- [[Query Understanding]]
- [[Faceted Search]]
