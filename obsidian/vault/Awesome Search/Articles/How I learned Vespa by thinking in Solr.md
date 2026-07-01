---
type: article
title: "How I learned Vespa by thinking in Solr"
source: "https://blog.vespa.ai/how-i-learned-vespa-by-thinking-in-solr/"
author: "[[Sujit Pal]]"
published: 2021-02-24
created: 2026-07-01
tags:
  - article
  - vespa
  - solr
  - vector-search
  - ann
  - search-platforms
  - onboarding
concepts:
  - "[[HNSW]]"
  - "[[Dense Vector Retrieval]]"
  - "[[Search Platforms]]"
topics:
  - "[[Migration between Search Engines]]"
companies:
  - "[[Vespa]]"
  - "[[Elsevier]]"
---

# How I learned Vespa by thinking in Solr

[[Sujit Pal]] (Technology Research Director, [[Elsevier]] Labs) documents how he flattened [[Vespa]]'s notoriously steep learning curve by mapping each [[Solr]] operation onto its Vespa equivalent. His thesis: if you already know Solr (or [[Elasticsearch]]), you can get a minimal Vespa MVP running quickly by reasoning through analogies, then pick up Vespa-specific features incrementally once something works.

---

## The Solr → Vespa mental model

The article walks through the full lifecycle of integrating a search platform and gives the Vespa analog for each Solr step.

| Solr operation | Vespa equivalent |
|---|---|
| Install Solr | Install Vespa (Docker image; ~6 GB RAM, ~50 GB disk) |
| Start the server | `docker start vespa` (starts the config server + deployed apps) |
| Check server status | `curl :19071/ApplicationStatus` (HTTP 200 when ready) |
| Create a **core** | Create an **application** (clone from `vespa-engine/sample-apps`) |
| Configure `managed-schema` + `solrconfig.xml` | Configure a whole directory tree: `hosts.xml`, `schemas/*.sd`, `services.xml`, `search/query-profiles/*` |
| Deploy configuration | `vespa-deploy prepare … && vespa-deploy activate` |
| Populate via update endpoint | POST/PUT to the document endpoint `/document/v1/<app>/<doctype>/docid/<id>` |
| Query the index | **YQL** (SQL-like) at `/search/` |
| More Like This (MLT) | `nearestNeighbor` vector search over embeddings |
| Stop the server | `docker stop vespa` (preserves indexes) |
| Delete the core | `docker rm -f vespa` (destroys indexes) |

### Key conceptual mappings

- **Solr core ≈ Vespa application** — but a Vespa application can hold *multiple* physical indexes under one config, whereas a core is a single index.
- **`managed-schema` ≈ `.sd` schema files** — each document type gets its own YAML-like schema. Solr's per-field `indexed`/`stored` flags map to Vespa's `attribute`, `summary`, and `index` field properties. Rank profiles are declared in the `.sd` file and referenced from queries.
- **Solr MLT ≈ `nearestNeighbor` ANN** — Pal retrieves a document's embedding by ID, then runs `nearestNeighbor` (roughly a Solr function query / SQL UDF) against the vector field. The query vector is declared in `query-profiles/types/root.xml`.
- **Convention over configuration** — Vespa's config directory feels Maven-like: structure signals purpose, at the cost of far more files than Solr's two.

## MVP setup

- Test corpus: the **CORD-19** dataset (~300k COVID-19 scientific papers, Allen AI) with precomputed **SPECTER** document embeddings.
- Index fields: paper ID, title, abstract, and the SPECTER vector.
- Two objectives — (1) plain text search on the title, and (2) vector "more-like-this" search via [[HNSW]]-backed approximate nearest neighbors on the SPECTER embedding. See [[Dense Vector Retrieval]].
- Pal wrapped the verbose Docker commands in shell scripts to make them feel like the shorter Solr commands he was used to.

## Takeaway

The steep learning curve is *justified* — Vespa trades simplicity for tensor computation, native ML ranking, and multi-index applications — but analogical onboarding from Solr makes the first MVP tractable. Pal flags Vespa's ML-model ranking and two-phase queries as the next things to explore.

## Related Concepts

- [[HNSW]] — the ANN index behind Vespa's `nearestNeighbor`
- [[Dense Vector Retrieval]] — vector search as MLT replacement
- [[Search Platforms]] — Solr / Elasticsearch / Vespa / OpenSearch selection

## Related Notes

- [[Migration between Search Engines]] — cross-engine mapping as an onboarding/migration aid
- [[ColBERT Comes to Apache Solr]] — another modern-retrieval-on-Solr piece
- [[Vinted - Migrating Search from Elasticsearch to Vespa]] · [[Kleinanzeigen - Vespa Migration for Homepage Feed]] — production ES→Vespa moves
- [[E-commerce Search and Recommendation with Vespa]] — a fuller Vespa application

## People

- [[Sujit Pal]] — author; Technology Research Director, [[Elsevier]] Labs
