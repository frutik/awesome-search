---
type: topic
aliases:
  - model bake-off
  - comparing embedding models
  - measuring fine-tuning
  - model selection
tags:
  - topic
  - search-evaluation
  - embeddings
  - fine-tuning
  - experimentation
related_concepts:
  - "[[Search Evaluation]]"
  - "[[Judgment Lists]]"
  - "[[NDCG]]"
  - "[[Embedding Fine-tuning]]"
  - "[[Hard Negative Mining]]"
  - "[[Query Sampling]]"
  - "[[Contrastive Learning]]"
  - "[[Statistical Significance in Search Evaluation]]"
related_topics:
  - "[[Embedding Models Compared]]"
  - "[[Retrieval Benchmarks and Leaderboards]]"
  - "[[A-B Testing for Search]]"
  - "[[Relevance Program Setup]]"
  - "[[Duality in Measuring Search]]"
created: 2026-08-05
---

# Model Selection and Fine-Tuning Evaluation

## Overview

Two questions that look different but share one piece of infrastructure:

1. **Which model should we use?** — a bake-off across N candidates at a point in time.
2. **Is our fine-tuning actually working?** — one model tracked across training.

Both are answered by the same asset: a frozen, leakage-free evaluation set with an honest baseline. Teams that build it once answer both cheaply; teams that don't end up shipping models on vibes and vendor benchmarks.

This is the *how*. For the *what* — the candidate models themselves — see [[Embedding Models Compared]]. For the public benchmark landscape that produces the shortlist, see [[Retrieval Benchmarks and Leaderboards]].

---

## Part 0: The Shared Harness

Nothing below works without this. Build it first.

**A frozen test set.** Sample queries via [[Query Sampling]] — PPS by frequency for head and torso, stratified for tail. Freeze it. The moment you regenerate the test set between experiments, you can no longer compare results across them.

**Graded judgments.** Human, [[LLM as Judge]], or [[Implicit Judgments]] derived from behaviour. See [[Judgment Lists]] for construction and [[Relevance Program Setup]] for running it as an ongoing practice.

**A real baseline.** Two of them, actually: [[BM25]] and whatever is in production today. A dense model that loses to BM25 on your head queries is a common and deeply embarrassing outcome — you want to find out offline.

**Everything else held constant.** Same chunking, same `k`, same normalization, same reranker (or none), same index parameters. A "model comparison" that also changed chunk size measured nothing.

---

## Part 1: Comparing Models

### The Prefix Contract

Before any number is trustworthy: several models require specific input prefixes or instructions (`query:` / `passage:` for E5, task instructions for Qwen3). Getting these wrong doesn't error — it silently degrades quality by a large margin. **A meaningful share of published "model X is bad" results are prefix bugs.** Verify each candidate's contract against its model card before scoring it.

### Compare at Equal Cost, Not Just Equal Quality

A 3072-dim model beating a 768-dim model by 2% NDCG is not obviously the better choice — it costs 4× the index and more query latency. Normalize the comparison:

- **Quality per dimension** — truncate [[Matryoshka Embeddings|MRL]]-capable models to a common size and re-score
- **Quality per dollar** — index size, GPU/CPU serving cost, API token cost at your query volume
- **Quality per millisecond** — p95 encode latency at your batch size

See [[Vector Search Tradeoffs]] and [[Dimensionality Reduction vs Quantization]].

### Metrics by Pipeline Stage

- **First-stage retrieval**: `recall@100` (or @1000). If the right document isn't in the candidate set, no reranker saves you. Optimizing NDCG@10 on a first-stage model is the wrong target.
- **Reranking / final ordering**: [[NDCG]]@10, [[MRR]] for known-item search, [[MAP]] for recall-oriented tasks. See [[Choosing Your Search Relevance Evaluation Metric]].
- **Approximation fidelity is a separate axis** — `overlap@k` against exact scan measures the *index*, not the model. Conflating them makes ANN tuning and model selection one indebuggable problem. See [[Vector Search Evaluation]].

### Read Per-Query Deltas, Never Just the Mean

A mean NDCG improvement of +0.004 across 500 queries tells you almost nothing. What you need:

- **Win / loss / tie counts** — 200 wins and 190 losses is a different story from 30 wins and 5 losses, even at identical means
- **The loss tail** — sort by biggest regression and read those queries. Model changes routinely improve the long tail while breaking navigational and brand queries, which is a net loss in revenue even at a positive mean.
- **Head vs torso vs tail broken out separately** — an aggregate hides the segment that carries your traffic
- **Significance** — paired bootstrap or a paired t-test over per-query scores. With a few hundred queries, differences below ~1–2% NDCG are usually noise. See [[Statistical Significance in Search Evaluation]].

