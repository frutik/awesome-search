---
type: concept
title: "Calibrated Relevance Probability"
aliases: ["calibrated reranker score", "relevance probability", "probability-valued relevance score", "calibrated ranking score"]
tags:
  - concept
  - ranking
  - reranking
  - search-evaluation
  - calibration
created: 2026-09-19
---

# Calibrated Relevance Probability

## Definition

A **calibrated relevance probability** is a reranker output that is a genuine probability — a
number in [0, 1] whose value means *"this fraction of documents scoring here are actually
relevant"* — rather than an uncalibrated score whose only meaningful property is its order
within one result list.

The distinction matters because ranking and thresholding are different jobs. An ordering-only
score answers "which of these is best?" A calibrated probability also answers "is any of these
good enough?" — a question a raw score cannot answer without per-corpus tuning.

## The Contrast with Cross-Encoder Logits

A [[Cross-Encoder]] emits a logit. Its magnitude is arbitrary: it is trained to separate
relevant from irrelevant *within* a candidate list, not to mean anything in absolute terms. To
use it as a cutoff you must pick a threshold empirically, per corpus, and re-pick it whenever
the corpus, the retriever, or the model version changes.

| | Uncalibrated score (logit) | Calibrated probability |
|---|---|---|
| Valid comparison | Within one result list | Across lists, shards, retrieval legs |
| Thresholding | Requires per-corpus tuning | Threshold is portable |
| Interpretation | Ordinal only | "0.9 means ~90% likely relevant" |
| Cross-model comparison | Meaningless | Meaningful if both are calibrated |

## What Calibration Buys You

Once the score is a probability, several operations become available that ordering alone does
not support:

- **Pruning an overfetched pool.** Retrieve deep, then drop everything below a fixed
  probability — the shortlist size becomes adaptive to how good the matches actually are
  instead of a fixed top-K. A single rerank call becomes a rerank *and* a prune.
- **Fusing across retrieval legs.** Scores from different shards or from the lexical and vector
  legs of a [[Hybrid Search]] pipeline are on one comparable axis, which is otherwise the whole
  reason [[Score Normalization]] and [[Reciprocal Rank Fusion]] exist.
- **Gating a downstream step.** A [[RAG]] pipeline can decline to answer, or escalate to a
  wider retrieval, when nothing clears a confidence bar — rather than always feeding the top-K
  whatever its quality.
- **[[Zero Results|Honest empty results]].** "Nothing here is relevant" is expressible.

## Measuring Calibration

Calibration is checked by bucketing scores and comparing the predicted rate against the judged
rate in each bucket: of the documents scored above 0.9, what fraction were actually labeled
relevant? A well-calibrated model tracks the diagonal; an overconfident one sits below it.

This is *not* what [[NDCG]] or [[MRR]] measure. Those are pure ranking metrics — they are
invariant to any monotonic transform of the scores, so a model can be perfectly ordered and
wildly miscalibrated at the same time. Calibration is a separate axis of quality that standard
reranker leaderboards do not report.

### Where Calibration Comes From

Calibration is a training objective, not a side effect. A [[Cross-Encoder]] is trained to
*separate* relevant from irrelevant within a candidate list, which fixes the ordering and
leaves the scale arbitrary. Getting a probability instead means optimizing for it directly —
[[Reinforcement Learning for Calibrated Decisions]] is one stated approach, used for the
[[System One Model|System One Models]] that produced the measurement below. Post-hoc
calibration of an existing scorer (Platt scaling, isotonic regression) is the classical
alternative, at the cost of a held-out judged set per corpus — which is the per-corpus tuning
the property was supposed to eliminate.

Two metrics summarise that check. [[Expected Calibration Error]] averages the per-bucket gap
between predicted and observed rates; [[Brier Score|Brier score]] takes the mean squared error of
the probabilities directly. They answer different questions and are worth reporting together with
log loss, which is the one that punishes *confident* mistakes hard enough to separate a fuzzy
model from a dangerous one.

A worked instance of exactly that separation: on a sentence-classification task,
[[Jev]] scored Brier 0.156 against a TF-IDF baseline's 0.102 — bad but not alarming — while log
loss came in at 1.849 against 0.335, five and a half times worse
([[Adapting Jev to Your Domain with GEPA]]). The second number is the true description of the
failure.

## In Practice

A worked measurement appears in [[Hev meets Jev]], which uses [[Jev]] — a structured-output
model that answers a true-or-false question as a probability — as a reranker over
[[BEIR]] shortlists. On the SciFact subset, documents the model scored above 0.9 were judged
relevant 76% of the time, and documents scored below 0.1, half a percent of the time. The
author's framing is that this — not the nDCG@10 figure, which sits level with the purpose-built
rerankers — is what the approach offers that a cross-encoder does not.

The claim is narrow and worth keeping narrow: a 0.9 bucket at 76% precision is *usable*, not
perfect calibration, and it was measured on one corpus.

## Calibration Is Not Grounding

