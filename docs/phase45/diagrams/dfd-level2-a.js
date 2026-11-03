// Draws the Level 2 data-flow diagrams of processes 1.0, 2.0 and 4.0 for section 2 as SVG files.
// Usage from the repository root: node docs/phase45/diagrams/dfd-level2-a.js docs/phase45/images
// The drawing helpers are copied from dfd.js so every data-flow diagram has the same look.
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
  // the dashed boundary of the parent process, with its title
  boundary(x, y, w, h, title, tx, ty) {
    this.under += `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="14" fill="#f4f8fe" stroke="${BLUE}" stroke-width="2" stroke-dasharray="7 5"/>`;
    this.under += `<text x="${tx}" y="${ty}" font-family="${FONT}" font-size="15" font-weight="700" fill="${DARK}">${esc(title)}</text>`;
  }
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
// An arrow into an external entity stops at the edge of its shadow, so the whole arrowhead shows.
const SHADOW = 6;

// ---------- Level 2 of 1.0 Manage Accounts and Settings ----------
// Administrators sit above the boundary. 1.1 to 1.3 each check one kind of change,
// and 1.4 saves every checked change in D1 and its audit entry in D8.
{
  const g = new Diagram();
  g.boundary(105, 140, 740, 440, "Level 2 of process 1.0", 122, 566);
  const p1 = { x: 140, y: 235, w: 170, h: 100 }, p2 = { x: 370, y: 235, w: 170, h: 100 };
  const p3 = { x: 640, y: 235, w: 170, h: 100 }, p4 = { x: 470, y: 425, w: 170, h: 110 };
  const adminBottom = 85;
  // inputs from Administrators and the status going back
  g.flow([{ x: 225, y: adminBottom }, { x: 225, y: p1.y }], "account details", { at: { x: 225, y: 140 }, labelW: 100 });
  g.flow([{ x: 455, y: adminBottom }, { x: 455, y: p2.y }], "role assignments", { at: { x: 455, y: 140 }, labelW: 110 });
  g.flow([{ x: 725, y: adminBottom }, { x: 725, y: p3.y }], "settings", { at: { x: 725, y: 140 }, labelW: 100 });
  g.flow([{ x: 590, y: p4.y }, { x: 590, y: adminBottom + SHADOW }], "account status", { at: { x: 590, y: 140 }, labelW: 100 });
  // checked changes go to 1.4
  g.flow([{ x: 225, y: p1.y + p1.h }, { x: 225, y: 470 }, { x: p4.x, y: 470 }], "account changes", { at: { x: 225, y: 405 }, labelW: 100 });
  g.flow([{ x: 505, y: p2.y + p2.h }, { x: 505, y: p4.y }], "role decisions", { at: { x: 505, y: 375 }, labelW: 100 });
  g.flow([{ x: 725, y: p3.y + p3.h }, { x: 725, y: 470 }, { x: p4.x + p4.w, y: 470 }], "setting changes", { at: { x: 725, y: 405 }, labelW: 100 });
  // 1.4 writes the stores
  g.flow([{ x: p4.x, y: 510 }, { x: 400, y: 510 }, { x: 400, y: 650 }], "user, role and setting records", { at: { x: 400, y: 600 }, labelW: 150 });
  g.flow([{ x: p4.x + p4.w, y: 510 }, { x: 710, y: 510 }, { x: 710, y: 650 }], "audit entries", { at: { x: 710, y: 600 }, labelW: 100 });
  // boxes
  g.add(external("Administrators", 180, 15, 570, adminBottom - 15, { sub: "business administrator, system administrator" }));
  g.add(store("D1", D.D1, 300, 650, 210, 48));
  g.add(store("D8", D.D8, 610, 650, 210, 48));
  g.add(processBox("1.1", "Check Account Details", p1.x, p1.y, p1.w, p1.h));
  g.add(processBox("1.2", "Authorise Role Assignments", p2.x, p2.y, p2.w, p2.h));
  g.add(processBox("1.3", "Check Setting Changes", p3.x, p3.y, p3.w, p3.h));
  g.add(processBox("1.4", "Save Changes", p4.x, p4.y, p4.w, p4.h));
  g.write("dfd-level2-1.svg", 930, 720);
}

