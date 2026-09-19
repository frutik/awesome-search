---
type: topic
title: Reasoning Reranking
aliases:
  - LLM Reranking
  - Generative Reranking
  - LLM Rerankers
  - Reasoning Rerankers
tags:
  - topic
  - reranking
  - llm
  - ranking
  - neural-ir
  - frontier
related_concepts: '["Reranking", "Cross-Encoder", "RankGPT", "RankLLaMA",
  "MonoT5", "LLM as Judge", "Late Interaction", "Listwise Relevance Evaluation",
  "Calibrated Relevance Probability"]'
related_topics:
  - Frontier of Search 2026
  - Conversational and Agentic Search
  - Search Quality Assurance
articles: '["[[When Reranking Becomes a System Boundary]]", "[[Cross-Encoders
  ColBERT and LLM-Based Re-Rankers]]", "[[LLM-as-a-Judge When to Use Reasoning
  CoT and Explanations]]", "[[Using Cross-Encoders as Reranker in Multistage
  Vector Search]]", "[[Multi-Stage Ranking]]", "[[Hev meets Jev]]"]'
companies: '["Cohere", "TypeSafe", "Voyage AI", "Mixedbread"]'
people: '["Ravindra Harige", "Hev"]'
created: 2026-06-18
---

# Reasoning Reranking

The reranking stage — once a fixed [[Cross-Encoder]] applied to the top-k — is now where the fastest model innovation in search is happening. **LLMs are being turned into rerankers**: prompted to reorder candidate lists, fine-tuned to score relevance, or asked to *reason* (chain-of-thought) about why a document answers a query. This topic tracks that shift from the classic cross-encoder reranker toward generative, instruction-following, and reasoning-based rankers — and the system-design tensions it creates.

For the base mechanics, see the [[Reranking]] concept; this topic focuses on the cutting-edge end of the cost/quality spectrum.

---

## The Reranker Cost/Quality Spectrum

Rerankers only need to score ~100–1000 surviving candidates, so they can afford far richer query-document interaction than first-stage retrievers. The frontier moves up this ladder:

| Family | Mechanism | Example | Trade-off |
|---|---|---|---|
| Feature-based (LTR) | Tabular features rescored | [[LambdaMART]] / [[Metarank]] | Cheap, fast, no semantics |
| [[Cross-Encoder]] | Joint query+doc encoding, single score | `bge-reranker`, Cohere Rerank | Strong, ~50–200ms/100 |
| [[Late Interaction]] | Token-level MaxSim | [[ColBERT]] | Between bi-encoder & cross-encoder |
| Pointwise LLM | Score one (q,d) pair | [[MonoT5]], [[RankLLaMA]] | High quality, higher cost |
| Listwise LLM | Reorder a whole list | [[RankGPT]] | Sees cross-document context; sliding window for long lists |
| Reasoning reranker | CoT before judging | reasoning LLM judges | Highest quality, highest cost/latency |

## Generative & LLM Rerankers

- **[[MonoT5]]** — frames relevance as a seq2seq task: score a (query, document) pair by the probability of generating a "true" vs "false" token. (DuoT5 is the pairwise variant.)
- **[[RankLLaMA]]** — a decoder LLM (RepLLaMA/RankLLaMA line, Tevatron) fine-tuned for **pointwise** relevance scoring.
- **[[RankGPT]]** — **listwise** reranking by prompting an instruction-tuned LLM to emit a permutation of the candidate list directly, using a sliding window to handle lists longer than the context window. No fine-tuning required.
- **Reasoning rerankers / [[LLM as Judge|LLM-as-judge]]** — let the model reason (chain-of-thought) and optionally emit explanations before scoring. See [[LLM-as-a-Judge When to Use Reasoning CoT and Explanations]] for when CoT actually helps vs. adds cost.

Pointwise vs. pairwise vs. listwise is the same axis explored in classic LTR (see [[Pointwise vs Pairwise vs Listwise Learning to Rank]]) — LLM rerankers re-instantiate it at the prompt level.

### Structured-Decision Rerankers

A newer variant sidesteps generation entirely. Instead of prompting a model to *emit* a
permutation or a "true"/"false" token, a structured-output model is asked one typed
true-or-false question per candidate against a shared state, and answers each independently
with a probability. [[Jev]] ([[TypeSafe]]) is the first worked example in this vault; the
benchmark is [[Hev meets Jev]].

