---
type: topic
aliases: ["conferences", "search conferences", "IR conferences", "search events"]
tags: [topic, events, conferences]
website: https://thesearchjuggler.com/conferences/
related_concepts:
  - "[[Hybrid Search]]"
  - "[[ColBERT]]"
  - "[[Late Interaction]]"
  - "[[BM25]]"
  - "[[Dense Embeddings]]"
  - "[[Judgment Lists]]"
  - "[[Search Evaluation]]"
  - "[[Reciprocal Rank Fusion]]"
related_topics:
  - "[[E-commerce Search]]"
  - "[[Search Quality Assurance]]"
  - "[[Conversational and Agentic Search]]"
  - "[[A-B Testing for Search]]"
  - "[[Relevance Program Setup]]"
articles:
  - "[[Hybrid search > sum of its parts? Berlin Buzzwords 2022]]"
  - "[[What Is a Judgment List?]]"
  - "[[What is ColBERT and Late Interaction and Why They Matter in Search?]]"
people:
  - "[[Lester Solbakken]]"
  - "[[Omar Khattab]]"
  - "[[Matei Zaharia]]"
  - "[[Doug Turnbull]]"
  - "[[Daniel Tunkelang]]"
  - "[[Trey Grainger]]"
created: 2026-05-17
---

# Events and Conferences

Industry and academic events where search, information retrieval, NLP, and AI are discussed and published. A practical guide to where the community gathers and what has come out of it.

> Full conference calendar: [The Search Juggler](https://thesearchjuggler.com/conferences/)

---

## Practitioner Events

### Haystack
Open-source search conference (Solr, Elasticsearch, OpenSearch). Practitioner-focused. [[Doug Turnbull]] and the OpenSource Connections community are closely associated with it.

🔗 https://haystackconf.com/

Notable vault connections:
- [[What Is a Judgment List?]] references a Haystack talk on human rater complexity

### Berlin Buzzwords
Open-source data and search conference (Berlin). Strong search engineering track.

🔗 https://berlinbuzzwords.de/

Notable vault connections:
- [[Hybrid search > sum of its parts? Berlin Buzzwords 2022]] — [[Lester Solbakken]] presenting hybrid search: [[BM25]] vs [[Dense Embeddings]] vs learned sparse, fusion strategies. Covers [[Hybrid Search]], [[Reciprocal Rank Fusion]], [[Embedding Fine-tuning]]

### Activate
Lucidworks-organized conference for search applications and practitioners.

🔗 https://www.activate-conf.com/

### Elastic{ON}
Elasticsearch ecosystem conference. Product announcements and engineering talks.

🔗 https://www.elastic.co/elasticon/

### MICES (Mix-Camp E-Commerce Search)
Dedicated e-commerce search conference. Close overlap with [[E-commerce Search]].

🔗 http://www.mices.co/

---



### AI Engineer
Conference series for AI engineering practitioners. Covers LLMs, agents, context engineering, retrieval, and production AI systems.

🔗 https://www.ai.engineer/

**AI Engineer Europe 2026** — London, April 8–10, 2026
🔗 https://www.ai.engineer/europe/2026

Notable vault connections:
- [[Agentic Search for Context Engineering]] — [[Leonie Monigatti]] ([[Elastic]]) workshop on agentic search tool patterns for [[Context Engineering]]; demonstrated semantic search, ES|QL query tool, and shell tool patterns

## Academic Conferences

### SIGIR
ACM flagship Information Retrieval conference.

Notable vault connections:
- [[ColBERT]] published at SIGIR 2020 by [[Omar Khattab]] and [[Matei Zaharia]]
- ColBERTv2 published at SIGIR 2021 — see [[What is ColBERT and Late Interaction and Why They Matter in Search?]]

### SIGIR eCommerce Workshop
E-commerce-specific IR workshop co-located with SIGIR.

🔗 https://sigir-ecom.github.io/index.html
- [2019](https://sigir-ecom.github.io/ecom2019/index.html)
- [2018](https://sigir-ecom.github.io/ecom2018/index.html)
- [2017](http://sigir-ecom.weebly.com/)

Close overlap with [[E-commerce Search]] and [[Query Understanding in Practice]].

### ECIR
European Conference on Information Retrieval.

### TREC
NIST-run evaluation benchmarks and tracks. Directly relevant to [[Search Evaluation]] and [[Judgment Lists]].

### WSDM
Web Search and Data Mining. Industry + academic mix; web-scale retrieval, recommendation, ranking.

### CIKM
Conference on Information and Knowledge Management.

### ACL / EMNLP / NAACL
NLP conferences. Source of foundational work on language models and embeddings. [[BERT]] — the basis for [[ColBERT]], [[Bi-Encoder]], and [[Cross-Encoder]] — originates from this community.

### NeurIPS / ICML / ICLR
Core ML conferences. Source of embedding architectures, [[Learning to Rank]] advances, and LLM research feeding into [[Agentic Search]] and [[RAG]].

---

## Conference Output in This Vault

| Article | Conference | Concepts |
|---|---|---|
| [[Hybrid search > sum of its parts? Berlin Buzzwords 2022]] | Berlin Buzzwords 2022 | [[Hybrid Search]], [[BM25]], [[Dense Embeddings]], [[Reciprocal Rank Fusion]] |
| [[What is ColBERT and Late Interaction and Why They Matter in Search?]] | SIGIR 2020 / 2021 | [[ColBERT]], [[Late Interaction]], [[Bi-Encoder]] |
| [[What Is a Judgment List?]] | References Haystack talk | [[Judgment Lists]], [[Search Evaluation]] |
| [[Agentic Search for Context Engineering]] | AI Engineer Europe 2026 | [[Context Engineering]], [[Agentic Search]], [[RAG]] |

---

## Related

- [[E-commerce Search]] — MICES, SIGIR eCommerce
- [[Search Quality Assurance]] — TREC, Haystack evaluation talks
- [[Conversational and Agentic Search]] — emerging topic at SIGIR and NeurIPS
- [[Books]] — companion reading list
- [[How to Start a Career in Search]] — where conferences fit in a learning path
