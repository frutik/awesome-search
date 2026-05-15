---
title: "Superintelligent Retrieval Agent (SIRA)"
source: "https://arxiv.org/pdf/2605.06647"
author: "Meta / Rice University (Zeyu Yang, Qi Ma, Jason Chen, Anshumali Shrivastava)"
published: 2026
tags: [retrieval, BM25, query-expansion, corpus-enrichment, agentic-search, BEIR]
---

# Superintelligent Retrieval Agent (SIRA)

**Paper:** Yang et al. (2026), Meta / Rice University  
**GitHub:** https://github.com/facebookresearch/sira

## Core Claim

> *Compress a multi-step exploratory retrieval process into one expert-level retrieval action.*

SIRA argues that modern agentic RAG systems behave like tourists (search → read → reformulate → repeat), while an expert already knows the right terminology. The fix: use LLMs to make *lexical retrieval itself smarter*, not to loop more.

## Architecture (5 stages)

1. Data preparation
2. BM25 indexing
3. **Corpus enrichment**: LLM reads each document and adds vocabulary users might search with (e.g., "myocardial infarction" → also indexed as "heart attack", "MI", "cardiac arrest")
4. **Query expansion**: LLM predicts which discriminative, rare terms are likely to appear in relevant documents — not just semantically related words, but terms that distinguish good from bad matches
5. LLM-based pointwise reranking

## Why BM25?

SIRA's key insight: BM25 naturally rewards rare, discriminative words via IDF. The problem with vector search is it compresses information too aggressively and loses:
- Rarity / discriminative power
- Controllability (constraints, exclusions)
- Interpretability

BM25 is interpretable, debuggable, controllable, cheap — and with LLM-generated vocabulary expansion it becomes far stronger than assumed.

## Results (BEIR benchmarks)

Wins average Recall@10 and NDCG@10 against:
- BM25, E5, SPLADE, HyDE
- Search-R1, grep-style retrieval agents (GrepRAG, ShellAgent)
- Multiple dense retrievers

GrepRAG and ShellAgent performed especially poorly, supporting the thesis that tool-use agentic loops are weaker than one carefully engineered retrieval action.

## Design Philosophy

- Retrieval is not about semantic similarity; it's about **ranking the correct document above confusing distractors**
- BM25 + IDF naturally handles discriminative vocabulary
- Embeddings fail on exact jargon, constraints, compositional filters
- Multi-step agents compensate for weak retrieval with more compute; SIRA invests that compute in the retrieval step itself

## Practical Takeaway

You may not need:
- 15 retrieval rounds
- Complicated memory accumulation
- Expensive vector infra everywhere

Instead: better query expansion, corpus-aware vocabulary generation, discriminative lexical terms, explicit constraints.

## Related Concepts

- [[Query Understanding]]
- [[BM25]]
- [[Agentic Search]]
- [[Dense Vector Retrieval]]
- [[Sparse Vector Retrieval]]
