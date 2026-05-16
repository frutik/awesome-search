---
type: article
tags: [article, llm, fine-tuning, unsloth, ollama, gguf]
source: "https://pub.towardsai.net/fine-tuning-llms-from-zero-to-hero-with-python-ollama-52258966bb6d"
author: [MahendraMedapati]
company: []
concepts: [LLM]
topics: [Conversational and Agentic Search]
---

# Fine-Tuning LLMs: From Zero to Hero with Python & Ollama

Practical tutorial: fine-tune a small LLM (Phi-3 Mini) using **Unsloth** (2× training speedup), export to **GGUF** format, and serve locally via **Ollama**.

## Key Steps

1. **Dataset**: 20–500 input-output pairs in JSON format
2. **Setup**: Google Colab T4 GPU (free); install `unsloth`, `trl`, `peft`
3. **Model**: Load `phi-3-mini-4k-instruct` in 4-bit via Unsloth
4. **LoRA**: `r=16`, target all projection layers via `get_peft_model`
5. **Train**: `SFTTrainer`, `max_steps=60`, `learning_rate=2e-4`
6. **Export**: `save_pretrained_gguf` → GGUF format for Ollama
7. **Serve**: `ollama create model-name -f Modelfile` → `ollama run model-name`

## Use Cases for Search

- Fine-tune for structured JSON output from search queries (consistent extraction)
- Domain-specific query classification
- On-premise deployment where privacy prevents using external APIs

## Key Tips

- Temperature 0.1–0.3 for consistent deterministic outputs
- 100+ diverse examples prevents overfitting to format
- Monitor training loss; should decrease steadily
- Unsloth is significantly faster than vanilla HuggingFace training
