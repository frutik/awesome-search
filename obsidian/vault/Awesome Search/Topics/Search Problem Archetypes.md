---
type: topic
aliases: ["search archetypes", "search problem patterns", "search problem diagnosis", "search problem types"]
tags: [topic, search-strategy, problem-diagnosis, search-archetypes]
related_concepts: ["[[Search Evaluation]]", "[[Judgment Lists]]", "[[Zero Results]]", "[[Knowledge Graph Search]]", "[[Agentic Search]]", "[[Precision and Recall]]", "[[Personalization]]", "[[Search Intent]]", "[[Query Types]]"]
related_topics: ["[[E-commerce Search]]", "[[Enterprise Search]]", "[[Relevance Program Setup]]", "[[Conversational and Agentic Search]]"]
articles: ["[[Before You Fix Your Search, Know What's Actually Broken]]", "[[Search - Intent Not Inventory]]", "[[Deconstructing E-Commerce Search - The 12 Query Types]]"]
created: 2026-06-18
---

# Search Problem Archetypes

A diagnostic framework for **naming the search problem you actually have before choosing a solution**. The premise — drawn from [[Atita Arora]]'s [[Before You Fix Your Search, Know What's Actually Broken]] and Russell Ackoff's systems thinking — is that most search problems are not unique: they are instances of a small number of recurring patterns. The most valuable thing you can do before investing in LTR, vector search, or a new model is to correctly identify *which pattern you are in*, because the archetype tells you **which layer to fix first** (data model vs. ranking vs. evaluation vs. architecture).

---

## Why Diagnosis Comes Before Solution

Teams self-diagnose with comfortable, sophisticated-sounding answers — "we need better ranking", "we need vector search", "we need a better model". But the problem definition is usually a *symptom, not a diagnosis*. The most common foundation failure: a team has built sophisticated retrieval but **never formally defined relevance** — no [[Search Evaluation|evaluation framework]], no [[Judgment Lists|judgment lists]], no shared definition of a good result. The model optimizes a signal nobody verified maps to user satisfaction. This is a **measurement / alignment problem**, and no ranking sophistication fixes it.

> "We fail more often because we solve the wrong problem than because we get the wrong solution to the right problem." — Russell Ackoff

## The 10 Archetypes

| # | Archetype | Core tension | Typical domains | Fix-first layer |
|---|---|---|---|---|
| 1 | **Uniqueness Problem** | One-of-a-kind inventory; freshness existential; thin demand signals; vocabulary mismatch | Marketplaces, pre-owned, handmade, classifieds | Data modeling |
| 2 | **Complexity Machine** | Variant-heavy catalog; mixed known-item + exploratory intent; sponsored vs. organic | Retail, fashion, health, price comparison | Intent routing / ranking |
| 3 | **Precision Mandate** | Plausible-but-wrong is worse than nothing; provenance & scope correctness first-class | Legal, clinical, tax, regulatory | Precision, lineage, scope |
| 4 | **Firehose** | Recency vs. relevance tug-of-war; authority explicit; unpredictable volume | News, media, social, live events | Freshness & authority signals |
| 5 | **Extraction** | Consumer is a machine/agent/pipeline; structured extraction at low latency; schema drift | Financial news→events, feeds, research pipelines | Extraction precision / latency |
| 6 | **Media Vault** | Non-text catalog (image/video/audio); sparse/missing metadata; conceptual/mood queries | Stock media, DAM, archives, video | Metadata / multimodal layer |
| 7 | **Knowledge Graph** | Answer composite across documents & entity relationships; taxonomy/ontology quality | Procurement, talent networks, compliance, gastronomy | Ontology / entity modeling |
| 8 | **Geospatial** | Distance, proximity, bounding box, polygon as first-class relevance | Satellite/aerial, urban planning, mapping, govt | Spatial indexing / architecture |
| 9 | **Q-commerce** | Real-time relevance under operational constraints (delivery window, availability, geo) | Food delivery, ride-hailing, on-demand, logistics | Supply/operational alignment |
| 10 | **Code Search** | Inherits KG + precision + firehose + extraction; vocabulary mismatch; version correctness | Coding agents, version control, API docs, code review | Depends on inherited pattern |

