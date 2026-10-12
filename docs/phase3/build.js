// Builds the Phase 3 SRS (.docx) from the Markdown files in ./sections.
// Usage from the repository root:  npm install  (once), then  npm run build:phase3
//
// Supported Markdown: # ## ### #### headings, paragraphs, "- " bullets, numbered steps
// such as "1." or "2a.", "> " notes, | pipe | tables |, **bold**, *italic* and images
// written as ![Figure caption](images/file.png) (PNG or JPG, relative to docs/phase3).
// "<!-- widths: a,b,c -->" above a table sets column widths (DXA, total about 9360).
// "<!-- pagebreak -->" starts a new page. Other HTML comments, including multi-line
// guidance comments, are not printed. Lines starting with "TODO" are not printed but
// are listed as a warning, so unfinished sections are easy to find.

const fs = require("fs");
const path = require("path");
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType, Table, TableRow, TableCell,
  WidthType, ShadingType, LevelFormat, PageBreak, TableOfContents, PageNumber, Footer, Header, ImageRun,
} = require("docx");

const FONT = "Calibri";
const ACCENT = "1F6F5C";
const TOTAL_W = 9360;
const MAX_IMG_W = 620; // pixels at 96 dpi, about 6.45 inches
const ROOT = __dirname;
const OUT_NAME = "Dawra_Campus_Phase3_SRS.docx";
const HEADER_TEXT = "Software Requirements Specification for Dawra Campus – COSC 336 Group 4";

const todos = [];

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

const HEADINGS = [HeadingLevel.HEADING_1, HeadingLevel.HEADING_2, HeadingLevel.HEADING_3, HeadingLevel.HEADING_4];
const heading = (level, text) => new Paragraph({ heading: HEADINGS[level - 1], keepNext: true, children: [new TextRun({ text, font: FONT })] });
const para = (text, extra = {}) => new Paragraph({ spacing: { after: 120, line: 276 }, children: inline(text, extra) });
const bullet = (text) => new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 60, line: 276 }, children: inline(text) });
const step = (num, text) => new Paragraph({ indent: { left: 720, hanging: 432 }, spacing: { after: 60, line: 276 }, children: [new TextRun({ text: `${num}\t`, font: FONT, size: 22 }), ...inline(text)] });
const note = (text) => new Paragraph({ spacing: { after: 120, line: 276 }, children: inline(text, { italics: true, size: 20 }) });
const spacer = () => new Paragraph({ spacing: { after: 120 }, children: [] });
const pageBreak = () => new Paragraph({ children: [new PageBreak()] });

function table(headers, rows, widths) {
  const ws = widths && widths.length === headers.length ? widths : headers.map(() => Math.floor(TOTAL_W / headers.length));
  const cell = (text, w, isHead) => new TableCell({
    width: { size: w, type: WidthType.DXA },
    shading: isHead ? { type: ShadingType.CLEAR, fill: ACCENT, color: "auto" } : undefined,
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({ spacing: { after: 0 }, children: inline(text, { size: 19, bold: isHead || undefined, color: isHead ? "FFFFFF" : undefined }) })],
  });
  return new Table({
    width: { size: ws.reduce((a, b) => a + b, 0), type: WidthType.DXA },
    columnWidths: ws,
    rows: [
      new TableRow({ tableHeader: true, cantSplit: true, children: headers.map((h, i) => cell(h, ws[i], true)) }),
      ...rows.map((r) => new TableRow({ cantSplit: true, children: headers.map((_, i) => cell(r[i] ?? "", ws[i], false)) })),
    ],
  });
}

function imageSize(buf, ext) {
  if (ext === "png") return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
  let i = 2; // JPEG: walk the markers until a start-of-frame marker
  while (i < buf.length) {
    if (buf[i] !== 0xff) { i++; continue; }
    const marker = buf[i + 1];
    const len = buf.readUInt16BE(i + 2);
    if (marker >= 0xc0 && marker <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(marker)) return { w: buf.readUInt16BE(i + 7), h: buf.readUInt16BE(i + 5) };
    i += 2 + len;
  }
  throw new Error("cannot read JPEG size");
}

function image(caption, rel, file) {
  const full = path.join(ROOT, rel);
  if (!fs.existsSync(full)) {
    todos.push(`${file}: image not found: ${rel}`);
    return [para(`[Missing image: ${rel}]`, { color: "C00000" })];
  }
  const ext = path.extname(full).slice(1).toLowerCase().replace("jpeg", "jpg");
  const buf = fs.readFileSync(full);
  const { w, h } = imageSize(buf, ext);
  const scale = Math.min(1, MAX_IMG_W / w);
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, children: [new ImageRun({ type: ext, data: buf, transformation: { width: Math.round(w * scale), height: Math.round(h * scale) } })] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 200 }, children: inline(caption, { italics: true, size: 19 }) }),
  ];
}

const splitRow = (line) => line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((c) => c.trim());

