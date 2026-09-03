# Claude Skills — Awesome Search

Skills for building and maintaining the Awesome Search knowledge graph in Obsidian, and for learning about search and IR.

## Knowledge Graph — Processing

| Skill | Trigger | What it does |
|---|---|---|
| `kg-article-processing` | Article URL, or a title/name of an already-clipped article/video not yet processed | Fetch → detect paywall → save the Article/Video source note; hands off to `kg-note-writing` |
| `kg-note-writing` | Handed off from `kg-article-processing`, or directly for "write/enrich a topic (or concept/person/company/tool) note" with no new source | Extract and normalize entities → create/update notes with correct frontmatter → add wikilinks and ground every claim, whether against fetched source text or existing vault notes |
| `awesome-search-knowledge-graph` | Invoked at the end of `kg-note-writing` (or standalone to repair invariants) | Graph-wide maintenance pass: History log entry, `kg-reviewer` audit, `global_toc.md`, `index.md`/`HOME.md` mirror |
| `awesome-search-tutor` | "Explain X", "what do practitioners think about Y" | Fetches articles from the README and answers questions about IR and search |
| `kg-plan-processing` | "queue this for processing", "add this to planned", `/kg-plan-processing <url-or-topic>` | Queues one article/video URL or topic into root-level `planned/` for later parallel processing — write only, doesn't fetch or dispatch |

## Knowledge Graph — Publishing

| Skill | Trigger | What it does |
|---|---|---|
| `kg-readme-writer` | After vault changes, or `/kg-readme-writer` | Syncs root `README.md` with the latest History weeks and `global_toc.md`, wikilinks converted to site links |
| `kg-mail-list` | `/kg-mail-list [<year>.<week>]`, or "write this week's email" | Compiles the week's History entries into a plain-language HTML digest at `mails/<year>.<week>.html`, no statistics |
| `kg-draft-to-html` | `/kg-draft-to-html [<draft>]`, or "render this draft to HTML" | Renders one `drafts/*.md` essay into a self-contained page at `drafts/html/<stem>.html` in the same house style — a faithful format conversion, never an edit |

## Knowledge Graph — Quality Audits

Run in this order for best results: **frontmatter → orphans → hubs → clusters**
— or run `kg-audit` instead, which does all four (plus duplicate-article and
broken-wikilink detection) in a single script-driven pass.

| Skill | What it checks | Output |
|---|---|---|
| `kg-audit` | All of the below in one pass, via `scripts/kg_audit.py` (filesystem-based, not MCP — the one deliberate exception, for speed at 800+ notes), plus duplicate-source articles, unresolved wikilinks, and a README-sync check (README.md is derived from global_toc.md + the newest History weeks and drifts silently) | Consolidated report; read-only, no writes |
| `kg-frontmatter` | Missing required frontmatter fields (`type`, `source`, `author`, `created`, `tags`, `concepts`) by note type | Violation report by folder; auto-fixes where values can be inferred |
| `kg-orphans` | Notes with zero inbound and outbound wikilinks | Triaged list (integrate / stub / noise); optionally adds missing links |
| `kg-hubs` | Inbound link counts ranked across all notes; compared against `Topics/` | Flags mismatches where high-traffic concepts lack a topic page, and under-linked topic pages |
| `kg-clusters` | Groups of notes that are internally linked but isolated from the rest of the graph | Suggests bridge links between disconnected clusters; surfaces existing bridge notes |
