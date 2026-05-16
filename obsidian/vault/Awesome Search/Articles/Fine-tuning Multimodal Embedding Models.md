---
title: "Fine-tuning Multimodal Embedding Models"
source: "https://medium.com/towards-data-science/fine-tuning-multimodal-embedding-models-bf007b1c5da5"
author: ["Shaw Talebi"]
tags:
  - clippings
  - embeddings
  - multimodal
  - fine-tuning
  - clip
concepts:
  - Multimodal Embeddings
  - Embedding Fine-tuning
  - Dense Vector Retrieval
created: 2026-05-15
---

# Fine-tuning Multimodal Embedding Models

**Source**: https://medium.com/towards-data-science/fine-tuning-multimodal-embedding-models-bf007b1c5da5  
**Author**: [[Shaw Talebi]]

## Summary

[[Shaw Talebi]] extends his embedding fine-tuning work to multimodal models, demonstrating CLIP fine-tuning for domain-specific image-text retrieval and cross-modal search.

## Multimodal Retrieval Scenarios

Cross-modal search requires a shared embedding space where images and text can be compared:

1. **Text → Image**: "a dog playing fetch" → retrieve matching images
2. **Image → Text**: photo of a dog → retrieve captions/descriptions  
3. **Image → Image**: photo similarity search
4. **Text → Text**: standard semantic search (as baseline)

## Why Fine-tune CLIP?

General CLIP (trained on 400M web image-text pairs) works well for natural photography. It fails on:
- **Medical**: CT scans, histology slides
- **Satellite imagery**: aerial photos with specific features
- **Industrial**: defect inspection, part identification
- **Fashion**: fine-grained attribute matching (hem length, collar type)
- **Scientific**: molecular diagrams, charts, graphs

The domain distribution of training data doesn't cover specialized visual vocabularies.

## CLIP Architecture Recap

```
Image → ViT (Vision Transformer) → image_embedding (512-dim)
                                    ↕ cosine similarity
Text  → Text Transformer         → text_embedding (512-dim)
```

Both encoders project to the same 512-dimensional space — that's the alignment that enables cross-modal search.

## Fine-tuning Procedure

```python
import torch
from transformers import CLIPModel, CLIPProcessor
from torch.utils.data import DataLoader

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Domain dataset: (image, caption) pairs
class DomainDataset(Dataset):
    def __getitem__(self, idx):
        return self.images[idx], self.captions[idx]

optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)

for epoch in range(10):
    for images, texts in dataloader:
        inputs = processor(text=texts, images=images, return_tensors="pt", padding=True)
        outputs = model(**inputs)
        
        # Contrastive loss: maximize similarity of matching pairs
        loss = clip_contrastive_loss(outputs.logits_per_image, outputs.logits_per_text)
        loss.backward()
        optimizer.step()
```

## Results

Talebi demonstrates on a fashion dataset (fine-grained clothing attributes):
- Base CLIP: 42% Recall@5 for text→image retrieval
- Fine-tuned CLIP: 71% Recall@5 (+29% absolute)

The fine-tuned model correctly distinguishes "slim fit jeans" from "relaxed fit jeans" — a distinction the base model collapses.

## Partial Fine-tuning

For small datasets, freeze earlier layers and only fine-tune:
- Image encoder top layers (last 2–4 transformer blocks)
- Text encoder top layers
- Projection heads

This prevents catastrophic forgetting of general visual features.

## Retrieval Infrastructure

Fine-tuned CLIP embeddings plug directly into standard [[Dense Vector Retrieval]] infrastructure:
- Index image embeddings with FAISS/Pinecone
- At query time: encode text → ANN search over image index
- Returns ranked image results

## Related Articles

- [[Fine-Tuning Text Embeddings For Domain-Specific Search]] — same author, text-only
- [[Nearest Neighbor Indexes for Similarity Search]] — ANN for image retrieval
- [[How to Choose the Best Model for Semantic Search]] — model selection

## Related Concepts

- [[Multimodal Embeddings]] — primary topic
- [[Embedding Fine-tuning]] — technique used
- [[Dense Vector Retrieval]] — retrieval infrastructure
- [[Bi-Encoder]] — same architecture principle (two encoders)
- [[Semantic Search]] — cross-modal semantic search

## People

- [[Shaw Talebi]] — author
