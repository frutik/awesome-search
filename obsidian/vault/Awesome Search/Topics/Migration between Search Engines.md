---
type: topic
title: "Migration between Search Engines"
aliases: ["Search Engine Migration", "Platform Migration", "Search Platform Migration"]
tags:
  - topic
  - migration
  - search-platforms
  - vector-search
related_concepts:
  - "[[Search Platforms]]"
  - "[[Search Architecture]]"
  - "[[Dense Vector Retrieval]]"
related_topics:
  - "[[Elasticsearch vs OpenSearch]]"
articles:
  - "[[How I learned Vespa by thinking in Solr]]"
  - "[[Amazon OpenSearch Service now offers AI-assisted migrations]]"
created: 2026-07-01
---

# Migration between Search Engines

Moving a production search workload from one engine to another — [[Solr]] / [[Elasticsearch]] / [[OpenSearch]] / [[Vespa]] and, increasingly, dedicated vector databases — is a recurring, high-risk theme in search engineering. The decisive wins are usually **operational** (shard toil, hot nodes, near-real-time visibility, fleet size) as much as raw relevance, and the hard part is cutting over *live* traffic without regressions.

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
- **The reindex API is too slow for big corpora.** At terabyte scale the Reindex API can run on the order of ~1 TiB/week — projecting to many months for tens of TiB. Options in rough order of speed/complexity: **snapshot/restore** (fastest, but snapshot compatibility caps out around ES 7.12), **remote reindex** (target pulls from the live source, no source downtime), and **Spark + `opensearch-hadoop`/`elasticsearch-hadoop`** for the largest jobs.
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
- **Relevance validation.** Prove the new engine matches or beats the old one — typically several A/B iterations (Vinted needed ~4 to reach parity). Compare *actual search results*, not just that documents/vectors moved.
- **Migration isn't one-directional.** Teams move ES→OpenSearch (licensing), OpenSearch→ES (Elastic publishes ROI claims for migrating *off* OpenSearch), and ES/Solr→Vespa or a vector DB (ML-native ranking, ops). The right target depends on cost, licensing, and workload — see [[Elasticsearch vs OpenSearch]] and [[Search Platforms]].

## Migration pathways

Organized by source and target engine. Vault case studies and external write-ups are folded into the pathway they belong to.

### Migrating between Elasticsearch and OpenSearch

The most common move, because it's the same [[Elasticsearch]]/[[OpenSearch]] fork lineage — but the client, plugin, snapshot-compatibility, and SigV4 issues above bite hardest here.

