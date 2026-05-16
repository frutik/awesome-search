---
type: case-study
company: "[[Canva]]"
articles:
  - "[[Canva Search Pipeline Part I]]"
  - "[[Canva Search Pipeline Part II]]"
topics:
  - "[[Managing a Search Team]]"
concepts:
  - "[[Search Architecture]]"
  - "[[Retrieval Pipeline]]"
people:
  - "[[Stuart Cam]]"
---

# Canva — Search Pipeline Modernization

Canva's search and recommendations team serves ~20,000 requests/second across templates, media, audio, and fonts. Their two-part architecture series documents how organic growth produced a system that blocked all further improvement — and how they replaced it.

## The Problem: Big Ball of Mud

Over several years, four separate search systems grew organically for different content types (templates, media, audio, fonts), each with distinct codebases. The systems coupled query construction to Solr syntax via string manipulation:

```
SolrQuery q = new SolrQuery();
q.setQuery("title:" + userInput + " AND ...");
```

**Consequences**:
- Technology lock-in: impossible to adopt dense vectors or new ML ranking without touching every system
- 50+ unique entry points, each with slightly different behavior
- No shared debugging tooling across systems
- ~80 engineers with no shared mental model of how search worked

**Scale context**: 70% of queries are single words ("cat", "dog"). 20% contain two words. Single-character queries common for CJK. Users rarely engage past position 240.

## The Solution: Componentized Pipeline

New architecture principle: **isolated, stateless, immutable pipeline phases with a shared interface**.

```
Validation & Rewriting
    ↓
Tokenization (locale-specific + semantic)
    ↓
Annotation (NER, language detection, synonyms)
    ↓
Candidate Generation (OpenSearch, Solr, SageMaker — parallel)
    ↓
Feature Extraction (Redis-backed feature stores)
    ↓
Re-ranking (business rules + ML models)
```

**Key design principles**:
- **Isolated components**: no shared state between concurrent steps
- **Stateless execution**: state managed externally (Redis/DynamoDB)
- **Immutable flow**: later steps cannot mutate results of earlier steps
- **Shared interface**: all content type pipelines implement the same abstract interface

## Performance Design

- **Parallel candidate generators** — OpenSearch, Solr, and SageMaker model endpoints run concurrently
- **50ms deadline** — generate as many candidates as possible; hard stop at deadline (graceful degradation over errors)
- **Pagination strategy**: overFetch top 500 for early pages (precision priority); fast execution for deep pages (bot detection and handling)

## Organizational Insight

The design process was collaborative: each engineer tackled an architecture area they cared about; outputs were consolidated into a shared initial design. The team credited the process with producing **a shared mental model** — which they argue is as valuable as the technical architecture itself. Contradictions surface early when everyone's working from the same diagram.

## What to Steal

| Pattern | Application |
|---|---|
| Abstract interface across pipeline variants | Enables A/B testing pipeline variants without separate codebases |
| Deadline-based parallel candidate generation | Graceful latency bound under partial backend failure |
| Stateless components, external state | Horizontal scaling and replay without session coupling |
| Collaborative architecture prototyping | Build shared mental model before code review |
| Overetch + pagination strategy | Separate precision-focused early pages from efficiency-focused deep pages |

## Related Case Studies

- [[Netflix - Content Search Architecture]] — similar federated multi-system challenge
- [[Zalando - Self-DoS via Facet Aggregation]] — architectural decisions under load
- [[Uber Eats - Scaling Search for Food Delivery]] — performance engineering at scale
