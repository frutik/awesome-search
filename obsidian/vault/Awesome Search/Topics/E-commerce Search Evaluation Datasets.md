---
type: topic
aliases:
  - e-commerce evaluation datasets
  - product search datasets
  - e-commerce relevance datasets
  - product search benchmarks
tags:
  - topic
  - search-evaluation
  - e-commerce
  - benchmark
  - dataset
related_concepts:
  - "[[Judgment Lists]]"
  - "[[Search Evaluation]]"
  - "[[NDCG]]"
  - "[[LLM as Judge]]"
  - "[[Zero-Shot Retrieval]]"
related_topics:
  - "[[E-commerce Search]]"
  - "[[Retrieval Benchmarks and Leaderboards]]"
  - "[[Model Selection and Fine-Tuning Evaluation]]"
  - "[[Search Quality Assurance]]"
created: 2026-10-01
---

# E-commerce Search Evaluation Datasets

Public product-search datasets give teams ready-made judged relevance data before they have built their own [[Judgment Lists|judgment lists]]. Four recur throughout search evaluation and fine-tuning work: [[Amazon ESCI Dataset|Amazon ESCI]], its community extension [[ESCI-S Dataset|ESCI-S]], Wayfair's [[WANDS Dataset|WANDS]], and the [[Home Depot Product Search Relevance|Home Depot]] Kaggle set. They differ less in size than in what their labels mean, and that difference decides which one fits which job.

---

## The Datasets at a Glance

| Dataset | Released by | Domain | Scale | Labels |
|---|---|---|---|---|
| [[Amazon ESCI Dataset]] | Amazon | General e-commerce; English, Japanese, Spanish | Very large | 4-class: Exact / Substitute / Complement / Irrelevant |
| [[ESCI-S Dataset]] | Community (shuttie) | Same as ESCI | ESCI pairs + enriched product metadata | Same ESCI labels, unchanged |
| [[WANDS Dataset]] | Wayfair | Home goods, furniture | ~42K query–product pairs | 3-class: Exact / Partial / Irrelevant |
| [[Home Depot Product Search Relevance]] | Home Depot (Kaggle) | Home improvement | ~74K query–product pairs | Continuous 1–3, average of crowdsourced annotators |

All four are human-labeled query–product pairs, so all four work as ready-made judgment lists for offline [[Search Evaluation|evaluation]], and all four support graded metrics such as [[NDCG]]. Home Depot's averaged scores have to be discretized first.

---

## Label Schemes Are the Real Difference

**ESCI labels shopping intent, not text match.** The Substitute and Complement grades capture the two near-misses that dominate product search: a product that could replace the requested one, and a product that goes with it. That shape has spread beyond the dataset. [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge|Allegro]] modeled the labeling guidelines for its 380K+ judgment set on it, and [[How Etsy Uses LLMs to Improve Search Relevance|Etsy]] plans to split its "partially relevant" grade along the same complement/substitute line. See [[Semantic Relevance]].

**WANDS collapses the near-misses into one Partial grade.** That's simpler to annotate, but you can't tell a substitute from an accessory. Its queries come from real Wayfair traffic, and its judgments are dense: the [[WANDS Dataset|WANDS]] note records 358.9 relevant products per query on average. Dense judgments change how fusion should be tuned. In [[How to Tune Hybrid Search in Qdrant]], [[Reciprocal Rank Fusion|RRF]] did best at high `k` on WANDS, while datasets with about one relevant document per query preferred low `k`.

**Home Depot's scores are averages.** A decimal 1–3 score suits regression-style relevance prediction better than classification. It is the oldest of the four and is used as a smoke test.

---

## Choosing One

