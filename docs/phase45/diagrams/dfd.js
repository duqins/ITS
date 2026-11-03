// Draws the context diagram and the data-flow diagrams for sections 1 and 2 as SVG files.
// Usage from the repository root: node docs/phase45/diagrams/dfd.js docs/phase45/images
const fs = require("fs");
const path = require("path");
const outDir = process.argv[2];

const FONT = "Segoe UI, Arial, sans-serif";
const BLUE = "#0b4fb3", DARK = "#0b3d91", FILL = "#c9dcf5", TEAL = "#1592a8";

const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// split text into lines that fit a width (rough width per character)
function wrap(text, width, size, bold) {
  const max = Math.max(4, Math.floor(width / (size * (bold ? 0.6 : 0.53))));
  const lines = [];
  let cur = "";
  for (const w of String(text).split(" ")) {
    if ((cur + " " + w).trim().length > max && cur) { lines.push(cur); cur = w; }
    else cur = (cur + " " + w).trim();
  }
  if (cur) lines.push(cur);
  return lines;
}

function textBlock(lines, cx, cy, size, opts = {}) {
  const lh = size * 1.18;
  const top = cy - ((lines.length - 1) * lh) / 2 + size * 0.35;
  return lines.map((l, i) => `<text x="${cx}" y="${top + i * lh}" text-anchor="middle" font-family="${FONT}" font-size="${size}"${opts.bold ? ' font-weight="700"' : ""} fill="${opts.color || "#111"}">${esc(l)}</text>`).join("");
}

function external(name, x, y, w, h, opts = {}) {
  const size = opts.size || 17;
  let s = `<rect x="${x + 6}" y="${y + 6}" width="${w}" height="${h}" fill="${DARK}"/>`;
  s += `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${FILL}" stroke="${DARK}" stroke-width="2"/>`;
  if (opts.dup) s += `<line x1="${x}" y1="${y + 14}" x2="${x + 14}" y2="${y}" stroke="${DARK}" stroke-width="2"/>`;
  const main = wrap(name, w - 18, size, true);
  const sub = opts.sub ? wrap(opts.sub, w - 14, 14) : [];
  const lhM = size * 1.15, lhS = 14 * 1.2;
  const total = main.length * lhM + sub.length * lhS;
  let yy = y + h / 2 - total / 2 + size * 0.85;
  main.forEach((l) => { s += `<text x="${x + w / 2}" y="${yy}" text-anchor="middle" font-family="${FONT}" font-size="${size}" font-weight="700" fill="#111">${esc(l)}</text>`; yy += lhM; });
  sub.forEach((l) => { s += `<text x="${x + w / 2}" y="${yy - 2}" text-anchor="middle" font-family="${FONT}" font-size="14" fill="#333">${esc(l)}</text>`; yy += lhS; });
  return s;
}

function processBox(num, name, x, y, w, h) {
  let s = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="#fff" stroke="${DARK}" stroke-width="2"/>`;
  s += `<path d="M${x} ${y + 26} V${y + 10} Q${x} ${y} ${x + 10} ${y} H${x + w - 10} Q${x + w} ${y} ${x + w} ${y + 10} V${y + 26} Z" fill="${BLUE}" stroke="${DARK}" stroke-width="2"/>`;
  s += `<text x="${x + w / 2}" y="${y + 19}" text-anchor="middle" font-family="${FONT}" font-size="15" font-weight="700" fill="#fff">${esc(num)}</text>`;
  s += textBlock(wrap(name, w - 18, 17, true), x + w / 2, y + 26 + (h - 26) / 2, 17, { bold: true });
  return s;
}

function store(id, name, x, y, w, h, opts = {}) {
  const fs2 = opts.size || 14.5;
  let s = `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#fff" stroke="none"/>`;
  s += `<path d="M${x + w} ${y} H${x} V${y + h} H${x + w}" fill="none" stroke="${DARK}" stroke-width="2"/>`;
  s += `<line x1="${x + 44}" y1="${y}" x2="${x + 44}" y2="${y + h}" stroke="${DARK}" stroke-width="2"/>`;
  if (opts.dup) s += `<line x1="${x + 8}" y1="${y}" x2="${x + 8}" y2="${y + h}" stroke="${DARK}" stroke-width="2"/>`;
  s += `<text x="${x + (opts.dup ? 26 : 22)}" y="${y + h / 2 + 5}" text-anchor="middle" font-family="${FONT}" font-size="15" font-weight="700" fill="#111">${esc(id)}</text>`;
  const lines = wrap(name, w - 56, fs2, true);
  const lh = fs2 * 1.15;
  let yy = y + h / 2 - ((lines.length - 1) * lh) / 2 + 5;
  lines.forEach((l) => { s += `<text x="${x + 52}" y="${yy}" font-family="${FONT}" font-size="${fs2}" font-weight="700" fill="#111">${esc(l)}</text>`; yy += lh; });
  return s;
}

