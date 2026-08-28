---
type: concept
title: "Kendall Rank Correlation"
aliases: ["Kendall's Tau", "Kendall's tau", "tau", "KRR", "rank correlation coefficient"]
tags:
  - concept
  - search-evaluation
  - metrics
  - ranking
created: 2026-08-28
---

# Kendall Rank Correlation

## Definition

Kendall rank correlation (Kendall's tau) measures how similar two orderings of the same set of items are. It compares every pair of items and checks whether the pair is ordered the same way in both rankings (**concordant**) or the opposite way (**discordant**):

```
tau = (concordant pairs - discordant pairs) / (n choose 2)
```

Equivalently, when there are no tied ranks, tau can be computed by counting **inversions** — pairs that are out of order between the two rankings — relative to the maximum possible number of pairs:

```
tau = 1 - (4 * inversions) / (n * (n - 1))
```

**Range**: -1 to +1.
- **+1** — the two orderings are identical.
- **0** — no relationship between the orderings.
- **-1** — the second ordering is the complete reverse of the first.

Common implementations: Apache Commons Math's `KendallsCorrelation` (Java), `scipy.stats.kendalltau` (Python).

## What It Measures vs. What It Doesn't

Kendall's tau compares two *orderings* against each other — it says nothing on its own about which ordering is *better*. It requires no ground-truth relevance labels, unlike [[NDCG]] or [[MAP]], which score a ranking against [[Judgment Lists]]. This makes it useful as a diagnostic for **how much an ordering changed**, but unsuited to answering **whether the change was an improvement** — that question still needs a relevance-grounded metric (NDCG, MAP) or an online signal (CTR, conversion).

## Use in Reranking Diagnostics

A low `krr` (e.g. 0.15) means the reranker substantially reshuffled the candidates relative to their input order. For a working LTR reranker this is the expected and desired outcome: `krr` near +1.0 would mean the model is echoing the input order back with little change, i.e. adding no ranking value. A near-zero or negative `krr` on its own is not a quality signal — it only confirms that reranking did something; whether that something helped users still requires NDCG/MAP against judgments, or online CTR/conversion metrics.

## Use in Comparing Judgment Lists

Kendall's tau is also used to compare *judgment systems* against each other — measuring how much two different methods for producing [[Judgment Lists]] (e.g. human-rated vs. click-derived) agree on relative document ordering, as one way of sanity-checking whether a judgment list is trustworthy. See [[What Is a Judgment List?]].

## Related Concepts

- [[NDCG]] — relevance-grounded ranking quality metric; contrast with tau, which requires no relevance labels
- [[MAP]] — binary-relevance ranking metric; same contrast as NDCG
- [[Learning to Rank]] — the family of models whose reranking behavior tau can be used to diagnose
- [[Reranking]] — the stage whose input/output order shift tau measures
- [[Judgment Lists]] — judgment-comparison use case for tau
- [[Search Evaluation]] — broader evaluation framework

## Tools

- [[Metarank]] — logs Kendall rank correlation (`krr`) as an operational diagnostic on every rerank request

## Articles

- [[What Is a Judgment List?]] — cites Kendall's Tau as a way to find correlation/agreement between different judgment systems
