---
title: "Query Types"
aliases: ["search query types", "query classification", "e-commerce query types"]
tags:
  - concept
  - query-understanding
  - e-commerce-search
---

# Query Types

## Definition

Query types are taxonomies that classify search queries by their structural characteristics, vocabulary, and user behavior patterns — distinct from [[Search Intent]] (which focuses on goal) but related.

## Baymard's 8 E-commerce Query Types

Baymard Institute's taxonomy for e-commerce search (widely referenced):

| Type | Example | Challenge |
|------|---------|-----------|
| **Exact product match** | "Nikon D800" | Match by SKU/model number exactly |
| **Category** | "cameras" | Return best in category, not just best-selling |
| **Non-product** | "return policy" | Service content, not products |
| **Symptom** | "blurry photos" | Infer product from problem |
| **Compatibility** | "lens for D800" | Structured matching required |
| **Comparative** | "mirrorless vs DSLR" | Educational content |
| **Thematic** | "birthday gift for photographer" | Discovery + semantic search |
| **Branded** | "Nike shoes" | Filter + rank within brand |

## Academic Query Type Taxonomies

### Factoid vs. Non-Factoid
- **Factoid**: has a short, definitive answer ("When was Napoleon born?")
- **Non-factoid**: requires explanation, opinion, or multiple facts

### Keyword vs. Natural Language
- **Keyword**: "iphone 15 review 2024"
- **Natural language**: "What do people think of the iPhone 15?"

### Head vs. Torso vs. Tail
Based on query frequency:
- **Head** (>1000 daily): "shoes" — simple, broad, easy to optimize
- **Torso** (10–1000): "running shoes women" — specific, addressable
- **Tail** (<10): "waterproof trail running shoes wide toe box women" — rare, hard to optimize individually

## Query Length and Complexity

| Length | Characteristics | Best Handled By |
|--------|----------------|-----------------|
| 1 word | Ambiguous, broad | Diversification + personalization |
| 2–3 words | Most common | Standard hybrid retrieval |
| 4–6 words | Specific | Semantic search excels |
| 7+ words | Conversational/complex | [[Asymmetric Semantic Search]], [[RAG]] |

## Query Type in Search Sampling

When building [[Judgment Lists]], stratified sampling by query type ensures evaluation covers all types proportionally rather than being dominated by head queries.

## Related Concepts

- [[Search Intent]] — goal-based classification (overlaps)
- [[Query Understanding]] — broader processing framework
- [[Judgment Lists]] — query type used in sampling strategy
- [[Diversity Metrics]] — exploratory/thematic queries need diversity
- [[Asymmetric Semantic Search]] — long queries benefit from asymmetric models

- [[Query Specificity]] — the degree of constraint in a query; head ↔ tail correlates with low ↔ high specificity

## People

- [[Daniel Tunkelang]] — query type taxonomy; query understanding framework
