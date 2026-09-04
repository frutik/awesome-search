---
type: article
title: "Fine-Tuning Sparse Embeddings for E-Commerce Search (Parts 1–5)"
source: https://qdrant.tech/articles/sparse-embeddings-ecommerce-part-1/
author: "[[Thierry Damiba]]"
published: 2026-03-09
company: "[[Qdrant]]"
tags:
  - article
  - sparse-retrieval
  - splade
  - fine-tuning
  - e-commerce
  - neural-ir
  - search-evaluation
topics:
  - "[[E-commerce Search]]"
  - "[[Learned Sparse Retrieval]]"
concepts:
  - "[[SPLADE]]"
  - "[[Sparse Embeddings]]"
  - "[[BM25]]"
  - "[[Hard Negative Mining]]"
  - "[[Embedding Fine-tuning]]"
  - "[[Search Evaluation]]"
tools:
  - "[[Qdrant Vector DB]]"
  - "[[Sentence Transformers]]"
  - "[[qdrant-sparse-finetune]]"
datasets:
  - "[[Amazon ESCI Dataset]]"
  - "[[WANDS Dataset]]"
  - "[[Home Depot Product Search Relevance]]"
  - "[[MS MARCO]]"
created: 2026-07-27
---

# Fine-Tuning Sparse Embeddings for E-Commerce Search

A five-part engineering series by [[Thierry Damiba]] ([[Qdrant]]) that fine-tunes a [[SPLADE]] sparse retriever on e-commerce catalog data, measures it against [[BM25]] and off-the-shelf SPLADE, tests how far it transfers across catalogs, and packages the whole pipeline as [[qdrant-sparse-finetune]]. The companion talk is [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]].

The through-line: **off-the-shelf SPLADE is trained on [[MS MARCO]] web search, and e-commerce catalogs are not web search.** Fine-tuning on catalog data closes most of that gap, but at a measurable cost to generality.

---

## Part 1 — Why Sparse Embeddings Beat BM25

🔗 https://qdrant.tech/articles/sparse-embeddings-ecommerce-part-1/

The case for [[Learned Sparse Retrieval]] in product search: dense embeddings blur exact matches and offer no interpretability, while sparse representations preserve per-term signal through an inverted index — which is what SKUs, sizes, and model numbers need. SPLADE adds learned [[Query Expansion]] on top: "summer dress" reaches "sundress", "floral", "cotton".

Two models were published to Hugging Face: `splade-ecommerce-esci` (single-domain) and `splade-ecommerce-multidomain`.

## Part 2 — Training SPLADE on Modal

🔗 https://qdrant.tech/articles/sparse-embeddings-ecommerce-part-2/

Training starts from **`distilbert/distilbert-base-uncased`**, not from an existing SPLADE checkpoint — deliberately, so the gain attributable to domain fine-tuning is measurable from a general-language baseline.

**Architecture** ([[Sentence Transformers]] v5 modules):

| Module | Role |
|---|---|
| `MLMTransformer` | Emits logits over the full vocabulary |
| `SpladePooling` | Max over tokens, ReLU activation |

**Loss** — `SpladeLoss` combines `SparseMultipleNegativesRankingLoss` (other products in the batch act as negatives) with sparsity regularization:

- Query regularizer: **5e-5** (higher → sparser queries)
- Document regularizer: **3e-5** (lower, because product descriptions need more terms to carry all attributes)

**Data** — [[Amazon ESCI Dataset]], 1.2M+ query-product pairs across four grades (Exact / Substitute / Complement / Irrelevant). **Exact and Substitute are used as positives.** Product text = title + bracketed brand + description + bullets, capped at 512 characters.

**Compute** — Modal, A100, 6-hour timeout, persistent volumes for checkpoints. Batch size 32, LR 2e-5, 1 epoch, warmup ratio 0.1, fp16. A 100K-sample run trains in **~6 minutes for under $1**; the full 1.2M set takes hours.

## Part 3 — Evaluation and Hard Negative Mining

🔗 https://qdrant.tech/articles/sparse-embeddings-ecommerce-part-3/

Evaluated on 2,000 test queries against 10,000 products. **nDCG@10** is the primary metric, chosen because it rewards putting Exact matches at the top and penalizes relevant results that rank low.

| Model | nDCG@10 | MRR@10 | vs BM25 |
|---|---|---|---|
| BM25 (baseline) | 0.305 | 0.313 | — |
| SPLADE (off-the-shelf) | 0.326 | 0.339 | +7.2% |
| SPLADE (fine-tuned) | **0.389** | 0.387 | **+27.5%** |

