---
type: topic
aliases:
  - Quepid custom search API
  - Quepid unsupported engines
  - driving Quepid against any engine
tags:
  - topic
  - evaluation
  - relevance-testing
  - tooling
related_concepts:
  - "[[Search Evaluation]]"
  - "[[Vector Search Evaluation]]"
  - "[[Judgment Lists]]"
  - "[[Multimodal Embeddings]]"
related_topics:
  - "[[Search Quality Assurance]]"
  - "[[Relevance Evaluation Tools Compared]]"
articles:
  - "[[How to Securely Hook Up Quepid to Vespa]]"
  - "[[How to Evaluate Image Search in Qdrant Using Quepid Part 2]]"
people:
  - "[[Charlie Hull]]"
  - "[[Andrew Kornilov]]"
created: 2026-08-10
---

# Quepid Beyond Supported Engines

[[Quepid]] ships native drivers for a handful of engines. Everything else goes through one
generic escape hatch — the **Custom Search API** endpoint type, where Quepid is reduced to an
HTTP client that POSTs a templated query and runs user-supplied JavaScript over the response.

This topic collects what is publicly documented about using that hatch: which engines people have
actually driven, what breaks, and how the mechanism has changed.

---

## What "Officially Supported" Even Means

The answer differs by source, which is itself worth knowing before claiming an engine is unsupported.

| Source | Engines named |
|---|---|
| GitHub repo description | OpenSearch, Elasticsearch, Solr, Vectara, Algolia, Custom Search |
| quepidapp.com | the same, **plus Fusion** (Lucidworks) |
| `splainer-search` (the underlying JS library) | solr, es, os, algolia *(experimental)*, vectara *(experimental)*, searchapi |

The README body itself names no engines — the list above comes from the repository's
description field, which omits Fusion while the marketing site carries it. And
[[Algolia]]/Vectara are marked *experimental* in the implementation even where they read as
first-class elsewhere. [[Vespa]],
[[Qdrant Vector DB|Qdrant]], Typesense and [[Weaviate Vector DB|Weaviate]] appear in none of them.

## The Mechanism

Four parts, configured per endpoint:

- **Endpoint URL** — the engine's query API.
- **Custom headers** — where API keys and bearer tokens ride. Engines requiring mTLS client
  certificates cannot be used as-is.
- **Query template** — a JSON body with a placeholder substituted per test query. Must be valid
  JSON, and the query field is length-capped (~2048 chars).
- **`docsMapper` / `numberOfResultsMapper`** — JavaScript flattening engine hits into Quepid's
  document model (`id`, `title`, `score`) and total count.

## Documented Cases

Only three public write-ups exist. Each hit a different wall, which is what makes the set useful.

### Vespa — the auth wall

[[Charlie Hull]], [[How to Securely Hook Up Quepid to Vespa]]. [[Vespa]] Cloud defaults to mTLS
client certificates, which Quepid cannot present. Resolved by switching the application to
**read-only token authentication**, declared in `services.xml` alongside the existing certificate
client so CLI access survives. Cost: every config change means a full redeploy.

### Qdrant — the query-representation wall

[[Andrew Kornilov]], [[How to Evaluate Image Search in Qdrant Using Quepid Part 2]]. Auth was
trivial; the *query* was the problem. A CLIP embedding is neither human-readable nor short enough
for the query field, and a raw float array breaks JSON template validation. Resolved by injecting
the vector through a **query-option placeholder** (`"vector": "#$qOption.clip##"`) while the
readable query text stays in the query field for raters. Cases generated programmatically via an
[unofficial HTTP API wrapper](https://github.com/frutik/quepid-api-unofficial). Still the only
public vector-native case.

### A .NET in-house API — the earliest instance

[[OpenSource Connections]], May 2022. Predates both of the above and targets a proprietary
in-house API rather than a named engine — the case the hatch was really built for.
*(Unread — the source blog returns 403; details unverified.)*

## Notable Absences

No public write-ups for Typesense, [[Weaviate Vector DB|Weaviate]], Meilisearch, Marqo, Amazon
Kendra, Vertex AI Search, Coveo, Bloomreach, Constructor, Sinequa, Endeca or Elastic App Search.
The pattern is near-certainly used more than it is published; three is the documented count, not
the real one.

## How the Hatch Has Improved

The Custom Search API path has quietly become much less hand-rolled:

- **Mapper Wizard** — generates the mapping JavaScript rather than requiring it by hand, for
  both JSON and HTML responses.
- **Custom headers + basic auth** in the Wizard — the enabling change behind token-based schemes
  like the Vespa one.
- **LLM-generated data mappers** — added explicitly to speed up custom-API onboarding.
- **Server-side HTTP** — an `HttpClientService` consolidating outbound request logic.

The last one is worth checking before repeating the common claim that *Quepid cannot reach
localhost*: a server-side proxy path may reach hosts a browser cannot. Unverified.

## When Not to Use It

The hatch buys an *interactive* judging loop. For batch or CI-shaped evaluation,
[[Rated Ranking Evaluator]] or a plain Pandas script is the better tool — see
[[Relevance Evaluation Tools Compared]].

## Related Concepts
- [[Search Evaluation]] — the practice the hatch exists to serve
- [[Vector Search Evaluation]] — where it is stretched hardest; the Qdrant case lives here
- [[Judgment Lists]] — what a working endpoint lets you build against a non-native engine
- [[Multimodal Embeddings]] — the CLIP vectors that make the query unrepresentable as text

## Related Topics
- [[Search Quality Assurance]] — the parent practice
- [[Relevance Evaluation Tools Compared]] — when Quepid is the wrong tool entirely

## Articles
- [[How to Securely Hook Up Quepid to Vespa]] — the auth-side case
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 2]] — the query-side case

## Tools
- [[Quepid]] · [[Vespa]] · [[Qdrant Vector DB]] · [[Rated Ranking Evaluator]]

## People
- [[Charlie Hull]] — Vespa case
- [[Andrew Kornilov]] — Qdrant / image-search case
