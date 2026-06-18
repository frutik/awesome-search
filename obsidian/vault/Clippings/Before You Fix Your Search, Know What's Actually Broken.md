---
title: "Before You Fix Your Search, Know What's Actually Broken"
source: "https://unscriptedai.substack.com/p/before-you-fix-your-search-know-whats"
author:
  - "[[Atita Arora]]"
published: 2026-06-16
created: 2026-06-18
description: "10 recurring patterns across every vertical. A self-slotting guide to knowing which search problem you're actually holding."
tags:
  - "clippings"
---
![](https://substackcdn.com/image/fetch/$s_!faqo!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F938c9a92-d597-495f-bab3-9d9465c8f347_800x2000.jpeg)

In 1974, the systems theorist Russell Ackoff wrote something that has aged uncomfortably well:  
  
***“Successful problem solving requires finding the right solution to the right problem. We fail more often because we solve the wrong problem than because we get the wrong solution to the right problem.” - Russell Ackoff***  
*Source -* Although he is primarily known for his systems thinking movement (https://fearlessrevival.com/russell-ackoff/) and has written and spoken about management systems, reading through his work, I feel he could have been talking about every search engagement I have walked into.  
  
Decades later, Udi Manber - who had led search at Amazon, Yahoo,Google and Youtube, names the exact misperception that makes this worse:  
***“Many people believe that search is essentially a solved problem, and it just works”***  
*Source: [https://www.linkedin.com/pulse/qa-udi-manber-google-search-guru-amir-konigsberg/](https://www.linkedin.com/pulse/qa-udi-manber-google-search-guru-amir-konigsberg/)* Most teams I work with aren't failing because they picked the wrong engine. They're failing because they're solving the wrong problem entirely.  
  
There have been a lot of interesting use cases and teams I have worked with in past 2 decades and I have walked into this situation, more than I’d like to admit -  
A team is deep into a sophisticated implementation of search, powered by every possible fancy bells and whistles - LTR, Vector Search, custom plugins and what not.  
Weeks of feature engineering, complicated index and training pipelines, mostly without but sometimes also with evaluation.  
The model looks good in the lab, until someone asks - ***“Define a good result from your user’s perspective?”***  
  
Silence.  
  
Not incompetence. The team is sharp. But nobody has formally defined relevance. No evaluation framework. No judgment lists. No shared answer to what success means when a user types a query.  
  
The model is optimising a signal nobody has verified maps to user satisfaction. Sometimes there are KPIs and sometimes not, most of them have spent watching classic conference talks and have chosen proxy metrics discussed by their favorite speaker. It is convenient but is it valid?  
This gap between lab and production isn’t a model bug - it is a foundation problem and no amount of ranking sophistication or vectors fixes it.  
  
Because what they essentially have is a measurement problem and/or alignment problem.  
Search operating in a silo, optimising for metrics which are not aligned or understood by the business.  
  
I usually go back to Ackoff and some of his work to get a handle!  
  
I have worked across search and retrieval and lately AI boosted features in ecommerce, health, media, finance, legal, enterprise, government platforms and quite recently also geospatial applications, marketplaces to systems processing thousands of queries, millions of documents from federated sources. The stacks vary, maybe even the team sizes but the misdiagnoses do not.

I agree that for search problems we always tend to reach out and fix understandably “root cause” at the search engine level while the real blocker may be something more fundamental.

What I have come to believe is that most search problems are not unique. They are in fact the instances of a small number of recurring patterns and the most valuable thing you can do before investing in a solution is correctly identifying which pattern you are in.

**Let’s put you on the map!**

The following ten archetypes cover the majority of search problems I have encountered across domains. Your situation may sit between two of them, or shift as your problem matures, but being able to name yours changes everything about what you do next and inspect first - data model before ranking or evaluation before architecture or data extraction before relevance.  
  
1\. **The uniqueness problem** - One of a kind inventory - usually seen in Marketplaces, pre-owned, handmade or classifieds.  
  
**How you know you’re here -**  
\- Difficult to leverage standard taxonomies (“handcrafted ceramic bowl” does not neatly fit into “kitchenware”)  
\- Freshness is existential (an item sold is gone)  
\- Demand signals are thin  
\- Delivery time, distance from seller, condition and pricing competition carry the relevance definition equally as the item attributes  
\- Catalog/Inventory stability is always concernful  
\- Query vocabulary is also not standardized - users search for what they imagine the thing may be called and it may be listed - classic vocabulary mismatch problem

**  
2\. The complexity machine** - Flip case of uniqueness problem - every product has multiple variants - colour, size, pattern along with deeply structured attributes - usually seen in classic e-commerce, retail, fashion, health & wellness, price comparison platforms.

**How you know you’re here -**  
\- variant-heavy catalog - Master / Variant SKUs articles  
\- fundamentally different user intents - known item / sku searches and exploratory weaved into a single query pipeline tuned for neither  
\- Sponsored products handling with relevance pipeline in an organic way  
\- Personalisation / Membership adding on top of relevance  
\- Classic LTR / Semantic search investment candidates (.. without evals and judgement lists in place:P!)

**  
3\. The precision mandate -** Contrary to the #1 and #2 which can be more recall focussed, in precision mandate problems a plausible-but-wrong result is worse than no result at all.  
Correctness, auditability and scope matters as much as relevance - usually seen in legal, research, tax and compliance, clinical tools and regulatory industries.

**How you know you’re here -**  
\- Recall is not enough - Precision is the king!  
\- Domain terminology usage - legal / finance / medical  
\- Confidence, result lineage and provenance, are first class requirements NOT nice to have.  
\- Scope correctness matters and plays a big role in relevance - returning something from the wrong jurisdiction, wrong revision (version) or wrong rate range is a fail

**  
4\. The firehose pattern -** Unlike #1, #2 and #3 where catalog volatility is measured in days or for most part the corpus is relatively stable, in this pattern time or better expressed as “content freshness” is the first grade issue here, which puts authority, recency and trend in the front seat of relevance definition. This is usually seen in news / media platforms, social media content discovery, live sport / event platforms.

**How you know you’re here -**  
\- Recency and relevance are in constant tug of war mode, the most relevant doc is years old, while the most recent may not have any reference to searched topic  
\- Often authority and credibility is explicitly part of relevance definition and not inferred  
\- Query volume is unpredictable and can spike around major news or event  
\- Personalisation is given and welcome even when sessions are anonymous  
\- Working with this use case feels like working with moving target

**5\. The Extraction pattern** - This one is close neighbour to #4 and is often seen on use cases that are an extension of the ones in #4 With a focus on information extraction, this pattern points to the use cases where the consumer is a machine, a pipeline or an agent and the information retrieval is served on extracted structured information from unstructured inputs at low latency. This is a classic pattern usually seen in news or feed inspired use cases like financial news turned into tradeable events or web content turned into categorised feeds, research pipelines, market data or crypto mining and/or agent driven retrieval.

**How you know you’re here -**  
\- Traditional relevance evals fail to be applicable  
\- Latency and throughout are first class constraints, not an add-on  
\- Precision of extracted info structure matters the most  
\- Noise is a first order problem - an irrelevant extracted info or failure to extract relevant information has compounding consequences.  
\- Schema drift is a real problem here as the world changes faster than extraction model and creates unknown / silent failures

**6\. The Media vault -** The last 4 patterns we saw essentially have a mix of text and multimedia catalog, while for this one the focus of the catalog is not text, but is images, videos, audio or mixed media documents. The query may often be conceptual or emotional, more so a mood or a creative direction than just a keyword.  
Metadata is the search surface and is also usually incomplete, inconsistent or entirely missing (:D)  
This is usually seen in use cases with stock photos, enterprise digital assets, publishing archives, creative platforms and video platforms.

**How you know you’re here -**  
\- Metadata sparsity as the ingestion pipeline matured over time leaving large portions of catalog invisible to tags and text based retrieval.  
\- Naming convention of an asset mismatch / all numbers / random names - no correlation with what’s in the asset.  
\- The wishful aspiration is to use semantic search or visual/multimodal search but lexical layer may still be handling most of the search  
\- Another nuance here is rights and restrictions (licenses) that play a role in relevance.  
\- Popularity signals driven by downloads, saves,view, favorites also play proxy in relevance even though they are sparse and biased (presentation / position / popularity bias:D)

**7\. The Knowledge Graph -** The use cases or problems where an answer is a composite of information from multiple documents and the relationships between entities - concepts, product information, ingredients, assembly, roles, skills, regulation or jurisdictions. The correctness and accuracy is often defined by how well the entities are mapped. Taxonomies, Ontologies quality or their absence become a real bottleneck than just disturbance in retrieval model.  
This is often seen in combination with the use cases prone to precision mandate problems along with procurement platforms, industrial /professional or talent networks, regulatory and compliance platforms and sometimes also in supplier or ingredient centric platforms like in gastronomy too.  
  
**How you know you’re here  
**\- User browse more than search with initial query being a starting point  
\- Filter, facet and taxonomy depth are differentiators but often unclear which brings more value  
\- Heavy synonyms files and old well maintained ontologies are hyped and very dear to the teams  
\- The document relationship often disguised as nested structures (supplier -> product -> certification -> conforming regulation) for queries like “halal supplier in 10963”  
\- Personalisation requires traversing multiple levels  
  
**8\. Geospatial use cases -** This one is quite unique as this may exist as part problem in any use case dependent on location / distance as a bolted on filter too. While the geospatial location could also be a first class dimension and criterion for location focussed use cases requiring focus on specific AOI (Area of Interest) shape and what defines the relevance. The complexity is not limited to a city filter but plays a big role in terms of distance, proximity, bounding box and spatial relationship which is intrinsic to correctness.  
Along with other use cases / problems above it can individually be seen in Satellite and aerial imagery platforms, urban planning and govt platforms, mapping and territorial platforms.

**How you know you’re here  
**\- Distinct spatial query types and index standardization to serve it at architecture level like bounding box, radius, polygon as these are often not served by standard search methods.  
\- Resolution and coverage makes or breaks search and can often result in false confidence.  
\- Interplay of Administrative boundary and jurisdiction  
\- Coordinate system and projection mechanism can create query time errors  
\- Search and GIS are separate sets of expertise,and are often perennial projects to align them on common ground.

**9\. Q-commerce use cases -** This is classic ecommerce problems definition with a tinge of handling real time demand and supply signal with delivery times and geospatial nuances. This is probably the most operationally constrained archetype with an interplay of Retrieval scope, ranking, availability and geo spatial criterion. This is not classic relevance but is real time relevance living in operational state.  
This is a pattern often seen in food delivery, q-commerce, ride hailing, on-demand services, logistics where the fulfillment window is a determining ranking signal.

**How you know you’re here  
**\- Supply side fulfilment and filters are often confused with query side sophistication  
\- Substitutes are core requirement but is treated as an edge case  
\- Personalisation is dire needed but may result in filtering out all the relevant matches  
\- Misalignment between - Search measuring q-rels (query-document relevance judgments) while business caring about fulfilled orders and delivery times

**10\. The Code Search -** Code search doesn’t fit cleanly in one single type and precisely what makes it instructive. It inherits traits from knowledge graph, correctness expectation of precision mandate and bit of firehose and extraction too. Understanding it requires the pattern it is built from.

This is mostly seen in coding agents, version control platforms, api docs, code review and dependency scanning.

**How you know you’re here  
**\- Playing with utmost ambiguity in query intent - is the query file name, function, class, call chain, property and that answers the granularity needed for a satisfactory answer.  
\- code repo is a graph - inheritance, calls, structure  
\- plausible but wrong answers between versions or deprecated calls  
\- Vocabulary mismatch / semantic search is not incidental - conn\_rety, retryConnection, connection\_rety, retry\_on\_connection\_error and non canonical form

**Disclaimer - there can be more archetypes and I would love reader’s thoughts!**

**A note before you close this tab!**  
  
I am glad you made it this far!

The hardest part of this article is not finding your archetype.  
It is accepting that you might be in a different one than you think.  
  
***Most teams self diagnose - “we need better ranking”, “we need vector search”, “we need a better model”.***  
It is the comfortable answer and it sounds sophisticated and may as well justify next quarter’s roadmap but your problem definition is just a symptom, not a diagnosis.  
  
The team I spoke about in the opener was not wrong about LTR being valuable.  
They were wrong about the order of execution. The similar distinction (as pointed out by Russell Ackoff) between **the right solution** and **the right solution to the right problem** and where most search investments quietly go to die.

So before you go and fix things -**  
This map is more of a starting point and not a territory or a verdict, use it to orient, not to conclude.  
**

**\-Most real systems sit between archetypes or outgrow the one they started as.**  
A small marketplace that lands a big retail partner suddenly has variants, suppliers and sponsored products problems, the one it did not have before. This is not a failure or the existing system - it is growth and a shift of archetype and so should the diagnosis.

**\- The same symptom may mean different things depending on where you are.  
**Take classic Zero results - In ecommerce (Uniqueness problem / Complexity Machine) - it is wasted real estate. You could show related products, substitutes, trending articles but never let user hit a dead end. While in precision mandate - zero results is often better than showing something marginally similar to a regulation or a legal precedent. Same metric on the same dashboard but opposite prescription.

**\- The archetype definition points which layer to fix first and not how to fix (No Solution mode yet)  
**If you are in the Uniqueness problem, reranking sophistication will not fix data modelling gaps or for a complexity machine problem, switching to a “better” embedding model will not fix the real problem of blending sponsored products with organic results, as search team optimises relevance and business tries to push revenue from sponsored products. There is no shared definition or understanding. So sequence matters and most teams skip to solutions before the problem is correctly discovered.

**Note on measurement - just because its measurable doesn’t mean its useful /helpful in your case!**

If you read this and immediately knew which archetype defines your use case - great.  
The next posts will go deeper in each one and what actually moves the needle, what common misdiagnoses look like and how to sequence the work.

If you read this and couldn’t decide between two (...or maybe three or more:P ) - that is also a good sign as it may mean that you’re sitting at a transition point and this may help you clarify which problem you’re solving is overdue.

**What about Agentic Retrieval?**

Agentic retrieval is not a separate archetype (let this one sit!:P) It is a consumption pattern that sits on top of whichever archetype your system already belongs to.  
An agent doing financial research is operating in the extraction pattern while the reviewing legal documents agent is operating in the precision mandate pattern.

Also the change is not because the consumer is now an agent rather than a human typing a query.  
What changes is the evaluation contract. The framework built for human experience breaks entirely when a downstream agent acts on results autonomously. A wrong result that a human would catch and ignore becomes a wrong action an agent executes without question. So the precision, result confidence and scope correctness all become harder requirements - not nice-to-haves.

Hence jumping straight to *“we need agentic ….”* without defining what problem are we in or trying to solve is just another version of the same mistake this whole article is about:D  
  
*If this resonated, subscribe. There’s more where this came from.*