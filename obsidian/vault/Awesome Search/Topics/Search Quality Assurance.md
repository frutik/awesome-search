---
type: topic
aliases:
  - SQA
  - search evaluation
  - search quality
tags:
  - topic
  - evaluation
  - search-quality
  - metrics
related_concepts:
  - "[[NDCG]]"
  - "[[MRR]]"
  - "[[MAP]]"
  - "[[Precision and Recall]]"
  - "[[MMR]]"
  - "[[APD]]"
  - "[[Diversity Metrics]]"
  - "[[Click Signals]]"
  - "[[Clicks Residual]]"
  - "[[Zero Results]]"
  - "[[Judgment Lists]]"
  - "[[LLM as Judge]]"
  - "[[Session-Based Evaluation]]"
  - "[[Query Sampling]]"
related_topics:
  - "[[A-B Testing for Search]]"
  - "[[Managing a Search Team]]"
articles:
  - "[[Session vs Query based search evals 1]]"
  - "[[Measuring Search Effectiveness 1]]"
  - "[[Choosing your search relevance evaluation metric]]"
  - "[[Measuring Search - Metrics Matter 1]]"
people:
  - "[[Daniel Tunkelang]]"
  - "[[James Rubinstein]]"
  - "[[Doug Turnbull]]"
created: 2026-05-16
---

# Search Quality Assurance

The practice of measuring, monitoring, and improving search quality systematically. SQA answers: "Is search getting better or worse, and how do we know?"

---

## Evaluation Paradigms

### Session-Based Evaluation
Measures outcomes at the session level — did the user accomplish their task?

- **Signals**: task completion, session abandonment, zero reformulations
- **Strength**: captures multi-query behavior; closer to business outcomes
- **Weakness**: harder to attribute to a specific ranking change; requires more data

See [[Session-Based Evaluation]].

### Query-Based Evaluation
Measures quality per individual query, averaged over a query set.

- **Signals**: NDCG, MRR, MAP, P@K on a labeled sample
- **Strength**: fast, targeted, actionable; easy to diff between systems
- **Weakness**: ignores session context; quality of eval depends entirely on the query sample

Most offline evaluation is query-based. The query sample construction is critical — see [[Query Sampling]].

---

## Building the Query Sample

The quality of your evaluation is only as good as your query sample. A biased sample gives misleading metrics.

| Method | When to use |
|---|---|
| **Random sampling** | Baseline; unbiased but over-represents rare queries |
| **Stratified sampling** | Sample separately by query type, frequency tier, or domain — ensures head/torso/tail are all represented |
| **PPS (Probability-Proportional-to-Size)** | Weight sample by traffic volume — head queries get more labels, but tail queries still appear proportionally |

See [[Query Sampling]] for full details.

---

## Metrics

### Ranking Quality
Measure whether the right results are ranked at the top.

| Metric | What it captures | Best for |
|---|---|---|
| [[NDCG]] | Graded relevance, discounted by position | Multi-grade labels, long result lists |
| [[MRR]] | Position of first relevant result | Navigational queries, single-answer tasks |
| [[MAP]] | Precision at each relevant result, averaged | Binary relevance, recall-sensitive tasks |
| [[Precision and Recall]] | Coverage and accuracy tradeoff | Filtering tasks, document retrieval |
| P@K | Precision in top-K results | Quick sanity check on top of SERP |

### Diversity Metrics
Measure whether results cover different aspects of the query intent.

| Metric | What it captures |
|---|---|
| [[MMR]] (Maximal Marginal Relevance) | Penalizes redundant results; balances relevance and novelty |
| [[APD]] (Average Pairwise Distance) | Average dissimilarity across all result pairs |
| Entropy | Distribution of result categories/topics |
| [[Diversity Metrics]] | Overview of diversity measurement approaches |

### Behavioral / Product Metrics
Derived from real user interactions — no labels needed, but noisier.

| Metric | What it captures |
|---|---|
| CTR | Click-through rate; engagement with results |
| Zero clicks | Queries where no result was clicked — possible failure or direct answer |
| [[Clicks Residual]] | Gap between expected and observed click distribution — success signal at query level |
| [[Zero Results]] | Queries returning no results — direct coverage failure |
| Query reformulation rate | Users who rephrase after seeing results — dissatisfaction signal |

---

## Evaluation Modes

### Offline Evaluation
Evaluate a system against a labeled dataset without user traffic.

**Advantages**: fast, cheap, reproducible, safe (no user exposure to bad systems)
**Limitations**: labels may not reflect current user intent; doesn't capture behavioral effects

Requires [[Judgment Lists]]. Three ways to produce labels:

- **Human judgments** — annotators rate query-document pairs; gold standard but slow and expensive
- **Implicit judgments** — derive labels from click logs, dwell time, purchases; fast but biased by position and existing ranking
- **LLM as judge** — use an LLM to produce relevance ratings; scalable but requires calibration against human labels (see [[LLM as Judge]])

### Online Evaluation
Measure the impact of a change on real users via controlled experiments.

See [[A-B Testing for Search]] for the full treatment: interleaving, A/B splits, metric selection, statistical considerations.

---

## Evaluation Cadence

| Type | Frequency | Purpose |
|---|---|---|
| Automated offline eval | Every code change (CI) | Catch regressions before deployment |
| Structured offline eval | Weekly/sprint | Track trends; inform roadmap |
| Human annotation refresh | Quarterly | Keep judgment set current with product changes |
| A/B test | Per significant change | Confirm offline wins translate to user behavior |
| Metric review with stakeholders | Monthly | Align on business-level quality definition |

---

## Common Failure Modes

**Evaluating against stale labels.** Judgment sets age. A 2-year-old label set reflects old product, old catalog, old user intent. Build annotation refresh into your process.

**Single-metric tunnel vision.** Optimizing NDCG alone can hurt diversity, freshness, or zero-results rate. Define a primary metric but track a dashboard of secondaries with guardrails.

**Head query bias.** Teams manually review their top-50 queries and call it evaluation. The long tail (60-80% of volume) determines real user experience.

**Conflating offline and online results.** An offline improvement that doesn't show up in A/B testing isn't necessarily a bad metric — it may reveal a flawed label set. Investigate the gap rather than dismissing one or the other.

---

## Related

- [[A-B Testing for Search]] — online evaluation in depth
- [[Judgment Lists]] — how to build and maintain a label set
- [[Query Sampling]] — how to build a representative query set
- [[Managing a Search Team]] — evaluation culture as a team practice
- [[LLM as Judge]] — scaling annotation with LLMs
