---
type: concept
title: "PLAID"
aliases: ["PLAID engine", "ColBERTv2 PLAID"]
tags: [concept, multi-vector, late-interaction, neural-ir, vector-search]
created: 2026-10-20
---

# PLAID

**PLAID** is the retrieval engine behind [[ColBERT|ColBERTv2]] for multi-vector [[Late Interaction]] search. It generates candidates with the *single-vector (SV) heuristic*: each query token is searched individually against the document token vectors, matching documents are collected (and deduplicated), and the candidates are then scored with full MaxSim/Chamfer similarity.

---

## As the Baseline for MUVERA

PLAID is the state-of-the-art baseline the [[MUVERA]] paper measures against ([[MUVERA - Multi-Vector Retrieval via Fixed Dimensional Encodings]]):

- The SV heuristic can miss true nearest neighbours and is costly and sensitive to parameter tuning.
- To match the deduplicated SV heuristic's recall on [[MS MARCO]], MUVERA's fixed dimensional encodings retrieve 1.75–3.75× fewer candidates at 4096 dims and 2.6–5× fewer at 10240 dims.
- End to end, MUVERA reports 10% higher Recall@k and 90% lower latency than PLAID on average across six [[BEIR]] datasets. On MS MARCO it stays within 0.4% of PLAID rather than beating it, which the authors suggest is possibly because PLAID was carefully tuned for that dataset.

Practitioners in the [[Muvera - Making Multi-Vector Retrieval as Fast as Single-Vector Search (HN Discussion)|Hacker News discussion]] framed the difference as PLAID needing specific index structures and clustering assumptions, where MUVERA reuses any single-vector [[Maximum Inner Product Search|MIPS]] index.

## Related Concepts
- [[ColBERT]] — the model PLAID serves
- [[Late Interaction]] — the scoring paradigm
- [[MUVERA]] — the fixed-dimensional alternative to the SV heuristic
- [[Maximum Inner Product Search]]

## Related Articles
- [[MUVERA - Multi-Vector Retrieval via Fixed Dimensional Encodings]]
- [[MUVERA - Transforming Multi-Vector Information Retrieval Through Fixed Dimensional Encodings]]
- [[Muvera - Making Multi-Vector Retrieval as Fast as Single-Vector Search (HN Discussion)]]

## Companies
- [[LightOn AI]] — ships NextPlaid / FastPlaid multi-vector engines
