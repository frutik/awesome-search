---
title: "Survey of the (Hybrid) Search Landscape"
aliases: ["Hybrid Search Blueprint Part 1", "Survey of the Hybrid Search Landscape"]
type: article
source: "https://medium.com/mongodb/survey-of-the-hybrid-search-landscape-a5477115f6a8"
author:
  - "[[Erik Hatcher]]"
company: ["[[MongoDB]]"]
published: 2025-04-01
created: 2026-07-30
tags:
  - article
  - hybrid-search
  - search-analytics
  - lexical-search
  - vector-search
  - mongodb
  - medium
concepts:
  - Hybrid Search
  - Reciprocal Rank Fusion
  - Relative Score Fusion
  - Dense Vector Retrieval
  - Full-Text Search
  - Matryoshka Embeddings
  - Vector Quantization
  - Click Signals
  - Implicit Judgments
  - Autocomplete
  - Search Architecture
topics:
  - Search Observability
  - E-commerce Search
  - Search UX
---

# Survey of the (Hybrid) Search Landscape

**[[Erik Hatcher]]** ([[MongoDB]]) opens the Hybrid Search series with a survey of the findability
landscape: what techniques exist, how they differ in *rankability*, and how search-centric
applications have historically combined them. The technical mechanics are deliberately deferred —
what this article establishes is the discipline that makes combining anything worthwhile.

First article in the series:
1. This article — survey of the landscape
2. [[Reciprocal Rank Fusion and Relative Score Fusion]] — RRF and RSF in detail
3. [[Hybrid Search Blueprint Series Semantic Boosting]] — [[Semantic Boosting]]

---

## Hybrid search, a definition

Hatcher offers a working definition drawn from experience rather than the literature:

> combining two or more search techniques to produce results better than any single technique alone.

The load-bearing word is **better**. Combining techniques is only justified if the combination
outperforms the parts, and the only way to know is to measure — which yields the mantra repeated
throughout the series.

He frames the whole exercise pragmatically: there is a lot of low-hanging fruit, and one can go a
long way just by turning on search and doing basic queries, or by vectorizing content and queries
for instant semantic findability. The recurring check is *"Is the juice worth the squeeze?"* — the
ability to over-engineer is not a reason to.

## Measure, tune, repeat

There is no single best metric for what makes one result better than another. Hatcher contrasts two
poles: [[E-commerce Search|e-commerce]], highly dynamic and subjective, where the ultimate business
metric is profit; and library search, more static and objective, where subject matter experts would
mostly agree on the best results for a given query.

His starting practice, before any tuning:

- **Log the queries** — with context: timestamp, number of results presented, and user details to
  whatever level is available and permitted. Sometimes the document IDs returned are logged too,
  since the result set changes over time and can be useful for auditing; the top ~20 shown at a time
  are tractable to log.
- **Log what users do with the results** — clicks, *including the position the result was at when
  clicked*, plus downstream actions like add-to-cart or purchase. What to capture is entirely
  application-dependent: what would be useful implicit feedback in your environment?
- **Analyze the query logs** — which queries found nothing, which are most popular, what a user tried
  in a session before landing on a chosen result. Can you learn from the query trail before the goal?

Only once basic search analytics are in hand does parameter tuning begin: adjust, measure against
the previous results, keep improvements, revert regressions.

## Search techniques, ordered by rankability

Three basic technologies, presented in order of **rankability** — the ability of the query-document
relationship to be given a numerical rank or score.

### Key/value matching

The most basic query: exact field values, served by the database's built-in **B-Tree index**. The
same structure serves range queries (e.g. a `published_date` within the last three months). A
document either matches or it doesn't — no explicit scoring or ranking. Proximity can still be
computed (how close `published_date` is to now), or documents can carry their own ranking value.

### Vector search

Vectors from an embedding model give semantic similarity: documents about the same topics sit close
together in a hyper-dimensional space, the query is embedded into the same space, and a geometric
distance measure indicates closeness.

The **embedding model choice is the primary relevancy factor**. Models vary in representational
capacity and technique — [[Matryoshka Embeddings]] and quantization awareness buy lower-dimensional
and faster calculations plus reduced storage while retaining meaning (see [[Vector Quantization]]).

This is precisely why the "measure" half of the mantra matters: you are entrusting your users'
search success to what Hatcher calls the **embedding black box**, so evaluating that results are as
expected is non-optional.

### Lexical search

Ligatures, diacritics, synonyms, elisions, Unicode, stems, acronyms — words matter, yet typos
happen. How do you find *"the most popular snorkling gear"* when the most important word in the
query is misspelled? Finding needles in haystacks needs a dictionary, or three.

Documents are ranked on how well they match, as precisely or as loosely as is sensible: blending
matches across fields and their particular dictionaries, attaching weights or formulas to query
clauses, and factoring in document statistics (term frequency) and corpus-level statistics
(document frequency). See [[Full-Text Search]] and [[BM25]].

