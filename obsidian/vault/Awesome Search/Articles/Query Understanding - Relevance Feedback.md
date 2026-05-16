---
title: "Relevance Feedback"
source: "https://queryunderstanding.com/relevance-feedback-c6999529b92c"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems use user feedback on results to refine queries and improve subsequent retrieval — part of the Query Understanding series."
tags:
  - clippings
---

# Relevance Feedback

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Relevance feedback uses signals from users about which results are relevant (or not) to refine the search query and retrieve better results. It's a mechanism for iterative search refinement.

## Types of Relevance Feedback

**Explicit feedback**
- User marks results as relevant/not relevant
- Thumbs up/down ratings
- "More like this" buttons
- Rare in practice — users don't want to provide explicit feedback

**Pseudo-relevance feedback (PRF)**
- Assume top-k results are relevant
- Extract key terms from those results
- Add terms to query and re-execute
- No user interaction needed; can drift if initial results are poor

**Implicit feedback**
- Clicks as positive signals
- Long dwell time → relevance
- Immediate back-navigation → not relevant
- Conversions (purchases) as strong positive signals

## Rocchio Algorithm

Classic explicit feedback algorithm:
```
new_query = α * original_query + β * avg(relevant_docs) - γ * avg(non_relevant_docs)
```

Moves query vector toward relevant documents and away from non-relevant ones in vector space.

## Modern Applications

- **"More like this"**: Elasticsearch `more_like_this` query
- **"Find similar"**: Visual similarity in image search
- **Session refinement**: Implicit feedback from click patterns
- **LLM-based rewriting**: Use clicked documents to rewrite query

## Challenges

- Explicit feedback rarely given by users
- Implicit signals are noisy (clicks ≠ relevance)
- Feature/item discovery problem: can't improve if user never sees relevant items

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Click Signals]]
- [[Session-Based Evaluation]]

## People

- [[Daniel Tunkelang]]
