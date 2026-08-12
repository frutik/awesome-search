---
type: concept
title: "Query Types"
aliases: ["search query types", "e-commerce query types", "query type taxonomy"]
tags:
  - concept
  - query-understanding
  - e-commerce-search
created: 2026-05-16
---

# Query Types

## Definition

Query types are taxonomies that classify search queries by their structural characteristics, vocabulary, and user behavior patterns — distinct from [[Search Intent]] (which focuses on goal) but related.

## Baymard's 8 E-commerce Query Types

Baymard Institute's taxonomy for e-commerce search, derived from large-scale usability testing. The percentage is the share of benchmarked sites that fail to support that type — see [[Ecommerce Search UX - 8 Query Types]].

| Type | Example | Sites with issues | Challenge |
|------|---------|---|-----------|
| **Exact** | "Nikon D800" | 12% | Match a specific model or SKU exactly |
| **Product Type** | "chairs" | 20% | Broad type; behaves like a category page request |
| **Feature** | "wireless noise cancelling headphones" | 39% | Attribute matching against structured data |
| **Use Case** | "running shoes for marathons" | 43% | Activity implies attributes never stated |
| **Abbreviation and Symbol** | "13in laptop", "tv w/ hdmi" | 54% | Tokenisation and normalisation of symbols and shorthand |
| **Compatibility** | "case for MacBook Air M2" | 44% | Structured relation between two products |
| **Symptom** | "my back hurts pillow" | 37% | Infer product category from a described problem |
| **Non-Product** | "return policy" | 66% | Service content, not products |

The ranking is the finding: the types sites handle worst are the ones furthest from the catalog's own vocabulary. Only "chairs" is an example drawn from the source; the rest are illustrative.

## Other Common Type Labels

Widely used in practice but **not** part of Baymard's taxonomy — worth keeping distinct when citing sources:

| Type | Example | Note |
|------|---------|------|
| **Category** | "cameras" | Overlaps Baymard's "Product Type" |
| **Branded** | "Nike shoes" | Filter + rank within brand |
| **Thematic** | "birthday gift for photographer" | Discovery; benefits from semantic retrieval |
| **Comparative** | "mirrorless vs DSLR" | Educational content, not a product listing |

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

- [[Query Classification]] — assigning queries to these types in production
- [[Search Intent]] — goal-based classification (overlaps)
- [[Query Understanding]] — broader processing framework
- [[Judgment Lists]] — query type used in sampling strategy
- [[Diversity Metrics]] — exploratory/thematic queries need diversity
- [[Asymmetric Semantic Search]] — long queries benefit from asymmetric models

- [[Query Specificity]] — the degree of constraint in a query; head ↔ tail correlates with low ↔ high specificity

## People

- [[Daniel Tunkelang]] — query type taxonomy; query understanding framework
