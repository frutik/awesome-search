---
type: concept
title: "Interleaving"
aliases: ["interleaving", "result interleaving", "zip merge"]
tags:
  - concept
  - ranking
  - evaluation
  - hybrid-search
created: 2026-06-11
---

# Interleaving

## Definition

Interleaving merges two ranked result lists into a single ranking by alternating ("zip-merge") items from each, optionally weighted by sampling probabilities so one source contributes more often. It serves two purposes:

1. **Fusion baseline** — a simple, hard-to-beat way to combine multiple retrievers (e.g. lexical + vector) when their scores are non-comparable, without training a model.
2. **Online evaluation** — interleaving two rankers and observing which side's items get clicked is a sensitive [[A-B Testing for Search|A/B testing]] alternative that needs less traffic than split testing.

## Why it matters

In a multi-retriever / [[Hybrid Search]] setup, interleaving solves the **cold-start** problem: you need behavioral history before you can train an LTR fusion model, but you need *some* unified ranking to collect clicks. Interleaving provides that initial ranking, after which a [[LambdaMART]] / [[Learning to Rank|LTR]] re-ranker (e.g. [[Metarank]]) can take over.

## Interleaving as online evaluation

The second use case deserves its own treatment, because it solves a problem A/B
testing cannot.

**Why parallel ranking A/B tests break.** Simultaneously running ranking
experiments violate the independence assumption — they influence each other's
outcomes — so you cannot simply run many at once. The workarounds (multivariate
experiments, splitting traffic into subgroups with one experiment each, or
leaning on indirect early-indicator metrics) each cost either statistical power
or considerable complexity.

**Team-draft interleaving.** Instead of randomizing on the *customer*, results
from two rankers are merged into one list and **each position becomes the unit of
randomization**. You then measure whether users interact more with results
attributed to ranker A or ranker B, using bootstrapping to obtain a distribution
over the relative wins.

**Why it is dramatically more sensitive.** The clearest explanation comes from
segmenting users by purchase intent:

| Segment | Behavior | Contribution to an RCT |
|---|---|---|
| Low intent | Browse, rarely convert | Noise — searches and pageviews, no conversions |
| High intent | Convert almost regardless of ranking | **Noise** — they convert even on a bad ordering, so they carry no evidence about quality |
| Convincible | Convert only if shown the right item | The only real signal — and extremely sparse |

An RCT learns almost solely from that last sliver. Interleaving also extracts
signal from high-intent users, because even a certain-to-convert user still picks
the item that fits best — and that pick is attributable to one ranker. The number
of meaningful votes rises substantially.

Booking.com reported potential for a **10–100x speedup** from this sensitivity,
allowing tests on less traffic with more variants in parallel. On statistics
alone their runtime could drop to hours, though they still run at least a day so
no decision rests on a single timezone's users.

**Limitations — interleaving is a preselection tool.** A conclusive preference in
an interleaving trial does *not* imply the corresponding metric will move
significantly in an RCT at the usual expected effect size, and interleaving
**cannot estimate effect size at all**. So it narrows the field of candidate
rankers, and a confirmatory RCT still follows. The worst case is promoting a
suboptimal model into that RCT rather than the best one.

## Related Concepts

- [[Reciprocal Rank Fusion]] — score-free rank fusion alternative
- [[Linear Score Combination]] · [[Relative Score Fusion]] — score-based fusion
- [[Hybrid Search]] — primary use case
- [[Learning to Rank]] · [[Click Signals]] — what interleaving bootstraps
- [[A-B Testing for Search]] — interleaving as an online eval method
- [[Isolated Feedback Loops]] — the leakage problem interleaving partly sidesteps
- [[Statistical Significance in Search Evaluation]] — where the sensitivity gain shows up
- [[Position Bias]] — position as unit of randomization is what neutralizes it

## Articles

- [[Hybrid Search and Learning-to-Rank with Metarank]] — interleaving as the cold-start baseline
- [[Getting Started on Search Relevance for the Understaffed Search Team]]
- [[Beyond Algorithms - Ranking at Scale at Booking.com]] — team-draft interleaving in production; the intent-segmentation argument and the stated limitations
