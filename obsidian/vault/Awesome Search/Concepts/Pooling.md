---
title: "Pooling"
aliases: ["sequence pooling", "mean pooling", "average pooling", "CLS pooling", "max pooling", "attention pooling", "weighted pooling"]
type: concept
tags:
  - concept
  - neural-ir
  - embeddings
  - retrieval
created: 2026-07-30
---

# Pooling

Collapsing many representations into fewer along some axis. In IR the word covers several
genuinely different operations that share only that shape — this note defines the general idea,
routes to the other senses, and covers **sequence pooling** (the unmarked default meaning in
embedding contexts) in detail.

---

## The six senses

| # | Sense | Collapses | Axis | Home |
|---|---|---|---|---|
| 1 | **Sequence pooling** | Per-token output vectors → one document vector | Sequence length | This note |
| 2 | **Token pooling** | Many token vectors → fewer token vectors | Sequence length, partially | [[Token Pooling]] |
| 3 | **Vocabulary pooling** | Per-token vocabulary distributions → one sparse vector | Vocabulary | [[SPLADE]] |
| 4 | **Judgment pooling** | Many systems' top-k → one judged document set | Result sets | [[Judgment Lists]] |
| 5 | **Behavioral sequence pooling** | A user's interaction history → one preference vector | Time / events | [[Personalization]] |
| 6 | **Similarity-matrix pooling** (MaxSim) | A query×document score matrix → one relevance score | Similarity scores | [[Late Interaction]] |

The sharpest cut is **what** gets pooled. Senses 1–3 pool *representations*, mostly at index time.
Sense 6 pools *scores*, at query time, after the representations have already been compared. Sense 4
is an evaluation practice and sense 5 a feature engineering step. They are unrelated beyond the name.

---

## Sequence pooling

A transformer encoder does not emit one vector for an input — it emits **one vector per token**.
Sequence pooling is the step that collapses that `[n_tokens × d]` matrix into the single `d`-dimensional
vector a [[Bi-Encoder]] actually stores and indexes.

```
"red running shoes"
      ↓ encoder
 [v₁, v₂, v₃, v₄]      ← one vector per token
      ↓ pooling
      v                ← one vector per document
```

### Strategies

**Mean / average pooling** — element-wise average across token vectors, masked so padding tokens
don't contribute. The common default in sentence-transformers, and the usual starting point.

**CLS pooling** — take the vector at the `[CLS]` position and discard the rest, relying on the model
having been trained to concentrate sequence-level meaning there. Cheap, but only sensible when the
training objective actually put something there.

**Max pooling** — element-wise maximum across token vectors; each dimension takes its strongest
activation from whichever token produced it. Favors salient tokens over the overall distribution.

**Attention / weighted pooling** — learn per-token weights instead of treating every token
identically, so the collapse can emphasize informative tokens.

### Why it's the interesting step

Pooling is where a [[Bi-Encoder]] becomes lossy. The model must decide **at training time** which
distinctions survive the collapse into one vector, and that decision is made against the training
query distribution — so distinctions that matter to *your* queries but not to the training data are
gone before retrieval ever runs.

This is precisely what [[Late Interaction]] defers: [[ColBERT]] keeps the per-token vectors and
matches at query time instead, trading storage for the ability to make that decision later. The two
sit at opposite ends of the same axis, with [[Token Pooling]] as the tunable middle — reduce the
vector count without going all the way to one.

Pooled single vectors are also what the classic embedding failure modes attach to: a pre-trained
model's pooled representation may simply not encode what your domain needs. See
[[Three mistakes when introducing embeddings and vector search]].

### Where it's configured

In [[Sentence Transformers]], pooling is an explicit module in the model pipeline rather than an
implicit behavior — a transformer module followed by a pooling module, which is why the strategy is
swappable and worth checking rather than assuming.

---

## The other senses, briefly

### Token pooling

Clusters semantically similar token/patch vectors and replaces each cluster with its mean, reducing
vector *count* without collapsing to one. A compression technique for multi-vector late interaction
models, from the [[ColPali]] paper. Average-vector compression is its limiting case
(`pool_factor = ∞`). See [[Token Pooling]].

### Vocabulary pooling

In [[SPLADE]], the MLM head emits a distribution over the full vocabulary *per token*; pooling
collapses those into one sparse vector. SPLADE v2 uses **max pooling** — each vocabulary term takes
its highest weight across all token positions. In [[Sentence Transformers]] v5 this is the
`SpladePooling` module (max over tokens plus ReLU), paired with `MLMTransformer`.

Note the axis: this pools over the *vocabulary*, not the sequence, so the output is a
vocabulary-sized sparse vector rather than a dense one. Sense 1 and sense 3 are not variants of each
other.

### Judgment pooling

Unrelated to representations. A TREC-style [[Search Evaluation|evaluation]] practice: run multiple
retrieval systems, take the top-k from each, and judge the union — because judging an entire corpus
is infeasible. Documents outside the pool are treated as **"unjudged"** rather than irrelevant, and
that is where pooling bias comes from: a new system that surfaces good non-pooled documents is
penalised for it. Building the pool from a single retrieval technique concentrates the bias further.
See [[Judgment Lists]] and [[Improving retrieval with LLM-as-a-judge]].

### Behavioral sequence pooling

Compressing a variable-length user interaction history into one fixed-size representation via mean,
sum or max. Sequence models (RNNs, Transformers) are the order-preserving alternative. See
[[Personalization]] and [[Patterns for Personalization]].

### Similarity-matrix pooling (MaxSim)

The easiest one to confuse with sense 1, because it is also "max pooling" and it also appears in
discussions of token vectors — but it operates on **scores**, not representations.

[[Late Interaction]]'s MaxSim scores a query of *m* tokens against a document of *n* tokens by
building the full `m × n` similarity matrix, then collapsing it:

```
Score = Σᵢ maxⱼ (qᵢ · dⱼ)
         ↑   ↑
         |   pool across document tokens — keep each query token's best match
         sum across query tokens
```

The `maxⱼ` is a pooling step over the document-token axis of the score matrix, reducing `m × n` to
`m`, which is then summed to a scalar.

The distinction that matters: sense 1 pools **before** comparison and destroys information
permanently at index time; MaxSim pools **after** comparison, at query time, with the full token
vectors still available. That is precisely the tradeoff late interaction exists to make — and why
[[ColBERT]] can defer the decision a [[Bi-Encoder]] has to make during training.

## Related Concepts

- [[Bi-Encoder]] — the architecture sequence pooling produces vectors for
- [[Embeddings]] · [[Dense Embeddings]] — what comes out the far side
- [[Late Interaction]] — defers the decision pooling forces early
- [[ColBERT]] — keeps per-token vectors instead of pooling them
- [[Token Pooling]] — the tunable middle ground between the two
- [[SPLADE]] — vocabulary-axis pooling into a sparse vector
- [[Judgment Lists]] — the evaluation sense
- [[Personalization]] — the behavioral sense
- [[Late Interaction]] — MaxSim, the score-level sense
- [[Interaction Paradigms]] — the no/late/early spectrum this sits on
- [[Sentence Transformers]] — where the strategy is configured

## Articles

- [[Three mistakes when introducing embeddings and vector search]] — what a pooled vector fails to carry
- [[Late Interaction Models - How to Scale and Optimize in Elasticsearch]] — average vectors vs token pooling in production
