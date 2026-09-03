---
title: "ANTIQUE"
aliases: ["ANTIQUE benchmark", "ANTIQUE dataset"]
tags:
  - dataset
  - benchmark
  - information-retrieval
  - search-evaluation
  - question-answering
  - non-factoid
type: dataset
source: "Helia Hashemi, Mohammad Aliannejadi, Hamed Zamani, W. Bruce Croft — arXiv:1905.08957 (2019)"
domain: open-domain non-factoid question answering (Yahoo! Answers)
related_concepts:
  - "[[Search Evaluation]]"
  - "[[Judgment Lists]]"
  - "[[LLM as Judge]]"
  - "[[Semantic Relevance]]"
website: https://arxiv.org/abs/1905.08957
created: 2026-09-03
---

# ANTIQUE

## Overview

**ANTIQUE** is a benchmark for **answer passage retrieval on non-factoid questions** — the "how", "why" and "what do you think" questions that have no short extractable answer. Its authors built it because, in their framing, "the community still feels the significant lack of large-scale non-factoid question answering collections with real questions and comprehensive relevance judgments."

The questions are real: **2,626 open-domain non-factoid questions** asked by actual users on Yahoo! Answers, spanning a diverse set of categories, with **34,011 manual relevance annotations** collected through crowdsourcing.

Introduced in *ANTIQUE: A Non-Factoid Question Answering Benchmark* by Helia Hashemi, Mohammad Aliannejadi, Hamed Zamani and W. Bruce Croft (arXiv:1905.08957, 2019).

## Grade Scale

A four-level scale, defined in terms of whether the answer is *convincing* rather than whether it contains a fact — which is what makes it non-factoid:

| Grade | Meaning |
|---|---|
| 4 | "It looks reasonable and convincing. Its quality is on par with or better than the 'Possibly Correct Answer.'" |
| 3 | "It can be an answer to the question, however, it is not sufficiently convincing." |
| 2 | "It does not answer the question or if it does, it provides an unreasonable answer, however, it is not out of context." |
| 1 | "It is completely out of context or does not make any sense." |

Note the direction: 1 is the *worst* grade, not the best, and there is no zero.

## Splits

| Split | Questions | Annotations |
|---|---|---|
| Train | 2,426 | 27,422 |
| Test | 200 | 6,589 |

Test questions were randomly sampled from the nfL6 collection after pre-processing and filtering, with candidate answers gathered by **depth-10 pooling** across multiple retrieval models — so the test split is judged far more deeply than the training split.

## Annotation Process

Three workers independently annotated each question-answer pair, with the label set by majority vote. Disagreements went to a second round; the 776 pairs still contested after two rounds were resolved by an expert annotator. The paper reports no inter-annotator agreement coefficient.

## Why It Matters Here

ANTIQUE is the counterweight in [[Benchmarking LLM-based Relevance Judgment Methods]]: alongside the web-passage collections of the [[TREC Deep Learning Track]], it tests whether [[LLM as Judge|LLM judges]] behave differently when "relevant" means *convincing* rather than *containing the answer*. It is the vault's only entry covering non-factoid retrieval evaluation.

## Related Datasets

- [[TREC Deep Learning Track]] — the factoid-leaning web counterpart it is paired against
- [[Natural Questions]] — question answering, but factoid
- [[MS MARCO]] — large-scale passage ranking with shallow judgments

## Related Concepts

- [[Search Evaluation]]
- [[Judgment Lists]] — ANTIQUE's crowdsourced annotations are one
- [[LLM as Judge]] — evaluated against these judgments
- [[Semantic Relevance]] — relevance here is defined by persuasiveness, not fact match

## Related Articles

- [[Benchmarking LLM-based Relevance Judgment Methods]] — uses ANTIQUE alongside TREC DL
