---
type: concept
title: Diversity Metrics
aliases:
  - result diversity
  - results diversity
  - search diversity
  - MMR
  - maximal marginal relevance
  - diversification
tags:
  - concept
  - search-evaluation
  - diversity
  - ranking
created: 2026-05-16
---

# Diversity Metrics

## Definition

Diversity metrics measure how well a search result set covers different aspects, subtopics, or perspectives of a query — rewarding systems that don't just return the best individual results but also ensure variety.

## Why Diversity Matters

For ambiguous queries (e.g., "jaguar"), a diverse result set:
- Shows documents about the car, the animal, and the sports team
- Serves different user intents simultaneously
- Reduces the need for reformulation

For broad queries (e.g., "python programming"), diversity ensures:
- Beginner and advanced resources
- Different Python frameworks
- Different content types (tutorials, docs, videos)

## Key Diversity Metrics

### MMR (Maximal Marginal Relevance)
The most common diversity-aware ranking algorithm:
```
MMR = argmax_d [ λ × sim(d, q) - (1-λ) × max_d'∈S sim(d, d') ]
```
Where:
- `sim(d, q)` = relevance to query (maximize relevance)
- `max_d'∈S sim(d, d')` = similarity to already-selected docs (minimize redundancy)
- `λ` = relevance vs. diversity tradeoff (0=diversity only, 1=relevance only)

Greedy algorithm: at each step, select the document maximizing MMR.

### α-NDCG
Extension of [[NDCG]] that discounts a document if its subtopics are already covered by higher-ranked documents.

### ERR (Expected Reciprocal Rank)
Models user as "cascade" — probability of being satisfied at each rank depends on previous ranks. Naturally incorporates some diversity by modeling saturation.

### Average Pairwise Distance (APD)
Mean embedding distance between all pairs in the result set:
```
APD = (2 / (n(n-1))) × Σᵢ<ⱼ dist(emb_i, emb_j)
```
Higher APD = more diverse set.

### Entropy-Based Diversity
Treat result set as a distribution over topics/categories:
- High entropy = many topics covered equally
- Low entropy = one topic dominates

### Positive Cluster Coverage (C)

Introduced in [[Uncovering the Bigger Picture - Comprehensive Event Understanding via Diverse News Retrieval|NEWSCOPE]]. Cluster the sentences of the *relevant* documents into semantic aspects, then measure what fraction of those aspects the top-k results actually surface:

```
C = # covered clusters / # total clusters in relevant documents
```

Fine-grained semantic recall. Unlike APD it is coverage-denominated, so it gives no credit for redundancy and none for spreading results apart in embedding space without adding aspects. The cost is that it needs an aspect inventory — something has to define what *ought* to be covered.

### Information Density Ratio (I)

Also from NEWSCOPE. Covered aspects per sentence returned:

```
I = # covered clusters / # total sentences in retrieved documents
```

An efficiency measure rather than a spread measure: it penalizes padding and repetition *inside* the results, favoring concise, information-rich passages. Useful wherever result length is a cost — RAG context windows especially.

## Diversity in Practice

### E-commerce
Diversity means different brands, price ranges, styles:
- Don't show all Nike shoes for "running shoes"
- Include budget and premium options

### News Search
Diversity = different perspectives on same event:
- Multiple sources
- Opposing viewpoints

### Enterprise Knowledge
Diversity = different document types, authors, departments.

## Diversity-Relevance Tradeoff

MMR's λ parameter controls the tradeoff:
- λ = 1: pure relevance ranking (standard NDCG optimization)
- λ = 0: pure diversity (maximum spread)
- λ = 0.5: balanced (typical default)

Optimal λ depends on query type: navigational queries need less diversity; exploratory queries need more.

## Related Concepts

- [[NDCG]] — standard metric diversity metrics extend
- [[MRR]] — no diversity component
- [[Search Evaluation]] — diversity as quality dimension
- [[Query Understanding]] — query intent determines diversity need
- [[Semantic Search]] — embedding-based diversity measurement

## People

- [[Daniel Tunkelang]] — diversity for broad/ambiguous queries
- [[Yixuan Tang]] · [[Yiqun Sun]] — Positive Cluster Coverage and Information Density Ratio

## Articles

- [[Searching for Goldilocks]]
- [[Thoughts on Search Result Diversity]]
- [[Uncovering the Bigger Picture - Comprehensive Event Understanding via Diverse News Retrieval]] — sentence-level diversity modeling; source of Positive Cluster Coverage and Information Density Ratio

## Related Datasets

- [[LocalNews]] · [[DSGlobal]] — benchmarks built to measure aspect coverage rather than embedding spread
