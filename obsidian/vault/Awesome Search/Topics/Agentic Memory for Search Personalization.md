---
type: topic
title: "Agentic Memory for Search Personalization"
aliases: ["Agentic Memory for Search Personalisation", "memory-based personalization", "memory-driven personalization"]
tags: [topic, agentic-memory, personalization, agentic-search, query-rewriting, opensearch, elasticsearch]
related_concepts: [Agentic Memory, Personalization, Query Rewriting, Reranking, Learning to Rank, Hybrid Search]
related_topics: [Personalization in Search, Conversational and Agentic Search, Multi-Tenancy in Search]
articles:
  - "[[Agentic Memory - OpenSearch Docs]]"
  - "[[AI Agent Memory - Creating Smart Agents with Elasticsearch Managed Memory]]"
  - "[[Hajer Bouafif - Personalize Search Results with OpenSearch Agentic Memory]]"
companies: [Amazon Web Services, Elastic]
people: [Hajer Bouafif, Gustavo Llermaly, Jeffrey Rengifo]
created: 2026-09-07
---

# Agentic Memory for Search Personalization

Personalizing search has traditionally meant training something: a [[Learning to Rank|ranking model]] with user features, a collaborative-filtering signal, a user embedding. [[Agentic Memory]] proposes a different substrate — store what you know about the user as **language**, let an LLM write it and read it, and apply it at query time. This topic covers what that buys you, what it costs, and what it still doesn't answer.

The distinction from [[Personalization in Search]] is one of mechanism, not of goal: same problem, different place to put the user model.

---

## The Case Against Features

The argument turns on a single worked example. A shopper buys an orange backpack, returns it, and writes *"too flashy for my work environment, I prefer neutral tones."*

A feature-based pipeline learns to decay the colour orange. Two things are lost:

- **The reason.** Someone who disliked orange would not have bought it. The operative signal is a *context* — work — not a colour.
- **The alternative.** "Neutral tones" is the actionable half of the feedback and has nowhere to live.

Compounding this, user context is **evolutive**: students become professionals, single shoppers start buying for infants. Absorbing that into a learned model means retraining and explicitly tracking drift. Absorbing it into memory is a write.

The counter-argument deserves equal billing: a ranking model is *measurable* and *cheap at serving time*, while an LLM in the loop is neither by default. Most of the engineering below exists to claw those two properties back.

## The Two-Stage Pipeline

The load-bearing architectural decision is to **split inference from serving**. Nearly every practical constraint follows from it.

**Offline — build the profile.**

1. Collect behavioural signal. [[User Behavior Insights|UBI]] clickstream is the natural source in an OpenSearch stack.
2. **Filter to what defines a profile** — purchases, explicit feedback, favourites. Drop hovers and other low-intent events.
3. Aggregate per user.
4. Pass to an LLM with inference enabled, which extracts preferences and writes them as facts to long-term memory.

Raw signals such as a purchase, a return, and the feedback *"perfect quality leather classic style"* become stored statements: *prefers neutral, dislikes flashy for work environments, values quality leather*.

**Online — apply it.**

1. Read the user's stored preferences, plus session state for follow-up resolution.
2. Enrich the query — `backpack` becomes `backpack leather neutral professional`.
3. Retrieve ([[Hybrid Search|hybrid]], lexical, or vector).
4. Rerank, with the same preference context supplied again.

The agent does **not** reason about preferences online. That is the whole point of the split.

## Where Preference Enters the Query

Three insertion points, in increasing order of how much damage they do when wrong:

| Point | Effect | Guidance |
|---|---|---|
| [[Query Rewriting]] | Adds preference terms to the query | The default; cheap and recoverable |
| [[Reranking]] | Re-orders using preference context | Catches what the rewrite missed |
| Filters | Removes documents outright | **Prefer soft over hard.** A preference is evidence, not a constraint |

A hard filter promotes an inference to a fact. Reserve it for attributes you know bind for that user — category and gender affinity are the cited examples — and let everything else be a boost.

One non-obvious detail: **store aversions as affirmatives**. Embedding models handle negation poorly, so "not flashy" is recorded as the positive statement of what the user does want. Anyone building this on dense retrieval will hit that.

## Two Implementations, Two Taxonomies

The same idea, cut along different axes — worth knowing which one a given document means.

