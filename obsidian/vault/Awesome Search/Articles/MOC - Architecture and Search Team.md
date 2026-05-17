---
title: "MOC — Architecture and Search Team"
tags:
  - moc
  - search
  - architecture
  - team
created: 2026-05-15
---

# MOC — Architecture and Search Team

Map of content covering search system architecture and the human side of search: team structure, process, and organizational practices.

## System Architecture

### Concepts
- **Concept**: [[Search Architecture]] — end-to-end pipeline: ingestion → retrieval → ranking → serving
- **Concept**: [[Retrieval Pipeline]] — multi-stage retrieve → rerank
- **Concept**: [[Knowledge Graph Search]] — entity graph + vector integration

### Case Studies
- [[Canva Search Pipeline Part I]] — motivation: big ball of mud, 20k rps
- [[Canva Search Pipeline Part II]] — solution: isolated, stateless, immutable phases

- [[Optimizing Search at Uber Eats]] — geosharding (H3), layout optimization, ETD indexing; [[Janani Narayanan]] & [[Karthik Ramasamy]]
- [[The Day Our Own Queries DoSed Us - Zalando Search]] — [[Maryna Kryvko]]; layered architecture; self-DoS via facet aggregation

## Search Team Organization

### Process
### Process
- [[Query Triage - The Secret Weapon for Search Relevance]] — Rubinstein: cross-functional triage meetings
- [[The Launch Review]] — go/no-go decision process for algorithm changes
- [[Search Relevance for Understaffed Teams]] — Turnbull: focus on NOW, not future headcount
- [[Getting Started on Search Relevance for the Understaffed Search Team]] — comprehensive strategy guide for lean teams
- [[Understaffed Search Team]] — topic: high-ROI techniques for resource-constrained teams

### Key Figures in Search Teams
- [[Daniel Tunkelang]] — search leadership, strategy, philosophy
- [[Doug Turnbull]] — search engineering, LTR, understaffed teams
- [[James Rubinstein]] — search product management, measurement
- [[Andreas Wagner]] — searchhub.io, Three Pillars of Search Quality

### Concepts
- [[Search Team]]
## Evaluation and Quality Process

### Tools and Methods
- **Concept**: [[Search Evaluation]] — offline vs. online; judgment-based vs. behavioral
- **Concept**: [[Judgment Lists]] — (query, document, grade) triples
- **Concept**: [[A-B Testing for Search]] — online experimentation
- [[A-B Testing for Search is Different]] — why session-level analysis matters

## Search Team Roles

- **Search Relevance Engineer**: LTR, ranking signals, evaluation harness
- **Search Product Manager**: query triage, launch reviews, business alignment
- **Search Data Scientist**: metric design, experiment analysis, judgment collection
- **Search UX Researcher**: user intent research, usability testing

## Related MOCs

- [[MOC - Search Quality Assurance and Query Understanding]]
- [[MOC - Ranking and Retrieval]]
- [[MOC - Case Studies]]


## Additional Articles — Case Studies & Architecture

- [[Netflix Elasticsearch Indexing Strategy in AMP]] — alias-based index management, mapping design, refresh tuning
- [[Twitter Search Stability and Scalability]] — Earlybird architecture, circuit breakers, real-time indexing at scale
- [[Thoughts about Managing Search Teams]] — combine product+engineering, data-driven, incremental execution
- [[Search Product Management - The Most Misunderstood Role]] — search PM must understand indexing, ranking, and experimentation
