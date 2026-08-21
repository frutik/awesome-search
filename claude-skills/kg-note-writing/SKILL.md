---
name: kg-note-writing
description: Write, enrich, or synthesize any Awesome Search KG entity note (Concept, Topic, Person, Company, Tool, Conference, Case Study, Dataset) — extract/normalize entities, create or update notes with correct frontmatter and structure, cross-link them, and ground every claim. Two entry points both use this skill — (1) handed off from kg-article-processing with freshly fetched source text to extract entities from, and (2) a direct request to write or enrich a note, most often a Topic, by synthesizing across notes already in the vault with no new external source (e.g. "write a topic note for X pulling together what we have on it", "connect these notes into a topic page", "enrich/link this existing concept note").
---

# KG Note Writing

This skill owns the mechanics of authoring a KG entity note, independent of
where the grounding material comes from. There are two entry points:

- **From a source** — `kg-article-processing` fetched an article or video,
  handled the paywall case, saved the Article/Video note, and hands off its
  text here. Entities are extracted from that text.
- **Synthesis, no new source** — the user asks directly for a note (typically
  a Topic, but a Concept works the same way) that ties together material
  already in the vault, with nothing new fetched. There is no "article text";
  the grounding basis is the existing notes you gather and link.

Everything below applies to both — substitute "the source text" for "the
existing related notes you've identified" wherever grounding is mentioned.

## Goal

Turn the grounding material (fetched source, or existing vault notes) into a
dense but meaningful set of connections inside the graph. Prefer creating
high-quality conceptual connections when substantial thematic overlap exists
with notes already in the vault.

## Supported Entities

The single source of truth for what this skill can extract, where it lives,
and how to store it. Every other section below refers back to this table
rather than re-listing entity types — if a new entity type is ever added, add
it here once.

| Entity type | Folder | What it is | Key frontmatter fields |
|---|---|---|---|
| Concept | `Concepts/` | A specific technical idea, method, algorithm, or term | `type: concept`, `aliases:`, `tags:` |
| Topic | `Topics/` | A broader thematic area grouping multiple concepts/trends/domains | `type: topic`, `aliases:`, `related_concepts:`, `related_topics:`, `articles:`, `website:` |
| Person | `People/` | An author, researcher, or practitioner | `type: person`, `aliases:`, `website:` or `blog:`, `affiliation:` |
| Company | `Companies/` | An organisation mentioned in the grounding material | `type: company`, `website:` |
| Tool | `Tools/` | A library, platform, or product | `type: tool`, `website:`, `repo:` |
| Conference | `Conferences/` | A named conference or recurring event referenced as the venue/source of a talk, paper, or claim | `type: conference`, `aliases:`, `website:`, `organizer:` (wikilink) |
| Case Study | `Case Studies/` | A concrete real-world implementation, experiment, or deployment | `type: case_study`, `companies:`, `related_concepts:`, `source:` |
| Dataset | `Datasets/` | A named benchmark or evaluation dataset (e.g. MS MARCO, BEIR, Natural Questions) | `type: dataset`, `aliases:`, `website:` or `repo:`, `related_concepts:` |

**Not authored by this skill, for reference only** — created by
`kg-article-processing`, which follows this same table:

| Entity type | Folder | What it is | Key frontmatter fields |
|---|---|---|---|
| Article | `Articles/` | Source note for a processed article | `type: article`, `source:`, `author:`, `published:`, `concepts:`, `topics:`, `paywall: true` (only when paywalled) |
| Video | `Videos/` | Source note for a processed talk/video | `type: video`, `title:`, `speaker:` (wikilink), `company:` (wikilink), `url:`, `published:`, `topics:`, `concepts:`, `tools:`, `people:` |

## Vault Access

**Always use the Obsidian MCP server for all vault operations** — never
access the vault directly via the filesystem (no Read/Write/Bash file tools).
The MCP server is the only sanctioned way to read, search, create, and edit
notes.

## Workflow

### 0. Establish the grounding basis (synthesis entry point only)

