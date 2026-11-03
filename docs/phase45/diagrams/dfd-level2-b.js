// Draws the Level 2 data-flow diagrams of processes 5.0, 6.0 and 7.0 for section 2 as SVG files.
// Usage from the repository root: node docs/phase45/diagrams/dfd-level2-b.js docs/phase45/images
// The drawing helpers are copied from dfd.js so the figures look the same.
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

// ---------- Level 2 helpers ----------
// SH is the shadow of an external entity; an arrow into an entity's right or bottom side stops at the shadow.
const SH = 6;
// horizontal flow from x1 to x2 at height y, label centred at lx (default: middle)
function H(g, x1, x2, y, label, o = {}) {
  g.flow([{ x: x1, y }, { x: x2, y }], label, { ai: o.ai, at: { x: o.lx === undefined ? (x1 + x2) / 2 : o.lx, y }, labelW: o.w || 100, size: o.size });
}
// vertical flow from y1 to y2 at x, label centred at ly (default: middle)
function V(g, x, y1, y2, label, o = {}) {
  g.flow([{ x, y: y1 }, { x, y: y2 }], label, { ai: o.ai, at: { x, y: o.ly === undefined ? (y1 + y2) / 2 : o.ly }, labelW: o.w || 100, size: o.size });
}
// dashed boundary of the parent process with its title in the bottom-left corner
function boundary(g, x, y, w, h, num) {
  g.under += `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="14" fill="#f4f8fe" stroke="${BLUE}" stroke-width="2" stroke-dasharray="7 5"/>`;
  g.under += `<text x="${x + 17}" y="${y + h - 14}" font-family="${FONT}" font-size="15" font-weight="700" fill="${DARK}">Level 2 of process ${num}</text>`;
}

// ---------- Level 2 of 5.0 Approve and Transfer Assets ----------
// 5.1 and 5.4 share D1 and D2, so they sit side by side under those two stores.
{
  const g = new Diagram();
  const L = { x: 15, w: 155 }, LE = L.x + L.w; // left column of entities and stores
  boundary(g, 215, 170, 625, 735, "5.0");
  const p1 = { x: 300, y: 250, w: 190, h: 165 }, p2 = { x: 300, y: 505, w: 190, h: 365 };
  const p4 = { x: 610, y: 250, w: 200, h: 165 }, p3 = { x: 610, y: 520, w: 200, h: 200 };
  // top stores: D1 and D2 feed 5.1 and 5.4, D7 takes the transfer impacts
  V(g, 330, 59, p1.y, "roles", { ly: 112, w: 70 });
  V(g, 710, 59, p4.y, "emission factors", { ly: 100, w: 90 });
  V(g, 450, 139, p1.y, "listings to approve", { ly: 195, w: 105 });
  V(g, 640, p4.y, 139, "new owner and location", { ly: 200, w: 112 });
  V(g, 780, p4.y, 59, "transfer impacts", { ly: 150, w: 90 });
  // 5.1 Plan Approval Stages
  H(g, LE, p1.x, 290, "end-of-life and repair cases", { w: 100 });
  H(g, LE, p1.x, 395, "holds and requests", { w: 100 });
  V(g, 395, p1.y + p1.h, p2.y, "approval stages", { ly: 455, w: 90 });
  // 5.2 Record Approval Decisions
  H(g, p2.x, LE, 535, "hold and request states", { w: 100 });
  H(g, p2.x, LE + SH, 590, "approval tasks", { w: 100 });
  H(g, LE, p2.x, 645, "approval decisions", { w: 100 });
  H(g, p2.x, LE + SH, 715, "review tasks", { w: 100 });
  H(g, LE, p2.x, 770, "end-of-life reviews", { w: 100 });
  H(g, p2.x, LE, 840, "audit entries", { w: 100 });
  V(g, 460, p2.y + p2.h, 940, "approval records", { ly: 897, w: 90 });
  H(g, p2.x + p2.w, p3.x, 565, "approved transfers", { w: 90 });
  // 5.3 Confirm Handover and Receipt
  V(g, 640, p3.y + p3.h, 940, "transfer records", { ly: 800, w: 90 });
  V(g, 720, 930, p3.y + p3.h, "handover records", { ly: 800, w: 90 });
  V(g, 795, p3.y + p3.h, 930, "transfer tasks", { ly: 880, w: 90 });
  V(g, 710, p3.y, p4.y + p4.h, "received transfers", { ly: 468, w: 90 });
  // boxes
  g.add(store("D1", D.D1, 310, 15, 420, 44));
  g.add(store("D2", D.D2, 410, 95, 255, 44));
  g.add(store("D7", D.D7, 745, 15, 180, 44));
  g.add(store("D6", D.D6, L.x, 268, L.w, 44));
  g.add(store("D3", D.D3, L.x, 375, L.w, 180));
  g.add(external("Approvers", L.x, 568, L.w, 100));
  g.add(external("Sustainability Officer", L.x, 693, L.w, 100));
  g.add(store("D8", D.D8, L.x, 818, L.w, 44));
  g.add(store("D5", D.D5, 420, 940, 260, 44));
  g.add(external("Asset Custodian", 700, 930, 215, 80));
  g.add(processBox("5.1", "Plan Approval Stages", p1.x, p1.y, p1.w, p1.h));
  g.add(processBox("5.2", "Record Approval Decisions", p2.x, p2.y, p2.w, p2.h));
  g.add(processBox("5.3", "Confirm Handover and Receipt", p3.x, p3.y, p3.w, p3.h));
  g.add(processBox("5.4", "Complete Transfer", p4.x, p4.y, p4.w, p4.h));
  g.write("dfd-level2-5.svg", 930, 1030);
}

