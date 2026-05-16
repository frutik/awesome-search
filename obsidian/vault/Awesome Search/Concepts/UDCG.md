---
title: UDCG (Utility and Distraction-aware Cumulative Gain)
aliases:
  - UDCG
  - Utility and Distraction-aware Cumulative Gain
tags:
  - concept
  - search-evaluation
  - metrics
  - agentic-search
---

# UDCG (Utility and Distraction-aware Cumulative Gain)

## Definition

UDCG is a retrieval evaluation metric designed for agentic and RAG systems where retrieved documents are consumed by an LLM rather than scanned by a human. It extends [[NDCG]] by assigning **negative utility scores** to distractors — passages that cause the model to answer incorrectly.

Introduced by Trappolini et al. to address the fundamental inadequacy of traditional IR metrics in the agentic era.

## Why Standard Metrics Fail

[[NDCG]], [[MAP]], and [[MRR]] were designed for human-facing search, where:
1. Relevance grades are monotonically non-negative (irrelevant = 0, perfect = 4)
2. Irrelevant documents are neutral — they waste a position but don't actively harm the user
3. Users can skip past bad results with minimal cost

Neither assumption holds for LLMs:
- Retrieved documents are **injected into context** and processed in parallel — there is no skipping
- Some passages are **actively harmful**: semantically plausible but factually wrong content that leads the model to incorrect conclusions
- A retriever can score high on nDCG@10 while consistently poisoning the context with high-confidence distractors

## The UDCG Formula

UDCG assigns utility scores based on **model behavior**:
- `u(d) > 0` — document helps the model answer correctly
- `u(d) = 0` — document is neutral / irrelevant
- `u(d) < 0` — document is a **distractor** (causes an incorrect answer)

```
UDCG@k = Σᵢ₌₁ᵏ  u(dᵢ) / log₂(i + 1)
```

Utility is derived empirically: include/exclude each document and observe whether model accuracy changes.

## Key Insight

> Precision is more valuable than recall in the agentic era, because **a miss costs less than a distractor**.

UDCG exposes that distractor injection — not just irrelevance — is the principal failure mode of retrieval in LLM pipelines. Systems optimizing for nDCG may produce worse agentic outcomes than systems with lower nDCG but fewer distractors.

Reported improvement: up to **36% better correlation** with end-to-end answer accuracy compared to traditional metrics.

## Implications for Retrieval Design

- Move from **relevance** to **utility** as the optimization target
- Treat context like an interface with explicit failure modes (see [[Clean Context]])
- Prefer **abstention** over injecting uncertain passages
- Use **dynamic-k** retrieval (stop when confidence drops) rather than fixed top-k

## Related Concepts

- [[NDCG]] — standard metric that UDCG extends with negative utility
- [[Clean Context]] — the goal UDCG incentivizes: context free of distractors
- [[Diversity Metrics]] — another extension of NDCG for coverage; UDCG extends it for harm
- [[Agentic Search]] — the context where UDCG matters most
- [[Search Evaluation]] — broader evaluation framework

## People

- Trappolini et al. — UDCG authors
- [[Lester Solbakken]] — UDCG metric advocacy and dynamic-k/abstention design

## Related Articles

- [[Mutually Assured Distraction]]