- **A general retail catalog, or substitutes and complements matter.** Use [[Amazon ESCI Dataset|ESCI]]. It's the standard e-commerce relevance set, and [[Retrieval Benchmarks and Leaderboards]] argues it tells an e-commerce team more than all of [[MTEB]].
- **Product images or richer product fields.** Use [[ESCI-S Dataset|ESCI-S]]. Its labels are identical to ESCI's, so scores stay comparable. Its image URLs are badly decayed: 131,054 products have no image, and about 46% of the image links that remain are dead. Sampling 40,000 products for [[How to Evaluate Image Search in Qdrant Using Quepid Part 1]] yielded only 21,589 with a working image. Validate every image before indexing.
- **A vertical catalog with attribute-heavy queries** like "mid-century modern sofa gray". Use [[WANDS Dataset|WANDS]]. It also recurs in LLM-labeling experiments: [[Doug Turnbull]] uses it as ground truth in [[Classic ML to Cope with Dumb LLM Judges]] and [[Don't Classify, Hallucinate]], and [[David Albrecht]] generates [[Synthetic Query Generation|synthetic queries]] from its product descriptions in [[LLM-Powered Query Extraction for Autocomplete]].
- **Technical, spec-heavy queries** like "3/4 inch PVC elbow". Use [[Home Depot Product Search Relevance|Home Depot]].

---

## They Don't Substitute for Each Other

The clearest evidence is in [[Fine-Tuning Sparse Embeddings for E-Commerce Search]]. A [[SPLADE]] model fine-tuned on ESCI beat [[BM25]] by 27.5% in-domain (nDCG@10 0.389). Its gains shrank on the other catalogs:

| Evaluated on | Fine-tuned nDCG@10 | vs BM25 |
|---|---|---|
| Amazon ESCI (in-domain) | 0.389 | +27.5% |
| WANDS | 0.355 | +7.9% |
| Home Depot | 0.384 | +10.0% |
| [[MS MARCO]] | 0.751 | −17.9% |

On Home Depot, the off-the-shelf model beat the ESCI-tuned one (0.391 vs 0.384). Training on all three e-commerce sets together, 50K samples each, gave up some in-domain ESCI score (0.372) and gained on WANDS (0.366) and Home Depot (0.410).

Two consequences:

1. **Evaluate on more than one catalog.** A result on ESCI alone says little about another retailer's products. Running the same model on ESCI, WANDS and Home Depot is a cheap check of [[Zero-Shot Retrieval|zero-shot]] transfer across catalogs.
2. **Never evaluate on the data you trained on.** ESCI works as a fine-tuning corpus: Exact and Substitute become positives and Complement is dropped. Once a model has trained on it, ESCI is no longer a neutral benchmark for that model. Split by query, as [[Model Selection and Fine-Tuning Evaluation]] describes.

---

## Limits

- **Label noise.** ESCI was crowdsourced before LLM labeling existed. WANDS judgments in home goods are partly matters of taste: style, color and material are subjective.
- **Frozen relevance.** Commerce relevance drifts. Etsy keeps an evolving labeling guideline because "face masks" meant costume masks before 2020 and protective masks after. A static public dataset can't follow that drift. See [[Do LLM Judges Actually Agree With Us]].
- **Not your catalog.** These datasets help you shortlist, calibrate annotator guidelines, and test methods before investing in custom annotation. As [[Retrieval Benchmarks and Leaderboards]] puts it, the decision still belongs to [[Judgment Lists|judgments]] on your own queries and products. [[Relevance Program Setup]] covers building those.
- **The LLM-judge boundary sits where ESCI is hardest.** Allegro's judge reached F1 around 0.94 on exact matches but only 0.51 and 0.33 on separating "highly substitutable" from "substitutable". The substitute boundary is where [[LLM as Judge|LLM judges]] are least reliable.
- **Relevance labels can manufacture other evaluation sets.** [[sQuIrRel - Large-Scale Evaluation of E-commerce Query Classification Models|sQuIrRel]] reuses the ESCI label scheme to derive query-to-product-type labels from a relevance model's exact matches. It is a method on internal Amazon data, not a dataset to download.

---

## Related Concepts

- [[ESCI Label Scheme]] — Exact / Substitute / Complement / Irrelevant as a scheme in its own right
- [[Judgment Lists]] — what each of these datasets is, structurally
- [[Search Evaluation]] · [[NDCG]] — the metrics they feed
- [[LLM as Judge]] · [[Semantic Relevance]] — ESCI-style labels as the target for LLM labeling
- [[Zero-Shot Retrieval]] — cross-catalog transfer as the test these datasets enable
- [[Hybrid Search]] · [[Reciprocal Rank Fusion]] — commonly tuned against WANDS

## Related Topics

- [[E-commerce Search]] — the domain these datasets model
- [[Retrieval Benchmarks and Leaderboards]] — where these sit among general IR benchmarks
- [[Model Selection and Fine-Tuning Evaluation]] — using them without fooling yourself
- [[Search Quality Assurance]] · [[Relevance Program Setup]] — moving from public data to your own judgments

## Related Articles

- [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] — cross-catalog transfer measured on ESCI, WANDS and Home Depot
- [[How to Tune Hybrid Search in Qdrant]] — fusion tuning on WANDS
- [[Classic ML to Cope with Dumb LLM Judges]] · [[Don't Classify, Hallucinate]] — WANDS as LLM-labeling ground truth
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 1]] — ESCI-S images in practice
- [[Automating Search Relevance Assessment at Scale with LLM-as-a-Judge]] — an ESCI-inspired in-house judgment set
- [[Do LLM Judges Actually Agree With Us]] — where ESCI-shaped labels break LLM judges

## People

- [[Doug Turnbull]] · [[David Albrecht]] · [[Thierry Damiba]] · [[Dylan Couzon]] · [[Andrew Kornilov]]
