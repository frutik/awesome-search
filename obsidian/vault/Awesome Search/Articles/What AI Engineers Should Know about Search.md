---
type: article
title: "What AI Engineers Should Know about Search"
source: "https://softwaredoug.com/blog/2024/06/25/what-ai-engineers-need-to-know-search"
author:
  - "[[Doug Turnbull]]"
published: 2024-06-25
created: 2026-05-31
concepts:
  - "[[BM25]]"
  - "[[Judgment Lists]]"
  - "[[Search Evaluation]]"
  - "[[Learning to Rank]]"
  - "[[Query Understanding]]"
  - "[[Query Relaxation]]"
  - "[[Click Models]]"
  - "[[Click Signals]]"
  - "[[Position Bias]]"
  - "[[Precision and Recall]]"
  - "[[NDCG]]"
  - "[[Reranking]]"
  - "[[Collocations]]"
  - "[[Synonyms]]"
  - "[[Retrieval Pipeline]]"
  - "[[LLM as Judge]]"
  - "[[Pointwise Relevance Evaluation]]"
  - "[[Pairwise Relevance Evaluation]]"
  - "[[Listwise Relevance Evaluation]]"
topics:
  - "[[Search Quality Assurance]]"
  - "[[Relevance Program Setup]]"
  - "[[Query Understanding in Practice]]"
tags:
  - article
  - search-fundamentals
  - lexical-search
  - learning-to-rank
  - search-evaluation
---

# What AI Engineers Should Know about Search

**[[Doug Turnbull]]** provides a 58-point primer for AI engineers entering the search domain — covering lexical search fundamentals (BM25, tokenization, phrase search), relevance evaluation and judgment methodology, query understanding pipelines, and Learning to Rank. Written to bridge the gap between LLM/RAG practitioners and classical IR knowledge.

---

## Core Argument

Two things matter most before any algorithmic sophistication:
1. Set up a solid **evaluation framework** — without it, you can't know if changes help
2. How you assemble the retrieval pipeline matters more than your choice of vector DB

---

## Relevance Evaluation (Points 1–11)

- Labels are called **judgments** — historically a human "judge" grades (query, result) pairs as relevant or not
- Three labeling approaches, each with biases:
  - **Human evaluators**: non-expert fatigue, position preference
  - **Clickstream data**: only labels top-N shown results; click = not always relevant
  - **LLM judge**: cheaper, faster — see [[LLM as Judge]]
- [[Position Bias]] / presentation bias: users click what they see; exploit/explore mindset needed to overcome it
- [[Click Models]] convert raw clicks into calibrated judgments
- Metrics: [[NDCG]], ERR, [[MAP]], [[Precision and Recall]]
- [[Precision and Recall|Precision/recall tradeoff]]: wider net → more relevant results, more noise

## BM25 and Lexical Scoring (Points 15–29)

- [[BM25]] = TF×IDF with saturation curves for term frequency and field length normalization
- IDF: rarer term → higher weight; each system uses its own non-linear IDF curve
- Parameters `k1` (TF saturation speed) and `b` (field-length penalty) are tunable
- BM25F: per-field term statistics
- Lexical scoring requires care: term rarity in one field ≠ rarity in another

## Tokenization and Phrase Search (Points 30–36)

- Tokenization choices (n-gram, wordpiece, stemming, punctuation) significantly affect recall
- Lucene token streams are **graphs**: synonyms and multi-word equivalents (USA → United States of America) are branches at the same position
- Phrase search encodes term positions; phrase queries are also graphs
- [[Collocations]] (statistically co-occurring bigrams like "Palo Alto") as "poor man's entities"

## Query Understanding (Points 37–41)

- [[Query Understanding]] covers: category classification, entity extraction, vector mapping
- [[Query Relaxation]]: try strict query first; relax (AND → OR or broader terms) on empty/poor results
- Relevance tiers: high-precision matches boosted, lower-precision as fallback
- Filter queries: exclude known irrelevant results explicitly

## Learning to Rank (Points 42–53)

- [[Learning to Rank]] applies ML to ranking; different from standard classification/regression
- [[Pairwise Relevance Evaluation|SVMRank]]: binary SVM on (relevant, irrelevant) pairs
- LambdaMART (see [[Learning to Rank]]): listwise optimization of [[NDCG]] via gradient boosting; old but reliable
- Multiple [[Reranking]] stages: cheap model for top-1K, expensive cross-encoder for final top-N
- Good LTR features are **orthogonal**: BM25, embeddings, freshness, popularity all measure different things
- Ranking ≠ similarity: high similarity docs can still be spammy or stale

## Signals and Feedback (Points 53–56)

- Signals collection: memorize engaging results per query; upboost on re-query
- Query feedback: learn category/embedding affinity from clicked results (relevance feedback)
- Tools: [SearchArray](https://github.com/softwaredoug/searcharray), [BM25S](https://github.com/xhluca/bm25s)

## Resources Mentioned

- *[Introduction to Information Retrieval](https://nlp.stanford.edu/IR-book/information-retrieval-book.html)* — Manning et al.; foundational IR textbook
- *AI Powered Search* (Manning) — chapters on signals, relevance tiers, presentation bias
- *Relevant Search* (Manning) — relevance tiers chapter
- *[Click Models for Web Search](https://clickmodels.weebly.com/uploads/5/2/2/5/52257029/mc2015-clickmodels.pdf)* — free book on click-to-judgment conversion
- [Awesome Search](https://github.com/frutik/awesome-search) — curated search/IR resource list

---

## Related Concepts

- [[BM25]] — core lexical scoring algorithm
- [[Judgment Lists]] — output of relevance evaluation
- [[Learning to Rank]] — ML-based ranking optimization
- [[Query Understanding]] — pre-retrieval intent parsing
- [[Click Models]] — clickstream → judgment conversion
- [[Position Bias]] — presentation bias in click data
- [[Collocations]] — statistical phrase discovery
- [[Pointwise Relevance Evaluation]] — per-item grading
- [[Pairwise Relevance Evaluation]] — LHS/RHS comparison
- [[Listwise Relevance Evaluation]] — full-list ranking

## Related Articles

- [[Classic ML to Cope with Dumb LLM Judges]] — [[Doug Turnbull]]; LLM judge evaluation in depth
- [[Getting Started on Search Relevance for the Understaffed Search Team]] — broader relevance program setup
- [[Semantic Search Without Embeddings]] — [[Doug Turnbull]]; co-occurrence embeddings via session data

## People

- [[Doug Turnbull]] — author; softwaredoug.com
