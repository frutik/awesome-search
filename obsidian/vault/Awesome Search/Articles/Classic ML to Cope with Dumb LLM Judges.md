---
type: article
title: "Classic ML to Cope with Dumb LLM Judges"
source: "https://softwaredoug.com/blog/2025/01/21/llm-judge-decision-tree"
author:
  - "[[Doug Turnbull]]"
published: 2025-01-21
created: 2026-05-31
concepts:
  - "[[LLM as Judge]]"
  - "[[Pairwise Relevance Evaluation]]"
  - "[[Decision Tree]]"
  - "[[Ensemble Methods]]"
  - "[[Precision-Recall Tradeoff]]"
topics:
  - "[[Search Quality Assurance]]"
companies:
  - "[[Wayfair]]"
tags:
  - article
  - llm-judge
  - search-evaluation
  - machine-learning
---

# Classic ML to Cope with Dumb LLM Judges

**[[Doug Turnbull]]** shows how to combine many "dumb" single-attribute LLM judges into a smarter relevance prediction by treating their outputs as features for a classical ML decision tree classifier. Using the [[Wayfair]] WANDS open e-commerce dataset as ground truth, he evaluates a local LLM (run on a laptop) across four product attributes — name, description, category taxonomy, and classification — in multiple prompt variants, then trains a scikit-learn decision tree on the resulting feature table to predict human pairwise preference.

---

## Core Problem

Individual LLM judges are noisy. Forcing a judgment on every pair yields ~75% precision; allowing "Neither" and double-checking (asking both orderings) raises precision to ~91% but cuts recall to ~12%. The tradeoff is fundamental: you can have confident decisions on few pairs, or uncertain decisions on all.

## The ML Reframe

Each (query, LHS product, RHS product) triple evaluated across all attribute × variant combinations produces a **feature row**:

| Query | LHS | RHS | Name | Name (dbl chk) | Desc | Category | Human Label |
|---|---|---|---|---|---|---|---|
| entrance table | aleah coffee table | marta coffee table | Neither | LHS | LHS | RHS | LHS |

This is a **classification problem**: features are the per-attribute LLM predictions; label is human preference. A decision tree learns the right ensemble weighting.

## Results

- Best single variant: 91.72% precision / 65.2% recall (uber prompt, force+double-check)
- Decision tree top result: 96.7% precision on 40% of pairs (5-feature combination)
- Extreme high-precision mode: 100% precision on 1.3% of pairs

## Why Decision Trees?

Trees are interpretable — you can dump the learned structure and read off which attributes the classifier prioritizes (e.g., category preference evaluated before name preference). This doubles as an exploratory tool for understanding what drives relevance in your domain.

## Key Insight

Local LLMs can serve as **ML feature generators** for relevance: keep each LLM call dumb, simple, and cacheable; aggregate with fast classical ML at the end. This avoids one expensive "uber prompt" while matching or exceeding its precision.

## Prompt Variants Tested

- Force vs. Allow Neither
- Single pass vs. Double-check (swap LHS/RHS, require consistent answer)
- Four fields: product name, description, category hierarchy, product classification

---

## Related Concepts

- [[LLM as Judge]] — individual LLM calls as the raw signal
- [[Pairwise Relevance Evaluation]] — comparison-based judgment paradigm
- [[Decision Tree]] — classifier used to combine weak signals
- [[Ensemble Methods]] — conceptual framing of combining multiple weak judges
- [[Judgment Lists]] — end product of the relevance evaluation pipeline
- [[Search Evaluation]] — broader context

## Related Articles

- [[Improving Retrieval with LLM as a Judge]] — [[Jo Kristian Bergum]]; similar LLM judge framing at Vespa
- [[LLM-as-a-Judge When to Use Reasoning CoT and Explanations]] — [[Aparna Dhinakaran]]; when to add CoT to LLM judge prompts
- [[Using LLMs to Amplify Human Labeling and Improve Dash Search Relevance]] — [[Dmitriy Meyerzon]]; LLM calibrated on human labels for scale-up
- [[Search Quality Assurance with AI as a Judge]] — [[Tao Ruangyam]]; Zalando production pipeline using LLM judge at scale

## People

- [[Doug Turnbull]] — author; OpenSource Connections; softwaredoug.com
