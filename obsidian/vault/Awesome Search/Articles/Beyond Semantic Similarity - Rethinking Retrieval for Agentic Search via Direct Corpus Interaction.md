---
created: 2026-05-16
title: "Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction"
source: "https://huggingface.co/papers/2605.05242"
arxiv: "2605.05242"
author: []
published: 2026-05-08
institution: "TIGER-Lab"
tags: [agentic-search, direct-corpus-interaction, retrieval, grep, multi-hop-QA, BEIR, BRIGHT, company-blog]
---

# Beyond Semantic Similarity: Rethinking Retrieval for Agentic Search via Direct Corpus Interaction

**Authors:** TIGER-Lab (Zhuofeng Li et al.)

## Abstract

Modern retrieval systems — whether lexical or semantic — expose a corpus through a **fixed similarity interface** compressing access into a single top-k retrieval step before reasoning. For agentic search, this is a bottleneck:
- Exact lexical constraints are hard to express
- Sparse clue conjunctions are difficult
- Local context checks require multiple steps
- Evidence filtered out early cannot be recovered by downstream reasoning

## Direct Corpus Interaction (DCI)

The key proposal: instead of any retrieval API, let an agent search the raw corpus **directly with general-purpose terminal tools** — `grep`, `find`, `bash`, shell pipelines, lightweight scripts.

This is analogous to a coding agent navigating a codebase:
- No embedding model needed
- No vector index needed
- No offline indexing needed
- Adapts naturally to evolving local corpora

## Results

DCI substantially outperforms strong sparse, dense, and reranking baselines:

| Benchmark | Gain vs Baselines |
|---|---|
| Agentic Search (BrowseComp-Plus) | +11.0% |
| Multi-hop QA | +30.7% |
| IR Ranking (BEIR/BRIGHT) | +21.5% |

## Key Insight

> As language agents become stronger, retrieval quality depends not only on reasoning ability but also on the **resolution of the interface** through which the model interacts with the corpus.

DCI opens a broader interface-design space — the interface itself matters, not just the retrieval model or reasoning capability.

## Why This Matters

Traditional retrieval is a one-shot, compressed view. DCI enables:
- **Exact lexical constraints** via grep patterns
- **Multi-step hypothesis refinement** — revise the search plan after partial evidence
- **Sparse clue conjunctions** — combine multiple weak signals
- **Local context checks** — verify evidence in context

## Limitations / Caveats

The approach requires a strong coding-capable agent and works best when the corpus fits in an accessible file system. May not apply to very large-scale web search scenarios.

## Related Concepts

- [[Agentic Search]] — the paradigm that motivates DCI
- [[Retrieval Pipeline]] — DCI replaces the traditional pipeline
- [[RAG]] — DCI provides an alternative to embedding-based RAG retrieval

## Related Articles

- [[Agentic Search as an Agile Engineering Process]]
- [[Superintelligent Retrieval Agent SIRA]]
- [[Mutually Assured Distraction]]
