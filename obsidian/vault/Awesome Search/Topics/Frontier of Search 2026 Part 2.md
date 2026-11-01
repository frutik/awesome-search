---
type: topic
title: Frontier of Search 2026 Part 2
aliases:
  - Frontier of Search 2026 H2
  - Search Frontier Late 2026
tags:
  - topic
  - frontier
  - llm-as-judge
  - reranking
  - calibration
  - agentic-search
  - commoditization
  - evaluation
related_concepts:
  - LLM as Judge
  - Staged Judging
  - Levels of Judge Agreement
  - Judge Calibration
  - Calibrated Relevance Probability
  - System One Model
  - Bag of Decisions
  - BlitzRank
  - Fast but Not Late Interaction
  - Relational Transformer
  - MUVERA
  - ASH
  - TurboQuant
  - Agentic Memory
  - Query Routing
  - Model Context Protocol
  - Benchmark Contamination
  - Catastrophic Forgetting
  - NDCG-m
  - Compute-Storage Disaggregation
related_topics:
  - Frontier of Search
  - Frontier of Search 2026
  - Frontier of Search 2025
  - Reasoning Reranking
  - Reception of Jev
  - Relevance Evaluation Tools Compared
  - Agentic Memory for Search Personalization
  - Retrieval Benchmarks and Leaderboards
  - Extreme Search Systems
  - Late Interaction in Qdrant
  - Late Interaction in OpenSearch
  - Late Interaction in Vespa
articles:
  - "[[Towards Scalable Relevance Engineering]]"
  - "[[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]]"
  - "[[How Etsy Uses LLMs to Improve Search Relevance]]"
  - "[[Benchmarking LLM-based Relevance Judgment Methods]]"
  - "[[Do LLM Judges Actually Agree With Us]]"
  - "[[Calibrate Before You Trust]]"
  - "[[Search golden sets are anything but]]"
  - "[[Introducing System One Models & Jev]]"
  - "[[Hev meets Jev]]"
  - "[[Adapting Jev to Your Domain with GEPA]]"
  - "[[BlitzRank - Principled Zero-shot Ranking Agents with Tournament Graphs]]"
  - "[[Lychee-Reranker - Fast but Not Late Interaction for Compressed Document
    Reranking]]"
  - "[[Relational Reranking - Scoring Search Results with Structured Facts]]"
  - "[[rerank-3 and rerank-3-lite - the next generation of Voyage rerankers]]"
  - "[[MUVERA - Multi-Vector Retrieval via Fixed Dimensional Encodings]]"
  - "[[Qdrant 1.19 - Turbo4 Datatype and Memory Tiers]]"
  - "[[Introducing OpenSearch Relevance Agent]]"
  - "[[AI Agent Memory - Creating Smart Agents with Elasticsearch Managed
    Memory]]"
  - "[[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]]"
  - "[[How to Build a 256 TB Search Index]]"
companies:
  - TypeSafe
  - Contextual AI
  - Voyage AI
  - RelativeDB
  - Allegro
  - Etsy
  - searchHub
  - Qdrant
  - Elastic
  - Google
  - turbopuffer
people:
  - Doug Turnbull
  - Andreas Wagner
  - Andrew Kornilov
  - Jo Kristian Bergum
  - Hajer Bouafif
  - Charles L. A. Clarke
  - Negar Arabzadeh
created: 2026-11-01
---

# Frontier of Search 2026 Part 2

[[Frontier of Search 2026]] described two shifts in June: agents becoming the user of search, and yesterday's research becoming a built-in engine feature. Both continued through the second half of the year. The material written up since then adds three more fronts: **the judge**, **the decision model**, and **cheaper reranking**. It also shows a growing doubt about the numbers everyone reports.

The short version: in late 2026 the hard part of search is less often *finding* candidates and more often *judging* them. That means deciding cheaply, at scale, and with a confidence you can trust whether a result is relevant, whether it should be reranked, and whether the metric reporting it can be believed.

---

## 1. The Judge Moves to the Centre

[[LLM as Judge]] stopped being an experiment and became infrastructure. The work shifted from "can an LLM grade relevance?" to "what does grading cost, and how do we know the grades are right?"

### Making judging affordable
- **[[Staged Judging]]**: the cascade [[Andreas Wagner]] describes at [[searchHub]]. Most query–document pairs are obviously relevant or obviously not, so behavioural signals prune first, quantized [[Bi-Encoder|bi-encoders]] score the survivors on CPU, only disagreements escalate to the full LLM, and its verdicts are [[Knowledge Distillation|distilled]] into a model that can be served. ([[Towards Scalable Relevance Engineering]].)
- **[[Allegro]]** found that removing few-shot examples *raised* judge accuracy and agreement, and that moving batch judging to a locally hosted 26B Gemma variant cut inference cost by 60% with parity on Polish. ([[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]].)
- **[[Etsy]]** distils an o3 annotator through a Qwen 3 VL 4B teacher into a BERT two-tower student, turning [[Semantic Relevance]] into a real-time ranking signal. The share of fully relevant listings rose from 58% to 62%. ([[How Etsy Uses LLMs to Improve Search Relevance]].)