/// ---------- Level 2 of 6.0 Maintain and Retire Assets ----------
// Work orders (6.1) and end-of-life proposals (6.2) both feed 6.3, which keeps the records; 6.4 adds up the impact.
{
  const g = new Diagram();
  const L = { x: 15, w: 155 }, LE = L.x + L.w, RX = 765, RW = 150;
  boundary(g, 215, 130, 505, 805, "6.0");
  const p1 = { x: 290, y: 250, w: 165, h: 150 }, p2 = { x: 490, y: 180, w: 145, h: 250 };
  const p3 = { x: 330, y: 510, w: 305, h: 170 }, p4 = { x: 380, y: 770, w: 200, h: 120 };
  // 6.1 Open Work Order
  V(g, 360, 75, p1.y, "defect reports", { ly: 165, w: 90 });
  H(g, p1.x, LE + SH, 380, "work orders", { w: 90 });
  V(g, 380, p1.y + p1.h, p3.y, "open work orders", { ly: 452, w: 90 });
  // 6.2 Prepare End-of-Life Proposal
  V(g, 530, 75, p2.y, "end-of-life reports", { ly: 125, w: 100 });
  H(g, p2.x + p2.w, RX, 205, "asset condition text", { ai: true, w: 100 });
  H(g, RX, p2.x + p2.w, 272, "action advice", { ai: true, w: 100 });
  H(g, p2.x + p2.w, RX, 340, "AI suggestions", { w: 100 });
  H(g, RX, p2.x + p2.w, 405, "asset details", { w: 100 });
  V(g, 590, p2.y + p2.h, p3.y, "end-of-life proposals", { ly: 466, w: 100 });
  // 6.3 Update Maintenance Records
  H(g, LE, p3.x, 535, "inspection and repair records", { w: 120 });
  H(g, LE, p3.x, 645, "approval decisions", { w: 110 });
  H(g, p3.x + p3.w, RX, 535, "condition and state", { w: 100 });
  H(g, p3.x + p3.w, RX, 635, "maintenance records", { w: 100 });
  V(g, 480, p3.y + p3.h, p4.y, "completed work", { ly: 725, w: 90 });
  // 6.4 Calculate Life-Cycle Impact
  H(g, LE, p4.x, 830, "emission factors", { w: 110 });
  H(g, p4.x + p4.w, RX, 830, "impact records", { w: 110 });
  // boxes
  g.add(external("Asset Custodian", 300, 15, 280, 60));
  g.add(external("Maintenance Staff", L.x, 360, L.w, 195));
  g.add(store("D5", D.D5, L.x, 614, L.w, 62));
  g.add(store("D1", D.D1, L.x, 808, L.w, 44));
  g.add(external(AI, RX, 182, RW, 110));
  g.add(store("D4", D.D4, RX, 318, RW, 44));
  g.add(store("D2", D.D2, RX, 383, RW, 174));
  g.add(store("D6", D.D6, RX, 613, RW, 44));
  g.add(store("D7", D.D7, RX, 808, RW, 44));
  g.add(processBox("6.1", "Open Work Order", p1.x, p1.y, p1.w, p1.h));
  g.add(processBox("6.2", "Prepare End-of-Life Proposal", p2.x, p2.y, p2.w, p2.h));
  g.add(processBox("6.3", "Update Maintenance Records", p3.x, p3.y, p3.w, p3.h));
  g.add(processBox("6.4", "Calculate Life-Cycle Impact", p4.x, p4.y, p4.w, p4.h));
  g.write("dfd-level2-6.svg", 930, 955);
}

