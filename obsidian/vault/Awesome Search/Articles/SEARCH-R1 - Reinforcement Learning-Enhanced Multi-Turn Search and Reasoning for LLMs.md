---
type: article
title: "SEARCH-R1 - Reinforcement Learning-Enhanced Multi-Turn Search and Reasoning for LLMs"
source: "https://medium.com/advancedai/search-r1-reinforcement-learning-enhanced-multi-turn-search-and-reasoning-for-llms-dc24bb8d7409"
author:
  - "[[QvickRead]]"
published: 2025-03-19
created: 2026-06-01
concepts:
  - "[[Search-R1]]"
  - "[[RAG]]"
  - "[[Agentic Search]]"
topics:
  - "[[Conversational and Agentic Search]]"
tags:
  - article
  - search-r1
  - reinforcement-learning
  - multi-turn-reasoning
  - rag
---

# SEARCH-R1: Reinforcement Learning-Enhanced Multi-Turn Search and Reasoning for LLMs

A technical walkthrough of the [[Search-R1]] framework (arxiv: [2503.09516](https://arxiv.org/abs/2503.09516)) — an RL-based approach that trains LLMs to interleave multi-turn search queries with chain-of-thought reasoning, without requiring human-labeled reasoning trajectories.

---

## Problem Addressed

Standard LLMs face two core limitations:
1. **Complex multi-step reasoning** — chain-of-thought alone is insufficient for hard QA tasks
2. **Stale parametric knowledge** — no access to current or domain-specific information

[[RAG]] mitigates the second but is constrained to single-turn retrieval and is sensitive to retrieval inaccuracy. Tool-use approaches require extensive supervised data.

## Core Contributions

### 1. RL-Based Search Integration
The model learns to generate search queries and use retrieved results through reinforcement learning — not supervised imitation. This removes dependence on hand-labeled reasoning trajectories.

### 2. Interleaved Multi-Turn Reasoning
Structured output using special tokens:
- `<think>…</think>` — internal chain-of-thought reasoning
- `<search>…</search>` — query issued to search engine
- `<information>…</information>` — retrieved passages inserted back

The model iterates: reason → search → incorporate results → reason again.

### 3. Token-Level Loss Masking
Retrieved passage tokens are **masked from the training loss**. Without this, the model trains on content it didn't generate, destabilising RL optimisation. This is a critical ingredient for stable performance.

### 4. Outcome-Based Reward Function
Uses final-answer exact match as the reward signal — simple and robust. Avoids reward hacking from complex process-based rewards.

### 5. Multi-Algorithm Compatibility
Evaluated with both:
- **PPO** (Proximal Policy Optimization) — better stability across model architectures
- **GRPO** (Group Relative Policy Optimization) — faster convergence

## Experimental Results

Evaluated on 7 QA datasets: NQ, TriviaQA, HotpotQA, 2WikiMultiHopQA, and others spanning single-hop and multi-hop reasoning tasks.

Performance gains over state-of-the-art baselines:
- **Qwen2.5-7B**: +26%
- **Qwen2.5-3B**: +21%
- **LLaMA3.2-3B**: +10%

Effective across both base and instruction-tuned model variants.

## Limitations

- Outcome-based reward may not capture nuances in complex tasks
- Search engine treated as a black box — no control over retrieval quality
- Current work is text-only; multimodal extension is open

## Related Concepts

- [[Search-R1]] — the framework itself
- [[RAG]] — prior architecture being extended
- [[Agentic Search]] — broader paradigm; Search-R1 is a concrete RL-based implementation
- [[Reinforcement Learning for Search]] — the training methodology

## Related Articles

- [[From RAG to Search-R1 - Evolving Language Models from Knowledge Retrieval to Autonomous Reasoning]] — accessible overview of the same framework
- [[Agentic Search for Context Engineering]] — related agentic retrieval framing
- [[Superintelligent Retrieval Agent SIRA]] — contrasting approach (BM25 enrichment, no RL)
