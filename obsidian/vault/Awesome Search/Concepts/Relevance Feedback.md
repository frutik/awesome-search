---
title: "Relevance Feedback"
aliases: ["PRF", "pseudo-relevance feedback", "implicit feedback", "explicit feedback"]
tags:
  - concept
  - search-evaluation
  - query-understanding
---

# Relevance Feedback

## Definition

Using signals about which results are relevant (or not) to iteratively refine a search query and improve subsequent retrieval. Bridges the gap between a user's initial query and their actual [[Search Intent]].

## Three Types

### Explicit Feedback
User directly marks results as relevant or irrelevant (thumbs up/down, "More like this"). Highest quality signal — but rare in practice because users don't want to do extra work.

### Pseudo-Relevance Feedback (PRF)
Assume the top-k results are relevant. Extract key terms from those documents, expand the query, and re-execute. Fully automated — no user interaction needed. Risk: drifts badly if the initial top-k is poor.

### Implicit Feedback
Infer relevance from user behaviour:
- Clicks → positive signal
- Long dwell time → likely relevant
- Immediate back-navigation → likely not relevant
- Conversion / purchase → strong positive signal

Cheap and abundant, but noisy — corrupted by [[Position Bias]] and [[Presentation Bias]].

## Rocchio Algorithm

Classic vector-space implementation of explicit feedback:

```
new_query = α × original_query + β × avg(relevant_docs) − γ × avg(non_relevant_docs)
```

Moves the query vector toward relevant documents and away from non-relevant ones.

## Modern Implementations

- **"More like this"** — Elasticsearch `more_like_this` query uses document terms as expansion
- **Session-level feedback** — clicks earlier in a session inform later query refinements
- **LLM-based query rewriting** — use clicked documents to rewrite query with an LLM
- **Contrastive feedback** — train embedding models on (query, clicked, skipped) triples

## Challenges

- Explicit feedback rarely occurs
- Implicit signals are noisy — [[Position Bias]] means top results get more clicks regardless of quality
- [[Presentation Bias]]: can only learn from results that were shown

## Related Concepts

- [[Click Signals]] — primary source of implicit feedback
- [[Position Bias]] — corrupts click-based relevance signals
- [[Presentation Bias]] — results not shown can't generate feedback
- [[Query Understanding]] — relevance feedback as a query refinement mechanism
- [[Session-Based Evaluation]] — session context shapes feedback
- [[Learning to Rank]] — implicit feedback used as LTR training signal

## Articles

- [[Query Understanding - Relevance Feedback]] — [[Daniel Tunkelang]]; explicit, pseudo, and implicit types
- [[What AI Engineers Should Know about Search]] — [[Doug Turnbull]]; relevance feedback as query feedback (point 55)

## People

- [[Daniel Tunkelang]] — queryunderstanding.com series
