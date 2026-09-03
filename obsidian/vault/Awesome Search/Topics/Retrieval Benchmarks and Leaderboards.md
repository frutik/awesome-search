---
type: topic
aliases:
  - retrieval benchmarks
  - IR benchmarks
  - embedding leaderboards
  - benchmarking frameworks
tags:
  - topic
  - search-evaluation
  - benchmark
  - leaderboard
  - information-retrieval
related_concepts:
  - "[[Search Evaluation]]"
  - "[[Judgment Lists]]"
  - "[[NDCG]]"
  - "[[Zero-Shot Retrieval]]"
related_topics:
  - "[[Model Selection and Fine-Tuning Evaluation]]"
  - "[[Embedding Models Compared]]"
  - "[[Relevance Evaluation Tools Compared]]"
created: 2026-08-05
---

# Retrieval Benchmarks and Leaderboards

## Overview

Two entirely different activities share the word "evaluation":

- **Public benchmarks** measure *general capability* on someone else's data. They answer "is this model any good in the abstract," and they are how the field compares research results.
- **Your-data evaluation** measures *your search* on your queries and your corpus. It answers the only question that ships.

This note maps the first. For the second, see [[Relevance Evaluation Tools Compared]] (Quepid, RRE, and friends) and [[Relevance Program Setup]]. For how to actually run a comparison without fooling yourself, see [[Model Selection and Fine-Tuning Evaluation]].

The short version of the relationship: **public benchmarks build your shortlist; your own judgments make the decision.**

---

## The Benchmark Families

### Training Corpora and Ranking Tracks

**[[MS MARCO]]** — web-search passage and document ranking from Bing logs. Its real significance is not as a benchmark but as the *training corpus* underneath nearly every retrieval model shipped in the last several years. That ubiquity is also its problem: because almost everything trains on it, MS MARCO appearing in an evaluation is a contamination risk, and its judgments are shallow (typically one known-relevant passage per query, everything else assumed irrelevant).

**TREC** — the NIST evaluation conferences, and the methodological origin of essentially all of this. TREC's contribution is *pooled, deeply judged* test collections: multiple systems contribute candidates, human assessors judge the pool, and the result is a far denser relevance picture than MS MARCO's sparse labels. The Deep Learning tracks re-judged the MS MARCO corpus this way. [[TREC-COVID]] is the vault's worked example.

### Zero-Shot Generalization

**[[BEIR]]** — 18 heterogeneous datasets spanning fact-checking, QA, bio-medical, argument retrieval, and more. Models train elsewhere (usually MS MARCO) and are evaluated without tuning. BEIR became *the* proof of generality for a retrieval model, and it is where the durable finding "[[BM25]] is a stubbornly strong zero-shot baseline" comes from.

*Caveats*: increasingly saturated and trained-against; several constituent datasets are small or noisily labelled; the headline average hides enormous per-dataset variance.

### Aggregate Leaderboards

**[[MTEB]] / MMTEB** — the Massive Text Embedding Benchmark. Broader than retrieval: it spans classification, clustering, reranking, STS, summarization and more across many languages, which is why a model can top MTEB overall while being unremarkable at search. Two traps: **MTEB v1 and v2 scores are not comparable**, and there are several boards (English v2, multilingual/MMTEB) with different leaders — quoting "the MTEB leader" without saying which board is meaningless.

**[[RTEB]]** (Retrieval Embedding Benchmark) — announced in beta on 1 October 2025 specifically to attack the generalization gap. Its design is the interesting part: a **hybrid of open and private datasets**, where the private half is held by the maintainers and never released. A model scoring well on the open half and collapsing on the private half has been trained on the test.

The follow-on story is worth knowing: in 2026 the private column was **temporarily removed** after concerns that model vendors with access to the private data held a structural advantage. It is a live demonstration that "just keep the test set secret" creates its own governance problem — someone has to hold the secret, and that someone competes.

### Stress Tests

**[[BRIGHT]]** (ICLR 2025) — 1,385 reasoning-intensive queries from StackExchange, LeetCode, and math competitions, where relevant documents are connected to the query only by inference, not surface similarity. It is the most useful corrective in the field: a model scoring 59.0 nDCG@10 on MTEB scored **18.3** on BRIGHT. Whatever embedding models are doing, on this class of query it is not reasoning. Cite BRIGHT whenever someone claims retrieval is solved.

### Multilingual

