---
title: "ColBERT-Zero: To Pre-train Or Not To Pre-train ColBERT Models?"
source: "https://huggingface.co/blog/lightonai/colbert-zero"
author:
  - "[[Antoine Chaffin]]"
  - "[[Luca Arnaboldi]]"
  - "[[Amélie Chatelain]]"
  - "[[Florent Krzakala]]"
published: 2026-02-19
company: "[[LightOn AI]]"
tags: [colbert, multi-vector, pretraining, knowledge-distillation, contrastive-learning, BEIR]
---

# ColBERT-Zero: To Pre-train Or Not To Pre-train ColBERT Models?

**Authors:** [[Antoine Chaffin]], [[Luca Arnaboldi]], [[Amélie Chatelain]], [[Florent Krzakala]] ([[LightOn AI]] / EPFL)

## Summary

State-of-the-art [[ColBERT]] models are conventionally built by taking a strong dense model and adding a small [[Knowledge Distillation]] step. This paper shows that performing contrastive pre-training directly in the **multi-vector setting** significantly improves performance.

**ColBERT-Zero** outperforms GTE-ModernColBERT and its dense base model on BEIR using only public data, setting a new SOTA for models under 150M parameters (55.43 vs 54.67 nDCG@10).

## Three Training Phases

1. **Unsupervised contrastive pre-training** — heavy lifting with in-batch negatives; most expensive (~10x cost of other phases)
2. **Supervised contrastive fine-tuning** — smaller, high-quality datasets with hard negatives
3. **Knowledge distillation (KD)** — transfers knowledge from teacher model; highest signal quality

## Key Findings

### Standard Recipe Leaves Performance on the Table
KD-only approach: 54.09 nDCG@10 vs 55.43 for full multi-vector pre-training — a meaningful 1.3-point gap.

### Efficient Alternative: Supervised + KD (~10x Cheaper)
Supervised contrastive step in multi-vector setting before distillation achieves 55.12 — 99.4% of full pre-training performance at ~10x lower cost (~40 vs ~408 GH200-hours).

### Prompt Alignment is Non-Negotiable
- Adding prompts to a model not pre-trained with them hurts performance
- Stripping prompts from a model pre-trained with them also hurts
- Rule: **always align your fine-tuning prompt setup with the base model's pre-training**
- Hypothesis: prompt tokens act as implicit query expansion — extra slots storing global sequence information

## Training with PyLate

- **GradCache** enables arbitrary batch size without VRAM constraints (standard gradient accumulation doesn't apply to contrastive learning)
- Cross-GPU gathering scales effective batch size to ~16k (required for plausible in-batch hard negatives)
- `split_batches` prevents shortcut learning across data sources

## BEIR Results

| Model | Avg nDCG@10 |
|---|---|
| GTE-ModernColBERT (prior SOTA) | 54.67 |
| **ColBERT-Zero Full** | **55.43** |
| ModernColBERT Supervised+KD | 55.12 |
| ModernColBERT KD only | 54.09 |
| gte-modernbert-base (dense) | 55.33 |

## Related Concepts

- [[ColBERT]] — the multi-vector late interaction architecture
- [[Late Interaction]] — MaxSim scoring mechanism
- [[Knowledge Distillation]] — the teacher-student training phase
- [[Embedding Fine-tuning]] — the broader domain

## Related Articles

- [[What is ColBERT and Late Interaction and Why They Matter in Search]]
- [[Announcing the Vespa ColBERT Embedder]]
- [[Cross-Encoders ColBERT and LLM-Based Re-Rankers]]

## People

- [[Antoine Chaffin]]
- [[Luca Arnaboldi]]
- [[Amélie Chatelain]]
- [[Florent Krzakala]]
