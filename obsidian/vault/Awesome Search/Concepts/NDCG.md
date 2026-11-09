---
type: concept
title: "NDCG (Normalized Discounted Cumulative Gain)"
aliases: ["nDCG", "normalized discounted cumulative gain", "DCG", "discounted cumulative gain", "CG", "cumulative gain"]
tags:
  - concept
  - search-evaluation
  - metrics
created: 2026-05-16
---

# NDCG (Normalized Discounted Cumulative Gain)

## Definition

NDCG is the most widely used ranking quality metric in information retrieval. It measures how well a ranked list puts the most relevant results at the top, accounting for the diminishing value of lower-ranked positions.

## Formula

**CG (Cumulative Gain)** — the simplest form, sums relevance scores with no position weighting:
```
CG@k = Σᵢ₌₁ᵏ rel_i
```
CG is position-insensitive — a relevant document at rank 10 counts the same as one at rank 1. Useful when position doesn't matter (e.g., measuring total coverage), but not for ranking quality.

**DCG (Discounted Cumulative Gain)** — adds a logarithmic discount so top positions matter more:
```
DCG@k = Σᵢ₌₁ᵏ  rel_i / log₂(i + 1)
```
where `rel_i` is the relevance score of the document at rank i.

**IDCG** (Ideal DCG): DCG of the perfect ranking.

**NDCG**:
```
NDCG@k = DCG@k / IDCG@k
```

Range: [0, 1]. NDCG@k = 1.0 means perfect ranking.

## Relevance Grades

NDCG supports graded relevance (unlike binary metrics):
| Grade | Meaning |
|-------|---------| 
| 0 | Not relevant |
| 1 | Marginally relevant |
| 2 | Relevant |
| 3 | Highly relevant |
| 4 | Perfect match |

The logarithmic discount means position 1 is worth much more than position 10 — reflecting user behavior (users rarely scroll far).

## Variants: "Flavors of NDCG"

Confusion arises because there are multiple valid formulations:

### Variant 1: Standard (Jarvelin & Kekalainen)
```
DCG = rel₁ + Σᵢ₌₂ᵏ rel_i / log₂(i)
```

### Variant 2: Burges (Microsoft/LightGBM default)
```
DCG = Σᵢ₌₁ᵏ (2^rel_i - 1) / log₂(i + 1)
```
The `2^rel - 1` transform emphasizes high-relevance documents more strongly.

Both normalize to NDCG the same way; the IDCG changes accordingly. Be explicit about which variant you use when comparing systems.

This is only one of *two* axes of ambiguity — the gain function (above) and the **normalization target** ("normalized to what?"). See [[NDCG Variants]] for the full two-axis treatment, library defaults, and practical guidance.

## NDCG@k Choices

- **NDCG@3**: measures top-3, relevant for autocomplete/instant answers
- **NDCG@5**: common for web search (above the fold)
- **NDCG@10**: most common standard benchmark (MS MARCO, BEIR)
- **NDCG@100**: measures recall quality in first-stage retrieval

## Computing NDCG

```python
import numpy as np

def dcg_at_k(relevances, k):
    relevances = np.asarray(relevances[:k], dtype=float)
    n = len(relevances)
    if n == 0:
        return 0.0
    discounts = np.log2(np.arange(2, n + 2))
    return np.sum((2**relevances - 1) / discounts)

def ndcg_at_k(relevances, k):
    ideal = sorted(relevances, reverse=True)
    return dcg_at_k(relevances, k) / dcg_at_k(ideal, k) if dcg_at_k(ideal, k) > 0 else 0.0
```

## NDCG in Practice

NDCG requires **relevance judgments** ([[Judgment Lists]]) — human-rated (query, document) pairs. Creating judgments is expensive; sampling strategy matters enormously ([[Search Evaluation]]).

**Benchmark usage**: MS MARCO, TREC, BEIR benchmarks use NDCG@10 as primary metric for comparing retrieval systems. [[ELSER]] reports 17% NDCG@10 improvement over BM25; [[Matryoshka Embeddings]] compares at 99% NDCG relative to full-dimension embeddings.

## NDCG Limitations in Agentic Systems

Standard NDCG assumes irrelevant documents are neutral (grade 0). In LLM/RAG pipelines, some documents actively harm accuracy by introducing distractors. [[UDCG]] extends NDCG with negative utility scores for distractor documents.

### NDCG Limitations in eCommerce Search

[[Andreas Wagner]] argues that NDCG's popularity in benchmarks and papers is no reason to make it the default optimization target for product search ([[Why nDCG Misleads eCommerce Search]]):

- **The discount is assumed, not measured.** The log curve rarely matches how shoppers actually examine results; if NDCG is used, its discount should come from measured attention across positions — the territory of [[Click Models]].
- **Grids break the curve.** Results are shown as product grids, not lists. On desktop the first four items can be equally visible, on mobile only one or two; real examination drops in steps at grid-row and viewport boundaries, while NDCG discounts position 2 sharply against position 1 on every device. See [[Position Bias]] and [[Presentation Bias]].
- **k is a decision.** NDCG@5 or @10 treats everything below the cutoff as irrelevant although shoppers scroll and compare far more; @50 or @100 covers more of the ranking but leaves the discount problem intact.
- **Weak link to business KPIs.** Once images, prices, brands and promotions drive clicks and purchases, a better NDCG does not automatically mean a better shop.
## Related Concepts

- [[MRR]] — simpler ranking metric (binary relevance, first relevant result)
- [[MAP]] — binary-relevance alternative; considers all relevant document positions
- [[Precision and Recall]] — non-ranking variants
- [[UDCG]] — NDCG extension with negative utility for distractors (agentic RAG)
- [[Judgment Lists]] — required input for NDCG computation
- [[Search Evaluation]] — broader evaluation framework
- [[LLM as Judge]] — automated relevance judgments
- [[Kendall Rank Correlation]] — contrast: measures how much two orderings differ, with no relevance labels required, unlike NDCG
- [[ERR]] — cascade-model alternative: credits a result only for the users not already satisfied above it


**Related videos:**
- [[Roman Grebennikov - Personalizing Search Results in Real-Time]] — 🎥 the "perfect ranking" behind NDCG encodes a business goal: weighting purchases over clicks (or sorting by margin) changes what the metric optimizes

- [[NDCG-m]] — normalises against a fixed all-max-grade ideal so corpus coverage shows up in the score
- [[NDCG-f]] — computes NDCG over labeled results only, as a regression check when labels are incomplete

## Articles

- [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]] — [[Joanna Marhula]], [[Mateusz Sidor]]; Allegro correlates LLM relevance labels with result position (position-1 mismatches critical, position-20 mismatches minor) to compute NDCG

- [[Search golden sets are anything but]] — [[Doug Turnbull]]; NDCG can hit 1 when a corpus has few relevant results, and unlabeled results skew it, motivating NDCG-m and NDCG-f

- [[Why nDCG Misleads eCommerce Search]] — [[Andreas Wagner]]; the log discount, small k and weak KPI correlation make NDCG a poor default target for product grids

## People

- [[Daniel Tunkelang]] — frequent NDCG commentary; Evaluating Search series
- [[Doug Turnbull]] — "Flavors of NDCG" post; practical NDCG guidance
