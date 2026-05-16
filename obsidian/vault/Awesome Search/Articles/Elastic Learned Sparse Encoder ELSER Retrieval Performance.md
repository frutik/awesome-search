---
title: "Improving Information Retrieval in the Elastic Stack: Introducing ELSER"
source: "https://www.elastic.co/search-labs/blog/elastic-learned-sparse-encoder-elser-retrieval-performance"
author: ["Elastic"]
tags:
  - clippings
  - elser
  - splade
  - elasticsearch
  - sparse-retrieval
concepts:
  - ELSER
  - SPLADE
  - Sparse Vector Retrieval
  - Retrieval Pipeline
created: 2026-05-15
---

# Improving Information Retrieval in the Elastic Stack: Introducing ELSER

**Source**: https://www.elastic.co/search-labs/blog/elastic-learned-sparse-encoder-elser-retrieval-performance  
**Publisher**: Elastic

## Summary

Elastic announces [[ELSER]] (Elastic Learned Sparse Encoder), their production-grade sparse retrieval model built on [[SPLADE]] principles. Reports 17% NDCG@10 improvement over BM25 and describes the distillation-based training approach.

## What is ELSER?

ELSER is Elastic's version of learned sparse retrieval, optimized for the Elasticsearch inverted index infrastructure:
- Based on SPLADE architecture
- 100M parameter BERT-based model
- Produces vocabulary-space sparse vectors (30,522 BERT vocabulary dimensions)
- Deployed natively in Elasticsearch/OpenSearch

## Training Methodology: Knowledge Distillation

ELSER was trained using a powerful **ensemble teacher**:

```
Teacher: MiniLM (fast bi-encoder) + MonoT5-3B (large cross-encoder reranker)
    ↓
Generate high-quality labels for MS MARCO + domain data
    ↓
Student: 100M parameter BERT MLM model
    ↓
ELSER: compressed, fast sparse encoder
```

The teacher ensemble captures complementary signals:
- MiniLM: semantic similarity
- MonoT5-3B: nuanced relevance judgment

This is an example of [[Retrieval Pipeline]] distillation — compressing a multi-stage pipeline into a single model.

## Performance Results

On MS MARCO dev set (NDCG@10):
| Model | NDCG@10 | Notes |
|-------|---------|-------|
| BM25 | 0.228 | Lexical baseline |
| **ELSER v1** | **0.267** | **+17% over BM25** |
| Dense bi-encoder | 0.253 | Semantic only |
| Hybrid BM25+Dense | 0.271 | Best combination |

ELSER outperforms both BM25 and standard dense bi-encoders individually, approaching hybrid quality with a single model.

## ELSER v2 Improvements

ELSER v2 brings:
- Better OOD (out-of-distribution) performance
- Faster inference
- Lower memory footprint
- Improved handling of numeric/code content

## Integration in Elasticsearch

```python
# Elasticsearch 8.x API
GET /my_index/_search
{
  "query": {
    "text_expansion": {
      "ml.tokens": {
        "model_id": ".elser_model_2_linux-x86_64",
        "model_text": "find documents about machine learning"
      }
    }
  }
}
```

Elasticsearch stores ELSER sparse vectors natively in its inverted index — no separate vector database required.

## ELSER as Hybrid Component

For best results, Elastic recommends ELSER + BM25 hybrid:
```json
{
  "query": {
    "bool": {
      "should": [
        {"match": {"content": "query"}},  // BM25
        {"text_expansion": {"ml.tokens": {"model_id": ".elser_model_2", "model_text": "query"}}}  // ELSER
      ]
    }
  }
}
```

## Related Articles

- [[SPLADE for Sparse Vector Search Explained]] — SPLADE foundations
- [[SPLADE - Sparse Bi-Encoder BERT Model for First-Stage Ranking]] — original research
- [[Hybrid Search SPLADE Sparse Encoder]] — hybrid implementation
- [[Awesome Search/Articles/Distilling Retrieval Pipelines to a Single Embedding Model]] — related distillation concept

## Related Concepts

- [[ELSER]] — primary topic
- [[SPLADE]] — architecture basis
- [[Sparse Vector Retrieval]] — category
- [[Retrieval Pipeline]] — distillation training
- [[Hybrid Search]] — recommended deployment
- [[Embedding Fine-tuning]] — distillation is a form of training
