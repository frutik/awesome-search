---
type: concept
title: "Adaptive Retrieval"
aliases: ["adaptive RAG", "retrieval necessity", "when to retrieve", "selective retrieval", "retrieval triggering"]
tags:
  - concept
  - rag
  - query-routing
related_concepts:
  - "[[RAG]]"
  - "[[Query Routing]]"
  - "[[Agentic Search]]"
created: 2026-09-26
---

# Adaptive Retrieval

## Definition

Deciding **per query whether to retrieve, and how much** — no retrieval, one retrieval step, or several rounds of retrieval and reasoning — instead of running the same RAG pipeline for everything. It is [[Query Routing]] where the routes are retrieval *strategies* of different cost rather than different data sources.

## Why It Matters

Traffic is mixed. Simple questions ("Paris is the capital of what?") are answered fine by the LLM alone; multi-hop ones need iterative retrieval. A fixed pipeline either overspends on the first or fails the second ([[Adaptive-RAG - Learning to Adapt Retrieval-Augmented LLMs through Question Complexity|Adaptive-RAG]]). Retrieval is not free of harm either: in [[Efficient Federated Search for RAG using Lightweight Routing|RAGRoute]]'s MMLU experiment, retrieving from randomly chosen sources scored *below* not retrieving at all (71.74% vs 73.35%), because irrelevant context distracts the model.

## Approaches

| Approach | Decision signal | Example |
|---|---|---|
| **Entity frequency** | Retrieve only when the question's entities are rare | Mallen et al. (2023), as described in Adaptive-RAG |
| **Complexity classifier** | A small model predicts no / single / multi-step | [[Adaptive-RAG - Learning to Adapt Retrieval-Augmented LLMs through Question Complexity\|Adaptive-RAG]] — T5-Large, labels from which strategy answered correctly |
| **Query-type classifier** | Factual / reasoning / summarization mapped to strategies of increasing cost | [[Lightweight Query Routing for Adaptive RAG - A Baseline Study on RAGRouter-Bench\|RAGRouter-Bench baselines]] — TF-IDF + SVM, simulated 28.1% token saving |
| **"No retrieval" as a ranked option** | Rank retrievers *and* abstention by expected gain in answer quality | [[LTRR - Learning To Rank Retrievers for LLMs\|LTRR]] |
| **Generation-time triggers** | Retrieve new documents when generated tokens have low confidence | Jiang et al. (2023), as described in Adaptive-RAG; Self-RAG (Asai et al., 2024) is the other adaptive baseline there. Agents make the decision step by step — see [[Agentic Search]] |

## Practical Notes

- **Imperfect routers still pay.** Adaptive-RAG's classifier is only ~55% accurate, yet matches always-multi-step F1 at under half the time, because its errors mostly lean toward retrieving more than necessary.
- **Cheap features go far.** On RAGRouter-Bench, TF-IDF beat sentence embeddings for predicting query type.
- **Query text is not the whole story.** Which strategy wins also depends on corpus structure; query-only routers are a floor.

## Related Concepts

- [[Query Routing]] — the general pattern
- [[RAG]] · [[Agentic Search]] — agents make the same decision step by step rather than once
- [[Query Classification]] · [[Query Specificity]]
- [[GraphRAG]] — one of the expensive strategies a router may choose

## Articles

- [[Adaptive-RAG - Learning to Adapt Retrieval-Augmented LLMs through Question Complexity]]
- [[Lightweight Query Routing for Adaptive RAG - A Baseline Study on RAGRouter-Bench]]
- [[LTRR - Learning To Rank Retrievers for LLMs]]
- [[Efficient Federated Search for RAG using Lightweight Routing]]
