---
title: Offline Search Evaluation Tools
type: topic
aliases:
  - offline evaluation tools
  - search evaluation tooling landscape
  - IR evaluation tools
  - relevance evaluation stack
tags:
  - topic
  - search-evaluation
  - relevance-testing
  - tooling
  - landscape
related_concepts:
  - "[[Search Evaluation]]"
  - "[[Judgment Lists]]"
  - "[[Query Sampling]]"
  - "[[LLM as Judge]]"
  - "[[Judge Calibration]]"
  - "[[Levels of Judge Agreement]]"
  - "[[Statistical Significance in Search Evaluation]]"
  - "[[Pairwise Relevance Evaluation]]"
  - "[[NDCG]]"
related_topics:
  - "[[Relevance Evaluation Tools Compared]]"
  - "[[Retrieval Benchmarks and Leaderboards]]"
  - "[[Relevance Program Setup]]"
  - "[[Search Quality Assurance]]"
  - "[[Model Selection and Fine-Tuning Evaluation]]"
  - "[[A-B Testing for Search]]"
created: 2026-11-14
---

# Offline Search Evaluation Tools

Offline evaluation is a pipeline, not a single activity: pick queries, collect judgments, run each system configuration, compute metrics, decide whether the difference is real. No one tool owns that whole pipeline. The landscape splits into **layers**, each with its own lineage — research metric libraries from the TREC world, experiment frameworks from academic IR groups, relevance workbenches from search consultancies and engine vendors, judgment generators from the [[LLM as Judge]] research line, and LLM-application evaluators from the RAG ecosystem.

This note maps those layers, what each one is actually good for, and where the gaps sit. For a head-to-head of the five practitioner workbenches ([[Quepid]], [[Search Relevance Workbench]], [[Elasticsearch Relevance Studio]], [[Rated Ranking Evaluator]], [[Releval]]), see [[Relevance Evaluation Tools Compared]]. For public benchmark suites, see [[Retrieval Benchmarks and Leaderboards]]. Online methods — [[A-B Testing for Search]], [[Interleaving]] — are the other half of the picture and out of scope here.

---

## The Pipeline and Its Layers

| Pipeline step | Layer | Representative tools |
|---|---|---|
| Choose queries | Query sampling | Rarely tooled; see [[Query Sampling]] |
| Produce judgments | Judgment generation | UMBRELA, autoqrels; LLM judges inside workbenches |
| Run systems, store results | Experiment frameworks · engine-native APIs | PyTerrier, `ir_datasets`, `beir`, `mteb`; Elasticsearch Ranking Evaluation API, [[Search Relevance Workbench]] |
| Compute metrics | Metric engines | `trec_eval`, `pytrec_eval`, `ir_measures`, `ranx` |
| Decide | Statistics · reporting · gating | `ranx`, PyTerrier; [[Rated Ranking Evaluator]] in CI |
| All of the above, for a team | Relevance workbenches | [[Quepid]], [[Rated Ranking Evaluator]], [[Search Relevance Workbench]], [[Elasticsearch Relevance Studio]], [[Releval]] |
| Evaluate an LLM app around retrieval | LLM-application evaluators | [[RAGAS]], [[Langfuse]], DeepEval, [[Jevals]] |

The lingua franca connecting the research layers is the TREC format: a **qrels** file (query, document, grade) and a **run** file (query, document, rank, score). Tools that speak it interoperate for free; tools that don't become islands.

---

## Layer 1 — Metric Engines

The layer everything else ultimately rests on, and the one where correctness matters most: two tools computing "nDCG@10" can disagree (see [[NDCG Variants]]).

- **`trec_eval`** — https://github.com/usnistgov/trec_eval — NIST's C program, described by its README as "the standard tool used by the TREC community for evaluating an ad hoc retrieval run, given the results file and a standard set of judged results." The reference implementation; when numbers disagree, this is the arbiter.
- **`pytrec_eval`** — https://github.com/cvangysel/pytrec_eval — MIT-licensed Python bindings over `trec_eval`. As of November 2026 its repository has seen no pushes since October 2023.
- **`ir_measures`** — https://ir-measur.es/ — Apache-2.0, from the Terrier Team at Glasgow: "a common interface to many IR measure tools." One measure syntax (`nDCG@15`, `P(rel=2)@5`, `Judged@10`) dispatched to interchangeable providers — `pytrec_eval`, `ranx`, `cwl_eval`, `gdeval`, `trectools`, `pyndeval`, `msmarco`, `judged` and others. Its `Judged@k` measure reports how much of the top *k* carries a judgment, which is the first number to check before trusting any other.
- **`ranx`** — https://github.com/AmenRa/ranx — MIT, Numba-accelerated. Its metrics (Hits, Hit Rate, Precision, Recall, F1, r-Precision, Bpref, RBP, [[MRR]], [[MAP]], DCG, [[NDCG]]) are "tested against TREC Eval for correctness". Beyond metrics it ships **statistical tests** — paired Student's t-test (default), Fisher's randomization test, Tukey's HSD — plus fusion algorithms with normalization strategies and automatic fusion optimization (see [[Reciprocal Rank Fusion]]).

