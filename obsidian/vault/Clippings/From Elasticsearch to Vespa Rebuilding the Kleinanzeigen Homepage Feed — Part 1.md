---
title: "From Elasticsearch to Vespa: Rebuilding the Kleinanzeigen Homepage Feed — Part 1"
source: "https://medium.com/berlin-tech-blog/from-elasticsearch-to-vespa-rebuilding-the-kleinanzeigen-homepage-feed-part-1-b6164e366ab8"
author:
  - "[[Andre Charton]]"
published: 2026-05-22
created: 2026-05-26
description: "More"
tags:
  - "clippings"
---
Why We Started Looking at Vespa

The Kleinanzeigen homepage feed is the first thing millions of users see when they open the app. For years, we powered it with Elasticsearch. The approach was straightforward: we maintained user profiles outside of Elasticsearch, fired keyword and attribute queries in real time, and assembled a feed from the results. It worked, but it had limits.

The core problem was that we were doing too much work outside the search engine. Profile learning, scoring, and retrieval were stitched together across multiple services. Every new signal — a click, a search keyword, an explicit preference — required a round-trip through our own orchestration layer. Scaling the personalization logic meant scaling everything that depended on it.

We wanted something that could:

👤 Store and query user behavioral profiles inside the search engine alongside ads  
⚡ Use WAND (Weighted AND) for fast inner-product retrieval over sparse attribute vectors without scanning every document  
🧠 Run embedding-based ANN search natively, close to the data  
🔄 Process click and search events as document updates within the platform itself  
  
Vespa offered all of that, so we started experimenting.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*al2n1YoK09OP1opVwwmT9g.png)

### The Starting Point: Infrastructure First

We first ran a proof of concept, learned what we didn’t know, and then rebuilt the system properly from scratch.

The first real decisions were infrastructure ones. We chose Vespa Cloud on AWS and deployed it in a European region close to our users. We set up a staging environment that mirrors production, configured private network connectivity for secure access, and split the application into separate read and write containers sharing the same content cluster. This separation lets us tune each independently and keep indexing traffic off the query path.

### The Data Model: Three document schemas

We landed on three schema types in a single content cluster:

**ads:** each classified ad, with its item attributes modeled as a weighted set <string>. The token format follows a field.value pattern (e.g., *color.red*, *brand.bmw*), allowing us to run a single WAND query across structured attributes without secondary indices. This lets us run a single WAND query across all structured attributes without secondary indices.

**user\_category\_profile:** one document per user per category, keyed as {userId}:category:{categoryId}. This contains the user’s click-derived attribute weights (L2-normalized to a shared scoring scale), their last X search keywords, their last clicked document IDs (for exclusion), their geolocation, and their explicit preferences.

**relations:** a global config document per category (replicated to all nodes), defining field importance weights and token similarity groups with propagation coefficients. This is what lets *color.red* contribute partial weight to *color.blue* during retrieval. They share a group with a defined similarity coefficient.

### Phase 1: WAND-Based Click Profile Matching

The first production feature was click profile retrieval. When a user clicks an ad, we fire a document update to Vespa. A Vespa document processor intercepts this update, asynchronously reads the clicked ad’s attributes and the existing user profile, and updates the profile in-process: existing signals decay over time, the new click is merged in, and the profile is trimmed to keep only the strongest features.

The result stays inside Vespa. No external profile store. No service hop at query time.

At query time, we read the profile, expand tokens through the relations graph, propagate weights to similar attributes, and fire a WAND query against the ads. Vespa’s WAND implementation guarantees that only promising candidates are fully evaluated, so even with millions of ads, we’re not scanning them all.

![](https://miro.medium.com/v2/resize:fit:1400/format:webp/1*1CuJ0vrogs4RqnS8EK0n4A.png)

By this point, we had proven something important: Vespa could own the full click-profile loop end-to-end. User behavior updates, profile maintenance, and retrieval all happened inside the serving platform itself, without external orchestration or profile storage. The system was faster, operationally simpler, and easier to evolve than the Elasticsearch setup it replaced.

But click history alone only tells part of the story…

Many users arrive with a strong intent before they ever click anything. Explicit preferences, especially in categories like Fashion, carry semantic meaning that behavioral signals alone cannot infer quickly enough. The next step was teaching the system how to combine learned behavior with directly expressed user intent.

That became the focus of Phase 2: integrating explicit preferences, advanced ranking strategies, and eventually semantic retrieval into the homepage feed architecture.

Continue with Part 2 of this series, where my colleague explores explicit preferences, ranking strategies, and semantic retrieval in more detail ✨.