Fine-tuned beats off-the-shelf by **19%**. (Part 1 quotes a slightly different rounding — 0.388 / 0.301 / 0.324 and "29%" — the Part 3/4 figures above are the detailed evaluation.) The series is explicit that these run on a 100k-product / 10k-query subsample and are **not comparable to official ESCI benchmarks**.

### The ANCE loop

[[Hard Negative Mining]] with the search engine inside the training loop:

1. Index products into [[Qdrant Vector DB]] with the current checkpoint
2. Retrieve top-K for each query
3. Filter out the known-relevant ones — what remains is what the model *wrongly believes* is relevant
4. Train on (query, positive, hard_negatives) triplets
5. Repeat with the updated model

Worth **5–10% on top of basic training**, and cheap to run: sparse retrieval mines at sub-millisecond per query in Qdrant.

### What fine-tuning actually changed

- **Query expansion** — "wireless earbuds" began pulling in "bluetooth", "airpods", "tws"
- **Term weighting** — brand names up, generic words like "good" down
- **Domain vocabulary** — "refurbished" gained real weight; web-search terms were deprioritized

## Part 4 — Specialization vs Generalization

🔗 https://qdrant.tech/articles/sparse-embeddings-ecommerce-part-4/

The ESCI-trained model tested across catalogs:

| Evaluated on | Fine-tuned nDCG@10 | vs BM25 |
|---|---|---|
| Amazon ESCI (in-domain) | 0.389 | +27.5% |
| [[WANDS Dataset]] (Wayfair furniture) | 0.355 | +7.9% |
| [[Home Depot Product Search Relevance]] | 0.384 | +10.0% |
| [[MS MARCO]] (general web) | 0.751 | **−17.9%** |

On Home Depot the **off-the-shelf model actually wins** (0.391 vs 0.384) — domain fine-tuning on Amazon does not automatically transfer to another retailer. And on MS MARCO the fine-tuned model falls well below BM25's 0.915: clear catastrophic forgetting, with Amazon-specific vocabulary ("renewed") and brand-heavy query patterns overwriting general language ability.

**Multi-domain training** (ESCI + WANDS + Home Depot, 50K samples each) trades peak for consistency:

| Evaluated on | Multi-domain nDCG@10 | vs single-domain |
|---|---|---|
| Amazon ESCI | 0.372 | −4.4% |
| WANDS | 0.366 | +3.1% |
| Home Depot | 0.410 | +6.8% |
| MS MARCO | 0.829 | +10.4% |

### Guidance

- **Single retailer with training data** → domain-specific fine-tuning, maximum performance on your catalog
- **Marketplace / multi-retailer** → multi-domain training, consistency over peak
- **No training data** → off-the-shelf, cold start

## Part 5 — From Research to Product

🔗 https://qdrant.tech/articles/sparse-embeddings-ecommerce-part-5/

Everything above, packaged as [[qdrant-sparse-finetune]] — see that note for install, config defaults, and the CLI / Python / dashboard interfaces.

---

## Why It Matters

The series is one of the few end-to-end, numbers-attached accounts of domain-adapting a learned sparse retriever for product search. Three things generalize beyond the specific models:

1. **Domain fine-tuning of sparse models pays** — +27.5% nDCG@10 over BM25, where off-the-shelf SPLADE managed only +7.2%.
2. **The transfer story is honest and negative** — a model tuned on one catalog is not a general e-commerce model, and can lose to the off-the-shelf baseline on a neighboring catalog.
3. **A search engine in the training loop is practical** — [[Hard Negative Mining]] via live retrieval is cheap when the representations are sparse.

## Related Concepts

- [[SPLADE]] — the model family being fine-tuned
- [[Learned Sparse Retrieval]] · [[Sparse Embeddings]] — the parent approach
- [[Hard Negative Mining]] — the ANCE loop
- [[Embedding Fine-tuning]] — the dense-side analogue
- [[BM25]] — the baseline throughout

## Related Topics


## Related Articles

- [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]] — the conference talk covering this work
- [[Fine-Tuning Text Embeddings For Domain-Specific Search]] — same problem, dense side
- [[The Complete Guide to Fine-Tuning Embedding Models]] — loss/dataset taxonomy
- [[SPLADE for Sparse Vector Search Explained]] — mechanism background
- [[Elastic Learned Sparse Encoder ELSER Retrieval Performance]] — the zero-shot-generalist counterposition

## People

- [[Thierry Damiba]] — author
- [[Evgeniya Sukhodolskaya]] — presented this work at [[MICES]]
