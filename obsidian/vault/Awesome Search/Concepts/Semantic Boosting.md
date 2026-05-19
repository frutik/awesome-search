---
title: "Semantic Boosting"
aliases: ["semantic boosting", "vector-boosted lexical search"]
type: concept
tags:
  - concept
  - hybrid-search
  - retrieval
  - boosting
created: 2026-05-19
---

# Semantic Boosting

A two-shot hybrid retrieval technique that executes a vector search first, then injects the resulting document IDs and similarity scores as explicit boost clauses into a final full-text lexical query.

Introduced (named) by [[Erik Hatcher]] at [[MongoDB]] in the context of MongoDB Atlas Search.

---

## How It Works

1. **Phase 1 — Vector search**: Run `$vectorSearch` to retrieve the top-N semantically similar candidates with their similarity scores
2. **Phase 2 — Score extraction**: Extract document IDs and scores; apply a weighting multiplier to determine boost magnitude
3. **Phase 3 — Boosted lexical search**: Inject each (ID, score) pair as a `boost` clause into a `compound.should` array inside the final `$search` query

The final output is generated entirely by the lexical search engine.

## Key Property

Because the final result set comes from the lexical engine, all standard text search features work natively on hybrid results:
- **Faceting** — no extra merging logic needed
- **Highlighting** — matched terms annotated by the lexical engine
- **Pagination** — single result cursor

This distinguishes Semantic Boosting from [[Reciprocal Rank Fusion]] and [[Relative Score Fusion]], which merge two separate ranked lists and require additional plumbing for pagination and facets.

## Relationship to Signal Incorporation

Semantic Boosting is a special case of the broader *signal incorporation* pattern — where external signals (clicks, purchases, query-doc associations) are pre-computed and fed as boost factors into a lexical query. Here, the "signal" is the real-time vector similarity score.

## Tuning

The boost multiplier (e.g., `score × 10`) is the primary tuning knob. Calibration requires:
- Sampling a representative query set
- Comparing metric scores (NDCG, MRR) across multiplier values
- Balancing vector influence against lexical relevance

## Limitations

- Requires running two queries sequentially (latency cost)
- The candidate pool from Phase 1 must be large enough — if a relevant document is missed by vector search, it can still be found lexically but won't receive the semantic boost
- Multiplier tuning is empirical; no principled derivation

## Related Concepts
- [[Hybrid Search]] — the broader category
- [[Reciprocal Rank Fusion]] — alternative fusion; merges two ranked lists
- [[Relative Score Fusion]] — alternative fusion; normalizes and combines scores
- [[Results Boosting]] — parent technique; Semantic Boosting is a special case
- [[Dense Vector Retrieval]] — Phase 1 signal source
- [[Linear Score Combination]] — another score-combination approach

## Articles
- [[Hybrid Search Blueprint Series Semantic Boosting]] — origin article

## People
- [[Erik Hatcher]] — named and described the technique
