---
type: dataset
title: "QASPER"
aliases: ["Qasper"]
tags: [dataset, question-answering, rag, chunking, scientific-papers]
related_concepts:
  - "[[Text Chunking]]"
  - "[[RAG]]"
created: 2026-10-11
---

# QASPER

A question-answering dataset over research papers, where researchers have marked the evidence paragraphs that answer each question. Because the evidence is marked at the paragraph level, it can score **how much of the answer a retrieved chunk actually contains**, which makes it useful for evaluating [[Text Chunking]] and not only answer quality.

---

## Use in This Vault

[[Jevjitsu - How We Tried Generalized Classifiers on Everything]] used 407 papers and 1,297 questions to compare a [[Jev]]-based topic-boundary chunker against fixed-size, recursive and embedding-based chunkers. [[Qdrant]] retrieved five chunks per question, scored with character-level recall, precision and intersection over union against the marked evidence. Jev led on all three at matched chunk sizes.

One property of the dataset shaped that result: answers are whole paragraphs, so a recursive splitter that breaks on blank lines first is already well aligned with the evidence. That baseline was the hardest to beat.

## Related Concepts

- [[Text Chunking]] · [[RAG]]

## Related Articles

- [[Jevjitsu - How We Tried Generalized Classifiers on Everything]]
