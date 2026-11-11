---
type: article
title: "Long-form Factuality in Large Language Models"
source: "https://arxiv.org/abs/2403.18802"
pdf: "https://arxiv.org/pdf/2403.18802"
repo: "https://github.com/google-deepmind/long-form-factuality"
author:
  - "[[Jerry Wei]]"
published: 2024-03-27
created: 2026-11-11
venue: "NeurIPS 2024"
companies:
  - "[[Google]]"
datasets:
  - "[[LongFact]]"
concepts:
  - "[[Atomic Claim Verification]]"
  - "[[Hallucination Detection]]"
  - "[[LLM as Judge]]"
  - "[[Precision and Recall]]"
topics: []
tags:
  - article
  - factuality
  - evaluation
  - llm
  - agents
---

# Long-form Factuality in Large Language Models

**Authors:** [[Jerry Wei]], Chengrun Yang, Xinying Song, Yifeng Lu, Nathan Hu, Jie Huang, Dustin Tran, Daiyi Peng, Ruibo Liu, Da Huang, Cosmo Du, Quoc V. Le · Google DeepMind ([[Google]]), Stanford, UIUC · **arXiv:2403.18802**, NeurIPS 2024 · code: [github.com/google-deepmind/long-form-factuality](https://github.com/google-deepmind/long-form-factuality)

## Summary

Three contributions for measuring the factuality of multi-paragraph answers: a prompt set ([[LongFact]]), an automated rater (**SAFE**, Search-Augmented Factuality Evaluator), and an aggregate metric (**F1@K**) that adds recall to factual precision. The authors deliberately say *factuality* (agreement with established world knowledge) rather than *hallucination* (agreement with the model's own knowledge).

## SAFE

An LLM agent that rates each fact in a response against Google Search rather than a fixed reference:

1. **Split** each sentence of the response into individual facts.
2. **Revise** each fact to be self-contained, replacing pronouns and vague references with the entities they refer to.
3. **Check relevance** of each fact to the prompt, which filters out statements like "I don't know".
4. **Rate** each relevant fact as supported or not, through a multi-step loop: the model writes a search query from the fact and the results so far, keeps three results per query, and after five steps reasons over everything it found.

Output per response: counts of supported, not-supported and irrelevant facts. The implementation used gpt-3.5-turbo-0125 and the Serper Google Search API. The authors see the main novelty in the agent issuing several queries in sequence and reasoning over them, which handles claims a single lookup cannot settle. See [[Atomic Claim Verification]].

## SAFE vs. Crowdsourced Humans

On the human annotations released with [[FActScore - Fine-grained Atomic Evaluation of Factual Precision|FActScore]] — 496 responses, 16,011 individual facts — SAFE agreed with the human label on **72.0%** of facts. On a random 100 of the disagreements, re-annotated by the researchers with full internet access, SAFE was right **76%** of the time and the crowd workers 19%.

Rating all 496 responses cost $96.31 ($64.57 for LLM calls, $31.74 for search), or **$0.19 per response**, against $4 per response for the human annotation — more than 20× cheaper.

## F1@K

Precision alone rewards a model for saying less. F1@K adds recall without needing a list of all relevant facts: K is a hyperparameter for the number of supported facts a user would want, recall is min(supported / K, 1), and F1@K combines that with factual precision. A response scores 1 only if it has no unsupported facts and at least K supported ones. Irrelevant facts are left out of both terms.

## Benchmark

Thirteen models from four families (Gemini, GPT, Claude, PaLM-2) on 250 LongFact-Objects prompts, with K = 64 (median number of facts per response) and K = 178 (maximum). Larger models generally scored higher within each family. At K = 64 the top three were GPT-4-Turbo (95.0), Gemini-Ultra (91.7) and PaLM-2-L-IT-RLHF (91.0).

## Open Questions

The authors list improving SAFE's reliance on a search-enabled LLM agent, and note it is still unclear how to measure hallucination — against the model's internal knowledge — in long-form output.

## Related Concepts

- [[Atomic Claim Verification]] — the method family; SAFE replaces the fixed knowledge source with search
- [[Hallucination Detection]] — the related problem the authors distinguish from factuality
- [[Precision and Recall]] — F1@K's precision and recall terms
- [[LLM as Judge]] — SAFE is an agentic judge, rating one fact at a time

## Related Datasets

- [[LongFact]] — the prompt set introduced here

## Related Articles

- [[FActScore - Fine-grained Atomic Evaluation of Factual Precision]] — the decomposition and the human annotations SAFE is validated against

## People

- [[Jerry Wei]] — first author
