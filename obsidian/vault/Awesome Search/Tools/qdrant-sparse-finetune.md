---
type: tool
title: "qdrant-sparse-finetune"
aliases: ["sparse-finetune", "Qdrant Sparse Finetune"]
website: https://qdrant.tech/articles/sparse-embeddings-ecommerce-part-5/
repo: https://github.com/qdrant/sparse-finetune
tags:
  - tool
  - sparse-retrieval
  - fine-tuning
  - open-source
related_concepts:
  - "[[SPLADE]]"
  - "[[Learned Sparse Retrieval]]"
  - "[[Hard Negative Mining]]"
  - "[[Embedding Fine-tuning]]"
created: 2026-07-27
---

# qdrant-sparse-finetune

Open-source framework from [[Qdrant]] for fine-tuning [[SPLADE]] sparse retrievers on a product catalog. It packages the pipeline from [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] so that a practitioner with a product CSV — and no relevance labels — can produce a domain-adapted sparse model.

🔗 Repo: https://github.com/qdrant/sparse-finetune

```bash
pip install git+https://github.com/qdrant/sparse-finetune.git
```

```python
from sparse_finetune import finetune
finetune("products.csv")
```

## Pipeline

Five stages under the hood:

1. **Parse the catalog** — several input formats; all text fields are concatenated into one string per product for the model
2. **Obtain queries** — use your own (click logs, labeled data) or **generate them with an LLM**
3. **Build the SPLADE architecture** from config
4. **Train with hard-negative mining** — the ANCE loop, using temporary [[Qdrant Vector DB]] collections
5. **Publish to Hugging Face** — prompts for a repo name, handles auth, prints the URL

### Synthetic query generation

Routed through `litellm`, so it works with OpenAI (`gpt-4o-mini`), Anthropic (`claude-sonnet`), and local Ollama models. The prompt is editable, and a human-in-the-loop verification pass is available. This is the step that removes the hardest prerequisite: you no longer need labeled query-product pairs to start.

### Configuration defaults

| Option | Default | Notes |
|---|---|---|
| `base_model` | DistilBERT | Starting encoder |
| `ance_iterations` | 3 | Hard-negative mining rounds |
| `batch_size` | 64 | |
| `mining_top_k` | 20 | Retrieval depth when mining |
| `num_negatives` | 3 | Negatives kept per query |

The architecture default is **inference-free SPLADE**, but [[Evgeniya Sukhodolskaya]] recommends switching to full SPLADE for e-commerce: the domain is intent-heavy, and the query-side encoder is what distinguishes "Apple juice" from "Apple iPhone". The regularizer weights control representation sparsity; defaults are described as reasonable to start with.

## Interfaces

- **Python API** — `finetune("products.csv")`, or the `Trainer` class for granular control
- **CLI** — end-to-end in one command, or stage by stage
- **Dashboard** — `qdrant-finetune studio`, a web UI with a tab per stage, live training logs, and job history

## Operational Notes

- Mining **creates temporary Qdrant collections**, indexes into them, searches, then deletes them — budget RAM and disk accordingly. A trial run fits on the free tier.
- **Evaluation runs against training data by default.** Sukhodolskaya had to hand-roll a held-out query split: *"if the numbers look too good, don't get too excited immediately."*
- Column mapping is not automatic — the ID column and text fields must be named explicitly.

Characterized by its own presenter as **"slightly shaky"** and open for contributions.

## Related Tools

- [[Sentence Transformers]] — the training library underneath
- [[Qdrant Vector DB]] — required, for the hard-negative mining loop

## Related Concepts

- [[SPLADE]] · [[Learned Sparse Retrieval]] · [[Hard Negative Mining]] · [[Embedding Fine-tuning]]

## Articles

- [[Fine-Tuning Sparse Embeddings for E-Commerce Search]] — Part 5 introduces the package
- [[Evgeniya Sukhodolskaya - Fine-Tuning Sparse Neural Retrievers for E-Commerce]] — walkthrough and caveats

## People

- [[Thierry Damiba]] · [[Evgeniya Sukhodolskaya]]