### Knowing whether to trust it
- **[[Levels of Judge Agreement]]** separates four claims that usually get run together: same label, same score, same ordering, same decision. Two judges can disagree heavily on labels and still produce the same leaderboard. ([[Do LLM Judges Actually Agree With Us]].)
- [[Benchmarking LLM-based Relevance Judgment Methods]] ([[Negar Arabzadeh]], [[Charles L. A. Clarke]]) shows that the best judging paradigm depends on the goal. Pairwise preferences win on agreement with human labels. Graded and binary pointwise labels win on agreement with human system rankings, reaching Kendall τ up to 0.922. [[LLMJudge]] benchmarks judges rather than rankers.
- **[[Judge Calibration]]** measures a judge against a reference on a frozen sample. It reports Krippendorff's α per pair and [[Kendall Rank Correlation|Kendall's τ]] over per-query nDCG@10 per ranking, because those two levels can come apart. ([[Calibrate Before You Trust]].)
- Graded schemes inspired by the [[ESCI Label Scheme]] show where grades get hard. On [[Allegro]]'s ESCI-inspired scale, a judge reached F1 around 0.94 on exact matches but only 0.33–0.51 on degrees of substitutability.

### The golden set itself is questioned
A golden set can score a system at NDCG 1 while users are unhappy, just because the corpus holds few relevant results. [[Doug Turnbull]] argues for [[NDCG-m]] (normalised against a fixed all-max-grade ideal, so corpus coverage shows), [[NDCG-f]] (labeled results only, as a regression check) and [[Rank-Biased Overlap]] (how far results moved, no labels needed). ([[Search golden sets are anything but]].)

### Evaluation gets agents too
The [[OpenSearch Relevance Agent]] (experimental in [[OpenSearch]] 3.6) splits relevance tuning across three agents. It keeps metric computation in deterministic tools outside the LLM and reaches the engine only through [[Model Context Protocol|MCP]]. [[Releval]] collects [[User Behavior Insights|UBI]] events itself and runs against any engine. Together with [[Search Relevance Workbench]] and [[Elasticsearch Relevance Studio]], evaluation is moving inside the engines and their surrounding tools. See [[Relevance Evaluation Tools Compared]].

---

## 2. Decision Models: The Score Becomes a Probability

A new category appeared: models that emit typed decisions with a calibrated probability instead of text. [[Jev]], from [[TypeSafe]], is the example covered here. See [[System One Model]] and [[Reinforcement Learning for Calibrated Decisions]].

- **As a reranker.** Over a [[BM25]] top-30 shortlist, untuned Jev reached 0.501 mean nDCG@10 across three [[BEIR]] subsets. [[Voyage AI|Voyage]] rerank-3 scored 0.504 and the unreranked shortlist 0.404. ([[Hev meets Jev]].)
- **Why it matters:** [[Calibrated Relevance Probability]]. A probability can be thresholded, pruned on and fused, which a [[Cross-Encoder]] logit cannot. [[Voyage rerank-3]] makes a related promise from the other side: it keeps rerank-2.5's score distributions so tuned thresholds survive the upgrade.
- **New patterns.** [[Bag of Decisions]] has an LLM write a yes/no rubric for each query and sums the answers. [[Jevals]] argues that once judging is cheap and calibrated, you grade the whole set instead of sampling it.
- **The pushback is part of the story.** At Jev's default prompt, [[Adapting Jev to Your Domain with GEPA]] measured an [[Expected Calibration Error|ECE]] of 0.173 against 0.052 for a tuned TF-IDF baseline. Rewriting the prompt with [[GEPA]] moved F1 from 69.1% to 79.7%. So calibration is partly a property of the prompt. [[Han-chung Lee]] questions whether the calibration comes from RLCD at all. [[Reception of Jev]] tracks the debate.

---

## 3. Reranking Gets Cheaper and More Structured

Reranking ([[Reranking]], [[Reasoning Reranking]]) saw several new approaches in the second half of 2026. The common goal was keeping LLM-grade ordering while cutting its cost.

