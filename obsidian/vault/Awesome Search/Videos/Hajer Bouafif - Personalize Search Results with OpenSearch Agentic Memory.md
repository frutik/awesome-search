---
type: video
title: "Personalize Search Results with OpenSearch Agentic Memory"
speaker: "[[Hajer Bouafif]]"
company: "[[Amazon Web Services]]"
medium: talk / video
url: https://www.youtube.com/watch?v=dY_ZuCM2vJw
published: 2026-06-09
conference: "[[Berlin Buzzwords]]"
duration: 20:56
tags:
  - video
  - personalization
  - agentic-memory
  - opensearch
  - query-rewriting
  - e-commerce
topics:
  - "[[Personalization in Search]]"
  - "[[Conversational and Agentic Search]]"
concepts:
  - "[[Agentic Memory]]"
  - "[[Personalization]]"
  - "[[Query Rewriting]]"
  - "[[Reranking]]"
  - "[[Hybrid Search]]"
  - "[[Learning to Rank]]"
tools:
  - "[[OpenSearch]]"
  - "[[User Behavior Insights]]"
people:
  - "[[Hajer Bouafif]]"
created: 2026-09-07
---

# Personalize Search Results with OpenSearch Agentic Memory

📺 **Watch:** https://www.youtube.com/watch?v=dY_ZuCM2vJw

Talk by [[Hajer Bouafif]] (OpenSearch Solutions Architect, [[Amazon Web Services]]) at [[Berlin Buzzwords]], June 2026. The argument: search [[Personalization]] should stop being a feature-engineering problem and become a **memory** problem. Instead of encoding user preferences into a vector space or an [[Learning to Rank|LTR]] feature set — both of which need retraining as the user changes — let an agent read and write durable memory, and let an LLM infer preferences from behavioural history in plain language.

The framing question is not "how do we better rank *black shoes*?" but **"who is running the query, and why are they running it now?"** Three people typing `black shoes` may mean high heels, sneakers, or boots for work.

## Key Moments

