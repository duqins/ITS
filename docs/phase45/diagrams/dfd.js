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

// External entity: a box with a shadow 6 px to the right and below.
function external(name, x, y, w, h, opts = {}) {
  const size = opts.size || 17;
  let s = `<rect x="${x + 6}" y="${y + 6}" width="${w}" height="${h}" fill="${DARK}"/>`;
  s += `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${FILL}" stroke="${DARK}" stroke-width="2"/>`;
  const main = wrap(name, w - 18, size, true);
  const sub = opts.sub ? wrap(opts.sub, w - 14, 14) : [];
  const lhM = size * 1.15, lhS = 14 * 1.2;
  const total = main.length * lhM + sub.length * lhS;
  let yy = y + h / 2 - total / 2 + size * 0.85;
  main.forEach((l) => { s += `<text x="${x + w / 2}" y="${yy}" text-anchor="middle" font-family="${FONT}" font-size="${size}" font-weight="700" fill="#111">${esc(l)}</text>`; yy += lhM; });
  sub.forEach((l) => { s += `<text x="${x + w / 2}" y="${yy - 2}" text-anchor="middle" font-family="${FONT}" font-size="14" fill="#333">${esc(l)}</text>`; yy += lhS; });
  return s;
}

// Process: rounded box with a blue band that holds the process number.
function processBox(num, name, x, y, w, h, opts = {}) {
  const band = opts.band || 26, numSize = opts.numSize || 15, size = opts.size || 17;
  let s = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="#fff" stroke="${DARK}" stroke-width="2"/>`;
  s += `<path d="M${x} ${y + band} V${y + 10} Q${x} ${y} ${x + 10} ${y} H${x + w - 10} Q${x + w} ${y} ${x + w} ${y + 10} V${y + band} Z" fill="${BLUE}" stroke="${DARK}" stroke-width="2"/>`;
  s += `<text x="${x + w / 2}" y="${y + Math.round(band * 0.73)}" text-anchor="middle" font-family="${FONT}" font-size="${numSize}" font-weight="700" fill="#fff">${esc(num)}</text>`;
  s += textBlock(wrap(name, w - 18, size, true), x + w / 2, y + band + (h - band) / 2, size, { bold: true });
  return s;
}

// Data store: open on the right, with the D-number in its own compartment.
function store(id, name, x, y, w, h, opts = {}) {
  const size = opts.size || 14.5, idSize = opts.idSize || 15, idW = opts.idW || 44;
  let s = `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="#fff" stroke="none"/>`;
  s += `<path d="M${x + w} ${y} H${x} V${y + h} H${x + w}" fill="none" stroke="${DARK}" stroke-width="2"/>`;
  s += `<line x1="${x + idW}" y1="${y}" x2="${x + idW}" y2="${y + h}" stroke="${DARK}" stroke-width="2"/>`;
  s += `<text x="${x + idW / 2}" y="${y + h / 2 + idSize / 3}" text-anchor="middle" font-family="${FONT}" font-size="${idSize}" font-weight="700" fill="#111">${esc(id)}</text>`;
  const lines = wrap(name, w - idW - 12, size, true);
  const lh = size * 1.15;
  let yy = y + h / 2 - ((lines.length - 1) * lh) / 2 + size / 3;
  lines.forEach((l) => { s += `<text x="${x + idW + 8}" y="${yy}" font-family="${FONT}" font-size="${size}" font-weight="700" fill="#111">${esc(l)}</text>`; yy += lh; });
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

const overlap = (a, b, m) => a.x < b.x + b.w + m && b.x < a.x + a.w + m && a.y < b.y + b.h + m && b.y < a.y + a.h + m;
// true when the straight segment p-q touches the rectangle r grown by m on every side
function segHitsRect(p, q, r, m) {
  const x0 = r.x - m, x1 = r.x + r.w + m, y0 = r.y - m, y1 = r.y + r.h + m;
  let t0 = 0, t1 = 1;
  const dx = q.x - p.x, dy = q.y - p.y;
  for (const [pp, qq] of [[-dx, p.x - x0], [dx, x1 - p.x], [-dy, p.y - y0], [dy, y1 - p.y]]) {
    if (pp === 0) { if (qq < 0) return false; continue; }
    const t = qq / pp;
    if (pp < 0) { if (t > t1) return false; if (t > t0) t0 = t; } else { if (t < t0) return false; if (t < t1) t1 = t; }
  }
  return true;
}
const segmentsOf = (pts) => pts.slice(1).map((q, i) => [pts[i], q]);

// A diagram collects lines, boxes and labels separately so labels are always drawn on top.
// With { auto: true }, a label without a given position is placed on its own line where it covers
// no other line, box, label or arrowhead.
class Diagram {
  constructor(opts = {}) {
    this.under = ""; this.lines = ""; this.boxes = ""; this.labels = "";
    this.auto = !!opts.auto; this.size = opts.size || 15; this.labelW = opts.labelW || 160;
    this.polys = []; this.rects = []; this.pills = []; this.pending = [];
  }
  // points: polyline; label placed at opts.at, or at fraction opts.t along the first segment
  flow(points, label, opts = {}) {
    const color = opts.ai ? TEAL : BLUE;
    this.lines += `<polyline points="${points.map((p) => `${p.x},${p.y}`).join(" ")}" fill="none" stroke="${color}" stroke-width="2"/>`;
    const n = points.length;
    this.lines += arrowHead(points[n - 2], points[n - 1], color);
    this.polys.push(points);
    if (!label) return;
    const size = opts.size || this.size;
    if (this.auto && !opts.at && opts.t === undefined) { this.pending.push({ points, label, opts, size, index: this.polys.length - 1 }); return; }
    let at = opts.at;
    if (!at) {
      const t = opts.t === undefined ? 0.5 : opts.t;
      at = { x: points[0].x + (points[1].x - points[0].x) * t, y: points[0].y + (points[1].y - points[0].y) * t };
    }
    const fit = clearOfArrow(points, at, opts.labelW || 160, size, label);
    this.labels += pill(label, fit.at.x, fit.at.y, fit.maxW, size);
    const { w, h } = pillSize(label, fit.maxW, size);
    this.pills.push({ x: fit.at.x - w / 2, y: fit.at.y - h / 2, w, h });
  }
  // rect: the area the box covers, so automatic labels stay off it
  add(svg, rect) { this.boxes += svg; if (rect) this.rects.push(rect); }
  // every free spot for a label on its own line, nearest the middle of a long straight part first
  spots(f, W, H, taken) {
    const out = [];
    const base = f.opts.labelW || this.labelW;
    for (const maxW of [base, 190, 300, 130, 110]) {
      const { w, h } = pillSize(f.label, maxW, f.size);
      segmentsOf(f.points).forEach(([a, b], i, all) => {
        const horiz = a.y === b.y, len = Math.abs(horiz ? b.x - a.x : b.y - a.y), dir = Math.sign(horiz ? b.x - a.x : b.y - a.y);
        const half = (horiz ? w : h) / 2, lo = half + 6, hi = len - half - (i === all.length - 1 ? CLEAR + 6 : 6);
        for (let d = lo; d <= hi; d += 4) {
          const c = horiz ? { x: a.x + dir * d, y: a.y } : { x: a.x, y: a.y + dir * d };
          const r = { x: c.x - w / 2, y: c.y - h / 2, w, h };
          if (r.x < 4 || r.y < 4 || r.x + w > W - 4 || r.y + h > H - 4) continue;
          if (this.rects.some((b2) => overlap(r, b2, 6))) continue;
          if (taken.some((b2) => overlap(r, b2, 5))) continue;
          if (this.polys.some((pts, k) => k !== f.index && segmentsOf(pts).some(([p, q]) => segHitsRect(p, q, r, 4)))) continue;
          const score = Math.abs(d - (lo + hi) / 2) / len - Math.min(len, 500) / 1000 + (f.opts.seg !== undefined && f.opts.seg !== i ? 3 : 0) + (maxW === base ? 0 : maxW > base ? 0.3 : 0.5);
          out.push({ score, c, maxW, r });
        }
      });
    }
    return out.sort((p, q) => p.score - q.score);
  }
  placeLabels(W, H) {
    const placed = new Map(); // flow -> chosen spot
    const taken = (except) => [...this.pills, ...[...placed].filter(([f]) => f !== except).map(([, sp]) => sp.r)];
    // labels with the fewest free spots go first
    const order = this.pending.map((f) => ({ f, n: this.spots(f, W, H, this.pills).length })).sort((a, b) => a.n - b.n);
    for (const { f } of order) {
      const best = this.spots(f, W, H, taken())[0];
      if (best) placed.set(f, best);
      else if (!this.makeRoom(f, W, H, placed, taken)) console.warn(`no free spot for the label "${f.label}"`);
    }
    for (const [f, sp] of placed) this.labels += pill(f.label, sp.c.x, sp.c.y, sp.maxW, f.size);
  }
  // when a label has no free spot, move up to two labels that are in its way to other free spots
  makeRoom(f, W, H, placed, taken) {
    for (const cand of this.spots(f, W, H, this.pills).slice(0, 60)) {
      const blockers = [...placed].filter(([, sp]) => overlap(sp.r, cand.r, 5)).map(([g2]) => g2);
      if (blockers.length > 2) continue;
      const old = blockers.map((b) => placed.get(b));
      blockers.forEach((b) => placed.delete(b));
      placed.set(f, cand);
      const moved = [];
      for (const b of blockers) { const sp = this.spots(b, W, H, taken(b))[0]; if (!sp) break; placed.set(b, sp); moved.push(b); }
      if (moved.length === blockers.length) return true;
      placed.delete(f);
      moved.forEach((b) => placed.delete(b));
      blockers.forEach((b, i) => placed.set(b, old[i]));
    }
    return false;
  }
  write(file, w, h) {
    if (this.pending.length) this.placeLabels(w, h);
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
        // on the left, lines end at the edge of the box shadow so the arrowhead is not hidden
        const ext = { x: isLeft ? box.x + box.w + 6 : box.x, y: yy }, pr = { x: isLeft ? P.x : P.x + P.w, y: yy };
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

// ---------- Store flows between two rows of processes and a row of stores ----------
// Each flow leaves its process edge straight, runs along its own horizontal track and enters its store edge
// straight. Ports keep the order of the boxes they lead to, and tracks are ordered to keep crossings low.
// list items: { p, s, write, label }; p.edge is "bottom" for the upper process row and "top" for the lower one.
// Tracks stay out of a strip of height `zone` next to each row, so the labels have room there.
function routeStoreFlows(g, list, gap, zone) {
  const spread = (items, lo, hi, key) => { // place ports in order, near their wish, at least `gap` apart
    items.sort((a, b) => a.wish - b.wish || a.tie - b.tie);
    const n = items.length, step = Math.min(gap, (hi - lo) / Math.max(1, n - 1));
    items.forEach((it, i) => { it[key] = Math.min(hi - (n - 1 - i) * step, Math.max(lo + i * step, it.wish)); });
    for (let i = 1; i < n; i++) items[i][key] = Math.max(items[i][key], items[i - 1][key] + step);
    for (let i = n - 2; i >= 0; i--) items[i][key] = Math.min(items[i][key], items[i + 1][key] - step);
  };
  const groups = (key) => { const m = new Map(); for (const f of list) { const k = key(f); if (!m.has(k)) m.set(k, []); m.get(k).push(f); } return [...m.values()]; };
  const centre = (b) => b.x + b.w / 2;
  // process ports: evenly spread, in the order of the stores they lead to
  for (const grp of groups((f) => f.p.id)) {
    const [lo, hi] = grp[0].p.range;
    grp.sort((a, b) => centre(a.s) - centre(b.s) || a.write - b.write);
    grp.forEach((f, i) => { f.xp = Math.round(grp.length === 1 ? (lo + hi) / 2 : lo + ((hi - lo) * i) / (grp.length - 1)); });
  }
  // store ports: straight under or over the process port when the store reaches it
  for (const grp of groups((f) => f.s.id + f.p.edge)) {
    const lo = grp[0].s.x + 14, hi = grp[0].s.x + grp[0].s.w - 14;
    grp.forEach((f) => { f.wish = Math.min(hi, Math.max(lo, f.xp)); f.tie = f.xp; });
    spread(grp, lo, hi, "xs");
  }
  // straighten a jog when one end can move straight over the other without passing a neighbour
  for (const f of list) {
    if (Math.abs(f.xp - f.xs) < 0.5) continue;
    const keepsOrder = (sibs, key, to) => sibs.every((o) => Math.abs(o[key] - to) >= 40 && Math.sign(o[key] - f[key]) === Math.sign(o[key] - to));
    const onP = list.filter((o) => o !== f && o.p === f.p), onS = list.filter((o) => o !== f && o.s === f.s && o.p.edge === f.p.edge);
    if (f.xs >= f.p.range[0] && f.xs <= f.p.range[1] && keepsOrder(onP, "xp", f.xs)) f.xp = f.xs;
    else if (f.xp >= f.s.x + 14 && f.xp <= f.s.x + f.s.w - 14 && keepsOrder(onS, "xs", f.xp)) f.xs = f.xp;
  }
  // tracks, one channel above the stores and one below
  for (const edge of ["bottom", "top"]) {
    const fl = list.filter((f) => f.p.edge === edge && Math.abs(f.xp - f.xs) > 0.5);
    if (!fl.length) continue;
    const yP = edge === "bottom" ? fl[0].p.y + fl[0].p.h : fl[0].p.y;
    const yS = edge === "bottom" ? Math.min(...list.filter((f) => f.p.edge === edge).map((f) => f.s.y)) : Math.max(...list.filter((f) => f.p.edge === edge).map((f) => f.s.y + f.s.h));
    const inside = (x, f) => x > Math.min(f.xp, f.xs) && x < Math.max(f.xp, f.xs);
    const cost = (f, g2) => (inside(f.xs, g2) ? 1 : 0) + (inside(g2.xp, f) ? 1 : 0); // f nearer the process row than g2
    const total = (o) => { let c = 0; for (let i = 0; i < o.length; i++) for (let j = i + 1; j < o.length; j++) c += cost(o[i], o[j]); return c; };
    let order = fl.slice().sort((a, b) => Math.abs(a.xp - a.xs) - Math.abs(b.xp - b.xs));
    for (let improved = true; improved;) {
      improved = false;
      for (let i = 0; i < order.length; i++) {
        const f = order[i], rest = order.filter((_, k) => k !== i);
        let best = total(order), bestAt = i;
        for (let k = 0; k <= rest.length; k++) { const c = total([...rest.slice(0, k), f, ...rest.slice(k)]); if (c < best) { best = c; bestAt = k; } }
        if (bestAt !== i) { order = [...rest.slice(0, bestAt), f, ...rest.slice(bestAt)]; improved = true; }
      }
    }
    const dir = Math.sign(yS - yP), span = Math.abs(yS - yP) - 2 * zone;
    order.forEach((f, i) => { f.track = Math.round(yP + dir * (zone + (span * (i + 0.5)) / order.length)); });
  }
  for (const f of list) {
    const yP = f.p.edge === "bottom" ? f.p.y + f.p.h : f.p.y, yS = f.p.edge === "bottom" ? f.s.y : f.s.y + f.s.h;
    const pts = Math.abs(f.xp - f.xs) > 0.5
      ? [{ x: f.xp, y: yP }, { x: f.xp, y: f.track }, { x: f.xs, y: f.track }, { x: f.xs, y: yS }]
      : [{ x: f.xp, y: yP }, { x: f.xs, y: yS }];
    g.flow(f.write ? pts : pts.reverse(), f.label);
  }
}

// ---------- Figure 2.1: Level 1 (printed alone on an A3 landscape page) ----------
// Processes 1.0 to 4.0 form the top row and 7.0, 5.0 and 6.0 the bottom row. The data stores sit between
// the rows, the external entities around the outside, and every entity and store is drawn once.
{
  const W = 2600, H = 1525;
  const g = new Diagram({ auto: true, size: 18, labelW: 170 });
  const F = (xy, label, opts) => g.flow(xy.map(([x, y]) => ({ x, y })), label, opts);
  const ent = (name, x, y, w, h) => { g.add(external(name, x, y, w, h, { size: 20 }), { x, y, w: w + 6, h: h + 6 }); };
  const proc = (id, num, name, x, y, w, h, edge, range) => { g.add(processBox(num, name, x, y, w, h, { band: 32, numSize: 19, size: 21 }), { x, y, w, h }); return { id, x, y, w, h, edge, range }; };
  const sto = (id, x, y, w, h = 58) => { g.add(store(id, D[id], x, y, w, h, { size: 18, idSize: 19, idW: 54 }), { x, y, w, h }); return { id, x, y, w, h }; };

  // rows (y): AI Provider 14, Requester 84, top processes 228-340, stores 594-652, bottom processes 986-1094,
  // then Approvers, Maintenance Staff and D6 at 1210, Sustainability Officer and D7 at 1340, Asset Custodian at 1450
  // processes: x, y, width, height, the edge that faces the stores, and the part of that edge the store flows use
  const P1 = proc("P1", "1.0", "Manage Accounts and Settings", 110, 228, 290, 112, "bottom", [300, 390]);
  const P2 = proc("P2", "2.0", "Register and Publish Assets", 620, 228, 360, 112, "bottom", [640, 960]);
  const P3 = proc("P3", "3.0", "Request, Match and Reserve Assets", 1200, 228, 400, 112, "bottom", [1220, 1580]);
  const P4 = proc("P4", "4.0", "Answer Assistant Questions", 1840, 228, 400, 112, "bottom", [1860, 2220]);
  const P7 = proc("P7", "7.0", "Report Impact and History", 110, 986, 590, 108, "top", [290, 690]);
  const P5 = proc("P5", "5.0", "Approve and Transfer Assets", 860, 986, 660, 108, "top", [880, 1500]);
  const P6 = proc("P6", "6.0", "Maintain and Retire Assets", 1700, 986, 680, 108, "top", [1720, 2360]);
  // stores between the rows; D6 and D7 sit under the bottom row because only 5.0, 6.0 and 7.0 use them
  const SY = 594, SW = 270;
  const D8 = sto("D8", 320, SY, SW), D3 = sto("D3", 668, SY, SW), D1 = sto("D1", 1016, SY, SW), D5 = sto("D5", 1364, SY, SW), D4 = sto("D4", 1712, SY, SW), D2 = sto("D2", 2060, SY, 320);
  sto("D6", 1500, 1210, 260, 52); sto("D7", 1380, 1340, 420, 52);
  // external entities
  ent(AI, 560, 14, 1720, 50);
  ent("Requester", 1370, 84, 670, 48);
  ent("Administrators", 110, 585, 180, 68);
  ent("Approvers", 600, 1210, 420, 52);
  ent("Sustainability Officer", 480, 1340, 720, 52);
  ent("Maintenance Staff", 2080, 1210, 300, 52);
  ent("Asset Custodian", 160, 1450, 1800, 52);

  // flows between the processes and the stores in the middle band
  const band = [
    [P1, D8, 1, "audit entries"], [P1, D1, 1, "user, role and setting records"],
    [P2, D1, 0, "categories"], [P2, D5, 0, "release decisions"], [P2, D2, 1, "asset and listing records"], [P2, D4, 1, "AI suggestions"],
    [P3, D2, 0, "published listings"], [P3, D5, 0, "request decisions"], [P3, D3, 1, "request and hold records"], [P3, D4, 1, "match records"],
    [P4, D2, 0, "permitted listings"], [P4, D4, 1, "assistant records"],
    [P5, D1, 0, "roles and emission factors"], [P5, D3, 0, "holds and requests"], [P5, D3, 1, "hold and request states"],
    [P5, D5, 1, "approval and transfer records"], [P5, D2, 0, "listings to approve"], [P5, D2, 1, "new owner and location"], [P5, D8, 1, "audit entries"],
    [P6, D1, 0, "emission factors"], [P6, D2, 0, "asset details"], [P6, D2, 1, "condition and state"], [P6, D5, 0, "approval decisions"], [P6, D4, 1, "AI suggestions"],
    [P7, D2, 0, "asset and listing records"], [P7, D3, 0, "request and hold records"], [P7, D4, 0, "AI records"], [P7, D4, 1, "AI suggestions"],
    [P7, D5, 0, "transfer records"], [P7, D8, 0, "audit entries"],
  ];
  routeStoreFlows(g, band.map(([p, s, w, label]) => ({ p, s, write: !!w, label })), 46, 72);

  // Administrators, between 1.0 and 7.0
  F([[166, 585], [166, 340]], "account details, role assignments, settings");
  F([[250, 340], [250, 585]], "account status");
  F([[166, 659], [166, 986]], "report requests");
  F([[250, 986], [250, 659]], "operational and audit reports");
  // AI Provider: straight down to 2.0, 3.0 and 4.0, round the left side to 7.0 and round the right side to 6.0
  const ai = { ai: true };
  F([[800, 228], [800, 70]], "asset text", ai);
  F([[920, 70], [920, 228]], "category and tags", ai);
  F([[1220, 228], [1220, 70]], "request text", ai);
  F([[1290, 70], [1290, 228]], "embedding vectors", ai);
  F([[2100, 228], [2100, 70]], "question context", ai);
  F([[2210, 70], [2210, 228]], "draft answer", ai);
  F([[110, 1016], [40, 1016], [40, 46], [560, 46]], "report figures", ai);
  F([[560, 26], [20, 26], [20, 1064], [110, 1064]], "draft report text", ai);
  F([[2380, 1016], [2560, 1016], [2560, 46], [2286, 46]], "asset condition text", ai);
  F([[2286, 26], [2580, 26], [2580, 1064], [2380, 1064]], "action advice", ai);
  // Requester, over 3.0 and 4.0
  F([[1390, 138], [1390, 228]], "resource request, match choice");
  F([[1580, 228], [1580, 138]], "ranked matches, request status");
  F([[1860, 138], [1860, 228]], "assistant question");
  F([[2000, 228], [2000, 138]], "assistant answer");
  // Asset Custodian: up the left side to 2.0, and straight up to 7.0, 5.0 and 6.0
  F([[720, 228], [720, 160], [60, 160], [60, 1488], [160, 1488]], "suggested category");
  F([[160, 1466], [80, 1466], [80, 200], [660, 200], [660, 228]], "asset details");
  F([[180, 1094], [180, 1450]], "asset history");
  F([[1240, 1450], [1240, 1094]], "handover records");
  F([[1300, 1094], [1300, 1450]], "transfer tasks");
  F([[1880, 1450], [1880, 1094]], "defect and end-of-life reports");
  // Approvers and Sustainability Officer, under 7.0 and 5.0
  F([[650, 1094], [650, 1210]], "finance and reuse reports");
  F([[880, 1210], [880, 1094]], "approval decisions");
  F([[980, 1094], [980, 1210]], "approval tasks");
  F([[520, 1094], [520, 1340]], "impact report");
  F([[1080, 1340], [1080, 1094]], "end-of-life reviews");
  F([[1170, 1094], [1170, 1340]], "review tasks");
  // Maintenance Staff, under 6.0
  F([[2140, 1210], [2140, 1094]], "inspection and repair records");
  F([[2320, 1094], [2320, 1210]], "work orders");
  // D6 and D7, between 5.0 and 6.0, with longer flows to 7.0
  F([[1510, 1210], [1510, 1094]], "end-of-life and repair cases");
  F([[1710, 1094], [1710, 1210]], "maintenance records");
  F([[1500, 1236], [1360, 1236], [1360, 1410], [440, 1410], [440, 1094]], "maintenance records");
  F([[1430, 1094], [1430, 1340]], "transfer impacts");
  F([[1790, 1094], [1790, 1340]], "impact records");
  F([[1400, 1392], [1400, 1424], [300, 1424], [300, 1094]], "impact records");

  g.write("dfd-level1.svg", W, H);
}

// ---------- Figure 2.2: Level 2 of 3.0 ----------
// 3.1 to 3.4 run top to bottom inside the dashed boundary of 3.0. The Requester sits on the left, the data
// stores and the AI Provider on the right, each drawn once; the hold record goes round the right edge to D3.
{
  const g = new Diagram();
  const F = (xy, label, at, opts = {}) => g.flow(xy.map(([x, y]) => ({ x, y })), label, { at: { x: at[0], y: at[1] }, labelW: 150, ...opts });
  g.under += `<rect x="300" y="14" width="280" height="890" rx="14" fill="#f4f8fe" stroke="${BLUE}" stroke-width="2" stroke-dasharray="7 5"/>`;
  g.under += `<text x="316" y="40" font-family="${FONT}" font-size="15" font-weight="700" fill="${DARK}">Level 2 of process 3.0</text>`;
  // 3.1 Record Request
  F([[128, 90], [330, 90]], "resource request", [216, 90]);
  F([[330, 135], [128, 135]], "request status", [222, 135]);
  F([[550, 110], [720, 110]], "request record", [640, 110], { labelW: 100 });
  F([[440, 160], [440, 290]], "request details", [440, 222]);
  // 3.2 Check Eligibility
  F([[720, 315], [550, 315]], "published listings", [650, 315], { labelW: 100 });
  F([[720, 375], [550, 375]], "request decisions", [650, 375], { labelW: 100 });
  F([[440, 390], [440, 510]], "eligible listings, request criteria", [440, 445], { labelW: 170 });
  // 3.3 Rank and Explain Matches
  F([[550, 528], [720, 528]], "request text", [640, 528], { ai: true, labelW: 100 });
  F([[720, 585], [550, 585]], "embedding vectors", [650, 585], { ai: true, labelW: 100 });
  F([[500, 630], [500, 696], [720, 696]], "match recommendations", [500, 664]);
  F([[330, 570], [128, 570]], "ranked matches", [226, 570]);
  F([[420, 630], [420, 750]], "ranked list", [420, 703]);
  // 3.4 Record Choice and Hold
  F([[128, 780], [330, 780]], "match choice", [214, 780]);
  F([[550, 800], [650, 800], [650, 716], [720, 716]], "match response", [650, 758], { labelW: 100 });
  F([[550, 850], [912, 850], [912, 175], [860, 175], [860, 135]], "hold record", [750, 850]);
  F([[330, 840], [128, 840]], "request status", [226, 840]);
  // boxes
  g.add(external("Requester", 12, 66, 110, 800));
  g.add(store("D3", D.D3, 720, 85, 170, 50, { size: 14 }));
  g.add(store("D2", D.D2, 720, 290, 170, 50, { size: 14 }));
  g.add(store("D5", D.D5, 720, 350, 170, 50, { size: 14 }));
  g.add(external(AI, 720, 500, 170, 100));
  g.add(store("D4", D.D4, 720, 676, 170, 50, { size: 14 }));
  g.add(processBox("3.1", "Record Request", 330, 60, 220, 100));
  g.add(processBox("3.2", "Check Eligibility", 330, 290, 220, 100));
  g.add(processBox("3.3", "Rank and Explain Matches", 330, 510, 220, 120));
  g.add(processBox("3.4", "Record Choice and Hold", 330, 750, 220, 120));
  g.write("dfd-level2-3.svg", 930, 920);
}
