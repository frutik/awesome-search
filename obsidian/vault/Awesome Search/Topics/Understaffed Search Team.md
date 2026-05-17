---
type: topic
aliases:
  - understaffed search
  - small search team
  - lean search team
  - resource-constrained search
tags:
  - topic
  - search-team
  - strategy
  - search-relevance
  - process
related_concepts:
  - "[[Signal Downboosting]]"
  - "[[Search Evaluation]]"
  - "[[Judgment Lists]]"
  - "[[Results Boosting]]"
  - "[[Relevance Feedback]]"
  - "[[Collocations]]"
  - "[[Query Relaxation]]"
  - "[[Reciprocal Rank Fusion]]"
  - "[[BM25]]"
  - "[[Synonyms]]"
related_topics:
  - "[[Managing a Search Team]]"
  - "[[Relevance Program Setup]]"
  - "[[Search Quality Assurance]]"
  - "[[A-B Testing for Search]]"
articles:
  - "[[Getting Started on Search Relevance for the Understaffed Search Team]]"
  - "[[Search Relevance for Understaffed Teams]]"
people:
  - "[[Doug Turnbull]]"
created: 2026-05-17
---

# Understaffed Search Team

How to improve search relevance under resource constraints — when leadership says "improve search" but won't give you more people or time to do it.

---

## The Core Problem

Understaffed search teams face a compounding challenge: search quality requires expertise across engineering, ML, product, and domain knowledge, but small teams can rarely cover all four. The result is either shallow coverage everywhere or deep expertise in one area with blind spots elsewhere.

Doug Turnbull's framing: resource constraints are a forcing function for strategic clarity. They force you to focus on **NOW** — high-ROI work that ships quickly — rather than elaborate long-term infrastructure projects.

## Strategy: Ship in Your Competence Areas

The most dangerous trap for an understaffed team is promising big and delivering nothing. Two statistics matter equally: **speed of delivery** and **magnitude of improvement**. Iterate confidently in small steps rather than betting on a long-horizon project.

### Prioritization Heuristics

1. **Head queries first** — the top 1000 queries often account for 50%+ of traffic; fixing these has outsized impact
2. **Zero results are low-hanging fruit** — straightforward to detect, measure, and fix
3. **Evaluation before experimentation** — build a minimal [[Judgment Lists|judgment set]] before building models; otherwise you can't tell if you're improving
4. **Rules before ML** — deterministic fixes (synonyms, boosts, query rewriting rules) are faster to ship and easier to audit than learned models on sparse data

## High-ROI Early Experiments

Techniques that consistently perform across projects and don't require large teams:

| Technique | Concept | Why it works for small teams |
|-----------|---------|------------------------------|
| Popularity boosting | [[Results Boosting]] | No training data required; signals usually already available |
| [[Signal Downboosting]] | [[Position Bias]] | Improves precision + diversity without training loop |
| Relevance feedback (Rocchio) | [[Relevance Feedback]] | Learns from existing click logs; no annotation required |
| Vector search | [[Dense Vector Retrieval]] | Pre-trained open-source models available; high recall lift |
| [[Reciprocal Rank Fusion]] | [[Hybrid Search]] | Combines existing rankers without a new model |
| Manual overrides | [[Synonyms]], [[Querqy]] | Fast patches for embarrassing or high-visibility failures |
| [[Collocations]] | [[Query Understanding]] | Simple statistical approach; no knowledge graph needed |
| [[Query Relaxation]] | [[Zero Results]] | Directly addresses zero-result queries |

## Infrastructure Philosophy: The Giant UNDO Button

Small teams can't afford to be blocked by index corruption or bad config. Build resilience into the stack:
- **Disposable indices** — delete and reindex without drama
- **Multiple index versions** — collection aliases in Solr/Elasticsearch enable instant rollback
- **Seamless re-indexing** — streaming (Flink, Beam) enables continuous updates without batch windows

## Blazing New Paths to Production

New infra paths (new indexing system, new search API) are as much an organizational challenge as a technical one. Tips:
- Share credit with infrastructure/SRE teams
- Show a prototype, don't write design docs
- Get into production fast — even a small traffic slice or feature flag wears the path and builds trust
- Present stakeholder options with natural consequences, not mandates

## Evaluation Strategy for Small Teams

A minimal but effective evaluation stack:
1. **A small judgment set** (~200–500 queries with relevance grades) — gives you NDCG/MAP offline
2. **Bad query exploration** — systematically review worst-performing queries; more actionable than aggregate metrics
3. **Zero-result monitoring** — dashboarded and alerting
4. **A/B framework** — even a basic split experiment protects against shipping regressions

For teams that can't run A/B tests yet: use interleaving experiments as a lighter-weight alternative.

---

## Related Concepts
- [[Signal Downboosting]]
- [[Search Evaluation]]
- [[Judgment Lists]]
- [[Results Boosting]]
- [[Relevance Feedback]]
- [[Collocations]]
- [[Query Relaxation]]
- [[Reciprocal Rank Fusion]]
- [[BM25]]
- [[Synonyms]]
- [[Position Bias]]
- [[Dense Vector Retrieval]]

## Related Topics
- [[Managing a Search Team]] — broader team org and leadership
- [[Relevance Program Setup]] — how to set up a relevance evaluation program
- [[Search Quality Assurance]] — evaluation methodology
- [[A-B Testing for Search]] — experimentation for small teams

## Articles
- [[Getting Started on Search Relevance for the Understaffed Search Team]] — comprehensive strategy guide (Google Doc)
- [[Search Relevance for Understaffed Teams]] — Turnbull blog post summary
- [[Query Triage - The Secret Weapon for Search Relevance]] — bad query exploration methodology
- [[What Is a Judgment List]] — evaluation foundation for small teams
- [[Ecommerce Search Governance - Move Faster Not Slower]] — governance at speed

## People
- [[Doug Turnbull]] — primary voice on this topic
