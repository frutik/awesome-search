---
type: concept
title: "Atomic Claim Verification"
aliases: ["atomic fact verification", "atomic fact decomposition", "claim decomposition", "FActScore", "SAFE", "Search-Augmented Factuality Evaluator", "F1@K", "long-form factuality evaluation"]
tags:
  - concept
  - factuality
  - evaluation
  - llm
related_concepts:
  - "[[Hallucination Detection]]"
  - "[[LLM as Judge]]"
  - "[[RAG]]"
  - "[[Precision and Recall]]"
created: 2026-11-11
---

# Atomic Claim Verification

Evaluating a long generated text by splitting it into **atomic claims** — short statements carrying a single piece of information each — and checking each claim on its own against evidence. Instead of one pass/fail verdict for the whole text, the result is a fraction of supported claims, plus the list of claims that failed.

---

## Why Decompose

One verdict for a whole passage throws away most of the information. Long generations mix true and false statements, and so do single sentences: in ChatGPT biographies, 40% of sentences contained both. Sentence-level scoring then needs either a subjective "partially supported" label or a strict rule under which a mostly-right text and a mostly-wrong one both score zero. Atomic claims avoid both. Each check is narrow enough to have a clear answer, and the failures point at exactly what is wrong.

## The Pipeline

1. **Split** the text into atomic claims, usually with an LLM.
2. **Make each claim self-contained**, replacing pronouns and vague references with the entities they refer to, so a claim can be checked without the surrounding text.
3. **Filter irrelevant claims**, ones that are not about the prompt, such as "I don't know".
4. **Check each claim against evidence**: retrieve passages and ask a judge whether they support the claim.
5. **Aggregate** into a score.

## Two Reference Implementations

| | FActScore | SAFE |
|---|---|---|
| Paper | [[FActScore - Fine-grained Atomic Evaluation of Factual Precision]] ([[Sewon Min]] et al., 2023) | [[Long-form Factuality in Large Language Models]] ([[Jerry Wei]] et al., Google DeepMind, 2024) |
| Evidence | A fixed, named knowledge source (Wikipedia), via a retriever | Google Search, queried by an LLM agent in up to five steps per claim |
| Truth means | Supported by the chosen source | Supported by search results |
| Metric | Factual precision: share of supported claims | F1@K: precision plus recall against K, the number of supported facts a user wants |
| Validation | Under 2% error against human FActScore | 72% fact-level agreement with crowd annotators; right in 76% of 100 disagreements |
| Cost | $4 per generation for human annotation | $0.19 per response, over 20× cheaper than humans |

FActScore treats truth as **relative to a chosen knowledge source** rather than global, which suits [[RAG]] and enterprise settings where the trusted corpus is defined. SAFE's main addition is the agent: it writes a search query, reads the results, and writes the next query, which settles claims that one lookup cannot.

## Findings Worth Knowing

- **Retrieval is what makes automatic checking work.** An evaluator LM with no retrieved evidence either had a high error rate or got the ranking of the evaluated models wrong.
- **A stronger judge is not automatically a better estimator.** ChatGPT checked individual facts more accurately than a smaller model, but its errors leaned one way, toward calling unsupported facts supported, so it overstated the aggregate score. A smaller, unbiased checker came closer overall.
- **Precision alone rewards saying less.** A model that abstains often, or makes fewer claims, scores higher. Report the abstention rate and claims per response alongside the score, or use a recall-aware metric like F1@K.
- **Errors concentrate where knowledge is thin:** rarer entities, and facts later in a generation. Search augmentation narrows the gap but does not close it, and citations did not track correctness.

## Limits

FActScore's authors state the assumptions plainly: each claim is objectively checkable, all claims are equally important, and the knowledge source does not contradict itself. So the method does not suit nuanced, open-ended or debatable content, or sources that frequently conflict. They also judge it unsuitable for text containing intentional or implicit deception, where statements can each be supported while the text as a whole misleads, and claim-by-claim checking is blind to that. It does not penalise omissions either: every stated claim can be supported while something that should have been said is missing.

## In Search Evaluation

This is the generation-side counterpart to relevance evaluation. Retrieval metrics tell you the right passage was found; atomic claim verification tells you which sentences of the answer the evidence actually supports. It is the finer-grained version of the reference-based family in [[Hallucination Detection]], and the checking step is itself an [[LLM as Judge]] — deciding, one claim at a time, whether the evidence supports it.

## Related Concepts

- [[Hallucination Detection]] — the broader problem; this is its claim-level, reference-based form
- [[LLM as Judge]] — the per-claim checker
- [[RAG]] — retrieval supplies the evidence, and RAG answers are a main target
- [[Precision and Recall]] — FActScore is precision-only; F1@K adds recall
- [[LLM Jury]] — splits the work across several judges rather than splitting the claim

## Related Datasets

- [[LongFact]] — long-form, multi-topic prompts built for SAFE

## Related Articles

- [[FActScore - Fine-grained Atomic Evaluation of Factual Precision]]
- [[Long-form Factuality in Large Language Models]]

## People

- [[Sewon Min]] — FActScore
- [[Jerry Wei]] — SAFE, F1@K, LongFact
