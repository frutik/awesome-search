---
type: tool
title: "Lychee-Reranker"
aliases: ["KaLM-Reranker", "KaLM-Reranker-V1", "KaLM-Reranker-V1-R2"]
website: "https://huggingface.co/KaLM-Embedding/KaLM-Reranker-V1-Large-R2"
repo: "https://github.com/HITsz-TMG/Lychee-Reranker"
tags: [tool, reranking, cross-encoder, encoder-decoder]
created: 2026-10-30
---

# Lychee-Reranker

An open reranker family built on the [[Fast but Not Late Interaction]] design, released as *KaLM-Reranker-V1* and renamed Lychee-Reranker in later revisions of its paper ([[Lychee-Reranker - Fast but Not Late Interaction for Compressed Document Reranking]]). Models are on Hugging Face under the KaLM-Embedding collection; code is at https://github.com/HITsz-TMG/Lychee-Reranker.

- Model card (Large R2): https://huggingface.co/KaLM-Embedding/KaLM-Reranker-V1-Large-R2
- Paper: https://arxiv.org/abs/2606.22807

---

## Models

Three sizes on T5Gemma2 encoder-decoders, by activated parameters: **Nano** (0.27B), **Small** (1B) and **Large** (4B). The R2 models keep the same architecture and inference interface as the original release.

## Usage

The document is wrapped as `<Document>: {document}` and fed to the encoder, where it is compressed by mean-pooling groups of encoder token states (the model card's Sentence Transformers example uses `chunk_size=4`). The decoder receives the instruction and query as a chat-style prompt and answers "yes" or "no". The score is P(yes) by default, or yes_logit minus no_logit with an Identity activation.

## Performance

On [[BEIR]], Large averages 63.53 nDCG@10 (Qwen3-Reranker-4B: 63.50, Qwen3-Reranker-8B: 65.11); on [[MIRACL]] Large averages 74.92. Estimated online cost is a small fraction of the Qwen3-Reranker series at comparable quality (Small 4.6x vs 28.2x for Qwen3-Reranker-0.6B). Details and caveats in the paper note.

## Related Concepts
- [[Fast but Not Late Interaction]] · [[Reranking]] · [[Cross-Encoder]] · [[Late Interaction]] · [[Matryoshka Embeddings]]

## Related Articles
- [[Lychee-Reranker - Fast but Not Late Interaction for Compressed Document Reranking]]