Why it matters here rather than as a footnote:

- **No ranking training at all.** The model was not built as a reranker. Untuned, with a
  deliberately generic prompt, it reached **0.501 mean nDCG@10** across three [[BEIR]] subsets
  — against 0.504 for Voyage rerank-3, 0.486 for [[Cohere]] rerank-v3.5, 0.476 for
  [[Mixedbread]] `mxbai-rerank-large-v2`, and 0.404 for the unreranked [[BM25]] order. A
  corpus-specific prompt did no better than the generic one.
- **[[Calibrated Relevance Probability|Calibrated output]].** The score is a probability, not a
  logit — which none of the purpose-built rerankers return, and which [[NDCG]] cannot detect.
- **Per-question independence** replaces the sliding-window machinery [[RankGPT]] needs, and
  avoids the cross-document contamination that makes listwise ordering sensitive to candidate
  order.

The same source makes the complementary finding about *general* LLMs as listwise rerankers:
they work, but on cost and latency rather than quality. On SciFact, `gpt-5.6-luna` with
reasoning off scored 0.747 and Claude Opus 5 at low effort scored 0.756 — competitive with the
specialists — but at 3.2 s and 5.0 s p50 respectively, against ~0.2 s, and at $2.36 and $94.68
per 1,000 queries. Opus also declined to judge 12 of the 300 claims. That is the practical
ceiling on the reasoning end of the spectrum in this table.
## Reranking in RAG and Agentic Pipelines

In [[RAG]] and agentic systems the context window is the bottleneck, so reranking is where precision is won or lost — a reranker narrows 50–100 retrieved chunks to the best 3–5 before generation. This connects directly to the agentic frontier: purpose-built agentic models (e.g. [[SID-1]]) end their loop with a dedicated **rerank turn**, and distractor-aware evaluation ([[UDCG]]) argues the reranker's real job is removing harmful passages, not just ordering relevant ones.

## When Reranking Becomes a System Boundary

A caution that scales with reranker power, from [[Ravindra Harige]]'s [[When Reranking Becomes a System Boundary]]:

- **Retrieval defines eligibility; reranking defines order.** A document not retrieved can never be recovered downstream.
- Reranking operates on a **lossy projection** of retrieval-time signals (term matches, field contributions, BM25 components are not recomputed).
- The system crosses a boundary when gains come from **widening the rerank window** rather than improving retrieval — at which point window size is load-bearing and reranking has become *compensatory*.
- Evaluation splits: retrieval owns Recall@K, reranking owns NDCG/MRR — and neither team's dashboard shows the full picture.

The more capable the LLM reranker, the easier it is to mask weak retrieval — making this boundary more important, not less.

---

## Related Concepts
- [[Reranking]] — the base concept and pipeline
- [[Cross-Encoder]] — the classic reranker the LLM variants extend
- [[MonoT5]] · [[RankLLaMA]] · [[RankGPT]] — the generative/LLM reranker line
- [[LLM as Judge]] — the same models scoring relevance/answers
- [[Late Interaction]] · [[ColBERT]] — the multi-vector middle ground
- [[Retrieval Pipeline]] — where reranking sits
- [[Calibrated Relevance Probability]] — the output property standard reranker metrics never report
- [[Jev]] · [[hev-rerank]] — the structured-decision reranker and its open implementation

## Related Topics
- [[Frontier of Search 2026]] — reranking is one front of the agentic-era shift
- [[Conversational and Agentic Search]] — agentic loops end with a rerank step
- [[Search Quality Assurance]] — the evaluation split this topic surfaces

## Related Articles
- [[When Reranking Becomes a System Boundary]] — [[Ravindra Harige]]
- [[Cross-Encoders ColBERT and LLM-Based Re-Rankers]]
- [[LLM-as-a-Judge When to Use Reasoning CoT and Explanations]]
- [[Using Cross-Encoders as Reranker in Multistage Vector Search]]
- [[Multi-Stage Ranking]]
- [[Hev meets Jev]] — [[Hev]]; structured-decision and LLM rerankers benchmarked against the purpose-built ones
- [[Introducing System One Models & Jev]] — [[Diogo Almeida]]; the model class behind the structured-decision reranker above

## People
- [[Ravindra Harige]] — the reranking-as-system-boundary analysis
