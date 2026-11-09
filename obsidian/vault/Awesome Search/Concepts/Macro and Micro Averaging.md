---
type: concept
created: 2026-11-09
aliases: ["Macro F1", "Micro F1", "macro-F1", "micro-F1", "macro-averaged F1", "macro averaging", "micro averaging", "weighted F1"]
tags: [evaluation, metrics, classification, F1]
---

# Macro and Micro Averaging

Some metrics, F1 among them (see [[Precision and Recall]]), are defined only for binary classification. Applying one to a multiclass or multilabel problem means treating it as one binary problem per class and combining the per-class scores. How the scores are combined has a large effect on the result: a "macro-F1" and a "micro-F1" computed from the same predictions can differ a lot, so a reported F1 needs to say which averaging it used.

---

## The averaging modes

Using the names from scikit-learn's `average` parameter:

| Mode | How it combines | What it rewards |
|---|---|---|
| **macro** | Mean of the per-class scores, every class weighted equally | Performance on rare classes counts as much as on common ones |
| **weighted** | Mean of the per-class scores, each weighted by the class's frequency in the true labels | Adjusts for class imbalance |
| **micro** | Sums the numerators and denominators (tp, fp, fn) across all classes, then computes one ratio | Every sample–class pair counts equally, so common classes dominate |
| **samples** | Computes the metric per sample over its labels, then averages across samples | Multilabel only |
| **none** | No combining: one score per class | The per-class breakdown |

## Properties worth knowing

- **Micro-F1 equals accuracy** in single-label multiclass problems when all classes are included. Micro precision, micro recall and micro F all become the same number.
- **Macro-F1 is the mean of the per-class F1 scores**, not the harmonic mean of macro precision and macro recall. Both definitions appear in the literature and they give different numbers, so two "macro-F1" figures are not always comparable.
- **Macro averaging has a cost**: assuming all classes matter equally is often wrong, and it gives extra weight to the usually poor score on an infrequent class. That same property makes it useful when a rare class is important.
- **Weighted F1 can fall outside** the range between precision and recall.
- **Micro averaging** suits multilabel problems, and multiclass problems where a dominant class is excluded from the score.

## In the vault

- [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]] reports **macro F1 0.836** alongside **accuracy 87.91%** on a 6-class task. Because micro-F1 equals accuracy in single-label multiclass, these are effectively the micro and macro views of the same classifier. The gap is consistent with some classes doing worse than the overall accuracy suggests.
- [[How Etsy Uses LLMs to Improve Search Relevance]] scores its annotator → teacher → student cascade with multi-class macro F1 (0.72 / 0.71 / 0.65) and also reports per-class F1 for Relevant, Partial and Irrelevant (the "none" mode). The breakdown shows that Irrelevant is the weakest class at every tier, which the single macro number hides. See [[Knowledge Distillation]] and [[LLM as Judge Vocabulary]].
- [[Lightweight Query Routing for Adaptive RAG - A Baseline Study on RAGRouter-Bench]] compares routing features by macro-F1 (TF-IDF 0.928 vs MiniLM embeddings 0.897), with the best router at 93.2% accuracy. See [[Query Classification]].

## Related Concepts
- [[Precision and Recall]] — the binary F1 that these modes average
- [[Inter-Annotator Agreement]] — the other common way to score judge or annotator labels
- [[Query Classification]] — multi-class tasks where macro vs micro matters

## Related Articles
- [[scikit-learn - Metrics and Scoring]]
