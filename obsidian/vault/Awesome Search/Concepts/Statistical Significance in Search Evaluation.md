---
type: concept
title: "Statistical Significance in Search Evaluation"
aliases: ["statistical significance", "paired t-test", "bootstrap resampling", "significance testing"]
tags:
  - concept
  - search-evaluation
  - statistics
  - experimentation
created: 2026-08-05
---

# Statistical Significance in Search Evaluation

## Definition

A ranking change moves your metric. Statistical significance testing answers whether that movement reflects a real difference between systems, or whether you would have seen it anyway from the particular queries you happened to sample.

It is the step most homegrown evaluation harnesses skip, and skipping it is how teams ship changes that do nothing — or worse, chase noise for a quarter.

## The Core Point: Use Paired Tests

Offline search evaluation has a structural advantage that should always be exploited: **both systems are run on the same queries**. That means you can compare per-query scores directly rather than comparing two independent averages.

Given system A and system B scored on the same N queries, the unit of analysis is the **per-query difference**. A paired test on those differences is dramatically more sensitive than an unpaired comparison of means, because it removes the largest source of variance — the fact that some queries are simply harder than others.

Two standard choices:

- **Paired t-test** — fast, standard, assumes roughly normal differences. Adequate in practice for a few hundred queries.
- **Paired bootstrap / permutation test** — resample the query set thousands of times and observe how often the sign of the difference flips. Makes no distributional assumption, which suits [[NDCG]] deltas well since they are bounded and skewed. Generally the better default.

## Why Mean NDCG Alone Misleads

A mean improvement of +0.004 NDCG across 500 queries is compatible with all of these situations:

- 250 small wins, 240 small losses — noise
- 30 large wins, 5 losses — a real, targeted improvement
- 15 enormous wins on tail queries, 100 modest losses on head queries — a **revenue regression** despite a positive mean

The mean cannot distinguish them. Always report alongside it:

- **Win / loss / tie counts** at some meaningful delta threshold
- **The loss tail** — the queries that regressed most, read by a human
- **Per-segment breakdown** — head, torso, tail scored separately, since an aggregate hides the segment carrying your traffic

## Effect Size and Test Set Size

Significance and importance are different questions. With a large enough query set, a trivially small difference becomes statistically significant; with 50 queries, a substantial improvement may not reach significance at all.

Rules of thumb worth holding loosely:

- With a few hundred queries, differences below roughly 1–2% relative [[NDCG]] are usually not distinguishable from noise
- Detecting smaller effects requires more queries, and the relationship is steep — halving the detectable effect costs roughly four times the queries
- Decide the smallest difference you would actually act on *before* running the test, and size the query set for that

## The Multiple Comparisons Trap

Testing twenty configurations against a baseline at p < 0.05 will produce about one "significant" winner by chance alone. Sweeping hyperparameters, negative-mining strategies, and base models against a single evaluation set is exactly this situation.

Correct for it (Bonferroni is crude but honest), or better: treat the sweep as *selection* rather than *evidence*, and confirm the winner on a held-out split opened once. See the dev-set trap in [[Model Selection and Fine-Tuning Evaluation]].

## Online Testing

The same logic governs [[A-B Testing for Search|A/B tests]], with additional hazards: peeking at results before the planned sample size inflates false positives, and user-level rather than query-level randomization changes the unit of analysis. [[Interleaving]] is substantially more sensitive per unit of traffic for ranking-order comparisons, which is why it is worth the implementation cost.

## Tooling

`ranx` provides significance testing built into its metric computation, which is the main reason to prefer it over hand-rolled metric code. See [[Retrieval Benchmarks and Leaderboards]].

## Related Concepts

- [[Search Evaluation]] · [[NDCG]] · [[MRR]] · [[MAP]]
- [[Judgment Lists]] — supplies the per-query scores being tested
- [[Query Sampling]] — determines what the test can generalize to
- [[Interleaving]] — the sensitive online counterpart

## Related Topics

- [[Model Selection and Fine-Tuning Evaluation]] — where this sits in the workflow
- [[A-B Testing for Search]] · [[Relevance Program Setup]] · [[Duality in Measuring Search]]
