---
type: person
name: Sergey Feldman
affiliation: Allen Institute for AI (AI2)
role: Senior Applied Research Scientist
tags: [person, learning-to-rank, academic-search, evaluation]
created: 2026-05-16
---

# Sergey Feldman

Senior Applied Research Scientist at **Allen Institute for AI (AI2)**. Built the ML reranker for Semantic Scholar — a 190M-paper academic search engine — taking evaluation score from 0.7 to 0.93 and delivering +8% clicks per query.

## Articles

- [[Building a Better Search Engine for Semantic Scholar]] — LightGBM reranker on Elasticsearch, data filtering as key lever

## Key Contributions

- **Training data filtering**: removing ~1/3 of training data via "sensibility checks" yielded 10-15% evaluation improvement — data quality > data quantity
- **Custom evaluation metric**: 250-query manually-annotated benchmark with component-level criteria; more predictive than generic NDCG
- **Rules + ML**: post-hoc rule corrections (exact year/phrase boosts) on top of learned model
- **Result**: 0.7 → 0.93 custom metric, +8% clicks per query, +9% MRR

## Related

- [[Semantic Scholar]] (AI2) · [[Learning to Rank]] · [[Judgment Lists]] · [[NDCG]]
