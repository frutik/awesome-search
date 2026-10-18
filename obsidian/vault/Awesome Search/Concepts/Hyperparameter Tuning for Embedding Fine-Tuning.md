---
type: concept
title: "Hyperparameter Tuning for Embedding Fine-Tuning"
aliases: ["hyperparameter tuning", "hyperparameters", "embedding fine-tuning hyperparameters"]
tags:
  - concept
  - embeddings
  - fine-tuning
  - hyperparameters
related_concepts:
  - "[[Embedding Fine-tuning]]"
  - "[[Embedding Loss Functions]]"
  - "[[Contrastive Learning]]"
created: 2026-10-18
---

# Hyperparameter Tuning for Embedding Fine-Tuning

[[Ritik Jain]]'s guide to fine-tuning an embedding model covers four settings — learning rate, batch size, warmup and number of epochs — each tuned from what the training curve shows. Elsewhere the data is found to matter more: the choice of negatives moves results more than the learning rate does ([[Contrastive Learning]], [[Hard Negative Mining]]).

---

## The four knobs

[[Ritik Jain]]'s rules of thumb:

- **Learning rate** — if the loss plateaus early, raise it; if the loss oscillates, lower it.
- **Batch size** — with in-batch-negative losses such as MNRL, a larger batch means more negatives and a stronger signal. Grow it while memory allows (32 → 64 → 128); on out-of-memory errors step down (32 → 16 → 8). When memory is the limit, the cached loss variant gets the effect of a large batch without the memory ([[Embedding Loss Functions]]).
- **Warmup** — keep the default of 10% of training steps; if the loss oscillates early in training, raise it to 15–20%.
- **Epochs** — on small datasets, one epoch, to avoid overfitting; on larger ones, one or two while watching the evaluation metrics.

## Parameter-efficient fine-tuning adds one more

With [[LoRA]], the adapter rank is the key extra hyperparameter: lower rank means fewer trainable parameters and less capacity.

## Tuning against the dev set

Picking the best checkpoint on a dev set once is fine. Sweeping dozens of runs and settings against that same set over-fits to it, and its numbers become optimistic. Keep a third split that is opened once, before shipping — see [[Model Selection and Fine-Tuning Evaluation]]. Long or aggressive training on one domain also increases [[Catastrophic Forgetting]] of everything outside it.

## Related Concepts
- [[Embedding Fine-tuning]] · [[Embedding Loss Functions]] · [[Dataset Types for Embedding Fine-Tuning]]
- [[Contrastive Learning]] · [[Hard Negative Mining]]
- [[LoRA]] · [[Catastrophic Forgetting]]

## Related Topics
- [[Model Selection and Fine-Tuning Evaluation]]

## Related Articles
- [[The Complete Guide to Fine-Tuning Embedding Models]]

## People
- [[Ritik Jain]]
