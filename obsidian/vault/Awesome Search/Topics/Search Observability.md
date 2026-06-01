---
type: topic
title: "Search Observability"
aliases: ["search monitoring", "search telemetry", "search instrumentation"]
tags:
  - topic
  - monitoring
  - metrics
  - search-quality
  - production
related_concepts:
  - "[[Search Observability]]"
  - "[[Click Signals]]"
  - "[[Clicks Residual]]"
  - "[[Zero Results]]"
  - "[[Intent Drift]]"
  - "[[Session-Based Evaluation]]"
  - "[[Position Bias]]"
related_topics:
  - "[[Search Quality Assurance]]"
  - "[[A-B Testing for Search]]"
  - "[[Understaffed Search Team]]"
articles:
  - "[[Measuring Search - Metrics Matter]]"
  - "[[Measuring Searcher Behavior]]"
  - "[[Evaluating Good Search - Measure It]]"
  - "[[When There's No Conversion Rate]]"
  - "[[Click Residual - A Query Success Metric]]"
  - "[[Building Smarter Search Products 3 Steps for Evaluating Search Algorithms]]"
people:
  - "[[Daniel Tunkelang]]"
  - "[[James Rubinstein]]"
  - "[[Doug Turnbull]]"
created: 2026-06-01
---

# Search Observability

The discipline of making a live search system's behavior, health, and quality continuously visible — so that degradation is detected before users notice it, and root causes can be traced when things go wrong.

---

## Why Search Needs Its Own Observability

Standard infrastructure monitoring (uptime, latency, error rate) catches infrastructure failure but misses the dominant failure mode in search: **silent quality degradation**. A search system can return HTTP 200 with P99 latency well within SLA while quietly serving irrelevant results. Users respond by abandoning or reformulating — neither triggers an alert.

Search observability closes this gap. It treats user behavior as a signal of system quality, not just traffic load.

**Key difference from [[Search Quality Assurance]]:**
- SQA is evaluation — comparing two systems or versions offline, producing a verdict
- Observability is monitoring — watching one system in production, continuously, producing a time series
- They share many metrics but differ in purpose, cadence, and action threshold

**Key difference from [[A-B Testing for Search]]:**
- A/B testing is hypothesis-driven and time-bounded; it answers "is B better than A?"
- Observability is continuous and unprompted; it answers "is A still as good as it was last week?"

---

## Three Planes of Observability

### Plane 1: User Behavior

Behavioral signals measure whether users are succeeding. They are always available (no annotation required), but are indirect and biased.

| Signal | What it measures | Interpretation pitfalls |
|---|---|---|
| **CTR** (click-through rate) | Fraction of queries receiving at least one click | Position bias; rewards clickbait; zero-click can be success (direct answer) |
| **Zero-result rate** | Fraction of queries returning no results | The one unambiguous failure — always bad |
| **Abandonment rate** | Fraction of sessions ending without success | Ambiguous: fast exit can mean success (found it fast) or failure (gave up) |
| **Query reformulation rate** | Fraction of queries followed by another query within the same session | Dissatisfaction signal; user didn't find what they wanted on first try |
| **Dwell time / long click** | Time spent on a clicked result | Long dwell = satisfaction; short dwell = pogo-sticking back to SERP |
| **[[Clicks Residual]]** | Gap between expected and actual click distribution for a query | Detects queries underperforming relative to their type; position-bias corrected |
| **Session success rate** | Fraction of sessions ending with a terminal success event (purchase, saved, no reformulation) | Closest to true task completion; slow to accumulate |

Segment all behavioral metrics by **query tier** (head / torso / tail). Head queries account for 50%+ of traffic but are not representative of the long tail where most quality problems hide.

### Plane 2: System Health

System metrics measure whether the infrastructure is operating correctly. These are the closest to conventional SRE monitoring.

