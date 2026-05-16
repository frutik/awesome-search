---
type: person
tags: [person, developer-advocacy, cross-encoders, colbert, vector-search]
name: Michael Ryaboy
affiliation: KDB.AI
role: Developer Advocate
articles: []
key_contributions: [cross-encoders-colbert-explainer, vector-search-reranking]
---

# Michael Ryaboy

Developer Advocate at **KDB.AI**. Author of accessible explanations of advanced neural reranking methods — particularly cross-encoders and ColBERT — for practitioners moving beyond bi-encoder dense retrieval.

---

## Key Contributions

- **Cross-Encoders and ColBERT**: Wrote practitioner-oriented explainers covering:
  - The quality gap between bi-encoders (fast, pre-computed) and cross-encoders (slow, query-aware, more accurate)
  - **ColBERT** — late interaction model that approximates cross-encoder quality at bi-encoder latency by storing per-token embeddings and computing MaxSim at query time
  - When each architecture is appropriate given latency budget and corpus size

---

## Articles

- [[Cross-Encoders ColBERT and LLM-Based Re-Rankers]]

## Related Concepts

- [[Cross-Encoders]]
- [[ColBERT]]
- [[Embeddings]]

## Related Topics

- [[Two-Stage Ranking]]
- [[Conversational and Agentic Search]]