| | [[Agentic Memory - OpenSearch Docs\|OpenSearch]] | [[AI Agent Memory - Creating Smart Agents with Elasticsearch Managed Memory\|Elasticsearch]] |
|---|---|---|
| **Axis** | Stage of processing | Kind of knowledge |
| **Types** | `sessions`, `working`, `long-term`, `history` | Procedural, episodic, semantic |
| **Unit** | Memory container (embedding model + LLM + strategies + namespaces) | Index with a multi-field `memory_text` |
| **Promotion** | `working` → `long-term` when `infer` is true (off by default) | LLM converts an exchange into a structured record on write |
| **Retrieval** | Strategy-driven (`SEMANTIC` / `USER_PREFERENCE` / `SUMMARY`) | [[Hybrid Search\|Hybrid]] keyword + [[ELSER]], fused with [[Reciprocal Rank Fusion\|RRF]] |
| **Isolation** | Namespaces partition; access control left to the operator | Role descriptor filters on `memory_type`; the engine enforces |

The taxonomies partly reconcile: episodic memory covers roughly what OpenSearch splits into `long-term` plus `sessions`, semantic memory is closer to ordinary [[RAG]] grounding than to per-user state, and **procedural memory is not storage at all** — it is the harness.

## Isolation Is a Retrieval Problem

Per-user memory turns access control into part of the query path, and the two implementations take opposite positions on who enforces it.

Elasticsearch pins the filter into the **role descriptor**, so credentials decide which memories exist and the agent issues the same query either way — isolation cannot be forgotten in application code, because application code is not what enforces it. OpenSearch supplies **namespaces** (`user_id`, `session_id`, `agent_id`) for partitioning and states plainly that access control remains the operator's job — index permissions, document-level security — flagged as especially critical when memories land outside a system index.

The general lesson: **partitioning is not enforcement**. See [[Multi-Tenancy in Search]].

## Operating It

Constraints that follow from putting an LLM anywhere near a search path:

- **Write memory asynchronously.** Never on the query path.
- **Cache the user profile.** Don't re-read preferences on every keystroke of a session.
- **Cap retrieval at the top 5–10 facts**, scoped to the current context rather than the whole history.
- **Tier the models** — a reasoning-capable model offline, a small language model online, where the actions are already known.
- **Set a TTL.** Preferences go stale as users change.
- **Keep a conventional fallback** — lexical, k-NN or hybrid — for when the agent is slow or misbehaves. Cited as the single most important item.

An asynchronous judge agent can compare query, results and known preferences after the fact, detect mismatches, and surface an explanation to the user rather than silently serving a poor list.

## Failure Modes

- **Context pollution.** Episodic memory is the most dynamic and personal, and the most prone to accumulating junk that later degrades retrieval.
- **Over-constraining.** Hard filters built from inferred preference remove correct results invisibly.
- **Negation.** Aversions stored as negations retrieve badly under dense models.
- **Silent staleness.** Without a TTL, a preference from a prior life stage keeps applying.
- **Latency creep.** Every synchronous LLM call is on the user's clock.

## Open Questions

These are not settled by the material here, and are flagged rather than answered:

- **Evaluation.** [[Search Evaluation]] assumes a fixed relevance judgment per query; per-user rewriting means the "correct" result set differs by user, and none of the sources describes an offline measurement approach for it.
- **Cold start.** The offline stage needs behavioural history that a new user does not have. See [[Personalization in Search]] for the general treatment.
- **Memory compression.** Named explicitly as an open problem and left unimplemented.
- **Attribution.** When a rewritten query underperforms, nothing here separates a bad preference from a bad rewrite from a bad retrieval.

## Implementation Checklist

- [ ] Decide which behavioural events define a profile — and which to discard
- [ ] Put preference inference offline; never at query time
- [ ] Choose insertion points: rewrite, rerank, and only then filters
- [ ] Default filters to soft; justify every hard one
- [ ] Store aversions as affirmatives if anything downstream embeds the query
- [ ] Decide who enforces isolation — the engine or your code — and write it down
- [ ] Set a TTL and a retrieval cap before launch, not after
- [ ] Build the non-agentic fallback path first
- [ ] Decide how you will know this is working at all

## Further Reading

- [[DICE]] — the same convergence reached from conversational agents; scored propositions, decay, bounded injection
- [[django-dice]] · [[Embabel DICE]] — two implementations, with an explicit inline-vs-background extraction trade
- [[Agentic Memory]] — the mechanism itself
- [[Agentic Memory - OpenSearch Docs]] — containers, memory types, strategies, namespaces
- [[AI Agent Memory - Creating Smart Agents with Elasticsearch Managed Memory]] — [[Gustavo Llermaly]] & [[Jeffrey Rengifo]]; engine-enforced isolation
- [[Hajer Bouafif - Personalize Search Results with OpenSearch Agentic Memory]] — [[Hajer Bouafif]] at [[Berlin Buzzwords]] 2026; the applied pipeline and production guidance
- [[Personalization in Search]] — the broader problem, including bandits, cold start and filter bubbles
- [[Conversational and Agentic Search]] — multi-turn context, of which session memory is one piece
- [[User Behavior Insights]] — the signal source feeding offline inference
- [[Multi-Tenancy in Search]] — isolation as a general problem
