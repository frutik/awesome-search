---
title: Getting Started on Search Relevance for the Understaffed Search Team
type: article
source: https://docs.google.com/document/d/1MVNnx-6WTbpZurlwLakAEvTfDuNTshM3hY83G7qMjJg/edit?tab=t.0
author: "[[Doug Turnbull]]"
published: null
created: 2026-05-17
tags:
  - search
  - search-team
  - relevance
  - strategy
  - process
concepts:
  - Signal Downboosting
  - Relevance Feedback
  - Collocations
  - Query Relaxation
  - Reciprocal Rank Fusion
  - NDCG
  - BM25
  - Presentation Bias
  - Embedding-based Retrieval
topics:
  - Managing a Search Team
  - Relevance Program Setup
  - Search Quality Assurance
  - Understaffed Search Team
---

# Getting Started on Search Relevance for the Understaffed Search Team

A comprehensive strategy guide by [[Doug Turnbull]] for search teams tasked with improving relevance without additional resources. Maintained as a living document via Google Docs with community practitioner input.

---

## Summary

Resource-constrained search teams face a paradox: they must deliver improvements without headcount growth. This guide reframes that constraint as a forcing function for strategic clarity — it forces focus on high-ROI work and quick iteration over elaborate long-term infrastructure projects.

## Getting Oriented

Before optimizing anything, align with stakeholders on the definition of success. Different stakeholders may define "better search" as conversion lift, user satisfaction, reduced zero-result rate, or latency improvement. Misalignment here leads to work that impresses no one.

## Evaluation Strategy

### Optimize Ranking Stats (NDCG, Judgments)

Build [[Judgment Lists]] and track [[NDCG]] as your compass. Use [[Search Evaluation]] harnesses to detect regressions.

