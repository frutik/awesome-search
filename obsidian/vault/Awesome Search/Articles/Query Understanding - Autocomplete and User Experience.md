---
title: "Autocomplete and User Experience"
source: "https://queryunderstanding.com/autocomplete-and-user-experience-421df6ab3000"
author:
  - "[[Daniel Tunkelang]]"
published: 2018-09-01
created: 2026-05-15
description: "How autocomplete affects user behavior and experience in search, including design considerations for helpful vs. harmful suggestion systems — part of the Query Understanding series."
tags:
  - clippings
---

# Autocomplete and User Experience

Part of the **Query Understanding** series by [[Daniel Tunkelang]].

## Overview

Autocomplete has a profound effect on user behavior: users often select from suggestions rather than completing their own queries. This makes suggestion quality critically important — both for search success and for avoiding user harm.

## UX Considerations

**Speed of appearance**
- Suggestions must appear within ~100ms to feel responsive
- Debouncing: don't query on every keystroke, wait for pause

**Number of suggestions**
- 5-8 suggestions is the standard range
- Too few: low coverage; too many: overwhelming

**Diversity**
- Don't show 5 near-identical suggestions
- Cover different intents implied by the prefix

**Visual design**
- Distinguish query completions from entity suggestions
- Show category labels, product thumbnails where helpful
- Keyboard navigability (accessibility)

## Behavioral Effects

- Users anchor to suggestions — if good, faster success; if bad, diverted from intent
- Suggestion acceptance rates (clickthrough) are high (30-50%)
- Poor suggestions can harm conversion rates

## Problematic Suggestions

- Offensive or inappropriate completions (risk of reputational harm)
- Legally sensitive suggestions (need moderation)
- Biased suggestions (can reinforce stereotypes)

## Quality Metrics

- Suggestion acceptance rate (CTR on suggestions)
- Time to first result click after autocomplete use
- Zero-result rate for accepted suggestions

> Note: Article content behind Medium paywall — accessible at source URL with Medium account.


## Related Concepts

- [[Autocomplete]]
- [[Query Understanding]]
- [[Zero Results]]

## People

- [[Daniel Tunkelang]]
