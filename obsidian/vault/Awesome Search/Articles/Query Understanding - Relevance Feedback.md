---
type: article
title: "Relevance Feedback"
source: "https://queryunderstanding.com/relevance-feedback-c6999529b92c"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
concepts:
  - "[[Relevance Feedback]]"
  - "[[Query Understanding]]"
  - "[[Click Signals]]"
  - "[[Session-Based Evaluation]]"
  - "[[Position Bias]]"
topics:
  - "[[Query Understanding in Practice]]"
  - "[[Search Quality Assurance]]"
tags:
  - article
  - query-understanding
  - relevance-feedback
  - search-evaluation
---

# Relevance Feedback

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Relevance feedback uses signals from users about which results are relevant (or not) to refine the search query and retrieve better results. It's a mechanism for iterative search refinement.

## Types of Relevance Feedback

**Explicit feedback**
- User marks results as relevant / not relevant
- Thumbs up / down ratings, "More like this" buttons
- Rare in practice — users don't want to provide explicit feedback

**Pseudo-relevance feedback (PRF)**
- Assume top-k results are relevant
- Extract key terms from those results, add to query and re-execute
- No user interaction needed; can drift if initial results are poor

**Implicit feedback**
- Clicks as positive signals; long dwell time → relevance
- Immediate back-navigation → not relevant
- Conversions (purchases) as strong positive signals
- See [[Click Signals]] and [[Session-Based Evaluation]]

## Rocchio Algorithm

Classic explicit feedback algorithm (vector-space model):

```
new_query = α × original_query + β × avg(relevant_docs) − γ × avg(non_relevant_docs)
```

Moves the query vector toward relevant documents and away from non-relevant ones.

## Modern Applications

- **"More like this"** — Elasticsearch `more_like_this` query
- **"Find similar"** — visual similarity in image search
- **Session refinement** — implicit feedback from click patterns
- **LLM-based rewriting** — use clicked documents to rewrite query via LLM

## Challenges

- Explicit feedback is rarely given by users
- Implicit signals are noisy (clicks ≠ relevance) — see [[Position Bias]]
- Feature/item discovery problem: can't improve if user never sees relevant items ([[Presentation Bias]])

## Related Concepts

- [[Relevance Feedback]] — concept note
- [[Query Understanding]] — series context
- [[Click Signals]] — source of implicit feedback
- [[Session-Based Evaluation]] — session context shapes relevance signals
- [[Position Bias]] — implicit feedback is corrupted by position
- [[Presentation Bias]] — users can only signal on what's shown

## Related Articles

- [[What is Presentation Bias in Search]] — [[Doug Turnbull]]; how presentation limits signal quality
- [[Query Understanding - Session Context]] — session-level signals
- [[Query Understanding - Introduction]] — series entry point

## People

- [[Daniel Tunkelang]] — author; queryunderstanding.com series
