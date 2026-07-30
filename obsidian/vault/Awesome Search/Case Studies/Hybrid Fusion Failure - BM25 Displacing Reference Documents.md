---
type: case-study
domain: developer documentation / RAG retrieval
concepts:
  - "[[Hybrid Search]]"
  - "[[Linear Score Combination]]"
  - "[[BM25]]"
  - "[[Retrieval Pipeline]]"
  - "[[Reranking]]"
topics:
  - "[[Search Quality Assurance]]"
people:
  - "[[Davit Khachaturyan]]"
tags: [case-study, hybrid-search, fusion, score-normalization, rag, opensearch, paywalled]
access: paywalled
source: "https://medium.com/@davit.khachaturyan.03/i-added-hybrid-search-to-fix-retrieval-it-made-it-worse-d6fd6064926d"
published: 2026-07-29
created: 2026-07-30
---

# Hybrid Fusion Failure — BM25 Displacing Reference Documents

A first-person production account from [[Davit Khachaturyan]]: adding a lexical branch to a
working vector retriever made the exact query class it was meant to fix *worse*, by removing the
correct document from the candidate set entirely.

## Problem

A vector retrieval system was strong on paraphrase and contextual similarity and weak where a
literal keyword carries the meaning — a config parameter, an error code, a version string, a
threshold value. For that query class the right document isn't the most semantically similar one;
it's the one that *contains the string*. Adding [[BM25]] alongside the vector branch is the
textbook fix, and that's what was done.

The result: on that same query class, the correct document **stopped appearing at all**. Not
ranked low — absent from the candidate set.

Two properties make this expensive:

- **Nothing alerts.** No error, no latency spike, no failed request.
- **Users don't report it.** They read the fluent answer, conclude something, and file no ticket.

Neither retrieval branch was broken. Both behaved correctly. The failure was in the arithmetic
that combined them — which is the backbone of almost every hybrid search application.

## The Worked Example

Query: `maxmemory-policy default eviction` — one fact wanted, which eviction policy Redis uses
when none is configured. The answer is a single value that may live in exactly one place. Two
documents compete:

| | Document A | Document B |
|---|---|---|
| What it is | Blog post, "Redis Eviction Policies Explained" | Reference material |
| Length | ~700 words | Long |
| Term frequency | `maxmemory-policy` ~15 times, walking all eight policies | States `maxmemory-policy noeviction` once |
| Answers the question? | **No** — never says which is the default | **Yes** |
| BM25 | Boosted — short and repetitive is the ideal BM25 profile | Poor — states the fact once, in a long document |
| Vector | 0.60 | 0.85 |

(Illustrative figures; magnitudes depend on the corpus.) The vector branch had it right. Those
scores were invisible in the sum.

The generated answer comes back fluent, explaining what each policy does, never mentioning which
one is the default — and nothing in it signals that the actual question went unanswered.

## Root Cause

The lowest-friction way to combine two branches in [[OpenSearch]] or [[Elasticsearch]] is a
`bool` query with two `should` clauses — one `match`, one `knn`. It works, returns a merged
result set with a single `_score`, and appears to be doing the right thing.

But in a `bool` query, a document matching multiple `should` clauses scores the **sum** of those
clauses. The effective ranking function is `BM25 + vector_score` — a raw addition of two numbers
on unrelated scales. **The engine does not normalize across clauses; it adds whatever each one
emits.**

| | Range |
|---|---|
| **BM25** | Unbounded. Rises with term frequency, term rarity (IDF) and shortness (length normalization). A short document repeating a distinctive term can emit a very high score, with no upper bound. |
| **Vector similarity** | Bounded. Cosine-derived scores sit in a narrow range, typically well under 1. |

Add them and the unbounded one can decide the ranking. The query compiles and returns results
while doing the wrong arithmetic — without an evaluation pipeline, you may never learn it is
happening.

## Diagnosing It

Three checks, in order:

1. **Are you on OpenSearch or Elasticsearch with hybrid built as a `bool` query with two `should`
   clauses?** If so you are summing incomparable scores right now — not hypothetically, that is
   simply what the query does.
2. **Pull the per-clause score breakdown for ~20 real queries** (`explain`, or named queries) and
   put the two distributions side by side. If lexical scores range across something like 5 to 50
   while vector scores sit between 0.5 and 0.9, the vector branch isn't really participating.
3. **Build a small query set whose answers live in reference-style documents** — a table, a config
   file, a spec sheet — then check whether the correct document is in the candidate set *at all*,
   rather than checking its rank.

## Two Things That Don't Save You

