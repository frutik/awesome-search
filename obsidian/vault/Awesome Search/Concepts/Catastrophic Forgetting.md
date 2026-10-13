---
type: concept
title: Catastrophic Forgetting
aliases:
  - Multi-Domain Fine-Tuning
  - multi-domain training
  - single-domain vs multi-domain fine-tuning
  - domain specialization
tags:
  - concept
  - fine-tuning
  - embeddings
  - retrieval
  - evaluation
created: 2026-10-13
---

# Catastrophic Forgetting

Catastrophic forgetting is what a retrieval model loses when it is fine-tuned hard on one domain: it gets better at that domain and worse everywhere else, sometimes worse than an off-the-shelf model that was never fine-tuned. It is the price of [[Embedding Fine-tuning|domain fine-tuning]], and the choice between single-domain training, multi-domain training, and per-domain experts is a choice about how much of that price to pay.

---

## What it looks like

The clearest measured case is [[Fine-Tuning Sparse Embeddings for E-Commerce Search|Thierry Damiba's SPLADE series]]. A [[SPLADE]] model fine-tuned on the [[Amazon ESCI Dataset]] reached 0.389 nDCG@10 in-domain, +27.5% over [[BM25]]. Tested elsewhere:

- On [[Home Depot Product Search Relevance|Home Depot]] data, the off-the-shelf model beat it (0.391 vs 0.384): fine-tuning on one retailer's catalog does not automatically transfer to another.
- On [[MS MARCO]] general web queries it scored 0.751 against BM25's 0.915. The series attributes this to Amazon-specific vocabulary ("renewed") and brand-heavy query patterns overwriting general language ability.

The figures come from a 100k-product / 10k-query subsample and are not comparable to official ESCI benchmarks.

## Single-domain, multi-domain, or experts

**Single-domain fine-tuning** gives the best score on the one catalog it was trained on and the steepest drop off it.

**Multi-domain training** mixes several domains into one training run. In Damiba's series, training on ESCI, [[WANDS Dataset|WANDS]], and Home Depot (50K samples each) gave up 4.4% on ESCI against the single-domain model and gained on the other three: +3.1% on WANDS, +6.8% on Home Depot, +10.4% on MS MARCO. It trades peak in-domain accuracy for consistency; it does not escape the tradeoff.

**Per-domain experts with routing** keep one frozen base encoder and train one [[LoRA]] adapter per domain, then route each query to the right expert. In [[RouterRetriever - Routing over a Mixture of Expert Embedding Models|RouterRetriever]], this beat a single MS MARCO-trained model by 2.1 nDCG@10 and a multi-task model by 3.2 on [[BEIR]] datasets. Adding experts kept helping with diminishing returns, while multi-task training degraded past a certain number of domains. Adding a domain means training one more adapter.

## Choosing

Damiba's series and [[Evgeniya Sukhodolskaya]]'s [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce|talk on the same work]] give the same rule:

- **One retailer with training data**: fine-tune on your own catalog.
- **A marketplace or several retailers**: multi-domain training.
- **No training data**: stay with an off-the-shelf model.

Sukhodolskaya adds a fourth case: if what you have already works, leave it alone.

## Catching it

[[Model Selection and Fine-Tuning Evaluation]] lists the signal: large gains on the fine-tuned domain together with a collapse on general queries. The check is to keep a held-out general set and score it at every checkpoint, alongside the in-domain dev set ([[Zero-Shot Retrieval]] behaviour).

## Limiting it during training

- **Freeze most of the model.** [[Fine-tuning Multimodal Embedding Models]] recommends, for small datasets, fine-tuning only the top layers and projection heads so the model keeps its general features. Per-domain [[LoRA]] adapters on a frozen encoder apply the same idea.
- **Mix domains** in training, as above.

## A different failure under the same name

[[Fine-Tuning an Embedding Model for Semantic Search]] uses "catastrophic forgetting" for a training collapse: trained with negatives that are too semantically similar to the positives, a model can lose the ability to tell texts apart and cluster all embeddings together. Its mitigation is clearly distinct negatives and shorter text segments. That is a failure of the training run itself, not the loss of other domains described above.

## Related Concepts

- [[Embedding Fine-tuning]] · [[SPLADE]] · [[LoRA]] · [[Hard Negative Mining]] · [[Zero-Shot Retrieval]] · [[Benchmark Contamination]]

## Datasets

- [[Amazon ESCI Dataset]] · [[WANDS Dataset]] · [[Home Depot Product Search Relevance]] · [[MS MARCO]] · [[BEIR]]

## Topics

- [[Model Selection and Fine-Tuning Evaluation]]

## Related Articles

- [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] · [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]] · [[RouterRetriever - Routing over a Mixture of Expert Embedding Models]] · [[Fine-tuning Multimodal Embedding Models]] · [[Fine-Tuning an Embedding Model for Semantic Search]]

## People

- [[Thierry Damiba]] · [[Evgeniya Sukhodolskaya]]
