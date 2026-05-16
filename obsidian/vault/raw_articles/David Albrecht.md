---
title: "David Albrecht"
source: "https://dpalbrecht.github.io/LLM-Autocomplete-Autosuggest.html"
author:
published:
created: 2026-05-15
description:
tags:
  - "clippings"
---
## LLM-powered Query Extraction for Auto-Complete and Auto-Suggest

## Motivation

The most powerful search systems have auto-complete (prefix matching) and/or auto-suggest (semantic/fuzzy prefix matching). There are at least three problems one encounters when building these types of systems:

1. If you don't have much search activity, then you have a cold-start problem and can't use queries to inform your product.
2. Even if you do have activity, users submit queries for what they want as opposed to what matches your documents. Sometimes you can remove noisy queries by using logged interactions if you have them but coming up with an exact threshold is not trivial.
3. You can extract phrases using more traditional NLP like SpaCy or directly with a search engine like OpenSearch, but those phrases are often very short and can be underwhelming.

Using LLMs as query extractors solves these problems by using your documents to simulate user queries, and letting the LLM use the documents in creative ways. This post takes us through how I processed 43k product descriptions from the [WANDS dataset](https://github.com/wayfair/WANDS/tree/main/dataset) for < $5 with GPT-4.1-nano. I'll start with the code and end with examples of results.

## Show me the code!

### 1) LLM Query Extraction

First we extract queries from product documents using an LLM. We load the dataset and define the system and task prompts. It's worth noting that processing all of these documents with GPT-4.1-nano takes several hours, even parallelized 10x, so batching is often the better choice for a first run since it cuts costs in half. I didn't batch my requests because 1) I'm impatient and 2) I find the workflow of batching requests, saving IDs, and fetching them in a day to be tedious.

```python
from pydantic import BaseModel, Field
from openai import OpenAI
import pandas as pd

product_df = pd.read_csv("../WANDS/dataset/product.csv", sep='\t').rename(columns={'category hierarchy': 'category_hierarchy'})

class PhrasesOutput(BaseModel):
    phrases: list[str] = Field(..., description="List of search queries for the product.")

system_prompt = "You are a helpful assistant that generates possible user queries from a product description."

def get_task_prompt(product_description: str) -> str:
    return f"""Given the below product information, generate queries that can be used to search for the product.
Product Information:
{product_description}

Adhere to the following rules:
1. Generate up to 10 queries.
2. Each query should be several words long, but not more than 10.
3. The query should be grounded in the description but does not need to use the exact same words.
4. Each query should be different from the other queries such that you capture all major aspects of the product."""

def format_product(product_row) -> str:
    return f"""Product Name: {product_row['product_name']}
Product Class: {product_row['product_class']}
Product Hierarchy: {product_row['category_hierarchy']}
Product Description: {product_row['product_description']}
"""

client = OpenAI()
def query_gpt(system_prompt: str, task_prompt: str, text_format):
    response = client.responses.parse(
        model="gpt-4.1-nano",
        temperature=None,
        instructions=system_prompt,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task_prompt},
        ],
        text_format=text_format,
    )
    return response, response.usage.input_tokens, response.usage.output_tokens
```

An example call looks like this:

```python
example_product = product_df.iloc[10]
response, in_tokens, out_tokens = query_gpt(
    system_prompt=system_prompt,
    task_prompt=get_task_prompt(format_product(example_product)),
    text_format=PhrasesOutput,
)
print(response.output_parsed.phrases)
```

The product description looks like this:

```
Product Name: trestle coffee table
Product Class: Coffee & Cocktail Tables
Product Hierarchy: Furniture / Living Room Furniture / Coffee Tables & End Tables / Coffee Tables / Rectangle Coffee Tables
Product Description: it is an elegant french design that can be placed well in most designer aesthetics .
```

The extracted queries look like this:

```
['French design coffee table',
 'Elegant rectangular coffee table',
 'Designer living room table',
 'French style coffee table',
 'Modern rectangle coffee table',
 'Stylish French coffee table',
 'Living room furniture coffee table',
 'Elegant coffee table for living room',
 'Designer coffee and cocktail table',
 'French inspired rectangle table']
```

These are pretty nice! You can see that we have a query that incorporates the fact that this table has a French design, which would be hard (or impossible) with traditional NLP approaches and perhaps unlikely from a user query perspective.

