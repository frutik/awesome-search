#!/usr/bin/env python3
"""Render one drafts/*.md file to a self-contained HTML page.

Faithful conversion only: every heading, paragraph, table, list, quote and
code block in the source comes out in the same order with the same words.
Nothing is summarised, reordered, stripped or rewritten — the draft is the
truth, this script is only a renderer.

Supported Markdown subset (everything the drafts actually use, plus code
and footnote-free fallbacks):

  headings h1-h6, paragraphs, hr, fenced code blocks, blockquotes,
  bullet/ordered lists with nesting, pipe tables with alignment row,
  inline: **strong**, *em*/_em_, `code`, [text](url), autolinked bare URLs
  left alone, and [[wikilinks]] kept verbatim as plain text.

Usage:
    draft_to_html.py drafts/foo.md [-o drafts/html/foo.html]
"""

import argparse
import html
import os
import re
import sys

CSS = """\
  body { font-family: Georgia, serif; max-width: 640px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; color: #1a1a1a; }
  h1 { font-size: 1.4rem; margin-bottom: 0.5rem; }
  h2 { font-size: 1.15rem; margin-top: 2rem; }
  h3 { font-size: 1.05rem; margin-top: 1.5rem; }
  h4, h5, h6 { font-size: 1rem; margin-top: 1.25rem; }
  a { color: #0b5fa5; }
  hr { border: none; border-top: 1px solid #ddd; margin: 2rem 0; }
  blockquote { margin: 1.25rem 0; padding: 0 0 0 1rem; border-left: 3px solid #ddd; color: #444; }
  table { border-collapse: collapse; width: 100%; margin: 1.25rem 0; font-size: 0.95rem; }
  th, td { border: 1px solid #ddd; padding: 0.4rem 0.6rem; text-align: left; vertical-align: top; }
  th { background: #f5f5f5; }
  code { font-family: Menlo, Consolas, monospace; font-size: 0.9em; background: #f5f5f5; padding: 0.1em 0.3em; }
  pre { background: #f5f5f5; padding: 0.75rem; overflow-x: auto; }
  pre code { background: none; padding: 0; }
  ul, ol { padding-left: 1.4rem; }
  li { margin: 0.25rem 0; }\
"""

FOOTER = "<hr>\n<p>Best,<br>Andrew</p>"

WIKILINK_RE = re.compile(r"\[\[[^\]]+\]\]")


# --------------------------------------------------------------------------
# inline rendering
# --------------------------------------------------------------------------

def render_inline(text):
    """Escape, then apply inline Markdown. Code spans are protected first."""
    slots = []

    def stash(payload):
        slots.append(payload)
        return "\x00%d\x00" % (len(slots) - 1)

    # code spans win over every other inline construct
    def code_span(m):
        return stash("<code>%s</code>" % html.escape(m.group(1), quote=False))

    text = re.sub(r"`([^`]+)`", code_span, text)
    text = html.escape(text, quote=False)

    # [label](url) — both halves are already escaped at this point; the label
    # may still carry emphasis, the url must not be escaped a second time
    def link(m):
        label, url = m.group(1), m.group(2).strip()
        url = url.replace('"', "&quot;")
        return stash('<a href="%s">%s</a>' % (url, apply_emphasis(label)))

    text = re.sub(r"\[([^\]\[]+)\]\(([^)\s]+(?:\s+&quot;[^&]*&quot;)?)\)", link, text)

    text = apply_emphasis(text)

    # hard line break: two trailing spaces already collapsed by the caller
    for i, payload in enumerate(slots):
        text = text.replace("\x00%d\x00" % i, payload)
    return text


def apply_emphasis(text):
    text = re.sub(r"\*\*(?=\S)(.+?)(?<=\S)\*\*", r"<strong>\1</strong>", text, flags=re.S)
    text = re.sub(r"(?<![\w*])\*(?=\S)([^*]+?)(?<=\S)\*(?![\w*])", r"<em>\1</em>", text, flags=re.S)
    text = re.sub(r"(?<![\w_])_(?=\S)([^_]+?)(?<=\S)_(?![\w_])", r"<em>\1</em>", text, flags=re.S)
    return text


# --------------------------------------------------------------------------
# block parsing
# --------------------------------------------------------------------------

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
HR_RE = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})\s*(\S*)\s*$")
BULLET_RE = re.compile(r"^(\s*)[-*+]\s+(.*)$")
ORDERED_RE = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)$")
QUOTE_RE = re.compile(r"^\s*>\s?(.*)$")
TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")


def strip_frontmatter(lines):
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() in ("---", "..."):
                return lines[i + 1:]
    return lines


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|") and not line.endswith("\\|"):
        line = line[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line)]


def alignments(sep_line):
    out = []
    for cell in split_row(sep_line):
        left, right = cell.startswith(":"), cell.endswith(":")
        out.append("center" if left and right else "right" if right else "left" if left else None)
    return out


