---
title: "You Say Search, I Say Recs: A Scalable Agentic Approach to Query Understanding and Exploratory Search at Spotify"
source: "https://research.atspotify.com/publications/you-say-search--i-say-recs-a-scalable-agentic-approach-to-query-understanding-and-exploratory-search-at-spotify"
author:
published:
created: 2026-05-15
description: "Spotify's official technology blog"
tags:
  - "clippings"
---
### Abstract

On online content platforms, users often aim to explore the catalog and discover new, personalized content through exploratory searches—such as "new releases for me." Traditional search systems, which prioritize lexical and semantic matching over personalized retrieval, have historically struggled to support this type of intent. In contrast, recommendation services that leverage user-item and item-item signals tend to be more effective for addressing exploratory queries. Agentic technologies offer a promising opportunity to enhance exploratory search by harnessing large language models (LLMs) to interpret complex query intents and route them to the most suitable downstream services. However, deploying such agentic systems at scale remains a significant challenge. In this paper, we present a scalable agentic approach to query understanding and exploratory search at Spotify. Our system combines an LLM router, post-training adaptation techniques, search and recommendation APIs, and specialized sub-agents to interpret user intent and deliver personalized results at scale. We outline the high-level system design and share key experimental results. By addressing the limitations of conventional search, our approach yields substantial improvements across several exploratory use cases, including discovering similar artists (+115%), broad podcast searches (+15%), new music releases (+91%), and broad music searches (+25%).

[View publication](https://dl.acm.org/doi/10.1145/3705328.3748127)