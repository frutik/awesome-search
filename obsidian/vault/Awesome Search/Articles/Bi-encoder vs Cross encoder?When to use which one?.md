---
title: "Bi-encoder vs Cross encoder?When to use which one?"
source: "https://medium.com/@sujathamudadla1213/bi-encoder-vs-cross-encoder-when-to-use-which-one-4a20edbe6d37"
author:
  - "[[Sujatha Mudadla]]"
published: 2023-11-13
created: 2026-05-15
description: "More"
tags:
  - "clippings"
  - medium
---
**Bi-encoder and cross-encoder** are two different approaches to designing models for natural language understanding tasks, particularly in the context of information retrieval and similarity search.

1. **Bi-Encoder:**
- **Architecture:** In a bi-encoder model, there are two separate encoders — one for encoding the input query and another for encoding the candidate documents. These encoders work independently, producing embeddings for the query and each document.
- **Training:** During training, the model is trained to maximize the similarity between the query and the relevant document, while minimizing the similarity between the query and irrelevant documents. Training is often done with a contrastive loss function.
- **Scoring:** At inference time, the model calculates the similarity score between the query and each document independently. The document with the highest similarity score is considered the most relevant.
- **Use Cases:** Bi-encoders are commonly used in tasks where document retrieval or ranking is the primary goal, such as search engines or recommendation systems.

2\. **Cross-Encoder:**

- **Architecture:** In a cross-encoder model, the query and document are processed together in a single encoder. This means that the model takes both the query and the document as input and produces a joint representation.
- **Training:** Similar to bi-encoders, cross-encoders are trained to maximize the similarity between relevant query-document pairs. However, since they process both the query and document together, they capture interactions between the two.
- **Scoring:** Cross-encoders generate a single similarity score for each query-document pair, considering the interaction between the query and document embeddings. The document with the highest score is considered the most relevant.
- **Use Cases:** Cross-encoders are useful when capturing the interaction between the query and document is crucial, such as in tasks where understanding the context or relationship between the query and document is important.

**When to Use Which One:**

- Bi-Encoder: Use bi-encoders when you have large-scale datasets and computational resources. They are often faster during inference since similarity scores can be computed independently. They are suitable for tasks where capturing complex interactions between the query and document is less critical.
- **Cross-Encoder:** Choose cross-encoders when capturing interactions between the query and document is crucial for your task. They are more computationally intensive but can provide better performance in scenarios where understanding the context or relationship between the query and document is essential.

**Ultimately, the choice between bi-encoder and cross-encoder depends on the specific requirements of your natural language understanding task and the computational resources available.**

## Related Concepts
- [[Embeddings]] — what both architectures produce
- [[Dense Embeddings]] — bi-encoders produce dense embedding vectors
- [[Bi-Encoder]] — two-tower architecture; precomputable; fast retrieval
- [[Cross-Encoder]] — joint encoding; no precomputed vectors; accurate reranker
- [[Retrieval Pipeline]] — bi-encoder for retrieval stage, cross-encoder for reranking
- [[Dense Vector Retrieval]] — downstream use of bi-encoder embeddings
- [[Semantic Search]] — bi-encoders enable semantic matching

## People
- [[Sujatha Mudadla]] — author