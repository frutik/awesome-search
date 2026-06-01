---
name: awesome-search-knowledge-graph
description: Build and maintain a dense semantic knowledge graph about search and IR inside an Obsidian vault. Triggers on article URLs, article titles or names (from Clippings/, raw_articles/, or unprocessed vault notes), and requests to enrich or reprocess existing notes for concepts, people, companies, tools, or topics.
---

# Awesome Search Knowledge Graph

Use this skill when the user asks to process any article into the knowledge graph. Triggers include:

- A URL to a new article to fetch and process
- A title or name of an article already in the vault (e.g. in `Clippings/`, `raw_articles/`, or `Awesome Search/Articles/`) that hasn't been fully processed yet
- A request to process, enrich, or link an existing note that is missing entity extraction, wikilinks, or related notes
- A request to update or reprocess a topic, concept, person, company, or tool note

## Goal

Build a dense but meaningful semantic knowledge graph inside Obsidian. Prefer creating high-quality conceptual connections when substantial thematic overlap exists.

## Vault Structure

- `Awesome Search/Articles/` — one note per processed article
- `Awesome Search/Concepts/` — technical ideas, methods, algorithms
- `Awesome Search/Topics/` — broader thematic areas
- `Awesome Search/People/` — authors, researchers, practitioners
- `Awesome Search/Companies/` — organisations mentioned
- `Awesome Search/Case Studies/` — real-world implementations

## Vault Access

**Always use the Obsidian MCP server for all vault operations** — never access the vault directly via the filesystem (no Read/Write/Bash file tools). The MCP server is the only sanctioned way to read, search, create, and edit notes.

## Invariant: index.md mirrors HOME.md

After every workflow run (or any operation that modifies `HOME.md`), read the current content of `HOME.md` and overwrite `index.md` with that exact content. These two files must always be identical. Do this as the final step before reporting completion.

## Workflow

When asked to read/process articles, follow these steps in order:

### 1. Download the article
Fetch the full article content from the provided URL using WebFetch. No confirmation needed.

### 1a. Detect paywall
After fetching, determine whether the full article body is accessible:

**Paywall signals** (any of these → treat as paywalled):
- Fetched text is significantly shorter than expected for an article (< ~300 words of body content)
- Content is cut off mid-sentence or ends with a subscription/login prompt
- Text contains phrases like "Subscribe to read", "Members only", "Sign in to continue", "This content is for subscribers", "Create a free account to read"
- Only a lede or first few paragraphs are present with no further detail

**If paywalled — aggressive summary mode:**
1. Work only from the content that was retrieved (title, lede, abstract, visible snippets).
2. Write a dense, information-maximising summary: core thesis, key claims, named entities, and any specific techniques or findings that are visible — no padding, no hedging.
3. Add frontmatter field `paywall: true` to the article note.
4. Add a prominent notice at the top of the note body:
   ```
   > [!warning] Paywall
   > Full text unavailable. Summary based on publicly visible content only.
   > Original article: <URL>
   ```
5. Still extract whatever entities, concepts, and links are inferable from the visible content.
6. Skip steps that require full article body (e.g. detailed section breakdown), but complete all other workflow steps normally.

**If not paywalled** — proceed normally through the rest of the workflow.

### 2. Save the article note
Save to `Awesome Search/Articles/<Title>.md` using the standard note structure (see below).

### 3. Extract entities
- **concepts** – specific technical ideas, methods, algorithms, terminology
- **topics** – broader thematic areas grouping multiple concepts/trends/domains
- **people**, **companies**, **tools**
- **case studies** – concrete real-world implementations, experiments, deployments

Rules:
- Only extract explicitly stated or strongly supported entities.
- Avoid trivial/incidental mentions unless likely to recur across multiple articles.

### 4. Normalize entities
- Use stable canonical forms; no duplicates under slightly different names.
- Do not merge distinct entities from the same company/product family.
- "agentic retrieval", "agentic search" → shared canonical concept when semantically equivalent.
- Prefer separate notes over incorrect merges.

### 5. Create or update entity notes
Auto-create/update: Article notes, Concept notes, Person notes, Company notes, Tool notes.

### 6. Add Obsidian wikilinks
Connect: articles ↔ concepts ↔ people ↔ companies ↔ topics

### 7. Apply linking rules
- Prioritize meaningful relationships, especially when entities are central to the article or strongly connected to existing notes in the vault.
- Prioritize entities that appear repeatedly or are central to the article's argument.
- Preserve relationship types: `author_of`, `discusses`, `implements`, `compares_to`, `critiques`, `works_for`
- **Factual**: must be explicitly stated or strongly supported by the article.
- **Semantic**: may be inferred when concepts, topics, or discussions substantially overlap.
- Acceptable to create conceptual links between related search, IR, ranking, recommendation, retrieval, and agentic-system topics even when the relationship is implicit.

### 8. Connect authors through shared concepts
If multiple authors write about the same concept → connect them via shared concept notes.

### 9. Related Notes sections
Include "Related Notes" sections only for strongly related concepts/entities.

### 10. Authorship rule
Do NOT assume someone invented something unless explicitly stated.

### 11. Preserve external URLs
Always capture URLs found in source material:
- **Conferences/events**: official website URL in note body and frontmatter as `website:`
- **Companies**: official website in frontmatter as `website:`
- **People**: personal blog, homepage, or primary professional URL in frontmatter as `website:` or `blog:`; also as a clickable link in note body
- **Tools**: repository (GitHub) and/or docs URL in frontmatter as `website:` and `repo:`; also in note body
- Preserve links to external resources (papers, talks, repos, blog posts) in the relevant entity note — do not discard URLs found in source material.
- Prefer the most canonical/stable URL (official site > GitHub > Medium profile).

## Note Structure

All notes must follow this structure:

```markdown
---
# frontmatter: type, title/aliases, tags, source (for articles), website/blog/repo (for entities), related_concepts, related_topics, people, companies, created
---

# Title

Brief summary paragraph.

---

## [Content sections]

## Related Concepts
- [[Concept]]

## Related Articles
- [[Article]]

## People
- [[Person]]
```

Use Obsidian-compatible Markdown. Preserve source URLs in frontmatter (`source:`) for article notes.

## Entity Frontmatter Fields

| Entity type | Key frontmatter fields |
|---|---|
| Article | `type: article`, `source:`, `author:`, `published:`, `concepts:`, `topics:`, `paywall: true` (only when paywalled) |
| Concept | `type: concept`, `aliases:`, `tags:` |
| Topic | `type: topic`, `aliases:`, `related_concepts:`, `related_topics:`, `articles:`, `website:` |
| Person | `type: person`, `aliases:`, `website:` or `blog:`, `affiliation:` |
| Company | `type: company`, `website:` |
| Tool | `type: tool`, `website:`, `repo:` |
