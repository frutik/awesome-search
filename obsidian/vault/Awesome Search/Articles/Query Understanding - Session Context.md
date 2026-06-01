---
title: "Session Context"
source: "https://queryunderstanding.com/session-context-4af0a355c94a"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How search systems use the history of queries within a session to better understand evolving user intent — part of the Query Understanding series."
tags:
  - clippings
---

# Session Context

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

A user's current query rarely exists in isolation — it typically follows other queries in the same session, and those prior queries reveal a great deal about what the user is actually trying to accomplish. Session context uses this history to resolve ambiguity and anticipate needs. A sequence of queries that progressively narrows in on a topic tells the system something different than a sudden shift in direction. Applying session context well requires knowing when earlier queries are still relevant and when the user has genuinely moved on to a new intent. It also introduces privacy considerations, since session data is necessarily tied to individual user behavior, and latency considerations, since incorporating session state adds overhead to each query.

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Query Understanding]]
- [[Session-Based Evaluation]]
- [[Click Signals]]

## People

- [[Daniel Tunkelang]]
