---
title: "Improve your RAG applications by moving to Task-aware Embeddings"
source: "https://medium.com/@gal.peretz/improve-your-rag-applications-by-moving-to-task-aware-embeddings-09ebee62616f"
author:
  - "[[Gal Peretz]]"
published: 2024-02-02
created: 2026-05-15
description: "Task-aware embeddings use instruction-following LLMs to encode both task and query, making query embeddings dynamic while keeping passage embeddings static — enabling a single model for multiple tasks."
tags:
  - clippings
---
# Improve your RAG applications by moving to Task-aware Embeddings

## The problem with task-specific embeddings

Traditional task-specific models are narrow and brittle:
- Limited generalization across diverse tasks
- Multiple models needed for varied queries
- Scalability and management complexity
- Costly to adapt to new tasks

## Task-aware embeddings

Recent approach: LLMs jointly encode both the **task** and the **query**.

Key innovation: **passage embeddings remain static** in the vector database, but **query embeddings adjust dynamically** based on the specific task at inference time.

Example: customer support queries embed differently when searching by topic vs. detecting duplicate questions.

## Implementation (intfloat/e5-mistral-7b-instruct)

```python
# Passage encoding (static)
from transformers import AutoTokenizer, AutoModel
model = AutoModel.from_pretrained('intfloat/e5-mistral-7b-instruct')

# Query encoding (task-aware)
def get_detailed_instruct(task_description: str, query: str) -> str:
    return f'Instruct: {task_description}\nQuery: {query}'

task = 'Given a web search query, retrieve relevant passages that answer the query'
query = get_detailed_instruct(task, 'how much protein should a female eat')
```

Use `last_token_pool` to extract the last token representation, then normalize.

## Benefits

A single model across various tasks — dynamic embeddings without indexing documents with numerous vectors. Potential future direction for unified, instruction-aware embedding systems.


## Related Concepts

- [[Task-Aware Embeddings]]
- [[Dense Embeddings]]
- [[Embeddings]]
- [[RAG]]
- [[Asymmetric Semantic Search]]
- [[Embedding Fine-tuning]]

## People

- [[Gal Peretz]]