function arrowHead(p1, p2, color) {
  const a = Math.atan2(p2.y - p1.y, p2.x - p1.x), L = 12, W = 6;
  const bx = p2.x - L * Math.cos(a), by = p2.y - L * Math.sin(a);
  return `<path d="M${p2.x} ${p2.y} L${bx + W * Math.sin(a)} ${by - W * Math.cos(a)} L${bx - W * Math.sin(a)} ${by + W * Math.cos(a)} Z" fill="${color}"/>`;
}

function pillSize(label, maxW, size) {
  const lines = wrap(label, maxW - 12, size);
  const w = Math.min(maxW, Math.max(...lines.map((l) => l.length)) * size * 0.53 + 14);
  return { lines, w, h: lines.length * size * 1.18 + 8 };
}
function pill(label, cx, cy, maxW, size) {
  const { lines, w, h } = pillSize(label, maxW, size);
  let s = `<rect x="${cx - w / 2}" y="${cy - h / 2}" width="${w}" height="${h}" rx="5" fill="#fff" stroke="#aab6cc" stroke-width="1"/>`;
  return s + textBlock(lines, cx, cy, size, { color: "#13213d" });
}

// A label on the last segment of a flow is moved back from the tip so the arrowhead always shows.
const CLEAR = 24;
function clearOfArrow(points, at, maxW, size, label) {
  const a = points[points.length - 2], b = points[points.length - 1];
  const horiz = a.y === b.y;
  const along = horiz ? at.x : at.y, start = horiz ? a.x : a.y, tip = horiz ? b.x : b.y;
  const across = horiz ? at.y - a.y : at.x - a.x;
  if (Math.abs(across) > 1 || (along - start) * (along - tip) > 0) return { at, maxW };
  const dir = Math.sign(tip - start), room = Math.abs(tip - start) - CLEAR - 4;
  if (horiz) maxW = Math.min(maxW, room);
  const half = (horiz ? pillSize(label, maxW, size).w : pillSize(label, maxW, size).h) / 2;
  const limit = tip - dir * (CLEAR + half);
  const moved = dir * (along - limit) > 0 ? limit : along;
  return { at: horiz ? { x: moved, y: at.y } : { x: at.x, y: moved }, maxW };
}

