---
title: "RankGPT"
aliases: ["RankGPT", "Rank GPT"]
tags:
  - concept
  - ranking
  - reranking
  - llm
  - neural-ir
---

# RankGPT

## Definition

RankGPT is a **listwise** LLM [[Reranking|reranker]] that prompts an instruction-tuned LLM (originally ChatGPT/GPT-4) to **reorder a candidate list directly** — generating a permutation of document identifiers rather than scoring documents one at a time. It requires **no fine-tuning**: the ranking ability comes from the base model's instruction following.

## How It Works

1. Pass the query plus a numbered list of candidate passages to the LLM.
2. Prompt it to output the candidates re-ordered by relevance (e.g. `[3] > [1] > [5] > ...`).
3. Because candidate lists usually exceed the context window, RankGPT uses a **sliding-window strategy**: rank a window of N candidates, carry the top survivors forward, slide, and repeat — progressively bubbling the best documents to the top.

Seeing the whole window at once lets the model use **cross-document context** (relative comparisons) that pointwise rerankers like [[MonoT5]] and [[RankLLaMA]] cannot.

## Pointwise vs Pairwise vs Listwise

| Style | Example | Sees |
|---|---|---|
| Pointwise | [[MonoT5]], [[RankLLaMA]] | One (query, doc) pair at a time |
| Pairwise | DuoT5 | Two docs compared |
| **Listwise** | **RankGPT** | A whole window of candidates |

This mirrors the classic [[Learning to Rank]] axis (see [[Pointwise vs Pairwise vs Listwise Learning to Rank]]), re-instantiated at the prompt level.

## Trade-offs

- **+** No training data or fine-tuning required; strong zero-shot quality; exploits cross-document comparison.
- **−** Expensive and slow (large-model inference over many windows); sensitive to prompt and document order; permutation outputs need parsing/validation.
- Often **distilled** into smaller specialized rerankers for production use.

## Related Concepts

- [[Reranking]] — the stage RankGPT implements
- [[RankLLaMA]] — fine-tuned pointwise LLM reranker (contrast: RankGPT is prompt-based, listwise)
- [[MonoT5]] — T5 pointwise reranker
- [[LLM as Judge]] — same models scoring relevance
- [[Listwise Relevance Evaluation]] — the evaluation style RankGPT embodies
- [[Cross-Encoder]] — the classic reranker LLM rankers extend

## Topics

- [[Reasoning Reranking]]
- [[Current Frontier of Search]]
