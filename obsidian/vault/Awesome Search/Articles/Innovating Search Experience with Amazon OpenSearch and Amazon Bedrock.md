---
title: "Innovating Search Experience with Amazon OpenSearch and Amazon Bedrock"
source: "https://bigdataboutique.com/blog/innovating-search-experience-with-amazon-opensearch-and-amazon-bedrock-d045bc"
author: ["Big Data Boutique"]
tags:
  - clippings
  - opensearch
  - aws
  - bedrock
  - rag
  - semantic-search
  - company-blog
concepts:
  - RAG
  - Dense Vector Retrieval
  - Semantic Search
  - Hybrid Search
created: 2026-05-15
---

# Innovating Search Experience with Amazon OpenSearch and Amazon Bedrock

**Source**: https://bigdataboutique.com/blog/innovating-search-experience-with-amazon-opensearch-and-amazon-bedrock-d045bc  
**Author**: Big Data Boutique

## Summary

A practical guide to building production semantic search and RAG using Amazon OpenSearch Service for vector storage and Amazon Bedrock (Claude, Titan) for embeddings and generation.

## Architecture Overview

```
User Query
    ↓
Amazon Bedrock (Titan Embeddings) → query_vector
    ↓
Amazon OpenSearch Service (kNN index) → top-k chunks
    ↓
Amazon Bedrock (Claude) → generated answer
    ↓
User Response
```

This is a fully AWS-native [[RAG]] stack.

## OpenSearch Vector Index Setup

```python
import boto3
from opensearchpy import OpenSearch

# Create index with vector field
index_body = {
    "settings": {
        "index.knn": True
    },
    "mappings": {
        "properties": {
            "embedding": {
                "type": "knn_vector",
                "dimension": 1536,
                "method": {
                    "name": "hnsw",
                    "space_type": "l2",
                    "engine": "nmslib"
                }
            },
            "content": {"type": "text"},
            "source": {"type": "keyword"}
        }
    }
}
```

## Bedrock Titan Embeddings

```python
bedrock = boto3.client("bedrock-runtime")

def embed(text):
    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=json.dumps({"inputText": text})
    )
    return json.loads(response["body"].read())["embedding"]
```

## Hybrid Search in OpenSearch

OpenSearch supports BM25 + kNN hybrid:
```json
{
  "query": {
    "hybrid": {
      "queries": [
        {"match": {"content": "query text"}},
        {"knn": {"embedding": {"vector": [...], "k": 10}}}
      ]
    }
  },
  "search_pipeline": {
    "phase_results_processors": [{
      "normalization-processor": {
        "combination": {"technique": "rrf"}
      }
    }]
  }
}
```

## RAG Generation with Claude

```python
def rag_answer(query, retrieved_chunks):
    context = "\n\n".join([c["content"] for c in retrieved_chunks])
    
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps({
            "messages": [{
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}"
            }]
        })
    )
    return json.loads(response["body"].read())["content"][0]["text"]
```

## Production Considerations

1. **Chunking strategy**: split documents before embedding (see [[Text Chunking]])
2. **Embedding cost**: Titan at $0.0001/1K tokens — budget for large corpora
3. **Index warm-up**: OpenSearch kNN needs warm-up after restart
4. **Metadata filtering**: OpenSearch supports pre-filter on non-vector fields

## Related Articles

- [[Migrating to Elasticsearch with Dense Vector for Carousell Spotlight]] — similar migration case study
- [[Chunking Strategies for LLM Applications]] — chunking for RAG
- [[Nearest Neighbor Indexes for Similarity Search]] — HNSW infrastructure

## Related Concepts

- [[RAG]] — primary pattern
- [[Dense Vector Retrieval]] — storage and retrieval
- [[Semantic Search]] — enabled capability
- [[Hybrid Search]] — BM25 + kNN
- [[Text Chunking]] — document preparation
- [[Agentic Search]] — potential extension with Bedrock agents
