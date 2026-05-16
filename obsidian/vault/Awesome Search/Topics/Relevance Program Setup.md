---
type: topic
tags: [topic, relevance, evaluation, program-management, judgment-collection]
related_concepts: [NDCG, MRR, Query Sampling, Clicks Residual]
related_topics: [Search Quality Assurance, A-B Testing for Search, Managing a Search Team, Hiring for Search]
articles: []
companies: [OpenSource Connections]
people: [Doug Turnbull]
---

# Relevance Program Setup

A relevance program is the organizational and operational infrastructure that makes search quality measurable, reproducible, and improvable over time. Without it, teams ship changes based on intuition, break relevance silently, and have no shared definition of "better."

This topic covers how to stand one up end-to-end.

---

## Why Programs Fail Without Structure

- **Relevance by anecdote**: One engineer's pet query drives decisions; silent regressions go undetected.
- **Metric worship**: Teams optimize NDCG without asking whether the judgment set reflects real user needs.
- **One-shot evaluation**: A test done once for a launch, never refreshed; the world moves on, the test set doesn't.
- **Human-only feedback loop**: No connection between offline metrics and online outcomes.

---

## The Four Pillars

### 1. Query Triage

Not all queries are equal. Before building a judgment set, understand your query distribution:

- **Head queries** (top 1–5% by volume): ~60–80% of traffic; small improvements have large impact; already have click data.
- **Torso queries** (next 15–20%): Moderate volume; reasonable training signal; often neglected.
- **Tail queries** (long tail): Each rare, but cumulatively significant; no click signal; hardest to judge.

Use [[Query Sampling]] — PPS by query frequency for head/torso; stratified or random for tail. Refresh the sample quarterly or when query distribution shifts.

### 2. Judgment Collection

**Explicit judgments** (human raters):
- Define a graded scale (0–3 or 0–4): Perfect / Good / Fair / Bad / Irrelevant
- Write clear guidelines with worked examples for your domain
- Use multiple raters per query-doc pair; compute Cohen's Kappa to measure agreement
- Budget: ~200–500 judgments/day per rater; plan for ~2,000–10,000 judgments for a meaningful offline set

**Implicit signals** (click/behavioral data):
- Clicks are noisy but cheap; use as supplement, not replacement
- Position-debias clicks before using as labels (see [[Clicks Residual]])
- Dwell time, add-to-cart, purchase — domain-specific stronger signals

**LLM-assisted judgment** (emerging):
- Use GPT-4 / Claude to generate draft judgments; human raters review edge cases
- ~3–5× cheaper for initial coverage; calibrate against human judgments before trusting
- Risk: LLM shares the same surface-form biases as embedding models

### 3. Metric Selection and Baseline

Choose 1–2 primary offline metrics before collecting judgments, not after:
- **[[NDCG]]@10** — standard for graded relevance; good for web/e-commerce
- **[[MRR]]** — good when one right answer exists (navigational, factual)
- **ERR** — position-aware; models users who stop after finding an answer

Set a baseline with your current system **before** any changes. Every experiment is measured as delta from baseline.

Key rule: **one primary metric, one guardrail**. The guardrail (e.g., tail query coverage) prevents optimizing the head while regressing the tail.

### 4. Launch Review Process

Establish a gate before any relevance change ships:

```
Change proposed
    │
    ├── Offline eval: delta NDCG vs baseline?
    │       └── < threshold → reject or iterate
    │
    ├── Regression check: any query-type buckets degraded?
    │       └── degraded → fix or escalate
    │
    └── A/B test (if offline passes): online metrics confirm?
            └── conflicting → investigate before shipping
```

**Tooling**: [[Quepid]] (judgment management + metric calculation), LTR plugins for Elasticsearch/Solr, RRE (Rated Ranking Evaluator) for CI/CD integration.

---

## Cadence

| Activity | Frequency |
|----------|-----------|
| Metric dashboard review | Weekly |
| New judgment collection cycle | Quarterly |
| Query sample refresh | Quarterly or on distribution shift |
| Full offline baseline re-run | Per major model change |
| A/B test for significant changes | Per launch |

---

## Connecting Offline to Online

The hardest part of a relevance program is closing the loop between offline metrics and user outcomes.

**What to track**:
- Does NDCG improvement correlate with lower reformulation rate?
- Does MRR improvement correlate with session length?
- Which query types drive online metric movement?

If offline and online metrics chronically disagree, the judgment set is stale, the metric is wrong for your user intent, or you have severe position bias in your signals.

---

## Organizational Requirements

A relevance program needs:
- **An owner**: Relevance PM or senior engineer who guards the process
- **Annotation capacity**: In-house raters or a vendor; domain expertise matters (medical, legal, e-commerce differ)
- **Engineering time**: ~10–20% of search team bandwidth for eval infrastructure
- **Stakeholder buy-in**: Product and leadership must accept "metric didn't move" as a valid launch outcome

---

## Tools

| Tool | Purpose |
|------|---------|
| [[Quepid]] | Judgment management, NDCG/MRR scoring, team collaboration |
| RRE | CI/CD relevance regression for Elasticsearch/Solr |
| Elasticsearch Learning to Rank plugin | LTR model training + serving |
| Custom notebooks | Exploratory analysis, metric visualization |

---

## Further Reading

- [[Search Quality Assurance]] — metrics taxonomy and evaluation modes
- [[A-B Testing for Search]] — online experimentation layer
- [[Managing a Search Team]] — relevance program as organizational practice
- [[OpenSource Connections]] — Doug Turnbull's consulting practice; Quepid tool
- [[Doug Turnbull]] — author of *Relevant Search*; originator of many of these practices