// A diagram collects lines, boxes and labels separately so labels are always drawn on top.
class Diagram {
  constructor() { this.under = ""; this.lines = ""; this.boxes = ""; this.labels = ""; }
  // points: polyline; label placed at opts.at, or at fraction opts.t along the first segment
  flow(points, label, opts = {}) {
    const color = opts.ai ? TEAL : BLUE;
    this.lines += `<polyline points="${points.map((p) => `${p.x},${p.y}`).join(" ")}" fill="none" stroke="${color}" stroke-width="2"/>`;
    const n = points.length;
    this.lines += arrowHead(points[n - 2], points[n - 1], color);
    if (label) {
      let at = opts.at;
      if (!at) {
        const t = opts.t === undefined ? 0.5 : opts.t;
        at = { x: points[0].x + (points[1].x - points[0].x) * t, y: points[0].y + (points[1].y - points[0].y) * t };
      }
      const size = opts.size || 15;
      const fit = clearOfArrow(points, at, opts.labelW || 160, size, label);
      this.labels += pill(label, fit.at.x, fit.at.y, fit.maxW, size);
    }
  }
  add(svg) { this.boxes += svg; }
  write(file, w, h) {
    const s = `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">\n<rect width="100%" height="100%" fill="#fff"/>\n${this.under}${this.lines}${this.boxes}${this.labels}\n</svg>\n`;
    fs.writeFileSync(path.join(outDir, file), s);
    console.log("wrote " + file);
  }
}

const AI = "AI Provider";
const D = {
  D1: "Users and Settings", D2: "Assets and Listings", D3: "Requests and Holds", D4: "AI Records",
  D5: "Approvals and Transfers", D6: "Maintenance Records", D7: "Sustainability Impacts", D8: "Audit Log",
};

// ---------- Figure 1.1: context diagram ----------
// External entities sit left and right of process 0 with straight flows; the AI Provider sits below.
{
  const g = new Diagram();
  const P = { x: 385, y: 30, w: 165, h: 480 };
  const L = { x: 15, w: 165 }, Rt = { x: 755, w: 165 };
  const slot = 72, gapY = 22;
  const left = [
    { name: "Requester", flows: [["in", "resource request, match choice, assistant question"], ["out", "ranked matches, request status, assistant answer"]] },
    { name: "Asset Custodian", sub: "or department representative", flows: [["in", "asset details, handover records, defect and end-of-life reports"], ["out", "suggested category, transfer tasks, asset history"]] },
    { name: "Maintenance Staff", flows: [["in", "inspection and repair records"], ["out", "work orders"]] },
  ];
  const right = [
    { name: "Approvers", sub: "department representative, finance officer, procurement officer", flows: [["in", "approval decisions"], ["out", "approval tasks, finance and reuse reports"]] },
    { name: "Sustainability Officer", flows: [["in", "end-of-life reviews"], ["out", "review tasks, impact report"]] },
    { name: "Administrators", sub: "business administrator, system administrator", flows: [["in", "account details, role assignments, settings, report requests"], ["out", "account status, operational and audit reports"]] },
  ];
  const side = (list, box, isLeft) => {
    const total = list.length * 2 * slot + (list.length - 1) * gapY;
    let y = P.y + (P.h - total) / 2;
    for (const e of list) {
      g.add(external(e.name, box.x, y + 4, box.w, 2 * slot - 8, { sub: e.sub }));
      e.flows.forEach(([dir, label], i) => {
        const yy = y + slot * i + slot / 2;
        const ext = { x: isLeft ? box.x + box.w : box.x, y: yy }, pr = { x: isLeft ? P.x : P.x + P.w, y: yy };
        g.flow(dir === "in" ? [ext, pr] : [pr, ext], label, { at: { x: (ext.x + pr.x) / 2, y: yy }, labelW: 185 });
      });
      y += 2 * slot + gapY;
    }
  };
  side(left, L, true);
  side(right, Rt, false);
  g.flow([{ x: 440, y: 510 }, { x: 440, y: 640 }], "approved text fields", { ai: true, at: { x: 440, y: 555 }, labelW: 110 });
  g.flow([{ x: 495, y: 640 }, { x: 495, y: 510 }], "AI output", { ai: true, at: { x: 495, y: 605 }, labelW: 100 });
  g.add(external(AI, 378, 640, 180, 58));
  g.add(processBox("0", "Dawra Campus System", P.x, P.y, P.w, P.h));
  g.write("dfd-context.svg", 935, 715);
}

