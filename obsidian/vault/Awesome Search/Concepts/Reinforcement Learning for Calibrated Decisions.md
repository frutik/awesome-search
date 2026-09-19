---
type: concept
title: "Reinforcement Learning for Calibrated Decisions"
aliases: ["RLCD", "calibrated-decision training"]
tags:
  - concept
  - llm
  - calibration
  - model-training
  - reinforcement-learning
created: 2026-09-19
---

# Reinforcement Learning for Calibrated Decisions

## Definition

**RLCD** is the training method [[TypeSafe]] says it developed for its
[[System One Model|System One Models]], and the stated reason [[Jev]]'s outputs are calibrated
probabilities rather than uncalibrated scores. Its optimization target is *epistemically honest
probabilities* on decision tasks — a model whose stated confidence tracks its actual accuracy.

The method itself is not published in technical detail; what the announcement provides is the
objective and the contrast with the alternatives, not the algorithm.

## The Contrast

The point of the name is what it is *not* optimizing:

| Method | Optimizes for | What that produces |
|---|---|---|
| **RLHF** | Human preference — responses raters like | Fluent, agreeable text; confidence that sounds right |
| **RLVR** | Verifiable rewards — programmatically checkable outputs | Correctness where a checker exists |
| **RLCD** | Calibrated decisions | Probabilities whose value means what it says |

The argument behind it, as the announcement puts it: a model that can do a task 95% of the time
but cannot say when it is in the remaining 5% cannot automate that task. Preference-trained
models are described as overconfident and inconsistent even when explicitly asked for a
confidence estimate — so confidence has to be trained for directly, not prompted for.

## Why It Matters for Ranking

This is the mechanism underneath [[Calibrated Relevance Probability]]. A
[[Cross-Encoder]] is trained to *separate* relevant from irrelevant within a candidate list, so
its logit is ordinal and its scale arbitrary. A model trained for calibration is optimizing a
different thing: that a score of 0.9 should correspond to roughly a 90% chance of being right.

Those two objectives are not in conflict, but neither implies the other, and standard ranking
metrics cannot tell them apart — [[NDCG]] and [[MRR]] are invariant to any monotonic transform
of the scores, so a perfectly ordered model can be arbitrarily miscalibrated and score
identically.

The measured consequence appears in [[Hev meets Jev]]: on the SciFact subset of [[BEIR]],
documents scored above 0.9 were judged relevant 76% of the time and those below 0.1, half a
percent — usable calibration, on one corpus, from a model that was never trained to rank.

## Caveats

- **Vendor-stated.** RLCD is described in a launch announcement, with no paper, no ablation, and
  no independent replication of the training claim.
- **Calibration is domain-dependent.** A model calibrated on its training distribution is not
  automatically calibrated on a new corpus; the one published search measurement covers a single
  BEIR subset.
- **"Cannot hallucinate" is a claim about the output space, not the judgment.** A fixed schema
  guarantees a valid value, not a correct one — a confidently wrong probability is still
  available.

## Related Concepts

- [[Calibrated Relevance Probability]] — what this training buys in a ranking context
- [[System One Model]] — the model class it trains
- [[Cross-Encoder]] — trained for separation, not calibration
- [[NDCG]] · [[MRR]] — ranking metrics blind to calibration
- [[Reinforcement Learning for Search]] — RL applied to ranking objectives instead
- [[LLM as Judge]] — judges with the same confidence problem
- [[Knowledge Distillation]] — the other route to a small, fast scorer

## Related Notes

- [[Jev]] — the model trained this way
- [[TypeSafe]] — the company
- [[Introducing System One Models & Jev]] — the source
- [[Hev meets Jev]] — where the calibration was independently measured
