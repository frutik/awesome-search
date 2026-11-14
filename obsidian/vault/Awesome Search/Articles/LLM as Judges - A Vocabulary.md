---
type: article
title: "LLM as Judges: A Vocabulary"
source: "https://www.linkedin.com/pulse/llm-judges-vocabulary-andrew-kornilov-pzgcf/"
author:
  - "[[Andrew Kornilov]]"
published: 2026-11-10
created: 2026-11-10
aliases:
  - LLM as Judge Vocabulary
  - LLM-as-a-judge vocabulary
  - LLM judge glossary
  - LLM judge terminology
concepts:
  - "[[LLM as Judge]]"
  - "[[LLM Jury]]"
  - "[[Levels of Judge Agreement]]"
  - "[[Inter-Annotator Agreement]]"
  - "[[Kendall Rank Correlation]]"
  - "[[Judgment Lists]]"
  - "[[Judge Calibration]]"
  - "[[Calibrated Relevance Probability]]"
  - "[[Knowledge Distillation]]"
  - "[[Staged Judging]]"
  - "[[Statistical Significance in Search Evaluation]]"
  - "[[NDCG]]"
  - "[[Macro and Micro Averaging]]"
topics:
  - "[[Search Quality Assurance]]"
companies:
  - "[[Etsy]]"
  - "[[Allegro]]"
tools:
  - "[[Quepid]]"
tags:
  - article
  - llm-judge
  - search-evaluation
  - inter-annotator-agreement
  - glossary
---

# LLM as Judges: A Vocabulary

**[[Andrew Kornilov]]**, who is involved in AI-as-judge work in [[Quepid]], defines nine words used about [[LLM as Judge|LLM relevance judges]] and what each one actually claims. The premise: "the judge agrees with humans", "the judge is consistent" and "the judge is calibrated" are separate claims, each tested its own way, and a judge can pass one and fail the other two. The closing line: none of these words means "the judge is right"; each covers a single, narrower claim.

The article opens with a short primer on the statistics it quotes: Cohen's, Fleiss' and quadratic-weighted κ, Krippendorff's α, raw agreement, Kendall's τ (with the τ ≥ 0.9 convention), nDCG@10, MRR, accuracy, precision and (macro) F1.

---

## The nine terms

- **Agreement** — compared at four [[Levels of Judge Agreement|levels]]: label, score, ranking, decision; they can move independently. A tape measure reading five centimetres short gets every plank wrong but still sorts them. NormasTCU (2026, Brazilian Portuguese legal search): Cohen's κ 0.32–0.53 on labels, yet Kendall τ ≥ 0.9 between the system rankings built from human and LLM labels on nDCG@10 and MRR. Otero, Parapar and Barreiro (2025) show the reverse: false significance calls at high τ, and a high overall τ hiding disagreement among the top systems ([[Statistical Significance in Search Evaluation]], [[Kendall Rank Correlation]]).
- **Inter-judge agreement** — between two distinct judges: human–human, LLM–human, LLM–LLM, prompt–prompt, panel–single judge. The bar is human–human agreement on your own data, not 1.0; a model scoring well above it against an adjudicated reference deserves a closer look. Reported figures: human–human κ can exceed 0.5 on binary relevance, LLM–human κ around 0.3–0.5 ([[Inter-Annotator Agreement]]).
- **Ordinal and binary agreement** — graded scales need weighted statistics (quadratic-weighted κ, ordinal α). Quietly collapsing graded labels to binary inflates agreement and drops the distinctions [[NDCG]] needs. In *Better Retrievers, Worse Labels* (Kochergin and Konovalov, 2026), three-label κ on context sufficiency was 0.38–0.49; restricted to yes/no cases with "partial" dropped, 0.59–0.79 — partly because the hardest cases left the sample. Report raw agreement next to κ.
- **Self-consistency** — the same judge run more than once on the same pair. Measures stability, not correctness; needs no reference labels. [[Etsy]] samples its annotator several times and is exploring using consistency to send only hard cases to humans.
- **Qrels** — query relevance judgments, i.e. [[Judgment Lists|judgment lists]]; what an LLM judge produces. An unjudged document is not irrelevant, even though evaluation tools score it as non-relevant by convention. In *Better Retrievers, Worse Labels*, from the weakest to the strongest of four retrievers the share of no-gold contexts that actually contained the answer rose from 28% to 72%, and the "no gold, so insufficient" shortcut's precision fell from 0.68 to 0.10.
- **Adjudication** — resolving disagreement by vote or expert; [[Allegro]] used two blind annotators plus an expert arbiter. *Learning* to adjudicate trains the arbiter: CADRE (Shu et al., 2026) uses three specialist agents (product attributes, user intent, business rules) and a trained verifier that debates only on disagreement. On 18,710 held-out e-commerce pairs the verifier reached 0.8334 accuracy, above an oracle picking any correct specialist label (0.8051); debate added about a quarter of a point. [[Classic ML to Cope with Dumb LLM Judges|Doug Turnbull]] shows a smaller version: single-attribute judges with a decision tree learning how much to trust each.
- **Distilled student** — a small model trained to copy an expensive teacher ([[Knowledge Distillation]]). Etsy's o3 annotator → teacher → BERT student (under 10 ms) scores macro F1 0.72 / 0.71 / 0.65. CADRE's mBERT student rose from 0.7456 to 0.7809 accuracy when trained on the reasoning as well as the labels. Risk: the student inherits the teacher's systematic mistakes, so check it against people. The author's own example: *Teaching a Small Model to Judge Like Amazon*.
- **Calibration** — two meanings. [[Judge Calibration]]: measure the judge against a trusted reference per prompt and collection, report pair-level (α, exact and within-one, error direction) and system-ranking agreement (τ), then adjust prompt, rubric or model. Probability calibration ([[Calibrated Relevance Probability]]): "70% relevant" is right 70% of the time. A review threshold can work without it if low scores pick out more errors (discrimination); calibration is what lets 0.4 mean 40%.
- **Jury** — several judges combined into one label ([[LLM Jury]]). A jury of four small open models in *Better Retrievers, Worse Labels* agreed with itself at Fleiss' κ 0.26 yet still reproduced the paper's main finding — good enough for direction, not for labels. In CADRE, letting specialists see earlier reports cut accuracy by 1.14 points, and seeing each other while revising by 1.76 (premature convergence). Members agreeing is inter-judge agreement; the same jury agreeing on a rerun is panel-level self-consistency; neither replaces a check against people.

