---
type: article
title: "Agents that extract and use preferences from conversations"
source: "https://medium.com/embabel/agents-that-extract-and-use-preferences-from-conversations-7b22cca9abb3"
author: ["Jettro Coenradie"]
published: 2026-01-28
paywall: true
tags:
  - clippings
  - context-engineering
  - agentic-memory
  - preference-extraction
  - kotlin
concepts:
  - DICE
  - Agentic Memory
  - Context Engineering
  - Personalization
tools:
  - Embabel DICE
people:
  - Jettro Coenradie
created: 2026-09-07
---

# Agents that extract and use preferences from conversations

**Source**: https://medium.com/embabel/agents-that-extract-and-use-preferences-from-conversations-7b22cca9abb3
**Published**: 28 January 2026 · **Author**: [[Jettro Coenradie]] · 12 min read

> [!warning] Paywall
> Member-only story on Medium. Following the link may show a truncated preview.
> Original article: https://medium.com/embabel/agents-that-extract-and-use-preferences-from-conversations-7b22cca9abb3

## Summary

A hands-on walkthrough of wiring [[Embabel DICE]] into a working chatbot so that preferences stated in conversation are extracted, stored, and injected into later turns. Not the framework's announcement — a practitioner's build, extending the author's earlier Embabel ChatBot (RAG over Lucene-indexed blogs) and following the Embabel team's own *Impromptu* sample.

## The Grounding Gap

The framing is the **grounding gap**: the absence of common ground between the LLM and the user's question. The worked scenario is deliberately mundane — tell the assistant you like posts about agents and Embabel, end the conversation, then ask later that day for something to read on the train. Without stored preference, the second conversation starts from nothing.

The author's point is that the interesting version is domain-specific: allergies when ordering food, a home address when ordering groceries. Common ground is what makes conversations run well, and a system that learns about the user can manufacture it.

## GUM: The Theory Behind It

[[DICE]] is credited to the **General User Models** paper:

> *Creating General User Models from Computer Use* — Omar Shaikh, Shardul Sapkota, Shan Rizvi, Eric Horvitz, Joon Sung Park, Diyi Yang, Michael S. Bernstein — https://arxiv.org/abs/2505.10831

The elements carried into DICE, as the author highlights them:

- Learn from the user's interactions with a computer, rather than asking them to state preferences.
- Observation produces **propositions** about what the user wants to accomplish, each with a **confidence** factor.
- New observations **revise** existing propositions.
- The system **audits** propositions for facts you do not want remembered.
- A **staleness** factor per proposition — some memories should outlive others.

The last one gets the article's best illustration: the difference between where you parked your car and the day you got married.

## Extraction in Practice

Given the input *"I like to watch tutorials about Agents, especially if the speaker uses a bit of humour but clearly knows what he is talking about"*, the extractor returns propositions such as **"User likes to watch tutorials about Agents"** at **90% confidence**, each carrying an **explanation** of why it was proposed — here, that the user explicitly said so.

That explanation field is worth noting: propositions are auditable by construction, not just scored.

## The Extraction Prompt

The extractor's prompt template composes DICE-provided partials (`dice/..._hints.jinja`, `dice/existing_propositions.jinja`) with four explicit extraction rules:

1. **User-centric** — extract facts about the user, not general domain knowledge.
2. **Single fact per proposition** — one subject, one object maximum.
3. **No inference beyond evidence** — only what the text explicitly supports.
4. **No overlap** — each fact distinct.

Worked from *"I want to read blogs about Embabel"*, good propositions look like *"Jettro likes to read blogs"* (no entity mention — period/style) and *"Jettro likes blogs about Embabel"* (entity: Embabel → Product).

The template also teaches the two scores directly:

| | |
|---|---|
| **High confidence** | Explicit statements — "I love reading about AI" |
| **Lower confidence** | Implied preferences — asking many questions about a topic |
| **Low decay** | Stable preferences — favourite topic, category preferences |
| **High decay** | Transient states — the topic currently being written about |

Rule 3 is the operative safeguard against a memory store filling with plausible inventions.

## Architecture

| Component | Role |
|---|---|
| `PropositionPipeline` | Orchestrates extraction and revision; built from an extractor, a reviser and a repository |
| `LlmPropositionExtractor` | Finds propositions in text |
| `LlmPropositionReviser` | Decides whether a proposition is new or an update to an existing one |
| `PropositionRepository` | Stores propositions; the in-memory variant needs an embedding model for similarity search |
| `PropositionPipelineController` | REST endpoint for extracting from supplied text |
| `MemoryController` | List, search, create and delete stored propositions |
| `DataDictionary` | Declares which entities to extract |
| `ChunkHistoryStore` | Prevents re-analysing the same chunk |
| `MemoryProjector` | Projects propositions as semantic (facts), procedural (preferences/rules) or episodic (events) memory |

## Extraction Runs Off the Response Path

The integration detail that matters most: after the agent responds, it publishes a `ConversationAnalysisRequestEvent`. A `ConversationPropositionExtraction` listener picks it up and runs the pipeline. Extraction is therefore **event-driven and out of band** — the user's turn is not blocked on it, the same trade [[django-dice]] later exposes as an explicit inline-vs-background switch.

Memory is then handed to the model as just another reference alongside RAG:

```java
var memory = Memory.forContext(user.getCurrentContext())
        .withRepository(propositionRepository)
        .withProjector(memoryProjector);

context.ai().withLlmByRole(CHEAPEST.name())
           .withReferences(toolishRag, memory)
```

Note the model role: the responding call is bound to `CHEAPEST`, while revision uses `STANDARD` and the repository's embedder a `FAST` role — model tiering by job, configured rather than hard-coded.

## A Worked Run

From the question *"I am really interested in blogs about Embabel. Do you have information about such blogs?"*, the extraction log shows:

```
• Jettro is really interested in blogs about Embabel (conf: 0.98) [NEW]
• Jettro asked for information about blogs about Embabel (conf: 0.95) [NEW]
Entities:
• [NEW] I (KnowledgeUser, __Entity__)
```

Two details worth carrying away. The pronoun **"I" is resolved to a `KnowledgeUser` entity** rather than being discarded. And the author singles out a proposition extracted **from the assistant's response**, not the user's — the system learns from both sides of the conversation, which is a larger surface than "record what the user said about themselves."

## Caveat

The build runs on snapshot dependencies — Embabel `0.3.3-SNAPSHOT` and DICE `0.1.0-SNAPSHOT`, pulled from Embabel's snapshot repository — because the author needed unreleased features. Treat API details here as pre-release.

## References Given

- Impromptu sample (the Embabel team's) — https://github.com/embabel/impromptu
- Embabel framework — https://github.com/embabel/embabel-agent
- DICE — https://github.com/embabel/dice
- This article's sample — https://github.com/jettro/embabel-agent-rag-sample

## Related Concepts

- [[DICE]] — the framework being exercised
- [[Agentic Memory]] — the broader pattern; note the projector's semantic/procedural/episodic split
- [[Context Engineering]] · [[Personalization]] · [[RAG]]

## Related Tools

- [[Embabel DICE]] — the library · [[Embabel]] — the framework it is a module of · [[django-dice]] — an independent Python implementation

## Related People

- [[Jettro Coenradie]]
