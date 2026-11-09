---
type: article
created: 2026-11-09
title: "Metrics and scoring: quantifying the quality of predictions"
source: "https://scikit-learn.org/stable/modules/model_evaluation.html"
author: "scikit-learn developers"
tags: [evaluation, metrics, classification, F1, averaging]
---

# Metrics and scoring: quantifying the quality of predictions

Section 3.4 of the scikit-learn user guide (documentation version 1.9.1). This note covers two parts of it: how a binary metric is extended to multiclass and multilabel problems (3.4.4.1), and the precision / recall / F-measure definitions (3.4.4.9).

## From binary to multiclass and multilabel

Some metrics, F1 among them, are defined only for binary classification. To apply one to a multiclass or multilabel problem, the data is treated as one binary problem per class, and the per-class scores are combined. The `average` parameter picks how they are combined:

- **`macro`**: the plain mean of the per-class scores, so every class counts equally. This brings out how rare but important classes are doing. It also assumes all classes matter equally, which is often false, so the usually weak score on an infrequent class gets overweighted.
- **`weighted`**: the mean of the per-class scores, each weighted by how often that class appears in the true labels. It adjusts for class imbalance, and the resulting F-score may fall outside the range between precision and recall.
- **`micro`**: every sample–class pair contributes equally. The numerators and denominators are summed across classes and a single ratio is computed from the totals. It suits multilabel problems, and multiclass problems where a majority class is left out.
- **`samples`**: multilabel only. The metric is computed for each sample over its true and predicted labels, and those values are averaged.
- **`None`**: returns one score per class and does no averaging.

Two consequences:
- When all labels are included in a multiclass (single-label) problem, micro-averaged precision, recall and F all equal **accuracy**.
- Macro F is the arithmetic mean of the per-class F scores, **not** the harmonic mean of macro precision and macro recall. Both versions appear in the literature, and they give different numbers.

## F-measure

F_β is a weighted harmonic mean of precision and recall, from 0 (worst) to 1 (best):

F_β = (1 + β²) · P · R / (β² · P + R)

With β = 1 precision and recall count equally, which gives F1 = 2·tp / (2·tp + fp + fn). The score is undefined when tp, fp and fn are all zero. scikit-learn returns 0 in that case by default, and the `zero_division` parameter changes this.

## Related Concepts
- [[Macro and Micro Averaging]]
- [[Precision and Recall]]
