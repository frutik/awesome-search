---
title: "Qwen Studio"
source: "https://qwen.ai/blog?id=qwen3-embedding"
author:
published:
created: 2026-05-15
description: "Qwen Studio offers comprehensive functionality spanning chatbot, image and video understanding, image generation, document processing, web search integration, tool utilization, and artifacts."
tags:
  - "clippings"
---
We release **Qwen3 Embedding series**, a new proprietary model of the Qwen model family. These models are specifically designed for **text embedding**, **retrieval**, and **reranking** tasks, built on the Qwen3 foundation model. Leveraging Qwen3's robust multilingual text understanding capabilities, the series achieves state-of-the-art performance across multiple benchmarks for text embedding and reranking tasks. We have open-sourced this series of text embedding and reranking models under the Apache 2.0 license on Hugging Face and ModelScope, and published the technical report and related code on GitHub.

![](https://mitalinlp.oss-cn-hangzhou.aliyuncs.com/dingkun/models/qwen-embedding/q3e-mteb-result-0605.png)

**Evaluation results for reranking models**

| Model | Param | MTEB-R | CMTEB-R | MMTEB-R | MLDR | MTEB-Code | FollowIR |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Qwen3-Embedding-0.6B** | 0.6B | 61.82 | 71.02 | 64.64 | 50.26 | 75.41 | 5.09 |
| Jina-multilingual-reranker-v2-base | 0.3B | 58.22 | 63.37 | 63.73 | 39.66 | 58.98 | \-0.68 |
| gte-multilingual-reranker-base | 0.3B | 59.51 | 74.08 | 59.44 | 66.33 | 54.18 | \-1.64 |
| BGE-reranker-v2-m3 | 0.6B | 57.03 | 72.16 | 58.36 | 59.51 | 41.38 | \-0.01 |
| **Qwen3-Reranker-0.6B** | 0.6B | 65.80 | 71.31 | 66.36 | 67.28 | 73.42 | 5.41 |
| **Qwen3-Reranker-4B** | 4B | **69.76** | 75.94 | 72.74 | 69.97 | 81.20 | **14.84** |
| **Qwen3-Reranker-8B** | 8B | 69.02 | **77.45** | **72.94** | **70.19** | **81.22** | 8.05 |

**Note**:

- We use the text retrieval subsets of MTEB(eng, v2), MTEB(cmn, v1), MTEB (Multilingual) and MTEB (Code), which are denoted as MTEB-R, CMTEB-R, MMTEB-R and MTEB-Code.

- All scores are our runs based on the top-100 candidates retrieved by dense embedding model [Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B).

**Key Features**:

**Exceptional Versatility**: The embedding model has achieved state-of-the-art performance across a wide range of downstream application evaluations. The 8B size embedding model ranks No.1 in the MTEB multilingual leaderboard (as of June 5, 2025, score **70.58**). The reranking models excel in text retrieval scenarios, significantly improving search relevance.

**Comprehensive Flexibility**: The Qwen3 Embedding series offers a diverse range of sizes (from 0.6B to 8B) for both embedding and reranking models, catering to various use cases that prioritize efficiency and effectiveness. Developers can seamlessly combine these two modules. Additionally, the embedding model allows for flexible vector definitions across all dimensions, and both embedding and reranking models support user-defined instructions to enhance performance for specific tasks, languages, or scenarios.

**Multilingual Capability**: The Qwen3 Embedding series support over 100 languages, including various programming languages, and provides robust multilingual, cross-lingual, and code retrieval capabilities.

**Model Overview**:

| Model Type | Models | Size | Layers | Sequence Length | Embedding Dimension | MRL Support | Instruction Aware |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Text Embedding** | Qwen3-Embedding-0.6B | 0.6B | 28 | 32K | 1024 | Yes | Yes |
|  | Qwen3-Embedding-4B | 4B | 36 | 32K | 2560 | Yes | Yes |
|  | Qwen3-Embedding-8B | 8B | 36 | 32K | 4096 | Yes | Yes |
| **Text Reranking** | Qwen3-Reranker-0.6B | 0.6B | 28 | 32K | \- | \- | Yes |
|  | Qwen3-Reranker-4B | 4B | 36 | 32K | \- | \- | Yes |
|  | Qwen3-Reranker-8B | 8B | 36 | 32K | \- | \- | Yes |

*Note: "MRL Support" indicates whether the embedding model supports custom dimensions for the final embedding. "Instruction Aware" notes whether the embedding or reranking model supports customizing the input instruction according to different tasks.*

## Model Architecture

Based on the Qwen3 foundation model, our Embedding and Reranking models are designed using dual-encoder and cross-encoder architectures. Through LoRA fine-tuning, we aim to fully preserve and enhance the text understanding capabilities of the base model. The Embedding model processes a single text segment as input, extracting the semantic representation by utilizing the hidden state vector corresponding to the final `[EOS]` token. In contrast, the Reranking model takes text pairs (such as user queries and candidate documents) as input, calculating and outputting a relevance score between the pairs using a cross-encoder structure.

![](https://mitalinlp.oss-cn-hangzhou.aliyuncs.com/dingkun/models/qwen-embedding/q3e-model-arc.png)

## Model Training

The training framework for the Qwen3 Embedding series follows the multi-stage training paradigm established by the GTE-Qwen series. During the training of the Embedding model, we implemented a three-stage training structure: the first stage involves contrastive pre-training with a large volume of weakly supervised data; the second stage focuses on supervised training using high-quality labeled data; and the final stage integrates multiple candidate models through a merging strategy to enhance overall performance. This staged training mechanism effectively balances the model's generalization ability and task adaptability. For the Reranking model, based on empirical validation results, we directly employed high-quality labeled data for supervised training, significantly improving training efficiency. Notably, during the first stage of weakly supervised training for the Embedding model, we developed an innovative multi-task adaptable prompt system. By leveraging the text generation capabilities of the Qwen3 foundation model, we dynamically generated weakly supervised text pairs tailored to different task types and languages. This approach addressed the limitations of traditional methods, which often relied on community forums or open-source data for text relevance pair collection, facilitating the efficient generation of large-scale weakly supervised data.

![](https://mitalinlp.oss-cn-hangzhou.aliyuncs.com/dingkun/models/qwen-embedding/q3e-train-pipeline.png)

## Future work

The Qwen3 Embedding series models represent a new starting point. Through ongoing optimizations of the Qwen foundation model, we will enhance the training efficiency of text embeddings and reranking models, thereby improving deployment performance across various scenarios. Additionally, we plan to expand our multimodal representation system to establish cross-modal semantic understanding capabilities. We look forward to seeing more developers explore a wider range of scenarios based on the Qwen3 Embedding series, driving deeper applications of the model across diverse contexts.