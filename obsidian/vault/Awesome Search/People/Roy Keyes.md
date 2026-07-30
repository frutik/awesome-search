---
title: "Roy Keyes"
type: person
aliases:
  - Keyes
role: "Data scientist / author"
website: "https://roycoding.com/"
blog: "https://roycoding.com/blog/"
tags:
  - person
  - data-science
  - machine-learning
created: 2026-07-30
---

# Roy Keyes

Data science practitioner and writer; runs Zefs Data Science and has written a book on hiring
data scientists and machine learning engineers. Blogs at
[roycoding.com](https://roycoding.com/).

He appears in this vault for one widely-reused sentence.

## Known For (here)

*The shortest definition of embeddings?* (19 Nov 2022) —
https://roycoding.com/blog/2022/embeddings.html

> Embeddings are learned transformations to make data more useful

The post unpacks the definition word by word:

- **Learned** — parameters determined from data rather than fixed by an algorithm, optimised for
  a specific task
- **Transformations** — moving data from one representation to another, e.g. words from
  high-dimensional one-hot encoding to lower-dimensional dense vectors
- **Data** — any modality: text, images, audio, webpages, time series
- **Useful** — a representation that serves the task at hand, whether by grouping similar items,
  reducing dimensionality, or being reusable across related tasks

The definition's value is that it puts the emphasis on *learned* and *useful for a task*, which
is exactly the ground on which pre-trained-without-fine-tuning embeddings fail — see
[[Embedding Fine-tuning]] and [[Zero-Shot Retrieval]].

## Cited In

- [[Three mistakes when introducing embeddings and vector search]] — [[Jo Kristian Bergum]]
  opens with this definition

## Related Concepts

- [[Embeddings]] — the concept being defined
- [[Embedding Fine-tuning]] — where "useful for the task" becomes load-bearing
