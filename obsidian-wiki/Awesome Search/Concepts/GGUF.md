---
title: "GGUF"
aliases: ["GGUF format", "llama.cpp quantization", "LLM quantization"]
tags:
  - concept
  - llm
  - quantization
  - deployment
---

# GGUF

A binary file format for storing quantized LLM weights, developed by the llama.cpp project. The successor to GGML. Enables running large language models locally on CPU and consumer GPU hardware by aggressively compressing model weights.

## Why GGUF Matters for Search

LLM components are increasingly part of search pipelines — query understanding, reranking, synthetic data generation. GGUF makes it practical to run these locally without cloud API costs. Relevant for:
- Local rerankers (cross-encoder models)
- Query expansion / HyDE generation
- LLM-as-Judge evaluation
- Synthetic query generation for autocomplete cold-start (cf. [[LLM-Powered Query Extraction for Autocomplete]])

## File Format Structure

GGUF is a self-describing binary container:
- **Header**: magic bytes, version, metadata key-value pairs (architecture, tokenizer, hyperparams)
- **Tensor index**: names, shapes, types, byte offsets
- **Tensor data**: raw quantized weight blocks, memory-mapped at inference time

Memory-mapping allows partial loading — only needed layers are paged in, enabling models larger than RAM.

## Quantization Schemes

### K-Quants (recommended for quality)
Mixed-precision block quantization. Each block of 32 floats gets a shared scale + min value.

| Quantization | Bits/weight | Size vs F16 | Quality |
|---|---|---|---|
| Q8_0 | 8 | 50% | near-lossless |
| Q5_K_M | 5.5 | ~34% | excellent |
| Q4_K_M | 4.5 | ~28% | good; recommended default |
| Q3_K_M | 3.9 | ~24% | acceptable |
| Q2_K | 2.6 | ~16% | noticeably degraded |

- **_S / _M / _L suffixes**: Small/Medium/Large — trade-off between attention layer precision and FFN precision
- K-Quants store scale and min per block in higher precision than data weights

### I-Quants (importance-matrix guided)
Uses an **importance matrix (imatrix)** — a calibration dataset run through the model to identify which weights matter most — then applies non-uniform quantization levels, preserving critical weights.

| Quantization | Notes |
|---|---|
| IQ4_XS | Better than Q4_K_S at same size |
| IQ3_S | Better than Q3_K_S |
| IQ2_XS | Aggressive; imatrix essential |

Without imatrix, I-Quants can be worse than K-Quants. With good imatrix, they outperform K-Quants at the same bitrate.

## Hardware Selection Guide

| Hardware | Best For | Notes |
|---|---|---|
| CPU only | Q4_K_M, Q5_K_M | Slow but runs anywhere; llama.cpp CPU path |
| Apple Silicon (Metal) | Q4_K_M to Q6_K | Unified memory; GPU layers via `-ngl` |
| Consumer GPU (8–24 GB VRAM) | Q4_K_M, Q5_K_M | Layer offloading to GPU |
| RTX 4090 (24 GB) | Q8_0 or even F16 small models | Best consumer FLOPS/$ |

For embedding inference economics, see [[Why Are Embeddings So Cheap]].

## Deployment Tools

- **Ollama**: user-friendly; auto-downloads GGUF models; REST API
- **llama-server** (llama.cpp): low-level; full control; OpenAI-compatible API
- **LM Studio**: GUI wrapper around llama.cpp

## Related Concepts
- [[Vector Quantization]] — quantization for embedding vectors (different domain: ANN index compression vs. LLM weight compression)
- [[LLM as Judge]]
- [[Embedding Fine-tuning]]
- [[RAG]]

## Articles
- [[GGUF Quantization - A Technical Deep Dive]] — [[Michael Hannecke]]; two-part series covering format internals, K-Quants, I-Quants, imatrix, and deployment

## People
- [[Michael Hannecke]] — GGUF deep-dive author
