---
type: article
title: "Amazon OpenSearch Service now offers AI-assisted migrations"
source: "https://aws.amazon.com/about-aws/whats-new/2026/06/amazon-opensearch-service-ai-migrations/"
author: "[[Amazon Web Services]]"
published: 2026-06-23
created: 2026-07-01
tags:
  - article
  - opensearch
  - solr
  - elasticsearch
  - migration
  - agentic
  - aws
concepts:
  - "[[Search Platforms]]"
topics:
  - "[[Migration between Search Engines]]"
  - "[[Elasticsearch vs OpenSearch]]"
companies:
  - "[[Amazon Web Services]]"
---

# Amazon OpenSearch Service now offers AI-assisted migrations

[[Amazon Web Services]] announcement: **Migration Assistant for Amazon OpenSearch Service** now includes an **AI-assisted experience** that simplifies moving self-managed [[Solr]], [[Elasticsearch]], or [[OpenSearch]] deployments to **OpenSearch Serverless** or **Managed Clusters**.

---

## What's new

- **Agent-guided workflow.** Users drive the migration with AI coding tools — AWS names **Kiro** and **Claude Code** — to *plan* a migration, *deploy* the necessary infrastructure, and *execute* both historical and live-traffic migration.
- **Live traffic capture and replay for Solr.** Previously available for Elasticsearch/OpenSearch, capture-and-replay now extends to Solr sources.
- Positioned as a reliability play: migrations traditionally need weeks of planning and remain error-prone; the agentic workflow helps structure, execute, and *validate* the migration faster and more reliably.

## Background

- Migration Assistant first launched in **December 2023** to automate manual tasks in moving existing and live data from self-managed clusters to Amazon OpenSearch Service.
- Supports migrations to **OpenSearch Serverless** and **Managed Clusters** from various Solr, Elasticsearch, and OpenSearch versions.
- Available in all commercial AWS Regions and AWS GovCloud (US) Regions where Amazon OpenSearch Service is offered.

## Why it matters

This is one of the first vendor-native applications of **agentic coding tools to search-platform migration**. Platform migration is a recurring, high-risk theme across this vault — see [[Migration between Search Engines]]. Where the [[Vinted - Migrating Search from Elasticsearch to Vespa|Vinted]] and [[Kleinanzeigen - Vespa Migration for Homepage Feed|Kleinanzeigen]] case studies show hand-built ES→Vespa migrations, AWS is instead automating Solr/ES/OpenSearch → OpenSearch with an LLM agent orchestrating planning, infrastructure, and traffic cutover.

## Related Concepts

- [[Search Platforms]] — the source/target engine landscape
- [[Elasticsearch vs OpenSearch]] — target-engine context

## Related Notes

- [[Migration between Search Engines]] — hub for platform-migration approaches
- [[Vinted - Migrating Search from Elasticsearch to Vespa]] · [[Kleinanzeigen - Vespa Migration for Homepage Feed]] — hand-built migrations for contrast
- [[How I learned Vespa by thinking in Solr]] — cross-engine mental mapping (the manual analog of what the assistant automates)
- [[Innovating Search Experience with Amazon OpenSearch and Amazon Bedrock]] — another AWS-native OpenSearch article

## Companies

- [[Amazon Web Services]] — publisher; Amazon OpenSearch Service / Migration Assistant
