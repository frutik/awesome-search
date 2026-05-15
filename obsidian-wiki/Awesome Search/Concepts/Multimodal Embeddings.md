---
title: "Multimodal Embeddings"
aliases: ["cross-modal embeddings", "vision-language embeddings", "CLIP embeddings", "image-text embeddings"]
tags:
  - concept
  - embeddings
  - multimodal
  - computer-vision
---

# Multimodal Embeddings

## Definition

Multimodal embeddings project multiple data modalities (text, images, audio, video) into a shared vector space, enabling cross-modal retrieval: search for images using text queries, or find text documents using image queries.

## CLIP Architecture

The dominant approach is CLIP (Contrastive Language-Image Pre-training, OpenAI):

```
Image → Vision Encoder (ViT) → image embedding ─┐
                                                  ├→ cosine similarity
Text  → Text Encoder (Transformer) → text emb  ──┘
```

Trained on 400M (image, caption) pairs from the web using contrastive loss — push matching pairs together, pull non-matching apart.

## Domain-Specific Fine-tuning

General CLIP models may fail on specialized visual domains:
- Medical imaging (CT scans, pathology slides)
- Satellite imagery
- Fashion/product images with fine-grained attributes
- Technical diagrams

[[Shaw Talebi]]'s work demonstrates fine-tuning CLIP for domain-specific multimodal search:
1. Collect domain (image, text description) pairs
2. Fine-tune with contrastive loss
3. Evaluate on domain-specific retrieval benchmarks

## Fine-tuning with `sentence-transformers`

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.losses import MultipleNegativesRankingLoss

model = SentenceTransformer("clip-ViT-B-32")
train_examples = [InputExample(texts=["a dog", image_path])]
train_loss = MultipleNegativesRankingLoss(model)
model.fit(train_objectives=[(train_dataloader, train_loss)])
```

## Applications

| Use Case | Query | Retrieved |
|----------|-------|-----------|
| E-commerce visual search | Image of shoe | Similar shoes |
| Medical report retrieval | Text symptoms | Related X-rays |
| Stock photo search | Text description | Matching images |
| Document understanding | Image of chart | Text explanations |
| Fashion similarity | Outfit photo | Similar products |

## Matryoshka + Multimodal

[[Matryoshka Embeddings]] (MRL) can be applied to multimodal models, enabling:
- Fast first-pass search with truncated (smaller) embeddings
- Re-ranking with full-dimension embeddings
- Storage savings for large image+text databases

## Relation to Text-Only Embeddings

Shares training principles with text [[Bi-Encoder]]:
- Contrastive loss
- Cosine similarity
- ANN index for retrieval ([[Dense Vector Retrieval]])

Differs in:
- Heterogeneous encoders (vision vs. language)
- Cross-modal alignment challenge
- Domain gap often more severe

## Related Concepts
- [[Embeddings]] — parent concept
- [[Dense Embeddings]] — multimodal embeddings are dense vectors spanning modalities

- [[Bi-Encoder]] — same architecture principle, text-only
- [[Embedding Fine-tuning]] — fine-tuning strategy
- [[Dense Vector Retrieval]] — downstream retrieval
- [[Matryoshka Embeddings]] — dimension flexibility
- [[Semantic Search]] — generalization

## People

- [[Shaw Talebi]] — CLIP fine-tuning for domain-specific multimodal search
