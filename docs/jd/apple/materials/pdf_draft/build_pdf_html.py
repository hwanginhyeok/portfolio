#!/usr/bin/env python3
"""
Convert resume_en.md + cover_letter.md → print-ready HTML.
Open the .html in a browser and use Ctrl+P → "Save as PDF" (Letter, no headers/footers).
No external dependencies — uses only stdlib regex.
"""
from pathlib import Path
import re
import html as html_mod

BASE = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent

CSS = """
@page { size: Letter; margin: 0.5in 0.6in; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body {
  font-family: "Helvetica Neue", "Arial", "Noto Sans KR", sans-serif;
  font-size: 9.6pt;
  line-height: 1.3;
  color: #111;
  max-width: 7.6in;
  margin: 0 auto;
  padding: 0;
}
h1 {
  font-size: 17pt;
  margin: 0 0 3pt 0;
  letter-spacing: 0.5px;
  border-bottom: 1.5pt solid #111;
  padding-bottom: 4pt;
}
h2 {
  font-size: 11pt;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  margin: 9pt 0 3pt 0;
  border-bottom: 0.5pt solid #888;
  padding-bottom: 1pt;
  color: #111;
}
h3 {
  font-size: 10.2pt;
  margin: 6pt 0 1pt 0;
  color: #222;
}
h4 {
  font-size: 9.6pt;
  margin: 4pt 0 1pt 0;
  font-weight: 700;
}
p { margin: 3pt 0; }
ul { margin: 2pt 0 3pt 0; padding-left: 15pt; }
li { margin: 0.5pt 0; }
strong { color: #000; }
em { color: #444; }
table { width: 100%; border-collapse: collapse; margin: 3pt 0 5pt 0; font-size: 9pt; }
th, td { border: 0.4pt solid #bbb; padding: 2pt 4pt; text-align: left; vertical-align: top; }
th { background: #f3f3f3; }
hr { border: 0; border-top: 0.5pt solid #ccc; margin: 4pt 0; }
.contact { font-size: 10pt; color: #333; margin-bottom: 6pt; }
.subtitle { font-size: 11pt; color: #444; margin: 0 0 4pt 0; font-weight: 600; }
blockquote { display: none; }
/* Tighten first item after heading */
h2 + p, h3 + p { margin-top: 2pt; }
"""


def md_to_html(md: str) -> str:
    """Minimal Markdown -> HTML covering what these resume files use."""
    # Strip front-matter blockquotes (>) lines at top
    lines = md.splitlines()
    out: list[str] = []
    in_table = False
    table_rows: list[list[str]] = []
    in_list = False

    def flush_table():
        nonlocal table_rows
        if not table_rows:
            return ""
        header = table_rows[0]
        body = table_rows[2:] if len(table_rows) > 2 else []
        s = "<table>\n<thead><tr>"
        for c in header:
            s += f"<th>{inline(c)}</th>"
        s += "</tr></thead>\n<tbody>\n"
        for row in body:
            s += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>\n"
        s += "</tbody></table>"
        table_rows = []
        return s

    def inline(s: str) -> str:
        # Order matters: escape first only the ampersands not in entities (skip for simplicity), then bold/italic/code/links
        # Bold
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        # Italic
        s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
        # Inline code
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        # Links [text](url)
        s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
        return s

    for raw in lines:
        line = raw.rstrip()

        # Skip frontmatter quotes
        if line.startswith(">"):
            continue

        # Table detection
        if re.match(r"^\s*\|.*\|\s*$", line):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            table_rows.append(cells)
            in_table = True
            continue
        elif in_table:
            out.append(flush_table())
            in_table = False

        if not line.strip():
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append("")
            continue

        # Horizontal rule
        if re.match(r"^-{3,}$", line.strip()):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append("<hr/>")
            continue

        # Headings
        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            if in_list:
                out.append("</ul>")
                in_list = False
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
            continue

        # List item
        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(m.group(1))}</li>")
            continue

        # Paragraph (or continuation)
        if in_list:
            out.append("</ul>")
            in_list = False
        out.append(f"<p>{inline(line)}</p>")

    if in_table:
        out.append(flush_table())
    if in_list:
        out.append("</ul>")

    return "\n".join(out)


def wrap(title: str, body_html: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html_mod.escape(title)}</title>
<style>{CSS}</style>
</head>
<body>
{body_html}
</body>
</html>
"""


def build(src_name: str, out_name: str, title: str):
    src = (BASE / src_name).read_text(encoding="utf-8")
    body = md_to_html(src)
    html = wrap(title, body)
    (OUT / out_name).write_text(html, encoding="utf-8")
    print(f"wrote {out_name}  ({len(html)} bytes)")


if __name__ == "__main__":
    build("resume_en.md", "resume_en.html", "Inhyeok Hwang — Resume (Apple Reliability Engineer)")
    build("cover_letter.md", "cover_letter.html", "Inhyeok Hwang — Cover Letter (Apple Reliability Engineer)")
    print("\nNext: open each .html in a browser and Ctrl+P → Save as PDF (Letter, no headers/footers).")
