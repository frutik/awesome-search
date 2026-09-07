---
title: Embabel
type: tool
aliases: ["embabel-agent", "Embabel Agent Framework"]
tags:
  - tool
  - agent-framework
  - java
  - kotlin
  - jvm
  - context-engineering
website: https://github.com/embabel/embabel-agent
repo: https://github.com/embabel/embabel-agent
created: 2026-09-07
---

# Embabel

An **agentic AI framework for Java and the JVM**, created by Rod Johnson, founder of the Spring Framework. [[DICE]] ships as a module of it, and [[Embabel DICE]] is that module's implementation.

- Framework: https://github.com/embabel/embabel-agent
- DICE module: https://github.com/embabel/dice
- Impromptu (reference sample): https://github.com/embabel/impromptu

---

## Shape of the API

From the worked example in [[Agents That Extract and Use Preferences from Conversations]], the programming model is annotation-driven in the Spring idiom:

- `@Action` methods, optionally with `canRerun` and a `trigger` type, run in response to typed events such as a `UserMessage`.
- An `OperationContext` / `ActionContext` carries process state, including the identity of the user the process is bound to.
- LLM calls are composed fluently — `context.ai().withLlmByRole(...).withReferences(...).withSystemPrompt(...).respond(...)`.

**Models are selected by role, not by name.** The sample binds the responding call to a `CHEAPEST` role, proposition revision to `STANDARD`, and the embedder to `FAST`, with the mapping configured in `application.yml`. That is model tiering as a first-class configuration concern — the same discipline [[Agentic Memory for Search Personalization]] argues for, expressed in the framework rather than bolted on.

References — RAG sources, memory — are passed to a call as a list, so agent memory enters the prompt through the same mechanism as retrieved documents.

## Related Tools

- [[Embabel DICE]] — the DICE module: proposition extraction, entity resolution, memory projection
- [[django-dice]] — an independent Python implementation of the same DICE design

## Related Concepts

- [[DICE]] · [[Agentic Memory]] · [[Context Engineering]] · [[RAG]]

## Articles

- [[Agents That Extract and Use Preferences from Conversations]] — [[Jettro Coenradie]]; a chatbot built on Embabel with DICE preference extraction wired in
