---
type: concept
title: "Agentic Memory"
aliases: ["agent memory", "long-term memory", "working memory", "session memory", "memory-based personalization"]
tags:
  - concept
  - agentic-search
  - personalization
  - memory
  - opensearch
created: 2026-09-07
---

# Agentic Memory

## Definition

**Agentic memory** is durable, agent-readable and agent-writable state that persists what a system has learned about a user or a task across turns and sessions. It sits alongside *grounding* — the corpus an agent retrieves from — and answers a different question: grounding says what exists in the world, memory says what this particular user means and wants.

The distinction matters most where the same query must produce different results for different people. A ranking model encodes preference as a learned numeric feature; memory stores it as a fact in language, which can be read, edited, expired, and reasoned over without retraining anything.

## Why Memory Instead of Features

Traditional [[Personalization]] encodes user preference into a [[Learning to Rank|learned ranking model]], a collaborative-filtering signal, or a user vector. All three share two structural weaknesses:

- **They compress away the reason.** A user who buys an orange backpack, returns it, and writes *"too flashy for my work environment, I prefer neutral tones"* teaches a conventional pipeline to decay the colour orange. The actual signal — a *context* (work) and an *alternative* (neutral tones) — is lost.
- **They go stale by construction.** User context is evolutive: students become professionals, single shoppers start buying for babies. Absorbing that means retraining models and explicitly tracking drift in the feature space.

Memory addresses both because it stores the situation rather than a coefficient, and because updating it is a write rather than a training run.

## Memory Types

Two taxonomies are in circulation, and they cut the same material along different axes — one by **lifetime**, one by **kind of knowledge**.

### By stage of processing (OpenSearch)

[[OpenSearch]] exposes four kinds, held together in a **memory container** — the unit that bundles an embedding model, an LLM, the processing strategies, and the namespaces for one use case:

| Type | Holds |
|---|---|
| `sessions` | Conversation sessions and their **metadata** — start time, participants, session state |
| `working` | Active conversation data — recent messages, current context, agent state, **execution traces**, temporary data |
| `long-term` | Processed knowledge and facts extracted over time; with inference on, the LLM promotes insights and preferences here **out of working memory** |
| `history` | An audit trail of memory **operations** — add, update, delete |

The division of labour is easy to get wrong in both directions: recent messages live in `working`, not in `sessions`, which carries only session metadata; and `history` records how memories changed, not what the agent reasoned — execution traces are `working` memory. The axis here is really **stage of processing**: raw material lands in `working` and is promoted to `long-term`, which is what the `infer` parameter controls (`false` by default, storing raw content without LLM involvement).

### By kind of knowledge (Elasticsearch)

The [[Elasticsearch]] write-up borrows the cognitive-psychology split instead:

| Type | Holds | Where it lives |
|---|---|---|
| **Procedural** | How the agent behaves — when to store, when to retrieve, how to summarize, how to use tools | Application code and prompts, **not** the search index |
| **Episodic** | Specific experiences tied to an entity and a context | Documents in the index, with user, role, timestamp and context metadata |
| **Semantic** | Generalized world knowledge independent of any one interaction — a company handbook | Retrieved through the same system with a different strategy |

The useful observation is that **procedural memory is not storage at all** — it is the harness. The two taxonomies overlap on the part that is: episodic memory is roughly what the lifetime view splits into long-term plus session, and semantic memory is closer to conventional [[RAG]] grounding than to per-user state.

Episodic memory is singled out as the most dynamic and personal, and the most prone to context pollution when handled carelessly — which is what motivates isolation.

## Isolation

Per-user memory makes access control a retrieval problem rather than an afterthought. Two positions appear:

- **Enforce in the engine.** The Elasticsearch approach pins a filter onto the memory document's type field inside the *role descriptor*, so credentials decide what is visible and the agent issues the same query either way. Isolation cannot be forgotten in application code because the application is not the thing enforcing it.
- **Scope the agent.** The OpenSearch framing relies on multi-tenancy and access patterns to restrict an agent to the memories it is entitled to read.

OpenSearch's documentation is blunt about where that responsibility sits: agentic memory is a *framework*, and the container's owner is responsible for access control — index-level permissions, document-level security, or equivalent — which it flags as especially critical when `use_system_index` is `false` and memories land in an ordinary index. **Namespaces** (`user_id`, `session_id`, `agent_id`) partition memories and make them searchable per user, but partitioning is not enforcement.

See [[Multi-Tenancy in Search]] for the general version of this problem.

## Storage Strategies

How raw signal becomes a memory entry:

