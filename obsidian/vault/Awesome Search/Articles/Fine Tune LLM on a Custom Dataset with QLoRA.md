---
created: 2026-05-16
type: article
tags: [article, llm, fine-tuning, qlora, lora, peft, quantization, medium]
source: "https://dassum.medium.com/fine-tune-large-language-model-llm-on-a-custom-dataset-with-qlora-fb60abdeba07"
author: [Suman Das]
company: []
concepts: [LLM, QLoRA, LoRA, PEFT]
topics: [Conversational and Agentic Search]
---

# Fine Tune LLM on a Custom Dataset with QLoRA

End-to-end tutorial for fine-tuning a large language model (Phi-2) on a domain-specific dataset using **QLoRA** (Quantized LoRA). Relevant for search practitioners who need to adapt LLMs for query understanding, document generation, or RAG pipelines.

## Key Concepts

**[[LoRA]]** (Low-Rank Adaptation): instead of fine-tuning all model weights, train two small matrices that approximate the weight update. Produces a small adapter (~MBs) that can be applied on top of the frozen base model.

**[[QLoRA]]**: LoRA + 4-bit quantization of the base model weights. Reduces GPU memory significantly (fits a 2.7B model on a single consumer GPU) with minimal accuracy loss.

**[[PEFT]]** (Parameter-Efficient Fine-Tuning): umbrella term for techniques like LoRA/QLoRA that update only a subset of parameters.

## Process

1. Load base model (Phi-2) in 4-bit via `BitsAndBytesConfig`
2. Apply LoRA adapter config (`r=32`, target Q/K/V projection layers)
3. Format dataset as instruction-response pairs
4. Train with `SFTTrainer` (supervised fine-tuning)
5. Evaluate with ROUGE metric against human baseline summaries

## When to Use Fine-tuning vs RAG

- Fine-tune for: strict output formatting (JSON), domain-specific terminology, cost reduction (small specialized model instead of GPT-4)
- RAG for: frequently changing knowledge, grounded citations, factual retrieval

## Search Relevance

Fine-tuning is directly relevant for: LLM-based query rewriting, intent classification, judgement label generation, and RAG synthesis layers.
