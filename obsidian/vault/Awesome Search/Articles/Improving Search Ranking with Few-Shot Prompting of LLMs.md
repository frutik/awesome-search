---
created: 2026-07-30
title: "Improving Search Ranking with Few-Shot Prompting of LLMs"
aliases:
  - "Improving Text Ranking with Few-Shot Prompting"
source: "https://blog.vespa.ai/improving-text-ranking-with-few-shot-prompting/"
author: "[[Jo Kristian Bergum]]"
published: 2023-02-03
type: article
concepts:
  - "[[Synthetic Query Generation]]"
  - "[[Consistency Filtering]]"
  - "[[FLAN-T5]]"
  - "[[Cross-Encoder]]"
  - "[[Knowledge Distillation]]"
  - "[[Hard Negative Mining]]"
  - "[[Zero-Shot Retrieval]]"
  - "[[PROMPTAGATOR]]"
topics:
  - "[[Search Quality Assurance]]"
  - "[[Reasoning Reranking]]"
tags: [article, synthetic-data, few-shot, llm, flan-t5, cross-encoder, knowledge-distillation, zero-shot, trec-covid, vespa, company-blog]
---

# Improving Search Ranking with Few-Shot Prompting of LLMs

**Author:** [[Jo Kristian Bergum]] (Chief Scientist, [[Vespa]])

## Summary

The end of the zero-shot series: instead of accepting whatever an off-the-shelf model gives you,
use a **3B-parameter open LLM to invent the training data you don't have**. An instruction prompt
with three labeled examples generates synthetic queries for [[TREC-COVID]] documents, a
consistency filter throws away the bad ones, and a **22M-parameter [[Cross-Encoder|cross-encoder]]**
trained on the survivors reaches **80.2 nDCG@10** — 4 points above the zero-shot hybrid baseline
from [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two|part two]] and 10 above
BM25.

Bergum's framing of the significance:

> The ability to create high-quality synthetic training data might be a turning point with the
> potential to revolutionize information retrieval.

The total human labeling cost was **three queries**.

---

## Why Not Just Use Clicks

Transformer-based ranking models are credited with advancing search results by over 30% on
[[MS MARCO]], but they need labeled data at a scale most domains don't have. The usual substitute
— pseudo-labels derived from clicks — carries known biases: **[[Presentation Bias|presentation
bias]]** (users click what was shown) and survivorship bias (you only observe the queries that
already worked). For a domain with no interaction data at all, neither path exists. Generative
LLMs are proposed as the third option.

See [[Implicit Judgments]] and [[Click Signals]] for the pseudo-label machinery this sidesteps.

## The Generator: FLAN-T5

The article discusses GPT-3 and Google's [[FLAN-T5]] as foundation models, noting that Google
open-sourced FLAN-T5 variants up to **11B parameters under Apache 2.0** — which is what makes the
method reproducible rather than an API dependency.

On what "foundation model" earns:

> Massive self-supervised training on piles of text, coupled with later fine-tuning on a broad,
> diverse set of tasks, is one of the reasons they are called foundation models.

Rather than fine-tuning, the weights stay frozen and the model is steered by **prompt
engineering** — natural-language instructions mixed with data in the prompt.

The generator used in the experiments is **flan-t5-xl (3B)**.

## The Pipeline

```
documents → instruction prompt (3 examples) → synthetic queries
          → consistency filter (source doc must rank #1)
          → + 2 sampled negatives → training triplets
          → 22M cross-encoder (2 epochs) → ONNX → Vespa rerank phase
```

Generation happens **offline**, which is the property that makes billion-parameter models
affordable here: no LLM sits in the query path. The overall effect is
[[Knowledge Distillation|distilling]] a 3B generative model into a 22M ranking model.

### Prompting

The instruction prompt told the model that **"The query must be specific and detailed"** and
supplied three human-annotated examples before asking for a synthetic query for each document.
That single sentence is reported as decisive — earlier iterations without it produced overly
generic queries. It is a concrete instance of prompt wording moving output quality, and it maps
onto [[Query Specificity]] as the property being requested.

The three few-shot examples were drawn from the TREC-COVID test queries.

**Coverage:** synthetic queries were generated for **33,099 of 171K documents** — roughly 19% of
the corpus. Generation ran on a single **A100 40GB at about $1/hour, producing ~3,600 queries per
hour**.

### Consistency Filtering

A generated query is only useful if it actually retrieves its source document. The zero-shot
hybrid ranking model from part two was used as the filter: keep the pair only when the source
document ranks **#1** for its generated query.

**33,099 pairs → 14,156 (43% retained).** The article reads the retention rate as evidence of
reasonable generation quality. See [[Consistency Filtering]].

### Negatives

Two negative examples were sampled per query from the top-100 ranked documents, forming training
triplets. Sampling from the retrieved top-100 rather than at random is what makes them hard
negatives — see [[Hard Negative Mining]].

