---
title: "FLAN-T5"
type: concept
aliases:
  - Flan-T5
  - flan-t5-xl
  - FLAN
tags:
  - concept
  - llm
  - foundation-model
  - synthetic-data
  - open-source
created: 2026-07-30
---

# FLAN-T5

Google's instruction-tuned variant of the T5 encoder-decoder model: a self-supervised base
fine-tuned on a broad, diverse mixture of tasks phrased as natural-language instructions. Google
open-sourced checkpoints **up to 11B parameters under the Apache 2.0 licence**.

For search work its significance is licensing and size rather than capability. Apache 2.0 plus
checkpoints small enough to run on one GPU makes it usable as an **offline data generator** — a
role where an API-gated model is awkward and an 11B open model is entirely sufficient.

---

## Why "Foundation Model"

The framing quoted in [[Improving Search Ranking with Few-Shot Prompting of LLMs]]:

> Massive self-supervised training on piles of text, coupled with later fine-tuning on a broad,
> diverse set of tasks, is one of the reasons they are called foundation models.

The instruction-tuning stage is what makes prompting work as a substitute for fine-tuning. The
weights stay frozen; behaviour is steered by instructions mixed with data in the prompt.

## Use as a Query Generator

`flan-t5-xl` (3B) is the generator in the vault's worked [[Synthetic Query Generation]] example:

| | |
|---|---|
| Model | flan-t5-xl, 3B parameters |
| Task | generate a search query for a given document |
| Prompt | instruction + **3** human-labeled examples |
| Throughput | ~3,600 queries/hour on one A100 40GB (~$1/hour) |
| Output | 33,099 synthetic queries over a 171K-document corpus |
| Downstream result | 22M [[Cross-Encoder|cross-encoder]] at **80.2 nDCG@10** on [[TREC-COVID]] |

The comparison that makes the size point: [[PROMPTAGATOR]] used a **137B** FLAN model for the same
kind of generation and reported 76.2 on the same dataset. Generator scale was not what decided the
outcome.

## Relation to Other Models in This Vault

| Model | Family | Role in retrieval |
|---|---|---|
| FLAN-T5 | T5, instruction-tuned | Offline generation of training data |
| [[MonoT5]] | T5, fine-tuned for ranking | Reranker; also a distillation teacher (monot5-3b in [[ELSER]]) |
| [[RankGPT]] | Decoder LLM, prompted | Listwise reranking at query time |
| [[BERT]] | Encoder | Backbone for bi-encoders, cross-encoders, [[ColBERT]] |

FLAN-T5 and MonoT5 share a base architecture and sit at opposite ends of the pipeline — one
manufactures labels before serving, the other scores documents during it.

## Related Concepts

- [[Synthetic Query Generation]] — the primary use here
- [[Knowledge Distillation]] — a 3B generator's knowledge ending up in a 22M ranker
- [[Consistency Filtering]] — what makes its raw output usable
- [[MonoT5]] — the T5 sibling fine-tuned for ranking instead of instruction-following
- [[RankGPT]] — prompting an LLM for ranking directly rather than for data
- [[LLM as Judge]] — the other way LLMs substitute for labels
- [[GGUF]] — the quantized-serving route for running open models like this locally

## Articles

- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — [[Jo Kristian Bergum]] ([[Vespa]]);
  flan-t5-xl as query generator, with released notebooks

## Source

- Model checkpoints — https://huggingface.co/google/flan-t5-xl
- *Scaling Instruction-Finetuned Language Models* — arXiv:2210.11416