- **Tuning the boost doesn't.** Multiplying an already-incomparable score changes the slope of the
  domination, not the comparability. It can shift *which* queries break, but no value makes the two
  scales comparable, because that isn't what boosting does.
- **Reranking doesn't either** — and this is the part teams miss. Debugging attention goes to the
  reranker and the generator, because that is where the visible output is. But the damage is done
  at **candidate selection**: Document B was displaced out of the top-N *before the reranker ran*.
  See [[Reranking]] and [[Retrieval Pipeline]].

## The Principled Fix

Make the two branches comparable before combining them. Three options, in order of how much
machinery they require:

1. **Use the purpose-built query instead of hand-rolling it.** [[OpenSearch]] has a dedicated
   hybrid query type that normalizes each branch into a comparable range before combining. Framed
   as the single most useful thing to know here: the intuitive path adds raw scores, the
   purpose-built path normalizes, and most teams don't find that out until something breaks.
2. **Normalize yourself, then weight** — see [[Linear Score Combination]]. Rescale each branch into
   a common range so the weights decide the outcome instead of the raw magnitudes.
3. **Route by query type.** Classify the query and set weights per class, so exact-term queries
   lean lexical and conceptual ones lean semantic. This addresses the tradeoff a single global
   boost creates, at the cost of a classifier you then have to maintain.

### Implementation notes

- **Min-max is only as stable as your extremes.** A single BM25 outlier can stretch the range and
  flatten everything else. **L2 is the steadier choice on noisy corpora.**
- **Geometric mean often behaves better than arithmetic** — it requires a document to score
  reasonably on *both* branches and pushes keyword-only matches toward zero.
- The query classifier **can be a single LLM call, but that adds latency on every request.** Budget
  for it before committing to routing.

## What Was Actually Shipped

A cap on how many documents BM25 could contribute to the merged set — **set to three.** That stops
an overpowering BM25 from taking every slot in the context given to the LLM, so a strong semantic
match reaches the reranker instead of being crowded out before anything downstream can see it.

Self-assessed as **a patch rather than a fix**: three is an arbitrary number, some queries need
more lexical results than that, and more importantly the two scores are still on completely
different scales.

## What Generalizes

The example is Redis, but the fault line runs through **any corpus that contains both explanatory
writing and reference material.** Explanations repeat terms; references state them once; BM25
prefers the explanation; and the reference is usually the thing that answers the question. That
describes developer documentation, legal text, financial filings, clinical references and most
internal wikis — which is to say most places people are pointing retrieval systems.

## Key Lessons

- **Going hybrid isn't automatically an improvement.** Adding hybrid search without thinking about
  fusion can make retrieval worse.
- **Check candidate selection before blaming the reranker or the model.** The failure is often
  upstream of where everyone is looking.
- **Boosting amplifies, it doesn't normalize.** If the branches being combined aren't comparable,
  tuning the boost just relocates the problem.
- **Evaluate by query class rather than in aggregate.** This failure was specific to one class, and
  an average hid it completely — which is exactly what averages do.

## What to Steal

- Before trusting a hybrid setup, print the two score distributions side by side for real queries.
- Add a reference-style query class to the evaluation set, and measure **presence in the candidate
  set**, not rank.
- Prefer the engine's purpose-built hybrid query over a hand-rolled `bool`/`should` merge.
- If buying rather than building: *"we use hybrid search"* answers nothing. Ask a vendor **how they
  combine the two scores**, and whether they can show retrieval quality broken out by query type.
  A team that has thought about it answers immediately.

## Related Concepts

- [[Hybrid Search]] — the pattern being critiqued
- [[Linear Score Combination]] — the normalize-then-weight fix
- [[Reciprocal Rank Fusion]] — rank-based fusion, structurally immune to this scale problem
- [[Relative Score Fusion]] — normalization-based fusion
- [[BM25]] — the unbounded half of the sum
- [[Retrieval Pipeline]] · [[Reranking]] — why nothing downstream recovers the lost document
- [[RAG]] — where the fluent-but-wrong answer surfaces
- [[Search Evaluation]] — evaluating by query class rather than in aggregate

## Related Articles

- [[RRF is Not Enough]] — [[Doug Turnbull]]; argues the real lever is upstream retrieval quality
  rather than the fusion strategy, and proposes **intent-based routing that allocates a result
  budget per source** (e.g. 80% semantic / 20% phrase). The BM25 cap shipped here is a blunt
  instance of exactly that idea, arrived at from the opposite direction

## People

- [[Davit Khachaturyan]]
