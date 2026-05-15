---
title: "Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex"
source: "https://blog.llamaindex.ai/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5"
author: ["LlamaIndex"]
tags:
  - clippings
  - chunking
  - rag
  - evaluation
  - llamaindex
concepts:
  - Text Chunking
  - RAG
  - Dense Vector Retrieval
created: 2026-05-15
---

# Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex

**Source**: https://blog.llamaindex.ai/evaluating-the-ideal-chunk-size-for-a-rag-system-using-llamaindex-6207e5d3fec5  
**Publisher**: LlamaIndex

## Summary

An empirical study using LlamaIndex's evaluation framework to determine the optimal chunk size for RAG systems, finding that **1024 tokens** performs best across multiple metrics.

## Methodology

The study uses LlamaIndex's built-in evaluation tools:
1. Build a RAG pipeline with varying chunk sizes: 128, 256, 512, 1024, 2048 tokens
2. Generate question-answer pairs from source documents
3. Evaluate with three metrics:
   - **Faithfulness**: Does the answer stick to retrieved context? (no hallucination)
   - **Relevancy**: Is the retrieved context relevant to the question?
   - **Response time**: Latency of the full RAG pipeline

## Key Findings

### Chunk Size vs. Quality

| Chunk Size | Faithfulness | Relevancy | Notes |
|-----------|-------------|-----------|-------|
| 128 tokens | 0.62 | 0.64 | Too small — missing context |
| 256 tokens | 0.71 | 0.73 | Still underpowered |
| 512 tokens | 0.79 | 0.80 | Good balance |
| **1024 tokens** | **0.86** | **0.85** | **Best overall** |
| 2048 tokens | 0.84 | 0.82 | Diminishing returns, slower |

### The 1024 Token Sweet Spot

Why 1024 tokens works best:
1. Enough context for the LLM to generate a faithful, grounded answer
2. Short enough that the embedding captures the chunk's topical coherence
3. Retrieval recall is high — the relevant sentence is typically within the chunk

### Faithfulness vs. Relevancy Tradeoff

Smaller chunks → higher relevancy scores (retrieved context is tightly focused) but lower faithfulness (not enough context for accurate answers).

Larger chunks → higher faithfulness potential but relevancy can suffer (irrelevant content in the chunk).

## Practical Recommendations

1. **Default starting point**: 1024 tokens
2. **Simple factual QA**: consider 512 tokens
3. **Complex multi-hop reasoning**: consider 1024–2048 tokens  
4. **Long-context models**: can experiment with larger chunks (2048+)
5. Always evaluate on *your domain* — optimal size varies by content type

## LlamaIndex Evaluation Framework

```python
from llama_index.evaluation import ResponseEvaluator, RelevancyEvaluator

# Build index with specific chunk size
service_context = ServiceContext.from_defaults(chunk_size=1024)
index = VectorStoreIndex.from_documents(docs, service_context=service_context)

# Evaluate
evaluator = ResponseEvaluator(service_context=service_context)
result = evaluator.evaluate(query=query, response=response, contexts=source_nodes)
```

## Related Articles

- [[Chunking Strategies for LLM Applications]] — strategy overview
- [[How to Chunk Text Data - A Comparative Analysis]] — different chunking approaches
- [[Improve your RAG applications by moving to Task-aware Embeddings]] — another RAG quality lever

## Related Concepts

- [[Text Chunking]] — primary topic
- [[RAG]] — system being evaluated
- [[Dense Vector Retrieval]] — indexing chunks
- [[Asymmetric Semantic Search]] — QA retrieval scenario
