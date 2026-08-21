---
type: concept
title: "Bayesian Optimization"
aliases: ["Bayesian search", "Bayesian parameter optimization"]
tags:
  - concept
  - relevance-tuning
  - search-relevance
created: 2026-08-21
---

# Bayesian Optimization

## Definition

A technique for tuning a small set of continuous ranking parameters — [[BM25]] `k1`/`b`, field boosts, minimum-should-match, fuzziness — without exhaustively grid-searching the space. A surrogate model (a Gaussian process, in the common formulation) is fit over past (parameter-set, relevance-metric) observations; nearby untested parameter sets are assumed to score similarly, with uncertainty growing with distance from what's been observed. Each round balances exploring uncertain regions against exploiting regions already known to score well, converging toward a good configuration far faster than grid search.

Framed by [[Doug Turnbull]] as a lightweight halfway point between hand-tuned boosts and full [[Learning to Rank]]: it optimizes the *existing* ranking function's parameters rather than learning an arbitrary new functional form, so it needs no new training/serving infrastructure — closer to a "semi-automated," human-in-the-loop tuning process than to LTR's more automated one.

## Practical Pitfalls (from Shopify's experience)

- **Optimizers exploit loopholes.** If the training/evaluation data has a shortcut (e.g. exact-length product titles happening to correlate with clicks), the optimizer will find and lean on it rather than genuinely improving relevance.
- **Check the training signal for bias**, not just the objective. Shopify's first run inherited **presentation bias**: because the prior engine used default [[BM25]], clicks skewed toward whatever it was already surfacing, feeding that bias back into the optimizer.
- **Don't just take the single best-scoring configuration.** Compare it against the distribution of near-best configurations — which parameters cluster tightly (doing real work) vs. which vary freely (not very influential) — as a sanity check on what the optimizer actually learned.
- **Fix parameters known to be uninfluential** rather than searching over them (e.g. `k1` barely matters when term frequencies are binarized rather than raw-counted).

See [[Haystack US 2022 - Bayesian Optimization of Relevance at Shopify]] for the full worked example.

## Related Concepts
- [[BM25]] — the parameters most commonly tuned this way
- [[Learning to Rank]] — the more infrastructure-heavy alternative
- [[NDCG]] — typical offline objective being optimized
- [[Search Evaluation]]

## People
- [[Doug Turnbull]] · [[Andy Toulis]]

## Videos
- [[Haystack US 2022 - Bayesian Optimization of Relevance at Shopify]]
