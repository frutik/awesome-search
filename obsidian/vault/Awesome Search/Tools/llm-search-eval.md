---
type: tool
title: "llm-search-eval"
aliases: ["llm_search_eval"]
tags:
  - tool
  - search-evaluation
  - relevance-testing
  - llm-judge
  - e-commerce
  - open-source
website: https://sadrmanesh.github.io/llm-search-eval/
repo: https://github.com/sadrmanesh/llm-search-eval
license: MIT
created: 2026-11-14
---

# llm-search-eval

**llm-search-eval** is an open-source Python tool for offline evaluation of product search. It scores one or more ranked runs against a shared label pool, filling gaps in human gold labels with [[LLM as Judge|LLM relevance judgments]], and attaches a paired significance test and bootstrap intervals to every comparison against a baseline. It ships as a CLI, a Python API, a Docker image and a reusable GitHub Action. MIT licensed, written by Naser Sadrmanesh; the first release, v0.1.0, was published on 30 October 2026, and v0.5.0 followed on 4 November 2026.

- Repository: https://github.com/sadrmanesh/llm-search-eval
- Documentation: https://sadrmanesh.github.io/llm-search-eval/
- PyPI: https://pypi.org/project/llm-search-eval/

It sits in the [[Offline Search Evaluation Tools]] landscape as a CLI- and CI-first tool, closest in form factor to [[Rated Ranking Evaluator]], but engine-neutral and built around LLM judging.

---

## How Labels Are Resolved

For every (query, product) pair in each system's top results, a label comes from, in order: a **gold label** from the user's qrels (never re-judged); a **cached judgment** keyed on judge configuration, prompt version and prompt hash, and product content; or a **judge call**. Without a judge, unlabeled results count as not relevant and the report shows the coverage gap. All systems are scored against the same merged pool, so the ideal ranking used by [[NDCG]] and the recall denominator are identical across systems. Grades run 0–3 (irrelevant, partially relevant, relevant, exact match); TREC qrels and run files are accepted alongside JSONL, CSV and TSV.

## Judges, Panels and Agreement

Judges are any OpenAI-compatible chat endpoint (including local servers), a deterministic mock judge for CI, or a user-supplied class. Repeating `--judge` forms a panel — the same idea as an [[LLM Jury]] — combined by majority (default), mean, median, min or max. Reports give the unanimous share, Fleiss' kappa, Krippendorff's alpha and pairwise Cohen's kappa ([[Levels of Judge Agreement]]). With `--calibrate`, gold-labelled pairs are also sent to the judges and agreement and bias against the gold labels are reported per judge and for the panel ([[Judge Calibration]]); gold labels still decide the scores.

## Metrics and Statistics

[[NDCG]]@k (exponential or linear gain), [[Precision and Recall|precision@k and recall@k]], [[MRR]] and [[MAP]], with a configurable relevance threshold and depth. Queries with no relevant product in the pool are excluded from means rather than scored as zero. Each system is compared to the baseline with a two-sided paired randomization (sign-flip) test on per-query values of the primary metric, plus percentile bootstrap intervals for means and paired bootstrap intervals for deltas — the approach recommended in [[Statistical Significance in Search Evaluation]].

## Pairwise Judging

An optional LLM judge compares two systems' top-*k* lists side by side, in both orders, counting only consistent verdicts as wins to cancel [[Position Bias|position bias]]; the report gives win rate with a Wilson interval and an exact sign test. See [[Pairwise Relevance Evaluation]].

## Sampling, Cost and CI

- **Sampling** — reproducible random or stratified [[Query Sampling|query samples]], stratified in proportion across any query field, with the primary metric reported per stratum.
- **Cost** — token usage per model against user-supplied prices, budgets on cost, tokens or judgments, and an `estimate` command that predicts calls, tokens and cost before a run.
- **CI** — a `gate` command and GitHub Action that fail a build on metric floors or drops, optionally only when the drop is significant, and keep a pull-request comment updated.
- **Connectors** — fetch runs from [[Elasticsearch]], [[OpenSearch]], [[Algolia]], Meilisearch, Typesense or any HTTP/JSON search API.

## Persian Handling

Persian and English queries are both handled explicitly: Arabic and Persian code points are unified, Persian and Arabic-Indic digits normalized, the zero-width non-joiner treated as a word boundary, and query language detected from script, with metrics broken down by language. Relevant to [[Multilingual Search]].

## Caveats

- New and single-author: as of November 2026 the repository has one contributor, two GitHub stars and no forks, and no independent adoption is documented.
- The project publishes no performance claims; its sample report and dashboard are built from a small bundled electronics dataset, so their numbers say nothing about any real system.
- Statistical and agreement features are described from the project's documentation, not independently verified.

## Related Concepts

- [[LLM as Judge]] · [[LLM Jury]] · [[Judge Calibration]] · [[Levels of Judge Agreement]]
- [[Statistical Significance in Search Evaluation]] · [[Pairwise Relevance Evaluation]] · [[Query Sampling]] · [[Judgment Lists]]
- [[NDCG]] · [[MRR]] · [[MAP]] · [[Precision and Recall]]

## Related Topics

- [[Offline Search Evaluation Tools]] — the landscape it belongs to
- [[Relevance Evaluation Tools Compared]] — the established workbenches
- [[E-commerce Search]] · [[Multilingual Search]]

## Related Tools

- [[Rated Ranking Evaluator]] — the other CI-first evaluation tool
- [[Quepid]] · [[Releval]] — engine-agnostic workbenches with LLM judging
