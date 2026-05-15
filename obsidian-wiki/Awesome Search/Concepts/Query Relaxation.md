---
title: "Query Relaxation"
aliases: ["query softening", "constraint relaxation", "facet relaxation"]
tags:
  - concept
  - query-understanding
  - search-quality
  - zero-results
---

# Query Relaxation

Progressively loosening query constraints when a search returns too few (or zero) results, in order to surface *something* useful rather than failing the user entirely. A key recovery strategy for [[Zero Results]] pages.

The goal is to preserve as much user intent as possible while dropping or softening the constraints least likely to be load-bearing.

## Relaxation Strategies

### Term Dropping
Remove the rarest or least-important terms, keeping the core noun phrase last.

```
"blue vintage leather motorcycle jacket size XL"
  → "vintage leather motorcycle jacket"
  → "leather motorcycle jacket"
```

Heuristics for drop order: IDF (rare terms first), adjectives before nouns, modifiers before head noun.

### AND → OR Conversion
Switch from requiring all terms (boolean AND) to any terms (boolean OR), relying on ranking to surface documents matching more terms at the top.

```
must(blue) must(leather) must(jacket)
  → should(blue) should(leather) must(jacket)
```

Minimum-should-match can be stepped down: `3 of 3` → `2 of 3` → `1 of 3`.

### Attribute / Facet Relaxation
For structured e-commerce queries, relax specific filter constraints in order of specificity:
1. Size → any size
2. Exact color (\"navy blue\") → color family (\"blue\") → any color
3. Sub-brand → brand → category

### Semantic Relaxation
Move up the taxonomy hierarchy to broaden scope:

```
"Nike Air Max 2024"  →  "Nike running shoes"  →  "running shoes"
```

Requires a product taxonomy or knowledge graph. Related to [[Semantic Search]] and [[Query Understanding]].

### Scope Expansion
Widen the catalog scope: scoped search (one department) → site-wide search → related catalog.

## Implementation Patterns

**Waterfall / Try-cascade**
Execute progressively relaxed queries until results appear. Most common pattern; adds latency (multiple round-trips).

```
query_1 = original
if hits == 0: query_2 = drop_one_term(query_1)
if hits == 0: query_3 = and_to_or(query_2)
...
```

**Parallel execution**
Issue the relaxed query in parallel with the original, keep results in reserve. No latency cost; wasteful if original query succeeds often.

**ML-predicted relaxation order**
Train a model on historical zero-result queries to predict which relaxation step will succeed. Skips unnecessary waterfall steps.

## UX: Communicating Relaxation

Don't silently substitute — users notice and lose trust.

- ✅ "No exact results. Showing results for **leather motorcycle jacket**"
- ✅ "We removed 'size XL' — showing all sizes. Filter to narrow down."
- ❌ Silently returning unrelated popular items
- ❌ Showing empty page with no guidance

## Key Tradeoffs

| Too conservative | Too aggressive |
|---|---|
| Empty result page | Irrelevant results |
| User abandons | User loses trust in relevance |

The right balance depends on query type: tail navigational queries need exact matches; broad exploratory queries tolerate more relaxation.

## Relation to Query Rewriting

Query relaxation is one class of **query rewriting** — transformations applied before retrieval to improve result coverage. Other rewrites include [[Synonyms|synonym expansion]], spelling correction, and query segmentation. Relaxation is specifically triggered by *insufficient* results rather than applied universally.

## Related Concepts
- [[Zero Results]] — primary trigger for relaxation
- [[Query Understanding]] — relaxation is part of the rewriting phase
- [[Faceted Search]] — attribute/facet relaxation
- [[Spelling Correction]] — parallel zero-result recovery strategy
- [[Synonyms]] — vocabulary-mismatch recovery (complement to relaxation)
- [[Semantic Search]] — semantic relaxation via taxonomy/embeddings

- [[Query Specificity]] — over-specific queries are the primary trigger for relaxation

## Articles
- [[Query Understanding - Query Relaxation]] — [[Daniel Tunkelang]]; term dropping, AND→OR, attribute & semantic relaxation strategies

## People
- [[Daniel Tunkelang]] — query relaxation as part of the Query Understanding series
