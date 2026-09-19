---
type: tool
title: "Langfuse"
aliases: ["langfuse"]
tags:
  - tool
  - observability
  - evaluation
  - llm
  - tracing
website: https://langfuse.com
repo: https://github.com/langfuse/langfuse
created: 2026-09-19
---

# Langfuse

**Langfuse** is an observability and evaluation platform for LLM applications. Applications
emit **traces** made of **observations** (individual generations and spans), and **scores** are
attached to those traces — either by human review or by an automated judge — so that quality can
be tracked over time rather than sampled by hand.

It is offered as a hosted service (`cloud.langfuse.com`) and self-hosted, with Python and
JavaScript SDKs and a public API for reading observations and writing scores back.

---

## Why It Appears in a Search Vault

Langfuse is not a search tool, and nothing here is retrieval-specific. It earns a note because
its trace/score model is the same loop [[Search Evaluation]] runs on — emit the thing that
happened, attach a judgment to it, aggregate — applied to LLM and agent pipelines. Where a
search team keeps [[Judgment Lists]] against queries, an LLM team keeps scores against traces,
and both face [[LLM as Judge]] at the point where volume exceeds human capacity.

For [[RAG]] and agentic search systems the two converge outright: the trace *is* the retrieval
pipeline, and scoring it means judging retrieved passages and final answers together.

## The Scoring Loop

From the worked example in [[Using TypeSafe's Jev for Evals]]:

1. Pull observations for a trace through the API.
2. Run a judge over them to produce a verdict.
3. Write the result back as a **score** on the trace, with supporting detail in the score
   comment.

That article uses [[Jev]] as the judge — one probability per rubric question rather than a
generated label — and notes the practical requirement to **pin the judge's model version**,
since a fixed decision threshold applied to a model that has shifted underneath produces silent
drift in the score history. The same hazard applies to any versioned judge behind a stored
cutoff.

## In This Vault

- [[Using TypeSafe's Jev for Evals]] — [[Annabell Schäfer]]; replacing generative rubric
  verdicts with a calibrated decision model, and the resulting three-band
  act / escalate / discard routing ([[Staged Judging]])

## Related Concepts

- [[Search Evaluation]] — the same measure-and-aggregate loop, on queries instead of traces
- [[LLM as Judge]] — the automated scoring this platform orchestrates
- [[Judgment Lists]] — the search-side equivalent of stored scores
- [[Staged Judging]] — escalation bands over a judge's confidence
- [[Calibrated Relevance Probability]] — what makes a stored threshold portable
- [[Session-Based Evaluation]] — evaluating a multi-step interaction rather than one result
- [[Search Observability]] — the search-side counterpart discipline
- [[RAG]] — the pipeline most often traced this way

## Related Tools

- [[Quepid]] · [[Rated Ranking Evaluator]] · [[Releval]] — relevance-evaluation tooling on the search side
- [[RAGAS]] — RAG-specific evaluation metrics
- [[User Behavior Insights]] — behavioural signal capture rather than judged scores