See: [NDCG is overrated](https://softwaredoug.com/blog/2023/05/06/ndcg-is-overrated.html) — Doug's argument that NDCG is a proxy, not a goal.

### Optimize for Bad Query Exploration

Track the worst-performing queries explicitly. Bad query exploration — systematically studying which queries fail and why — is a more actionable feedback loop than aggregate metrics. See also: [[Query Triage - The Secret Weapon for Search Relevance]].

## Early Search Experiments (Consistently High Performers)

### Boost Generally Popular Results

Global popularity signals (sales rank, conversion rate in search) correlate with relevance for many queries. Start simple and iterate. See [[Results Boosting]].

### Explicitly Downboost Poor Performers

Rather than signal boosting (which amplifies [[Position Bias]]), prefer **[[Signal Downboosting]]**: identify items with high impressions but statistically poor performance per query, and push them toward the bottom. This improves precision, increases diversity, and overcomes presentation bias without locking in a local optimum.

Reference: [What is Presentation Bias in Search](https://softwaredoug.com/blog/2022/07/16/what-is-presentation-bias-in-search.html)

### Use Relevance Feedback Techniques

[[Relevance Feedback]] (Rocchio and similar approaches) learns from what users click/convert for a query. If users searching "shoes" consistently click "footwear" category items, boost that category association. Any document property can be associated with a query by observing query→relevant document relationships.

See: [Rocchio algorithm](https://en.m.wikipedia.org/wiki/Rocchio_algorithm)

### Invest in Embedding-Based Retrieval (Vector Search)

Embedding-based retrieval (text, image, multimodal) provides recall improvements that keyword search cannot. Open-source models make this accessible. Combine with Rocchio-type approaches to build accurate query embeddings for short queries.

References:
- [Vector search for the uninitiated](https://softwaredoug.com/blog/2023/02/13/why-vector-search.html)
- [[Sease]] has training on vector-based retrieval (http://sease.io)

See also: [[Dense Vector Retrieval]], [[Embeddings]]

### Interleaving and Rank Fusion

[[Reciprocal Rank Fusion]] combines multiple rankers by summing 1/rank from each underlying ranker. This is essential for combining vector search with traditional retrieval. Interleaving is also an effective [[A/B Testing for Search]] strategy.

Reference: [A/B Testing Search: Thinking Like a Scientist](https://jamesrubinstein.medium.com/a-b-testing-search-thinking-like-a-scientist-1cc34b88392e) — [[James Rubinstein]]

### Manual Overrides: Rules, Synonyms, Boosts

Hand-managed recommendations and [[Synonyms]] can outperform algorithmic results for specific queries. Rules are crucial for patching embarrassing or legally questionable results. Use sparingly — rules go stale.

Tool: **[[Querqy]]** (https://querqy.org/) — system for managing query rewriting rules.

### BM25 Text Matching Hacks

For keyword-based retrieval, optimize for [[BM25]]'s expectations:
- BM25 works best with article-length text (not book-length or snippets). Chunk accordingly.
- **Proximity matters**: phrase queries with slop score terms that appear closer together higher.
- **Position matters**: terms appearing earlier in text should score higher.

### Query Understanding: Collocations and Compounds

Simple query understanding without building knowledge graphs:
- **[[Collocations]]**: recognize statistically co-occurring terms as single units ("Palo Alto", "Mazda Miata"). Use phrase search on identified collocations.
- **Compound words**: detect common compounded/decompounded pairs (backpack / back pack).

Reference: [The Unreasonable Effectiveness of Collocations](https://opensourceconnections.com/blog/2019/05/16/unreasonable-effectiveness-of-collocations/)

### Mine Query Refinements for Corrections

How users correct their queries within a session reveals common misspellings and confusions. Short-circuit common corrections to offer them automatically. See [[Spelling Correction]].

### Relax the Query to Increase Recall

Zero results? Retry with a relaxed query: AND→OR, fuzzy matching, vector retrieval interleaving, or [strategic term dropping](https://www.youtube.com/watch?v=FQsX3H3I6fM). See [[Query Relaxation]].

### Communicate Relevance in the UI

Users report poor relevance when the UI doesn't demonstrate *why* a result is relevant. Highlighting, relevant snippets, and key attribute display all help.

Reference: [Introduction to Search Quality](https://opensourceconnections.com/blog/2018/11/19/an-introduction-to-search-quality/)

## Infrastructure Considerations

### Make Re-indexing Seamless

Streaming systems (Flink, Beam) enable both real-time updates and historical batch re-indexing. Treat re-indexing as a routine operation, not a project.

### Multiple Index Versions in Production

Maintain rollback capability via index aliases:
- Solr: [collection aliases](https://solr.apache.org/guide/8_2/collection-aliasing.html)
- Elasticsearch: [index aliases](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-aliases.html)

### Make Search Indices Disposable

A strange index should be deletable and rebuildable, not a crisis. The "giant UNDO button" philosophy.

## Strategy: Ship in Your Competence Areas, Build Deeper Leverage

### The Most Important Thing

Ship improvements fast. The quickest way to get a project cancelled is to promise without delivery. Two statistics matter: speed of delivery AND magnitude of improvement. Iterate confidently.

### Blazing New Paths to Production

New infrastructure paths (a new indexing system, a new search API) require building organizational muscle and stakeholder trust — not just technical work. Treat each new production path as a political and social project as much as a technical one.

Tips for blazing new paths:
- **Make partner teams part of the solution** — share credit with infrastructure teams
- **Show, don't tell** — prototype over design documents
- **Find a way to ship ASAP** — behind a feature flag, on a side surface, with a small traffic percentage
- **Discuss options and natural consequences** — present stakeholders with choices, not mandates

## Tools and Community Resources

- **Awesome Search** repo: https://github.com/frutik/awesome-search
- **[[Querqy]]** — query rewriting rules (https://querqy.org/)
- **[[Sease]]** — vector search training (http://sease.io)

---

## Related Concepts
- [[Signal Downboosting]]
- [[Position Bias]]
- [[Relevance Feedback]]
- [[Collocations]]
- [[Query Relaxation]]
- [[Reciprocal Rank Fusion]]
- [[BM25]]
- [[NDCG]]
- [[Results Boosting]]
- [[Synonyms]]
- [[Spelling Correction]]
- [[Dense Vector Retrieval]]
- [[A/B Testing for Search]]
- [[Search Evaluation]]
- [[Judgment Lists]]

## Related Articles
- [[Search Relevance for Understaffed Teams]]
- [[What is Presentation Bias in Search]]
- [[Bayesian BM25 is Cool]]
- [[Query Triage - The Secret Weapon for Search Relevance]]
- [[A-B Testing Search Thinking Like a Scientist]]
- [[Real Talk About Synonyms and Search]]
- [[Query Understanding - Query Relaxation]]
- [[Query Understanding - Relevance Feedback]]

## People
- [[Doug Turnbull]]
- [[James Rubinstein]]

## Companies
- [[OpenSource Connections]]
- [[Sease]]
