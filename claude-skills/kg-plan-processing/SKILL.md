---
name: kg-plan-processing
description: Queue a single article/video URL (or a bare topic name) into the repo-root planned/ directory for later parallel processing — writes the queue file only, does not fetch or process it now. Triggers on "queue this for processing", "add this to planned", "queue <url>", or /kg-plan-processing <url-or-topic>. Does not dispatch the queue or write vault content — see .claude/agents/kg-writer.md for how queued items later get processed (one kg-writer agent per file, spawned directly, not through this skill).
---

# KG Plan Processing

Adds one item to the `planned/` work queue. This skill only *enqueues* — it
never fetches a URL, never writes vault content, and never spawns
`kg-writer`. Dispatching the queue (spawning one `kg-writer` agent per queued
file, in parallel) is a separate, manual step done directly with the Agent
tool per `.claude/agents/kg-writer.md`, not something this skill does.

If there's no batch intent — the user just wants one URL processed right
now — skip this skill entirely and invoke `kg-article-processing` (or
`kg-note-writing` for a topic with no new source) directly instead.

`planned/` lives at the repo root (sibling to `obsidian/`, `claude-skills/`),
not inside the vault — it's a task queue, not vault content, so use plain
filesystem tools (Read/Write/`ls`) on it, not the Obsidian MCP server.

## Workflow

1. Take the input: a URL (article or video) or a bare topic/entity name.
2. Check it isn't already queued or already processed — grep the URL/topic
   string against `planned/*.md`, `planned/done/*.md`, and (via the Obsidian
   MCP server) existing `Articles/`/`Videos/`/entity notes in the vault. If a
   match turns up, don't silently skip or silently requeue it — stop and ask
   the user what to do (AskUserQuestion), stating where the existing copy is
   (which file/note) and offering choices such as: skip (leave it as is,
   recommended default), queue it anyway (e.g. to force reprocessing), or
   view/open the existing item first. Proceed to step 3 only once they answer.
3. Derive a filename slug: for a URL, slugify the URL itself (strip
   scheme, replace non-alphanumerics with `-`); for a topic, slugify the
   topic name. Don't fetch the URL to get a title — that's `kg-writer`'s job
   when it's later dispatched, not this skill's.
4. Write `planned/<slug>.md` containing exactly one line — the URL or topic
   name, nothing else — per the one-liner format in
   `.claude/agents/kg-writer.md`. Create `planned/` if it doesn't exist yet.
5. Report the file written and, briefly, what it'll produce when processed
   (a new Article/Video note plus extracted entities, or a topic/concept
   enrichment).

## Notes

- Multiple calls (one per URL) queue multiple files — this skill handles one
  item per invocation; queueing several items is just calling it several
  times.
- This skill deliberately stops after writing the file. It does not check
  whether other items are already queued and does not suggest dispatching
  them — that's a separate decision the user makes.
