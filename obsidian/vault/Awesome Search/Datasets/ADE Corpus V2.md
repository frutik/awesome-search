---
type: dataset
title: "ADE Corpus V2"
aliases: ["ADE Corpus", "ade_corpus_v2", "Adverse Drug Event Corpus"]
tags:
  - dataset
  - classification
  - benchmark
  - biomedical
website: https://huggingface.co/datasets/ade-benchmark-corpus/ade_corpus_v2
related_concepts:
  - "[[Precision and Recall]]"
  - "[[Brier Score]]"
  - "[[Staged Judging]]"
created: 2026-09-20
---

# ADE Corpus V2

A biomedical benchmark of sentences drawn from **medical case reports**, labelled for whether
they describe an adverse drug event. The corpus originates with Gurulingappa et al., *Development
of a benchmark corpus to support the automatic extraction of drug-related adverse effects from
medical case reports*, Journal of Biomedical Informatics 45(5): 885–892 (2012), and is
redistributed on Hugging Face.

🔗 https://huggingface.co/datasets/ade-benchmark-corpus/ade_corpus_v2

## Shape

The `ade_corpus_v2_classification` configuration is a sentence-level binary task: each row is
one sentence, labelled `ade_related` or `not_related`. It carries **23,516 rows**, reducing to
**20,895** after normalization and deduplication. Positives are a minority — roughly one sentence
in five in the samples drawn from it.

Two properties worth knowing before using it:

- **There are no article identifiers** in the classification table. Deduplicating sentences
  cannot stop two sentences from the same case report landing on opposite sides of a train/test
  split, so a nominally held-out set is not held out at the document level.
- The Hugging Face **dataset card lists the license as unknown**.

Pinning the revision matters; work in this vault uses `4ba01c7`.

## Why It Appears Here

Not a search dataset. It appears in this vault because
[[Adapting Jev to Your Domain with GEPA]] uses it as the testbed for the first independent
measurement of [[Jev]]'s [[Calibrated Relevance Probability|calibration]], and the task shape
transfers directly to relevance work: a cheap classifier over a large candidate pool, an
imbalanced positive class, a threshold you choose, and a human queue behind it.

That structure is why the paper's **review-policy** tables — how much of the queue can be
skipped, and how many positives get deferred doing it — are the reusable part, rather than the
F1 numbers. It is [[Staged Judging]] on a literature-screening workload, and the same arithmetic
governs a relevance-judging backlog.

Headline measurements taken on it: [[Jev]] at its default prompt reached 95.1% recall at 53.2%
precision on a 300-sentence test set, against 67.2%/58.6% for a threshold-tuned TF-IDF baseline
fit on 20,395 labelled sentences — while scoring substantially worse on every probability
metric. A [[GEPA]]-optimized prompt then moved F1 from 69.1% to 79.7% on a fresh 300-sentence
split.

## Related Concepts

- [[Precision and Recall]] — the imbalanced-class trade this corpus forces
- [[Brier Score]] · [[Expected Calibration Error]] — the probability metrics measured on it
- [[Calibrated Relevance Probability]] — the property under test
- [[Staged Judging]] — the review-policy framing the screening task shares

## Related Articles

- [[Adapting Jev to Your Domain with GEPA]] — [[Praneeth Paikray]]; two experiments on this corpus

## Related Notes

- [[Jev]] · [[GEPA]] · [[Praneeth Paikray]]
- [[BEIR]] — the retrieval-side benchmark [[Jev]] was measured on in [[Hev meets Jev]]
