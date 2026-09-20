---
type: index
title: "Tools"
aliases: ["search tools", "Tools Index"]
tags: [index, moc, tools]
created: 2026-06-19
---

# Tools

The software landscape for building and evaluating search — engines, vector databases, ranking libraries, query tuning, and Postgres-based options. Compare platforms in [[Search Platforms]].

## Search engines
- [[Elasticsearch]]
- [[OpenSearch]]
- [[Solr]]
- [[Manticore Search]]

## Vector databases
- [[FAISS]] — library (not a DB): reference ANN index implementations
- [[Milvus Vector DB]]
- [[Pinecone Vector DB]]
- [[Qdrant Vector DB]]
- [[Weaviate Vector DB]]
- [[turbopuffer Search DB]] — object-storage-native; index lives in S3/GCS with a local cache hierarchy

## Learning to Rank & models
- [[RankLib]]
- [[Metarank]]
- [[XGBoost]]
- [[LightGBM]]
- [[CatBoost]]
- [[ONNX]] — model interchange format and runtime for serving ranking/embedding models
- [[Jev]] — structured-decision model usable as a calibrated reranker, with no ranking training
- [[hev-rerank]] — minimal open-source reranker wrapper around [[Jev]]

## Query tuning & evaluation
- [[Querqy]] — rules-based query rewriting
- [[Quepid]] — judgment lists and relevance measurement
- [[Search Relevance Workbench]] — OpenSearch-native relevance evaluation (query sets, judgments, experiments)
- [[User Behavior Insights]] — open standard (UBI) + engine plugins for capturing queries and the user events that follow them
- [[Elasticsearch Relevance Studio]] — Elastic's experimental agentic relevance-engineering tool
- [[Rated Ranking Evaluator]] — CI/CD-oriented offline evaluation library for Solr/Elasticsearch (Sease)
- [[ann-benchmarks]] — the standard recall-vs-QPS comparison across ANN implementations; blind to indexing cost and CRUD support
- [[eland]] — Python/ML interface for Elasticsearch
- [[Releval]]
- [[OpenSearch Relevance Agent]]
- [[Langfuse]] — LLM/agent tracing with judged scores attached to traces
- [[Jevals]] — confidence-gated eval framework graded by a calibrated decision model

## Postgres-based search
- [[PostgreSQL]]
- [[pgvector]]
- [[pgvectorscale]]
- [[pg_trgm]]
- [[pg_textsearch]]
- [[psql_bm25s]]
- [[VectorChord]]
- [[ParadeDB]]

## Embedding training & fine-tuning
- [[Sentence Transformers]] — the standard library for training bi-encoders, cross-encoders, and (v5+) sparse encoders
- [[qdrant-sparse-finetune]] — [[SPLADE]] fine-tuning on a product catalog, with synthetic query generation and hard-negative mining
- [[qdrant-relevance-feedback]] — fits the scoring parameters for [[Qdrant]]'s index-native [[Relevance Feedback]] query

## RAG & LLM frameworks
- [[LlamaIndex]]
- [[LangChain]]
- [[Haystack (deepset)]]
- [[DSPy]]
- [[GEPA]] — reflective prompt optimizer, Pareto candidate selection
- [[AutoRAG]]
- [[RAGAS]] — RAG-specific evaluation metrics

## Other
- [[SID-1]]
- [[Embabel]]
- [[Embabel DICE]]
- [[django-dice]]

## Related
- [[Topics]] · [[Concepts]] · [[Case Studies]] · [[People]]
