---
title: "Improve Your RAG Applications by Moving to Task-Aware Embeddings"
source: "https://medium.com/@gal.peretz/improve-your-rag-applications-by-moving-to-task-aware-embeddings-09ebee62616f"
author: ["Gal Peretz"]
tags:
  - clippings
  - embeddings
  - rag
  - task-aware
  - retrieval
  - medium
concepts:
  - Task-Aware Embeddings
  - RAG
  - Asymmetric Semantic Search
  - Bi-Encoder
created: 2026-05-15
---

# Improve Your RAG Applications by Moving to Task-Aware Embeddings

**Source**: https://medium.com/@gal.peretz/improve-your-rag-applications-by-moving-to-task-aware-embeddings-09ebee62616f  
**Author**: Gal Peretz

## Summary

Argues that standard "one-size-fits-all" embeddings in RAG pipelines leave significant quality on the table, and that task-aware embeddings (using different representations for queries vs. documents, and for different retrieval tasks) meaningfully improve retrieval quality.

## The Problem: Task Mismatch

A typical RAG pipeline:
1. Encode documents with model M at index time
2. Encode query with the same model M at query time
3. Retrieve by cosine similarity

**Problem**: The optimal embedding for "a document about machine learning" is different from the optimal embedding for "the question 'what is machine learning?'". Using the same model and prompt for both creates a **task mismatch**.

## Task-Aware Embedding Models

### Instruction-Following Models (e.g., Instructor)

```python
from InstructorEmbedding import INSTRUCTOR

model = INSTRUCTOR('hkunlp/instructor-large')

# Different instructions for different task aspects
query_instruction = "Represent the question for retrieving relevant passages: "
doc_instruction = "Represent the passage for retrieval: "

query_emb = model.encode([[query_instruction, "What is machine learning?"]])
doc_emb = model.encode([[doc_instruction, "Machine learning is a field of AI..."]])
```

The instruction modifies the embedding's orientation in vector space.

### E5 Models (Microsoft)

Use `query:` and `passage:` prefixes:
```python
query_emb = model.encode("query: What is machine learning?")
doc_emb = model.encode("passage: Machine learning is a field of AI...")
```

### Impact on RAG Quality

The author reports significant improvements on domain-specific benchmarks:
- 8–15% improvement in NDCG@10 on domain-specific corpora
- Especially impactful for asymmetric tasks (short question → long passage)

## Multi-Task RAG Scenarios

Enterprise RAG often requires multiple retrieval tasks simultaneously:
- FAQ matching (question-question similarity) 
- Document retrieval (question-passage asymmetric)
- Similar document finding (document-document symmetric)
- Code search (natural language → code)

Task-aware models handle all by varying the instruction prefix — one model, multiple optimal configurations.

## Implementation in RAG Pipeline

```python
class TaskAwareRAG:
    def __init__(self, model):
        self.model = model
        self.task_instructions = {
            "qa": ("Represent the question:", "Represent the passage:"),
            "summary": ("Represent the query:", "Represent the document summary:"),
            "code": ("Represent the code query:", "Represent the code:"),
        }
    
    def index(self, documents, task="qa"):
        _, doc_instruction = self.task_instructions[task]
        return self.model.encode([[doc_instruction, d] for d in documents])
    
    def retrieve(self, query, task="qa"):
        query_instruction, _ = self.task_instructions[task]
        return self.model.encode([[query_instruction, query]])
```

## Related Articles

- [[How Context-Aware Embeddings Are Transforming Enterprise Search]] — enterprise angle
- [[Chunking Strategies for LLM Applications]] — other RAG quality lever
- [[Evaluating the Ideal Chunk Size for a RAG System using LlamaIndex]] — chunk size impact
- [[Introduction to Matryoshka Embedding Models]] — another embedding improvement

## Related Concepts

- [[Task-Aware Embeddings]] — primary concept
- [[RAG]] — use case
- [[Asymmetric Semantic Search]] — asymmetric task alignment
- [[Bi-Encoder]] — base architecture
- [[Embedding Fine-tuning]] — alternative approach for task alignment
