---
title: "Steering Vectors"
aliases: ["steering vectors", "activation steering", "representation engineering", "activation addition"]
tags:
  - concept
  - embeddings
  - interpretability
  - representation-learning
  - llm
---

# Steering Vectors

A direction in a model's **activation space** that, when added to the hidden states at inference time, shifts the model's behavior toward (or away from) a target attribute — tone, refusal, a topic, a style. Constructed by contrasting activations on examples that have the attribute against those that don't (closely related to [[Concept Vectors|concept activation vectors]]), then adding a scaled copy of that difference vector during the forward pass. The basis of "activation steering" / representation engineering for LLMs.

Steering vectors rely on the **linear representation** view: meaningful concepts are directions in a point-vector space. This is the same point-vector paradigm that [[Region-Based Representation|region representations]] like [[Box Embedding|box embeddings]] extend — boxes add *volume and containment* to "meaning" instead of treating it purely as a direction.

> Note: an LLM interpretability / control technique, related here thematically rather than from the box-embedding article — both are about imposing useful geometric structure on learned representations.

## Related Concepts
- [[Concept Vectors]] — the concept directions steering vectors add
- [[Embeddings]] — the representation space steering operates on
- [[Box Embedding]] — region-based view of meaning vs. direction-based steering


## Techniques (Representation Engineering)

In **representation engineering**, steering splits into two stages: **representation reading** (find the [[Concept Vectors|concept direction]] from contrast pairs, e.g. via **LAT**) and **representation steering** (inject it). Common steering methods:
- **Contrastive Activation Addition** — add a scaled contrast-derived vector to the residual stream during the forward pass.
- **Spectral editing** — more efficient targeted edits.
- **Mean-centering** — yields more effective steering directions.

Reported uses: reducing sycophancy, improving truthfulness, preference alignment, and jailbreak detection.

## Reference
- Jan Wehner, *[An Introduction to Representation Engineering](https://www.alignmentforum.org/posts/3ghj8EuKzwD3MQR5G/an-introduction-to-representation-engineering-an-activation)* (AlignmentForum, 2024) — activation-based control of LLMs. *(LLM interpretability/alignment — referenced as background, not search/IR.)*