| Signal | What it measures | Alert threshold guidance |
|---|---|---|
| **Query latency P50/P99** | Response time distribution | P99 > SLA threshold; sudden P50 jumps indicate index or model changes |
| **Error rate** | Fraction of queries returning 5xx or timeout | Any sustained increase; zero-result from infrastructure error vs. genuine no-match |
| **Indexing lag** | Delay between document update and searchability | Domain-specific; e-commerce: minutes; news: seconds; enterprise: hours acceptable |
| **Cache hit rate** | Fraction of queries served from cache | A drop signals query distribution shift or cache invalidation issue |
| **Shard/replica health** | Availability of index shards | Missing shards silently degrade recall without error codes |
| **Ranking model freshness** | Age of the deployed model | Model older than retraining cadence → possible [[Intent Drift]] accumulation |

### Plane 3: Quality Trends

Quality signals track whether relevance is staying stable or drifting. Unlike behavioral signals, these require a baseline to be meaningful — they're about change, not absolute level.

| Signal | What it measures |
|---|---|
| **CTR trend by query tier** | Is engagement stable or declining over weeks/months? Head query CTR drop is an early warning |
| **Zero-result rate trend** | Is catalog coverage keeping up with evolving query vocabulary? |
| **NDCG on a reference set** | Run offline eval on a locked human-judged query set on a schedule; detects silent ranking regression |
| **Clicks Residual distribution** | Are more queries accumulating negative residual (fewer clicks than expected)? Drift signal |
| **New query volume** | Fraction of queries with no historical click data — proxy for how fast vocabulary is evolving |
| **Query reformulation trend** | Rising reformulation rate = worsening first-result quality |

---

## What to Instrument

### The Search Event

Every search interaction should emit a structured event capturing:

```
{
  query_id:        unique identifier for this search request
  session_id:      groups queries in a single user session
  user_id:         (hashed/anonymised) for session reconstruction
  query_text:      raw query string
  query_timestamp: epoch ms
  result_ids:      ordered list of returned document IDs
  result_positions: [1, 2, 3, ...]
  retrieval_strategy: "bm25" | "hybrid" | "neural" | ...
  model_version:   ranking model identifier
  latency_ms:      total query latency
  zero_results:    boolean
  num_results:     count returned
}
```

### The Click Event

```
{
  query_id:        links back to the search event
  session_id:
  clicked_result_id:
  click_position:  rank of the clicked result
  click_timestamp:
  dwell_time_ms:   time until return to SERP (if measurable)
}
```

### The Session Event

Derived by joining search and click events within a session window:

```
{
  session_id:
  query_count:           total queries in session
  reformulation_count:   queries after unsatisfied prior query
  click_count:
  success_event:         boolean (purchase, save, zero reformulation after click, etc.)
  session_duration_ms:
}
```

Shopify's approach (see [[Building Smarter Search Products 3 Steps for Evaluating Search Algorithms]]) stitches these from Kafka events into "search facts" for near-real-time metric computation.

---

## Metrics Dashboard Design

A practical observability dashboard has three tiers:

**Tier 1 — Always Visible (operational health)**
- Zero-result rate (current + 7-day trend)
- Query latency P99 (current + SLA line)
- Error rate
- Indexing lag

**Tier 2 — Quality health (reviewed daily/weekly)**
- CTR by query tier (head / torso / tail, trended 30 days)
- Abandonment rate (trended)
- Query reformulation rate (trended)
- Session success rate (trended)

**Tier 3 — Deep diagnostics (on-demand or weekly)**
- Bottom-N queries by clicks residual (worst underperforming queries)
- New / zero-click query list
- NDCG on reference set (weekly scheduled run)
- Zero-result query log (full text for vocabulary analysis)

---

## Alerting

Alert on leading indicators, not lagging ones. By the time CTR drops significantly, many users have already had a bad experience.

| Alert | Trigger condition | Priority |
|---|---|---|
| Zero-result rate spike | > 2× baseline over 1 hour | P1 — likely indexing or configuration failure |
| Latency P99 breach | Sustained above SLA threshold | P1 — infrastructure issue |
| Error rate spike | > 1% over 15 min | P1 |
| CTR drop — head queries | > 10% relative drop week-over-week | P2 — quality regression |
| Indexing lag | > 2× normal for domain | P2 — freshness issue |
| Abandonment surge | > 15% relative increase | P2 — possible ranking regression |
| Zero-result rate creep | Slow upward trend over 2+ weeks | P3 — vocabulary drift, needs catalog/synonym work |

