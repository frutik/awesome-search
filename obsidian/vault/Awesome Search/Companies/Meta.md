---
type: company
industry: technology / social media / AI research
products:
  - Facebook / Instagram / WhatsApp
  - FAISS (open-source)
  - Llama (open-source LLM family)
  - PyTorch
category: technology-provider
search_domain: large-scale retrieval research and open-source tooling
---

# Meta

## Search and Retrieval Contributions

Meta (formerly Facebook) is one of the most prolific contributors to open-source retrieval infrastructure and research. Their work spans approximate nearest neighbor search, dense retrieval, and most recently agentic retrieval.

### Open-Source Tools
- **FAISS** (Facebook AI Similarity Search) — the dominant library for approximate nearest neighbor search. Underpins most dense retrieval systems globally. Implements IVF, HNSW, PQ, and hybrid indexes with GPU support
- **PyTorch** — the standard ML framework; underpins most embedding model training

### Research
- **[[SIRA]]** (Superintelligent Retrieval Agent) — argues that retrieval quality is a query formulation problem, not an architecture problem. A single LLM-generated BM25 query outperforms complex agentic retrieval pipelines on BEIR benchmarks (Recall@10, NDCG@10)
- Dense Passage Retrieval (DPR) — early influential bi-encoder retrieval model (not in this vault but foundational to the field)

## Why SIRA Matters

SIRA is a direct challenge to the prevailing agentic-RAG orthodoxy. Meta's position: the search community has over-invested in retrieval architecture complexity (multi-step loops, vector ensembles, agentic pipelines) when the real bottleneck is the quality of the query itself. See [[SIRA]] for full analysis.

## People

- Zeyu Yang, Qi Ma, Jason Chen, Anshumali Shrivastava — SIRA paper authors (Meta / Rice University)

## Articles

- [[Superintelligent Retrieval Agent SIRA]]

## Concepts

[[SIRA]] · [[Dense Vector Retrieval]] · [[Agentic Search]] · [[BM25]]