### How to Know Which One You're In (selected tells)
- **Uniqueness** — standard taxonomies don't fit ("handcrafted ceramic bowl" ≠ "kitchenware"); an item sold is gone.
- **Complexity Machine** — Master/Variant SKUs; a single pipeline tuned for neither known-item nor exploratory intent.
- **Precision Mandate** — recall isn't enough; wrong jurisdiction / wrong revision / wrong rate range is a hard fail.
- **Firehose** — most relevant doc is years old while the most recent has no topical reference; query volume spikes on events.
- **Extraction** — traditional relevance evals don't apply; failure to extract has compounding downstream consequences.
- **Media Vault** — asset names are random/numeric with no relation to content; lexical layer still doing most of the work.
- **Knowledge Graph** — users browse more than search; nested relationships (supplier → product → certification → regulation).
- **Geospatial** — bounding box / radius / polygon queries not served by standard search; coordinate-system errors at query time.
- **Q-commerce** — supply-side fulfilment confused with query-side sophistication; substitutes treated as edge case.
- **Code Search** — query intent ambiguous (file? function? class? call chain?); `conn_rety` / `retryConnection` / `retry_on_connection_error`.

## Operating Principles

- **Same symptom, different meaning.** [[Zero Results|Zero results]] in e-commerce (Uniqueness / Complexity Machine) is wasted real estate — show substitutes, never a dead end. In a Precision Mandate, zero results is often *better* than a marginally-similar regulation or precedent. Same metric on the same dashboard, opposite prescription.
- **Systems sit between archetypes and outgrow them.** A small marketplace landing a big retail partner suddenly inherits variants, suppliers, and sponsored-products problems — a shift of archetype, so the diagnosis should shift too.
- **The archetype names which layer to fix first, not how.** Reranking won't fix data-modeling gaps; a "better" embedding won't fix sponsored-vs-organic business misalignment. Sequence matters; most teams skip to solutions before the problem is discovered.
- **Measurable ≠ useful.** Just because a metric is measurable doesn't mean it's valid for your case.

## Agentic Retrieval Is Not an Archetype

[[Agentic Search|Agentic retrieval]] is a **consumption pattern** that sits on top of whichever archetype the system already belongs to (a financial-research agent → Extraction; a legal-review agent → Precision Mandate). What changes is the **evaluation contract**: a wrong result a human would catch and ignore becomes a wrong *action* an agent executes autonomously. Precision, result confidence, and scope correctness become hard requirements, not nice-to-haves.

---

## Related Topics
- [[E-commerce Search]] — spans the Uniqueness Problem and the Complexity Machine
- [[Enterprise Search]] — frequently a Knowledge Graph or Precision Mandate problem
- [[Relevance Program Setup]] — building the evaluation foundation whose absence drives most misdiagnoses
- [[Conversational and Agentic Search]] — agentic retrieval as a consumption pattern over archetypes

## Related Concepts
- [[Search Evaluation]] · [[Judgment Lists]] — the foundation most teams skip
- [[Zero Results]] — canonical "same metric, opposite prescription" example
- [[Knowledge Graph Search]] · [[Precision and Recall]] · [[Search Intent]] · [[Query Types]]

## Articles
- [[Before You Fix Your Search, Know What's Actually Broken]] — [[Atita Arora]]; source of this framework
- [[Search - Intent Not Inventory]] — complementary "name the real problem" framing
- [[Deconstructing E-Commerce Search - The 12 Query Types]] — query-level taxonomy within the e-commerce archetypes

## People
- [[Atita Arora]] — author of the archetype framework
- [[Udi Manber]] — "search is essentially a solved problem" misperception
