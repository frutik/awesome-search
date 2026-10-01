---
type: article
title: "sQuIrRel: Large-Scale Evaluation of E-commerce Query Classification Models"
source: https://www.amazon.science/publications/squirrel-large-scale-evaluation-of-e-commerce-query-classification-models
pdf: https://cdn.amazon.science/13/cb/22a64f874be28c7f9eb6601a3fa2/squirrel-large-scale-evaluation-of-e-commerce-query-classification-models.pdf
doi: https://doi.org/10.1145/3701716.3715261
author: "Anna Tigunova, Ghadir Eraisha, Ezgi Akcora (Amazon)"
published: 2025-05-08
venue: "Companion Proceedings of the ACM Web Conference 2025 (WWW Companion '25)"
aliases:
  - sQuIrRel
  - Query Intent from Relevance
tags:
  - article
  - paper
  - query-classification
  - query-understanding
  - search-evaluation
  - e-commerce
topics:
  - "[[Query Classification]]"
  - "[[E-commerce Search Evaluation Datasets]]"
  - "[[Query Understanding in Practice]]"
concepts:
  - "[[Query Understanding]]"
  - "[[Search Intent]]"
  - "[[Click Signals]]"
  - "[[Implicit Judgments]]"
  - "[[Judgment Lists]]"
  - "[[Precision and Recall]]"
datasets:
  - "[[Amazon ESCI Dataset]]"
created: 2026-10-01
---

# sQuIrRel: Large-Scale Evaluation of E-commerce Query Classification Models

