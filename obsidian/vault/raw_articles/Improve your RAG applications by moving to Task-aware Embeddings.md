---
title: "Improve your RAG applications by moving to Task-aware Embeddings"
source: "https://medium.com/@gal.peretz/improve-your-rag-applications-by-moving-to-task-aware-embeddings-09ebee62616f"
author:
  - "[[Gal Peretz]]"
published: 2024-02-02
created: 2026-05-15
description: "Michael Ryaboy highlighted"
tags:
  - "clippings"
---
## The Purpose of Embeddings in RAG applications

Embedding models are key to enabling machines to understand human language by mapping words and phrases into a structured digital space. These models are crucial for Retrieval-Augmented Generation (RAG) applications, which enhance text generation with data retrieval, allowing for responses that are both accurate and relevant to the given context.

## What's a Task-Specific Embedding?

Task-specific embedding models are like experts in very specific types of puzzles (or tasks) but can struggle when you switch themes or need versatility.

## Disadvantages of Task-Dependent Embeddings

1. **Limited Generalization:** Task-specific models are great at handling narrow tasks but often fall short when applied to a broader range of activities.

2. **Need for Multiple Embeddings**: Answering diverse questions or covering various tasks may require indexing data with several models, increasing complexity and resource demands.

3. **Scalability Issues:** Managing and integrating multiple models for different tasks can be cumbersome.

4. **Adaptability Challenges**: These models may not easily adapt to task changes or unforeseen tasks, often requiring significant retraining or redesign.

5. **Cost Implications**: The need for specific datasets and continuous development for new tasks makes task-specific models expensive.

## Task-aware Embedding Models

A recent paper titled "[Improving Text Embeddings with Large Language Models](https://arxiv.org/pdf/2401.00368.pdf)" has unveiled an innovative method for leveraging Large Language Models (LLMs) to create embeddings by jointly encoding both the task and the query. Traditionally, queries and passages are encoded into separate, static embeddings. However, with this new approach, the query's embedding becomes dynamic, changing based on the task at hand.

## Using Task-aware Embedding Model In Practice

In this new settings the embeddings of the passages (the documents) that goes to your VectorDB are still static, however the query's embedding that we use in the online phase when we want to retrieve the right passages goes along with a specific task.

Here is how we initialize the [model](https://huggingface.co/intfloat/e5-mistral-7b-instruct) itself:

```c
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('intfloat/e5-mistral-7b-instruct')
model = AutoModel.from_pretrained('intfloat/e5-mistral-7b-instruct')
```

Now, encoding the passages is straightforward. Then you can ingest them to your VectorDB as usual. To encode the query we define a specific task:

```c
def get_detailed_instruct(task_description: str, query: str) -> str:
    return f'Instruct: {task_description}\nQuery: {query}'

task = 'Given a web search query, retrieve relevant passages that answer the query'
queries = [
    get_detailed_instruct(task, 'how much protein should a female eat'),
    get_detailed_instruct(task, 'summit define')
]
```

Now we can embed the queries with the task to tune the queries' embedding to the task, then use this dynamic queries to query your VectorDB.

## Summary

Task-aware embeddings offer a dynamic twist to traditional retrieval systems, breaking away from the static approach. This innovation could enable the use of a single embedding model across various tasks, providing dynamic embeddings without the need for indexing documents with numerous vectors, all while maintaining retrieval accuracy.