### 2) Auto-Complete

The idea with auto-complete is that it matches the current query's prefix and returns the most likely ending to that result. This is a *very* rudimentary prefix matcher for example purposes that doesn't bake in any notion of relevance apart from matching the prefix. I sorted from shortest to longest matches, but re-ranking by semantic similarity would be an interesting heuristic to use instead. You should almost certainly use your search engine's native capabilities for prefix matching.

```python
from collections import defaultdict
from tqdm import tqdm

def generate_prefix_index(extracted_phrases):
    prefix_index = defaultdict(list)
    for phrase in tqdm(extracted_phrases):
        for i in range(len(phrase)):
            prefix_index[phrase[:i]].append(phrase)
    # Order by shortest first for readability
    prefix_index = {k: sorted(v, key=lambda x: len(x)) for k, v in prefix_index.items()}
    return prefix_index

def autocomplete(prefix: str, k: int = 5):
    return prefix_index.get(prefix, [])[:k]

prefix_index = generate_prefix_index(extracted_phrases)
```

### 3) Auto-Suggest

The idea with auto-suggest is that we don't have to match the user's query *exactly*. Instead, we try to find similar matches. If auto-complete works directly in the search bar, then auto-suggest is a dropdown of possible queries. Auto-suggest can be a good fallback for auto-complete when the user is being creative. The funny part about this is it's just an embedding + cosine similarity calculation, so it itself could be considered a basic search system. Latency and recall can be hard to balance here, especially when it really matters we serve quickly, but I could see a world in which this is actually a hybrid BM25 + vector similarity search system.

```python
import numpy as np
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embedding_model.encode(extracted_phrases, normalize_embeddings=True)

def autosuggest(query: str, k: int = 5):
    query_embedding = embedding_model.encode(query, normalize_embeddings=True)
    similarities = np.dot(embeddings, query_embedding)
    top_inds = np.argsort(similarities)[::-1][:k]
    return [(extracted_phrases[i], float(similarities[i])) for i in top_inds]
```

## Show me the results!

There are some interesting completions and suggestions! It looks like we don't have great matches for shoes at all (maybe they don't exist in the corpus and it can be good to signal that to users). The completions for 'bed' are nice, while the suggestions are pretty funny. What is a bed for if not sleeping and relaxing? It looks like the 'nautical' keyword had no direct completions but really nice suggestions.

We might want to clean up specific categories of queries, use counts to normalize them, or filter out underperformers over time if users aren't clicking. It would be really interesting to set up an online learner, like a contextual bandit, to constantly manage which completions/suggestions are better in a certain context.

```python
print(autocomplete('shoe'))
# ['shoe-themed wall art', 'shoes over door rack', 'shoe and clothing rack', 'shoe closet with doors', 'shoe rack for mudrooms']
print(autosuggest('shoe'))
# [('compact shoe wardrobe', 0.6652849), ('household shoe organization', 0.6594601), ('sneaker and heel shoe tower', 0.6581194), ('office shoe organization', 0.63617384), ('walk-in closet shoe organization', 0.6343239)]

print(autocomplete('bed'))
# ['bed riser blocks', 'bed security pad', 'bedroom decor rug', 'bedroom floor rug', 'bedroom robe hook']
print(autosuggest('bed'))
# [("bed for a good night's rest", 0.7434023), ('bed in Bed & Bath category', 0.7412436), ('bed for sleeping and relaxing', 0.73879534), ('bed for lounging and sleeping', 0.72971493), ('bed for kids and adults', 0.724908)]

print(autocomplete('red'))
# ['red light bulb', 'red area rug 5x8', 'red lighting bulb', 'red LED light bulb', 'red brown farm rug']
print(autosuggest('red'))
# [('red light bulb', 0.6643039), ('colored light bulb red', 0.6152657), ('red lighting bulb', 0.5931589), ('red and green decor night light', 0.5804265), ('red ambiance light bulb', 0.5620998)]

print(autocomplete('nautical furniture'))
# []
print(autosuggest('nautical furniture'))
# [('furniture with nautical elements', 0.9628852), ('nautical coastal furniture for living room', 0.8871477), ('nautical style furniture for entryway', 0.8692392), ('Nautical map bar furniture', 0.81977165), ('unique boat-shaped dining furniture', 0.79033804)]
```

That's it! Now you can use an LLM to extract queries and phrases from documents for your search system.