---
type: article
title: "Before You Fix Your Search, Know What's Actually Broken"
source: "https://unscriptedai.substack.com/p/before-you-fix-your-search-know-whats"
author: "[[Atita Arora]]"
published: 2026-06-16
created: 2026-06-18
tags: [article, search-strategy, problem-diagnosis, search-archetypes]
concepts: ["[[Search Problem Archetypes]]", "[[Search Evaluation]]", "[[Judgment Lists]]", "[[Zero Results]]", "[[Agentic Search]]", "[[Knowledge Graph Search]]", "[[Personalization]]", "[[Precision and Recall]]"]
topics: ["[[Search Problem Archetypes]]", "[[E-commerce Search]]", "[[Relevance Program Setup]]"]
people: ["[[Atita Arora]]", "[[Udi Manber]]"]
---

# Before You Fix Your Search, Know What's Actually Broken

[[Atita Arora]] argues that most search engagements fail not because the team picked the wrong engine or model, but because they are **solving the wrong problem entirely**. Before investing in LTR, vector search, or any sophistication, you must correctly identify *which recurring pattern* your search problem belongs to — because the diagnosis determines which layer to fix first (data model vs. ranking vs. evaluation vs. architecture).

The piece is framed around Russell Ackoff's observation that "we fail more often because we solve the wrong problem than because we get the wrong solution to the right problem," and Udi Manber's warning that many people wrongly believe "search is essentially a solved problem."

---

## The Core Diagnosis

The recurring failure mode: a team is deep into a sophisticated implementation — LTR, vector search, custom plugins, feature engineering — and the model "looks good in the lab." Then someone asks *"Define a good result from your user's perspective?"* and there is silence. Nobody has formally defined relevance. No [[Search Evaluation|evaluation framework]]. No [[Judgment Lists|judgment lists]]. The model is optimizing a signal nobody verified maps to user satisfaction — a **measurement and alignment problem**, not a model bug. No amount of ranking sophistication fixes a foundation problem.

## The 10 Search Problem Archetypes

The article's central contribution — a self-slotting diagnostic taxonomy. See the full breakdown in [[Search Problem Archetypes]].

1. **The Uniqueness Problem** — one-of-a-kind inventory (marketplaces, pre-owned, handmade); freshness existential, thin demand signals, vocabulary mismatch.
2. **The Complexity Machine** — variant-heavy catalogs (retail, fashion); mixed known-item + exploratory intents, sponsored vs. organic blending. Classic LTR/semantic candidate.
3. **The Precision Mandate** — legal, clinical, regulatory; a plausible-but-wrong result is worse than none. Provenance and scope correctness are first-class.
4. **The Firehose Pattern** — news/media/live events; freshness vs. relevance tug-of-war, authority explicit in relevance.
5. **The Extraction Pattern** — machine/agent consumer; structured extraction from unstructured input at low latency; schema drift causes silent failures.
6. **The Media Vault** — image/video/audio catalogs; sparse, missing metadata; conceptual/mood queries; rights & popularity signals.
7. **The Knowledge Graph** — answers composite across documents and entity relationships; taxonomy/ontology quality is the bottleneck.
8. **Geospatial Use Cases** — distance/proximity/bounding-box/polygon as first-class relevance; GIS vs. search expertise split.
9. **Q-commerce Use Cases** — real-time relevance under operational constraints (delivery window, availability, geo); substitutes are core, not edge.
10. **The Code Search** — inherits traits from knowledge graph, precision mandate, firehose, extraction; severe vocabulary mismatch and version-correctness.

## Why Naming the Archetype Matters

- **Same symptom, opposite prescription.** [[Zero Results|Zero results]] in e-commerce is wasted real estate (show substitutes); in a precision mandate it is often *better* than a marginally-similar legal precedent. Same dashboard metric, opposite fix.
- **Systems sit between archetypes and outgrow them.** A small marketplace landing a big retail partner suddenly inherits variants, suppliers, and sponsored-products problems — a shift of archetype, so the diagnosis should shift too.
- **The archetype points at which layer to fix first**, not how. Reranking sophistication won't fix data-modeling gaps in the Uniqueness Problem; a "better" embedding won't fix sponsored-vs-organic misalignment in the Complexity Machine. Sequence matters.
- **Measurable ≠ useful.** Many teams adopt proxy metrics from conference talks without verifying validity.

## On Agentic Retrieval

[[Agentic Search|Agentic retrieval]] is **not a separate archetype** — it is a *consumption pattern* sitting on top of whichever archetype the system already belongs to (an agent doing financial research is in the Extraction Pattern; a legal-review agent is in the Precision Mandate). What changes is the **evaluation contract**: a wrong result a human would catch and ignore becomes a wrong *action* an agent executes autonomously — so precision, result confidence, and scope correctness become hard requirements, not nice-to-haves. Jumping to "we need agentic…" without defining the problem is the same mistake the whole article warns against.

---

## Related Concepts
- [[Search Problem Archetypes]] — the full diagnostic taxonomy this article introduces
- [[Search Evaluation]] / [[Judgment Lists]] — the missing foundation behind most failures
- [[Zero Results]] — canonical "same metric, opposite prescription" example
- [[Agentic Search]] — consumption pattern, not an archetype
- [[Knowledge Graph Search]] · [[Precision and Recall]] · [[Personalization]]

## Related Articles
- [[Search - Intent Not Inventory]] — complementary "name the real problem" framing
- [[Getting Started on Search Relevance for the Understaffed Search Team]] — sequencing relevance work
- [[What is a Relevant Search Result]] — defining relevance from the user's perspective

## People
- [[Atita Arora]] — author
- [[Udi Manber]] — quoted; "search is essentially a solved problem" misperception
