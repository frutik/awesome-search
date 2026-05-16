---
type: topic
aliases: ["search economics", "search ROI", "cost of search"]
tags: [topic, economics, strategy, search-team]
related_concepts: ["[[Search Relevance]]", "[[Learning to Rank]]", "[[Search Quality]]"]
related_topics: ["[[Managing a Search Team]]", "[[A-B Testing for Search]]"]
articles: ["[[The Economics of Search]]"]
created: 2026-05-16
---

# Economics of Search

How to think about search as a business investment: where money goes, how to justify spend, and how to optimize the cost/value ratio.

---

## Why Search Is Expensive

Search is not a feature you build once. It requires:

- **Infrastructure**: index storage, query serving, ML inference at query time
- **Data pipelines**: crawl, ingest, transform, re-index continuously
- **People**: relevance engineers, ML engineers, data scientists, PMs — all specialized
- **Tooling**: annotation platforms, A/B frameworks, offline eval harnesses
- **Iteration**: relevance is never done; every product change can break search

The cost is ongoing and often underestimated because search looks simple from the outside.

---

## Where the Money Goes

| Cost Center | What Drives It | Optimization Lever |
|---|---|---|
| Compute (serving) | QPS × latency budget × replica count | Caching, index pruning, model distillation |
| Compute (ML inference) | Model size × query volume | Two-stage ranking, lighter re-rankers |
| Indexing pipeline | Document count × update frequency | Incremental updates, tiered freshness |
| Vector search | Embedding size × corpus size | Quantization (BBQ/INT8), HNSW tuning |
| Annotation / eval | Label throughput × iteration cadence | Implicit signals, active learning |
| Engineering headcount | Team size × seniority | Platform leverage, shared tooling |

---

## How to Justify Search Investment

### Revenue Attribution
The most direct argument: search drives conversion. Calculate:
- **Click-through lift** from relevance improvements
- **Add-to-cart / purchase rate** on search vs. browse sessions
- **Zero-results rate** reduction → recovered revenue
- **Session abandonment** reduction tied to search quality

A/B tests that show +2% conversion on 30% of sessions that touch search translate directly to revenue.

### Cost Avoidance
- Better recall → fewer support tickets ("I can't find X")
- Faster search → lower infrastructure bill (latency SLAs constrain replica count)
- Better tooling → fewer engineer-hours per relevance fix

### Strategic Value
- Search quality is a **retention lever** — users leave products where search fails
- Enterprise B2B: poor search = lost deal, not just lost session
- Search as competitive moat when product catalog is similar across competitors

---

## Common Pitfalls

**Underinvesting until it breaks.** Teams often treat search as infrastructure until a competitor's better search drives churn, then scramble.

**Measuring the wrong thing.** Optimizing for clicks (CTR) instead of outcomes (purchase, task completion) can improve metrics while harming the business.

**Ignoring tail queries.** Head queries (top 1%) look great because they get tuned. Long tail (60-80% of volume) determines real user experience.

**Overspending on infrastructure, underspending on relevance.** Adding hardware is visible; improving recall on edge cases is invisible until you measure it.

**Big bang rewrites.** Ground-up search rebuilds take 12-18 months and often fail to beat the system they replace. Incremental beats wholesale.

---

## ROI Framework for Search Projects

Before committing to a project, estimate:

1. **Baseline**: current metric value (conversion rate, zero-results %, P@1)
2. **Lift estimate**: from similar projects or early experiments
3. **Affected traffic**: what % of queries / sessions does this touch
4. **Revenue impact**: lift × affected sessions × avg order value
5. **Cost**: engineering months × loaded cost + infra delta
6. **Payback period**: cost ÷ monthly revenue impact

If payback > 12 months, the project needs a stronger case or scope reduction.

---

## Cost Optimization Without Sacrificing Quality

- **Two-stage ranking**: cheap first-stage retrieval (BM25 / ANN) + expensive re-ranker only on top-N candidates
- **Query result caching**: cache results for repeated head queries; invalidate on index update
- **Model distillation**: train a smaller model to mimic a larger one; 10× cheaper inference at 95% quality
- **Embedding quantization**: INT8/BBQ reduces vector storage and lookup cost with minimal recall loss (see [[Elastic]] BBQ)
- **Tiered freshness**: real-time indexing only for high-traffic documents; batch for long tail

---

## Related

- [[Managing a Search Team]] — staffing and org decisions affect economics directly
- [[A-B Testing for Search]] — measuring ROI requires a working experiment framework
- [[Results Merchandising]] — merchandising is the business layer above pure relevance
- [[Learning to Rank]] — LTR projects have high upfront cost but compound over time
