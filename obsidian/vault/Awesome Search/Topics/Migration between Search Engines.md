---
type: topic
title: "Migration between Search Engines"
aliases: ["Search Engine Migration", "Platform Migration", "Search Platform Migration"]
tags:
  - topic
  - migration
  - search-platforms
related_concepts:
  - "[[Search Platforms]]"
  - "[[Search Architecture]]"
related_topics:
  - "[[Elasticsearch vs OpenSearch]]"
articles:
  - "[[How I learned Vespa by thinking in Solr]]"
  - "[[Amazon OpenSearch Service now offers AI-assisted migrations]]"
created: 2026-07-01
---

# Migration between Search Engines

Moving a production search workload from one engine to another — [[Solr]] / [[Elasticsearch]] / [[OpenSearch]] / [[Vespa]] — is a recurring, high-risk theme in search engineering. The decisive wins are usually **operational** (shard toil, hot nodes, near-real-time visibility, fleet size) as much as raw relevance, and the hard part is cutting over *live* traffic without regressions.

---

## Challenges

Grouped by where teams actually get stuck. The first four are the ones most under-appreciated at planning time.

### 1. Query & schema translation
- **Query-language rewrite.** Solr's string-based `edismax` request handlers and response structure have no mechanical mapping to Elasticsearch's JSON **Query DSL**. Every query, facet, custom boost, and analyzer chain has to be audited and rewritten — automated translators need manual validation or they silently change relevance.
- **Schema model mismatch.** Solr's explicit `schema.xml` / `solrconfig.xml` vs Elasticsearch/OpenSearch **index templates + mappings**. ES defaults to **dynamic mapping**; you must set `dynamic: strict` up front or the target quietly accepts malformed fields. Mapping changes are **not retroactive** — altering a template doesn't touch live indices, so a rethink means a reindex.
- **Feature-parity gaps.** Solr streaming expressions, certain faceting behaviors, and custom update processors have no direct equivalent on the target and need reimplementation.

### 2. Client, plugin & application-code compatibility
- **Client-library divergence.** Since the 2021 fork, the Elasticsearch and OpenSearch client libraries have drifted enough that application code usually needs rewriting — not just an endpoint swap. Newer ES clients also actively reject connecting to OpenSearch.
- **Plugin availability.** First- *and* third-party plugins must be confirmed to exist and be compatible on the target before you can claim feature parity.
- **Auth/signing changes.** e.g. moving to Amazon OpenSearch Service means AWS SigV4 request signing throughout the client tier.

### 3. Data transfer at scale
- **The reindex API is too slow for big corpora.** monday.com measured ~1 TiB/week via the Reindex API — a projected **half-year for 40 TiB**. Options in rough order of speed/complexity: **snapshot/restore** (fastest, but snapshot compatibility caps out around ES 7.12), **remote reindex** (target pulls from the live source, no source downtime), and **Spark + `opensearch-hadoop`/`elasticsearch-hadoop`** for the largest jobs.
- **Version-skew transformation.** Migrating across several major versions means transforming historic data into the new on-disk/mapping format before it will load.
- **Source-cluster load.** Any pull-based copy competes with live traffic on the source; schedule off-peak and tune scroll size.

### 4. Cutover & consistency
- **Alias-based atomic cutover.** Applications should read/write through **aliases**, never raw index names, so cutover is a single atomic alias flip rather than a redeploy.
- **Dual-write partial failures.** While double-writing to old and new engines, a write can succeed on one and fail on the other. The app must **detect and handle partial write failure**, or the two stores silently diverge.
- **Reconciliation jobs.** Teams run scheduled jobs comparing document counts and field values across old engine, new engine, and the system-of-record (relational DB), alerting on any mismatch; cut reads over only once the mismatch rate holds at zero over a sustained window (shadow-read / dark-launch).

### 5. Operational-model differences
- **State management.** SolrCloud's external **ZooKeeper** vs Elasticsearch/OpenSearch built-in master nodes; **manual** shard/AZ placement vs automatic AZ-aware balancing.
- **Lost tooling & observability.** Familiar admin dashboards disappear; teams must rebuild custom metrics/observability before they can debug the new engine in production.
- **Multi-tenancy paradigm shifts.** Consolidating single-tenant clusters onto a shared managed service forces per-tenant index isolation and access control that didn't exist before.

