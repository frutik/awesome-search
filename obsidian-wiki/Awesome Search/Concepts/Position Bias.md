---
title: "Position Bias"
aliases: ["presentation bias", "rank bias", "click bias", "position effect"]
tags:
  - concept
  - search-evaluation
  - bias
  - ranking
---

# Position Bias

## Definition

Position bias is the tendency for users to click on higher-ranked search results independent of their actual relevance — simply because they appear earlier. It is the primary confounder when using click data as a relevance signal.

## The Problem

In a ranked result list:
- Rank 1 gets ~30–40% of all clicks
- Rank 3 gets ~10% 
- Rank 10 gets ~2%

But if users never see rank 10 results (they don't scroll), that 2% doesn't mean rank 10 results are bad — they just weren't examined.

## Examination Hypothesis

The standard model: a user clicks a result if and only if:
1. They **examine** it (probability depends on position)
2. They find it **relevant** (probability depends on actual quality)

```
P(click | position i) = P(examine | position i) × P(relevant | document i)
```

Position bias = the `P(examine | position i)` factor varying by rank.

## Types of Presentation Bias

### Position Bias
Items at top of list get more clicks regardless of quality.

### Cascade Model  
User reads results top-to-bottom, stops at first satisfactory result. Probability of examining rank i depends on not being satisfied at ranks 1...(i-1).

### Trust Bias
Users trust certain sources (Wikipedia, Amazon) more — click them even at lower ranks.

### Social Proof Bias
Items with more ratings/reviews get clicked more — regardless of actual quality match.

## Correcting for Position Bias

### Inverse Propensity Scoring (IPS)
Weight each click by the inverse probability of being shown at that position:
```
debiased_label = click_label / P(examine | position i)
```
Where `P(examine | position i)` is estimated from randomization experiments.

### Counterfactual Evaluation
Occasionally swap rank positions (interleaving or randomization) to observe how clicks change.

### Position-Aware Training
For [[Learning to Rank]] models, include position as a training feature but not as a test feature.

## Impact on LTR Training

Training LTR models on biased click data:
- Model learns to place high-CTR items first (regardless of quality)
- Creates feedback loop: top items get more clicks → model ranks them higher → they get even more clicks
- "Rich get richer" effect compounds over time

Debiasing is essential for unbiased LTR models.

## Position Bias in Evaluation

When evaluating search systems, position bias affects:
- **A/B test CTR**: system that shows popular items first looks better in CTR but may serve users worse
- **NDCG from click labels**: biased toward top positions
- **Session abandonment**: hard to distinguish "satisfied at rank 1" from "frustrated after rank 1"

## Related Concepts

- [[Click Signals]] — position bias is the main issue with click signals
- [[Learning to Rank]] — must correct for bias in training data
- [[Search Evaluation]] — bias affects online evaluation validity
- [[Diversity Metrics]] — diversity reduces concentration at top positions
- [[Judgment Lists]] — human judgments are position-unbiased (when evaluated blindly)

## People

- [[Daniel Tunkelang]] — position bias in search quality discussion
- [[Doug Turnbull]] — debiasing in LTR training
