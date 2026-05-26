---
title: "Search Evaluation"
aliases: ["search quality evaluation", "search quality assurance", "SQA", "IR evaluation"]
tags:
  - concept
  - search-evaluation
  - quality
---

# Search Evaluation

## Definition

Search evaluation is the systematic process of measuring how well a search system serves user information needs. It encompasses offline measurement (against static test sets), online measurement (from live user behavior), and the processes for creating, maintaining, and acting on quality signals.

## Two Axes of Evaluation

### Offline vs. Online

**Offline evaluation**: Evaluate against a fixed test set of (query, document, relevance) triples.
- Reproducible, cheap to iterate
- Requires [[Judgment Lists]] (expensive to create)
- Metrics: [[NDCG]], [[MRR]], [[Precision and Recall]]
- Risk: judgment distribution may not match production queries

**Online evaluation**: Measure user behavior on live traffic.
- Ground truth from real users
- Requires A/B testing infrastructure
- Metrics: CTR, session success, conversion rate, zero-result rate
- Risk: noisy, confounded, slow to iterate

### Session-Based vs. Query-Based

**Query-based evaluation**: Each query is an independent unit.
- Simpler, standard IR approach
- Misses multi-query sessions where intent evolves

**Session-based evaluation**: A session (sequence of queries + interactions) is the unit.
- Captures reformulation, abandonment, success
- Better model of real-world search experience
- Requires session tracking infrastructure

## Evaluation Modes Deep Dive

### Offline with Human Judgments
1. Sample queries (random, stratified, or PPS — see [[Sampling Strategies]])
2. Retrieve candidate documents per query
3. Have annotators rate relevance (0–4 scale)
4. Compute [[NDCG]] or [[MRR]] against gold judgments

**Annotation guidelines**: critical for consistent quality. Ambiguous guidelines → noisy judgments → misleading metrics.

### Offline with LLM as Judge
Use an LLM to generate relevance judgments instead of humans:
- Cost: ~10–100x cheaper than human annotation
- Quality: good for obvious cases, weaker for nuanced relevance
- See [[LLM as Judge]]

### Online: A/B Testing
- Split traffic: A = control (existing system), B = treatment (new system)
- Measure behavioral metrics over 1–2 weeks
- Requires statistical significance analysis

## Evaluation Challenges in Search

1. **Incomplete judgments**: only sampled queries judged → unjudged documents treated as irrelevant (biases against new retrieval methods)
2. **Annotation cost**: full coverage impossible; sampling design matters
3. **Freshness**: query distribution shifts over time; static test sets become stale
4. **Multi-objective tradeoff**: precision vs. recall vs. diversity vs. latency

## Recall@1000 vs. NDCG@10

These measure different things:
- **Recall@1000**: does the first retrieval stage find relevant docs at all? (pipeline quality)
- **NDCG@10**: are the top-10 results the best ones? (ranking quality)

Both are needed; a system can have high NDCG@10 but low Recall@1000 (high-quality ranking of a poor candidate set).

## Public Evaluation Datasets

Public benchmark datasets provide pre-built judgment lists for offline evaluation without the cost of in-house annotation. Especially common in e-commerce search:

| Dataset | Domain | Scale | Label type |
|---|---|---|---|
| [[Amazon ESCI Dataset]] | General e-commerce | Very large | 4-class (E/S/C/I) |
| [[WANDS Dataset]] | Home goods | ~42K pairs | 3-class |
| [[Home Depot Product Search Relevance]] | Home improvement | ~74K pairs | Continuous 1–3 |
| [[ESCI-S Dataset]] | General e-commerce | ESCI + enriched metadata | 4-class |

Use cases: benchmarking embeddings, LTR training, hybrid search evaluation, model transfer experiments.

## Related Concepts

- [[NDCG]] — primary offline ranking metric
- [[MRR]] — simpler offline metric
- [[Precision and Recall]] — foundational measures
- [[Judgment Lists]] — required for offline evaluation
- [[LLM as Judge]] — automated judgment generation
- [[Session-Based Evaluation]] — query-sequence evaluation
- [[Click Signals]] — online evaluation via behavior
- [[Diversity Metrics]] — result set quality beyond relevance

## People

- [[Daniel Tunkelang]] — "Evaluating Search" series; search evaluation philosophy
- [[James Rubinstein]] — "Measuring Search" series; statistical approaches
- [[Doug Turnbull]] — practical evaluation tooling (Quepid, NDCG variants)

- [[Click Residual - A Query Success Metric]]
- [[What is a Relevant Search Result]]
- [[Thoughts about Managing Search Teams]]
- [[Search Product Management - The Most Misunderstood Role]]