If there is no fetched source text — i.e. you were asked directly for a
synthesis note — first search the vault for the existing notes the new note
should draw on and link to. These notes *are* your source: every claim in the
new note must trace back to one of them (or to well-established, uncontroversial
background knowledge). If the request names specific notes, start there; also
search for related notes that weren't named but clearly belong.

Skip this step when entering from `kg-article-processing` — the source text
already serves this role.

### 1. Extract entities

Identify instances of the entity types listed in **Supported Entities**
above.

Rules:
- Only extract explicitly stated or strongly supported entities.
- Avoid trivial/incidental mentions unless likely to recur across multiple sources.

### 2. Normalize entities
- Use stable canonical forms; no duplicates under slightly different names.
- Do not merge distinct entities from the same company/product family.
- "agentic retrieval", "agentic search" → shared canonical concept when semantically equivalent.
- Prefer separate notes over incorrect merges.

### 3. Create or update entity notes

Auto-create/update a note per entity, per **Supported Entities** above
(folder + frontmatter fields). Article and Video source notes are created by
`kg-article-processing`, not here.

### 4. Add Obsidian wikilinks
Connect: articles/videos ↔ concepts ↔ people ↔ companies ↔ topics

### 5. Apply linking rules
- Prioritize meaningful relationships, especially when entities are central to the source or strongly connected to existing notes in the vault.
- Prioritize entities that appear repeatedly or are central to the argument.
- Preserve relationship types: `author_of`, `discusses`, `implements`, `compares_to`, `critiques`, `works_for`
- **Factual**: must be explicitly stated or strongly supported by the grounding material.
- **Semantic**: may be inferred when concepts, topics, or discussions substantially overlap.
- Acceptable to create conceptual links between related search, IR, ranking, recommendation, retrieval, and agentic-system topics even when the relationship is implicit.

### 6. Connect authors through shared concepts
If multiple authors write about the same concept → connect them via shared concept notes.

### 7. Related Notes sections
Include "Related Notes" sections only for strongly related concepts/entities.

### 8. Authorship rule
Do NOT assume someone invented something unless explicitly stated.

### 9. Grounding (mandatory, invisible)

The note must be true to its grounding material — but nothing about grounding
appears in the note itself. No tags, no labels, no "(source)" markers. Clean
prose only.

Before saving, silently check every claim:
- Specifics — numbers, dates, quotes, author names, affiliations, benchmark
  results — must come from the source text, or from the existing notes you're
  synthesizing. Never fill these from memory.
- "X invented / created / introduced Y" — only if the grounding material says so.
- A relationship link (`implements`, `compares_to`, `critiques`, "builds on") —
  only if both the grounding material and the linked note actually support it.
- Everything else must be either a well-established, uncontroversial fact or
  clearly written as tentative ("appears to", "likely"). If it's neither, cut it.

Paywalled / thin sources, or thinly-linked synthesis material, mean MORE
caution, not confident gap-filling.

### 10. Preserve external URLs
Always capture URLs found in the grounding material:
- **Conferences/events**: official website URL in note body and frontmatter as `website:`
- **Companies**: official website in frontmatter as `website:`
- **People**: personal blog, homepage, or primary professional URL in frontmatter as `website:` or `blog:`; also as a clickable link in note body
- **Tools**: repository (GitHub) and/or docs URL in frontmatter as `website:` and `repo:`; also in note body
- Preserve links to external resources (papers, talks, repos, blog posts) in the relevant entity note — do not discard URLs found in the grounding material.
- Prefer the most canonical/stable URL (official site > GitHub > Medium profile).

## Note Structure

All notes must follow this structure:

```markdown
---
# frontmatter: see the Supported Entities table above for the fields for this entity type, plus a `created` date on every note
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

## Handing off

Writing/enriching notes is only half the job. Once the notes above are
created or updated, invoke the **awesome-search-knowledge-graph** skill to run
the graph-wide maintenance pass (History log entry, `kg-reviewer` audit and
fixes, `global_toc.md`, `index.md`/`HOME.md` mirror) before reporting
completion — do not consider the batch done until that pass has run.