**[[MIRACL]]** — human-annotated retrieval across 18 languages, built to avoid the translation artifacts that plague machine-translated multilingual sets. Together with MMTEB it is the honest test for the "supports 100+ languages" claims discussed in [[Embedding Models Compared]]. See also [[Multilingual Search]].

### Long-Tail

**[[LoTTE]]** (Long-Tail Topic-stratified Evaluation, from the [[ColBERT|ColBERTv2]] work) — StackExchange queries deliberately stratified toward long-tail topics rather than the head-heavy distributions of web-search corpora. Useful because head-query performance and tail-query performance diverge sharply, and most benchmarks over-sample the head.

### Domain and E-Commerce

Closest to product reality, and the vault already covers these in depth:

- **[[Amazon ESCI Dataset]]** / **[[ESCI-S Dataset]]** — multilingual product search with graded Exact/Substitute/Complement/Irrelevant labels; the standard e-commerce relevance set
- **[[WANDS Dataset]]** — Wayfair product search with dense human judgments
- **[[Home Depot Product Search Relevance]]** — older Kaggle set, still a reasonable smoke test

### A Different Axis Entirely

**[[ann-benchmarks]]** / **[[SIFT1M]]** measure *approximation fidelity* — recall against an exact scan — not relevance. A model with terrible relevance can post perfect recall@10. Keep the two axes separate; see [[Vector Search Evaluation]].

---

## How Leaderboards Mislead

- **Train/test contamination** — the dominant problem. Public test sets leak into training corpora, deliberately or not, and the leaderboard rewards it.
- **Benchmark fit ≠ model quality** — position reflects optimization *against the benchmark* as much as capability. It is routine for a board leader to lose to a mid-ranked model on in-domain data.
- **Averages hide everything** — a suite average smooths over the one task type that matches your use case.
- **Version incomparability** — MTEB v1 vs v2, dataset revisions, changed metric definitions.
- **Self-reported numbers** — vendor blog figures are often produced under favourable and unstated conditions (prefixes, `k`, reranking).
- **General domain ≠ your domain** — a benchmark built on Wikipedia and StackExchange predicts little about furniture SKUs or legal contracts.

---

## Benchmarking Frameworks

Libraries that actually run these suites — distinct from the your-data dashboards in [[Relevance Evaluation Tools Compared]]:

- **`mteb`** — the official runner; evaluates any [[Sentence Transformers]]-compatible model across MTEB/MMTEB/RTEB tasks and submits to the leaderboard. The path of least resistance for reproducing a published number.
- **`beir`** — the BEIR toolkit; standard loaders and evaluation for the suite, with support for lexical, dense, and reranking pipelines.
- **`ir_datasets`** — unified access to a very large catalogue of IR collections (TREC, MS MARCO, BEIR members and many more) with consistent loaders. Removes most of the misery of dataset wrangling.
- **`pytrec_eval`** — Python bindings to `trec_eval`, NIST's reference metric implementation. When two papers disagree on NDCG, this is the tiebreaker.
- **`ir_measures`** — one interface over several metric backends, so metric definitions stay consistent across tools.
- **`ranx`** — fast metric computation plus fusion methods and, importantly, **built-in statistical significance testing** — the piece most homegrown harnesses skip. See [[Statistical Significance in Search Evaluation]].
- **Sentence Transformers evaluators** — `InformationRetrievalEvaluator` and friends, for computing retrieval metrics *during* training at checkpoints. See [[Model Selection and Fine-Tuning Evaluation]].

---

## Using Benchmarks Well

1. **Shortlist, don't select.** Use leaderboards to get from 50 candidates to 3–5. Pick among those on your own judgments.
2. **Match the benchmark to the task.** Retrieval board, not the overall average. Multilingual board if you're multilingual. [[BRIGHT]] if your queries need inference.
3. **Read the per-dataset table**, never the headline average.
4. **Check the training data** for overlap with the benchmark you're citing.
5. **Prefer domain sets** — [[Amazon ESCI Dataset]] tells an e-commerce team more than all of MTEB.
6. **Treat a private-set drop as the real signal** where one is available.

---

## Related

- [[The Generalization Cliff]] — the argument this benchmark landscape is evidence for
- [[Model Selection and Fine-Tuning Evaluation]] — the methodology these feed into
- [[Embedding Models Compared]] — the models being ranked
- [[Search Evaluation]] · [[Judgment Lists]] · [[NDCG]] · [[Zero-Shot Retrieval]]
- [[Relevance Evaluation Tools Compared]] · [[Relevance Program Setup]] — your-data counterpart