def render(lines):
    out = []
    i, n = 0, len(lines)

    while i < n:
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        fence = FENCE_RE.match(line)
        if fence:
            marker, lang = fence.group(1), fence.group(2)
            body, i = [], i + 1
            while i < n and not (lines[i].strip().startswith(marker[0] * 3) and set(lines[i].strip()) == {marker[0]}):
                body.append(lines[i])
                i += 1
            i += 1  # closing fence (or EOF)
            attr = ' class="language-%s"' % html.escape(lang, quote=True) if lang else ""
            out.append("<pre><code%s>%s</code></pre>" % (attr, html.escape("\n".join(body), quote=False)))
            continue

        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            out.append("<h%d>%s</h%d>" % (level, render_inline(heading.group(2)), level))
            i += 1
            continue

        if HR_RE.match(line):
            out.append("<hr>")
            i += 1
            continue

        if line.lstrip().startswith("|") and i + 1 < n and TABLE_SEP_RE.match(lines[i + 1]):
            header = split_row(line)
            aligns = alignments(lines[i + 1])
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            out.append(render_table(header, aligns, rows))
            continue

        if QUOTE_RE.match(line):
            block = []
            while i < n and (QUOTE_RE.match(lines[i]) or (block and is_lazy_continuation(lines[i]))):
                m = QUOTE_RE.match(lines[i])
                block.append(m.group(1) if m else lines[i].strip())
                i += 1
            inner = render(block)
            out.append("<blockquote>\n%s\n</blockquote>" % indent(inner))
            continue

        if BULLET_RE.match(line) or ORDERED_RE.match(line):
            block, base = [], leading(line)
            while i < n and lines[i].strip() and (
                BULLET_RE.match(lines[i]) or ORDERED_RE.match(lines[i]) or leading(lines[i]) > base
            ):
                block.append(lines[i])
                i += 1
            out.append(render_list(block))
            continue

        para = []
        while i < n and lines[i].strip() and not (
            HEADING_RE.match(lines[i]) or HR_RE.match(lines[i]) or FENCE_RE.match(lines[i])
            or QUOTE_RE.match(lines[i]) or BULLET_RE.match(lines[i]) or ORDERED_RE.match(lines[i])
            or lines[i].lstrip().startswith("|")
        ):
            para.append(lines[i].strip())
            i += 1
        if para:
            out.append("<p>%s</p>" % render_inline(" ".join(para)))
        else:  # a construct we bailed on; never loop forever
            out.append("<p>%s</p>" % render_inline(line.strip()))
            i += 1

    return "\n".join(out)


def is_lazy_continuation(line):
    """A bare paragraph line continuing a blockquote — never another block."""
    return bool(line.strip()) and not (
        HEADING_RE.match(line) or HR_RE.match(line) or FENCE_RE.match(line)
        or BULLET_RE.match(line) or ORDERED_RE.match(line) or line.lstrip().startswith("|")
    )


def leading(line):
    return len(line) - len(line.lstrip())


def render_table(header, aligns, rows):
    def cell(tag, text, idx):
        align = aligns[idx] if idx < len(aligns) else None
        attr = ' style="text-align:%s"' % align if align else ""
        return "<%s%s>%s</%s>" % (tag, attr, render_inline(text), tag)

    parts = ["<table>", "<thead>", "<tr>"]
    parts += [cell("th", c, j) for j, c in enumerate(header)]
    parts += ["</tr>", "</thead>", "<tbody>"]
    for row in rows:
        parts.append("<tr>")
        parts += [cell("td", c, j) for j, c in enumerate(row)]
        parts.append("</tr>")
    parts += ["</tbody>", "</table>"]
    return "\n".join(parts)


def render_list(block):
    """Render one list block, recursing on indented sub-lists."""
    items, kind = [], None
    for line in block:
        b, o = BULLET_RE.match(line), ORDERED_RE.match(line)
        if (b or o) and (not items or leading(line) <= items[0][0]):
            if kind is None:
                kind = "ol" if o else "ul"
            content = o.group(3) if o else b.group(2)
            items.append((leading(line), [content]))
        elif items:
            items[-1][1].append(line[items[-1][0]:] if leading(line) > items[-1][0] else line.strip())
        else:  # continuation with no opener; treat as its own item
            items.append((leading(line), [line.strip()]))

    parts = ["<%s>" % kind]
    for _, content in items:
        first, rest = content[0], [c for c in content[1:]]
        rendered = render_inline(first)
        tail = [c for c in rest if c.strip()]
        if tail:
            nested = render(dedent(rest))
            parts.append("<li>%s\n%s\n</li>" % (rendered, indent(nested)))
        else:
            parts.append("<li>%s</li>" % rendered)
    parts.append("</%s>" % kind)
    return "\n".join(parts)


def dedent(lines):
    widths = [leading(l) for l in lines if l.strip()]
    cut = min(widths) if widths else 0
    return [l[cut:] if l.strip() else l for l in lines]


def indent(text, pad="  "):
    return "\n".join(pad + l if l else l for l in text.split("\n"))


# --------------------------------------------------------------------------

def build_page(md_text):
    lines = strip_frontmatter(md_text.replace("\r\n", "\n").split("\n"))

    title = None
    for line in lines:
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == 1:
            title = re.sub(r"[*`_]", "", m.group(2)).strip()
            break

    body = render(lines)
    wikilinks = sorted(set(WIKILINK_RE.findall(md_text)))

    page = (
        "<!doctype html>\n"
        '<html lang="en">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        "<title>%s</title>\n"
        "<style>\n%s\n</style>\n"
        "</head>\n"
        "<body>\n%s\n\n%s\n\n</body>\n</html>\n"
    ) % (html.escape(title or "Draft", quote=False), CSS, body, FOOTER)
    return page, title, wikilinks


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="path to the draft Markdown file")
    ap.add_argument("-o", "--output", help="output path (default: drafts/html/<stem>.html next to the draft)")
    args = ap.parse_args()

    if not os.path.isfile(args.source):
        sys.exit("no such draft: %s" % args.source)

    with open(args.source, encoding="utf-8") as fh:
        page, title, wikilinks = build_page(fh.read())

    out = args.output
    if not out:
        stem = os.path.splitext(os.path.basename(args.source))[0]
        out = os.path.join(os.path.dirname(os.path.abspath(args.source)), "html", stem + ".html")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(page)

    print("wrote %s" % out)
    print("title: %s" % (title or "(none — no H1 in the draft)"))
    if wikilinks:
        print("wikilinks left verbatim (%d): %s" % (len(wikilinks), ", ".join(wikilinks)))


if __name__ == "__main__":
    main()
