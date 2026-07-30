---
created: 2026-07-30
title: "Improving Zero-Shot Ranking with Vespa Hybrid Search - part two"
source: "https://blog.vespa.ai/improving-zero-shot-ranking-with-vespa-part-two/"
author: "[[Jo Kristian Bergum]]"
published: 2023-01-09
type: article
concepts:
  - "[[Zero-Shot Retrieval]]"
  - "[[Hybrid Search]]"
  - "[[ColBERT]]"
  - "[[Late Interaction]]"
  - "[[BM25]]"
  - "[[Score Normalization]]"
  - "[[Linear Score Combination]]"
  - "[[Reranking]]"
  - "[[PROMPTAGATOR]]"
topics:
  - "[[Late Interaction in Vespa]]"
  - "[[Search Quality Assurance]]"
tags: [article, zero-shot, hybrid-search, colbert, late-interaction, bm25, score-normalization, beir, vespa, company-blog]
---

# Improving Zero-Shot Ranking with Vespa Hybrid Search - part two

**Author:** [[Jo Kristian Bergum]] (Chief Scientist, [[Vespa]]) · Part two of two

## Summary

Where [[Improving Zero-Shot Ranking with Vespa Hybrid Search|part one]] argued that
in-domain wins don't transfer, part two builds a ranking model that survives the transfer:
a tuned [[BM25]] baseline, a **22M-parameter distilled [[ColBERT]]** reranker, and
[[Score Normalization|min-max normalized]] linear fusion of the two. On [[BEIR]] it reaches
**0.481 average nDCG@10** against 0.453 for BM25 alone and 0.363 for ColBERT alone — winning
**12 of 13 datasets** — with no fine-tuning on any of them and end-to-end latency under 60 ms
on CPU.

The through-line is about baselines as much as about hybrid ranking: the article's own BM25
implementation beats the BM25 numbers published with BEIR, which means part of the neural
literature's reported gains are measured against a weaker lexical baseline than necessary.

---

## Step One: A BM25 Baseline Worth Beating

BM25 hyperparameters set to **k1=0.9, b=0.4**, with the scoring function applied *independently*
to the title and text fields and the two combined linearly. That configuration outperforms the
BM25 results published alongside BEIR:

| Dataset | Original BM25 | Vespa BM25 |
|---|---|---|
| TREC-COVID | 0.656 | 0.690 |
| HotpotQA | 0.603 | 0.623 |
| ArguAna | 0.315 | 0.393 |
| **Average** | **0.440** | **0.453** |

The ArguAna gap is the largest — a reminder that "BM25" in a results table names a family of
implementations with different field handling and parameters, not one number. See
[[BM25]] and [[Linear Score Combination]].

## Step Two: A Distilled ColBERT Reranker

The [[ColBERT]] model deployed is a distilled MiniLM variant, aggressively shrunk relative to the
original:

| Property | Original ColBERT | This model |
|---|---|---|
| Parameters | 110M | **22M** |
| Dimensions per wordpiece | 128 | **32** |
| Vector storage | float | **bfloat16** |
| Max query length | — | 32 wordpieces |
| Max document length | — | 180 wordpieces |

It runs as a **re-ranking phase over the top 2,000 BM25 results**, scoring with MaxSim across
query and document token embeddings. See [[Late Interaction in Vespa]] for how MaxSim is expressed
as a tensor ranking expression, and [[Knowledge Distillation]] for the compression that produced
this model.

## Step Three: Normalized Hybrid Fusion

The hybrid method is not a rank-based merge. Both the BM25 and ColBERT scores are **min-max scaled
to the 0–1 range** and then linearly weighted — which is only well-defined if the extremes are
computed over the *whole* result set, and Vespa distributes the query across content nodes.

The mechanism, implemented as a custom searcher in the query dispatcher:

1. Collect **match-features** from the content nodes
2. Compute the global maximum and minimum scores across nodes
3. Scale all scores uniformly against those globals
4. Apply linear weighting to combine the normalized values

This is the distributed answer to the problem [[Score Normalization]] describes: per-node min-max
would normalize the same document differently depending on which shard it landed on, so the
normalization has to happen after the merge, at the dispatcher, using features carried up from the
nodes.

## BEIR Results (nDCG@10)

| Dataset | BM25 | ColBERT | Hybrid |
|---|---|---|---|
| TREC-COVID | 0.690 | 0.658 | **0.750** |
| NFCorpus | 0.313 | 0.304 | **0.350** |
| Natural Questions | 0.327 | 0.403 | **0.404** |
| HotpotQA | 0.623 | 0.298 | **0.632** |
| FiQA-2018 | 0.244 | 0.252 | **0.292** |
| ArguAna | 0.393 | 0.286 | **0.404** |
| Touché-2020 | 0.413 | 0.315 | **0.415** |
| Quora | 0.761 | 0.817 | **0.826** |
| DBPedia | 0.327 | 0.281 | **0.365** |
| SCIDOCS | 0.160 | 0.107 | **0.161** |
| FEVER | 0.751 | 0.534 | **0.779** |
| CLIMATE-FEVER | **0.207** | 0.067 | 0.191 |
| SciFact | 0.673 | 0.403 | **0.679** |
| **Average** | 0.453 | 0.363 | **0.481** |

Two things worth reading off this table beyond the average:

**ColBERT alone loses to BM25** — 0.363 against 0.453. The hybrid wins not because the neural
model is better but because the two are wrong on different documents. On HotpotQA and FEVER
ColBERT is catastrophically behind (0.298 vs 0.623, 0.534 vs 0.751) and the hybrid still edges
past BM25.

