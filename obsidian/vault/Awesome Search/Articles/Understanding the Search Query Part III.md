---
title: "Understanding the Search Query — Part III"
source: "https://sonusharma-mnnit.medium.com/understanding-the-search-query-part-iii-a0c5637a639"
author:
  - "[[Sonu Sharma]]"
published: 2019-02-11
created: 2026-05-15
description: "Covers Docker and Kubernetes deployment strategies for a search query understanding system with containerized ML model serving."
tags:
  - clippings
  - medium
---

# Understanding the Search Query — Part III

## Docker Deployment

Two containers communicate over a bridge network (172.16.0.0/16):

| Container | Image | Port | IP |
|---|---|---|---|
| Crocodile Model | `crocodile-model:latest` | 8501 | 172.16.0.2 |
| Service Orchestrator | `service` | 8080 | 172.16.0.3 |

The orchestrator consumes the Crocodile model's REST API, applies business logic (query normalization, dimension detection), then returns responses.

## Kubernetes Orchestration

Scaled using deployment manifests:
- **Replicas**: 2 for redundancy
- **Resource limits**: 2GB memory, 1 CPU per container
- **Resource requests**: 512MB memory, 0.5 CPU per container
- **Persistent Volume**: Attached for data retention across pod replicas

Traffic management via Istio Ingress VirtualService for routing and load distribution.

Health monitoring via liveness and readiness probes — orchestrator exposes `/healthz` endpoint.


## Related Concepts

- [[Query Understanding]]
- [[Search Architecture]]

## People

- [[Sonu Sharma]]
