---
title: "Mutually Assured Distraction"
source: "https://hornet.dev/blog/mutually-assured-distraction"
author: "[[Lester Solbakken]]"
published: 2026-01-30
tags: [agentic-search, retrieval, evaluation, distractor, RAG]
---

# Mutually Assured Distraction

**Author:** [[Lester Solbakken]] (hornet.dev)

## Core Thesis: MAD

**Mutually Assured Distraction (MAD)**: a dynamic where locally rational optimizations in retrieval and reasoning lead to global system instability.

- Better retrievers → more convincing distractors (hard negatives that survive ranking)
- Better reasoners → deeper trust in those convincing distractors
- Both sides improve; reliability degrades

## Why LLMs Can't Ignore

For humans, skipping an irrelevant search result has near-zero mental cost. For an LLM, every retrieved document is injected into context and *processed in parallel via attention* — there is no "ignore." Every token competes for probability mass.

A **distractor** = text that is plausible, semantically adjacent, high-confidence, and wrong. It looks like evidence, survives ranking, and once in the context window, degrades reliability.

## Key Research Findings

- **"Lost in the Noise"**: hard negatives can drop multi-hop reasoning accuracy by up to 80%
- **"The Power of Noise"**: padding with *random* documents can improve accuracy (random noise → higher attention entropy; distractors concentrate attention on the wrong evidence)
- **Inverse scaling under noise**: giving the model more time to think (longer CoT) lowers accuracy in the presence of distractors — reasoning capacity becomes a liability when context is polluted

> "You cannot reason your way out of bad context, and you cannot compute your way out of distraction."

## Agentic Collapse

In agentic loops, distractor errors compound: error from step t becomes part of context for step t+1. A system at 90% per-step accuracy → ~53% success after 6 steps, with active distractors making degradation faster (model over-trusts its own previous outputs → emergent misalignment, context rot).

## Wrong Metrics

Traditional IR metrics (nDCG, MAP, MRR) assume:
1. Monotonic decay by rank position (human scan model)
2. Irrelevant documents have utility = 0 (neutral, not harmful)

Both assumptions break for LLMs. A retriever can score high on nDCG while consistently injecting poisonous distractors.

**UDCG (Utility and Distraction-aware Cumulative Gain)**: assigns negative utility to distractors based on whether a passage makes the model answer *incorrectly* or answer *when it should abstain*. Reports 36% better correlation with end-to-end accuracy vs. classic IR metrics.

**Key implication:** precision > recall in the agentic era. A miss costs less than a distractor.

## Defensive Retrieval

Three changes to break the MAD cycle:

1. **What you measure**: move from relevance to utility; assign negative utility to distractors
2. **What you inject**: treat each extra chunk as a liability; prefer dynamic-k over "always return k"; stop only when sufficiency is met
3. **What you do under uncertainty**: make abstention a first-class outcome → retry with different query/filters/tool

## Related Concepts

- [[Agentic Search]]
- [[LLM as Judge]]
- [[Retrieval Pipeline]]
- [[Search Evaluation]]
