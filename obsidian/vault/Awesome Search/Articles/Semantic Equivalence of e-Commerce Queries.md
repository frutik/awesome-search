---
title: "Semantic Equivalence of e-Commerce Queries"
aliases: ["Query Semantic Equivalence", "Tunkelang KDD 2023"]
tags:
  - clippings
  - search
  - query-understanding
  - embeddings
source: "https://queryunderstanding.com/semantic-equivalence-of-e-commerce-queries-8f3c2b1a9e4d"
author: "Daniel Tunkelang"
created: 2026-05-15
concepts:
  - Query Understanding
  - Asymmetric Semantic Search
  - Embedding Fine-tuning
---

# Semantic Equivalence of e-Commerce Queries

**Source:** https://queryunderstanding.com/semantic-equivalence-of-e-commerce-queries-8f3c2b1a9e4d
**Author:** [[Daniel Tunkelang]]

## Summary

How do you determine that two e-commerce queries are semantically equivalent? This is foundational for query clustering, synonym detection, and cache reuse. Presented work related to KDD 2023.

### Problem Definition
Two queries Q1 and Q2 are semantically equivalent if they express the same shopping intent — i.e., a user would be equally satisfied by the result sets for either query.

This differs from lexical similarity ("laptop" vs "laptops") and general semantic similarity ("big TV" vs "large television").

### Approach 1: Behavioral Aggregation
Queries that produce similar click distributions are semantically equivalent:
- Aggregate clicks by (query → item) pairs
- Represent each query as a weighted vector over clicked items
- Compute cosine similarity between query vectors
- **Advantage**: grounded in actual user behavior
- **Challenge**: data sparsity for rare queries

### Approach 2: Sentence Transformers
Fine-tune a bi-encoder on pairs of (equivalent, non-equivalent) queries:
- Training signal: human-labeled pairs, or weak labels from behavioral similarity
- At inference: embed both queries, compare cosine similarity
- **Advantage**: generalizes to unseen queries
- **Challenge**: requires training data; may hallucinate equivalences

### Hybrid Approach
Use behavioral similarity as weak supervision to train the sentence transformer:
1. Compute behavioral similarity for high-traffic query pairs
2. Label pairs above threshold as equivalent
3. Fine-tune sentence transformer on these labels
4. Apply transformer to low-traffic queries

### Applications
- **Query clustering**: group equivalent queries for aggregate analytics
- **Synonym expansion**: rewrite rare queries to equivalent high-traffic forms
- **Cache reuse**: serve cached results for semantically equivalent queries
- **A/B test bucketing**: bucket equivalent queries together for cleaner experiments

## Key Concepts
- **Behavioral equivalence** — click-distribution similarity as proxy for semantic equivalence
- **Sentence transformers** — bi-encoder fine-tuned on query pairs
- **Weak supervision** — using behavioral signal to generate training labels
- **Query clustering** — grouping equivalent queries

## Related Concepts
- [[Query Understanding]]
- [[Asymmetric Semantic Search]]
- [[Embedding Fine-tuning]]
- [[Synonyms]]
- [[Personalization]]

## Related Articles
- [[Affordances for Conversational Search]]
- [[Autosuggest Ranking]]

## People
- [[Daniel Tunkelang]]