// ---------- Level 1 rows ----------
// Each row: external entities on the left, the process in the middle, data stores on the right.
// Every arrow is a straight horizontal line, so rows never cross each other.
const ROW = { extX: 15, extW: 160, procX: 360, procW: 180, storeX: 730, storeW: 190, slot: 46 };

function drawRow(g, row, y0, seen) {
  const gap = 12;
  const leftSlots = row.left.reduce((n, e) => n + e.flows.length, 0);
  const rightSlots = row.right.reduce((n, s) => n + s.flows.length, 0);
  const leftH = leftSlots * ROW.slot + (row.left.length - 1) * gap;
  const rightH = rightSlots * ROW.slot + (row.right.length - 1) * gap;
  const procH = Math.max(110, leftH, rightH);
  let y = y0 + (procH - leftH) / 2;
  for (const e of row.left) {
    const h = e.flows.length * ROW.slot;
    const key = "E:" + e.name;
    g.add(external(e.name, ROW.extX, y + 3, ROW.extW, h - 6, { dup: seen.has(key), size: 16 }));
    seen.add(key);
    e.flows.forEach((f, i) => {
      const yy = y + ROW.slot * i + ROW.slot / 2;
      const ai = e.name === AI;
      const a = { x: ROW.extX + ROW.extW, y: yy }, b = { x: ROW.procX, y: yy };
      g.flow(f.dir === "in" ? [a, b] : [b, a], f.label, { ai, at: { x: (a.x + b.x) / 2, y: yy }, labelW: 162 });
    });
    y += h + gap;
  }
  y = y0 + (procH - rightH) / 2;
  for (const s of row.right) {
    const h = s.flows.length * ROW.slot;
    const key = "S:" + s.id;
    g.add(store(s.id, D[s.id], ROW.storeX, y + 3, ROW.storeW, h - 6, { dup: seen.has(key) }));
    seen.add(key);
    s.flows.forEach((f, i) => {
      const yy = y + ROW.slot * i + ROW.slot / 2;
      const a = { x: ROW.procX + ROW.procW, y: yy }, b = { x: ROW.storeX, y: yy };
      g.flow(f.dir === "write" ? [a, b] : [b, a], f.label, { at: { x: (a.x + b.x) / 2, y: yy }, labelW: 165 });
    });
    y += h + gap;
  }
  g.add(processBox(row.num, row.name, ROW.procX, y0, ROW.procW, procH));
  return procH;
}

function level1(file, rows) {
  const g = new Diagram();
  const seen = new Set();
  let y = 15;
  for (const r of rows) y += drawRow(g, r, y, seen) + 36;
  g.write(file, 930, y - 20);
}

const st = (id, flows) => ({ id, flows });
const R = (label) => ({ dir: "read", label }), Wr = (label) => ({ dir: "write", label });
const In = (label) => ({ dir: "in", label }), Out = (label) => ({ dir: "out", label });

level1("dfd-level1-a.svg", [
  { num: "1.0", name: "Manage Accounts and Settings",
    left: [{ name: "Administrators", flows: [In("account details, role assignments, settings"), Out("account status")] }],
    right: [st("D1", [Wr("user, role and setting records")]), st("D8", [Wr("audit entries")])] },
  { num: "2.0", name: "Register and Publish Assets",
    left: [{ name: "Asset Custodian", flows: [In("asset details"), Out("suggested category")] }, { name: AI, flows: [Out("asset text"), In("category and tags")] }],
    right: [st("D1", [R("categories")]), st("D5", [R("release decisions")]), st("D2", [Wr("asset and listing records")]), st("D4", [Wr("AI suggestions")])] },
  { num: "3.0", name: "Request, Match and Reserve Assets",
    left: [{ name: "Requester", flows: [In("resource request, match choice"), Out("ranked matches, request status")] }, { name: AI, flows: [Out("request text"), In("embedding vectors")] }],
    right: [st("D2", [R("published listings")]), st("D5", [R("request decisions")]), st("D3", [Wr("request and hold records")]), st("D4", [Wr("match records")])] },
  { num: "4.0", name: "Answer Assistant Questions",
    left: [{ name: "Requester", flows: [In("assistant question"), Out("assistant answer")] }, { name: AI, flows: [Out("question context"), In("draft answer")] }],
    right: [st("D2", [R("permitted listings")]), st("D4", [Wr("assistant records")])] },
]);

