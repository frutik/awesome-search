---
type: person
title: "Praneeth Paikray"
aliases: ["Praneeth16"]
tags:
  - person
  - evaluation
  - calibration
website: https://praneethpaikray.com/
blog: https://praneeth16.github.io/
github: https://github.com/Praneeth16
linkedin: https://www.linkedin.com/in/praneeth-paikray/
created: 2026-09-20
---

# Praneeth Paikray

Practitioner who published the first independent measurement of [[Jev]]'s **calibration**, five
days after the model's launch — [[Adapting Jev to Your Domain with GEPA]].

🔗 https://praneethpaikray.com/ · https://github.com/Praneeth16 · [LinkedIn](https://www.linkedin.com/in/praneeth-paikray/)

## What He Measured

Two experiments on sentence-level adverse-drug-event classification over [[ADE Corpus V2]],
published with executed notebooks rather than described from memory:

1. **[[Jev]] at the default prompt against a supervised TF-IDF baseline.** Zero-shot, [[Jev]]
   won on F1 (68.2% vs 62.6%) and recall (95.1% vs 67.2%) while losing badly on every
   probability metric — [[Brier Score|Brier]] 0.156 vs 0.102, log loss 1.849 vs 0.335, 10-bin
   [[Expected Calibration Error|ECE]] 0.173 vs 0.052.
2. **The same model with a [[GEPA]]-optimized prompt.** Optimizing against Brier score rather
   than accuracy raised F1 from 69.1% to 79.7% on a fresh test set and cut Brier by 44.9%.

## Why the Work Matters Here

Three contributions that no other piece in this vault supplies.

**He put a number on "valid is not correct."** Every one of 300 responses passed schema
validation; 54 were wrong; the confidence statistic came back at exactly 1.0 on 150 of them,
ten of those incorrect. [[Reception of Jev]] records the "confidently wrong inside a valid
schema" objection as the loudest criticism of the launch and the calibration evidence as the
thing nobody produced. This is that evidence, and it goes against the vendor.

**He showed the default prompt is not the ceiling.** A prompt rewrite moving F1 ten points and
halving Brier means published zero-shot figures for the model — [[Hev]]'s included — are lower
bounds ([[Prompt Sensitivity]]).

**He reported latency that contradicts the vendor's.** Median client-observed 14.69 s and
19.59 s across the two experiments, against [[TypeSafe]]'s stated 70–500 ms, while saying
plainly that he cannot separate inference from transport and queueing.

The methodological care is the other reason to read him: bootstrap confidence intervals on both
headline deltas, prompts interleaved on the same test set, the optimization and test splits kept
disjoint from the sentences the model had already seen, and a limitations section that names his
own study's holes — no article identifiers to group sentences by source report, unknown
pretraining exposure, and the possibility that [[GEPA]] learned the corpus's annotation
conventions rather than clinical validity.

## Related Articles

- [[Adapting Jev to Your Domain with GEPA]] — the two experiments

## Related Concepts

- [[Calibrated Relevance Probability]] · [[Brier Score]] · [[Expected Calibration Error]]
- [[Prompt Optimization]] · [[Prompt Sensitivity]]
- [[Staged Judging]] — the review-policy framing his tables use

## Related Notes

- [[Jev]] · [[TypeSafe]] · [[GEPA]] · [[ADE Corpus V2]]
- [[Reception of Jev]] — where his measurement lands in the argument
- [[Hev]] — the other independent measurer, on retrieval rather than classification
