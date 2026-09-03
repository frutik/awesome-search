---
type: topic
aliases:
  - embedding model
  - embedding models
  - text embedding models
  - dense retrieval models
tags:
  - topic
  - embeddings
  - dense-retrieval
  - model-selection
  - multilingual
related_concepts:
  - "[[Embeddings]]"
  - "[[Dense Embeddings]]"
  - "[[Matryoshka Embeddings]]"
  - "[[Bi-Encoder]]"
  - "[[Embedding Fine-tuning]]"
  - "[[Scalar Quantization]]"
related_topics:
  - "[[Vector Search Tradeoffs]]"
  - "[[Multilingual Search]]"
  - "[[Dimensionality Reduction vs Quantization]]"
  - "[[Retrieval Benchmarks and Leaderboards]]"
  - "[[Model Selection and Fine-Tuning Evaluation]]"
created: 2026-08-05
---

# Embedding Models Compared

## Overview

The embedding model is the single most consequential choice in a [[Dense Embeddings|dense retrieval]] stack. It fixes your vector dimensionality (and therefore index cost), your maximum chunk size, your language coverage, and your serving latency — and changing it later means re-embedding the entire corpus.

This note is a decision aid, not a leaderboard. Public rankings move monthly; the tradeoff structure does not. The model roster below is a snapshot as of August 2026 — the axes above it should age well.

## The Axes That Actually Matter

Before comparing models, know which of these bind for you:

- **Dimensionality** — drives index size and query latency more than model quality does. A 3072-dim index costs 4× a 768-dim one. [[Matryoshka Embeddings|MRL]] support lets you truncate after the fact, which is now table stakes.
- **Context length** — mostly a red herring. A 32K-token model does not save you from chunking; long inputs get averaged into mush. Matters for whole-document embedding, not passage retrieval.
- **Multilingual coverage** — a model trained on 100+ languages is not equally good in all of them. Check your actual languages, not the count.
- **Open weights vs API** — determines whether you can fine-tune, quantize, and self-host. For high-volume e-commerce search, per-token API pricing usually loses to a self-hosted small model.
- **Instruction / prefix awareness** — several models require specific prompts (`query:` / `passage:`, or task instructions). Mismatching them between indexing and query time is the most common silent quality bug in dense retrieval.
- **Serving footprint** — an 8B embedding model needs a GPU. A 300M model runs on CPU in single-digit milliseconds. For first-stage retrieval at scale, the small model usually wins on total system quality because you can afford to run it everywhere.

## Proprietary API Models

**Gemini Embedding 2** (Google) — natively multimodal (text, images, video, audio, PDFs) into one 3072-dim space, with MRL truncation.
- *Strengths*: strongest general-purpose quality at the top of English and cross-lingual boards; genuinely unified multimodal space; long-document handling.
- *Weaknesses*: 3072 dims is expensive to index at scale unless you truncate; Google Cloud lock-in; no self-hosting, so no domain fine-tuning.

**OpenAI `text-embedding-3-large` / `-small`** — 3072 / 1536 dims, adjustable via the `dimensions` parameter, ~8K context.
- *Strengths*: trivially easy to adopt; `-small` is very cheap and adequate for most RAG; dimension reduction built in.
- *Weaknesses*: shipped January 2024 and still has no announced successor — it has been overtaken by open-weight models on multilingual and retrieval benchmarks. English-centric, text-only, no fine-tuning.

**Cohere `embed-v4.0`** — 1536 default (256/512/1024/1536), 128K context, handles text, images, and PDFs.
- *Strengths*: by far the longest context of the major APIs; strong on mixed-modality business documents; compressed-embedding support for cheap indexes.
- *Weaknesses*: proprietary; per-token cost dominates at e-commerce query volumes.

**Voyage 4 family** — `voyage-4-large` / `-4` / `-4-lite`, 1024 default (256–2048), 32K context, plus domain variants (`voyage-code-3`, `voyage-finance-2`, `voyage-law-2`) and an open-weight `voyage-4-nano`.
- *Strengths*: consistently strong retrieval quality per dollar; the domain-specific variants are meaningfully better in-domain than any general model; nano is open-weight.
- *Weaknesses*: smaller ecosystem and less tooling integration; domain variants only help if your domain is one of the three.

## Open-Weight General Purpose

