---
type: concept
title: "Reinforcement Learning for Search"
aliases:
  - "RL for Search"
  - "RL-based Retrieval"
tags:
  - concept
  - reinforcement-learning
  - search
  - llm
related_concepts:
  - "[[Search-R1]]"
  - "[[Agentic Search]]"
  - "[[RAG]]"
created: 2026-06-01
---

# Reinforcement Learning for Search

Using reinforcement learning to train language models to perform search — deciding *when* to query, *what* to query, and *how* to use retrieved results — without requiring human-labeled reasoning trajectories.

---

## Why RL for Search

Supervised approaches to teaching LLMs to use search tools require labeled examples of "good" search sequences — expensive to produce and brittle across domains. RL sidesteps this by rewarding the model for final answer correctness, letting it discover effective search strategies autonomously.

## Key Design Choices

### Reward Function
- **Outcome-based** (e.g., exact match on final answer) — simple, robust, avoids reward hacking
- Process-based rewards (rewarding intermediate steps) are more complex and prone to gaming

### Loss Masking
When retrieved content is inserted into the model's context, those tokens should be **masked from the training loss** — the model should not be rewarded or penalised for content it retrieved but did not generate. Without this, training is unstable.

### RL Algorithms
- **PPO** (Proximal Policy Optimization) — more stable across architectures
- **GRPO** (Group Relative Policy Optimization) — faster convergence

## Current Implementations

- [[Search-R1]] — interleaved `<think>`, `<search>`, `<information>` token loop; outcome reward; token-level loss masking

## Relationship to Other Approaches

| Approach | How It Uses Search |
|---|---|
| [[RAG]] | Single retrieval before generation; no RL |
| Tool-use / ReAct | Prompting or RL; often needs supervised trajectories |
| [[Search-R1]] | Pure RL; no human trajectories; multi-turn |

## Related Concepts

- [[Search-R1]] — primary RL-for-search framework
- [[Agentic Search]] — broader paradigm this training methodology enables
- [[RAG]] — the supervised single-turn baseline

## Related Articles

- [[SEARCH-R1 - Reinforcement Learning-Enhanced Multi-Turn Search and Reasoning for LLMs]]
- [[From RAG to Search-R1 - Evolving Language Models from Knowledge Retrieval to Autonomous Reasoning]]

## Topics

- [[RL-Trained Search Agents]]
- [[Frontier of Search 2026]]
