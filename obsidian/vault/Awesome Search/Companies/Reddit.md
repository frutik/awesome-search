---
title: Reddit
type: company
tags:
  - company
  - social-media
  - search
website: https://www.reddit.com
created: 2026-06-01
---

# Reddit

Social media and community platform with large-scale search and recommendation infrastructure. Reddit Engineering has published detailed write-ups on their search and ML infrastructure decisions.

- Website: https://www.reddit.com
- Engineering Blog: https://www.reddit.com/r/RedditEng/

---

## Search & ML Infrastructure

Reddit operates at significant scale — their 2025 vector search evaluation covered workloads of 340M+ vectors (Reddit post embeddings at 384 dimensions). Their engineering culture values open-source software, Go as the primary backend language, and reproducible benchmark-driven decisions.

In 2025, Reddit selected **Milvus** as their company-wide vector database for ANN search, replacing fragmented solutions (Vertex AI Vector Search, Apache Solr ANN, Facebook FAISS sidecars).

## People
- [[Chris Fournie]] — Staff Software Engineer; led vector database evaluation

## Articles
- [[Choosing a Vector Database for ANN Search at Reddit]]

## Case Studies
- [[Reddit - Vector Database Selection]]