Separate **infrastructure alerts** (P1) from **quality alerts** (P2/P3). Infrastructure pages on-call; quality routes to the search team's daily review queue.

---

## Diagnostic Workflow

When a metric deviates, a structured investigation prevents chasing symptoms:

1. **Triage** — is this infrastructure (latency, errors, shard health) or quality (CTR, abandonment)?
2. **Scope** — which query tier? Which device/locale/surface? Which time window?
3. **Correlate** — did a deployment, index update, or catalog change coincide?
4. **Sample** — pull the worst-performing queries (lowest clicks residual, highest zero-result rate) for manual inspection
5. **Hypothesize** — vocabulary gap? Ranking regression? Catalog coverage? Feature drift in the ranking model?
6. **Verify** — run targeted offline eval on the affected query sample; compare model versions

The zero-result query log is often the fastest diagnostic: reading 50 zero-result queries usually reveals the vocabulary gap or catalog problem within minutes.

---

## Observability Stack Patterns

**Event pipeline**: search and click events → streaming platform (Kafka, Kinesis) → aggregate metrics store (ClickHouse, BigQuery, Druid) → dashboards (Grafana, Looker)

**Near-real-time**: aggregate over 5–15 minute windows for operational tier metrics; enables fast detection of indexing failures or misconfigured deploys

**Batch**: join session events, compute clicks residual, run NDCG on reference set — typically daily or weekly; feeds quality tier

**Log sampling**: for high-traffic systems, sample query events (e.g. 10%) for behavioral analysis while logging 100% of zero-result and error events — zero-result events are rare enough to capture fully and too valuable to sample away

---

## Common Failure Modes

**Monitoring only infrastructure.** Latency and error rate are necessary but insufficient. A system can be fast and reliable while serving bad results. Add behavioral metrics from day one.

**No baseline.** A CTR of 34% means nothing without knowing last week was 36% or last year was 28%. All quality metrics need a baseline and a trend; absolute values are rarely actionable alone.

**Head query bias.** Monitoring average CTR over all queries is dominated by head queries. Tail queries (60–80% of query volume) have lower baseline CTR and will suppress signals from rare-query degradation. Always segment by query tier.

**Conflating zero-click with failure.** Zero-click rate is not the same as abandonment. Informational queries answered in snippets are zero-click successes. Segment by query type or measure reformulation-after-zero-click as the failure signal.

**Alert fatigue from noisy metrics.** CTR and abandonment have high day-of-week seasonality. Alerting on raw week-over-week drops without seasonality adjustment generates constant false positives. Use rolling baselines or day-of-week normalization.

**No zero-result vocabulary process.** Teams build alerting for zero-result rate but have no workflow to act on it. The metric is only useful if someone regularly reviews the zero-result query log and routes it to synonym/catalog work.

**Model version tracking gaps.** A CTR drop is hard to diagnose if you can't correlate it to a specific model version, index snapshot, or config change. Tag every event with the model version and configuration hash.

---

## Relationship to [[Search Quality Assurance]]

SQA and observability are complementary layers of the same quality feedback loop:

```
Observability (production)
    ↓ signals quality degradation or regression
SQA offline eval
    ↓ confirms and quantifies the issue on labeled data
Fix deployed
    ↓
Observability confirms improvement in production
```

Observability without SQA: you know something is wrong but can't measure it precisely.  
SQA without observability: you evaluate carefully but never know what production is actually doing.

---

## Related

- [[Search Quality Assurance]] — offline evaluation; the investigation tool triggered by observability signals
- [[A-B Testing for Search]] — controlled experiments; complement to passive observability
- [[Click Signals]] — the core behavioral signal layer
- [[Clicks Residual]] — query-level success metric; the key quality observability signal
- [[Zero Results]] — the clearest failure signal in the behavioral plane
- [[Intent Drift]] — the quality problem observability is designed to detect early
- [[Understaffed Search Team]] — prioritisation: zero-result monitoring and bad-query review as minimum viable observability