### Don't Select on Public Benchmarks

[[MTEB]] and [[BEIR]] measure general-domain performance and are heavily optimized against — leaderboard position reflects benchmark fit as much as model quality. It is routine for the board leader to lose to a mid-ranked model on in-domain data. Use public benchmarks to build a shortlist of 3–5 candidates; use your own judgments to pick from it. Datasets like the [[Amazon ESCI Dataset]] are a useful middle ground for e-commerce when you have no judgments yet. See [[Retrieval Benchmarks and Leaderboards]].

---

## Part 2: Measuring Fine-Tuning Progress

### Split by Query, Not by Pair

The most damaging and least visible mistake. If the same query appears in both train and test with different documents, the model has seen your test queries and your metrics are inflated — sometimes dramatically. Split at the **query** level. For production systems, also prefer a **temporal split** (train on older data, test on newer), which mirrors how the model will actually be used and exposes staleness.

### Training Loss Is Not Retrieval Quality

[[Contrastive Learning|Contrastive loss]] going down means the model separates your training triplets better. It does not mean retrieval improved. Loss and NDCG decouple constantly — especially when negatives are too easy, where loss drops fast and quality doesn't move at all.

**Evaluate retrieval metrics on the dev set at checkpoint intervals, and treat that curve as the real signal.** Loss curves are for diagnosing whether training is broken, not whether it's working.

### Negatives Determine the Outcome

More than the base model, more than the learning rate. Random negatives teach the model to separate "shoes" from "washing machines" — a distinction it already knew — and produce near-zero real gain. The gains come from [[Hard Negative Mining]]: negatives the current model already ranks highly but that are wrong. Mine them from the model you're improving, and re-mine as it improves.

### Overfitting Signals

- Dev retrieval metric plateaus or declines while training loss keeps falling → stop
- Large gains on the fine-tuned domain plus collapse on general queries → catastrophic forgetting; check a held-out general set ([[Zero-Shot Retrieval]] behaviour) each checkpoint
- Gains that shrink each time you refresh the test set → you were fitting the test set

### The Dev-Set Trap

Selecting the best checkpoint on a dev set is fine, once. Doing it across dozens of runs, hyperparameter sweeps, and negative-mining strategies means you are optimizing *against the dev set* and its numbers are now optimistic. Keep a **third split, opened once**, before you commit to shipping.

### Calibrate Expectations

Domain fine-tuning of a small model on decent data typically produces meaningful, not miraculous, gains — and often beats reaching for a larger general model at a fraction of serving cost. A reported 40% NDCG jump almost always indicates leakage, a broken baseline, or a prefix bug in the baseline. Investigate large wins as bugs before celebrating them.

See [[The Complete Guide to Fine-Tuning Embedding Models]], [[Fine-Tuning Text Embeddings For Domain-Specific Search]], [[Fine-Tuning Sparse Embeddings for E-Commerce Search]].

---

## Part 3: Offline Wins Are a Hypothesis

An offline gain is a prediction that users will behave differently. It is not evidence that they will.

- **[[A-B Testing for Search|A/B test]]** is the arbiter — but slow and traffic-hungry
- **[[Interleaving]]** is the cheaper bridge: far more sensitive per unit of traffic, good for ranking-order changes
- **Measure the correlation itself.** Over several shipped changes, track whether offline metric movement predicted online movement. If it doesn't, your judgments encode the wrong notion of relevance and the whole harness needs rework — see [[Duality in Measuring Search]] and [[Clicks Residual]].

---

## Common Failure Modes

| Symptom | Usual cause |
|---|---|
| New model wins offline, flat or negative online | Judgment list doesn't reflect real user intent; or head queries regressed |
| Enormous fine-tuning gain | Query-level leakage between train and test |
| Fine-tuning changes nothing | Negatives too easy — no [[Hard Negative Mining]] |
| Model scores far below its reputation | Prefix / instruction contract violated |
| Results move every time you re-run | Test set not frozen; or too small for the effect size |
| Dense model loses to [[BM25]] | Expected on head and navigational queries — use [[Hybrid Search]] |

---

## Related

- [[Embedding Models Compared]] — the candidates
- [[Retrieval Benchmarks and Leaderboards]] — public benchmarks and the libraries that run them
- [[Relevance Program Setup]] — running this as an ongoing organizational practice
- [[Relevance Evaluation Tools Compared]] · [[Quepid]] — tooling
- [[Search Quality Assurance]] · [[Vector Search Evaluation]]

## Articles

- [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]] — [[Joanna Marhula]], [[Mateusz Sidor]]; Allegro's cloud-vs-local, thinking-vs-no-thinking judge model bake-off; "no-thinking" variants won on accuracy
