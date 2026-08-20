---
type: article
title: "Automating Search Relevance Assessment at Scale with LLM-as-a-Judge"
source: "https://blog.allegro.tech/2026/08/automating-search-relevance-llm-as-a-judge.html"
author:
  - "[[Joanna Marhula]]"
  - "[[Mateusz Sidor]]"
published: 2026-08-20
created: 2026-08-20
concepts:
  - "[[LLM as Judge]]"
  - "[[Judgment Lists]]"
  - "[[NDCG]]"
topics:
  - "[[Search Quality Assurance]]"
  - "[[Multilingual Search]]"
  - "[[Model Selection and Fine-Tuning Evaluation]]"
companies:
  - "[[Allegro]]"
tags:
  - article
  - llm-judge
  - search-evaluation
  - e-commerce
  - multilingual
  - company-blog
---

# Automating Search Relevance Assessment at Scale with LLM-as-a-Judge

**[[Joanna Marhula]]** and **[[Mateusz Sidor]]** ([[Allegro]]) describe the Relevance Assessment Tool (RAT), an [[LLM as Judge|LLM-as-a-judge]] framework built to automate search relevance evaluation across Allegro's e-commerce catalog — 13 departments in four languages (Polish, Czech, Slovak, Hungarian).

---

## The Annotation Dataset

Search relevance evaluation traditionally relied on subjective assessment or costly human annotation. Allegro built a 380K+ multilingual judgment dataset using 30 experts, with structured labeling guidelines inspired by the [[Amazon ESCI Dataset|ESCI (Exact, Substitute, Complement, Irrelevant) scale]]. Quality control ran dual blind annotators per pair plus expert arbitration on disagreements.

## Prompt Design Findings

- **Few-shot examples hurt performance** — removing examples from the prompt improved both accuracy and inter-rater agreement, the opposite of the usual few-shot assumption.
- **Structured reasoning mattered more than examples** — embedding domain-specific business logic and step-by-step interpretation instructions in the prompt outperformed pattern-matching-style prompts.
- **Simple text-only inputs were sufficient** — adding department and category metadata to the prompt didn't improve results, since product names already carried the information needed.

## Model Performance

Gemini 3.1 Flash Lite served as the cloud baseline, performing strongly across all four languages. A locally-hosted model — internally named cyankiwi-gemma, a 26B Gemma 4 variant — matched or exceeded that baseline on Polish, reaching a quadratic-weighted Cohen's kappa of 0.69.

Accuracy varied sharply by relevance class: strong on "exact match" and "complement" pairs (F1 0.94 and 0.83), but weak on the harder middle distinctions — separating "highly substitutable" from "substitutable" products (F1 0.51 and 0.33).

## Dual-Speed Architecture

RAT serves both real-time (asynchronous API calls) and batch (scheduled jobs) evaluation from shared core logic. For cost and latency, whole product pages are judged in a single request against cloud models — but that same batching strategy degrades local-model reliability, so local inference reverted to single-item requests.

## Migrating to Local Inference

Moving the batch workload to cyankiwi-gemma (a 4-bit AWQ-quantized, "no-thinking" 26B Gemma 4 variant) delivered:

- 60% reduction in inference cost
- ~16 query-product pairs judged per second — 2.5x the throughput of a 12B variant
- Quality parity with the cloud baseline on Polish
- A parse-error rate under 0.2% across languages

## Notable Experimental Findings

- **"No-thinking" model variants outperformed "thinking" ones** — reasoning/chain-of-thought variants consistently scored lower, suggesting relevance judging favors direct classification over multi-step reasoning.
- **Whole-page batching hurt local inference specifically** — for the Gemma 4 4B local variant, quadratic-weighted kappa dropped from 0.56 to 0.34–0.37 under the batched-request pattern that worked fine for cloud models.
- **Czech was the hardest language** for every model tested; Hungarian performed especially well.

## From Labels to Business Metrics

Raw LLM relevance classifications are converted into actionable metrics by correlating them with product position: a mismatch at position #1 is treated as a critical failure, while a mismatch at position #20 is far less severe. This weighting feeds [[NDCG]] and related relevance metrics.

## What's Next

Planned work includes multimodal input using product images (targeting departments like fashion and home design, where text alone under-describes the product), more granular query- and specification-level understanding, and continued expansion of the benchmarking pipeline across the multilingual catalog.

---

## Related Concepts

- [[LLM as Judge]] — core evaluation mechanism
- [[Judgment Lists]] — the 380K+ dataset RAT was validated against
- [[NDCG]] — metric computed from RAT's relevance labels
- [[Amazon ESCI Dataset]] — annotation scale RAT's guidelines were inspired by

## Related Topics

- [[Search Quality Assurance]] — automated, scaled relevance evaluation
- [[Multilingual Search]] — four-language evaluation with real per-language quality variance
- [[Model Selection and Fine-Tuning Evaluation]] — the cloud-vs-local, thinking-vs-no-thinking model bake-off underlying RAT

## Related Articles

- [[Search Quality Assurance with AI as a Judge]] — [[Tao Ruangyam]]; Zalando's production LLM-as-judge pipeline for multi-language pre-launch validation
- [[Classic ML to Cope with Dumb LLM Judges]] — [[Doug Turnbull]]; complementary approach treating LLM judge outputs as ML features
- [[Improving retrieval with LLM-as-a-judge]] — [[Jo Kristian Bergum]]; LLM judge for retrieval benchmarking at Vespa

## Companies

- [[Allegro]] — author organisation; multilingual e-commerce platform

## People

- [[Joanna Marhula]] — author
- [[Mateusz Sidor]] — author
