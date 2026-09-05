---
type: article
title: "Patterns for Building LLM-based Systems & Products"
source: "https://eugeneyan.com/writing/llm-patterns/"
author: ["Eugene Yan"]
tags:
  - clippings
  - llm
  - rag
  - evaluation
  - architecture
concepts:
  - RAG
  - LLM Guardrails
  - LLM as Judge
created: 2026-09-05
---

# Patterns for Building LLM-based Systems & Products

**Source**: https://eugeneyan.com/writing/llm-patterns/
**Author**: [[Eugene Yan]]

## Summary

A synthesis of seven recurring patterns for putting LLMs into production. Included here mainly as the canonical statement of the **guardrails** pattern ([[LLM Guardrails]]), which little else in this vault covers.

## The Seven Patterns

| Pattern | Purpose, as stated |
|---|---|
| **Evals** | "To measure performance" |
| **RAG** | "To add recent, external knowledge" |
| **Fine-tuning** | "To get better at specific tasks" |
| **Caching** | "To reduce latency and cost" |
| **Guardrails** | "To ensure output quality" |
| **Defensive UX** | "To anticipate & handle errors gracefully" |
| **Collect user feedback** | "To build our data flywheel" |

## Named Techniques

- **Benchmarks**: MMLU, EleutherAI Eval, HELM, AlpacaEval
- **Metrics**: BLEU, ROUGE, BERTScore, MoverScore
- **Retrieval**: Dense Passage Retrieval, FAISS, HNSW, ScaNN, HyDE, E5, Instructor, GTE
- **Fine-tuning**: LoRA, QLoRA, prefix-tuning, adapters, soft prompt tuning
- **Tooling**: GPTCache, Guardrails, NeMo-Guardrails, Guidance, sentence-transformers

## Related Concepts

- [[LLM Guardrails]] — the pattern this is cited for
- [[RAG]] · [[LLM as Judge]] · [[Dense Passage Retriever]] · [[HNSW]] · [[Hypothetical Document Embeddings]] · [[LoRA]] · [[QLoRA]]

## Related Tools

- [[Sentence Transformers]] · [[FAISS]]

## Related People

- [[Eugene Yan]]
