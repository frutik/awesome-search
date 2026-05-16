---
type: topic
aliases: ["search experimentation", "search A/B tests", "online evaluation"]
tags: [topic, experimentation, evaluation, search-quality]
related_concepts: ["[[NDCG]]", "[[MAP]]", "[[Search Relevance]]", "[[Interleaving]]"]
related_topics: ["[[Managing a Search Team]]", "[[Economics of Search]]"]
articles: ["[[A-B Testing for Search is Different]]", "[[A-B Testing for Search]]"]
created: 2026-05-16
---

# A/B Testing for Search

How to design, run, and interpret search experiments. Search has specific challenges that make standard web A/B testing methodology fail if applied naively.

---

## Why Search A/B Testing Is Different

### Query Sparsity
Most queries are rare. The long tail of queries means:
- A given query may appear only once in a 2-week experiment window
- Traditional per-session or per-user randomization dilutes signal because users see different queries
- You cannot get statistical significance on individual query-level changes

**Implication**: randomize at the query level or use interleaving, not just user-level split.

### Session Effects
Search is not one interaction — it's a session of multiple queries, reformulations, and clicks. A bad result on query 1 affects behavior on query 2.

- Users may abandon after a bad result and not return within the session
- CTR on later queries in a session is confounded by earlier results
- Standard independence assumptions don't hold

**Implication**: measure session-level outcomes (task completion, session conversion) not just per-query metrics.

### Novelty and Primacy Effects
Users adapt to a new ranking over time. An improvement that looks small in week 1 may show stronger signal in week 3 as users learn. Conversely, a regression may be masked by user novelty curiosity.

### Metric Sensitivity
Search metrics are noisy. DCG and conversion rate on search sessions have high variance because:
- Query distribution shifts day-to-day (trending queries, seasonal patterns)
- User intent is implicit and inferred from clicks, not stated
- Different query types (navigational vs. informational vs. transactional) have very different behavior

---

## Experimentation Methods

### A/B Test (User-Level Split)
- Split users into control/treatment buckets
- Each user always sees the same ranking system
- Simple to implement; standard for product changes that affect the whole session
- **Problem**: slow — needs large sample to detect small relevance changes

### Interleaving
- For a single query, interleave results from both systems in one ranked list
- Infer preference from which system's documents users clicked
- Much more sensitive than A/B split — detects smaller differences faster
- **Types**: team draft interleaving, balanced interleaving
- **Limitation**: measures click preference, not business outcomes (conversion, revenue)
- Best used for early-stage signal before committing to a full A/B test

### Bucket Testing (Query-Level)
- Assign queries to buckets deterministically (e.g., hash of query string)
- Ensures same query always routes to same system
- Needed when query-level consistency matters (caching, personalization)

### Shadow Mode
- New system runs alongside old system without serving results to users
- Compare outputs offline; useful for regression detection before launch
- Does not measure user behavior; pairs well with offline eval

---


### Quasi-Experiments
When random user assignment isn't feasible (small user base, shared sessions, infrastructure constraints):
- **Query-level split**: route queries deterministically by hash — same query always hits the same system
- **Time-based split**: run control for period A, treatment for period B; less clean but usable for large changes
- **Geographic split**: treat regions as experimental units

Lower statistical rigor, but often the only option for low-traffic search products.

---

## Offline → Online Pipeline

The canonical workflow to avoid shipping bad changes:

1. **Offline eval** — filter out candidates that hurt NDCG/MAP on your judgment set (cheap, fast)
2. **Interleaving** — compare survivors using click preference signal (faster online signal)
3. **A/B test** — confirm winner against real business metrics before full rollout (slow, definitive)

Skipping offline eval wastes experiment bandwidth. Stopping at offline eval misses real user behavior.

## Metric Selection

| Metric | What it measures | Pitfalls |
|---|---|---|
| CTR (click-through rate) | Engagement | Position bias; rewards clickbait |
| P@1 | Top result quality | Ignores rest of page |
| Session conversion | Business outcome | Slow to accumulate; many confounders |
| Zero-results rate | Coverage | Doesn't capture bad results that return something |
| Abandonment rate | Failure signal | Ambiguous (quick exit = success or failure?) |
| NDCG (online) | Relevance via implicit labels | Needs position-debias; only as good as your click model |
| Time to click | Task efficiency | Fast click ≠ good result (position 1 always fast) |

**Rule**: always pair an engagement metric with a business outcome metric. CTR improvements that don't lift conversion are not wins.

---


| Query reformulation rate | Dissatisfaction proxy | Users rephrase when they didn't find what they wanted |
| Dwell time / long click | Result quality | Short dwell = unsatisfied; long dwell = engaged |

## Statistical Considerations

- **Sample size**: search experiments often need 1-2 weeks minimum due to query sparsity. Use power calculations before starting.
- **Multiple testing**: if you test 10 metrics, expect 0.5 false positives at p<0.05. Use Bonferroni correction or focus on a single primary metric.
- **Novelty effect**: run for at least 2 weeks to wash out first-week novelty behavior.
- **Segment analysis**: overall neutral can hide wins on head queries and losses on tail. Always segment by query frequency.
- **Guardrail metrics**: define metrics that must not degrade (e.g., zero-results rate, page load time). An experiment that lifts conversion but breaks latency is not shippable.

---

## Common Failure Patterns

**Shipping on offline eval alone.** NDCG in an offline eval doesn't predict user behavior reliably — especially for subtle ranking changes. Offline eval is necessary but not sufficient.

**Underpowered experiments.** Running for 3 days with 5% traffic gives no useful signal. Short-cut experimentation leads to wrong decisions.

**Ignoring query distribution shift.** If a trending event dominates the experiment window, results don't generalize. Check for anomalies in query logs.

**Gaming CTR.** Optimizing purely for CTR leads to clickbait results at position 1. Anchor on downstream conversions.

**Not logging enough.** You can't debug an unexpected result if you didn't log query, result set, and user interaction together. Invest in logging infrastructure upfront.

---

## Practical Setup

1. **Offline eval harness first** — catch regressions before they reach users
2. **Logging pipeline** — query, results, clicks, conversions, joined at session level
3. **Experiment framework** — deterministic bucketing, consistent assignment, holdout group
4. **Dashboard** — real-time metric monitoring with statistical significance indicators
5. **Ramp protocol** — 1% → 5% → 25% → 50% → 100%, with automatic kill switch on guardrail breach

---

## Related

- [[NDCG]], [[MAP]] — offline metrics that precede online experiments
- [[Interleaving]] — faster alternative to A/B split for early signal
- [[Managing a Search Team]] — experimentation culture is a team-level investment
- [[Economics of Search]] — experiments are how you measure ROI