| Time | Topic |
|---|---|
| [00:21](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=21s) | The "black shoes" problem — three personas, one query |
| [00:54](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=54s) | Three kinds of context: user, domain, business |
| [01:37](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=97s) | Traditional approaches: collaborative filtering, LTR, user preference vectors |
| [02:09](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=129s) | Why they fall short — the returned orange backpack |
| [03:05](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=185s) | User context is evolutive; retraining and drift |
| [04:06](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=246s) | Agentic query personalization: agents + memory |
| [05:28](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=328s) | OpenSearch's four memory types |
| [06:04](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=364s) | Agentic memory in OpenSearch 3.3; context management in 3.5 |
| [07:22](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=442s) | Three storage strategies: user preferences, semantic, summary |
| [09:17](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=557s) | The offline ingestion pipeline |
| [09:36](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=576s) | What [[User Behavior Insights|UBI]] is, and which signals to keep |
| [11:13](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=673s) | Raw signals → extracted preferences stored as facts |
| [12:21](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=741s) | The online search pipeline |
| [13:26](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=806s) | Soft filters over strong filters; rerank with context |
| [14:05](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=845s) | The asynchronous explanation / judge agent |
| [15:28](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=928s) | Production recommendations |
| [17:51](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=1071s) | Demo: three personas in a marketplace |
| [19:35](https://www.youtube.com/watch?v=dY_ZuCM2vJw&t=1175s) | Aversions rewritten as affirmatives |

---

## The Case Against Feature Engineering

The talk opens on three kinds of context a personalized system might use — **user** (preferences, purchase history), **domain** (healthcare, car parts, marketplaces), and **business** (current priorities, campaigns to push). It then narrows to user context for the rest of the session.

The traditional toolkit is collaborative filtering with product recommendations, trained [[Learning to Rank]] models with hand-built features, or user preferences encoded into a vector space and applied at query time. Bouafif's objection is illustrated with one worked example:

> A user purchases an orange backpack, returns it, and leaves the feedback *"This is too flashy for my work environment. I prefer neutral tones."*

A conventional pipeline decays the orange colour and stops. That loses three things:

- **The reason.** If the user simply disliked orange they would not have bought it. The problem is *flashy for a work environment* — a context, not a colour.
- **The alternatives.** "Neutral tones" is the actionable half of the feedback, and nothing captures what those are.
- **The query stays generic.** All three personas still type the same words.

On top of this, user context is **evolutive**: a student becomes a working professional; someone single starts shopping for a baby. Absorbing that into the traditional approaches means retraining models and explicitly capturing drift in the feature space, while still only ever encoding a numeric feature rather than the situation that produced it.

## Agents and Memory

The proposal is **agentic query personalization**. Agents are dynamic — you give them tools and a harness, and they adapt to change without retraining. But an agent needs two things:

- **Grounding** — the product catalog, PDFs, whatever the domain corpus is.
- **Memory** — described here as the *source of intelligence*: the evolving record of who this user is, which tells the agent what to consider when it rewrites the query.

[[OpenSearch]] ships four memory types out of the box — **long-term, session, history, and working** — with native APIs to add, update and delete memories. Bouafif dates [[Agentic Memory]] to **OpenSearch 3.3**, with **context management** arriving in **3.5** to help the agent retrieve what matters from a long history via sliding windows and summarisation. Memory can be stored as text or as dense vectors for semantic retrieval, and multi-tenancy and access controls scope each agent to the memories it should see.

### Three storage strategies

| Strategy | What gets stored |
|---|---|
| **User preferences** | An LLM reasons over a long behavioural history and extracts the preferences (the approach used in the demo) |
| **Semantic** | Repeated related mentions collapse into one line — "I work in consulting" plus "client-facing" becomes `professional context consultant client-facing` |
| **Summary** | Many memories compress to a single line — a 20-message session becomes "prefers boutique hotels, vegetarian, this budget per night" |

## Two Pipelines

**Offline ingestion** builds the preferences. [[User Behavior Insights|UBI]] clickstream is the input, but Bouafif is explicit that not all of it belongs: filter to the interactions that actually define a profile — **purchases, feedback, favourites** — and drop hover events. Aggregate by user, then write to OpenSearch memory with `infer: true`, and an LLM infers the preferences and stores them in long-term memory **as facts**.

The worked example: raw signals (a purchase, a return, direct feedback *"perfect quality leather classic style"*) become stored preferences — *prefers neutral, dislikes flashy for work environment, values quality leather*. No feature engineering, no training pipelines; the LLM's reasoning absorbs behavioural change as it appears, and the output is regenerated semantic information rather than the raw facts.

**Online search** consumes them. The agent fetches **two** memories: long-term (the preferences) and session (the conversation, so that a follow-up query of `in blue` is understood as *the backpack* in blue). It enriches the query — `backpack` becomes `backpack leather neutral professional` — detects aversions, and runs neural, hybrid or lexical search.

Two design notes from this stage:

- **Prefer soft filters to strong filters**, unless you know a given filter genuinely matters to that user.
- **Feed the preference context to the reranker as well**, to catch anything the rewrite missed.

Asynchronously, an **explanation (or judge) agent** compares the original query, the results served, and the known preferences, and detects mismatches — surfacing a message to the user along the lines of *we don't carry this exact product, so here is what we recommend instead*. The agent also writes to **working memory** (the enriched query and the reasoning behind it), **session memory** (multi-turn context), and **history memory**, which acts as an audit trail of actions and reasoning for later trace analysis.

## Production Recommendations

- **Write memory asynchronously** — never block the search path, or latency suffers.
- **Infer preferences offline**, not at query time.
- **Cache user profiles** — don't re-retrieve preferences on every keystroke of a session.
- **Limit retrieval to the top 5–10 facts**, scoped to the current context rather than the user's whole history.
- **Use tiered models** — reasoning-capable models for offline ingestion, a small language model (SLM) online, where the actions are already known and deep reasoning is unnecessary.
- **Set a memory TTL** so stale context expires as the user changes.
- **Always have a fallback strategy** — lexical, k-NN or hybrid search — for when the agent is too slow or behaves unexpectedly. Emphasised as the single most important item.

## Demo

A marketplace with three personas: an anonymous user (no personalization), **Sara** (young working professional) and **Alex** (student). For the query `shoes`, the anonymous user's OpenSearch query is just `shoes`. Sara's is rewritten to **`shoes leather lace-up neutral black tan brown understated`**, with *strong* filters on category and gender — chosen deliberately because category and gender affinity are judged important for that user — and the inferred attributes fed to the rerank model as well.

One detail worth isolating: **semantic aversions are stored as affirmatives, not negations**, because embedding models handle negation poorly. Rather than encoding "not flashy", the system translates the aversion into the positive statement of what the user does want.

## Related Concepts

- [[Agentic Memory for Search Personalization]] — the topic this talk anchors
- [[Agentic Memory]] — the mechanism the talk is built on
- [[Personalization]] — the problem being solved; this is the memory-based approach to it
- [[Query Rewriting]] — how preferences are actually applied at search time
- [[Reranking]] — the second place preference context is injected
- [[Hybrid Search]] — one of the retrieval modes, and part of the recommended fallback
- [[Learning to Rank]] — the feature-engineering approach being argued against

## Tools

- [[OpenSearch]] — agentic memory and context management (dated in the talk to 3.3 and 3.5), and the retrieval stack
- [[User Behavior Insights]] — the behavioural signal source feeding offline inference

## People

- [[Hajer Bouafif]] — speaker; OpenSearch Solutions Architect at [[Amazon Web Services]]
