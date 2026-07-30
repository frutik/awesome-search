---
title: ONNX
type: tool
tags:
  - tool
  - machine-learning
  - model-serving
  - inference
website: https://onnx.ai/
repo: https://github.com/onnx/onnx
maintainer: "Linux Foundation (LF AI & Data)"
created: 2026-06-29
---

# ONNX

**ONNX** (Open Neural Network Exchange) is an open, framework-agnostic format for representing machine-learning models, with **ONNX Runtime** as the high-performance inference engine. A model trained in PyTorch / TensorFlow / scikit-learn is exported to a single `.onnx` graph and served anywhere ONNX Runtime runs — decoupling training framework from serving.

- Website: https://onnx.ai/
- GitHub: https://github.com/onnx/onnx

---

## Why It Matters for Search

ONNX is the standard way to ship **neural rankers and embedders into a search engine** without a separate model server:

- **[[Vespa]]** runs ONNX models inside ranking expressions via the `onnx(...)` function — typically a [[Cross-Encoder]] in the `global-phase` of [[Vespa Learning to Rank]]; inference is accelerated by ONNX Runtime on the content/container nodes.
- Used to serve [[Reranking|rerankers]], [[Bi-Encoder|bi-encoders]], and other transformer models at query time across engines.

A worked instance: in [[Improving Search Ranking with Few-Shot Prompting of LLMs]] a 22M-parameter
6-layer MiniLM cross-encoder trained on synthetic data is exported to ONNX and deployed as a Vespa
rerank phase over the top 30 hits — the whole path from a training notebook to production serving, with
no model server in between. Small transformer rerankers are where the format earns its place: the model
is a few tens of MB and runs on CPU inside the engine.

It complements GBDT formats: Vespa imports [[XGBoost]] / [[LightGBM]] as GBDT and ONNX as neural, and can ensemble them in one ranking expression.

## Related Tools

- [[Vespa]] — runs ONNX models in ranking expressions
- [[XGBoost]] · [[LightGBM]] — GBDT counterparts for [[Learning to Rank]]

## Related Concepts

- [[Vespa Learning to Rank]] — ONNX cross-encoders as the `global-phase` reranker
- [[Cross-Encoder]] — the model type most often served via ONNX in search
- [[Reranking]] — ONNX models as the rescoring stage
- [[Synthetic Query Generation]] — how the cross-encoder in the example above was trained

## Articles

- [[Improving Search Ranking with Few-Shot Prompting of LLMs]] — [[Jo Kristian Bergum]] ([[Vespa]]);
  ONNX export as the handoff between training and serving