**Pattern:** metric computation is a solved problem with a reference implementation. The live question in this layer is not "which library" but "which metric definition", and `ir_measures` exists precisely to make that explicit.

## Layer 2 — Experiment Frameworks and Dataset Access

These wrap the metric engines in a way to *run* systems and compare them.

- **PyTerrier** — https://github.com/terrier-org/pyterrier — MPL-2.0. Declarative pipelines for sparse, learned-sparse and dense retrieval plus reranking, and `pt.Experiment` to compare them. `pt.Experiment` takes a `baseline` (counting queries improved and degraded and computing significance against it), a `test` parameter (paired t-test by default), and a `correction` parameter for multiple-testing correction (`bonferroni`, `holm`, `hs`). Described in *Declarative Experimentation in Information Retrieval using PyTerrier* (Craig Macdonald and Nicola Tonellotto, ICTIR 2020); its README makes citing that paper a condition of use.
- **`ir_datasets`** — https://github.com/allenai/ir_datasets — Apache-2.0, "a common interface to many IR ranking datasets"; PyTerrier loads standard collections through it.
- **`beir`** and **`mteb`** — the runners behind [[BEIR]] and [[MTEB]]; they evaluate *models* on *public* suites. Covered in [[Retrieval Benchmarks and Leaderboards]].

**Pattern:** this layer is built for researchers comparing retrieval methods on shared collections. It is the most statistically rigorous part of the landscape, and the hardest fit for a product search team, because it assumes the retriever is Python code in the experiment, not a configured engine behind an HTTP endpoint.

## Layer 3 — Engine-Native Evaluation

The engines themselves now evaluate.

- **Elasticsearch Ranking Evaluation API** (`_rank_eval`) — https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-rank-eval — generally available, added in 6.2.0. A request carries a set of rated requests (each a query, or a search template with params, plus `_index`/`_id`/`rating` triples) and one metric: Precision@k, Recall@k, mean reciprocal rank, DCG (optionally normalized), or [[ERR|Expected Reciprocal Rank]]. A bare primitive — one metric per request, no UI, no judgment management.
- **[[Search Relevance Workbench]]** — [[OpenSearch]]'s in-engine workbench (OpenSearch 3.1+), with judgments stored in an index, LLM and [[User Behavior Insights|UBI]]-derived judgments, and hybrid-search parameter grid search. Repository: https://github.com/opensearch-project/search-relevance.
- **[[Elasticsearch Relevance Studio]]** — Elastic's experimental, agent-driven lifecycle app over [[Elasticsearch]].

**Pattern:** engine-native tools win on zero extra infrastructure and lose on portability — the judgments live in one vendor's index.

## Layer 4 — Relevance Workbenches

The practitioner layer: tools a search team actually opens on a Tuesday. [[Quepid]] (engine-agnostic web app, [[OpenSource Connections]]), [[Rated Ranking Evaluator]] (a JVM build library from [[Sease]], designed for CI), [[Releval]] (proprietary, self-hosted, native clickstream capture), plus the two engine-native workbenches above. [[Relevance Evaluation Tools Compared]] compares them dimension by dimension; the summary relevant to the landscape:

- They own **judgment management and collaboration** — the part research libraries ignore entirely.
- They expose **fixed metric sets** (Quepid alone allows arbitrary JavaScript scorers).
- **Statistical significance is not among the capabilities that comparison records for any of the five.** Metric deltas are shown; whether a delta is noise is left to the user.

