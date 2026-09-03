---
name: kg-draft-to-html
description: Render a long-form draft from drafts/*.md into a self-contained HTML page at drafts/html/<stem>.html, in the same house style as the mailing-list digests (Georgia, 640px, inline CSS, "Best, Andrew" sign-off). A faithful format conversion only — the draft's words, order and structure are never edited, summarised or rewritten. Triggers on `/kg-draft-to-html [<draft>]` or "make an HTML version of this draft" / "render the draft to HTML".
---

# Awesome Search — Draft to HTML

Turns one hand-written draft in `drafts/` into a single standalone HTML file
that can be pasted into an email, attached, or opened in a browser.

This is a **published artifact, not a vault note** — like `kg-readme-writer`'s
README.md and `kg-mail-list`'s digests. Vault conventions (approval, History
entries, `kg-reviewer`, wikilink resolution) do not apply, and the output is
written outside `obsidian/vault/`.

## When to use

- `/kg-draft-to-html [<draft path or name>]`
- "make an HTML version of this draft", "render the draft to HTML",
  "turn drafts/foo.md into HTML"
- No draft given → list the `.md` files in `drafts/` and ask which one.
  Never guess, and never render all of them unasked.

## Output

- `drafts/html/<stem>.html`, where `<stem>` is the draft's filename without
  `.md` (`drafts/llm-judge-agreement-plain-talk.md` →
  `drafts/html/llm-judge-agreement-plain-talk.html`). Create `drafts/html/`
  if missing.
- One file per draft. Re-running overwrites it — the draft is the only truth,
  and the HTML is a derived file that is never hand-edited. If someone has
  hand-edited the HTML, those edits are lost; say so before overwriting when
  you have reason to suspect it.

## The hard rule: convert, never rewrite

This skill is a **renderer, not an editor**. Every word, sentence, heading,
table row, list item and link in the draft comes out in the same order with
the same wording. Specifically, do not:

- summarise, tighten, expand or re-voice any passage;
- strip statistics, counts or numbers — unlike `kg-mail-list`, whose no-stats
  rule exists because it *derives* an email from History entries, this skill
  reproduces a document the author already wrote;
- rewrite `[[wikilinks]]` into site links, or resolve them at all — they stay
  verbatim as plain text (the script reports any it finds so the author can
  decide);
- reorder sections, drop a trailing section, add a preamble, or invent a
  subtitle, dateline or byline the draft does not have;
- fix the draft's typos, grammar or facts. If something looks wrong, mention
  it in your summary and leave the file alone — the fix belongs in the
  Markdown, not in the HTML.

The only additions to the author's text are the fixed `<head>` (title +
inline CSS) and the fixed footer sign-off, both described below.

## Procedure

1. Resolve which draft to render (argument, or ask). Accept a bare name
   (`llm-judge-agreement-plain-talk`) as well as a path.
2. Run the renderer from the repo root:

   ```sh
   python3 claude-skills/kg-draft-to-html/scripts/draft_to_html.py drafts/<name>.md
   ```

   It is stdlib-only Python 3, no dependencies. `-o <path>` overrides the
   default output location. **Use the script rather than hand-writing the
   HTML** — hand conversion of a 300-line essay is where paraphrase and
   dropped paragraphs creep in.
3. Read the script's report: output path, the `<title>` it picked, and any
   `[[wikilinks]]` left verbatim.
4. Spot-check the output — that the last section of the draft is present,
   that tables and blockquotes rendered as such, and that no `&amp;amp;` or
   stray `<` escaping artefacts appear.
5. Stage the file with `git add drafts/html/<stem>.html` (add-only — never
   commit or push; that stays the user's call).
6. Report: which draft was rendered, where the HTML went, the page title, and
   any wikilinks or unsupported constructs worth the author's attention.

## Page shape

Same house style as `mails/<year>.<week>.html` — self-contained, minimal,
valid HTML with no external stylesheets, scripts, fonts or images, so it
renders correctly with no network access.

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title><the draft's first H1, markup stripped></title>
<style> /* Georgia, max-width 640px, inline */ </style>
</head>
<body>
<h1>...</h1>          <!-- the draft's own H1, in place -->
...                   <!-- the draft's body, converted -->

<hr>
<p>Best,<br>Andrew</p>
</body>
</html>
```

- The `<title>` is the draft's first level-1 heading with `*`/`` ` ``/`_`
  stripped; if the draft has no H1, it falls back to `Draft` and the script
  says so — that is a cue to add an H1 to the Markdown, not to invent one in
  the HTML.
- The H1 stays where the author put it; there is no separate dateline unless
  the draft itself has one as body text.
- The footer is fixed and always present, exactly `<hr>` followed by
  `<p>Best,<br>Andrew</p>` — a sign-off, never a place for counts, credits or
  boilerplate.

## What the renderer supports

Headings (h1–h6), paragraphs, `---` horizontal rules, fenced code blocks
(with a `language-*` class), blockquotes, bullet and ordered lists including
nesting, and pipe tables with the `:---:` alignment row. Inline: `**strong**`,
`*em*`/`_em_`, `` `code` ``, `[text](url)`. YAML frontmatter is stripped.
Everything is HTML-escaped exactly once, so `&`, `<` and `>` in prose and in
URLs survive intact.

Known gaps: reference-style links, footnotes, inline HTML and images all
come through as literal text, and a setext heading's `===`/`---` underline
becomes a horizontal rule with the heading text left as a paragraph — so use
`#`-style headings in drafts. The drafts don't currently use them; if a
draft starts to, extend `draft_to_html.py` rather than hand-patching its
output.
