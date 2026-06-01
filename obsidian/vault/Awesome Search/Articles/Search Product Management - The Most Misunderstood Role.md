---
title: "Search Product Management: The Most Misunderstood Role"
aliases: ["Search PM Role", "Rubinstein Search PM"]
tags:
  - clippings
  - search
  - product-management
  - search-architecture
  - medium
source: "https://medium.com/@JamesRubinstein/search-product-management-the-most-misunderstood-role-b2e7f4c9d1a3"
author: "James Rubinstein"
created: 2026-05-15
concepts:
  - Search Architecture
  - Search Evaluation
  - A-B Testing for Search
---

# Search Product Management: The Most Misunderstood Role

**Source:** https://medium.com/@JamesRubinstein/search-product-management-the-most-misunderstood-role-b2e7f4c9d1a3
**Author:** [[James Rubinstein]]

## Summary

Search is uniquely difficult to manage as a product because it touches every part of the stack — and PMs who don't understand the technical internals make consistently bad decisions. Rubinstein argues that search PM is the most misunderstood PM role in tech.

### Why Search PM Is Different

Most PM roles involve feature decisions: what to build, when, for whom. Search PM involves:
- **System decisions**: indexing strategy, query rewriting, ranking model architecture
- **Measurement decisions**: what metrics to track, how to run experiments
- **Trade-off decisions**: relevance vs. latency vs. coverage vs. freshness

These require technical depth that typical PM training doesn't provide.

### What Search PMs Must Understand

**Indexing**: How documents are parsed, tokenized, and stored. Why freshness matters. How schema changes ripple through ranking.

**Query Understanding**: How queries are parsed, normalized, expanded. Why "kids shoes" and "children's shoes" should return similar results.

**Query Rewrites**: Spelling correction, synonym expansion, query relaxation. Each rewrite is an editorial decision with quality implications.

**Ranking**: What features are used. How the model was trained. What it's optimizing for. Why changing one signal can break others.

**Metrics**: What NDCG means. Why CTR can be misleading. How to design A/B tests for search that control for query mix.

### "Everything in Search Is an Experiment"
Rubinstein's core thesis: **you can't reason about search changes in the abstract**. Every change to indexing, query parsing, or ranking must be measured — because search is too complex for intuition alone.

This has org implications:
- Experimentation infrastructure is table stakes
- PMs must be comfortable interpreting statistical results
- "It feels better" is not a ship criterion

### Common Search PM Failure Modes
1. **Feature thinking** — "let's add a filter" without understanding impact on result quality
2. **Metric blindness** — optimizing a proxy metric that diverges from user value
3. **Big-bang rewrites** — replacing ranking models without staged rollout
4. **Ignoring tail queries** — optimizing head queries while long tail degrades

## Key Concepts
- **Search PM depth** — technical understanding required beyond typical PM skills
- **Everything is an experiment** — no search change ships without measurement
- **Query rewrites as editorial decisions** — each rewrite has quality implications
- **Tail queries** — long-tail query quality often neglected

## Related Concepts
- [[Search Architecture]]
- [[Search Evaluation]]
- [[A-B Testing for Search]]
- [[Query Understanding]]
- [[Learning to Rank]]

## Related Articles
- [[Thoughts about Managing Search Teams]]
- [[Setting Up a Relevance Evaluation Program]]
- [[Statistical and Human-Centered Approaches to Search Improvement]]

## People
- [[James Rubinstein]]
- [[Daniel Tunkelang]]
