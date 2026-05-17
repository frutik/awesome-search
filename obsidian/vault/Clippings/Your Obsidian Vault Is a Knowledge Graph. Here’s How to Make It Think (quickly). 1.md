---
title: "Your Obsidian Vault Is a Knowledge Graph. Here’s How to Make It Think (quickly)."
source: "https://medium.com/graph-praxis/your-obsidian-vault-is-a-knowledge-graph-heres-how-to-make-it-think-quickly-1487614a7682"
author:
  - "[[Alexander Shereshevsky]]"
published: 2026-04-11
created: 2026-05-17
description: "More"
tags:
  - "clippings"
---
[Open in app](https://play.google.com/store/apps/details?id=com.medium.reader&referrer=utm_source%3DmobileNavBar&source=post_page---top_nav_layout_nav-----------------------------------------)

Sidebar menu

[](https://medium.com/?source=post_page---top_nav_layout_nav-----------------------------------------)

[

Search

](https://medium.com/search?source=post_page---top_nav_layout_nav-----------------------------------------)

![Andrew Kornilov](https://miro.medium.com/v2/resize:fill:64:64/0*Q1V5FFCsbN98zCDU.)

[

## 

Graph Praxis



](https://medium.com/graph-praxis?source=post_page---publication_nav-4877625dfe3e-1487614a7682---------------------------------------)

·

Follow publication

# Your Obsidian Vault Is a Knowledge Graph. Here’s How to Make It Think (quickly).

[

](https://medium.com/@shereshevsky?source=post_page---byline--1487614a7682---------------------------------------)

Follow

More

![](https://miro.medium.com/v2/resize:fit:1400/1*AVgvTJTFCdvywVkChliZrA.png)

_Following the yes LLM Wiki / no LLM Wiki debate, I want to share my experience from the last five years of building a second brain in Obsidian. Connecting it to Claude Code showed me what I’d been leaving on the table._

I opened my first Obsidian vault in 2021. It was a mess — a migration dump from Evernote, Notion, and a decade of text files scattered across three computers. Five years later, that vault holds over 5,000 notes spanning my consulting work, personal research, investment theses, and the day-to-day texture of life — meeting notes, book highlights, half-finished ideas, and the kind of thinking you only do when you know nobody’s watching.

Obsidian became load-bearing infrastructure for me. Not in the productivity-influencer sense. In the sense that when a client asks me to synthesize six months of project history, I open my vault instead of my email. When I’m evaluating a company, I pull up my investment framework note and the industry research I’ve accumulated over the years. When I need to write something, the first draft already exists as fragments scattered across a hundred notes.

But here’s what I couldn’t do: I couldn’t ask the vault a question. I couldn’t say “what connects my distributed systems notes to my organizational design notes?” and get an actual answer. The knowledge was all there — linked, tagged, structured — but the only thing that could traverse it was me, manually, one note at a time.

That changed when I connected Claude Code to my vault. And it changed more than I expected.

![](https://miro.medium.com/v2/resize:fit:1400/1*dKW1Un2pPrjlsSy5jIwkDQ.png)

## What Most Obsidian-AI Guides Get Wrong

Most integration guides start with the tool. Install this plugin. Configure this server. Here’s a JSON blob. They miss the fundamental insight that makes the whole thing work.

Claude Code wasn’t built for note-taking. It was built to navigate codebases — read files, understand structure, follow references, make targeted edits, and execute multi-step plans. An Obsidian vault maps onto this almost perfectly. A codebase has source files, import statements, directory structure, and configuration. Your vault contains Markdown notes, wikilinks, folder hierarchies, and YAML front matter. Claude Code navigates them with similar fluency.

The simplest integration is the most underrated:

cd ~/my-vault  
claude

That’s it. Claude Code can now read every note, create new files, edit content, search with regex, and run shell commands against your vault. No plugins, no servers, no configuration.

But “can access files” is table stakes. The five years I’d spent structuring my vault — the conventions, the folder architecture, the linking patterns — that’s what makes the integration actually useful. And teaching Claude those conventions is where the real work begins.

## CLAUDE.md: The File That Changes Everything

When you run `claude` in a directory, it automatically reads a file called `CLAUDE.md` at the root. Think of it as onboarding documentation for an extremely capable new hire who will forget everything between sessions.

I run `/init` the first time, which generates a starting point by scanning my vault structure. Then I rewrite it heavily. The generated version captures the obvious stuff — folder names, file types. But it doesn't know my conventions, my active projects, or the things I need Claude to never touch.

Here’s what five years of vault discipline taught me to put in CLAUDE.md:

# Vault Context  
This is my personal + professional knowledge vault. Five years   
of notes across consulting, investing, and distributed systems   
research, and personal development. Notes use Obsidian-flavored   
Markdown with [[wikilinks]], callouts, and YAML frontmatter.  
## Structure  
- Projects/ - active client and personal work  
- Areas/ - ongoing domains (health, finance, ML research)  
- Resources/ - reference material, book notes, papers  
- Archive/ - completed work (still searchable, not active)  
- _attachments/ - images and PDFs (NEVER modify)  
- _templates/ - Obsidian templates (NEVER modify)  
- _ai-drafts/ - staging area for AI-generated content  
## Conventions  
- Internal links: always [[wikilinks]], never bare URLs  
- Tags: hierarchical #domain/topic format  
- MOCs: prefixed "MOC - " (Maps of Content)  
- Daily notes: Journal/YYYY/YYYY-MM/YYYY-MM-DD.md  
- Source notes: must include `source:` in frontmatter  
## Rules  
- NEVER modify _attachments/, _templates/, or .obsidian/  
- NEVER delete notes without my explicit confirmation  
- Always include YAML frontmatter: date, tags, aliases  
- When synthesizing, use ONLY content from my notes  
- Output drafts to _ai-drafts/ - never directly into the vault  
## Active Context (I update this before each session)  
- Working on: Q2 client architecture review  
- Open questions: containerization strategy for legacy systems  
- Recent focus: Areas/distributed-systems/, Projects/client-acme/

Three non-obvious practices I’ve learned matter more than the template itself:

**Keep the Active Context fresh.** I update this section before every session. Stale context is worse than no context — it sends Claude charging down yesterday’s priorities. Even better: at the end of each session, I ask Claude to append a brief session log. That creates continuity I didn’t expect to value as much as I do.

**Reference, don’t inline.** My interests, active projects, and professional context live in separate notes. CLAUDE.md references them. This keeps the root file focused and avoids burning tokens on context that isn’t relevant to every session.

**Include negative instructions.** “Never modify _templates/” is more effective than hoping Claude will figure it out. I learned this the hard way when an early session helpfully “improved” one of my Templater scripts.

![](https://miro.medium.com/v2/resize:fit:1400/1*1WAo1CVe5mylgt_WyImeww.png)

## The Knowledge Graph You Already Have

Here’s what clicked for me after years of linking notes: my vault isn’t just a folder of Markdown files. It’s a graph database.

Every Obsidian vault contains an implicit graph. Notes are nodes. Wikilinks create edges — when you write `[[Distributed Consensus]]` in your Raft notes, you've created an edge from one concept to another. Individual wikilinks are directed (note A links to note B), but Obsidian's backlinks feature creates a bidirectional navigation layer, so you can traverse connections in either direction. Tags act as labels grouping nodes into subgraphs. Frontmatter properties become node attributes that graph-aware tools can query and filter.

Obsidian’s Graph View shows you this structure. It’s beautiful. But it’s passive — it can’t reason over the graph, can’t tell you which notes are hubs, can’t identify the clusters that should be connected but aren’t.

After 5,000 notes and five years of linking, my graph has real structure worth analyzing. And this is where Claude Code — especially through MCP servers with graph capabilities — fills a gap that Obsidian itself doesn’t.

## Graph Metrics That Actually Matter

Once you connect Claude Code to your vault via an MCP server that supports graph operations, you unlock analysis I used to do by eye (badly) or not at all:

**Centrality ranking** identifies your true hub notes — the concepts that connect to the most other concepts. I discovered that my actual hubs don’t always match my “official” MOCs (Maps of Content). My note on “Feedback Loops” had 38 incoming links across four domains. My MOC for Systems Thinking had 7. That mismatch was a sign I needed to restructure.

Here’s what a centrality query looks like in practice using TurboVault:

> get_centrality_ranking(limit=5)  
  
1. Feedback Loops - 38 connections (Areas/systems-thinking,   
   Projects/client-acme, Resources/books)  
2. MOC - Distributed Systems - 34 connections  
3. Bayesian Reasoning - 29 connections (bridges 3 clusters)  
4. Second-Order Effects - 26 connections  
5. Margin of Safety - 24 connections (Areas/investing,   
   Projects/portfolio)

**Orphan detection** finds notes with zero incoming or outgoing links. In my vault, I had 340 orphans — ideas I captured but never connected. Some were worth integrating. Most were archive candidates. Either way, I didn’t know they existed until I asked.

**Cluster analysis** reveals natural groupings and, more importantly, which clusters are disconnected. My investing notes and my systems thinking notes were two separate islands despite obvious conceptual overlap. That was an integration opportunity I’d been missing for years.

**Bridge note identification** finds the rare notes that connect otherwise isolated clusters. These are often your most original insights — the places where you’ve drawn connections between fields that other people keep separate.

## The Tools: What Actually Works

I tested every major integration path. Here’s what I’d recommend, ranked by increasing complexity.

## Tier 1: Direct Filesystem (Start Here)

Just run `claude` from your vault root. Add CLAUDE.md. Install the official [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) — five skill files from Obsidian CEO Steph Ango that teach Claude Code the full Obsidian format: wikilinks, callouts, Bases, Canvas, and the CLI. Without them, Claude treats `[[wikilinks]]` as broken Markdown and `> [!warning]` as a blockquote.

npx skills add git@github.com:kepano/obsidian-skills.git

This combination — CLI + CLAUDE.md + skills — handles 80% of what I need. I used just this for the first two months.

## Tier 2: MCP Server (When You Need Structured Search)

When my vault crossed 2,000 notes, raw file access started feeling slow for search-heavy workflows. MCP servers expose your vault as structured tools that Claude Code can invoke programmatically: search, frontmatter operations, tag management, graph traversal.

My recommendation for most people — **MCPVault**: zero Obsidian plugin dependencies, 14 methods, BM25-ranked search, and 40–60% smaller token usage from response compression. Set it up in your Claude config:

`~/.claude.json`:

{  
  "mcpServers": {  
    "obsidian": {  
      "command": "npx",  
      "args": ["@bitbonsai/mcpvault@latest", "/path/to/your/vault"]  
    }  
  }  
}

For deeper Obsidian integration, **obsidian-claude-code-mcp** runs an MCP server inside Obsidian itself with WebSocket auto-discovery — run `claude`, type `/ide`, and select your vault from the list. For semantic (meaning-based) search, **obsidian-mcp-tools** integrates with the Smart Connections plugin to find conceptually related notes even when they share no common terms.

## Tier 3: Graph Analysis (For Large, Heavily-Linked Vaults)

**TurboVault** is the power tool — a Rust engine with 47 specialized tools, sub-500ms BM25 search on 100,000 notes, SQL queries against frontmatter, and the graph analysis capabilities (centrality, clusters, bridges) that I described above. If your vault has 10,000+ notes or you care about graph-level insights, this is worth the setup.

**obsidian-mcp-plugin** takes a different approach — it exposes your vault as a connected knowledge graph with multi-hop traversal, backlink analysis, and concept discovery. The AI navigates the graph structure itself rather than treating notes as isolated files.

## Tier 4: Embedded Plugins (For Sidebar Devotees)

Plugins like [Claudian](https://github.com/YishenTu/claudian) and [Cortex](https://forum.obsidian.md/t/plugin-cortex-an-ai-obsidian-vault-agent-powered-by-claude-code/112430) embed Claude directly in Obsidian’s sidebar with persistent sessions and active-note awareness. The UX is seamless, but you’re dependent on plugin maintenance. I prefer the CLI for its flexibility — but if you live in Obsidian all day, the sidebar experience is compelling.

## Workflows That Earn Their Keep

Not every AI workflow sticks. These are the ones I still use weekly after months of iteration.

## Automated Backlinking (The Gateway Drug)

Read my journal entry for today and add [[wikilinks]] to all   
people, places, and books mentioned. Search the vault for   
existing notes on each entity. If no note exists, create a   
stub in Resources/People/ or Resources/Places/ with basic   
frontmatter.

This was my first Claude Code workflow, and it’s still the one with the highest ROI. What used to take me 10–15 minutes of manual linking now happens while I wait. After three months of consistent use, my daily journal entries went from dead-end notes to richly connected nodes in the graph. The compounding effect is real — each linked entry gives Claude better context for the next one.

## Cross-Domain Synthesis

This is the workflow that made me rethink what a vault is for:

Read my notes in Areas/distributed-systems/ and   
Areas/organizational-design/. Identify concepts that appear   
in both domains or that share structural similarities.   
Write a synthesis note at _ai-drafts/cross-domain-synthesis.md   
mapping the parallels. Use ONLY content from my notes —   
do not add external claims. Include [[wikilinks]] to all   
source notes.

Claude found connections I hadn’t made explicit: my notes on consensus protocols and on decision-making in flat organizations described the same coordination problem from different angles. That synthesis note became the seed of a conference talk. I would not have written it manually — not because I couldn’t, but because the activation energy of reading 40 notes across two folders and holding them all in working memory was too high.

## Vault Health Audit (Monthly Maintenance)

==Find all orphan notes (no incoming or outgoing links),   
notes missing YAML frontmatter, and broken wikilinks.   
Output a report at _ai-drafts/vault-health-report.md.==

I run this monthly. It’s the PKM equivalent of running your test suite. Before I started, my vault had a 9% orphan rate and wildly inconsistent frontmatter. Six months of monthly audits brought orphans below 2% and frontmatter compliance above 95%.

## Gap Analysis

Examine Areas/investing/ and list topics that are serious   
practitioner would expect to find, but aren't covered by   
any existing note.

Claude identified that my investing notes covered valuation and moats extensively but had almost nothing on position sizing, risk management, or portfolio construction. That gap had been invisible to me for three years because the notes I _did_ have felt comprehensive.

## Quick CLI Piping

claude -p "Summarize Resources/RFID/ in 200 words" \  
  > Resources/RFID-summary.md

The `-p` (or `--print`) flag runs Claude non-interactively and outputs to stdout. I use this for batch operations — generating summaries for entire folders, extracting key claims from research notes, or creating stub notes from a list of topics.

## Why Obsidian + Claude, Not Notion AI or Logseq + GPT

I’ve tried the alternatives. Here’s why I keep coming back:

**Local files, not cloud lock-in.** My vault is a folder of Markdown files on my filesystem. I own them. I can `grep` them, `git` them, back them up, or switch tools tomorrow. Notion AI is powerful, but your data lives on Notion's servers in a proprietary format. When I give Claude Code access to my vault, it reads the same files I edit in Obsidian — no sync layer, no API translation, no data leaving my machine.

**Agentic, not autocomplete.** Most AI integrations in PKM tools are autocomplete on steroids — you type, they suggest. Claude Code is an agent. It can read 40 notes, determine which are relevant, create new files, add wikilinks, and report on what it did. The difference between “AI-assisted writing” and “AI-assisted knowledge management” is the difference between a better keyboard and a research assistant.

**Composable, not monolithic.** I can swap MCP servers and change my CLAUDE.md, add skills, pipe output through shell scripts, or use a completely different AI model tomorrow. The architecture is layers of plain text and open protocols. Nothing is locked in.

Claude Code requires a Max subscription or API usage, which incurs costs, and that's worth acknowledging. For my usage patterns — a few sessions per week, each touching 20–50 notes — the cost is a rounding error compared to the consulting hours it saves. Your math will vary, but it’s worth tracking for the first month.

## Safety Practices You’ll Wish You’d Set Up First

I learned these through mistakes. Set them up before your first session.

**Use git for your vault.** This is the single most important safety net. Every change Claude makes becomes a reviewable diff. Every mistake becomes reversible.

cd ~/vault  
git init  
echo ".obsidian/workspace.json" >> .gitignore  
echo "_attachments/" >> .gitignore

Review staged files before your first commit — make sure you’re not accidentally tracking sensitive data.

**Route all AI outputs through** `**_ai-drafts/**`**.** Claude's work is a draft until you've reviewed it. Never let it write directly into your main vault structure. Promote notes manually after review. This preserves your vault as a repository of _your_ thinking.

**Always constrain synthesis prompts.** “Use ONLY content from my notes” is not optional. Without it, Claude mixes your knowledge with its training data, and the result looks authoritative but contains claims you never made. I add this constraint to every synthesis and summary request — it’s the PKM equivalent of input sanitization.

**Scope requests to specific folders.** “Summarize Resources/quantum-computing/” is safe and fast. “Summarize my entire vault” is a token bomb that produces shallow results.

## The Compound Effect

The real payoff isn’t any single workflow. It’s what happens over months of consistent AI-assisted maintenance.

After three months of automated backlinking, my daily notes transformed from dead-end entries into connected nodes. After six months of vault health audits, my orphan rate dropped from 9% to under 2%. After running a gap analysis on each knowledge domain, I started writing notes that fill structural holes rather than piling onto already dense clusters.

The graph gets denser, more connected, and more navigable — for both me and the AI. Better-linked notes give Claude better context, which produces better suggestions, which create better links. Each improvement compounds.

This is the trajectory that the Zettelkasten method promised, but few people achieve manually. The organizational work — backlinking, tagging, formatting, consistency — is exactly what AI excels at. You bring the thinking. Claude brings the bookkeeping.

## Getting Started This Week

If you’ve read this far and haven’t started, here’s the 30-minute setup:

1. **Install Claude Code** — `npm install -g @anthropic-ai/claude-code`
2. **Initialize** — `cd ~/vault && claude` then `/init`
3. **Rewrite CLAUDE.md** — use the template above, tailored to _your_ vault structure and conventions
4. **Install obsidian-skills** — `npx skills add git@github.com:kepano/obsidian-skills.git`
5. **Run your first audit** — “Find all orphan notes and notes missing YAML frontmatter. Output a report to _ai-drafts/vault-audit.md.”

And here’s the Week 1 challenge to push past the tutorial stage: automate backlinking on 7 daily notes. Run your first vault health audit. Ask Claude to find connections between your two most separate knowledge domains. By Friday, you’ll have a measurable sense of whether this transforms your workflow or is just another shiny tool.

I’m betting on the former. Five years of building my vault made it valuable. Connecting it to an agent that can actually think with it made that value accessible in ways I hadn’t imagined.

The graph was always there. Now something can traverse it.

_Open-source tools referenced:_ [_kepano/obsidian-skills_](https://github.com/kepano/obsidian-skills) _(official agent skills),_ [_MCPVault_](https://github.com/bitbonsai/mcpvault) _(zero-dependency MCP server),_ [_TurboVault_](https://github.com/Epistates/turbovault) _(Rust graph analysis),_ [_obsidian-claude-code-mcp_](https://github.com/iansinnott/obsidian-claude-code-mcp) _(WebSocket integration),_ [_obsidian-mcp-tools_](https://github.com/jacksteamdev/obsidian-mcp-tools) _(semantic search),_ [_Claudian_](https://github.com/YishenTu/claudian) _(sidebar plugin). Star counts and features are current as of April 2026._

260

1

[

Knowledge Graph

](https://medium.com/tag/knowledge-graph?source=post_page-----1487614a7682---------------------------------------)

[

Obsidian

](https://medium.com/tag/obsidian?source=post_page-----1487614a7682---------------------------------------)

[

Claude Code

](https://medium.com/tag/claude-code?source=post_page-----1487614a7682---------------------------------------)

[

Graphrag

](https://medium.com/tag/graphrag?source=post_page-----1487614a7682---------------------------------------)

[

LLM

](https://medium.com/tag/llm?source=post_page-----1487614a7682---------------------------------------)

260

1

[

![Graph Praxis](https://miro.medium.com/v2/resize:fill:128:128/1*rUElHORNRlPmVu9QZUkR-A.png)



](https://medium.com/graph-praxis?source=post_page---post_publication_info--1487614a7682---------------------------------------)

Follow

[

## Published in Graph Praxis

](https://medium.com/graph-praxis?source=post_page---post_publication_info--1487614a7682---------------------------------------)

[247 followers](https://medium.com/graph-praxis/followers?source=post_page---post_publication_info--1487614a7682---------------------------------------)

·[Last published May 6, 2026](https://medium.com/graph-praxis/what-music-recognition-can-teach-anti-money-laundering-d1cd23efb41a?source=post_page---post_publication_info--1487614a7682---------------------------------------)

Where knowledge graph theory meets production reality. Enterprise architectures for Graph RAG, dynamic ontologies, and AI agents that actually remember.

[

![Alexander Shereshevsky](https://miro.medium.com/v2/resize:fill:128:128/1*Yam5uYmyyy1ZE3QqSBDekA.jpeg)



](https://medium.com/@shereshevsky?source=post_page---post_author_info--1487614a7682---------------------------------------)

Follow

[

## Written by Alexander Shereshevsky

](https://medium.com/@shereshevsky?source=post_page---post_author_info--1487614a7682---------------------------------------)

[602 followers](https://medium.com/@shereshevsky/followers?source=post_page---post_author_info--1487614a7682---------------------------------------)

·[36 following](https://medium.com/@shereshevsky/following?source=post_page---post_author_info--1487614a7682---------------------------------------)