## How the words fit together

A judge or jury produces qrels. Self-consistency says it is stable; inter-judge agreement, at a stated level and scale, says whether it matches a reference; calibration is that check done carefully before trusting it. Disagreements are adjudicated, by hand or by a learned arbiter, and a distilled student reproduces the result cheaply, mistakes included.

## Sources cited

- [NormasTCU — A Brazilian Portuguese IR Dataset and an Evaluation of LLM-as-a-Judge for Relevance Assessment](https://arxiv.org/abs/2608.27746) (arXiv, 2026)
- [Limitations of Automatic Relevance Assessments with Large Language Models for Fair and Reliable Retrieval Evaluation](https://arxiv.org/abs/2411.13212) — David Otero, Javier Parapar, Álvaro Barreiro (SIGIR 2025)
- [Better Retrievers, Worse Labels](https://arxiv.org/abs/2610.40966) — Ivan Kochergin, Vasily Konovalov (arXiv, 2026)
- [Learning to Adjudicate](https://arxiv.org/abs/2611.02758) — Shi Shu et al. (arXiv, 2026)
- [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]] · [[How Etsy Uses LLMs to Improve Search Relevance]] · [[Classic ML to Cope with Dumb LLM Judges]]
- [Teaching a Small Model to Judge Like Amazon](https://medium.com/@frutik/teaching-a-small-model-to-judge-like-amazon-94e69829e6b4) — Andrew Kornilov (Medium)

---

## Related Concepts

- [[LLM as Judge]] · [[LLM Jury]] · [[Levels of Judge Agreement]] · [[Inter-Annotator Agreement]] · [[Kendall Rank Correlation]]
- [[Judge Calibration]] · [[Calibrated Relevance Probability]] · [[Statistical Significance in Search Evaluation]]
- [[Judgment Lists]] · [[Knowledge Distillation]] · [[Staged Judging]] · [[NDCG]] · [[Macro and Micro Averaging]]

## Related Topics

- [[Search Quality Assurance]]

## Related Articles

- [[Do LLM Judges Actually Agree With Us]] — the earlier piece the four agreement levels come from
- [[Calibrate Before You Trust]] — judge calibration in practice
- [[Replacing Judges with Juries]] — the PoLL paper behind the jury approach
- [[How Etsy Uses LLMs to Improve Search Relevance]] · [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]] · [[Classic ML to Cope with Dumb LLM Judges]]

## Companies

- [[Etsy]] · [[Allegro]]

## People

- [[Andrew Kornilov]] — author
- [[Doug Turnbull]]
