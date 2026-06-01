---
type: concept
title: "Search-R1"
aliases:
  - "SEARCH-R1"
  - "Search R1"
tags:
  - concept
  - agentic-search
  - reinforcement-learning
  - llm
  - multi-turn-retrieval
related_concepts:
  - "[[RAG]]"
  - "[[Agentic Search]]"
  - "[[Reinforcement Learning for Search]]"
created: 2026-06-01
---

# Search-R1

An RL-trained framework that teaches LLMs to interleave multi-turn web search with chain-of-thought reasoning — enabling autonomous, iterative research behaviour rather than single-pass retrieval. Introduced in arxiv paper [2503.09516](https://arxiv.org/abs/2503.09516).

---

## Core Idea

Instead of retrieving once before generating ([[RAG]]), Search-R1 trains an LLM to:
1. **Reason** about what information it needs
2. **Issue search queries** to a live search engine
3. **Incorporate retrieved results** into ongoing reasoning
4. **Repeat** until sufficient context is gathered
5. **Generate** a final answer

The model learns this entire loop — including *when* and *what* to search — through reinforcement learning, with no human-labeled reasoning trajectories.

## Training Design

| Component | Design Choice |
|---|---|
| Learning method | Reinforcement learning (PPO or GRPO) |
| Token format | `<think>`, `<search>`, `<information>` special tokens |
| Loss masking | Retrieved tokens masked — model only trains on its own generated tokens |
| Reward signal | Outcome-based (exact match); no process reward |
| Trajectories | No human labels required |

**Token-level loss masking** is a critical technical contribution: without it, the model inadvertently optimises over retrieved content it didn't generate, leading to unstable training.

## Performance

Evaluated on 7 QA datasets (NQ, TriviaQA, HotpotQA, 2WikiMultiHopQA, and others):

| Model | Gain over baseline |
|---|---|
| Qwen2.5-7B | +26% |
| Qwen2.5-3B | +21% |
| LLaMA3.2-3B | +10% |

## Comparison to RAG

| Aspect | RAG | Search-R1 |
|---|---|---|
| Retrieval turns | 1 | Multiple (dynamic) |
| Query source | Fixed user query | RL-generated mid-reasoning |
| Knowledge source | Static index | Live web |
| Training | Supervised | Reinforcement learning |
| Latency | Fast | Slower (external API calls) |

## Related Concepts

- [[RAG]] — the single-turn retrieval architecture Search-R1 extends
- [[Agentic Search]] — the broader paradigm; Search-R1 is a concrete RL-trained instance
- [[Reinforcement Learning for Search]] — training methodology

## Related Articles

- [[SEARCH-R1 - Reinforcement Learning-Enhanced Multi-Turn Search and Reasoning for LLMs]] — technical paper breakdown
- [[From RAG to Search-R1 - Evolving Language Models from Knowledge Retrieval to Autonomous Reasoning]] — accessible comparison overview