**Qwen3-Embedding** (0.6B / 4B / 8B) — Apache 2.0, 32K context, 32–4096 dims via MRL, 100+ languages, instruction-aware. Took #1 on the MTEB multilingual board on release.
- *Strengths*: best open-weight quality available; permissive license; the 0.6B is the current sweet spot for quality-per-GPU-dollar; instruction-awareness lets one model serve retrieval, clustering, and classification.
- *Weaknesses*: the 8B needs real GPU capacity to serve; instruction prompts must match exactly between index and query time or quality collapses silently.
- See [[Qwen3 Embedding Series]], [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]]

**BGE-M3** — multi-functional: emits dense, sparse, and multi-vector ([[ColBERT]]-style) representations from one model. 8192 context, 100+ languages.
- *Strengths*: one model covers [[Hybrid Search]] end to end — no second sparse model to train or serve; still the reliable multilingual workhorse.
- *Weaknesses*: 2024-vintage quality, now beaten by newer models on pure dense retrieval; the three-in-one output complicates the serving path.

**multilingual-e5** (`-large` / `-base` / `-small`) — the pragmatic production default for years.
- *Strengths*: extremely well understood; quantizes cleanly (INT8) with little quality loss; `-small` delivers sub-20ms CPU inference, which makes it viable for scoring at billions-of-pairs scale and a common [[Knowledge Distillation]] target.
- *Weaknesses*: 512-token limit; aging quality; **requires `query:` / `passage:` prefixes** — omitting them is the classic silent failure.

**Jina Embeddings v5** — `text-small` (677M, Qwen3-0.6B backbone, 1024d) and `text-nano` (239M, EuroBERT backbone, 768d), both 32K context with MRL down to 32 dims; `v5-omni` variants add image, audio, and video in a back-compatible space.
- *Strengths*: distills large-model quality into sub-1B models; aggressive MRL truncation cuts index cost hard; existing text indexes stay valid when you add multimodal content — no reindex.
- *Weaknesses*: newer and less battle-tested in production; commercial licensing needs checking for the hosted variants.

**EmbeddingGemma** (300M) — Google's on-device model, 768 dims truncatable to 512/256/128, 100+ languages.
- *Strengths*: runs offline on a phone or laptop; best-in-class for its size; permissive enough for embedded and edge use.
- *Weaknesses*: capacity-limited — it will not match a 4B model on hard or long-tail queries.

## Sparse and Late-Interaction Alternatives

Dense embeddings are not the only option, and often not the best first stage. The vault covers these separately:

- [[SPLADE]] and [[ELSER]] — [[Learned Sparse Retrieval]], keeps term-level interpretability and inverted-index serving
- [[ColBERT]] and [[Late Interaction]] — token-level matching, higher quality, higher storage
- [[Hybrid Search]] — combining lexical and dense, usually the strongest practical baseline

## Choosing

1. **Do not trust the leaderboard.** Public benchmarks measure general-domain performance. Real evaluations routinely find that a mid-ranked model wins on in-domain data while the board leader underperforms. Build a [[Judgment Lists|judgment list]] on your own queries first — see [[How to Choose the Best Model for Semantic Search]] and [[Retrieval Benchmarks and Leaderboards]].
2. **Fine-tuning beats model shopping.** A fine-tuned small model on your domain typically beats a larger general model off the shelf, at a fraction of the serving cost. See [[Embedding Fine-tuning]] and [[Model Selection and Fine-Tuning Evaluation]].
3. **Budget the index, not the model.** Embedding inference is a one-time cost per document; the index is forever. See [[Why Are Embeddings So Cheap]] and [[Dimensionality Reduction vs Quantization]].
4. **Check the prefix contract** before blaming the model for bad results.

## Related

- [[The Generalization Cliff]] — why leaderboard rankings for these models don't transfer to your domain
- [[Vector Search Tradeoffs]] · [[Multilingual Search]] · [[E-commerce Search]]
- [[Retrieval Benchmarks and Leaderboards]] — where these rankings come from
- [[MTEB]] · [[BEIR]] — the benchmarks themselves
- [[Sentence Transformers]] — the standard library for serving and fine-tuning open-weight models
- [[Dimensionality Reduction vs Quantization]] — the compression axis behind the dimensionality tradeoff
- [[Honey, I Shrunk the Embeddings - Matryoshka vs PCA]] — how far three of these models compress before nDCG@10 falls off, and whether MRL support is the advantage it looks like
