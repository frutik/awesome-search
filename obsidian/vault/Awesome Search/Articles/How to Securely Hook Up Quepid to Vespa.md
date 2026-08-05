---
type: article
title: "How to Securely Hook Up Quepid to Vespa"
source: "https://thesearchjuggler.com/how-to-securely-hook-up-quepid-to-vespa/"
author:
  - "[[Charlie Hull]]"
published: 2026-01-01
created: 2026-07-03
description: "A proof-of-concept for wiring the Quepid relevance workbench to a Vespa Cloud application using read-only token authentication, a Custom Search API endpoint, and JavaScript result mappers — filling Vespa's gap in interactive offline relevance testing."
tags:
  - search
  - search-evaluation
  - relevance
  - blog
concepts:
  - Search Evaluation
  - Judgment Lists
topics:
  - Relevance Program Setup
  - Search Quality Assurance
---

# How to Securely Hook Up Quepid to Vespa

[[Charlie Hull]] ([[The Search Juggler]]) documents a proof-of-concept for connecting [[Quepid]] — the open-source relevance workbench from [[OpenSource Connections]] — to a [[Vespa]] application. Vespa is "hugely flexible and powerful" but approaches search differently from the Lucene-based engines Hull usually works with, and crucially it lacks an easy, *interactive* way to tune queries offline. Quepid fills that gap, but getting the two to talk securely is non-obvious.

> [!note] Companion resource
> Hull also co-presented a Maven "Lightning Lesson" with [[Trey Grainger]] — *Offline search relevance testing with Vespa & Quepid* — covering the same territory in video form.

---

## Why This Matters

Vespa ships some offline evaluation tools in Python, but nothing that gives a relevance engineer a fast, interactive loop over test queries and human judgements. [[Quepid]] provides exactly that for many engines as a free, open-source-backed service — the challenge is that it isn't obvious how to extract the data Quepid needs from Vespa's API, or how to authenticate against a cloud deployment. This is a concrete instance of driving Quepid against a **custom search API** rather than its native Elasticsearch/Solr integrations.

## The Setup

### 1. Vespa Cloud (not localhost)
Quepid cannot connect to a localhost HTTP server, so Hull deployed to **Vespa Cloud** using its free $300 developer credits rather than self-hosting. He used the **Music** example application (5 album documents), deployed via Docker and the Vespa CLI on Windows PowerShell.

### 2. Token authentication (not certificates)
Quepid cannot use Vespa's default self-signed client certificates, so Hull switched to **read-only token authentication**:
- Generate an auth token in the Vespa Cloud console.
- Edit `services.xml` to add a `<clients>` block granting `read` permission to a token client, while keeping certificate-based access for CLI operations via a second client definition.

```xml
<clients>
  <client id="query-token-client" permissions="read">
    <token id="vespaquepid1"/>
  </client>
</clients>
```

### 3. Redeploy on every change
A key gotcha: **every configuration change requires re-deploying the Vespa application.**

```
vespa auth cert -f
vespa deploy --wait 600
vespa feed ../dataset/documents.jsonl
```

### 4. Verify with cURL
Before touching Quepid, Hull confirmed token auth works by querying Vespa with YQL and a `Bearer` token authorization header, checking the JSON response.

### 5. Quepid Custom Search API endpoint
In Quepid he created a **Custom Search API** endpoint holding:
- the Vespa Cloud application URL,
- an `Authorization` header carrying the token (in JSON format),
- JavaScript parsing functions mapping Vespa's response into Quepid's document model:
  - `numberOfResultsMapper` — extracts the total result count,
  - `docsMapper` — transforms Vespa hits into docs with `id`, `title`, `artist`, `year`, and relevance `score`.

### 6. Query with YQL
Quepid sends queries using YQL syntax, with a placeholder token replaced by each test query.

## Future Directions

Hull suggests exploring more complex YQL queries, larger datasets with multiple result documents, and — notably — **exporting Quepid ratings as training data for Vespa's re-ranking**, closing the loop from offline judgement to learned ranking. He reiterates that Vespa lacks built-in offline testing facilities, making Quepid a valuable complementary tool.

---

## Related Concepts
- [[Search Evaluation]] — the offline judgement → metric loop this enables for Vespa
- [[Judgment Lists]] — what you build in Quepid once it's wired up
- [[NDCG]] — the metric you'd score Vespa results against

## Related Articles
- [[Creating Judgement Lists with Quepid]] — the human judging workflow inside Quepid
- [[Why Setting Up Quepid for Vector Search Evaluation Went Wrong]] — the parallel struggle wiring Quepid to a non-Lucene backend
- [[How to Evaluate Image Search in Qdrant Using Quepid Part 2]] — Quepid-as-custom-endpoint against another non-standard engine (Qdrant)
- [[How I learned Vespa by thinking in Solr]] — onboarding to Vespa's API and YQL from a Lucene mindset

## People
- [[Charlie Hull]] — author; [[The Search Juggler]]
- [[Trey Grainger]] — co-presenter of the companion Maven lesson

## Tools
- [[Quepid]] · [[Vespa]]