OpenSearch names these as strategies on the container, each scoped to a namespace:

| Strategy | What gets stored |
|---|---|
| `USER_PREFERENCE` | An LLM reasons over a long behavioural history and extracts the preferences as facts |
| `SEMANTIC` | Related memories group by meaning — "I work in consulting" plus "client-facing" collapsing to `professional context consultant client-facing` |
| `SUMMARY` | Many memories compress into a single line — a 20-message session becoming "prefers boutique hotels, vegetarian, this budget per night" |

Strategies are optional; a container can be created without any for plain storage. Entries may be stored as text or as dense vectors for semantic retrieval, and memories are added as either `conversational` messages or structured `data` such as agent state and checkpoints.

## Operational Pattern

The load-bearing architectural decision is to **split inference from serving**:

- **Offline** — behavioural signals ([[User Behavior Insights|UBI]] clickstream, purchases, feedback, favourites) are filtered, aggregated per user, and passed to an LLM that infers preferences and writes them to long-term memory as facts. Low-value events such as hovers are dropped.
- **Online** — the agent *reads* memory, enriches the query, retrieves, and reranks. It does not reason about preferences here.

Practical constraints that follow from that split:

- Write memory **asynchronously** — never on the search path.
- **Cache** the user profile rather than re-retrieving it per query.
- **Cap retrieval** at the top 5–10 facts, scoped to the current context rather than the whole history.
- **Tier the models** — reasoning-capable offline, a small language model online.
- Set a **TTL** so stale context expires as the user changes.
- Keep a **conventional fallback** (lexical, k-NN or hybrid) for when the agent is slow or misbehaves.

Multi-tenancy and access control matter here in a way they do not for a stateless ranker: memory is per-user data, and an agent must be scoped to the memories it is entitled to read.

## Applying Memory to a Query

Retrieved preferences are injected at two points — the [[Query Rewriting|query rewrite]] (`backpack` → `backpack leather neutral professional`) and the [[Reranking|rerank]] step, so that context missed by the rewrite can still be recovered.

Two details worth carrying across implementations:

- **Prefer soft filters to hard filters.** A preference is evidence, not a constraint; promote it to a hard filter only when you know it genuinely binds for that user.
- **Store aversions as affirmatives.** Embedding models handle negation poorly, so "not flashy" is recorded as the positive statement of what the user does want.

## Availability

Agentic memory is documented as **introduced in OpenSearch 3.3**, in the ml-commons plugin, with APIs under `/_plugins/_ml/memory_containers/`. It is built for OpenSearch's own agents and for external frameworks — LangChain and LangGraph are named explicitly.

**Context management** — sliding windows and summarisation to pull the relevant subset out of a long history — is dated to **OpenSearch 3.5** in Bouafif's talk; the reference page above does not cover it, so treat that number as the speaker's.

## Related Concepts

- [[DICE]] — a third taxonomy (semantic/procedural/episodic/working) with scored, decaying propositions, grounded in the domain model instead of an engine-native store
- [[Agentic Memory for Search Personalization]] — the applied topic: building personalized search on memory end to end
- [[Personalization]] — the problem agentic memory is applied to here
- [[Agentic Search]] — the broader agent-driven retrieval pattern
- [[Query Rewriting]] — where memory is applied at search time
- [[Reranking]] — the second injection point for preference context
- [[Learning to Rank]] — the feature-based approach memory is contrasted against
- [[Hybrid Search]] — typical retrieval mode and recommended fallback
- [[RAG]] — semantic/world knowledge, as distinct from per-user memory
- [[Multi-Tenancy in Search]] — isolating one user's memories from another's
- [[Model Context Protocol]] — the tool-access half of an agent's needs

## Tools

- [[OpenSearch]] — four memory types by lifetime, with native memory APIs
- [[Elasticsearch]] — the procedural/episodic/semantic split, with document-level security as the isolation mechanism
- [[User Behavior Insights]] — behavioural signal source for offline preference inference

## Articles

- [[Agentic Memory - OpenSearch Docs]] — the reference: memory containers, the four types, payload types, `infer`, strategies, namespaces
- [[AI Agent Memory - Creating Smart Agents with Elasticsearch Managed Memory]] — [[Gustavo Llermaly]] & [[Jeffrey Rengifo]]; the three-type taxonomy and engine-enforced memory isolation

## Videos

- [[Hajer Bouafif - Personalize Search Results with OpenSearch Agentic Memory]] — [[Hajer Bouafif]] ([[Amazon Web Services]]) at [[Berlin Buzzwords]] 2026
