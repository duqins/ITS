// Builds Phase1_Initial_Plan_and_Requirements.docx from the Markdown files in ./sections.
// Usage (from repo root):  npm install   (once)   then   node docs/phase1/build.js
//
// Supported Markdown: # ## ### headings, paragraphs, "- " bullets, "> " notes,
// | pipe | tables |, **bold**, *italic*. A "<!-- widths: a,b,c -->" comment above a
// table sets column widths (DXA, sum ≈ 9360). A file starting with "<!-- titlepage -->"
// is rendered as a centred title page.

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, LevelFormat, PageBreak, TableOfContents, PageNumber, Footer, Header,
} = require("docx");

const FONT = "Calibri";
const ACCENT = "C55A11";
const TOTAL_W = 9360;
const OUT_NAME = "Phase1_Initial_Plan_and_Requirements.docx";
const HEADER_TEXT = "COSC 336 – Phase 1: Initial Plan and Requirement Gathering Document";

// ---- inline markdown (**bold**, *italic*) -> TextRuns ----
function inline(text, base = {}) {
  const runs = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*)/g;
  let last = 0, m;
  while ((m = re.exec(text))) {
    if (m.index > last) runs.push(new TextRun({ text: text.slice(last, m.index), font: FONT, size: 22, ...base }));
    const tok = m[0];
    if (tok.startsWith("**")) runs.push(new TextRun({ text: tok.slice(2, -2), font: FONT, size: 22, bold: true, ...base }));
    else runs.push(new TextRun({ text: tok.slice(1, -1), font: FONT, size: 22, italics: true, ...base }));
    last = m.index + tok.length;
  }
  if (last < text.length) runs.push(new TextRun({ text: text.slice(last), font: FONT, size: 22, ...base }));
  return runs;
}

function heading(level, text) {
  const lv = [HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3][level - 1];
  return new Paragraph({ heading: lv, children: [new TextRun({ text, font: FONT })] });
}
const para = (text, extra = {}) => new Paragraph({ spacing: { after: 120, line: 276 }, children: inline(text, extra) });
const bullet = (text) => new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 60, line: 276 }, children: inline(text) });
const note = (text) => new Paragraph({ spacing: { after: 120, line: 276 }, children: inline(text, { italics: true, size: 20 }) });
const spacer = () => new Paragraph({ spacing: { after: 120 }, children: [] });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

function table(headers, rows, widths) {
  const ws = widths && widths.length === headers.length ? widths : headers.map(() => Math.floor(TOTAL_W / headers.length));
  const cell = (text, w, isHead) => new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: isHead ? { type: ShadingType.CLEAR, fill: ACCENT, color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ spacing: { after: 0 }, children: inline(text, { size: 20, bold: isHead || undefined, color: isHead ? "FFFFFF" : undefined }) })],
  });
  return new Table({
    width: { size: ws.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: ws,
    rows: [
      new TableRow({ tableHeader: true, children: headers.map((h, i) => cell(h, ws[i], true)) }),
      ...rows.map((r) => new TableRow({ children: r.map((c, i) => cell(c ?? "", ws[i], false)) })),
    ],
  });
}

const splitRow = (line) => line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());

// ---- markdown file -> array of docx elements ----
function parseMarkdown(md, { titlePage = false } = {}) {
  const lines = md.split(/\r?\n/);
  const out = [];
  let pendingWidths = null;
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    const t = line.trim();
    const wm = t.match(/^<!--\s*widths:\s*([\d,\s]+)\s*-->$/);
    if (wm) { pendingWidths = wm[1].split(",").map((n) => parseInt(n.trim(), 10)); i++; continue; }
    if (t.startsWith("<!--")) { // skip single- or multi-line HTML comments
      while (i < lines.length && !lines[i].includes("-->")) i++;
      i++; continue;
    }
    if (t === "") { i++; continue; }

    if (t.startsWith("|")) {
      const rows = [];
      while (i < lines.length && lines[i].trim().startsWith("|")) { rows.push(splitRow(lines[i])); i++; }
      const headers = rows[0];
      const body = rows.slice(1).filter((r) => !r.every((c) => /^:?-{2,}:?$/.test(c)));
      out.push(table(headers, body, pendingWidths));
      out.push(spacer());
      pendingWidths = null;
      continue;
    }

    const hm = t.match(/^(#{1,4})\s+(.*)$/);
    if (hm) {
      const level = hm[1].length, text = hm[2];
      if (titlePage) {
        const size = [32, 40, 30, 28][level - 1];
        const color = level === 2 ? ACCENT : undefined;
        const bold = level !== 3;
        const after = [200, 200, 600, 1200][level - 1];
        out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: level === 1 ? 1800 : 0, after }, children: [new TextRun({ text, font: FONT, size, bold, color })] }));
      } else {
        out.push(heading(Math.min(level, 3), text));
      }
      i++; continue;
    }

    if (t.startsWith("- ")) { out.push(bullet(t.slice(2))); i++; continue; }
    if (t.startsWith("> ")) { out.push(note(t.slice(2))); i++; continue; }

    // paragraph: join consecutive plain lines
    const buf = [t];
    i++;
    while (i < lines.length && lines[i].trim() !== "" && !/^(#|-|>|\||<!--)/.test(lines[i].trim())) { buf.push(lines[i].trim()); i++; }
    if (titlePage) buf.forEach((l) => out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 100 }, children: [new TextRun({ text: l, font: FONT, size: 26 })] })));
    else out.push(para(buf.join(" ")));
  }
  return out;
}

// ---- assemble ----
const dir = path.join(__dirname, "sections");
const files = fs.readdirSync(dir).filter((f) => f.endsWith(".md")).sort();
const children = [];
for (const f of files) {
  const md = fs.readFileSync(path.join(dir, f), "utf8");
  const isTitle = /^<!--\s*titlepage\s*-->/.test(md.trim());
  children.push(...parseMarkdown(md, { titlePage: isTitle }));
  if (isTitle) {
    children.push(pageBreak());
    children.push(new Paragraph({ spacing: { before: 360, after: 160 }, children: [new TextRun({ text: "Table of Contents", font: FONT, size: 32, bold: true, color: ACCENT })] }));
    children.push(new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-2" }));
    children.push(note("(In Word, right-click the table and choose “Update Field” to refresh page numbers.)"));
    children.push(pageBreak());
  }
}

const doc = new Document({
  creator: "COSC 336 Group 4",
  title: "Phase 1 – Initial Plan and Requirement Gathering Document",
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 32, bold: true, color: ACCENT, font: FONT }, paragraph: { spacing: { before: 360, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, color: "1F3864", font: FONT }, paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 23, bold: true, font: FONT }, paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 2 } },
    ],
  },
  numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] },
  sections: [{
    properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: HEADER_TEXT, font: FONT, size: 16, color: "666666" })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Page ", font: FONT, size: 16 }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16 })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const out = path.join(__dirname, OUT_NAME);
  fs.writeFileSync(out, buf);
  console.log(`wrote ${out} (${buf.length} bytes) from ${files.length} section files`);
});
