# Claude Skills — Awesome Search

Skills for building and maintaining the Awesome Search knowledge graph in Obsidian, and for learning about search and IR.

## Knowledge Graph — Processing

| Skill | Trigger | What it does |
|---|---|---|
| `awesome-search-knowledge-graph` | Article URL, note title, or "process/enrich this note" | Full KG ingestion pipeline: fetch article → extract entities → create/update notes → add wikilinks across articles, concepts, people, companies, topics |
| `awesome-search-tutor` | "Explain X", "what do practitioners think about Y" | Fetches articles from the README and answers questions about IR and search |

## Knowledge Graph — Quality Audits

Run in this order for best results: **frontmatter → orphans → hubs → clusters**

| Skill | What it checks | Output |
|---|---|---|
| `awesome-search-kg-frontmatter` | Missing required frontmatter fields (`type`, `source`, `author`, `created`, `tags`, `concepts`) by note type | Violation report by folder; auto-fixes where values can be inferred |
| `awesome-search-kg-orphans` | Notes with zero inbound and outbound wikilinks | Triaged list (integrate / stub / noise); optionally adds missing links |
| `awesome-search-kg-hubs` | Inbound link counts ranked across all notes; compared against `Topics/` | Flags mismatches where high-traffic concepts lack a topic page, and under-linked topic pages |
| `awesome-search-kg-clusters` | Groups of notes that are internally linked but isolated from the rest of the graph | Suggests bridge links between disconnected clusters; surfaces existing bridge notes |