A five-page Amazon paper (Anna Tigunova, Ghadir Eraisha, Ezgi Akcora; WWW Companion '25) proposing **sQuIrRel — "Query Intent from Relevance"**, a procedure for *automatically* building evaluation data for e-commerce [[Query Classification|query classifiers]]. Instead of labelling queries by hand or by clicks, it borrows labels from the products a high-precision relevance model judges to be exact matches. The paper applies it to query-to-product-type (Q2PT) prediction — mapping a query like "carry on luggage" to a catalogue product type like `SUITCASE`.

---

## What It Is

A **recipe**, not a resource. The contribution is a six-step construction procedure plus one demonstration of using its output to diagnose a production classifier. The authors say it "can be used in any other e-commerce store with minimal modifications", and position it as applicable to other query-understanding labels too (brand classification is named as future work).

The motivating gap: Q2PT models are usually trained and validated on aggregated [[Click Signals|click-through data]], which the authors call noisy and prone to exposure bias, while human-labelled evaluation sets are small, slow to refresh, and randomly sampled — so they likely under-cover long-tail product types (`snowblower`). sQuIrRel aims for four properties at once: high-precision labels, cheap (re)creation, coverage of every product type, and store-specific knowledge.

## What It Is Not

- **Not a released dataset.** The paper states it uses "internal data". Search logs, the relevance classifier, the product catalogue, and the human comparison set are all Amazon-internal; there is no download, repository, or data statement. The CC BY 4.0 licence covers the paper text only. It does not belong among the downloadable sets in [[E-commerce Search Evaluation Datasets]].
- **Not built from the public ESCI release.** Its relevance model predicts the *ESCI label scheme* (exact / substitute / complement / irrelevant), but it is described only as a multilingual BERT classifier "fine-tuned on human-labeled query-item pairs, sampled from real e-commerce data". The paper never cites the [[Amazon ESCI Dataset|Shopping Queries Dataset]]. The connection is the taxonomy, nothing more.
- **Not a click-based method.** Search logs supply only *which products were shown* for a query; clicks are deliberately not used as labels.
- **Not LLM-based.** The authors reject generating evaluation queries with an LLM: out-of-the-box models lack store knowledge (catalogue, brand availability), and in pilot experiments produced "unnatural queries", lacking the conciseness and abbreviations of real traffic. No numbers are given for that pilot. Labelling is done by a fine-tuned BERT model, not an [[LLM as Judge|LLM judge]].
- **Not a benchmark.** One in-house classifier is evaluated; there are no baselines, splits, or leaderboard.

## How It Works

1. **Obtain query–item pairs** from search logs: each query with all products returned to the customer.
2. **Filter exact matches.** The relevance model labels every pair; keep only *exact*, and only with confidence ≥ 0.8. The model is reported at over 0.9 precision on the exact label.
3. **Get catalogue attributes** — the product type of every kept item.
4. **Aggregate by query.** Collect product types from the query's exact matches; drop those backed by fewer than 3 items. (The text says "less than 3"; Figure 1 says ">3", so the exact boundary is ambiguous.)
5. **Filter noisy labels.** Drop product types holding under 1/3 of the query's exact matches, leaving 0–2; keep only queries with exactly one. Broad-intent queries ("gifts for kids") and multi-product-type queries are excluded by design.
6. **Sample per product type** — at most 50 queries each.

**Where product types come from.** They are not inferred by the method. Each catalogue item already carries a product-type attribute, and step 3 simply reads it. Amazon's are upper-snake-case codes such as `VIDEO_CARD`, `SUITCASE` or `TV_SEASON`, with about 1.5k sampled for the experiments. The inferred part is the *query's* label: the type that dominates among its exact matches. The classifier under test predicts from the same closed set of codes. That set is fixed at any one time but changes with the catalogue ("causing changes in product type label space"), which is why cheap regeneration matters. It also varies by market — "catalogue availability and product type attribution can vary for different locales" — so each locale is built separately. The paper does not say how items get their product type in the first place (seller-supplied, curated, or model-predicted), or whether the types form a hierarchy; it treats them as flat labels.

The method therefore assumes item-level product types are trustworthy, since they become the ground truth. If a catalogue's categories are themselves model-predicted, a mis-categorised item passes its error to every query it matches, and if a similar model drives the query classifier being evaluated, the evaluation partly grades that model against its own kind of guesses. Restricting construction to items with human-curated categories, or comparing results with and without predicted ones, guards against this.

**Evaluation metric:** per-product-type recall at 0.8 [[Precision and Recall|precision]], macro-averaged — chosen because downstream consumers need high-precision query understanding.

## What the Paper Reports

- **Scale:** 2.7M samples across 20 locales and over 1.5k product types (the analysis section says "over 2M" queries, ~130k per locale).
- **Label quality:** 87% accuracy on 400+ manually checked queries from 8 locales. The one systematic error was **complementary product-type confusion** — "around 20%" — e.g. `vacuum cleaner` for the query "vacuum cleaner handle".
- **Versus click labels** (100 queries each from Singapore and the UK, majority clicked product type with P > 0.5): agreement of 64% in the small store and 81% in the large one. Disagreements show clicks tracking behaviour rather than the query — "integrated graphics" clicks land on `NOTEBOOK_COMPUTER` (sQuIrRel: `VIDEO_CARD`); "carry on luggage" buyers settle for a cheaper `BACKPACK` (sQuIrRel: `SUITCASE`), which the authors concede is also technically correct.
- **Versus human labels:** the in-house manual set is about 30× smaller and covers only about 600 of 1k+ product types, most with too few samples. Humans can assign several labels per query; sQuIrRel assigns one. Disagreements fall into synonyms ("biscuits": `cracker` vs `cookie`), disambiguation (Singapore "follow me": a shampoo brand to humans, `book` to sQuIrRel), and multi-type subsets.
- **Classifier diagnosis:** a click-trained BERT Q2PT model scored 0.82 macro recall at 0.8 precision. It was strong on electronics (`INTERNAL_MEMORY`, `KEYBOARDS`) and weak on media (`TV_SEASON`, `MUSIC_TRACK`, `SOFTWARE`), with confusions of media into `BOOK`, synonyms (`TUNIC` → `SHIRT`), complements (`BED` → `BED_FRAME`), and near neighbours (`MODEM` → `NETWORKING_ROUTER`).

## Applying It to Your Own Data

**Prerequisites:** search logs that record the products shown per query; a product-type (or category) attribute on every catalogue item, reliable enough to serve as ground truth (see "Where product types come from" above); and a relevance model that is genuinely high-precision on "exact".

**Left unspecified by the paper:**
- **The relevance model** — the critical component — is described in a sentence: training data, architecture details, and calibration are not given (it is called a "bi-encoder" in one place and a "BERT-based classifier" in another). A model trained on the public ESCI data or an LLM judge are plausible substitutes, but the paper tests neither.
- **What counts as "returned"** — log window, result depth, minimum query frequency.
- **Threshold choice** — no sensitivity analysis for 0.8, 3 items, or 1/3.
- **Sampling arithmetic** — a cap of 50 queries over ~1.5k product types allows at most ~75k queries per locale, which does not reconcile with the stated ~130k average.
- **No code.**

## Using It in Practice

The question a sQuIrRel-style set answers is narrow: **does the query classifier assign the right product type, and for which product types does it fail?** It does not measure search result quality — whether a better label actually improves retrieval needs a separate relevance or ranking evaluation (the "downstream effect" in [[Query Classification]]).

Uses, in order of how directly the paper supports them:

- **Find the product types a classifier handles badly.** This is what the paper does: per-product-type recall at 0.8 precision, best and worst types, and the confusion patterns behind the worst (media → `BOOK`, synonyms, complements).
- **Rebuild after catalogue or taxonomy changes.** Cheap re-creation is one of the paper's stated requirements; when product types are added, split, or reattributed, regenerate the set rather than patching a human one.
- **Monitor over time.** Regenerate on a schedule and re-run the current classifier to catch drift as queries and catalogue shift (see [[Search Observability]]).
- **Compare classifier versions before deploying** — old vs new model, prompt, or ruleset, per product type, with the queries where the new one got worse. The paper never does this (one model, no baselines), so treat it as an extension and mind the caveats below.

**Caveats when comparing versions:**

- **Incumbent bias.** The paper notes Q2PT predictions feed downstream components, retrieval included. If yours does too, the products shown for a query — and so its derived label — were partly chosen by the classifier currently in production. A challenger that disagrees with the incumbent can be scored wrong for disagreeing. Build the set from traffic where the classifier did not steer retrieval, or route old/new disagreements to manual review instead of counting them as errors.
- **Small per-type samples.** At most 50 queries per product type means per-type recall moves in large steps; check a regression is real before acting on it (see [[Statistical Significance in Search Evaluation]]).
- **Shared supervision.** If the new model is trained on labels from the same relevance model that built the evaluation set, its score is inflated. The model evaluated in the paper was trained on click data, independent of the set.
- **Label noise.** About 13% of labels were wrong in the paper's manual check; read the regressing queries before concluding the model got worse.
## Pitfalls

- **The engine's blind spot becomes the evaluation's blind spot.** Labels can only come from products the production engine already returned. Where retrieval never surfaces the right product type, the query gets no label or a wrong one — precisely where a classifier evaluation should be catching problems. The paper does not discuss this.
- **Judge errors become ground truth.** Labels inherit the relevance model's mistakes. The one systematic error found (~20% complementary-type confusion, e.g. `vacuum cleaner` for "vacuum cleaner handle") looks like an exact-versus-complement miss, though the paper does not say where in the pipeline it arises.
- **Ambiguous queries are out of scope.** Excluding broad and multi-intent queries skews the set toward unambiguous traffic, so it cannot measure a classifier on those queries at all. Addressing broad and vague queries is listed as future work.
- **Single label against a multi-label reality.** Where several product types are equally valid (`cracker`/`cookie`, `TUNIC`/`SHIRT`), a classifier predicting the other one can be scored as wrong.
- **Thin evidence.** One model, no baselines, no confidence intervals, a 400-query accuracy check and a 200-query click comparison.
- **Not reproducible as published.** With internal data and an undescribed relevance model, results can't be checked; only the procedure transfers.

## Relation to the Bag-of-Documents Model

The paper does not cite [[Daniel Tunkelang]], but sQuIrRel reads as a narrow, discretised application of his [[Bag-of-Documents Model]] — the query represented as the set of products that satisfy it, not as its text.

- **Same representation.** Tunkelang models a query as a distribution over relevant documents, P(d | q); sQuIrRel represents it as its set of confident exact-match products and reads the label off that set.
- **Same way of estimating the bag.** In [[Distilling Retrieval Pipelines to a Single Embedding Model]], a strong relevance pipeline estimates P(d | q) to produce training signal; sQuIrRel uses a high-precision relevance model to produce evaluation labels. The bag-of-documents framing also admits clicks as an input — exactly the signal sQuIrRel refuses.
- **The filters are a specificity threshold.** Tunkelang measures [[Query Specificity]] as the cohesion of a query's bag — mean cosine similarity between the bag's centroid and its documents. sQuIrRel's 1/3-share and single-type rules measure the same thing categorically: how concentrated the bag is on one product type. The "broad-intent" queries it discards are low-specificity bags.
- **Opposite stance on ambiguity.** The point of keeping a distribution is to preserve ambiguity — "python" holds mass on the language, the snake and Monty Python at once. sQuIrRel collapses each bag to one label and drops the queries where that fails. Seen through the bag-of-documents lens, the obvious extension is to keep the product-type distribution as a soft, multi-label ground truth instead of discarding mixed bags; the paper lists multi-type and broad queries as future work.
- **Different purpose.** Tunkelang uses the bag as a retrieval representation (embeddings, centroids, distillation); sQuIrRel uses it only to manufacture evaluation labels for a classifier.

A practical by-product: the bag sQuIrRel already builds is all a bag-of-documents specificity score needs, so per-query specificity comes almost free alongside the labels.
## Related Concepts

- [[Query Classification]] — the task it evaluates; see the Evaluation section there
- [[Query Understanding]] · [[Search Intent]] — the signal family Q2PT belongs to
- [[Click Signals]] · [[Implicit Judgments]] · [[Presentation Bias]] — the click-label approach it argues against
- [[Judgment Lists]] — the human-labelled alternative it compares with
- [[Amazon ESCI Dataset]] — source of the label scheme its relevance model uses
- [[LLM as Judge]] · [[Synthetic Query Generation]] — approaches it contrasts with
- [[Multilingual Search]] — built per locale across 20 markets
- [[Bag-of-Documents Model]] · [[Query Specificity]] — the query-as-a-set-of-products framing it applies, and the bag cohesion its filters approximate

## Related Topics

- [[Query Classification]]
- [[Query Understanding in Practice]]
- [[E-commerce Search Evaluation Datasets]]
- [[Search Observability]] — continuous monitoring of a production query signal

## Source

- Amazon Science: https://www.amazon.science/publications/squirrel-large-scale-evaluation-of-e-commerce-query-classification-models
- PDF: https://cdn.amazon.science/13/cb/22a64f874be28c7f9eb6601a3fa2/squirrel-large-scale-evaluation-of-e-commerce-query-classification-models.pdf
- DOI: https://doi.org/10.1145/3701716.3715261
- Predecessor preprint by overlapping authors: Tigunova, Ricatte, Eraisha, "Transfer Learning for E-commerce Query Product Type Prediction", https://arxiv.org/abs/2410.07121
