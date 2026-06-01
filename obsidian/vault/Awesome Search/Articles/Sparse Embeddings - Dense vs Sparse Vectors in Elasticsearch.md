---
type: article
tags: [article, sparse-vectors, elser, splade, elasticsearch, semantic-search, company-blog]
source: "https://www.elastic.co/search-labs/blog/sparse-vector-embedding"
author: [Dai Sugimori]
company: [Elastic]
concepts: [Sparse Vector Retrieval, SPLADE, ELSER, Semantic Search, Hybrid Search]
topics: []
---

# Sparse Embeddings: Dense vs Sparse Vectors in Elasticsearch

**[[Dai Sugimori]]** (Elastic) explains sparse vectors, compares them to dense vectors, and covers Elasticsearch 8.17's new support for uploading custom sparse models from Hugging Face.

## Dense vs Sparse

| Dimension | Dense | Sparse |
|-----------|-------|--------|
| Representation | Fixed-length float array (all nonzero) | Key-value pairs (mostly zero) |
| Interpretability | Low — dimensions have no clear meaning | High — keys are often meaningful tokens |
| Zero-shot performance | Needs domain-specific fine-tuning | Works well out of the box (ELSER) |
| Resource efficiency | Higher memory/storage | Lower (only nonzero values stored) |
| Infrastructure | kNN/ANN index | Lucene inverted index |

## Sparse Vectors in Elasticsearch

- Legacy: `rank_features` query
- Current: `sparse_vector` query + field type (ES 8.16+)
- ES 8.17+: upload any Hugging Face sparse model (BERT/RoBERTa/XLM-RoBERTa tokenization) via Eland CLI

## Why Use Sparse Over Dense?

- **Zero-shot generalization**: Works in new domains without fine-tuning
- **Interpretability**: You can see which tokens drove the match
- **Lucene integration**: No separate vector infrastructure — uses the existing inverted index

## Example

SPLADE v3-distilbert embeds "Elasticsearch provides semantic search" as `{software: 3.26, web: 2.07, browser: 1.90, ...}` — concepts not in the original text but semantically related.

## Key Recommendation

Use sparse vectors (ELSER or SPLADE) when you can't fine-tune a dense model for your domain. Combine with dense vectors in hybrid search via RRF for best precision.

## Related Concepts

[[Sparse Vector Retrieval]] · [[SPLADE]] · [[ELSER]] · [[Hybrid Search]] · [[Semantic Search]]
