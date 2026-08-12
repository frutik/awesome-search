---
type: case-study
company: "[[Delivery Hero]]"
domain: food delivery / multi-market e-commerce search
problem: classify 300K distinct multilingual search terms into a usable taxonomy across 16 markets
scale: 300,000 distinct search terms, 16 markets, multiple languages and scripts
source: "https://deliveryhero.jobs/blog/classifying-300k-noisy-search-terms-across-16-markets/"
author: "[[Hailey Cheong]]"
published: 2026-07-14
topics:
  - "[[Query Classification]]"
  - "[[Query Understanding in Practice]]"
  - "[[Multilingual Search]]"
  - "[[E-commerce Search]]"
concepts:
  - "[[Query Understanding]]"
  - "[[Out-of-Vocabulary]]"
  - "[[Knowledge Distillation]]"
people:
  - "[[Hailey Cheong]]"
created: 2026-08-12
---

# foodpanda — Classifying 300K Noisy Search Terms Across 16 Markets

[[Hailey Cheong]], a Senior Product Analyst at [[Delivery Hero]] working across foodpanda, foodora and Yemeksepeti, needed a classification of foodpanda's search traffic before any analysis of it was possible. The account is unusually candid about the failure modes: the first working classifier put **37% of 300,000 search terms into a bucket called `Others`**, and most of the work was the validation loop that followed.

## Problem

300,000 distinct search terms, 16 markets, multiple languages and scripts. The vocabulary is far messier than a product catalog:

- "McDonald's" alone appears as `mc`, `mcd`, `麥當勞`, and **1,355 further variants**.
- A single character like `m` in the Philippines is simultaneously a brand abbreviation, a typo, and a dead end.

As the author puts it, a pivot table was not going to tell them anything.

## Approach

Three options were weighed. Manual reclassification with regex patterns was too tedious. Google Sheets' `=AI()` function was too slow across 300K rows. Claude Code won on two specific properties: its BigQuery MCP gave the model direct read/write access to the dataset, and every change was automatically written to a `.md` changelog.

The initial prompt followed a structured **role → context → definitions → objective** pattern. Then the validation loop began — described as by far the most tedious yet most important part of the work.

## Three Things the Classifier Got Wrong

### 1. 37% classified as `Others`

The catch-all absorbed everything the model did not recognise: non-English terms, obscure local restaurant names, and food items with no English cognate. The figure looked like a third of the data being unclassifiable noise. It was not noise — it was Turkish offal dishes, Taiwanese beverage chains, and food written in Lao script. The classifier simply did not know them.

**Fix:** re-examine every `Others` term and assign it a **33%, 66%, or 99% confidence** of belonging to another category, factoring in market language and local context — a graded reassignment rather than a forced hard label.

### 2. Biased assumptions on ambiguous terms

The model assumed "pu" in the Philippines meant Puregold (a major supermarket chain), while failing to connect "panda" to Pandamart — over-matching on partial strings in one direction and missing an obvious link in the other.

**Fix:** an intermediate cleanup step grouping similar variants under a canonical label *before* reclassification, removing the incentive to pattern-match on fragments.

### 3. Stale key insights

The model did not cascade logic changes back through previously written output sections, so the "Key Insights" narrative drifted out of coherence with the data points it described.

**Fix:** explicitly prompt "Update Key Insights" after every material change. The author's conclusion is blunt: human-in-the-loop is not optional here.

## Result

The final output was a **deterministic BigQuery classifier** — global chains matched by regex patterns, market-specific brands scoped by country ID, dietary terms determined via keyword lists. No model in the serving path.

- **98.7% classification rate**
- `Others` down from 37% to **1.3%** — a 35.7pp drop

## What to Steal

- **Treat the residual bucket as a vocabulary report, not a noise measurement.** A large `Others` share told the team which markets and cuisines their label set had no words for. That is a finding, not a defect.
- **Canonicalise variants before classifying, not after.** Collapsing 1,355 spellings of one brand to a single label removes most of the ambiguity the classifier would otherwise have to resolve. See [[Semantic Equivalence of e-Commerce Queries]] for the principled version of this step.
- **Grade the residual instead of forcing labels.** Confidence bands on reassignment keep the uncertainty visible rather than converting unknown coverage into unknown error.
- **Use the LLM to author the classifier, then ship rules.** The end artifact is regex, country-scoped brand lists, and keyword lists — inspectable, free to run, and auditable, with the model's contribution frozen at build time.
- **Scope label sets by market.** Global brand patterns and market-specific brand patterns are different mechanisms and were implemented as such.

## Caveats

The account is a practitioner narrative rather than an ML systems write-up. It names no classifier model or held-out evaluation set, and "validation loop" means iterative manual review rather than a measured benchmark. The 98.7% figure is a **coverage** number — the share of terms that received a label — and is not a statement about label accuracy.

## What's Next

The author frames the classifier as a means to an end. Early analysis reportedly reveals a misalignment between search queries and the restaurants currently surfaced — the gap that defines the next phase of the work.

## Related Notes

- [[Query Classification]] — this case study anchors the residual-class and build-time-LLM dimensions
- [[Don't Classify, Hallucinate]] — the opposite resolution of the same closed-vocabulary tension: loosen the model instead of tightening the taxonomy
- [[Multilingual Search]] — transliteration and script coverage as a classification problem
- [[Query Understanding - Language Identification]] — why short multilingual queries resist classification
- [[Uber Eats - Scaling Search for Food Delivery]] — the neighbouring food-delivery query understanding stack
- [[Etsy - Search Quality and Query Understanding]] — long-tail vocabulary defeating standard techniques in a different catalog
