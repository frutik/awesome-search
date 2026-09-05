---
type: concept
title: "RAG"
aliases: ["Retrieval-Augmented Generation", "Retrieval Augmented Generation"]
tags:
  - concept
  - search
  - llm
  - rag
created: 2026-05-16
---

# RAG (Retrieval-Augmented Generation)

## Definition

**RAG** combines a retrieval system with a generative language model. Instead of relying on the LLM's parametric memory alone, RAG retrieves relevant context from an external knowledge base and passes it to the LLM as context for generation.

```
User query → Retrieval → Top-k documents → LLM (query + docs) → Response
```

## Core Components

1. **Chunking** — Split documents into indexable units ([[Text Chunking]])
2. **Indexing** — Embed chunks and store in vector database
3. **Retrieval** — Find chunks most relevant to query ([[Dense Vector Retrieval]], [[Hybrid Search]])
4. **Generation** — LLM synthesizes answer from retrieved context

## Why RAG Matters for Search

- Grounds LLM responses in actual documents (reduces hallucination)
- Enables citing sources
- Knowledge can be updated without retraining the LLM
- Domain adaptation without fine-tuning

## RAG Quality Factors

**Retrieval quality** (most critical):
- Correct chunks must be retrieved; LLM can't fix bad retrieval
- [[Text Chunking]] strategy affects what's retrievable
- [[Embedding Fine-tuning]] improves domain-specific retrieval
- [[Hypothetical Document Embeddings]] boosts zero-shot recall

**Generation quality:**
- Context window management
- Prompt engineering
- Cross-encoder reranking before passing to LLM

## Agentic RAG

[[Agentic Search]] extends RAG by making retrieval iterative:
- Agent decides what to retrieve next based on current knowledge state
- Multi-step reasoning with multiple retrieval rounds
- Tools beyond text search (calculators, APIs, databases)


### Search-R1: RL-Trained Multi-Turn Retrieval

[[Search-R1]] takes agentic RAG further by training the model via [[Reinforcement Learning for Search]] — no human-labeled trajectories needed. The model learns to interleave `<think>`, `<search>`, and `<information>` tokens, iteratively querying a live search engine during reasoning. This contrasts with standard RAG's static index and single-turn retrieval pattern.

## Beyond Flat Chunk Retrieval

Baseline RAG scores each passage independently, which breaks on two classes of question: those needing facts joined across documents, and those about themes across a whole collection. Two families of response:

- **Restructure the index** — [[GraphRAG]] builds an LLM-generated knowledge graph and retrieves over its structure; [[HippoRAG]] runs Personalized PageRank over that graph to reach multi-hop answers in a single step.
- **Enlarge the window** — [[Long-Context RAG]], which the evidence says *supplements* retrieval rather than replacing it, and runs into the "lost in the middle" limit measured by the [[Needle in a Haystack Test]].

## Operating a RAG Pipeline

| Concern | Where it is handled |
|---|---|
| Which path should this query take at all? | [[Query Routing]] |
| Context too large or too expensive | [[Prompt Compression]] |
| Constraining what goes in and comes out | [[LLM Guardrails]] |
| Is the answer actually supported by the evidence? | [[Hallucination Detection]] |

## Frameworks

[[LlamaIndex]] · [[LangChain]] · [[Haystack (deepset)]] for orchestration; [[RAGAS]] for evaluation; [[DSPy]] for optimizing the prompts rather than authoring them.

## Related Concepts
- [[Embeddings]] — the retrieval component of RAG uses embeddings to find relevant context
- [[Dense Embeddings]] — typically the retrieval representation in RAG pipelines

- [[Text Chunking]] — preprocessing for RAG
- [[Dense Vector Retrieval]] — typical retrieval method in RAG
- [[Hybrid Search]] — combining sparse + dense for better RAG retrieval
- [[Hypothetical Document Embeddings]] — query-side improvement
- [[Agentic Search]] — agentic extension of RAG
- [[Task-Aware Embeddings]] — improves RAG by task-conditioning queries

- [[Search-R1]] — RL-trained evolution of RAG; multi-turn live-web retrieval interleaved with reasoning
- [[Reinforcement Learning for Search]] — training paradigm that replaces supervised trajectory labeling

- [[GraphRAG]] · [[HippoRAG]] — graph-structured retrieval for multi-hop and thematic questions
- [[Long-Context RAG]] · [[Needle in a Haystack Test]] — how far a bigger window actually gets you
- [[Query Routing]] · [[Prompt Compression]] · [[LLM Guardrails]] · [[Hallucination Detection]] — pipeline operation

## Articles

- [[Chunking Strategies for LLM Applications]]
- [[Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex 1]]
- [[raw_articles/Improve your RAG applications by moving to Task-aware Embeddings]]
- [[Hypothetical Document Embeddings HyDE]]
- [[Agentic Search as an Agile Engineering Process]]
- [[Agentic Search for Context Engineering]] — [[Leonie Monigatti]]; traces evolution RAG → agentic RAG → context engineering; articulates where single-pass RAG breaks
- [[From RAG to Search-R1 - Evolving Language Models from Knowledge Retrieval to Autonomous Reasoning]] — [[Lakshmi Devi Prakash]]; traces evolution from RAG to RL-based multi-turn search
- [[SEARCH-R1 - Reinforcement Learning-Enhanced Multi-Turn Search and Reasoning for LLMs]] — technical breakdown of Search-R1 framework
- [[GraphRAG - Unlocking LLM discovery on narrative private data]] — [[Jonathan Larson]], [[Steven Truitt]]; LLM-built knowledge graphs over private corpora
- [[HippoRAG - Neurobiologically Inspired Long-Term Memory for Large Language Models]] — single-step multi-hop retrieval at 10–30× lower cost than iterative
- [[NVIDIA Research - RAG with Long Context LLMs]] — [[Ravi Theja]]; retrieval still helps at 32K, and 5–10 chunks beats 20
- [[Patterns for Building LLM-based Systems and Products]] — [[Eugene Yan]]; seven production patterns
- [[Routing in RAG Driven Applications]] — [[Sami Maameri]]; seven router types
- [[How to Cut RAG Costs by 80% Using Prompt Compression]] — [[Iulia Brezeanu]]
- [[Measuring Hallucinations in RAG Systems]] — [[Shane Connelly]]; the Vectara leaderboard

## Related Tools

- [[LlamaIndex]] · [[LangChain]] · [[Haystack (deepset)]] · [[RAGAS]] · [[DSPy]] · [[AutoRAG]]