| Approach | Idea | Reported result |
|---|---|---|
| [[BlitzRank]] ([[Contextual AI]]) | Read one listwise answer as every pairwise preference inside it, infer more pairs by transitivity, stop once the top ten are settled | 56.9 nDCG@10 on 42k tokens per query vs 57.0 on 324k for a pairwise reranker |
| [[Fast but Not Late Interaction]] ([[Lychee-Reranker]]) | Encode passages offline into compressed token states that a learned decoder reads alongside the query | Compression adjustable from 1x to 128x at inference; cost figures are analytical estimates |
| [[Relational Transformer]] ([[RelativeDB]]) | Score candidates from typed database fields and linked rows, not serialized text | 0.633 NDCG@10 on a product-search slice vs 0.286 for MiniLM retrieval alone |
| [[Voyage rerank-3]] | Built for longer documents and agent traffic | Vendor-reported 13.84% lead over Cohere Rerank v4.0 Pro on [[LongEmbed]] |
| [[Asymmetric Re-ranking]] in [[Vespa]] | Algebraic rewrite moves a query-only term out of the per-document loop | 267 ms → 193 ms at 1M documents |

All of these figures are the authors' own. [[Voyage AI]] says coding agents now send many reranker queries with longer candidate documents, which ties this front back to the agentic shift.

---

## 4. Commoditization Keeps Descending

The June note's second shift, research turning into a configuration option, sped up.

- **Late interaction everywhere.** It now has engine-native support in [[Late Interaction in OpenSearch|OpenSearch]], [[Late Interaction in Qdrant|Qdrant]] and [[Late Interaction in Vespa|Vespa]], alongside [[Late Interaction in Elasticsearch|Elasticsearch]]. [[MUVERA]] (from [[Google]]) folds a multi-vector document into one ANN-searchable encoding. It ships in [[Weaviate Vector DB]], [[Qdrant Vector DB]] via [[FastEmbed]], and an OpenSearch plugin. Its benchmarks keep 87–97% of exact quality after rerank, against 28–52% for average vectors.
- **Quantization goes further.** [[Qdrant Vector DB|Qdrant]] 1.19's turbo4 stores only the 4-bit [[TurboQuant]] code, with nine times less disk and no rescoring stage, so the error is permanent. [[ASH]] shows that, at a fixed bit budget, fewer dimensions at more bits can win if the reduction is learned.
- **Fusion and feedback move into the engine.** [[Distribution-Based Score Fusion]] sits next to [[Reciprocal Rank Fusion|RRF]] in Qdrant. Qdrant 1.17 applies [[Relevance Feedback]] to [[HNSW]] hop selection rather than to the query.
- **Smaller footprints.** [[sqlite-sparse]] runs [[Learned Sparse Retrieval]] inside one SQLite file with no model on the query path. [[Brute-Force Vector Search]] beats an ANN index on most small corpora ([[Vector Search Tradeoffs]]).
- **Storage and compute separate.** In [[How to Build a 256 TB Search Index]], [[turbopuffer Search DB|turbopuffer]] scales a namespace from 4 TB to 256 TB. Under [[Compute-Storage Disaggregation]], a lost node costs a cache refill, not a rebalance. See [[Extreme Search Systems]].

---

## 5. Agents Get Memory and Routing

The agent-as-user front from June gained two pieces of infrastructure.

- **[[Agentic Memory]].** OpenSearch ships four memory types (dated to 3.3). Elasticsearch enforces memory isolation through role descriptors, so credentials decide which memories exist at all. [[DICE]] keeps memory in the application's own domain model, with per-fact confidence and decay. [[Agentic Memory for Search Personalization]] holds the user model as language, applied through [[Query Rewriting]], rerank or filters. From [[Hajer Bouafif]]'s [[Berlin Buzzwords]] 2026 talk and the vendor docs.
- **[[Query Routing]].** The 2009 web-search problem of [[Vertical Selection]] has returned as RAG routing: [[Adaptive Retrieval]], expert encoders, ranked retrievers and per-query hybrid weights. In one paper, a complexity router that was only 55% accurate still matched always-multi-step answers in under half the time.
- **[[Model Context Protocol]]** is becoming the common interface. Relevance agents, evaluation tools and memory layers all reach the engine through it.

---

## 6. Doubt About the Numbers

Running through all five fronts is growing scepticism about the figures the field reports:

- **[[Benchmark Contamination]].** [[MS MARCO]] sits under nearly every retrieval model, and in 2026 [[RTEB]]'s private column was temporarily removed over vendor-access concerns. See [[Retrieval Benchmarks and Leaderboards]].
- **Baseline artifacts.** [[Jo Kristian Bergum]]'s tuned BM25 beats the BM25 numbers published with BEIR, so some published neural gains may come from weak baselines. ([[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]].)
- **Fine-tunes don't travel.** An ESCI-tuned [[SPLADE]] gains 27.5% over BM25 on ESCI but only 8–10% on WANDS and Home Depot. [[Catastrophic Forgetting]] covers the responses.
- **Static benchmarks miss churn.** [[Vector Index Updates]]: never trust a benchmark that inserts once and replays queries.
- **Received wisdom gets re-measured.** In one benchmark, [[PCA]] held 82% of nDCG@10 at 64 dimensions against [[Matryoshka Embeddings|Matryoshka]] truncation's 71%.

