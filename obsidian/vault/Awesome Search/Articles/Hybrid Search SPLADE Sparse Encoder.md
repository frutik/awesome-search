---
title: "Hybrid Search: SPLADE Sparse Encoder"
source: "https://medium.com/@sowmiyajaganathan/hybrid-search-splade-sparse-encoder-neural-retrieval-models-d092e5f46913"
author: ["Sowmiya Jaganathan"]
tags:
  - clippings
  - splade
  - hybrid-search
  - sparse-retrieval
  - neural-retrieval
  - medium
concepts:
  - SPLADE
  - Hybrid Search
  - Sparse Vector Retrieval
created: 2026-05-15
---

# Hybrid Search: SPLADE Sparse Encoder

**Source**: https://medium.com/@sowmiyajaganathan/hybrid-search-splade-sparse-encoder-neural-retrieval-models-d092e5f46913  
**Author**: Sowmiya Jaganathan

## Summary

Explains how [[SPLADE]] works as a sparse encoder for hybrid search, contrasting it with BM25 and dense bi-encoders, with practical implementation guidance for combining SPLADE with dense retrieval.

## Why SPLADE for Hybrid Search?

Traditional hybrid search uses BM25 (sparse) + bi-encoder (dense). SPLADE offers a better sparse component:

| Aspect | BM25 | SPLADE | Dense Bi-Encoder |
|--------|------|--------|-----------------|
| Term expansion | No | Yes (learned) | N/A |
| Semantic understanding | No | Partial | Yes |
| Storage | Inverted index | Inverted index | Vector index |
| Speed | Very fast | Fast | Medium |
| Interpretability | High | Medium | Low |

SPLADE bridges BM25 and bi-encoders: it uses an inverted index like BM25 but learns semantic term weights like a neural model.

## SPLADE in Hybrid Pipeline

```python
from transformers import AutoTokenizer, AutoModelForMaskedLM
import torch

def splade_encode(text, model, tokenizer, max_length=512):
    tokens = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_length)
    
    with torch.no_grad():
        output = model(**tokens)
    
    # MLM logits → log(1 + ReLU(x)) → MaxPool over sequence
    logits = output.logits  # shape: [1, seq_len, vocab_size]
    activated = torch.log(1 + torch.relu(logits))
    sparse_vec = torch.max(activated, dim=1).values.squeeze()  # [vocab_size]
    
    # Convert to sparse dict of {token_id: weight}
    non_zero = sparse_vec.nonzero().squeeze(-1).tolist()
    return {tokenizer.decode([tok_id]): sparse_vec[tok_id].item() 
            for tok_id in non_zero}
```

## Hybrid Fusion with RRF

```python
def reciprocal_rank_fusion(splade_results, dense_results, k=60):
    fused_scores = {}
    
    for rank, (doc_id, _) in enumerate(splade_results):
        fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1/(k + rank + 1)
    
    for rank, (doc_id, _) in enumerate(dense_results):
        fused_scores[doc_id] = fused_scores.get(doc_id, 0) + 1/(k + rank + 1)
    
    return sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
```

## When SPLADE Hybrid Outperforms Pure Dense

SPLADE hybrid is particularly effective when:
- Queries contain rare domain terms (product codes, technical jargon)
- Exact phrase matching matters
- Documents have specific named entities (people, companies, places)
- Query vocabulary doesn't overlap with how documents are written (vocabulary mismatch)

## Comparison with Standard BM25+Dense Hybrid

SPLADE+Dense typically outperforms BM25+Dense by:
- 5–10% NDCG improvement on MS MARCO
- Larger gains on domain-specific corpora with specialized vocabulary

The improvement comes from SPLADE's term expansion: the sparse component now matches semantically related terms, reducing vocabulary mismatch.

## Related Articles

- [[SPLADE for Sparse Vector Search Explained]] — deeper SPLADE theory
- [[SPLADE - Sparse Bi-Encoder BERT Model for First-Stage Ranking]] — original NAVER paper
- [[Elastic Learned Sparse Encoder ELSER Retrieval Performance]] — production SPLADE

## Related Concepts

- [[SPLADE]] — core model
- [[Hybrid Search]] — primary application
- [[Sparse Vector Retrieval]] — SPLADE's category
- [[Bi-Encoder]] — dense component of hybrid
- [[Dense Vector Retrieval]] — dense side infrastructure

## People

- [[Stéphane Clinchant]] — SPLADE co-inventor
- [[Thibault Formal]] — SPLADE co-inventor