## The Ranking Model

A **22M-parameter cross-encoder based on 6-layer MiniLM**, trained for **two epochs** on the
synthetic triplets, exported to [[ONNX]] and deployed in [[Vespa]] as a re-ranking phase over the
**top 30** results from the hybrid model.

## Results on TREC-COVID (nDCG@10)

| Model | nDCG@10 |
|---|---|
| **Cross-encoder trained on synthetic data** | **80.2** |
| Zero-shot hybrid (part two) | 76.0 |
| [[PROMPTAGATOR]] (137B FLAN) | 76.2 |
| Unsupervised [[BM25]] | 70.0 |
| OpenAI GPT embeddings | 64.9 |

**+4 points over the zero-shot hybrid, +10 over BM25** — and ahead of PROMPTAGATOR despite
PROMPTAGATOR using a 137B generator against this pipeline's 3B.

> Note on the baselines: part two's BEIR table reports TREC-COVID as 0.690 for BM25 and 0.750 for
> the hybrid, while this article quotes 70.0 and 76.0. The figures differ slightly between the two
> posts; each is recorded here as its own article states it.

The OpenAI embedding number is the weakest in the table, which is consistent with part one's
argument about single-vector models out-of-domain rather than a claim about that specific model.

## Deployment Choices

**Cross-encoder over [[Bi-Encoder|bi-encoder]]**, for two stated reasons: better effectiveness, and
simpler model versioning — swapping a cross-encoder requires no re-processing of the document
corpus, whereas a new bi-encoder means re-embedding everything. That operational argument is often
the deciding one and is easy to miss when comparing the architectures on quality alone.

Cross-encoder cost was managed by shrinking what the model has to read:

- **Query-contextual Vespa dynamic summaries** instead of full abstracts — the passage handed to
  the model is already narrowed to the query-relevant part
- **Re-ranking depth capped at 30** documents
- Shorter sequences as a direct consequence of the query-aware summarization

Deployed to the [cord19.vespa.ai](https://cord19.vespa.ai/) demo. See
[[Vespa - Ranking Without Labels on CORD-19]].

## What Was Released

Three Jupyter notebooks covering the pipeline end to end:

1. FLAN-T5 query generation with instruction prompting
2. Consistency checking and negative sampling
3. Cross-encoder training

Plus the **14,156 consistency-checked training pairs**, the **33,099 synthetic queries** in TSV,
and the complete Vespa application, open-sourced on GitHub.

## Closing Direction

The stated conclusion: instruction-prompted LLMs make synthetic training data practical with
minimal human labeling, and flan-t5-xl produced high-quality domain-specific queries from three
examples. Future work named — generative models for re-ranking, summarization, and
question-answering inside retrieval-augmented systems — with retrieval quality treated as
foundational to everything downstream. See [[RAG]].

## Related Concepts

- [[Synthetic Query Generation]] — the technique this article is the vault's primary source for
- [[Consistency Filtering]] — the quality gate, with its 43% retention rate
- [[FLAN-T5]] — the generator
- [[Cross-Encoder]] — the trained ranker, and the versioning argument for choosing it
- [[Knowledge Distillation]] — 3B generative teacher → 22M ranker
- [[Hard Negative Mining]] — negatives sampled from the retrieved top-100
- [[Query Specificity]] — what the prompt instruction was asking for
- [[Zero-Shot Retrieval]] — the baseline this improves on, and its "synthetic in-domain labels" option
- [[PROMPTAGATOR]] — the prior work with the same shape and a much larger model
- [[Presentation Bias]] · [[Implicit Judgments]] — the click-based alternative and its biases
- [[ONNX]] — how the model reaches the serving path
- [[Reranking]] · [[Retrieval Pipeline]] — where the cross-encoder sits

## Related Articles

- [[Improving Zero-Shot Ranking with Vespa Hybrid Search - part two]] — supplies both the baseline and the consistency filter
- [[Improving Zero-Shot Ranking with Vespa Hybrid Search]] — part one, the problem statement
- [[Improving retrieval with LLM-as-a-judge]] — [[Jo Kristian Bergum]]; LLMs generating *labels* rather than *queries*
- [[Distilling Retrieval Pipelines to a Single Embedding Model]] — distillation of a pipeline rather than of a generator

## Datasets

- [[TREC-COVID]] — the experimental domain, 171K documents
- [[MS MARCO]] — referenced for the 30% neural improvement figure
- [[BEIR]] — the suite TREC-COVID belongs to

## People

- [[Jo Kristian Bergum]] — author

## External References

- Part two — https://blog.vespa.ai/improving-zero-shot-ranking-with-vespa-part-two/
- CORD-19 search demo — https://cord19.vespa.ai/
- PROMPTAGATOR paper — https://arxiv.org/abs/2209.11755
