---
created: 2026-07-30
title: "Improving Zero-Shot Ranking with Vespa Hybrid Search"
aliases:
  - "Improving Zero-Shot Ranking with Vespa Hybrid Search - part one"
source: "https://blog.vespa.ai/improving-zero-shot-ranking-with-vespa/"
author: "[[Jo Kristian Bergum]]"
published: 2023-01-05
type: article
concepts:
  - "[[Zero-Shot Retrieval]]"
  - "[[BM25]]"
  - "[[Dense Passage Retriever]]"
  - "[[NDCG]]"
  - "[[Search Evaluation]]"
topics:
  - "[[Search Quality Assurance]]"
  - "[[Vector Search Tradeoffs]]"
tags: [article, zero-shot, beir, bm25, dense-retrieval, search-evaluation, ndcg, vespa, company-blog]
---

# Improving Zero-Shot Ranking with Vespa Hybrid Search

**Author:** [[Jo Kristian Bergum]] (Chief Scientist, [[Vespa]]) · Part one of two

## Summary

Part one is the problem statement, not the solution. It sets up why a ranking model that wins
on [[MS MARCO]] cannot be trusted on your corpus: proper IR evaluation, what [[BEIR]] measures,
and the concrete case of a dense retriever that beats [[BM25]] in its training domain and loses
to it everywhere else. The hybrid ranking method itself arrives in
[[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two|part two]].

The framing question is the practical one: you are building search for a domain with **no
interaction data and no relevance labels**, so every model you can reach for is being used
zero-shot whether you acknowledge it or not.

---

## In-Domain vs Zero-Shot

The distinction the article draws:

| Setting | Training and evaluation data |
|---|---|
| **In-domain** | Same data distribution — train on a corpus's labels, evaluate on held-out queries from that same corpus |
| **Zero-shot** | Model applied to a new domain with no fine-tuning on it |

Prior work referenced here established that pre-trained language models such as [[BERT]],
fine-tuned for ranking, outperform lexical matching in the controlled in-domain setting. Three
model families are named as the ways to do it:

- single dense vector representations ([[Bi-Encoder]])
- late interaction over multiple vectors ([[ColBERT]] / [[Late Interaction]])
- [[Cross-Encoder|cross-encoders]]

Part one's argument is that the in-domain ordering of these does not survive the move to a new
domain.

## How Ranking Gets Measured

The article walks through IR evaluation as a precondition for the rest: effectiveness measured
against a [[Judgment Lists|labeled judgment set]] using standard metrics — nDCG@10, Precision@10,
Recall@100.

Set against this is the industry habit Bergum names **"LGTM (*Looks Good To Me*)@10"** — eyeballing
the first page for a handful of queries. The joke carries the argument: the reason in-domain
numbers mislead is that most teams never measure across enough queries or enough domains to notice.

See [[Search Evaluation]] and [[NDCG]].

## What BEIR Actually Contains

[[BEIR]] evaluates ranking models across **18 datasets** spanning different domains and task
types, all monolingual English, with **nDCG@10** as the reported metric. The article's point is
that the datasets are not interchangeable — judgment depth in particular varies by orders of
magnitude:

| Dataset | Queries | Judgments per query | Relevance |
|---|---|---|---|
| [[TREC-COVID]] | 50 | ~493.5 | Graded |
| [[Natural Questions]] | 4,352 | ~1.2 | Binary |

Document counts, query volumes, and passage lengths differ as well. A single "BEIR average"
therefore blends a deeply judged 50-query set with a shallowly judged 4,352-query one — the
per-dataset table is where the information lives, a caveat also recorded in the [[BEIR]] note.

## The Corpus Shift That Breaks Models

The comparison the article uses to make domain shift concrete:

| | [[MS MARCO]] | [[Natural Questions]] |
|---|---|---|
| Query length | 5.9 words | 9.2 words |
| Document length | 56.6 words | 76.0 words |
| Document corpus | 8.84M | 2.68M |

MS MARCO derives from web search results; NQ uses Wikipedia passages exclusively. The two look
superficially similar — English, question-like queries, passage-length documents — and are
different enough to break transfer.

## The DPR Result

[[Dense Passage Retriever]], trained on Natural Questions, performs strongly in-domain on NQ and
**underperforms BM25 when evaluated zero-shot on MS MARCO**. The BEIR leaderboard shows the same
pattern more broadly: dense embedding models trained on NQ substantially underperform BM25 across
nearly all BEIR datasets.

This is the article's load-bearing observation, stated as:

> In-domain performance is not a good indicator for out-of-domain generalization.

## Why BM25 Keeps Winning

On MS MARCO specifically, BM25 is reported to trail neural approaches by **7–18 points**. Across
the diverse BEIR datasets it is robust — the article's reading is that BM25 demonstrates superior
generalization precisely because it has nothing fitted to a query distribution.

The practical instruction that follows: evaluate on more than one dataset before believing a
model, and treat BM25 as the baseline to beat rather than a formality. That baseline is what
part two builds first.

## Related Concepts

- [[Zero-Shot Retrieval]] — the concept this article is the vault's clearest statement of
- [[BM25]] — the parameter-free baseline that survives domain shift
- [[Dense Passage Retriever]] — the worked example of in-domain success failing to transfer
- [[Bi-Encoder]] · [[ColBERT]] · [[Cross-Encoder]] — the three model families named
- [[NDCG]] · [[Search Evaluation]] · [[Judgment Lists]] — the measurement apparatus
- [[Precision and Recall]] — the other metrics named (P@10, Recall@100)

## Related Articles

- [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] — the method this post sets up
- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — the follow-on that stops being zero-shot
- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]] compresses
  this argument into "Mistake #2"

## Datasets

- [[BEIR]] — the benchmark under discussion
- [[MS MARCO]] — the in-domain corpus whose numbers mislead
- [[Natural Questions]] — DPR's training domain
- [[TREC-COVID]] — the deeply judged contrast case

## People

- [[Jo Kristian Bergum]] — author

## External References

- Part two — https://blog.vespa.ai/improving-zero-shot-ranking-with-vespa-part-two/
- BEIR — https://github.com/beir-cellar/beir