- **Elasticsearch to OpenSearch** (usually licensing-driven):
  - [[Amazon OpenSearch Service now offers AI-assisted migrations]] — AWS Migration Assistant; agent-guided (Kiro / Claude Code) planning, infra, and historical + live-traffic migration.
  - *AWS — Elasticsearch on EC2 → multi-tenant Amazon OpenSearch Service* ([aws.amazon.com/blogs/apn](https://aws.amazon.com/blogs/apn/migrating-elasticsearch-on-amazon-ec2-to-modernized-multi-tenant-amazon-opensearch-service-architecture/)) — the hard part was the single-tenant → multi-tenant paradigm shift and guaranteeing each customer sees only their own indices.
- **OpenSearch to Elasticsearch** (usually performance/cost-driven):
  - *Elastic — ROI of migrating off OpenSearch* ([elastic.co](https://www.elastic.co/blog/return-on-investment-migrating-off-opensearch-search-logging)) — vendor-authored counterpoint; migrations run both directions.

### Migrating from Solr to Elasticsearch or OpenSearch

The classic modernization move off self-managed [[Solr]]. Dominated by query-DSL rewrite, ZooKeeper removal, and `schema.xml` → mappings.

- **[[Canva]] — Solr → Elasticsearch** ([canva.dev](https://www.canva.dev/blog/engineering/migrating-from-solr-to-elasticsearch-and-their-differences/)) — left self-managed Solr (run since 2014) because it "took a literal team of engineers" to maintain, ZooKeeper added failure points, and Elastic talent is easier to hire. Gotchas: `edismax` strings → JSON DSL, `dynamic: strict` to keep structure, non-retroactive template changes, lost visual shard dashboards. Migrated smaller indices first. *(Distinct from the [[Canva - Search Pipeline Modernization]] work already in the vault.)*
- **Ten Mile Square — gradual DB → Elasticsearch** ([tenmilesquare.com](https://tenmilesquare.com/resources/software-development/migrating-to-elastic-search-a-case-study/)) — migrate incrementally to bound blast radius; while double-writing to Solr and ES, detect and handle **partial write failures**; a **nightly reconciliation job** compares ES vs Solr vs the relational DB and emails on any inconsistency.

### Migrating from Solr to Vespa

- [[How I learned Vespa by thinking in Solr]] — [[Sujit Pal]] ([[Elsevier]]) maps Solr operations onto [[Vespa]] equivalents (core ≈ application, `managed-schema` ≈ `.sd`, MLT ≈ `nearestNeighbor`, YQL ≈ SQL). The manual analog of what automated assistants try to do — cross-engine onboarding as a migration aid.

### Migrating from Elasticsearch to Vespa

The heaviest hand-built migrations in the vault; the enabling trick is porting Lucene text analyzers into [[Vespa]] to preserve analysis-config parity.

- [[Vinted - Migrating Search from Elasticsearch to Vespa]] — billion-item, 20k-RPS platform; Lucene-analyzers-in-Vespa as the enabling detail; ~4 A/B iterations to parity; halved server fleet, change-visibility 300s → 5s.
- [[Kleinanzeigen - Vespa Migration for Homepage Feed]] — the same ES→Vespa move for a personalized homepage feed.
- [[From Elasticsearch to Vespa - Rebuilding the Kleinanzeigen Homepage Feed Part 1]] — the source write-up.

### Migrating to a vector database (Qdrant, Weaviate, Milvus, pgvector)

A distinct pathway: usually **augmenting** lexical search with semantic retrieval rather than a like-for-like swap, so it coexists with (or feeds) [[Hybrid Search]]. New failure modes appear that the lexical migrations above don't have.

- **Extra challenges:**
  - **Embedding-model consistency.** Vectors are only comparable if produced by the same model; changing the model means **re-embedding the whole corpus**, not just copying vectors.
  - **Backfill + CDC / dual-write.** Backfill historical embeddings, keep a change-data-capture or dual-write stream to the new store, then flip reads behind a feature flag and keep the old system as fallback (edge cases surface days later).
  - **ANN index & recall shifts.** A baseline captured on pgvector **IVFFlat** (lower recall) can look "better" on [[Qdrant Vector DB|Qdrant]]'s **[[HNSW]]** — validate against ground truth, not the old system's output. Verify all **partitions/shards** migrated, not just the primary table.
  - **Filtered vector search & no BM25.** Payload/metadata filtering semantics differ per engine, and a pure vector DB has no lexical BM25 tier — plan the hybrid story explicitly.
- **Vault notes:** [[Reddit - Vector Database Selection]] · [[Choosing a Vector Database for ANN Search at Reddit]] (Milvus over Qdrant/Vespa/Weaviate/Solr/…) · [[Migrating to Elasticsearch with Dense Vector for Carousell Spotlight]] ([[Carousell]]) · [[Dense Retrieval at Vinted]] · [[Adopting Vespa for Recommendation Retrieval at Vinted]].
- **External write-ups:** *GlassDollar — Elasticsearch → Qdrant* nearing ~10M docs under an agentic query-fan-out workload, and *Sprinklr* reporting ~90% faster writes / ~80% lower latency / 2.5× RPS vs Elastic ([towardsai.net](https://towardsai.net/p/machine-learning/how-to-migrate-from-elasticsearch-to-qdrant-a-complete-guide-with-real-world-solutions)); *pgvector → Qdrant* field notes ([0xhagen on Medium](https://0xhagen.medium.com/migrating-vector-embeddings-from-postgresql-to-qdrant-challenges-learnings-and-insights-f101f42f78f5)); Qdrant's live [migration tool](https://qdrant.tech/documentation/database-tutorials/migration/).

## Related Notes

- [[Search Platforms]] — engine landscape and selection
- [[Elasticsearch vs OpenSearch]] — the most common fork-vs-original decision
- [[Search Architecture]] — what changes structurally across engines
- [[Solr]] · [[Elasticsearch]] · [[OpenSearch]] · [[Vespa]] · [[Qdrant Vector DB]] · [[Weaviate Vector DB]] · [[Milvus Vector DB]] · [[pgvector]] — the engines involved
