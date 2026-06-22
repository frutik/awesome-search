---
title: "Concept Vectors"
aliases: ["concept vectors", "concept activation vectors", "CAV", "concept directions"]
tags:
  - concept
  - embeddings
  - interpretability
  - representation-learning
---

# Concept Vectors

A **direction** in a model's representation (embedding or activation) space that corresponds to a human-interpretable concept. Moving along the vector adds "more" of the concept; the dot product of a representation with the concept vector measures how strongly the concept is present. Concept Activation Vectors (CAVs) are the canonical example: a linear probe trained to separate examples that have a property from those that don't, with the probe's normal as the concept direction.

Concept vectors treat meaning as a **linear direction in point-vector space**, which is the same representational world that [[Region-Based Representation|region representations]] react against — a point/direction cannot express containment or set operations the way a [[Box Embedding|box]] can. They are closely related to [[Steering Vectors]], which *add* concept directions to activations to change model behavior.

> Note: a representation-engineering / interpretability concept, related here thematically — both concept vectors and [[Box Embedding|boxes]] are attempts to give geometric structure to "meaning", but along different axes (linear direction vs. region/volume).

## Related Concepts
- [[Steering Vectors]] — concept directions used to steer model behavior
- [[Embeddings]] — the vector space concept directions live in
- [[Box Embedding]] — region-based alternative to direction-based meaning
- [[Set-Theoretic Embeddings]] — set-based vs. direction-based notions of concept


## How They're Read (Representation Engineering)

In the **representation engineering** framing, finding a concept vector is called **representation reading**: build **contrast pairs** (inputs differing only in the target concept), record activations, and derive the linear direction from their difference. Techniques include **LAT (Linear Artificial Tomography)** and **mean-centering** for cleaner directions. The read direction is then used by [[Steering Vectors|representation steering]] to control behavior.

## Reference
- Jan Wehner, *[An Introduction to Representation Engineering](https://www.alignmentforum.org/posts/3ghj8EuKzwD3MQR5G/an-introduction-to-representation-engineering-an-activation)* (AlignmentForum, 2024) — reading vs. steering; LAT, contrast pairs, mean-centering. *(LLM interpretability — referenced here as background for the representation-geometry theme, not search/IR.)*