Many of the results above are vendor- or author-reported, and the notes say so. That caution is itself a sign of how the frontier works now.

---

## Late 2026 at a Glance

| Front | What changed | Anchor notes |
|---|---|---|
| The judge | LLM judging made cheap (cascades, local models, distillation) and scrutinised (agreement levels, calibration) | [[Staged Judging]], [[Levels of Judge Agreement]], [[Judge Calibration]] |
| Decision models | Calibrated probability as the output of a reranker or classifier | [[Jev]], [[Calibrated Relevance Probability]], [[Bag of Decisions]] |
| Cheaper reranking | LLM-grade ordering at a fraction of the tokens or latency | [[BlitzRank]], [[Fast but Not Late Interaction]], [[Relational Transformer]] |
| Commoditization | Multi-vector, aggressive quantization, fusion, feedback as engine features | [[MUVERA]], [[TurboQuant]], [[Distribution-Based Score Fusion]] |
| Agents | Memory and routing as infrastructure, MCP as the interface | [[Agentic Memory]], [[Query Routing]], [[Model Context Protocol]] |
| Doubt | Contamination, weak baselines, non-transferring fine-tunes | [[Benchmark Contamination]], [[Catastrophic Forgetting]] |

---

## Related Concepts
- [[LLM as Judge]] — the central technique of the period
- [[Staged Judging]] — cascade economics for judging
- [[Levels of Judge Agreement]] — what "the judge agrees" actually means
- [[Judge Calibration]] — measuring a judge before trusting it
- [[Calibrated Relevance Probability]] — scores you can threshold and fuse
- [[System One Model]] — the decision-model architecture
- [[BlitzRank]] · [[Fast but Not Late Interaction]] · [[Relational Transformer]] — the new rerankers
- [[MUVERA]] · [[ASH]] · [[TurboQuant]] — commoditized retrieval and compression
- [[Agentic Memory]] · [[Query Routing]] · [[Model Context Protocol]] — agent infrastructure
- [[Benchmark Contamination]] · [[Catastrophic Forgetting]] · [[NDCG-m]] — the doubt

## Related Topics
- [[Frontier of Search]] — year-by-year index
- [[Frontier of Search 2026]] — the first half of the year (agents as the user; the frontier becoming a commodity)
- [[Frontier of Search 2025]] — the prior period
- [[Reasoning Reranking]] — LLM rerankers
- [[Reception of Jev]] — the decision-model debate
- [[Relevance Evaluation Tools Compared]] — evaluation tooling
- [[Agentic Memory for Search Personalization]] — memory applied to search
- [[Retrieval Benchmarks and Leaderboards]] — the benchmarks under question
- [[Extreme Search Systems]] — scale and storage

## Related Articles
- [[Towards Scalable Relevance Engineering]]
- [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]]
- [[How Etsy Uses LLMs to Improve Search Relevance]]
- [[Benchmarking LLM-based Relevance Judgment Methods]]
- [[Do LLM Judges Actually Agree With Us]]
- [[Calibrate Before You Trust]]
- [[Search golden sets are anything but]]
- [[Introducing System One Models & Jev]]
- [[Hev meets Jev]]
- [[Adapting Jev to Your Domain with GEPA]]
- [[BlitzRank - Principled Zero-shot Ranking Agents with Tournament Graphs]]
- [[Lychee-Reranker - Fast but Not Late Interaction for Compressed Document Reranking]]
- [[Relational Reranking - Scoring Search Results with Structured Facts]]
- [[rerank-3 and rerank-3-lite - the next generation of Voyage rerankers]]
- [[MUVERA - Multi-Vector Retrieval via Fixed Dimensional Encodings]]
- [[Qdrant 1.19 - Turbo4 Datatype and Memory Tiers]]
- [[Introducing OpenSearch Relevance Agent]]
- [[AI Agent Memory - Creating Smart Agents with Elasticsearch Managed Memory]]
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]]
- [[How to Build a 256 TB Search Index]]

## People
- [[Doug Turnbull]] — golden-set critique, Bag of Decisions, pairwise judging with Jev
- [[Andreas Wagner]] — staged judging at searchHub; Jev sceptic
- [[Andrew Kornilov]] — judge agreement and calibration essays
- [[Negar Arabzadeh]] · [[Charles L. A. Clarke]] — benchmarking LLM judgment paradigms
- [[Jo Kristian Bergum]] — zero-shot hybrid ranking and the baseline critique
- [[Hajer Bouafif]] — agentic memory for personalization
