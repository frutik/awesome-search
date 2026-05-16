---
type: person
tags: [person, ml-engineering, ranking, two-stage-ranking]
name: Jaideep Ray
affiliation: unknown
role: Sr. Staff ML Engineer
articles: []
key_contributions: [multi-stage-ranking, two-stage-retrieval-reranking]
---

# Jaideep Ray

Sr. Staff ML Engineer. Author of writing on **multi-stage ranking** in search systems — the architecture of separating a fast, high-recall retrieval stage (BM25, ANN) from a slower, high-precision reranking stage (cross-encoders, LLM-based scoring).

---

## Key Contributions

- **Multi-Stage Ranking**: Articulated the engineering tradeoffs in two-stage pipelines — why retrieve-then-rerank outperforms either stage alone, how to set the retrieval recall budget (top-k candidates passed to reranker), and the latency/quality Pareto curve for each stage.

---

## Articles

- [[Multi-Stage Ranking]]

## Related Topics

- [[Two-Stage Ranking]]
- [[Learning to Rank]]
- [[Cross-Encoders]]