function parseMarkdown(md, file, { titlePage = false } = {}) {
  const lines = md.split(/\r?\n/);
  const out = [];
  let widths = null;
  let i = 0;
  while (i < lines.length) {
    const t = lines[i].trim();
    const wm = t.match(/^<!--\s*widths:\s*([\d,\s]+)\s*-->$/);
    if (wm) { widths = wm[1].split(",").map((n) => parseInt(n.trim(), 10)); i++; continue; }
    if (/^<!--\s*pagebreak\s*-->$/.test(t)) { out.push(pageBreak()); i++; continue; }
    if (t.startsWith("<!--")) { while (i < lines.length && !lines[i].includes("-->")) i++; i++; continue; }
    if (t === "") { i++; continue; }
    if (/^TODO\b/.test(t)) { todos.push(`${file}: ${t.slice(0, 90)}`); i++; continue; }

    if (t.startsWith("|")) {
      const rows = [];
      while (i < lines.length && lines[i].trim().startsWith("|")) { rows.push(splitRow(lines[i])); i++; }
      const body = rows.slice(1).filter((r) => !r.every((c) => /^:?-{2,}:?$/.test(c)));
      out.push(table(rows[0], body, widths));
      out.push(spacer());
      widths = null;
      continue;
    }

    const im = t.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
    if (im) { out.push(...image(im[1], im[2], file)); i++; continue; }

    const hm = t.match(/^(#{1,4})\s+(.*)$/);
    if (hm) {
      const level = hm[1].length, text = hm[2];
      if (titlePage) {
        const size = [40, 30, 26, 24][level - 1];
        out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: level === 1 ? 1600 : 0, after: [240, 200, 600, 200][level - 1] }, children: [new TextRun({ text, font: FONT, size, bold: level !== 3, color: level <= 2 ? ACCENT : undefined })] }));
      } else out.push(heading(level, text));
      i++; continue;
    }

    if (t.startsWith("- ")) { out.push(bullet(t.slice(2))); i++; continue; }
    const sm = t.match(/^(\d+[a-z]?\.)\s+(.*)$/);
    if (sm) { out.push(step(sm[1], sm[2])); i++; continue; }
    if (t.startsWith("> ")) { out.push(note(t.slice(2))); i++; continue; }

    const buf = [t];
    i++;
    while (i < lines.length && lines[i].trim() !== "" && !/^(#|- |>|\||<!--|!\[|TODO\b|\d+[a-z]?\.\s)/.test(lines[i].trim())) { buf.push(lines[i].trim()); i++; }
    if (titlePage) buf.forEach((l) => out.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 80 }, children: inline(l, { size: 24 }) })));
    else out.push(para(buf.join(" ")));
  }
  return out;
}

const dir = path.join(ROOT, "sections");
const files = fs.readdirSync(dir).filter((f) => f.endsWith(".md")).sort();
const children = [];
for (const f of files) {
  const md = fs.readFileSync(path.join(dir, f), "utf8");
  const isTitle = /^<!--\s*titlepage\s*-->/.test(md.trim());
  children.push(...parseMarkdown(md, f, { titlePage: isTitle }));
  if (isTitle) {
    children.push(pageBreak());
    children.push(new Paragraph({ spacing: { before: 240, after: 160 }, children: [new TextRun({ text: "Table of Contents", font: FONT, size: 32, bold: true, color: ACCENT })] }));
    children.push(new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-2" }));
    children.push(note("In Word, right-click the table of contents and choose Update Field to refresh page numbers."));
    children.push(pageBreak());
  }
}

const doc = new Document({
  creator: "COSC 336 Group 4",
  title: "Software Requirements Specification for Dawra Campus",
  styles: {
    default: { document: { run: { font: FONT, size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 32, bold: true, color: ACCENT, font: FONT }, paragraph: { spacing: { before: 360, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 26, bold: true, color: "1F3864", font: FONT }, paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 23, bold: true, font: FONT }, paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 2 } },
      { id: "Heading4", name: "Heading 4", basedOn: "Normal", next: "Normal", quickFormat: true, run: { size: 22, bold: true, italics: true, font: FONT }, paragraph: { spacing: { before: 160, after: 60 }, outlineLevel: 3 } },
    ],
  },
  numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] },
  sections: [{
    properties: { page: { margin: { top: 1300, bottom: 1300, left: 1440, right: 1440 } } },
    headers: { default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: HEADER_TEXT, font: FONT, size: 16, color: "666666" })] })] }) },
    footers: { default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [new TextRun({ text: "Page ", font: FONT, size: 16 }), new TextRun({ children: [PageNumber.CURRENT], font: FONT, size: 16 })] })] }) },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  const out = path.join(ROOT, OUT_NAME);
  fs.writeFileSync(out, buf);
  console.log(`wrote ${path.relative(process.cwd(), out)} from ${files.length} section files`);
  if (todos.length) {
    console.log(`\n${todos.length} unfinished item(s) – these are not printed in the document:`);
    todos.forEach((t) => console.log("  - " + t));
  } else console.log("No TODO items left.");
});
