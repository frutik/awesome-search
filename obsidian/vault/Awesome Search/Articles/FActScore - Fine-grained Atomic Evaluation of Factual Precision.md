---
type: article
title: "FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long
  Form Text Generation"
source: https://arxiv.org/abs/2305.14251
pdf: https://arxiv.org/pdf/2305.14251
repo: https://github.com/shmsw25/FActScore
author:
  - "[[Sewon Min]]"
published: 2023-05
created: 2026-11-11
venue: arXiv (cs.CL)
companies:
  - "[[Meta]]"
concepts:
  - "[[Atomic Claim Verification]]"
  - "[[Hallucination Detection]]"
  - "[[LLM as Judge]]"
  - "[[Precision and Recall]]"
  - "[[RAG]]"
topics: []
tags:
  - article
  - factuality
  - evaluation
  - llm
---

# FActScore: Fine-grained Atomic Evaluation of Factual Precision

**Authors:** [[Sewon Min]], Kalpesh Krishna, Xinxi Lyu, Mike Lewis, Wen-tau Yih, Pang Wei Koh, Mohit Iyyer, Luke Zettlemoyer, Hannaneh Hajishirzi · University of Washington, UMass Amherst, Allen Institute for AI, [[Meta]] AI · **arXiv:2305.14251** (2023) · code: [github.com/shmsw25/FActScore](https://github.com/shmsw25/FActScore), `pip install factscore`

## Summary

A pass/fail verdict on long-form text throws away most of the information: a generation is usually a mix of supported and unsupported statements, and even a single sentence mixes them (in ChatGPT output, 40% of sentences did). FActScore splits a generation into **atomic facts** — short statements carrying one piece of information each — and reports the fraction supported by a chosen knowledge source. See [[Atomic Claim Verification]].

## Two Design Choices

- **The atomic fact is the unit**, not the sentence. Sentence-level scoring needs either a subjective "partially supported" label or a strict rule that scores both a mostly-right and a mostly-wrong bio at 0.
- **Truth is relative to a named knowledge source**, not global. The score asks whether a fact is supported by the source the end user trusts — here, English Wikipedia.

The score is averaged only over responses where the model did not abstain. It measures **precision, not recall**: a model that abstains often or says less can score higher. The authors recommend always reporting FActScore together with the abstention rate and the average number of facts per response.

## Human Evaluation

People biographies generated from "Tell me a bio of <entity>" for 183 Wikidata entities, decomposed into atomic facts (InstructGPT drafts, revised by annotators) and labelled Supported / Not-supported / Irrelevant against Wikipedia. Annotation cost $4 per generation; agreement between two annotators on 10% of the data was 88–96%.

| Model | FActScore |
|---|---|
| InstructGPT | 42.5% |
| ChatGPT | 58.3% |
| PerplexityAI (search-augmented) | 71.5% |

- **Rarer entities score far lower** — for ChatGPT, from 80% down to 16% — and search augmentation does not remove the drop: PerplexityAI's score fell by 50% relative at the atomic level.
- **Later facts are worse** than earlier ones in the same generation, so short-answer evaluation misses errors that arise late in long outputs.
- **Citations did not track correctness** for PerplexityAI: 36.0% of supported and 37.6% of unsupported sentences carried a citation. A sample of its errors also included copying subjective quotes as fact and pulling irrelevant search results into the answer.

## Automatic Estimator

The estimator splits text into atomic facts, then checks each with an evaluator LM. Variants: the LM alone with no context; **Retrieve→LM**, which retrieves passages from the knowledge source (GTR retriever) and asks True/False; a nonparametric masked-LM likelihood (NP); and an ensemble that marks a fact Supported only if both Retrieve→LM and NP do.

- **Retrieval matters most.** The no-context variant either had a high error rate or failed to preserve the ranking of the three models.
- **The best variant had under 2% error** against the human FActScore.
- **The stronger judge was not the better estimator.** ChatGPT validated individual facts better, but most of its mistakes were marking unsupported facts as supported, so it overestimated the aggregate score; Inst-LLaMA + NP was unbiased and closer in aggregate. The best variant depended on the model being evaluated.
- Applied to 6,500 generations from 13 subjects (12 LMs plus human-written bios), which would have cost about $26K by human annotation. GPT-4 and ChatGPT were more factual than the public models, and Vicuna and Alpaca were among the best public ones.

## Limitations

FActScore assumes facts are objectively checkable, equally important, and that the knowledge source is internally consistent. It does not fit nuanced, debatable or open-ended content, sources that frequently contradict each other, or text containing intentional deception. It also does not penalise missing important information.

## Related Concepts

- [[Atomic Claim Verification]] — the method this paper defined
- [[Hallucination Detection]] — the wider problem; FActScore is a reference-based member of it
- [[Precision and Recall]] — why a precision-only score rewards abstention
- [[LLM as Judge]] — the evaluator LM is a judge checking one fact at a time
- [[RAG]] — retrieval is what makes the estimator work

## Related Articles

- [[Long-form Factuality in Large Language Models]] — SAFE builds on this decomposition, adds search-based checking and a recall term

## People

- [[Sewon Min]] — first author
