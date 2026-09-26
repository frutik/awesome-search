---
type: article
title: "Build an Advanced RAG App: Query Routing"
source: https://dev.to/rogiia/build-an-advanced-rag-app-query-routing-cn1
author:
  - "[[Roger Oriol]]"
published: 2024-09-12
tags:
  - article
  - rag
  - query-routing
  - query-understanding
  - tutorial
concepts:
  - "[[Query Routing]]"
  - "[[RAG]]"
  - "[[Agentic Search]]"
  - "[[Semantic Search]]"
topics:
  - "[[Query Classification]]"
created: 2026-09-26
---

# Build an Advanced RAG App: Query Routing

**Author:** [[Roger Oriol]]
**Source:** https://dev.to/rogiia/build-an-advanced-rag-app-query-routing-cn1
**Published:** 2024-09-12 · DEV Community, part of his *Build an Advanced RAG App* series
**Notebook:** [Google Colab](https://colab.research.google.com/drive/1B1rGvGriKIVe7PMClrMC0z3wMBbsLIYW?usp=sharing)

## Summary

Once a [[RAG]] app has several data sources, or different questions need different kinds of context, it has to choose between one pipeline for everything and one that adapts per query. Oriol's answer is [[Query Routing]]: a module, usually placed after query rewriting and guardrails, that "takes the query from the user and uses it to make a decision on the next action to take, from a list of predefined choices." He presents it as the glue that ties other advanced RAG techniques together — and as the first step toward agents.

## What the Router Chooses Between

- **Different data sources** — e.g. one store about a product, another about return policies. Sources can be vector databases, regular databases or graph databases.
- **Different indexes for the same source** — keyword vs vector index (or both, with the contexts combined), or different retrieval strategies: summaries, sentence window, parent-child. The router can pick by how *specific* the question is.
- **Other tools** — a web search engine, or a service API such as weather forecasting.

Each choice must be implemented first and given a detailed description, because the description is what the router decides on.

## Router Types

- **LLM Selector** — a prompt lists every choice with its description plus the query; the LLM's completion names the path.
- **LLM Function Calling** — each choice is phrased as a tool and the model picks one.
- **Semantic Router** — a few example queries are written per choice; the incoming query is embedded and routed to the choice of its nearest example.
- **Zero-shot classification** — as he describes it, a small LLM fine-tuned on user queries labelled with the correct route, whose only job is to classify; small models are cheaper and good enough for this.
- **Language classification** — routes by the language of the query, detected by an ML classifier or a prompted LLM.
- **Keyword router** — e.g. a query containing "return" goes to the returns source; plain code, no model.

## Single vs Multiple Choice

Some use cases take one path; others need several — a question spanning topics, or one whose answer differs per source — with the results consolidated into a single answer. The router has to be designed for this from the start.

## The Walkthrough

Built with [[LlamaIndex]]. Three options:

1. A vector store of a paper about RAG
2. A vector store of a chicken gyros recipe (Mike Price, tasty.co)
3. A Google Search tool (own API keys)

Documents are chunked and embedded with BGE small, an open-source embedding model, into two vector stores. Each option becomes a Query Engine Tool with a description, and a Router Query Engine uses an **LLM selector** in *single* mode — exactly one tool per query. The RAG question routes to the paper, the ingredients question to the recipe, and a general question to Google Search. The response's `selector_result` shows which tool was chosen and the LLM's reason — a built-in trace of the routing decision.

## Caveats

- The prose announces an LLM function-calling router for the example, but the code described uses an LLM selector.
- His "zero-shot classification" router is fine-tuned on labelled examples, which is not zero-shot in the usual sense; [[Routing in RAG Driven Applications]] describes the same type as assigning a label from a predefined set.
- A toy corpus of two documents; no routing accuracy is measured.

## Related Concepts

- [[Query Routing]] — primary topic
- [[RAG]] · [[Query Understanding]] · [[Query Classification]]
- [[Semantic Search]] · [[Full-Text Search]] — the keyword-vs-vector index choice
- [[Agentic Search]] — "the next stepping stone" after routing
- [[LLM Guardrails]] · [[Query Rewriting]] — the stages that come before the router

## Related Notes

- [[Routing in RAG Driven Applications]] — [[Sami Maameri]]'s near-identical taxonomy, plus logical routers
- [[Query Routing - Direct Queries to the Right Source]] — cascade, multi-route and contextual routing
- [[Andrei Cristea - Qdrant Vector Search and Hybrid Routing]] — a trained router choosing between sparse, dense and fused retrieval
- [[LlamaIndex]] · [[Roger Oriol]]
