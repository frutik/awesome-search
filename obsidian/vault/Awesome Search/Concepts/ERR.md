---
type: concept
title: "ERR (Expected Reciprocal Rank)"
aliases: ["ERR", "Expected Reciprocal Rank", "expected reciprocal rank metric"]
tags:
  - concept
  - evaluation
  - metrics
  - search-quality
created: 2026-09-16
---

# ERR (Expected Reciprocal Rank)

## Definition

ERR is a ranking quality metric that scores a result list by how soon a user is likely to be *satisfied* by it. Unlike [[NDCG]], which credits every relevant document independently, ERR assumes the user reads top-down and stops once satisfied — so a document only earns credit for the share of users who were still looking when they reached it.

## Formula

```
ERR = Σᵢ  (1/i) × Rᵢ × Πⱼ<ᵢ (1 - Rⱼ)
```

Where `Rᵢ` is the probability of satisfaction at rank *i*, a function of that result's relevance grade. The trailing product is the probability that nobody was satisfied at any earlier rank — the discount is therefore not a fixed positional curve but depends on what the ranker put above.

## The Underlying User Model

ERR models users as a **cascade**: read rank 1, stop if satisfied, otherwise read rank 2, and so on. Two consequences follow:

- If the first result is perfect (`Rᵢ = 1.0`), later results contribute almost nothing — the user never sees them.
- A highly relevant document at rank 3 is worth far less when ranks 1 and 2 are also highly relevant than when they are poor.

[[NDCG]] instead uses an **independent utility model**: all relevant documents are worth finding, position matters through a fixed logarithmic discount, and documents do not compete with each other.

## ERR vs. NDCG

| Scenario | NDCG | ERR |
|---|---|---|
| Perfect result at rank 1, more relevant at rank 5 | Rewards rank 5 (adds to DCG) | Minimal reward — user already satisfied |
| Two good results at ranks 1 and 2 | Sums both | Rank 2 partially discounted |
| Ambiguous query needing multiple angles | Rewards a diverse set of good results | Stops at first satisfaction |
| Known-item search | Equivalent to [[MRR]] | Behaves similarly |

## When to Use ERR

Choose ERR when *"one great result beats two good results"* is the right model of your user:

- Navigational queries
- Known-item search

Choose [[NDCG]] instead when the user genuinely wants to see several options — e-commerce product search, exploratory and informational queries, research evaluation where multiple relevant documents are expected.

## Normalization

Like [[NDCG]], ERR can be computed normalized (against the ideal ordering) or unnormalized. Normalized values sit in [0,1] and can be compared across query sets of differing difficulty; unnormalized values measure absolute quality but are harder to compare across queries.

## Relation to Other Metrics

ERR sits between [[MRR]] and [[NDCG]]. [[MRR]] is the special case of a binary, single-answer world — credit for the rank of the first relevant result and nothing else. ERR generalizes that to graded relevance: partial satisfaction at each rank, with the remaining probability mass flowing down the list. [[NDCG]] drops the stopping model entirely.

Because its discount is behavioral rather than positional, ERR belongs to the same family of thinking as [[Click Models]], which likewise express a metric or score in terms of an assumed reading behaviour, and as [[Session-Based Evaluation]], which models a sequence of actions rather than a single ranked list.

## Related Concepts

- [[NDCG]] — the independent-utility alternative; the standard default for graded relevance
- [[MRR]] — the binary, single-answer case ERR generalizes
- [[MAP]] — binary-relevance alternative over all relevant positions
- [[Search Evaluation]] — where offline ranking metrics fit
- [[Judgment Lists]] — the graded labels ERR consumes
- [[Click Models]] — the wider family of user-behaviour models ERR's stopping assumption belongs to
- [[Session-Based Evaluation]] — evaluation beyond the single ranked list
- [[Position Bias]] — why later ranks are examined less in the first place

## Articles

- [[Demystifying nDCG and ERR]] — the NDCG-vs-ERR contrast, user models, and when to use each
- [[Choosing Your Search Relevance Evaluation Metric]] — the broader metric-selection decision guide
- [[Flavors of NDCG]] — NDCG formulation variants
- [[Session vs Query based Search Evals]] — session models ERR gestures at
