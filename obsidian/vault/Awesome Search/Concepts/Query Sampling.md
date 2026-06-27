---
type: concept
aliases: ["query set construction", "evaluation query set", "query sampling", "PPS sampling"]
tags: [concept, evaluation, sampling, search-quality]
related: ["[[Judgment Lists]]", "[[Search Evaluation]]", "[[Search Quality Assurance]]", "[[NDCG]]"]
created: 2026-05-16
---

# Query Sampling

How to construct a representative query set for offline evaluation. The quality of your judgment-based metrics (NDCG, MAP, MRR) is only as good as the queries you evaluate against.

A biased sample produces misleading metrics — optimizing against it can harm real user experience.

---

## The Problem with Naive Sampling

If you sample uniformly from your query log, rare queries dominate the sample (they are the vast majority of unique queries). Your evaluation then measures performance on the long tail, which may not reflect where most user value comes from.

If you sample by traffic volume, head queries dominate, and you miss systematic failures on the tail.

The right approach depends on your evaluation goal.

---

## Sampling Methods

### Random Sampling
Draw queries uniformly at random from the query log (unique queries or all occurrences).

- **Pro**: simple, unbiased with respect to query distribution
- **Con**: over-represents the long tail (which has many unique queries but little traffic); expensive to label if most sampled queries are rare

Best for: auditing coverage, discovering unknown failure modes.

---

### Stratified Sampling
Divide the query space into strata (e.g., by frequency tier, query type, domain) and sample independently from each stratum.

Example strata:
- **Head** (top 1% of queries by volume)
- **Torso** (1-20%)
- **Tail** (bottom 80%)
- By query type: navigational, transactional, informational

Sample a fixed number from each stratum regardless of stratum size.

- **Pro**: guarantees representation of all segments; prevents any one tier from dominating
- **Con**: requires defining meaningful strata; labels from different strata have different signal value

Best for: balanced evaluation across query tiers; catching failures in head queries that a uniform sample would dilute.

---

### Probability-Proportional-to-Size (PPS) Sampling
Sample queries with probability proportional to their traffic volume (query frequency).

- High-traffic queries are more likely to be sampled → more annotation effort goes where user impact is highest
- Rare queries still appear, just proportionally less

Formally: $P(\text{query}_i \text{ selected}) \propto \text{frequency}_i$

- **Pro**: annotation effort is allocated where it matters most (by traffic impact); avoids wasting labels on rare queries
- **Con**: long-tail failures are underrepresented; rare but high-value query types may be missed

Best for: efficient use of annotation budget when you want your eval to reflect user-weighted impact; standard choice for production eval sets.

---

## Comparison

| Method | Head coverage | Tail coverage | Annotation efficiency | Best for |
|---|---|---|---|---|
| Random | Low | High | Low | Discovery, coverage audits |
| Stratified | Guaranteed | Guaranteed | Medium | Balanced regression testing |
| PPS | High | Proportional | High | Production quality tracking |

---

## Practical Guidance

- Use **PPS** as your default production eval set — it reflects where users actually live
- Maintain a separate **stratified** set for regression testing — ensures a bad tail change doesn't go undetected
- Refresh sampling periodically — query distributions shift with product changes, seasonality, and growth
- Label a minimum of 100-300 queries before trusting NDCG trends; 1000+ for stable estimates


## Per-Tier Handling (Not Just Sampling)

Sampling decides *which* queries you look at; it doesn't decide what to *do* with each tier. [[Nick Zadrozny]] ([[Bonsai]]) argues each frequency tier calls for a different response — and that the response often lives **outside search**:

- **Head** — worth manual, hand-tuned attention. But ask whether the fix belongs elsewhere: a frequent **navigational** query may be better solved by site navigation or a prominent feature than by ranking. A head query can signal an unmet product need, not a search bug.
- **Torso** — build **generalizable models from first principles** instead of special-casing; sample representative torso queries so you don't over-fit to the head; align intent with index and request design during development.
- **Tail** — keep in the test suite despite rarity; the tail is irreducibly hard (free-form expression), so scale with **ML and engagement signals** rather than human labels alone. Novel queries are a large share of traffic — Google has reported ~15% of daily queries are never-before-seen.

The framing: *you are not optimizing search results, you are optimizing the end-user experience — a holistic product concern.* Stratified [[Query Sampling|sampling]] is what makes all three tiers visible at once.

## Related

- [[Judgment Lists]] — the labels applied to the sampled queries
- [[Search Evaluation]] — the broader offline evaluation framework
- [[Search Quality Assurance]] — query sampling is one step in the full SQA practice
- [[NDCG]], [[MAP]], [[MRR]] — metrics computed over the sampled query set

## Articles
- [[Query Sampling for Relevancy Testing]] — [[Nick Zadrozny]] / [[Bonsai]]; per-tier (head/torso/tail) handling strategy and the product-concern framing
- [[Succeeding with Relevance Evaluation using PPS Sampling]] — the PPS technique in depth
- [[Setting Up a Relevance Evaluation Program]] — weighted random sampling by query frequency