### 6. Validation, cost & direction
- **Relevance validation.** Prove the new engine matches or beats the old one — typically several A/B iterations (Vinted needed ~4 to reach parity).
- **Migration isn't one-directional.** Teams move ES→OpenSearch (licensing), OpenSearch→ES (Elastic publishes ROI claims for migrating *off* OpenSearch), and ES/Solr→Vespa (ML-native ranking, ops). The right target depends on cost, licensing, and workload — see [[Elasticsearch vs OpenSearch]] and [[Search Platforms]].

## Case studies in this vault

### Hand-built migrations (ES → Vespa)
- [[Vinted - Migrating Search from Elasticsearch to Vespa]] — billion-item, 20k-RPS platform; Lucene-analyzers-in-Vespa as the enabling detail; ~4 A/B iterations to parity.
- [[Kleinanzeigen - Vespa Migration for Homepage Feed]] — the same ES→Vespa move for a personalized homepage feed.
- [[From Elasticsearch to Vespa - Rebuilding the Kleinanzeigen Homepage Feed Part 1]] — the source write-up.

### Tool-assisted / agentic migrations (→ OpenSearch)
- [[Amazon OpenSearch Service now offers AI-assisted migrations]] — AWS Migration Assistant with an agent-guided (Kiro / Claude Code) workflow for Solr/ES/OpenSearch → Amazon OpenSearch; live-traffic capture & replay, now including Solr sources.

### Cross-engine mental mapping (onboarding as migration aid)
- [[How I learned Vespa by thinking in Solr]] — [[Sujit Pal]] maps Solr operations onto Vespa equivalents; the manual analog of what automated assistants try to do.

## External case studies

Real-world write-ups not (yet) processed as full vault notes — kept here for reference.

- **[[Canva]] — Solr → Elasticsearch** ([canva.dev](https://www.canva.dev/blog/engineering/migrating-from-solr-to-elasticsearch-and-their-differences/)). Left self-managed Solr (run since 2014) because it "took a literal team of engineers" to maintain, ZooKeeper added failure points, and Elastic talent is easier to hire. Concrete gotchas: `edismax` strings → JSON DSL, `dynamic: strict` needed to keep structure, non-retroactive template changes, lost visual shard dashboards. Migrated smaller indices first. *(Distinct from the [[Canva - Search Pipeline Modernization]] work already in the vault.)*
- **monday.com — 40 TiB OpenSearch re-partition** ([engineering.monday.com](https://engineering.monday.com/migrating-a-multi-terabyte-opensearch-cluster/)). Reindex API projected >½ year for 40 TiB; switched to **Spark + `opensearch-hadoop`** (export to JSON Lines on S3, then bulk index) → done in **<2 weeks, ~20× faster, ~$215** on four `m7g.xlarge` EMR nodes. Lessons: use the RDD API for schemaless data (DataFrame schema inference breaks), `opensearch.scroll.size` dominates speed/load, parallelism is bounded by node/shard count.
- **Ten Mile Square — gradual DB → Elasticsearch** ([tenmilesquare.com](https://tenmilesquare.com/resources/software-development/migrating-to-elastic-search-a-case-study/)). Migrate incrementally to bound blast radius; while double-writing to Solr and ES, detect and handle **partial write failures**; a **nightly reconciliation job** compares ES vs Solr vs the relational DB and emails the team on any inconsistency.
- **AWS — Elasticsearch on EC2 → multi-tenant Amazon OpenSearch Service** ([aws.amazon.com/blogs/apn](https://aws.amazon.com/blogs/apn/migrating-elasticsearch-on-amazon-ec2-to-modernized-multi-tenant-amazon-opensearch-service-architecture/)). The hard part was the single-tenant → multi-tenant paradigm shift and guaranteeing each customer sees only their own indices.
- **Elastic — ROI of migrating *off* OpenSearch** ([elastic.co](https://www.elastic.co/blog/return-on-investment-migrating-off-opensearch-search-logging)). Vendor-authored counterpoint: migrations run both directions; performance/cost, not just licensing, drives target choice.

## Related Notes

- [[Search Platforms]] — engine landscape and selection
- [[Elasticsearch vs OpenSearch]] — the most common fork-vs-original decision
- [[Search Architecture]] — what changes structurally across engines
- [[Solr]] · [[Elasticsearch]] · [[OpenSearch]] · [[Vespa]] — the engines involved