**The one loss is a length problem.** CLIMATE-FEVER is the single dataset where the hybrid falls
below BM25 (0.191 vs 0.207), and its queries average **20.2 words** — pressing against the model's
32-wordpiece query limit. ColBERT scores 0.067 there, so the fusion is dragged down by a component
that is effectively noise.

## Distillation Costs More Out-of-Domain

The distilled model underperformed full-sized ColBERT variants in the zero-shot setting, and the
article's stated observation is that **model compression and distillation show a greater impact
zero-shot than in-domain**. In-domain evaluation understates what you lose by shrinking a model —
the same asymmetry [[Zero-Shot Retrieval]] describes for architecture choice, now applied to
compression. See [[ColBERT]] and [[Knowledge Distillation]].

## Comparison with Few-Shot PROMPTAGATOR

The article positions its zero-shot result against [[PROMPTAGATOR]], which uses a large language
model to generate synthetic in-domain training data and so is *not* zero-shot. Reported averages
over the subset of BEIR datasets PROMPTAGATOR covers:

| Model | Average nDCG@10 |
|---|---|
| Vespa Hybrid (zero-shot) | 0.456 |
| PROMPTAGATOR (dense retriever) | 0.478 |
| PROMPTAGATOR (cross-encoder) | **0.528** |

Per-dataset figures available from the article's table:

| Dataset | Vespa Hybrid | PROMPTAGATOR (dense) | PROMPTAGATOR (cross-encoder) |
|---|---|---|---|
| TREC-COVID | 0.750 | 0.756 | 0.762 |
| FiQA-2018 | 0.292 | 0.462 | 0.494 |
| ArguAna | 0.404 | 0.594 | 0.630 |
| HotpotQA | 0.632 | 0.614 | 0.736 |

> The reported averages do not reconcile with these four rows alone, so the comparison covers
> more datasets than are captured here. The averages above are as the article states them.

PROMPTAGATOR's cross-encoder wins on quality, but it re-ranks the top 200 and depends on
billion-parameter LLM inference for data generation. The article's claim for the hybrid model is
**efficiency**, not superiority: comparable-order quality at a fraction of the compute, and no
per-domain training step at all.

The obvious next question — what happens if you *do* generate synthetic in-domain data, cheaply —
is what [[Improving Search Ranking with Few-Shot Prompting of LLMs]] answers a month later.

## Why It Is Cheap

- **CPU-only inference** — no GPU or TPU in the serving path
- **End-to-end pipeline latency under 60 ms**
- Reranking confined to a shortlist via Vespa's phased ranking, so the expensive model only sees
  2,000 documents
- Distributed scoring via match-features, so normalization scales with the cluster

See [[Retrieval Pipeline]] and [[Late Interaction in Vespa]].

## Deployment

The full CORD-19 dataset is indexed and searchable at
[cord19.vespa.ai](https://cord19.vespa.ai/) with selectable ranking strategies, so the BM25,
ColBERT, and hybrid profiles can be compared interactively. The application is open source,
deployed on Vespa Cloud, and can be run locally from a container image; reproduction instructions
live in the GitHub repository. See [[Vespa - Ranking Without Labels on CORD-19]].

## On Weak Baselines

The article closes on methodology: reporting against weak baselines inflates the apparent progress
of neural methods. Its own BM25 numbers beating the published BEIR BM25 numbers is offered as
evidence that this happens in practice. The constructive version of the claim is that a pragmatic
combination of well-understood techniques can match or exceed more complex single-model approaches
zero-shot, without domain-specific fine-tuning.

## Related Concepts

- [[Hybrid Search]] — the technique, here with normalized score fusion rather than RRF
- [[Score Normalization]] — the distributed min-max mechanism is this article's main contribution to it
- [[Linear Score Combination]] — how the normalized scores are weighted
- [[ColBERT]] · [[Late Interaction]] — the reranking model
- [[BM25]] — the baseline, tuned rather than defaulted
- [[Knowledge Distillation]] — how a 110M model became 22M, and what that costs zero-shot
- [[Reranking]] · [[Retrieval Pipeline]] — the phased architecture
- [[Zero-Shot Retrieval]] — the setting
- [[PROMPTAGATOR]] — the few-shot alternative compared against
- [[Reciprocal Rank Fusion]] — the rank-based fusion this article does *not* use

## Related Articles

- [[Improving Zero-Shot Ranking with Vespa Hybrid Search]] — part one, the problem statement
- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — the sequel that adds synthetic training data
- [[Announcing the Vespa ColBERT Embedder]] — the later native embedder and 32× binary quantization
- [[Hybrid Fusion Failure - BM25 Displacing Reference Documents]] — what un-normalized fusion looks like when it breaks

## Datasets

- [[BEIR]] — the evaluation suite
- [[TREC-COVID]] — the dataset behind the cord19.vespa.ai deployment

## People

- [[Jo Kristian Bergum]] — author

## External References

- Part one — https://blog.vespa.ai/improving-zero-shot-ranking-with-vespa/
- CORD-19 search demo — https://cord19.vespa.ai/
- Application source — https://github.com/vespa-cloud/cord-19-search
- BEIR — https://github.com/beir-cellar/beir
- PROMPTAGATOR paper — https://arxiv.org/abs/2209.11755
- InPars paper — https://arxiv.org/abs/2202.05144
- Vespa Cloud — https://cloud.vespa.ai/ · Vespa docs — https://docs.vespa.ai/
