---
type: article
title: "RouterRetriever: Routing over a Mixture of Expert Embedding Models"
source: https://arxiv.org/abs/2409.02685
author:
  - Hyunji Lee
  - Luca Soldaini
  - Arman Cohan
  - Minjoon Seo
  - Kyle Lo
published: 2024-09-04
tags:
  - article
  - paper
  - query-routing
  - dense-retrieval
  - domain-adaptation
  - aaai
concepts:
  - "[[Query Routing]]"
  - "[[Dense Vector Retrieval]]"
  - "[[LoRA]]"
  - "[[Embedding Fine-tuning]]"
  - "[[Zero-Shot Retrieval]]"
topics:
  - "[[Embedding Models Compared]]"
created: 2026-09-26
---

# RouterRetriever: Routing over a Mixture of Expert Embedding Models

**Authors:** Hyunji Lee (KAIST AI), Luca Soldaini, Arman Cohan, Minjoon Seo, Kyle Lo (KAIST AI, Allen Institute for AI, Yale)
**Venue:** AAAI 2025 · [arXiv 2409.02685](https://arxiv.org/abs/2409.02685) · [code](https://github.com/amy-hyunji/RouterRetriever) · [weights](https://hf.co/amy-hyunji/RouterRetriever)

## Summary

A general-purpose embedding model trained on [[MS MARCO]] is reasonable everywhere and best nowhere: domain-specific retrievers beat it on their own domains. The usual fixes are to retrain one model on everything (multi-task) or to adapt it per domain. RouterRetriever instead keeps **several domain experts and routes each query to one of them** — [[Query Routing]] applied not to data sources or retrieval strategies but to *which embedding model encodes the query*.

## How It Works

- **Experts are cheap.** One frozen base encoder (Contriever) plus one [[LoRA]] module per domain, each trained on that domain's data. Adding a domain means training one more LoRA, with a small parameter increase.
- **Pilot embeddings.** For each training instance in each domain, find which expert gives it the best embedding; group instances by winning expert and take the **centroid** of their base-encoder embeddings. Each centroid is a *pilot embedding* tied to an expert — up to T² of them for T domains.
- **Routing.** Embed the query with the base encoder, compute its average similarity to each expert's pilot embeddings, and pick the expert with the highest score. That expert encodes the query.

No router is trained, so experts can be added or removed without retraining anything else — the same example-centroid mechanism as a [[Query Routing|semantic router]], built from training data instead of hand-written utterances.

## Results

On [[BEIR]] (datasets including SciFact, HotpotQA, TREC-COVID, NFCorpus, Climate-FEVER, FiQA, ArguAna):

- **+2.1 nDCG@10** (absolute) over a single MS MARCO-trained model, and **+3.2** over a multi-task model.
- The pilot-embedding router beats routing techniques borrowed from language-model mixture-of-experts work by **+1.8** on average — those techniques "don't necessarily translate" to retrieval.
- Adding experts keeps helping, with diminishing returns, while multi-task training degrades past a certain number of domains.
- It also beats the single general model on domains with **no dedicated expert**.
- Compared with an instance-level oracle, the router's expert choices are sparser — it leans on fewer experts than would be ideal.

## Related Concepts

- [[Query Routing]] — here the routed resource is the encoder
- [[Dense Vector Retrieval]] · [[Embedding Fine-tuning]] · [[LoRA]]
- [[Zero-Shot Retrieval]] — the generalisation-to-unseen-domains claim
- [[MS MARCO]] · [[BEIR]]

## Related Notes

- [[LTRR - Learning To Rank Retrievers for LLMs]] — routing across a pool of retrievers, learned from downstream utility
- [[Query Routing - Direct Queries to the Right Source]] — the same centroid-of-examples routing, for data sources
- [[Embedding Models Compared]] — the no-single-best-model premise
