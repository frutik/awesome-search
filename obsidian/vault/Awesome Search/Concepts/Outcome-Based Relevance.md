---
type: concept
title: Outcome-Based Relevance
aliases:
  - outcome-based relevancy
  - performance-based recommendation
  - engagement-based relevance
tags:
  - concept
  - search-evaluation
  - e-commerce
  - recommendation
created: 2026-10-04
---

# Outcome-Based Relevance

Relevance judged by what users do with a result, such as clicks, purchases and downstream engagement, rather than by how well its content matches the query. The recommender-systems literature calls it performance-based recommendation. Its counterpart is [[Semantic Relevance]], which [[Criteo]] calls *accuracy*.

---

## Definition

Matching a query on content does not tell you which of several matching products shoppers will actually pick. Outcome-based relevance scores that difference. In Criteo's framing, semantic match is the entry ticket. Measuring and optimising the outcome side needs commerce data: clicks, sales and other behavioural signals.

## Measuring it

Criteo's offline versions are rank-based. One takes the position of the product a user actually clicked, or actually bought, within a fixed candidate set, normalized into a reciprocal-rank style score ([[MRR]]). Negatives that share the target's brand or category force a model past surface text matching (see [[Hard Negative Mining]]).

## The tension with semantic relevance

[[Etsy]] and Criteo pull in opposite directions on the same signal:

- **Etsy** treats engagement as biased towards already-popular listings and adds semantic relevance to correct it (see [[Semantic Relevance]]).
- **Criteo's** largest reported gain on the outcome side comes from adding popularity. Re-ranking 400 semantically retrieved candidates by recent sales share, instead of by semantic similarity, more than doubled the normalized rank score of the purchased product (0.029 → 0.074). Criteo labels the gain +60%, apparently measured against the new value.

Both positions can hold at once. Semantic relevance is the floor that keeps results on-intent, and outcome signals order what clears it. That is the guardrail-then-optimise layout [[CLEPR]] uses in production. Outcome metrics inherit the biases of the behaviour they are built from, such as [[Position Bias]] and the invisibility of relevant items nobody clicked.

## Related Concepts

- [[Semantic Relevance]] — the content-match counterpart
- [[Click Signals]] · [[Implicit Judgments]] — the behavioural evidence it is built from
- [[Position Bias]] — the main distortion in that evidence
- [[MRR]] — the rank metric used to score it
- [[Hard Negative Mining]] — same-brand or same-category negatives in the benchmark
- [[Reranking]] — the stage where commerce signals usually enter

## Related Articles

- [[Leveraging Commerce Data for Outcome-Based Relevancy in Agentic Recommendation Systems]] — the framing and benchmarks
- [[Introducing CLEPR, our model for semantic understanding]] — the same split applied to sponsored products

## Related Topics

- [[Outcome-Based vs Semantic Relevance]] — how the two signals are sourced, why they diverge, and how systems combine them
- [[E-commerce Search]] · [[Conversational and Agentic Search]]
