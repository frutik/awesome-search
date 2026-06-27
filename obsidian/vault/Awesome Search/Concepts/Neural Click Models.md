---
title: "Neural Click Models"
aliases: ["neural click model", "NCM", "CACM", "context-aware click model", "GraphCM", "deep click model", "neural examination model"]
tags:
  - concept
  - search
  - evaluation
  - ranking
  - behavioral
  - deep-learning
created: 2026-06-27
---

# Neural Click Models

## Definition

Neural click models replace the hand-specified parametric structure of classical [[Click Models]] (PBM, Cascade, DBN, UBM) with neural networks that learn **distributed representations** of queries, documents, and browsing state. Instead of estimating one tabular attractiveness/examination parameter per (query, document) pair, they encode context into embeddings and predict click probability from learned functions — letting the model generalize to rare and unseen query-document pairs.

They serve the same purpose as classical click models — de-biasing click logs to recover relevance for [[Learning to Rank]] and offline evaluation — but trade interpretability for expressiveness and tail coverage.

---

## Why Go Neural

Classical click models have two structural weaknesses neural models target:

1. **Sparsity / no generalization.** PBM, DBN, and UBM store parameters *per query-document pair*. Tail queries and freshly indexed documents have too few impressions to estimate these reliably — the model has nothing to fall back on. Neural models share parameters through embeddings, so signal transfers across similar queries and documents.
2. **Rigid behavioral assumptions.** The cascade family hard-codes a specific scan-and-stop process and strong independence assumptions. Neural sequence models learn the dependency between examinations and prior clicks from data rather than asserting it.

## Common Models

### NCM (Neural Click Model)
Introduced by Borisov et al. (WWW 2016). Models a browsing session as a **sequence of vector states** processed by an RNN: at each rank the hidden state encodes everything seen so far, and click probability is read off from that evolving state. Drops the explicit [[Position Bias|examination hypothesis]] — the network learns examination and relevance jointly rather than factoring them by hand.

### CACM (Context-Aware Click Model)
Chen et al. (SIGIR 2020). Keeps the classical relevance × examination factorization but makes **both components neural and context-aware**: a relevance estimator and an examination predictor are learned over query/document/session context, then combined. More interpretable than NCM while still benefiting from learned representations.

### GraphCM
Frames click modeling as inference over a **query–document bipartite graph** and uses a graph neural network to propagate signal between neighboring nodes. Directly attacks the data-sparsity problem: a tail document inherits behavioral signal from documents that co-occur with the same queries.

### Two-Tower / Additive Position Models
Used in industrial unbiased LTR (e.g. Huawei's PAL, and additive two-tower setups at web-search scale). One tower predicts **examination from position-only features**, a second predicts **relevance from query-document features**, and the towers are combined (multiplicatively or additively). At serving time the position tower is dropped, leaving an unbiased relevance score. A neural restatement of the [[Position Bias|examination hypothesis]] trained end-to-end with the ranker.

---

## Relationship to Unbiased LTR

Neural click models are one half of the unbiased learning-to-rank picture:

- **Click-model route** — fit a (neural) click model to logs, then use its relevance posteriors as soft labels for [[Learning to Rank]].
- **Counterfactual route** — estimate propensities (often via a neural examination model) and reweight clicks with **IPS** (Inverse Propensity Scoring) directly inside the ranking loss.

The boundary blurs: two-tower additive models *are* both the propensity estimator and the ranker, trained jointly.

## Tradeoffs

| Strength | Cost |
|---|---|
| Generalizes to tail / cold-start query-doc pairs | Data-hungry; needs large click logs |
| Captures rich session and context dependencies | Lower interpretability than PBM/DBN parameters |
| Shares signal via embeddings and graphs | Harder to extract clean, reusable propensities |
| Trains end-to-end with the ranker | More moving parts; risk of feedback loops if not debiased |

---

## Related Concepts

- [[Click Models]] — the classical (PBM/Cascade/DBN/UBM) family these extend
- [[Position Bias]] — the bias the examination tower is designed to absorb
- [[Click Signals]] — the raw log data neural click models are fit to
- [[Learning to Rank]] — downstream consumer of de-biased relevance estimates
- [[Implicit Judgments]] — click-derived labels that click models refine
- [[Session-Based Evaluation]] — neural click models operate over full sessions
