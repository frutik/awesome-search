---
title: "Fine-Tuning Qwen3 Embeddings for product category classification on the Large-Scale Product Corpus"
source: "https://blog.ivan.digital/fine-tuning-qwen3-embeddings-for-product-category-classification-on-the-large-scale-product-corpus-3a0919506bc8"
author:
  - "[[Ivan]]"
published: 2025-07-20
created: 2026-05-15
description: "Fine-Tuning Qwen3 Embeddings for product category classification on the Large-Scale Product Corpus Language-models such as GPT, Llama, DeepSeek, Qwen trained with a filtered slice of Common Crawl …"
tags:
  - "clippings"
---
Language-models such as GPT, Llama, DeepSeek, Qwen trained with a filtered slice of Common Crawl. For e-commerce work, though, we can start with the **Web Data Commons** ([WDC](https://webdatacommons.org/)), the project by the University of Mannheim. It extracts web pages that carry some metadata and publishes the result as the **Large-Scale Product Corpus (LSPC)**. Follow up of this post is [Qwen3 SFT and DPO fine-tuning tutorial.](https://blog.ivan.digital/finetuning-qwen3-with-lora-done-right-94d6343e1814) And another one is about how to train from scratch [Pytorch Embedding Classifier model](https://blog.ivan.digital/beating-qwen3-lora-with-a-tiny-pytorch-encoder-on-the-large-scale-product-corpus-afe536de205f).

Search engines like Google reward pages that include detailed product markup, so merchants already populate their sites with SEO-friendly fields such as title, brand, GTIN, price — and, crucially, category labels. Thanks to these built-in annotations, the WDC Large-Scale Product Corpus arrives almost fully self-labelled. I used those labels to fine-tune [Qwen3 Embedding](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) with Low-Rank Adaptation (LoRA), [code is available on github](https://github.com/ivan-digital/web-product-data). The resulting 615 million-parameter checkpoint fits comfortably in limited GPU memory yet updates the model's representation space, mapping raw product titles to six top-level categories with a macro-F1 of **0.836 (83.6 %)**.

**Understanding Product Data**

At the heart of any classification system is its data. This project utilises a rich dataset known as the **Large-Scale Product Corpus (LSPC) V2020**, which is derived from the **Web Product Common Crawl subset** using web page metadata filtering to extract product data. Think of it as a massive collection of product information scraped from the internet.

For this specific classification task, the project focuses on the six most represented categories: **Automotive,** **Baby,** **Books, Clothing, Jewelry, Shoes**.

**Qwen3 Embedding Models**

The classification pipeline relies on the **Qwen3 Embedding** family of models. As documented in its accompanying paper, Qwen3 currently occupies the top position on the Hugging Face **MTEB** leaderboard. Qwen3 Embeddings are focused on: **text embeddings extraction and reranking.**

Because Qwen 3 is a large language model trained on diverse text, its embeddings capture subtleties such as brand references, synonyms, and domain-specific jargon. The Qwen3 Embedding series offers a range of model sizes, including 0.6 billion, 4 billion, and 8 billion parameters.

**Our Experiments and Performance**

For product title classification specifically, which focuses on a 6-class categorisation, the project achieved results:

- **Macro F1**: **0.8360 (83.60%)**.
- **Accuracy**: **0.8791 (87.91%)**.

The github repository highlights specific optimisations:

- **LoRA Fine-tuning**: r=16, alpha=32.
- **Optimiser and Learning Rate**: adamw_torch optimizer, learning rate of 5e-5 over a single epoch.

**Practical inference performance on CUDA GPUs**

On a single 32 GB-VRAM NVIDIA RTX 5090 GPU, the 615 M-parameter Qwen3-Embedding LoRA checkpoint consistently delivered impressive latency: **3.3–3.9 ms per title** across batch sizes 16, 32, 64, and 128. Batch size 32 gave the best results, achieving a throughput of **≈ 299 titles · s⁻¹**.

**Conclusion**

- **Massive fine-tuning pay-off.** Training on tens of millions of titles from the Web Data Commons LSPC vault reshaped Qwen3-Embedding into a domain-aware vectoriser that hits 0.836 macro-F1 on six broad categories — without touching the full model weights.
- **Real-time speed on a single GPU.** The 615 M-parameter LoRA head processes ~300 titles · s⁻¹ at 3–4 ms latency on an RTX 5090.
- **Plug-and-play for new teams.** Checkpoints, training scripts, and benchmarking code are all public.