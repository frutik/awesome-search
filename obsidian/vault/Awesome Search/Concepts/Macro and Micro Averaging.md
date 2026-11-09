---
type: concept
created: 2026-11-09
aliases: ["Macro F1", "Micro F1", "macro-F1", "micro-F1", "macro-averaged F1", "macro averaging", "micro averaging", "weighted F1"]
tags: [evaluation, metrics, classification, F1]
---

# Macro and Micro Averaging

Some metrics, F1 among them (see [[Precision and Recall]]), are defined only for binary classification. Applying one to a multiclass or multilabel problem means treating it as one binary problem per class and combining the per-class scores. How the scores are combined has a large effect on the result: a "macro-F1" and a "micro-F1" computed from the same predictions can differ a lot, so a reported F1 needs to say which averaging it used. In search, F1 has a further problem: it measures a set, while search is judged by rankings. Most F1 figures in search score a judge or classifier, not the results the user sees (covered in the F1-in-search section below).

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

## F1 in search: where it fits and where it misleads

F1 comes from classification, and search uses it in two different ways. One is to score a set of results. The other is to score a model inside the search system. Both have limits.

**F1 scores a set, not a ranking.** It ignores order: a relevant result at position 1 counts the same as one at position 50. For a ranked result page, [[NDCG]] and other position-discounted metrics are generally preferred (see [[Precision and Recall]]). The exception is a result set the user reads in full. For progressive scroll, [[Doug Turnbull]] (at [[Shopify]]) argues in [[Finding the Relevance Cutoff - When to Stop Showing Search Results]] that F1 over the whole returned set fits better than NDCG, because it penalises both cutting relevant results and padding with irrelevant ones. Its catch is on the recall side: it needs the total number of relevant results in the corpus.

**Most F1 numbers in search score a component, not the results.** The figures in this note come from relevance judges, query classifiers and routers, which are models sitting inside the search system. A better component F1 does not by itself mean better search. [[Query Classification]] says so directly: what matters commercially is whether the label changes retrieval for the better, measured by zero-results rate and NDCG rather than classifier F1.

**One number hides the boundary that matters.** Relevance labels are graded, and a single F1, micro or macro, smooths over the hard distinctions. [[Allegro]]'s judge ([[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]]) reached per-class F1 of 0.94 on exact matches and 0.83 on complements, but only 0.51 and 0.33 on separating "highly substitutable" from "substitutable", the boundary merchandisers actually argue about. Its overall weighted κ of 0.69 did not show this. F1 also has no chance baseline, so 0.33 does not mean "coin flip". The fix is to report per-class precision, recall and F1, alongside the confusion matrix ([[Do LLM Judges Actually Agree With Us]], [[Inter-Annotator Agreement]]).

**F1 is often not what the operation buys.** When a judge or classifier triages work for human reviewers, the question is how much of the queue can be skipped without losing positives. In [[Adapting Jev to Your Domain with GEPA]], an optimised prompt raised F1 from 69.1% to 79.7% but deferred two more true positives at the same cutoff. [[Staged Judging]] describes the result in terms of review bands and positive retention, not F1.

**F1 is one choice of β.** F1 weights precision and recall equally. In F_β, missed relevant items are weighted by β², so F2 punishes low recall harder and F0.5 punishes low precision harder. [[Rated Ranking Evaluator]] ships F0.5, F1 and F2. Pick β by which error costs more: a missed relevant document in a first-stage retriever, or an irrelevant one shown on the page.

## In the vault

- [[Fine-Tuning Qwen3 Embeddings for Product Category Classification]] reports **macro F1 0.836** alongside **accuracy 87.91%** on a 6-class task. Because micro-F1 equals accuracy in single-label multiclass, these are effectively the micro and macro views of the same classifier. The gap is consistent with some classes doing worse than the overall accuracy suggests.
- [[How Etsy Uses LLMs to Improve Search Relevance]] scores its annotator → teacher → student cascade with multi-class macro F1 (0.72 / 0.71 / 0.65) and also reports per-class F1 for Relevant, Partial and Irrelevant (the "none" mode). The breakdown shows that Irrelevant is the weakest class at every tier, which the single macro number hides. See [[Knowledge Distillation]] and [[LLM as Judge Vocabulary]].
- [[Lightweight Query Routing for Adaptive RAG - A Baseline Study on RAGRouter-Bench]] compares routing features by macro-F1 (TF-IDF 0.928 vs MiniLM embeddings 0.897), with the best router at 93.2% accuracy. See [[Query Classification]].

## Related Concepts
- [[Precision and Recall]] — the binary F1 that these modes average
- [[NDCG]] — the position-aware alternative for ranked results
- [[Inter-Annotator Agreement]] — chance-corrected agreement, the other way to score judge labels
- [[Staged Judging]] — measuring triage by review bands instead of F1
- [[Query Classification]] — multi-class tasks where macro vs micro matters

## Related Articles
- [[scikit-learn - Metrics and Scoring]]
- [[Finding the Relevance Cutoff - When to Stop Showing Search Results]] — F1 for progressive scroll
- [[Do LLM Judges Actually Agree With Us]] — per-class F1 vs overall κ
- [[Adapting Jev to Your Domain with GEPA]] — higher F1, worse positive retention
