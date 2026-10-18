---
type: concept
title: Domain-Specific Semantic Gaps
aliases:
  - domain semantic gap
  - domain-specific semantic gap
tags:
  - concept
  - embeddings
  - fine-tuning
  - domain-adaptation
related_concepts:
  - "[[Embedding Fine-tuning]]"
  - "[[Out-of-Vocabulary]]"
  - "[[Catastrophic Forgetting]]"
created: 2026-10-18
---

# Domain-Specific Semantic Gaps

A domain-specific semantic gap is a relationship that matters inside a field but that a general-purpose embedding model does not encode: two terms the domain treats as equivalent land far apart in the vector space, or a domain's abbreviations and their meanings are not connected. The model knows the words; it does not know what the domain means by them.

---

## What it looks like

[[Ritik Jain]] gives three cases from production work:

- **Legal** — "indemnification clause" and "hold harmless provision" are synonyms to a lawyer, but a general model may not place them together.
- **Healthcare** — clinical abbreviations and the relationships between them need specialised knowledge.
- **Finance** — domain terms and how they relate carry the meaning of a document.

[[Embedding Fine-tuning]] adds the same pattern elsewhere: "apoptosis" in biology, "covenant" in legal text.

## Why it matters for retrieval

A gap in the embedding space becomes a gap in recall: the relevant passage is phrased in the other term and is never retrieved. In [[RAG]] the error carries forward — weaker embeddings mean less relevant retrieved context, which means worse generated answers. The author reports gains in retrieval metrics on domain tasks from closing these gaps by fine-tuning, quoting ranges from 5–25% to 7–22% in different parts of the guide; none is a measured benchmark result.

## How it differs from a vocabulary gap

A lexical vocabulary gap — "sofa" vs. "couch", a typo, an unexpanded abbreviation — can be closed outside the model with synonym dictionaries, spelling correction or [[Query Expansion]] (see [[Synonyms and Vocabulary Management]]). A semantic gap sits in the geometry of the model itself, and closing it means changing the embedding space: fine-tuning on domain data so that the domain's own equivalences pull together. Terms the model has never seen are a related but separate problem — see [[Out-of-Vocabulary]].

## The cost of closing it

Pulling a model toward one domain's semantics tends to push it away from others. [[Catastrophic Forgetting]] covers how much general quality is lost and how multi-domain training limits it.

## Related Concepts
- [[Embedding Fine-tuning]] — the fix
- [[Dataset Types for Embedding Fine-Tuning]] — what training data encodes the domain's relationships
- [[Synonyms and Vocabulary Management]] — the lexical counterpart, solved outside the model
- [[Out-of-Vocabulary]] · [[Query Expansion]]
- [[Catastrophic Forgetting]] — the trade-off
- [[Zero-Shot Retrieval]] — what a general model offers before fine-tuning

## Related Articles
- [[The Complete Guide to Fine-Tuning Embedding Models]]

## People
- [[Ritik Jain]]
