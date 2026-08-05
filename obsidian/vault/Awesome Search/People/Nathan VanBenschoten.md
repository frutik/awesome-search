---
type: person
title: "Nathan VanBenschoten"
aliases: ["natevanben", "nvanbenschoten"]
role: "Chief Architect"
affiliation: "turbopuffer"
former_affiliation: "Cockroach Labs"
website: "https://x.com/natevanben"
tags:
  - person
  - search-infrastructure
  - distributed-systems
created: 2026-08-05
---

# Nathan VanBenschoten

Chief architect at [[turbopuffer]], working on scalable vector search. Previously a principal
engineer at Cockroach Labs, working on CockroachDB's **transactions and replication** — specifically
the performance of its transaction, replication, and persistence layers.

That background is worth knowing when reading his search work: the design argument in
[[How to Build a 256 TB Search Index]] is a distributed-transactions argument imported into search
infrastructure. The decision to reject two-phase commit in favour of a single ordered write-ahead log
consumed in parallel by N shards is the reasoning of someone who has paid 2PC's coordination costs in
a database and does not want to pay them again on top of object storage latency.

- X: https://x.com/natevanben
- GitHub: https://github.com/nvb

## Articles in This Vault

- [[How to Build a 256 TB Search Index]] — single-WAL multi-shard design; raising the per-namespace
  ceiling to 256 TB on object storage, and why 2PC was avoided

## Key Contributions

- **Single-WAL multi-shard architecture** for object-storage-native search — total write ordering
  without distributed commit ([[Sharding]], [[Compute-Storage Disaggregation]])
- The argument that ephemeral NVMe caching removes rebalancing as a constraint on shard size

## Related Notes

- [[turbopuffer]] · [[turbopuffer Search DB]]
- [[Compute-Storage Disaggregation]]
- [[Sharding]]
- [[Extreme Search Systems]]
