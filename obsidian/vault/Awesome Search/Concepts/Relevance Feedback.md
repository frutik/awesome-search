---
type: concept
title: "Relevance Feedback"
aliases: ["PRF", "pseudo-relevance feedback", "implicit feedback", "explicit feedback"]
tags:
  - concept
  - search-evaluation
  - query-understanding
created: 2026-05-31
---

# Relevance Feedback

## Definition

Using signals about which results are relevant (or not) to iteratively refine a search query and improve subsequent retrieval. Bridges the gap between a user's initial query and their actual [[Search Intent]].

## Three Types

### Explicit Feedback
User directly marks results as relevant or irrelevant (thumbs up/down, "More like this"). Highest quality signal — but rare in practice because users don't want to do extra work.

### Pseudo-Relevance Feedback (PRF)
Assume the top-k results are relevant. Extract key terms from those documents, expand the query, and re-execute. Fully automated — no user interaction needed. Risk: drifts badly if the initial top-k is poor.

### Implicit Feedback
Infer relevance from user behaviour:
- Clicks → positive signal
- Long dwell time → likely relevant
- Immediate back-navigation → likely not relevant
- Conversion / purchase → strong positive signal

Cheap and abundant, but noisy — corrupted by [[Position Bias]] and [[Presentation Bias]].

### Model-Generated Feedback

The feedback provider need not be a user at all. Move the loop *inside* the application and let a model judge relevance — an LLM, an agent, a [[Cross-Encoder]], a [[Learning to Rank]] model — then show the user only the converged result set. This sidesteps the fundamental limit on explicit feedback (*"people are lazy"* — Google shipped thumbs up/down on its results page and removed it because nobody pressed them), at the cost of trusting the model's notion of relevance to match your users'.

## Where the Feedback Is Applied

Orthogonal to *who* provides feedback is *what it changes*. Search decomposes into query, documents, and the function matching them:

| Target | Status |
|---|---|
| **Query** | The default. Rewrite or expand it — Rocchio, RM3, BERT-QE, LLM rewriting. See [[Query Expansion]]. |
| **Documents** | Not done — you wouldn't rewrite the corpus per query. |
| **Scoring function** | Rare, because search engines are black boxes you must build *around*. |

The usual workaround for the third row is to over-fetch from the black box, rerank the candidates with the feedback model, and show the top — see [[Reranking]]. It only ever touches a retrieved subset; you would rerank the whole collection if you could afford to.

### Index-Native Relevance Feedback

If you own the index, feedback can go *into the traversal itself*. [[Qdrant]] 1.17 (February 2026) modifies the [[HNSW]] hop-selection function: instead of choosing the next neighbour by cosine similarity to the query alone, it uses a combination of similarity and the feedback scores from the previous loop. Feedback bends the **path** through the graph, so its effect reaches the whole collection rather than a top-k.

```
F = a · score + Σ_pairs confidence_p^b · c · delta_p
```

Three parameters are fitted once per *(feedback model, collection, retriever)* — not per query — by pairwise ranking loss. The objective is [[Knowledge Distillation]]: make cheap dense retrieval rank the way an expensive feedback model would, since that model could never be run over the full corpus.

Two ways to use it: as a **cheaper substitute** for reranking (distil a handful of feedback scores, let the index rank at scale), or **complementary** to it. Reported [[BEIR]] gains span **−3.9% to +38.7%** relative on a custom relevance-recall metric — the benefit exists only where the feedback model actually disagrees with the retriever, and is capped by how much of that disagreement the retriever's vector space can represent. See [[Relevance Feedback in Qdrant]].

The standing caveat still applies — documents never surfaced never earn feedback, so this suits domains where humans can't stay in the loop (scientific, medical literature) better than human-centric ones like [[E-commerce Search]].

See [[Evgeniya Sukhodolskaya - Relevance Feedback Inside the Search Engine]] and [[qdrant-relevance-feedback]].

## Rocchio Algorithm

Classic vector-space implementation of explicit feedback:

```
new_query = α × original_query + β × avg(relevant_docs) − γ × avg(non_relevant_docs)
```

Moves the query vector toward relevant documents and away from non-relevant ones.

## Modern Implementations

- **"More like this"** — Elasticsearch `more_like_this` query uses document terms as expansion
- **Session-level feedback** — clicks earlier in a session inform later query refinements
- **LLM-based query rewriting** — use clicked documents to rewrite query with an LLM
- **Contrastive feedback** — train embedding models on (query, clicked, skipped) triples

## Challenges

- Explicit feedback rarely occurs
- Implicit signals are noisy — [[Position Bias]] means top results get more clicks regardless of quality
- [[Presentation Bias]]: can only learn from results that were shown

## Related Concepts

- [[Click Signals]] — primary source of implicit feedback
- [[Position Bias]] — corrupts click-based relevance signals
- [[Presentation Bias]] — results not shown can't generate feedback
- [[Query Understanding]] — relevance feedback as a query refinement mechanism
- [[Session-Based Evaluation]] — session context shapes feedback
- [[Learning to Rank]] — implicit feedback used as LTR training signal

## Articles

- [[Query Understanding - Relevance Feedback]] — [[Daniel Tunkelang]]; explicit, pseudo, and implicit types
- [[What AI Engineers Should Know about Search]] — [[Doug Turnbull]]; relevance feedback as query feedback (point 55)

- [[Relevance Feedback (Wikipedia)]] — Wikipedia; foundational IR reference covering explicit, implicit, and pseudo-relevance feedback with the Rocchio algorithm

- [[Relevance Feedback in Informational Retrieval]] — [[Evgeniya Sukhodolskaya]] ([[Qdrant]], 2025); taxonomy of feedback types (pseudo / binary / re-scored) crossed with where they apply (query refinement vs similarity scoring), and why neural search has no production answer
- [[Relevance Feedback in Qdrant]] — the same author's follow-through: the index-native formula, training procedure and [[BEIR]] results

## Videos

- [[Evgeniya Sukhodolskaya - Relevance Feedback Inside the Search Engine]] — [[Berlin Buzzwords]] 2026; feedback propagated into [[HNSW]] traversal

## People

- [[Daniel Tunkelang]] — queryunderstanding.com series
- [[Evgeniya Sukhodolskaya]] — index-native relevance feedback at [[Qdrant]]