Sweet spots Hatcher highlights:

- **As-you-type suggest** — with a few characters and some context, the user finds what they want
  and has already acted on it. See [[Autocomplete]].
- **Part numbers and similar codes** — SKUs, years, makes, models. Users enter them in a form
  slightly different from the canonical value; a spurious dash shouldn't block them.
- **Voice-to-text queries** — the transcription carries the important terms but may be garbled, with
  spurious rambling attached. Fuzzy lexical matching plus typical or domain synonyms catches many
  mangled queries.

But he is explicit about the limits: it is *just* lexical matching. It isn't the tool for true
semantic search, and it's overkill for exact-value-only matching.

## Historical "hybrid search"

Before vector fusion, hybrid meant something broader — Hatcher treats "hybrid" as a philosophy or
mindset of blending rather than a prescriptive recipe.

A search system shouldn't be an island. **Implicit contexts** are factors like time of day, device
type, location where available, and language settings. **Explicit feedback** includes the items a
user interacts with, the activity type performed on them (add-to-cart, purchase, read-detail, save
to favorites), the session behavior trail, and — notably — what a user was presented but did *not*
interact with.

The loop:

1. Collect **signals** — any bits of information users provide via queries, clicks, and interactions.
2. **Learn from the signals** — ML jobs aggregate raw signals into actionable insights.
3. At query time, **look up** insights available for this user, search context, or query, and
   **augment** the search engine request with the relevant actions.
4. **Log** the query and its contextual information.

Concrete insights he gives:

- A user searches `blue shoez`; learned spell correction internally rewrites it to `blue shoes` from
  there onward. See [[Spelling Correction in Search]].
- Previous `blue shoes` queries led to purchases of Product #3748, so that product ID is boosted in
  the main query. See [[Results Boosting]].
- Desktop app users see several additional facets versus mobile users — a manual rule set up by
  online experience managers.

The synergy is the whole being greater than the sum of the parts: feedback loops that learn from
system activity and feed useful insights back in.

## Hybrid fusion techniques

With vector-based semantic matching on the rise, and lexical search bringing in otherwise-missing
but potentially highly relevant content, it is now common practice to embed the query, issue both a
vector search and a lexical search, and **fuse** the two result sets.

Conceptually it's zipping two result sets together. [[Reciprocal Rank Fusion]] (RRF) and
[[Relative Score Fusion]] (RSF) are the popular mechanisms — blending by relevancy *order* (ignoring
the actual computed distance or relevancy scores), or by sorting on sensible score range
normalizations. Detailed in [[Reciprocal Rank Fusion and Relative Score Fusion]].

## The 747 cockpit

Hatcher's analogy for the tuning surface: knobs, dials, levers, meters, displays, graphs, buttons,
pedals, status indicators, buzzers, and additional computers (agents). There is no one right setting
for every condition — settings change in response to the current environment. Even in autopilot, the
computer makes minute adjustments constantly to keep things smooth.

## Beyond the ranked list

The hybrid search challenge is more than producing a single good result set. What matters is what
the user does with it, and that depends on how they arrive at it: **presentation, format, facets and
navigation** affect the overall experience immensely. Can the user find what they want in a few
taps? Can they navigate sensibly despite their typos? Is the system understanding their
information-seeking intent and making good use of all the implicit and explicit signals? Is
information **ambiently findable**?

## Related Concepts

- [[Hybrid Search]] — the family this article defines and surveys
- [[Reciprocal Rank Fusion]] — fusion by relevancy order
- [[Relative Score Fusion]] — fusion by normalized score range
- [[Semantic Boosting]] — the series' third technique
- [[Full-Text Search]] — the lexical leg
- [[Dense Vector Retrieval]] — the semantic leg
- [[Matryoshka Embeddings]] — cited for lower-dimensional, faster embeddings
- [[Vector Quantization]] — quantization awareness for reduced storage
- [[Click Signals]] — the raw material of the signals loop
- [[Implicit Judgments]] — implicit feedback derived from behavior
- [[Autocomplete]] — a named lexical sweet spot
- [[Results Boosting]] — how learned insights re-enter the query
- [[Search Architecture]] — the surrounding system

## Related Articles

- [[Reciprocal Rank Fusion and Relative Score Fusion]] — part 2 of this series
- [[Hybrid Search Blueprint Series Semantic Boosting]] — part 3 of this series
- [[RRF is Not Enough]] — a sharper critique of rank-only fusion
- [[Hybrid search > sum of its parts? Berlin Buzzwords 2022]] — tests the "better than the parts" claim

## Related Topics

- [[Awesome Search/Topics/Search Observability|Search Observability]] — the logging and analytics practice this article prescribes
- [[E-commerce Search]] — his example of a dynamic, subjective relevance environment
- [[Search UX]] — presentation, facets and navigation as part of findability

## People

- [[Erik Hatcher]]

## Companies

- [[MongoDB]]
