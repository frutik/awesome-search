---
type: topic
title: "RL-Trained Search Agents"
aliases: ["Reinforcement Learning for Search Agents", "RL Search Agents", "RL for Retrieval"]
tags: [topic, reinforcement-learning, agentic-search, llm, multi-turn-retrieval, frontier]
related_concepts: [Reinforcement Learning for Search, Search-R1, Agentic Search, RAG, Purpose-Built Agentic Search Models]
related_topics: [Current Frontier of Search, Conversational and Agentic Search]
articles:
  - "[[SEARCH-R1 - Reinforcement Learning-Enhanced Multi-Turn Search and Reasoning for LLMs]]"
  - "[[From RAG to Search-R1 - Evolving Language Models from Knowledge Retrieval to Autonomous Reasoning]]"
created: 2026-06-18
---

# RL-Trained Search Agents

Most agentic search today *prompts* a general or specialized LLM to use search tools. The frontier underneath it is **training the searcher itself with reinforcement learning** — letting the model discover *when* to search, *what* to query, and *how* to fold results into reasoning, rewarded only by final-answer correctness rather than human-labeled trajectories. This is the methodological complement to [[Purpose-Built Agentic Search Models]]: one trains the *policy* of searching, the other ships a *product* model.

See [[Reinforcement Learning for Search]] for the methodology and [[Search-R1]] for the canonical framework.

---

## Why RL for Search

Supervised tool-use training needs labeled examples of "good" search sequences — expensive to produce and brittle across domains. RL sidesteps this: reward the model for getting the final answer right and let it learn the search strategy autonomously. This is what separates RL search agents from prompted [[Agentic Search]] and from single-shot [[RAG]].

## Key Design Choices

| Component | Choice | Why |
|---|---|---|
| Reward | Outcome-based (e.g. exact match) | Simple, robust, resists reward hacking; process rewards are gameable |
| Loss masking | Mask retrieved tokens from the loss | The model must not be trained on content it retrieved but didn't generate — without this, training is unstable |
| RL algorithm | PPO (stable) / GRPO (faster convergence) | Trade stability vs. speed |
| Trajectories | None required | The point: no human-labeled reasoning chains |

**Token-level loss masking** is the critical technical contribution that makes the loop trainable.

## Search-R1: The Canonical Framework

[[Search-R1]] (arXiv:2503.09516) trains an LLM to interleave reasoning and retrieval with `<think>`, `<search>`, `<information>` tokens:

1. Reason about what's needed → 2. Issue a search query → 3. Incorporate results → 4. Repeat until sufficient → 5. Answer.

Reported gains over baselines: +26% (Qwen2.5-7B), +21% (Qwen2.5-3B), +10% (LLaMA3.2-3B) across 7 QA datasets (NQ, TriviaQA, HotpotQA, 2WikiMultiHopQA, …).

| Aspect | [[RAG]] | RL-trained ([[Search-R1]]) |
|---|---|---|
| Retrieval turns | 1 | Multiple, dynamic |
| Query source | Fixed user query | RL-generated mid-reasoning |
| Training | Supervised / none | Reinforcement learning |
| Knowledge source | Static index | Live search |

## Where It Sits in the Frontier

RL-trained agents and [[Purpose-Built Agentic Search Models]] are two bets on making the searcher smart: train the *search policy* with RL (Search-R1) vs. train a *task-specialized model* on the rewrite/retrieve/rerank outcome ([[SID-1]]). Both contrast with [[Direct Corpus Interaction]], which keeps a general agent but upgrades the *interface* to the corpus. All three are the live edge of [[Current Frontier of Search]].

---

## Related Concepts
- [[Reinforcement Learning for Search]] — the training methodology
- [[Search-R1]] — the canonical RL search framework
- [[Agentic Search]] — the broader paradigm RL enables
- [[RAG]] — the single-turn baseline being surpassed
- [[Purpose-Built Agentic Search Models]] — the sibling "train the searcher" bet

## Related Topics
- [[Current Frontier of Search]] — RL agents are one of its live fronts
- [[Conversational and Agentic Search]] — multi-turn retrieval + reasoning

## Related Articles
- [[SEARCH-R1 - Reinforcement Learning-Enhanced Multi-Turn Search and Reasoning for LLMs]] — technical breakdown
- [[From RAG to Search-R1 - Evolving Language Models from Knowledge Retrieval to Autonomous Reasoning]] — accessible comparison
