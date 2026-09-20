---
title: "Adapting Jev to Your Domain with GEPA"
type: article
tags: [article, calibration, evaluation, prompt-optimization, classification, structured-output]
source: "https://praneeth16.github.io/blog/adapting-jev-with-gepa/"
author:
  - "[[Praneeth Paikray]]"
published: 2026-09-20
created: 2026-09-20
concepts:
  - "[[Calibrated Relevance Probability]]"
  - "[[System One Model]]"
  - "[[Prompt Optimization]]"
  - "[[Brier Score]]"
  - "[[Expected Calibration Error]]"
  - "[[Staged Judging]]"
  - "[[Precision and Recall]]"
  - "[[Prompt Sensitivity]]"
  - "[[Statistical Significance in Search Evaluation]]"
topics:
  - "[[Reception of Jev]]"
  - "[[Search Quality Assurance]]"
companies:
  - "[[TypeSafe]]"
tools:
  - "[[Jev]]"
  - "[[GEPA]]"
datasets:
  - "[[ADE Corpus V2]]"
---

# Adapting Jev to Your Domain with GEPA

**Author:** [[Praneeth Paikray]]
**Source:** https://praneeth16.github.io/blog/adapting-jev-with-gepa/
**Published:** 2026-09-20
**Code:** [companion notebooks](https://github.com/Praneeth16/Praneeth16.github.io/tree/main/study) — both experiments are executed and reproducible

## Summary

Two experiments, run five days after [[Jev]]'s launch, on sentence-level screening of medical
literature for adverse drug events. The first measures [[Jev]] against a supervised baseline and
finds the pattern everyone predicted but nobody had measured: very high recall, mediocre
precision, and **badly calibrated probabilities**. The second uses [[GEPA]], a reflective prompt
optimizer, to rewrite the instruction against a Brier-score objective — raising F1 by 10.6 points
and nearly halving the [[Brier Score|Brier score]] on a fresh test set.

This is the first public measurement that goes at [[Jev]]'s **calibration** claim directly, with a
reliability figure attached. [[Reception of Jev]] records that gap as the open question of the
launch — commenters asked for calibration benchmarks and did not get them. This supplies one, on
one task, and the answer at the default prompt is unflattering.

Not a search paper. It matters here because sentence-level ADE screening is structurally the same
problem as relevance screening: a cheap classifier over a large candidate pool, a threshold you
choose, and a queue a human works through. The review-policy framing below is the part that
transfers.

## Setup

The [[ADE Corpus V2|ADE Corpus V2]] classification split from Hugging Face, pinned to revision
`4ba01c7` — 23,516 rows, 20,895 after normalization and deduplication. Each row is one sentence
from a medical case report, labelled `ade_related` or `not_related`. Model version pinned at
`jev-1.13.0`, using the **Choice** primitive, which returns class probabilities plus a separate
confidence statistic.

**Experiment 1** (seed 42): 20,395 train / 200 validation / 300 test, the test set carrying 61
positives and 239 negatives. Baseline is TF-IDF word unigrams and bigrams (max 50,000 features)
into logistic regression, fit on all 20,395 labelled training sentences — evaluated both at the
default 0.5 threshold and at a validation-selected F1 threshold of 0.31. The author is explicit
that this is **not a matched comparison**: the baseline saw 20,395 labels, [[Jev]] saw a 503-character
natural-language instruction and nothing else.

**Experiment 2** (seed 20260919): 100 train / 100 validation / 300 fresh test, all drawn clear of
the 500 sentences [[Jev]] had already seen in Experiment 1.

## Experiment 1: the default prompt

| Metric | Baseline (0.5) | Baseline (tuned, 0.31) | Jev (original prompt) |
|---|---|---|---|
| Accuracy | 85.7% | 83.7% | 82.0% |
| ADE precision | 84.6% | 58.6% | 53.2% |
| ADE recall | 36.1% | 67.2% | **95.1%** |
| ADE F1 | 50.6% | 62.6% | **68.2%** |

Zero-shot, [[Jev]] beats a fully supervised baseline on F1 and misses only 3 of 61 positives
against the tuned baseline's 20. Relative to that baseline it finds 17 more positives at the cost
of flagging 22 more negatives — a trade a screening workflow will usually take.

The probabilities are a different story:

| Metric | Baseline | Jev (original prompt) |
|---|---|---|
| [[Brier Score\|Brier]] | 0.102 | 0.156 |
| Log loss | 0.335 | **1.849** |
| 10-bin [[Expected Calibration Error\|ECE]] | 0.052 | **0.173** |

The log loss is the damning number — it is the one that punishes confident mistakes, and it is
five and a half times the baseline's. Three supporting observations, each of which is the
["confidently wrong inside a valid schema"](https://news.ycombinator.com/item?id=49717558)
objection made quantitative:

- Confidence came back at exactly **1.0 on 150 of 300** test sentences; 10 of those disagreed
  with the label.
- At confidence ≥ 0.9, **30 disagreements among 233** sentences.
- P(ADE) = 1.0 was assigned to **61 sentences, 12 of them negatives**.

The author's conclusion is blunt and is the finding worth carrying out of the piece: the
confidence statistic **provides no independent evidence of correctness**. Every one of the 300
responses passed schema validation — valid labels, finite probabilities summing to one — and 54
of them were wrong. This is the distinction [[Calibrated Relevance Probability]] rests on, and
the first time anyone has shown the gap with numbers.

The characteristic errors are legible. Missed positives include a drug that *reduced* vomiting
caused by another drug, and symptoms disappearing after withdrawal. False positives cluster on
compact paper titles that merely name a drug class beside a condition, on monitoring warnings,
and on unnamed therapies.

## The review-policy framing

The part that transfers to search. F1 is not what a screening operation buys; what it buys is
**how much of the queue a reviewer can skip without losing positives**. Thresholds picked on the
200-sentence validation set:

| Model | Cutoff | In review | Deprioritized | Positives deferred | Positive retention |
|---|---|---|---|---|---|
| Baseline | 0.135 | 141 | 159 | 6 | 90.2% |
| Jev (original) | 0.400 | 112 | 188 | 3 | 95.1% |

[[Jev]] removes 29 more sentences from the queue *and* defers half as many positives. Poor
calibration did not stop it winning the operational metric — which is exactly why the operational
metric has to be reported separately. Compare [[Staged Judging]]: this is the same cutoff-on-a-
probability manoeuvre, with the escalation band collapsed to two.

## Experiment 2: optimizing the prompt with GEPA

[[GEPA]] (`gepa==0.1.4`) is a Genetic-Pareto optimizer — it inspects failures, proposes instruction
revisions, scores them, and keeps a Pareto front of candidates that win on different examples
rather than a single best. The generative model proposing revisions here is the assistant, not
[[Jev]]; [[Jev]] is only the thing being evaluated.

The objective is the interesting choice: **minimize [[Brier Score|Brier score]]**, not maximize
accuracy. The optimizer is pointed at the probability quality that Experiment 1 found wanting,
and the classification gains fall out as a consequence. Search space of 4 proposals, 20 reflection
examples per round, crossover disabled, capped at 700 metric calls and using 660.

| Candidate | Validation Brier |
|---|---|
| 0 — original | 0.1250 |
| 1 — first revision | 0.0915 |
| **2 — selected** | **0.0839** |
| 3 | 0.0899 |
| 4 | 0.1029 |

What the winning revision actually does is demand three explicit elements — an identifiable drug
or drug class, a specific harmful clinical effect, and a stated relation between them — while
forbidding the model from reconstructing the surrounding report's context or inferring known
toxicities it happens to know about. It also disambiguates compact titles and the *direction* of
the relation: a drug improving a condition is not a drug causing it. In other words, the
optimizer found the two error families by itself and wrote them out of the instruction. The prompt
grows from 503 to 2,020 characters, and mean input tokens per request from 424.2 to 694.2 (+64%).

Results on the 300 fresh sentences, with the original and selected prompts interleaved:

| Metric | Original | GEPA-selected |
|---|---|---|
| Accuracy | 83.0% | 90.7% |
| ADE precision | 54.8% | 71.4% |
| ADE recall | 93.4% | 90.2% |
| ADE F1 | 69.1% | **79.7%** |
| [[Brier Score\|Brier]] | 0.1357 | **0.0747** |
| Log loss | 1.878 | 1.002 |
| 10-bin ECE | 0.142 | 0.069 |

F1 up 10.62 points, 95% bootstrap CI +5.06 to +16.49. Brier down 0.0609, a 44.9% relative
reduction, CI −0.0863 to −0.0372. Both intervals exclude zero — the author does the
[[Statistical Significance in Search Evaluation|significance work]] rather than quoting a point
estimate. Underneath: false positives 47 → 22, false negatives 4 → 6, net 23 fewer errors.

The review-policy table records what that cost:

| Prompt | Cutoff | In review | Deprioritized | Positives deferred | Positive retention |
|---|---|---|---|---|---|
| Original | 0.400 | 106 | 194 | 4 | 93.4% |
| GEPA-selected | 0.400 | 78 | 222 | 6 | 90.2% |

28 fewer sentences to read, two more positives missed. Whether that is an improvement is a policy
question, not a metrics question — and the author notes the validation set had only 21 positives,
so deferring one clears a 95% retention target and deferring two fails it. The threshold signal
is that coarse.

## Cost and latency

Input at $0.042 per million tokens, outputs free. Experiment 1: 505 requests, 213,832 input
tokens, **$0.00898**. Experiment 2: 1,260 evaluations (660 optimization + 600 test), 730,168
tokens in the preserved records, **$0.03067** as a lower bound. Tokens are effectively free at
this scale; the real bill is reflection calls, orchestration and human review, none of which are
in that figure.

Latency is the surprise. Median client-observed **14.69 s** in Experiment 1 (p95 15.62 s), 12.35 s
on a serial smoke test; **19.59 s** median in Experiment 2 (p95 24.37 s) with longer prompts and
up to 24 concurrent requests. The author sets this against TypeSafe's launch claims of 70–500 ms
and says plainly that he cannot separate model inference from transport and queueing — so it is
an observation about the service as reachable in September 2026, not a measurement of the model.
It is still an order of magnitude and a half away from the headline, and it is the second
independent latency reading in the vault after [[Hev]]'s laptop-side numbers.

## Limitations the author states

Unusually complete, and worth reading as a template:

- The classification table has **no article identifiers**, so deduplicating sentences cannot stop
  two sentences from the same case report landing on opposite sides of a split.
- Whether [[Jev]] was pretrained on ADE Corpus or on medical literature generally is **unknown**,
  and the study cannot address it.
- [[GEPA]] may be learning **corpus annotation conventions** rather than clinical validity; nobody
  independently adjudicated the labels.
- One task, one model version, one search of four candidates.
- The TF-IDF baseline is deliberately simple — no modern supervised or generative baseline is
  included.
- Dataset card lists the license as unknown; the corpus is not redistributed with the code.

## Why it matters here

Three things this settles, at least for one task:

1. **Schema validity is not correctness.** Demonstrated with a number: 100% valid responses, 82%
   accurate, confidence 1.0 on ten wrong answers.
2. **The default prompt is not the model's ceiling.** A 44.9% Brier reduction from instruction
   rewriting alone means published zero-shot numbers for [[Jev]] — including [[Hev]]'s
   ([[Hev meets Jev]]) — are lower bounds, and that comparisons against tuned systems are
   comparing an untuned artifact.
3. **Calibration is tunable as an objective.** Optimizing for Brier rather than accuracy improved
   accuracy anyway. That is the practical answer to the calibration complaint in
   [[Reception of Jev]]: not "it is calibrated" but "calibrate it yourself, and measure it."

## Related Concepts

- [[Calibrated Relevance Probability]] — the property under test; this is the first note with a measurement attached
- [[Brier Score]] · [[Expected Calibration Error]] — the metrics used, and the optimization objective
- [[System One Model]] — the model class
- [[Prompt Optimization]] — what [[GEPA]] does, and the lever this article pulls
- [[Prompt Sensitivity]] — a 503→2,020 character rewrite moving F1 ten points is the phenomenon
- [[Staged Judging]] — the review-policy tables are this pattern with two bands
- [[Precision and Recall]] — the recall-heavy default and what tuning traded away
- [[Statistical Significance in Search Evaluation]] — bootstrap CIs on both headline deltas
- [[Reinforcement Learning for Calibrated Decisions]] — the training method whose output is being audited here
- [[LLM as Judge]] — the comparison class for this kind of screening

## Related Notes

- [[Jev]] · [[TypeSafe]] — the model and vendor
- [[GEPA]] — the optimizer
- [[ADE Corpus V2]] — the dataset
- [[Reception of Jev]] — where this lands in the wider argument
- [[Hev meets Jev]] — the other independent measurement, on retrieval rather than classification
- [[Using TypeSafe's Jev for Evals]] — the rubric-design reading of the same confidence behaviour
- [[JEV vs LLM - Your Software Doesn't Want a Conversation It Wants a Decision]] — the audit of the vendor's cost and latency claims this one adds data to
- [[Introducing System One Models & Jev]] — the announcement
