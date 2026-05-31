---
title: "Pairwise Relevance Evaluation"
aliases: ["pairwise comparison", "LHS/RHS evaluation", "pairwise judgment"]
tags:
  - concept
  - search-evaluation
  - llm-judge
---

# Pairwise Relevance Evaluation

## Definition

A relevance judgment method where an evaluator (human or LLM) is shown **two candidates side-by-side** — conventionally called **LHS** (left-hand side) and **RHS** (right-hand side) — and asked which is more relevant to a given query. Produces relative preference labels rather than absolute scores.

## Why Pairwise Over Point-wise?

Point-wise scoring (rate this document 0–3) is hard to calibrate consistently — annotators disagree on what "2 out of 3" means. Pairwise comparison is cognitively simpler: "which of these two is better?" Humans and LLMs both agree more reliably on relative preferences than on absolute grades.

## The LHS/RHS Prompt Format

A canonical pairwise LLM judge prompt:

```
Which of these products is more relevant to the search query?

Query: entrance table

Product LHS: aleah coffee table
Product RHS: marta coffee table

Only respond 'LHS' or 'RHS' if you are confident.
Otherwise respond 'Neither'.
```

Forcing a binary choice (LHS or RHS, no Neither) maximizes recall but lowers precision (~75%). Allowing "Neither" and requiring double-check consistency raises precision (~91%) at the cost of recall (~12%).

## Double-Check (Swap) Technique

Run the same prompt twice with LHS and RHS swapped. Accept the judgment only when both orderings agree:

- Pass 1: LHS=product A, RHS=product B → LHS
- Pass 2: LHS=product B, RHS=product A → RHS (consistent — both prefer A)

If the two passes disagree, label the pair "Neither". This detects positional bias and low-confidence judgments.

## Combining with Classical ML

Individual pairwise LLM judges per attribute (name, description, category, classification) can be treated as **binary features** for a downstream classifier. A decision tree trained on these features outperforms any single judge:

| Feature combination | Precision | Recall |
|---|---|---|
| Best single judge (force+double-check) | 91.7% | 65.2% |
| 5-feature decision tree | 96.7% | ~40% |
| Extreme high-precision tree | 100% | 1.3% |

See [[Classic ML to Cope with Dumb LLM Judges]] for the full experiment.

## Tradeoffs

| Approach | Precision | Recall | Cost |
|---|---|---|---|
| Force LHS/RHS | ~75% | ~100% | 1× |
| Allow Neither | ~85% | ~50% | 1× |
| Double-check swap | ~91% | ~12% | 2× |
| ML ensemble of judges | ~97% | ~40% | N× per attribute |

## Comparison to Other Paradigms

| Paradigm | Input | Output | Scalability | Signal strength |
|---|---|---|---|---|
| [[Pointwise Relevance Evaluation\|Pointwise]] | (query, doc) | absolute grade | O(n) | weakest |
| **Pairwise** | (query, doc_A, doc_B) | preference | O(n²) | strong |
| [[Listwise Relevance Evaluation\|Listwise]] | (query, [doc_1…doc_k]) | ranked order | O(k per query) | strongest |

## Related Concepts

- [[Pointwise Relevance Evaluation]] — scores items independently; simpler but weaker signal
- [[Listwise Relevance Evaluation]] — ranks full list; most holistic, best for reranking evaluation
- [[LLM as Judge]] — the evaluation paradigm pairwise comparison is used within
- [[Judgment Lists]] — output that pairwise judgments contribute to
- [[Search Evaluation]] — broader context
- [[Decision Tree]] — classical ML used to ensemble pairwise signals
- [[Precision-Recall Tradeoff]] — fundamental tension in the Neither/force choice

## Articles

- [[What AI Engineers Should Know about Search]] — [[Doug Turnbull]]; mentions pairwise as an LTR training paradigm (SVMRank)
- [[Classic ML to Cope with Dumb LLM Judges]] — [[Doug Turnbull]]; per-attribute LHS/RHS LLM judges as ML features → decision tree; 96.7% precision on 40% of pairs
- [[Search Quality Assurance with AI as a Judge]] — [[Tao Ruangyam]]; Zalando production pipeline using pairwise-style LLM evaluation at scale

## People

- [[Doug Turnbull]] — explored LHS/RHS prompt variants and ML ensembling of pairwise judges
