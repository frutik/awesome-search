---
title: "Understanding BERT and Search Relevance"
aliases: ["BERT Search Relevance", "OSC BERT", "Max Irwin BERT"]
tags:
  - clippings
  - search
  - bert
  - dense-retrieval
  - embeddings
source: "https://opensourceconnections.com/blog/2019/11/05/understanding-bert-and-search-relevance/"
author: "Max Irwin"
created: 2026-05-15
concepts:
  - Dense Vector Retrieval
  - Bi-Encoder
  - Cross-Encoder
  - Embedding Fine-tuning
---

# Understanding BERT and Search Relevance

**Source:** https://opensourceconnections.com/blog/2019/11/05/understanding-bert-and-search-relevance/
**Author:** Max Irwin

## Summary

An early practical analysis of BERT for search relevance (2019), examining how BERT's contextualized token embeddings work, what they cost in a search context, and where they add value.

### BERT Basics for Search
BERT (Bidirectional Encoder Representations from Transformers) produces **contextualized embeddings**: each token's representation depends on the surrounding tokens.

For search relevance, the key output is the [CLS] token embedding — a 768-dimensional vector representing the meaning of the entire input (query or document).

### The Storage Challenge
BERT embeddings for search at scale:
- Each document: 768 × 4 bytes = ~3KB for a single [CLS] vector
- 1M documents: ~3GB for just the CLS vectors
- If storing per-token embeddings (for ColBERT-style late interaction): 1000x more
- **Storage is ~1000x larger than BM25 inverted index** for equivalent coverage

This was a significant practical barrier in 2019; less so today with vector DBs and quantization.

### The "Black Box" Challenge
Unlike BM25 (where you can see which term matched and why), BERT similarity is opaque:
- Two documents with no lexical overlap can score identically to one with exact matches
- Explaining why a result ranked highly requires interpretability techniques (LIME, SHAP, attention visualization)
- This complicates debugging and user trust

### BERT Use Cases in Search (2019 perspective)

**Good fit:**
- Semantic query understanding (query type classification)
- Cross-encoder reranking of a small candidate set (< 1000 docs)
- Entity extraction from queries

**Poor fit:**
- First-stage retrieval over millions of documents (too slow without ANN index)
- Real-time query embedding with latency < 10ms (BERT was ~100ms on CPU in 2019)

### Progress Since 2019
- Bi-encoders + FAISS/HNSW enable BERT-based first-stage retrieval
- Quantization reduces storage 4-8x
- Distilled models (MiniLM, DistilBERT) cut latency 5-10x
- ColBERT demonstrated that per-token late interaction improves accuracy

## Key Concepts
- **CLS vector** — 768-dim BERT embedding representing full sequence
- **Storage overhead** — BERT embeddings ~1000x larger than inverted index
- **Black box opacity** — no lexical explanation for BERT similarity
- **Cross-encoder for reranking** — practical early use case for BERT in search
- **Bi-encoder + ANN** — the solution to first-stage retrieval latency

## Related Concepts
- [[Dense Vector Retrieval]]
- [[Bi-Encoder]]
- [[Cross-Encoder]]
- [[Embedding Fine-tuning]]
- [[ColBERT]]
- [[Late Interaction]]

## Related Articles
- [[What is a Relevant Search Result]]
- [[Sparse, Dense, and Attentive Representations for Text Retrieval]]
- [[ColBERT - Efficient and Effective Passage Search]]

## People
- [[Doug Turnbull]]
- [[Omar Khattab]]
