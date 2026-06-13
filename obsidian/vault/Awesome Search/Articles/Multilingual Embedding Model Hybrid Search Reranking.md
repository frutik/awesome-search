---
created: 2026-05-15
title: "Multilingual Embedding Model: Hybrid Search Reranking"
source: "https://www.elastic.co/search-labs/blog/multilingual-embedding-model-hybrid-search-reranking"
author: "[[Quynh Nguyen]]"
published: 2025-10-30
tags: [multilingual, embeddings, hybrid-search, reranking, elasticsearch, E5, company-blog]
---

# Multilingual Embedding Model: Hybrid Search Reranking

**Author:** [[Quynh Nguyen]] (Elastic)

## Setup

Uses Elastic's pre-trained **E5 multilingual model** (`.multilingual-e5-small_linux-x86_64_search`) on a COCO captions dataset in multiple languages (English, German, Italian, Vietnamese).

## Cross-Lingual Retrieval

Searching for "kitty" in English returns results in German, Italian, Vietnamese — the model represents meaning in a **shared semantic space**. 

Notably, searching in Korean (고양이) returns German and Vietnamese results even though no Korean documents are indexed. The model bridges vocabulary gaps across languages automatically.

## Hybrid Search + Reranking Pipeline

When top-1 results from pure vector search aren't precise enough (e.g., "What color is the cat?" in Vietnamese), adding RRF hybrid + Cohere reranking improves precision:

```json
"retriever": {
  "text_similarity_reranker": {
    "retriever": {
      "rrf": {
        "retrievers": [{"knn": {...}}],
        "rank_window_size": 100
      }
    },
    "field": "description",
    "inference_id": "cohere_rerank",
    "inference_text": "con mèo màu gì?"
  }
}
```

**Cohere rerank-v3.5** used as cross-encoder reranker.

## Unexpected Win

Vector search found a "brown striped cat" document even though the English reference caption missed that detail — demonstrated that cross-lingual vector search can *correct* dataset label omissions.

## Related Concepts

- [[Hybrid Search]]
- [[Dense Vector Retrieval]]
- [[Semantic Search]]