Quepid is also where judge validation is starting to reach a workbench. It has generated judgments with an LLM since v8, and a proposed **judge calibration tool** ([PR #1827](https://github.com/o19s/quepid/pull/1827)) has an AI judge re-rate a random sample of pairs a reference has already rated, reporting agreement at pair level (ordinal Krippendorff's α, a confusion table) and at rank level (Kendall's τ over per-query nDCG@10), re-running prompt changes on the same frozen pairs. The case for it is made in [[Calibrate Before You Trust]]. For automation, the community wrapper quepid-api-unofficial (https://github.com/frutik/quepid-api-unofficial) adds the one-at-a-time query and case creation Quepid's official API has no endpoint for — see [[Quepid]].

## Layer 5 — Judgment Generation

Judgments are the expensive input, and a separate tool category has grown to produce or extend them.

- **UMBRELA** — https://github.com/castorini/umbrela — Apache-2.0, from the castorini group: "an open-source reproduction of the Bing RELevance Assessor". Assigns graded 0–3 judgments with cloud or open-weight LLMs, can compare judge backends, and includes an `EnsembleJudge` that majority-votes across several judges. Its grading scheme is the "UMBRELA-style" pointwise baseline benchmarked in [[Benchmarking LLM-based Relevance Judgment Methods]], where it tracked human system rankings closely on [[TREC Deep Learning Track|TREC Deep Learning]] (Kendall τ 0.920 / 0.894 / 0.890 on DL-19/20/21).
- **autoqrels** — https://github.com/seanmacavaney/autoqrels — Apache-2.0. Infers qrels for unjudged documents in a run from the judged ones, implementing one-shot labeling (1SL) from MacAvaney and Soldaini, *One-Shot Labeling for Automatic Relevance Estimation* (SIGIR 2023). Speaks the `ir_measures` API, so its inferred-label measures plug straight into PyTerrier.
- **Inside the workbenches** — Quepid (v8+), SRW, ESRS and Releval all ship an LLM judging path.

**Pattern:** the hard part is no longer *producing* LLM judgments but *trusting* them. Agreement and calibration — see [[Levels of Judge Agreement]], [[Judge Calibration]], [[Adversarial Relevance Judgment]] — are research topics with good literature and thin tooling. Ensembling (UMBRELA) is the most common built-in safeguard; measuring a judge against a human gold slice is mostly left to the user.

## Layer 6 — LLM-Application Evaluators

A neighbouring ecosystem, built for RAG and agents rather than ranked lists, that increasingly overlaps with search evaluation.

- **[[RAGAS]]** — Apache-2.0, LLM-based and traditional metrics separating retrieval quality from generation quality, plus synthetic test-set generation. Its repository now lives at https://github.com/vibrantlabsai/ragas.
- **[[Langfuse]]** — trace-and-score observability: scores from human review or automated judges attached to production traces.
- **DeepEval** — https://github.com/confident-ai/deepeval — Apache-2.0, describing itself as "The LLM Evaluation Framework".
- **[[Jevals]]** — gating by a calibrated decision model ([[Jev]]) rather than a generative judge; a self-described research preview.

**Pattern:** these tools measure *answers*; ranked-list metrics are an afterthought. For a search team they are the right tool for the generation stage of [[RAG]] and the wrong one for ranking regressions.

---

## Cross-Cutting Comparison

| Concern | Where it is handled well | Where it is weak |
|---|---|---|
| Metric correctness | `trec_eval`; `ranx` (tested against it); `ir_measures` makes definitions explicit | Workbenches with fixed, lightly documented metric variants |
| Unjudged documents | `ir_measures` `Judged@k`; autoqrels infers labels; SRW and ESRS report unrated documents | Anywhere unjudged = irrelevant is assumed silently |
| Significance testing | `ranx` (t-test, randomization, Tukey HSD); PyTerrier (`baseline`, `test`, `correction`) | Not recorded for any practitioner workbench |
| Judge validation | UMBRELA ensembles; research methodology in [[Judge Calibration]] | Most workbench LLM-judge features |
| CI / regression gating | [[Rated Ranking Evaluator]] (Maven build) | Interactive workbenches; research frameworks |
| Query sampling | — | Almost everywhere; see below |
| Engine portability | Quepid, Releval, RRE (Solr + ES), any TREC-format pipeline | SRW, ESRS, `_rank_eval` |

---

## Where the Landscape Is Thin

1. **Statistics live on the wrong side of the divide.** The tools that compute significance well (`ranx`, PyTerrier) are research libraries that expect qrels and runs as files; the workbenches product teams use show metric deltas, and the comparison records no significance test in any of them. Bridging the two means getting per-query scores out of the workbench and into a statistics library — an extra manual step outside the tool the team actually works in. See [[Statistical Significance in Search Evaluation]].
2. **LLM judging shipped faster than judge validation.** Four of the five workbenches in [[Relevance Evaluation Tools Compared]] added an LLM judge; that comparison records none of them reporting judge–human agreement as a first-class number. The literature is clear that agreement with human labels and agreement with human *system rankings* are different properties ([[Benchmarking LLM-based Relevance Judgment Methods]]); a tool that reports a single "judge accuracy" figure does not say which one it measured. The proposed judge calibration tool for [[Quepid]] would report the two separately — pair-level Krippendorff's α and rank-level Kendall's τ — but it is still a proposal.
3. **Query sampling is untooled.** Every guide starts with "sample your queries" — random, stratified by head/torso/tail, or probability-proportional-to-size ([[Query Sampling]], [[Query Sampling for Relevancy Testing]], [[Succeeding with Relevance Evaluation using PPS Sampling]]) — and none of the established tools in the layers above takes a query log as input and produces a stratified sample. It is left to ad hoc scripts, which makes the periodic refresh those guides recommend easy to skip.
4. **Pairwise judging has not reached the workbenches.** [[Pairwise Relevance Evaluation]] is well studied and aligned best with human labels in the Arabzadeh–Clarke benchmark, but none of the five workbenches in [[Relevance Evaluation Tools Compared]] lists a "which of these two result lists is better" judging mode.
5. **Cost is not a first-class input.** LLM judging turns evaluation into a metered expense, and estimating or capping that expense before a run is not among the capabilities recorded for the workbenches.

One recent entrant addresses several of these gaps: [[llm-search-eval]], an MIT-licensed Python CLI whose first release, v0.1.0, was published on 30 October 2026. Its documentation describes LLM judging limited to the pairs that have no gold label, judge panels with inter-judge agreement, a paired randomization test and bootstrap intervals for system deltas, pairwise list judging, stratified query sampling, cost budgets and a CI gate. As of November 2026 it has a single contributor, two GitHub stars and no forks, and no independent adoption is documented.

---

## Assembling a Stack

- **Research or model-selection work, Python retrievers** → PyTerrier + `ir_datasets` + `ir_measures`; `ranx` when fusion or extra statistical tests are needed. See [[Model Selection and Fine-Tuning Evaluation]].
- **Product search team, human raters, any engine** → [[Quepid]] for judgments and inspection; take per-query scores out and test significance separately (see [[Statistical Significance in Search Evaluation]]).
- **Relevance regressions blocking deploys on a JVM / Solr / Elasticsearch stack** → [[Rated Ranking Evaluator]] in the build.
- **All-in on one engine, minimal infrastructure** → [[Search Relevance Workbench]] on OpenSearch; the `_rank_eval` API or [[Elasticsearch Relevance Studio]] on Elasticsearch.
- **Scaling judgments with LLMs** → UMBRELA-style graded judging, validated against a human gold slice per [[Judge Calibration]] before the labels are trusted; autoqrels to fill holes in existing qrels.
- **RAG on top of search** → keep a ranking stack for retrieval, add [[RAGAS]] or [[Langfuse]] for the generation stage.

Whatever the stack, the order of trust is: sample honestly → check `Judged@k` → compute metrics with a known definition → test the delta → only then celebrate.

---

## Related Concepts

- [[Search Evaluation]] · [[Judgment Lists]] · [[Query Sampling]] · [[Implicit Judgments]]
- [[LLM as Judge]] · [[Judge Calibration]] · [[Levels of Judge Agreement]] · [[Adversarial Relevance Judgment]] · [[Pairwise Relevance Evaluation]]
- [[Statistical Significance in Search Evaluation]]
- [[NDCG]] · [[MRR]] · [[MAP]] · [[ERR]] · [[Precision and Recall]] · [[Reciprocal Rank Fusion]]

## Related Topics

- [[Relevance Evaluation Tools Compared]] — the five workbenches head to head
- [[Retrieval Benchmarks and Leaderboards]] — public suites and their runners
- [[NDCG Variants]] — why metric definitions diverge between tools
- [[Relevance Program Setup]] · [[Search Quality Assurance]] — the practice these tools serve
- [[Model Selection and Fine-Tuning Evaluation]] — methodology for comparing models
- [[A-B Testing for Search]] · [[Duality in Measuring Search]] — the online side

## Related Articles

- [[Benchmarking LLM-based Relevance Judgment Methods]]
- [[Do LLM Judges Actually Agree With Us]]
- [[Calibrate Before You Trust]] — the case for a judge calibration tool in Quepid
- [[Query Sampling for Relevancy Testing]]
- [[Succeeding with Relevance Evaluation using PPS Sampling]]

## Related Tools

- [[Quepid]] · [[Rated Ranking Evaluator]] · [[Search Relevance Workbench]] · [[Elasticsearch Relevance Studio]] · [[Releval]]
- [[llm-search-eval]] — a recent CLI/CI entrant built around LLM judge panels and paired statistics
- [[RAGAS]] · [[Langfuse]] · [[Jevals]] · [[User Behavior Insights]] · [[Sentence Transformers]]

## People

- [[Doug Turnbull]] — Quepid co-creator
- [[Daniel Wrigley]] — introduced Search Relevance Workbench
- [[Negar Arabzadeh]] · [[Charles L. A. Clarke]] — benchmarked LLM relevance-judgment methods
- [[Nick Zadrozny]] — stratified query sampling for relevance testing