// ---------- Level 2 of 7.0 Report Impact and History ----------
// 7.1 gathers the figures; 7.2 drafts the AI text; 7.3 issues the reports; 7.4 reads the audit log for history.
{
  const g = new Diagram();
  const L = { x: 15, w: 160 }, LE = L.x + L.w;
  boundary(g, 215, 160, 625, 775, "7.0");
  const p1 = { x: 320, y: 215, w: 180, h: 375 }, p2 = { x: 610, y: 215, w: 190, h: 185 };
  const p3 = { x: 320, y: 670, w: 180, h: 210 }, p4 = { x: 610, y: 780, w: 190, h: 120 };
  // 7.1 Calculate Report Totals
  const reads = [["D2", "asset and listing records"], ["D3", "request and hold records"], ["D5", "transfer records"], ["D6", "maintenance records"], ["D7", "impact records"]];
  reads.forEach(([id, label], i) => {
    const y = 240 + i * 66;
    H(g, LE, p1.x, y, label, { w: 110 });
    g.add(store(id, D[id], L.x, y - 28, L.w, 56));
  });
  H(g, LE, p1.x, 566, "report requests", { w: 110 });
  V(g, 470, 134, p1.y, "AI records", { ly: 180, w: 90 });
  H(g, p1.x + p1.w, p2.x, 300, "report totals", { w: 90 });
  V(g, 410, p1.y + p1.h, p3.y, "report totals", { ly: 624, w: 90 });
  // 7.2 Draft Report Summary
  V(g, 640, p2.y, 134, "AI suggestions", { ly: 180, w: 90 });
  V(g, 715, p2.y, 60 + SH, "report figures", { ai: true, ly: 100, w: 80 });
  V(g, 790, 60, p2.y, "draft report text", { ai: true, ly: 169, w: 110 });
  g.flow([{ x: 650, y: p2.y + p2.h }, { x: 650, y: 720 }, { x: p3.x + p3.w, y: 720 }], "draft summary", { at: { x: 575, y: 720 }, labelW: 100 });
  // 7.3 Issue Reports
  H(g, p3.x, LE + SH, 700, "operational and audit reports", { w: 110 });
  H(g, p3.x, LE + SH, 770, "finance and reuse reports", { w: 110 });
  H(g, p3.x, LE + SH, 845, "impact report", { w: 110 });
  // 7.4 Trace Asset History
  H(g, p4.x, p3.x + p3.w, 830, "audit results", { w: 90 });
  V(g, 650, 990, p4.y + p4.h, "audit entries", { ly: 946, w: 90 });
  V(g, 765, p4.y + p4.h, 980, "asset history", { ly: 934, w: 90 });
  // boxes
  g.add(external("Administrators", L.x, 548, L.w, 170));
  g.add(external("Approvers", L.x, 742, L.w, 56));
  g.add(external("Sustainability Officer", L.x, 815, L.w, 60));
  g.add(store("D4", D.D4, 400, 90, 270, 44));
  g.add(external(AI, 700, 10, 210, 50));
  g.add(store("D8", D.D8, 470, 990, 230, 44));
  g.add(external("Asset Custodian", 720, 980, 195, 70));
  g.add(processBox("7.1", "Calculate Report Totals", p1.x, p1.y, p1.w, p1.h));
  g.add(processBox("7.2", "Draft Report Summary", p2.x, p2.y, p2.w, p2.h));
  g.add(processBox("7.3", "Issue Reports", p3.x, p3.y, p3.w, p3.h));
  g.add(processBox("7.4", "Trace Asset History", p4.x, p4.y, p4.w, p4.h));
  g.write("dfd-level2-7.svg", 930, 1070);
}
