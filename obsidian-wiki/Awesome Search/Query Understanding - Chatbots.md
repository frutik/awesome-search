---
title: "Query Understanding and Chatbots"
source: "https://queryunderstanding.com/query-understanding-and-chatbots-5fa0c154f"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How query understanding powers chatbot-based search interfaces and the unique challenges of conversation-driven information retrieval — part of the Query Understanding series."
tags:
  - clippings
---

# Query Understanding and Chatbots

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Chatbots that help users find information must integrate query understanding with dialogue management. Unlike traditional search, chatbot search requires managing conversation state, understanding references across turns, and generating natural language responses.

## Chatbot Search Architecture

**Components**
1. **Natural Language Understanding (NLU)**: Intent classification + entity extraction from user utterance
2. **Dialogue State Tracking**: Maintain context across conversation turns
3. **Query Construction**: Build search query from dialogue state + current utterance
4. **Search Execution**: Retrieve results from search backend
5. **Response Generation**: Convert results to natural language response

## Dialogue Challenges

**Reference resolution**
- "Show me that in blue" → resolve "that" to previously mentioned product
- "What about a cheaper option?" → maintain category/attribute context

**Ellipsis handling**
- "What about in size L?" → ellipsis of implicit subject (the product just discussed)

**Intent switching**
- User abandons current search intent mid-conversation
- System must detect and handle gracefully

## NLU for Chatbot Search

- **Intent classification**: What does user want to do? (search, filter, compare, buy)
- **Entity extraction**: What entities did they mention? (product, brand, attribute, value)
- **Slot filling**: Progressively fill required search parameters

## Modern Chatbot Search

LLM-powered chatbots (ChatGPT plugins, Perplexity, Bing Chat) have simplified some of these challenges by using the LLM itself for:
- Intent understanding
- Multi-turn context management
- Natural language query-to-retrieval translation
- Response synthesis

But challenges remain around hallucination, attribution, and latency.

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Agentic Search]]
- [[Search Intent]]

## People

- [[Daniel Tunkelang]]