// ---------- Level 2 of 2.0 Register and Publish Assets ----------
// The custodian is on the left with D5, the AI Provider above, and D1, D4 and D2 on the right.
{
  const g = new Diagram();
  g.boundary(205, 100, 510, 590, "Level 2 of process 2.0", 222, 124);
  const p1 = { x: 275, y: 190, w: 165, h: 100 }, p2 = { x: 485, y: 205, w: 165, h: 110 };
  const p3 = { x: 275, y: 425, w: 165, h: 100 }, p4 = { x: 485, y: 570, w: 165, h: 100 };
  const custRight = 165, aiBottom = 70;
  // 2.1 Check Asset Details
  g.flow([{ x: custRight, y: 245 }, { x: p1.x, y: 245 }], "asset details", { at: { x: 220, y: 245 }, labelW: 95 });
  g.flow([{ x: 420, y: p1.y + p1.h }, { x: 420, y: 350 }, { x: 560, y: 350 }, { x: 560, y: p2.y + p2.h }], "asset description", { at: { x: 490, y: 350 }, labelW: 110 });
  g.flow([{ x: 340, y: p1.y + p1.h }, { x: 340, y: p3.y }], "checked details", { at: { x: 340, y: 357 }, labelW: 95 });
  // 2.2 Suggest Category
  g.flow([{ x: 775, y: 233 }, { x: p2.x + p2.w, y: 233 }], "categories", { at: { x: 720, y: 233 }, labelW: 95 });
  g.flow([{ x: 525, y: p2.y }, { x: 525, y: aiBottom + SHADOW }], "asset text", { ai: true, at: { x: 525, y: 112 }, labelW: 95 });
  g.flow([{ x: 620, y: aiBottom + SHADOW }, { x: 620, y: p2.y }], "category and tags", { ai: true, at: { x: 620, y: 150 }, labelW: 95 });
  g.flow([{ x: 500, y: p2.y }, { x: 500, y: 160 }, { x: custRight + SHADOW, y: 160 }], "suggested category", { at: { x: 240, y: 160 }, labelW: 170 });
  g.flow([{ x: p2.x + p2.w, y: 290 }, { x: 775, y: 290 }], "AI suggestions", { at: { x: 710, y: 290 }, labelW: 95 });
  // 2.3 Save Asset Record
  g.flow([{ x: p3.x + p3.w, y: 450 }, { x: 775, y: 450 }], "asset records", { at: { x: 706, y: 450 }, labelW: 95 });
  g.flow([{ x: p3.x + p3.w, y: 500 }, { x: 565, y: 500 }, { x: 565, y: p4.y }], "confirmed asset", { at: { x: 503, y: 500 }, labelW: 95 });
  // 2.4 Publish Listing
  g.flow([{ x: 165, y: 625 }, { x: p4.x, y: 625 }], "release decisions", { at: { x: 220, y: 625 }, labelW: 95 });
  g.flow([{ x: p4.x + p4.w, y: 615 }, { x: 840, y: 615 }, { x: 840, y: 478 }], "listing records", { at: { x: 840, y: 550 }, labelW: 95 });
  // boxes
  g.add(external("Asset Custodian", 15, 135, 150, 150, { sub: "or department representative" }));
  g.add(external(AI, 485, 14, 165, aiBottom - 14));
  g.add(store("D1", D.D1, 775, 210, 145, 46));
  g.add(store("D4", D.D4, 775, 267, 145, 46));
  g.add(store("D2", D.D2, 775, 422, 145, 56));
  g.add(store("D5", D.D5, 15, 597, 150, 56));
  g.add(processBox("2.1", "Check Asset Details", p1.x, p1.y, p1.w, p1.h));
  g.add(processBox("2.2", "Suggest Category", p2.x, p2.y, p2.w, p2.h));
  g.add(processBox("2.3", "Save Asset Record", p3.x, p3.y, p3.w, p3.h));
  g.add(processBox("2.4", "Publish Listing", p4.x, p4.y, p4.w, p4.h));
  g.write("dfd-level2-2.svg", 930, 710);
}

// ---------- Level 2 of 4.0 Answer Assistant Questions ----------
// The Requester is above the boundary, D2 on the left, and D4 and the AI Provider on the right.
{
  const g = new Diagram();
  g.boundary(205, 110, 510, 445, "Level 2 of process 4.0", 222, 540);
  const p1 = { x: 275, y: 215, w: 165, h: 100 }, p3 = { x: 490, y: 215, w: 165, h: 100 };
  const p2 = { x: 380, y: 410, w: 165, h: 100 };
  const reqBottom = 80;
  // 4.1 Check Question Access
  g.flow([{ x: 360, y: reqBottom }, { x: 360, y: p1.y }], "assistant question", { at: { x: 360, y: 168 }, labelW: 100 });
  g.flow([{ x: 410, y: p1.y + p1.h }, { x: 410, y: p2.y }], "checked question", { at: { x: 410, y: 357 }, labelW: 100 });
  // 4.2 Gather Permitted Records
  g.flow([{ x: 165, y: 460 }, { x: p2.x, y: 460 }], "permitted listings", { at: { x: 230, y: 460 }, labelW: 100 });
  g.flow([{ x: p2.x + p2.w, y: 470 }, { x: 775, y: 470 }], "question context", { ai: true, at: { x: 680, y: 470 }, labelW: 100 });
  g.flow([{ x: 520, y: p2.y }, { x: 520, y: p3.y + p3.h }], "source records", { at: { x: 520, y: 368 }, labelW: 100 });
  // 4.3 Check and Return Answer
  g.flow([{ x: 840, y: 440 }, { x: 840, y: 295 }, { x: p3.x + p3.w, y: 295 }], "draft answer", { ai: true, at: { x: 840, y: 370 }, labelW: 95 });
  g.flow([{ x: p3.x + p3.w, y: 240 }, { x: 775, y: 240 }], "assistant records", { at: { x: 705, y: 240 }, labelW: 100 });
  g.flow([{ x: 570, y: p3.y }, { x: 570, y: reqBottom + SHADOW }], "assistant answer", { at: { x: 570, y: 168 }, labelW: 100 });
  // boxes
  g.add(external("Requester", 290, 15, 350, reqBottom - 15));
  g.add(external(AI, 775, 440, 145, 60));
  g.add(store("D2", D.D2, 15, 435, 150, 50));
  g.add(store("D4", D.D4, 775, 217, 145, 46));
  g.add(processBox("4.1", "Check Question Access", p1.x, p1.y, p1.w, p1.h));
  g.add(processBox("4.2", "Gather Permitted Records", p2.x, p2.y, p2.w, p2.h));
  g.add(processBox("4.3", "Check and Return Answer", p3.x, p3.y, p3.w, p3.h));
  g.write("dfd-level2-4.svg", 930, 580);
}
