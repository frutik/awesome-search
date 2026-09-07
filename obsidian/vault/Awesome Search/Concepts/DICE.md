---
type: concept
title: "DICE"
aliases: ["Domain Injected Context Engineering", "Domain Integrated Context Engineering", "DICE framework"]
tags:
  - concept
  - context-engineering
  - agentic-memory
  - personalization
  - preference-extraction
created: 2026-09-07
---

# DICE

## Definition

**DICE** is a framework for integrating a domain model into LLM interactions: the application's own business ontology — not the prompt — is the source of truth, and structured facts about the user are extracted from conversation, persisted, and injected back into later context.

The acronym is rendered two ways in its own sources: **Domain Injected Context Engineering** and **Domain Integrated Context Engineering**. Both appear in the project's documentation.

Its stated premise is that LLMs get safer as structure is added to their inputs and outputs. The problem it addresses has been called the **grounding gap** — the absence of common ground between the model and the user's question, which a system can close by learning about the user from observation instead of asking.

## Four Principles

1. **Domain-first architecture** — domain objects and business ontology are the source of truth, not prompts.
2. **Structured bidirectional mapping** — domain structure governs both what is sent to the LLM and what comes back.
3. **Code-driven context filtering** — *code*, not the model, decides what enters the context window.
4. **Persistent domain integration** — LLM-derived knowledge is grounded in existing persistence (SQL, graph), not a greenfield vector store.

Principle 3 is the load-bearing one for anyone who has watched a context window fill with marginally relevant retrieved text. Principle 4 is the contrarian one: it declines the default assumption that agent memory implies a new vector database.

DICE ships **no built-in entity types or predicates** — the schema is entirely user-defined. An e-commerce schema might declare entity types `Customer, Product, Category, Brand, Feature, PriceRange` and predicates `prefers, dislikes, is looking for, has budget of, owns, is interested in, needs`.

## Propositions

The unit of storage is a natural-language **proposition** carrying three scores:

| Score | Range | Meaning |
|---|---|---|
| **Confidence** | 0.0–1.0 | How certain the fact is |
| **Importance** | 0.0–1.0 | How much the fact matters |
| **Decay** | 0.0–1.0 | How quickly it goes stale |

Decay is the difference between where you parked your car and the day you got married. Propositions also carry an **explanation** of why they were proposed — *"user explicitly says they like tutorials about agents"* for a 90%-confidence preference — which makes the store auditable rather than merely scored.

**Effective confidence** applies time-based decay, so retrieval ranks by recency-weighted certainty rather than raw score. Propositions are treated as the system of record, accumulating evidence and *projecting* into typed backends rather than being overwritten.

## The Pipeline

1. **Extract** — the LLM reads a conversation turn plus the schema and existing propositions, returning new propositions.
2. **Revise** — new propositions are deduplicated and reconciled against the store; the reference implementation classifies each as `IDENTICAL`, `SIMILAR`, `CONTRADICTORY`, `GENERALIZES` or `UNRELATED`, merging similar ones and reducing confidence on conflicts.
3. **Inject** — the top-N propositions by `importance × confidence` are prepended to the agent's system prompt.

The Kotlin implementation adds an **entity resolution** stage between extraction and revision, escalating through progressively more expensive candidate searchers — by id, exact name, normalized name, partial name, fuzzy name, vector, then agentic — with an LLM bake-off to pick between candidates. It also adds a **projection** stage materializing propositions into Neo4j graphs, Prolog facts, or agent memory.

## Memory Types

DICE splits memory four ways:

| Type | Holds | Durability |
|---|---|---|
| **Semantic** | Stable facts — "prefers Sony", "hates leather", "budget under €100" | Permanent (low decay) |
| **Procedural** | How the user wants things done — "always show prices first", "don't suggest bundles" | Permanent |
| **Episodic** | Specific past events — "bought running shoes last March" | Medium-lived |
| **Working** | In-session context — "currently looking for a gift for her husband" | Expires fast (high decay) |

This is the cognitive-psychology taxonomy also used in the [[AI Agent Memory - Creating Smart Agents with Elasticsearch Managed Memory|Elasticsearch treatment]] of [[Agentic Memory]], plus a working type. Note the divergence in what *procedural* means: DICE stores user preferences about interaction style as procedural data, where the Elasticsearch write-up treats procedural memory as agent behaviour that lives in code and is never persisted.

The split is not cosmetic — it decides scope. In [[django-dice]], semantic, procedural and episodic memories are written globally with a null conversation id and survive every future conversation, while working memory is tied to the current conversation and disappears with it.

## Relation to Search Personalization

DICE arrives at the same place as [[Agentic Memory for Search Personalization]] from a different direction — conversational agents rather than a search box — and the mechanics converge: an LLM extracting durable preference statements, scoring them, decaying them, and injecting a bounded top-N at inference time. The `importance × confidence` cap is the same instinct as capping preference retrieval at a handful of facts.

Where it differs is grounding: DICE insists preferences live in the domain schema and existing persistence, rather than in an engine-native memory store.

## Provenance

The framework is credited to [[Embabel]], the JVM agent framework created by Rod Johnson (founder of the Spring Framework), whose Kotlin/Spring library is the reference implementation. It is heavily inspired by the **General User Models (GUM)** paper:

> *Creating General User Models from Computer Use* — Omar Shaikh, Shardul Sapkota, Shan Rizvi, Eric Horvitz, Joon Sung Park, Diyi Yang, Michael S. Bernstein — https://arxiv.org/abs/2505.10831

What DICE carries over from GUM: learning from observed interaction rather than stated preference; propositions with confidence; revision of propositions as new observations arrive; a staleness factor; and an **audit** step for facts the system should not remember. The [[django-dice]] documentation additionally reports 76% accuracy for high-confidence propositions — recorded as that project states it, not independently verified here.

## Related Concepts

- [[Context Engineering]] — DICE is a specific, domain-model-driven discipline of it
- [[Agentic Memory]] — the same problem; compare taxonomies and storage assumptions
- [[Personalization]] — what extracted preferences are for
- [[Knowledge Graph Search]] — propositions projected into a graph backend

## Related Tools

- [[Embabel DICE]] — the Kotlin/Spring reference implementation
- [[django-dice]] — a Python/Django implementation for e-commerce preference inference

## Articles

- [[Agents That Extract and Use Preferences from Conversations]] — [[Jettro Coenradie]]; the GUM lineage, a worked extraction example, and extraction moved off the response path

## Related Topics

- [[Agentic Memory for Search Personalization]]