level1("dfd-level1-b.svg", [
  { num: "5.0", name: "Approve and Transfer Assets",
    left: [{ name: "Approvers", flows: [In("approval decisions"), Out("approval tasks")] }, { name: "Sustainability Officer", flows: [In("end-of-life reviews"), Out("review tasks")] },
           { name: "Asset Custodian", flows: [In("handover records"), Out("transfer tasks")] }],
    right: [st("D1", [R("roles and emission factors")]), st("D3", [R("holds and requests"), Wr("hold and request states")]), st("D6", [R("end-of-life and repair cases")]),
            st("D5", [Wr("approval and transfer records")]), st("D2", [R("listings to approve"), Wr("new owner and location")]), st("D7", [Wr("transfer impacts")]), st("D8", [Wr("audit entries")])] },
  { num: "6.0", name: "Maintain and Retire Assets",
    left: [{ name: "Asset Custodian", flows: [In("defect and end-of-life reports")] }, { name: "Maintenance Staff", flows: [In("inspection and repair records"), Out("work orders")] },
           { name: AI, flows: [Out("asset condition text"), In("action advice")] }],
    right: [st("D1", [R("emission factors")]), st("D2", [R("asset details"), Wr("condition and state")]), st("D5", [R("approval decisions")]),
            st("D6", [Wr("maintenance records")]), st("D4", [Wr("AI suggestions")]), st("D7", [Wr("impact records")])] },
  { num: "7.0", name: "Report Impact and History",
    left: [{ name: "Administrators", flows: [In("report requests"), Out("operational and audit reports")] }, { name: "Approvers", flows: [Out("finance and reuse reports")] },
           { name: "Sustainability Officer", flows: [Out("impact report")] }, { name: "Asset Custodian", flows: [Out("asset history")] },
           { name: AI, flows: [Out("report figures"), In("draft report text")] }],
    right: [st("D2", [R("asset and listing records")]), st("D3", [R("request and hold records")]), st("D4", [R("AI records"), Wr("AI suggestions")]), st("D5", [R("transfer records")]), st("D6", [R("maintenance records")]), st("D7", [R("impact records")]), st("D8", [R("audit entries")])] },
]);

