---
type: tool
title: "LlamaIndex"
aliases: ["llama_index", "LlamaIndex OSS", "GPT Index"]
website: https://www.llamaindex.ai/
repo: https://github.com/run-llama/llama_index
tags:
  - tool
  - rag
  - llm
  - indexing
  - open-source
related_concepts:
  - "[[RAG]]"
  - "[[Text Chunking]]"
  - "[[Multimodal RAG]]"
  - "[[Query Routing]]"
created: 2026-09-05
---

# LlamaIndex

A data framework for building LLM applications, maintained by `run-llama` under an MIT license. It provides data connectors, indexing and data-structuring tools, and retrieval/query interfaces, with both a high-level API (roughly five lines of code) and customisable lower-level APIs.

🔗 https://www.llamaindex.ai/ · https://github.com/run-llama/llama_index

The project has since repositioned around document agents and OCR, describing itself as "the leading document agent and OCR platform"; **LlamaParse** is the enterprise document parsing/extraction product, with agentic OCR across 130+ formats.

## Why It Matters Here

LlamaIndex produced much of the empirical RAG-tuning literature this vault draws on — the chunk-size study, the embedding/reranker bake-off, and the long-context retrieval analysis all came out of its blog and its `RetrieverEvaluator` module. Its evaluation tooling is the reason those posts carry numbers rather than opinions.

## Multi-Modal Abstractions

Introduced for [[Multimodal RAG]]: the `OpenAIMultiModal` class, a `MultiModalEmbedding` base class with a `ClipEmbedding` implementation, and `MultiModalVectorIndex` for indexing text and image modalities into separate vector store collections.

## Related Tools

- [[Haystack (deepset)]] · [[LangChain]] — comparable orchestration frameworks
- [[RAGAS]] — evaluation
- [[Qdrant Vector DB]] · [[Pinecone Vector DB]] · [[Weaviate Vector DB]] — backing stores

## Related Concepts

- [[RAG]] · [[Text Chunking]] · [[Multimodal RAG]] · [[Query Routing]] · [[Long-Context RAG]]

## Articles

- [[Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex]]
- [[Boosting RAG - Picking the Best Embedding and Reranker models]]
- [[NVIDIA Research - RAG with Long Context LLMs]]
- [[Multi-Modal RAG - Indexing And Retrieval Guide]]
- [[Hands-On RAG guide for personal data with Vespa and LLamaIndex]]