The limit worth stating alongside the property, put sharply in
[[How to Use Jev - A Practical Guide]]: a scoring model knows only the state it was handed. It
cannot look anything up. So if the candidate set is assembled from a weak source, the model
returns *a well-calibrated judgment about bad material* — the number is honest about the
verdict, and the verdict was reached on evidence that should not have been there.

Two distinct failures hide behind one confident-looking score:

| | What a calibrated probability tells you | What it does not |
|---|---|---|
| Judgment | How likely this verdict is correct | Whether the candidate deserved to be judged |
| Evidence | — | Whether retrieval surfaced the right pool at all |

This is the [[Precision and Recall|recall problem]] wearing a different hat: a reranker scoring
0.95 on the best of thirty wrong documents is well-calibrated and useless. Calibration makes
thresholds portable; it does not make the candidate set correct, and it cannot signal that the
right answer was never retrieved. The same guide's practical rule — retrieve precisely, then
judge cheaply — is the mitigation, along with padding the state as little as possible, since
accuracy degrades as irrelevant material accumulates ([[Clean Context]]).
## Calibration Does Not Travel

A third limit, distinct from the other two: calibration is measured **on a distribution**, not
guaranteed as a property of the model. On data unlike what it was calibrated against — a new
corpus, a new domain, a shifted query mix — it will still return confident-looking probabilities,
and those will be miscalibrated. Nothing in the output signals that it has left familiar ground.

This bites in exactly the case the property is most attractive for. The selling point is a
threshold you need not re-tune per corpus; the catch is that whether the threshold still holds is
itself a per-corpus question. The one published search measurement covers a single [[BEIR]]
subset — a long way from evidence that a 0.9 cutoff means the same thing on a product catalogue
or a legal corpus.

The practical answer is the cheap one: spot-check calibration against a judged sample whenever
the corpus changes, in the same spirit as [[Out-of-Time Validation]]. A calibrated score gives
you a defensible starting threshold, not a permanent one.

## Calibration Is Partly a Property of the Prompt

A fourth limit, and the most actionable one. For a model that takes its question in natural
language, how well-calibrated it is depends on **how you asked** — not only on how it was
trained.

[[Adapting Jev to Your Domain with GEPA]] separates the two. The same [[Jev]] version on the same
300 sentences scored a 10-bin [[Expected Calibration Error|ECE]] of 0.142 under a hand-written
instruction and 0.069 under one optimized against [[Brier Score|Brier score]] — [[Brier Score|Brier]]
itself falling 44.9%. Nothing about the model changed. Roughly half the miscalibration was
attributable to the wording.

Two consequences. First, a vendor's calibration claim and a third party's calibration measurement
can both be honest and disagree, because they are measuring different instructions
([[Prompt Sensitivity]]). Second, calibration is a **tunable objective** rather than an inherited
property: point a [[Prompt Optimization|prompt optimizer]] at a probability metric instead of an
accuracy metric and you can move it deliberately. The catch is that this makes the prompt a
fitted parameter — one that needs a held-out set, and that can learn a corpus's annotation
conventions rather than the truth.
## Related Concepts

- [[Reranking]] — the stage where these scores are produced
- [[Cross-Encoder]] — the incumbent, logit-valued architecture
- [[Score Normalization]] — the workaround calibration would make unnecessary
- [[Reciprocal Rank Fusion]] — rank-based fusion, used precisely because scores are not comparable
- [[Hybrid Search]] — where cross-leg score comparability is the core difficulty
- [[Distribution-Based Score Fusion]] — another attempt at making scores comparable
- [[NDCG]] · [[MRR]] — ranking metrics that are blind to calibration
- [[Search Results Explainability]] — an interpretable score is a partial explanation
- [[Zero Results]] — the case an absolute threshold makes expressible
- [[RAG]] — the pipeline where gating on confidence matters most
- [[LLM as Judge]] — judges face the same calibration question
- [[Brier Score]] · [[Expected Calibration Error]] — the metrics that make the property measurable
- [[Prompt Optimization]] — calibration as something you tune, not inherit
- [[Prompt Sensitivity]] — why two honest calibration measurements of one model can disagree

## Related Articles

- [[Hev meets Jev]] — measures calibration of a probability-valued reranker on BEIR
- [[Introducing System One Models & Jev]] — the training method behind that calibration, as stated by its vendor
- [[Using TypeSafe's Jev for Evals]] — the same property used for rubric verdicts, with three-band act/escalate/discard routing
- [[How to Use Jev - A Practical Guide]] — the limit: calibration describes the verdict, not the evidence
- [[TypeSafe Cookbook - Re-ranking]] — calibrated per-pair scoring on legal case retrieval
- [[Adapting Jev to Your Domain with GEPA]] — the same model measured badly calibrated at its default prompt, and largely fixed by optimizing one

## Related Topics

- [[Reasoning Reranking]] — the frontier this property belongs to
- [[Search Quality Assurance]] — calibration as an evaluation axis