// ---------- Figure 2.3: Level 2 of 3.0 ----------
{
  const g = new Diagram();
  g.under += `<rect x="215" y="112" width="485" height="660" rx="14" fill="#f4f8fe" stroke="${BLUE}" stroke-width="2" stroke-dasharray="7 5"/>`;
  g.under += `<text x="232" y="138" font-family="${FONT}" font-size="15" font-weight="700" fill="${DARK}">Level 2 of process 3.0</text>`;
  const p1 = { x: 285, y: 160, w: 175, h: 96 }, p2 = { x: 285, y: 375, w: 175, h: 112 };
  const p3 = { x: 505, y: 375, w: 175, h: 112 }, p4 = { x: 505, y: 620, w: 175, h: 100 };
  // 3.1 Record Request
  g.flow([{ x: 175, y: 185 }, { x: 285, y: 185 }], "resource request", { at: { x: 230, y: 185 }, labelW: 90 });
  g.flow([{ x: 285, y: 232 }, { x: 175, y: 232 }], "request status", { at: { x: 230, y: 232 }, labelW: 90 });
  g.flow([{ x: 305, y: 256 }, { x: 305, y: 318 }, { x: 175, y: 318 }], "request record", { at: { x: 240, y: 318 }, labelW: 120 });
  g.flow([{ x: 380, y: 256 }, { x: 380, y: 375 }], "request details", { at: { x: 380, y: 318 }, labelW: 120 });
  // 3.2 Check Eligibility
  g.flow([{ x: 175, y: 405 }, { x: 285, y: 405 }], "published listings", { at: { x: 230, y: 405 }, labelW: 90 });
  g.flow([{ x: 175, y: 462 }, { x: 285, y: 462 }], "request decisions", { at: { x: 230, y: 462 }, labelW: 90 });
  g.flow([{ x: 400, y: 487 }, { x: 400, y: 545 }, { x: 540, y: 545 }, { x: 540, y: 487 }], "eligible listings, request criteria", { at: { x: 470, y: 545 }, labelW: 150 });
  // 3.3 Rank and Explain Matches
  g.flow([{ x: 555, y: 375 }, { x: 555, y: 72 }], "request text", { ai: true, at: { x: 555, y: 230 }, labelW: 95 });
  g.flow([{ x: 635, y: 72 }, { x: 635, y: 375 }], "embedding vectors", { ai: true, at: { x: 635, y: 300 }, labelW: 100 });
  g.flow([{ x: 680, y: 405 }, { x: 735, y: 405 }], "match recommendations", { at: { x: 725, y: 356 }, labelW: 145, size: 14 });
  g.flow([{ x: 680, y: 462 }, { x: 800, y: 462 }, { x: 800, y: 515 }], "ranked matches", { at: { x: 740, y: 462 }, labelW: 90 });
  g.flow([{ x: 620, y: 487 }, { x: 620, y: 620 }], "ranked list", { at: { x: 620, y: 575 }, labelW: 90 });
  // 3.4 Record Choice and Hold
  g.flow([{ x: 800, y: 605 }, { x: 800, y: 650 }, { x: 680, y: 650 }], "match choice", { at: { x: 740, y: 650 }, labelW: 100 });
  g.flow([{ x: 680, y: 700 }, { x: 790, y: 700 }, { x: 790, y: 762 }], "hold record", { at: { x: 790, y: 730 }, labelW: 90 });
  g.flow([{ x: 505, y: 690 }, { x: 175, y: 690 }], "request status", { at: { x: 340, y: 690 }, labelW: 120 });
  g.flow([{ x: 590, y: 720 }, { x: 590, y: 800 }], "match response", { at: { x: 590, y: 752 }, labelW: 150 });
  // boxes
  g.add(external("Requester", 15, 165, 160, 88));
  g.add(store("D3", D.D3, 15, 293, 160, 50, { size: 13.5 }));
  g.add(store("D2", D.D2, 15, 380, 160, 50, { size: 13.5 }));
  g.add(store("D5", D.D5, 15, 437, 160, 50, { size: 13.5 }));
  g.add(external("Requester", 15, 660, 160, 60, { dup: true }));
  g.add(external(AI, 520, 14, 160, 58));
  g.add(store("D4", D.D4, 735, 383, 185, 44));
  g.add(external("Requester", 735, 515, 180, 90, { dup: true }));
  g.add(store("D3", D.D3, 715, 762, 205, 44, { dup: true }));
  g.add(store("D4", D.D4, 470, 800, 205, 44, { dup: true }));
  g.add(processBox("3.1", "Record Request", p1.x, p1.y, p1.w, p1.h));
  g.add(processBox("3.2", "Check Eligibility", p2.x, p2.y, p2.w, p2.h));
  g.add(processBox("3.3", "Rank and Explain Matches", p3.x, p3.y, p3.w, p3.h));
  g.add(processBox("3.4", "Record Choice and Hold", p4.x, p4.y, p4.w, p4.h));
  g.write("dfd-level2-3.svg", 930, 860);
}
