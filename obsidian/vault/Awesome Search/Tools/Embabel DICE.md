---
title: Embabel DICE
type: tool
aliases: ["embabel/dice", "dice (Kotlin)"]
tags:
  - tool
  - context-engineering
  - agentic-memory
  - knowledge-graph
  - kotlin
  - incubating
website: https://github.com/embabel/dice
repo: https://github.com/embabel/dice
created: 2026-09-07
---

# Embabel DICE

The reference implementation of [[DICE]], and a module of the [[Embabel]] agent framework — a Kotlin/Spring library for knowledge-graph construction and reasoning over LLM-extracted propositions. Carries an **Incubating** badge; pre-release.

- Repo: https://github.com/embabel/dice

---

## What It Does

Turns unstructured text into typed, scored propositions, resolves the entities they mention to canonical ids, reconciles them against what is already stored, and projects the result into whichever backend the application needs. Propositions are the system of record; graphs, Prolog facts and agent memory are all *projections* of them.

The four stages:

1. **Extraction** — `LlmPropositionExtractor` pulls typed propositions with confidence, importance and decay scores.
2. **Entity resolution** — mentions resolve to canonical entity ids through an escalating chain.
3. **Revision** — `LlmPropositionReviser` classifies each new proposition as `IDENTICAL`, `SIMILAR`, `CONTRADICTORY`, `GENERALIZES` or `UNRELATED`; similar ones merge, conflicting ones lose confidence.
4. **Projection** — into Neo4j graphs, Prolog facts, or agent memory.

`PropositionPipeline` orchestrates the first three.

## Entity Resolution

The design worth stealing: `EscalatingEntityResolver` runs `CandidateSearcher`s **cheapest first** — by id, exact name, normalized name, partial name, fuzzy name, vector, then agentic — stopping as soon as one resolves. Where several candidates survive, `LlmCandidateBakeoff` asks a model to choose.

This keeps the expensive paths (vector search, an LLM call) off the common case, which is the same instinct behind tiering models in [[Agentic Memory for Search Personalization]].

## Memory Model

`MemoryProjection` separates propositions by `KnowledgeType` — `SEMANTIC`, `EPISODIC`, `PROCEDURAL`, `WORKING`. The `Memory` class implements `LlmReference` with both eager and on-demand retrieval, and `MemoryMaintenanceOrchestrator` consolidates, abstracts and retires memories over time.

`ContextId` is the primary scoping mechanism for every proposition query: one user may hold several contexts (personal, team, project), and one context may be shared between users.

## Stack

Kotlin with Java interop · Spring Boot · Maven · **tuProlog** for inference · **Neo4j** for graph projection · Jinja templates for prompts · Apache Tika for file extraction · Micrometer for metrics.

A REST surface exposes `/api/v1/contexts/{contextId}/` for extraction, proposition CRUD and search, and entity-scoped memory retrieval, with optional `X-API-Key` authentication.

## Related Tools

- [[django-dice]] — an independent Python/Django implementation of the same design

## Related Concepts

- [[Agents That Extract and Use Preferences from Conversations]] — a practitioner walkthrough wiring this into a chatbot, with the controller/pipeline bean setup
- [[DICE]] — the framework this implements
- [[Agentic Memory]] · [[Context Engineering]] · [[Knowledge Graph Search]]
