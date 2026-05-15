---
title: "Map of Content: Search Quality Assurance & Query Understanding"
tags:
  - moc
  - search-evaluation
  - query-understanding
  - metrics
created: 2026-05-15
---

# Map of Content: Search Quality Assurance & Query Understanding

Entry point for the knowledge graph covering the **Search Quality Assurance** and **Query Understanding** sections of the Awesome Search collection.

---

## Evaluation Metrics

| Metric | Type | Best For |
|--------|------|---------| 
| [[NDCG]] | Offline, graded | Overall ranking quality |
| [[MRR]] | Offline, binary | QA / known-item search |
| [[Hit Rate at K\|Hit Rate@K]] | Offline, binary | RAG retrieval coverage, recommendation systems |
| [[Precision and Recall]] | Offline, foundational | Coverage + accuracy |
| [[Diversity Metrics]] / MMR | Offline, result quality | Ambiguous / exploratory queries |
| [[Click Signals]] | Online, behavioral | Real-user engagement |

## Evaluation Infrastructure

- [[Judgment Lists]] — (query, document, grade) triples; foundation of offline eval
- [[LLM as Judge]] — automated judgment generation; 10–100x cheaper than humans
- [[Search Evaluation]] — full evaluation framework (offline + online + session)
- [[Session-Based Evaluation]] — multi-query session quality; captures reformulation

---

## Query Understanding Components

- [[Query Understanding]] — full framework (formulation + intent + context)
- [[Search Intent]] — what the user is trying to accomplish
- [[Query Segmentation]] — parsing multi-word queries into meaningful units
- [[Query Types]] — taxonomy: navigational, informational, transactional, discovery

---

- [[Query Relaxation]] — term dropping, AND→OR, facet/attribute softening, semantic hierarchy traversal

- [[Query Specificity]] — spectrum from "shoes" (browse) to exact SKU; impacts retrieval strategy, ranking, and UX

## Key People

| Person | Key Contributions |
|--------|------------------|
| [[Daniel Tunkelang]] | Query Understanding series, Evaluating Search series, "Intent Not Inventory" |
| [[Doug Turnbull]] | Flavors of NDCG, Judgment Lists, Quepid, Session eval |
| [[James Rubinstein]] | Measuring Search series (metrics + human approach) |
| [[Andreas Wagner]] | Three Pillars: Findability, Relevance, Discovery |
| [[Jo Kristian Bergum]] | LLM-as-a-judge for retrieval (Vespa) |
| [[Aparna Dhinakaran]] | LLM-as-judge methodology; explanation-first pattern |

---

## Articles by Topic

### Search Evaluation Philosophy
- [[Measuring Search Effectiveness]] — Tunkelang's three-layer framework
- [[Measuring Search - Metrics Matter]] — Rubinstein's metric landscape
- [[Session vs Query based Search Evals]] — session vs. query debate

### Metrics Deep Dives
- [[Flavors of NDCG]] — NDCG formulation variants
- [[Demystifying nDCG and ERR]] — NDCG vs. ERR
- [[Compute MRR using Pandas]] — practical MRR computation
- [[Choosing Your Search Relevance Evaluation Metric]] — metric selection guide

### Judgment & Annotation
- [[What Is a Judgment List]] — fundamentals
- [[Evaluating Search - Using Human Judgments]] — Tunkelang's annotation guide
- [[Measuring Search - A Human Approach]] — Rubinstein's annotation methodology
- [[Succeeding with Relevance Evaluation using PPS Sampling]] — sampling strategy
- [[Improving Retrieval with LLM as a Judge]] — LLM as annotation alternative

- [[LLM-as-a-Judge When to Use Reasoning CoT and Explanations]] — [[Aparna Dhinakaran]]; explanation-first pattern; when CoT helps vs. hurts

### Query Understanding
- [[Query Understanding - Introduction]] — what is QU and why it matters
- [[Query Understanding - Divided into Three Parts]] — formulation + intent + context
- [[AI for Query Understanding]] — LLM-era QU
- [[Mapping Search Queries To Search Intents]] — intent mapping
- [[Search - Intent Not Inventory]] — intent philosophy
- [[Food Discovery with Uber Eats - Building a Query Understanding Engine]] — production QU at scale

---

## Cross-Section Connections

```
Query Understanding ←→ Agentic Search
(agent must understand multi-turn intent)

Judgment Lists ←→ LLM as Judge
(LLM automates what humans do manually)

Session-Based Evaluation ←→ Click Signals
(session behavior is the ground truth)

NDCG ←→ Retrieval Pipeline quality
(NDCG@10 is the standard retrieval benchmark)
```

---

## Relation to Embeddings & Retrieval

The evaluation framework in this section applies to measuring the concepts from the Embeddings section:
- [[Matryoshka Embeddings]] — measured by NDCG at various dimensions
- [[SPLADE]] / [[ELSER]] — "17% NDCG@10 improvement over BM25"
- [[ColBERT]] — BEIR benchmark NDCG@10
- [[RAG]] — evaluated by faithfulness + relevancy (related to NDCG + recall)

See [[MOC - Agentic Search and Embeddings]] for the retrieval section.


## Additional Articles — Evaluation & Metrics

- [[Click Residual - A Query Success Metric]] — label-free query success metric controlling for position bias
- [[What is a Relevant Search Result]] — task-centered "verb the item" definition of relevance
- [[Search Product Management - The Most Misunderstood Role]] — everything in search is an experiment
- [[Thoughts about Managing Search Teams]] — 4 principles: combined org, data-driven, incremental, holistic

## Additional Articles — Query Understanding & Facets

- [[Semantic Equivalence of e-Commerce Queries]] — behavioral + sentence transformer approach to query similarity
- [[Affordances for Conversational Search]] — affordance gap in conversational search UX
- [[Facets - Constraints or Preferences]] — hard vs. soft facet semantics; ML to infer flexibility
- [[Facets, But Which Ones]] — supply-based, demand-based, editorial facet selection strategies
- [[Searching for Goldilocks]] — Wundt Curve, MMR, NP-hard diversity optimization
- [[Thoughts on Search Result Diversity]] — ambiguity hedging, KL-divergence, greedy reranking
- [[Autosuggest Retrieval Data Structures and Algorithms]] — Trie, FST, Levenshtein DFA, N-grams
- [[Autosuggest Ranking]] — probabilistic + LTR ranking for autocomplete; two-phase pipeline
- [[Search Query Expansion with Query Embeddings]] — Grubhub Query2Vec; session-context embeddings
- [[Semantic Search Without Embeddings]] — [[Doug Turnbull]]; taxonomy-based search; hierarchical tokenizer + BM25; LLMs for classification
- [[Superintelligent Retrieval Agent SIRA]] — LLM-enriched BM25 for query expansion
- [[Incremental AI Adoption for E-commerce Search]] — 4-level progression framework for QU maturity