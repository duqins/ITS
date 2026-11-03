// Turns one of the earlier SVG diagrams of sections 1, 2, 8 and 10 into an editable draw.io file next to it
// (same name, .drawio). Every box, line, label, arrowhead, diamond
// and circle becomes its own draw.io shape, so the diagram can be opened and changed in draw.io.
// drawio-svg.js draws the .drawio file back into the same picture.
// Usage from the repository root: node docs/phase45/diagrams/svg2drawio.js docs/phase45/images/erd-full.svg [more.svg ...]
const fs = require("fs");

// a text label is stored as a box whose top sits ASC font sizes above the baseline
const ASC = 0.95, LINE = 1.25;
const attrs = (s) => Object.fromEntries([...s.matchAll(/([\w:-]+)="([^"]*)"/g)].map((m) => [m[1], m[2]]));
const xml = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
const unent = (s) => s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&amp;/g, "&");
const html = (s) => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const num = (v) => Number(v);
const r4 = (v) => Math.round(v * 1e4) / 1e4;
const style = (o) => Object.entries(o).filter(([, v]) => v !== undefined && v !== null).map(([k, v]) => (v === true ? k : `${k}=${v}`)).join(";") + ";";

function pathPoints(d) {
  const t = d.match(/[MLHVQZ]|-?[\d.]+(?:e-?\d+)?/gi);
  const pts = [], cmds = new Set();
  let i = 0, x = 0, y = 0, closed = false;
  while (i < t.length) {
    const c = t[i++].toUpperCase();
    cmds.add(c);
    if (c === "M" || c === "L") { x = num(t[i++]); y = num(t[i++]); pts.push([x, y]); }
    else if (c === "H") { x = num(t[i++]); pts.push([x, y]); }
    else if (c === "V") { y = num(t[i++]); pts.push([x, y]); }
    else if (c === "Q") { const cx = num(t[i++]), cy = num(t[i++]); x = num(t[i++]); y = num(t[i++]); pts.push([cx, cy], [x, y]); }
    else if (c === "Z") closed = true;
  }
  return { pts, cmds, closed };
}
const near = (a, b) => Math.abs(a - b) < 0.02;
const box = (pts) => {
  const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
  const x = Math.min(...xs), y = Math.min(...ys);
  return { x, y, w: Math.max(...xs) - x, h: Math.max(...ys) - y };
};
// direction of an axis-aligned triangle, named by where its tip points (draw.io "triangle" shape)
function triangleDirection(pts) {
  const b = box(pts), mx = b.x + b.w / 2, my = b.y + b.h / 2;
  const has = (x, y) => pts.some((p) => near(p[0], x) && near(p[1], y));
  if (has(b.x + b.w, my) && has(b.x, b.y) && has(b.x, b.y + b.h)) return "east";
  if (has(b.x, my) && has(b.x + b.w, b.y) && has(b.x + b.w, b.y + b.h)) return "west";
  if (has(mx, b.y) && has(b.x, b.y + b.h) && has(b.x + b.w, b.y + b.h)) return "north";
  if (has(mx, b.y + b.h) && has(b.x, b.y) && has(b.x + b.w, b.y)) return "south";
  return null;
}
const isRhombus = (pts) => {
  const b = box(pts), mx = b.x + b.w / 2, my = b.y + b.h / 2;
  const has = (x, y) => pts.some((p) => near(p[0], x) && near(p[1], y));
  return pts.length === 4 && has(mx, b.y) && has(b.x + b.w, my) && has(mx, b.y + b.h) && has(b.x, my);
};
const stroke = (a) => ({ strokeColor: a.stroke || "none", strokeWidth: a["stroke-width"] });

function convert(file) {
  const src = fs.readFileSync(file, "utf8");
  const { width, height } = attrs(src.match(/<svg\b[^>]*>/)[0]);
  const cells = [];
  let n = 2;
  const vertex = (st, g, value = "") => cells.push(`        <mxCell id="c${n++}" value="${xml(value)}" style="${xml(style(st))}" vertex="1" parent="1">\n          <mxGeometry x="${r4(g.x)}" y="${r4(g.y)}" width="${r4(g.w)}" height="${r4(g.h)}" as="geometry" />\n        </mxCell>`);
  const edge = (st, pts) => {
    const mid = pts.slice(1, -1).map((p) => `              <mxPoint x="${p[0]}" y="${p[1]}" />`).join("\n");
    cells.push(`        <mxCell id="c${n++}" style="${xml(style(st))}" edge="1" parent="1">\n          <mxGeometry relative="1" as="geometry">\n            <mxPoint x="${pts[0][0]}" y="${pts[0][1]}" as="sourcePoint" />\n            <mxPoint x="${pts[pts.length - 1][0]}" y="${pts[pts.length - 1][1]}" as="targetPoint" />` +
      (mid ? `\n            <Array as="points">\n${mid}\n            </Array>` : "") + `\n          </mxGeometry>\n        </mxCell>`);
  };
  const lineStyle = (a) => ({ endArrow: "none", startArrow: "none", html: 1, rounded: 0, ...stroke(a) });
  const els = [...src.matchAll(/<(rect|polyline|line|path|circle)\b([^>]*?)\/>|<text\b([^>]*)>([\s\S]*?)<\/text>/g)];
  const used = new Set();
  els.forEach((m, i) => {
    if (used.has(i)) return;
    if (m[3] !== undefined) {
      // a label: plain text, or text with bold parts in <tspan font-weight="700">
      const a = attrs(m[3]), fs2 = num(a["font-size"]);
      const runs = m[4].replace(/<tspan\b([^>]*)>([\s\S]*?)<\/tspan>/g, (all, ta, inner) => (/font-weight="(700|bold)"/.test(ta) ? `<b>${html(unent(inner))}</b>` : html(unent(inner))));
      const plain = unent(m[4].replace(/<[^>]+>/g, ""));
      const w = Math.max(8, plain.length * fs2 * 0.58), h = fs2 * LINE;
      const anchor = a["text-anchor"] || "start";
      let bx = anchor === "middle" ? num(a.x) - w / 2 : anchor === "end" ? num(a.x) - w : num(a.x);
      let by = num(a.y) - ASC * fs2;
      let rotation;
      const rot = (a.transform || "").match(/rotate\(\s*(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s*\)/);
      if (rot) {
        // draw.io turns a shape around its centre; move the box so the turned text lands where it was
        rotation = num(rot[1]);
        const th = (rotation * Math.PI) / 180, k = (0.5 * LINE - ASC) * fs2; // the box centre is k below the baseline (k is negative)
        const cx = num(a.x) + (anchor === "middle" ? 0 : anchor === "end" ? -w / 2 : w / 2), cy = num(a.y);
        // the box centre sits at (cx, baseline + k); solve for the shift that keeps the turned text in place
        const e = [num(rot[2]) - cx, num(rot[3]) - (cy + k)];
        const R = [[Math.cos(th), -Math.sin(th)], [Math.sin(th), Math.cos(th)]];
        // shift d = (I - R)(p - c) where p is the turning point and c the box centre before the shift
        const d = [e[0] - (R[0][0] * e[0] + R[0][1] * e[1]), e[1] - (R[1][0] * e[0] + R[1][1] * e[1])];
        bx += d[0]; by += d[1];
      }
      const bold = /font-weight="(700|bold)"/.test(m[3]) ? 1 : 0, italic = a["font-style"] === "italic" ? 2 : 0;
      // no whiteSpace=wrap: drawio-svg.js draws such a label as one line of SVG text on its baseline
      vertex({ text: true, html: 1, strokeColor: "none", fillColor: "none", align: anchor === "middle" ? "center" : anchor === "end" ? "right" : "left", verticalAlign: "middle",
        spacing: 0, fontFamily: (a["font-family"] || "Arial").split(",")[0].trim(), fontSize: fs2, fontColor: a.fill || "#000000",
        fontStyle: bold + italic || undefined, rotation }, { x: bx, y: by, w, h }, runs);
      return;
    }
    const tag = m[1], a = attrs(m[2]);
    if (tag === "rect") {
      if (a.width === "100%") return; // page background; drawio-svg.js paints it
      const st = { rounded: a.rx ? 1 : 0, absoluteArcSize: a.rx ? 1 : undefined, arcSize: a.rx ? 2 * num(a.rx) : undefined, whiteSpace: "wrap", html: 1,
        fillColor: a.fill || "#000000", ...stroke(a), opacity: a.opacity ? Math.round(num(a.opacity) * 100) : undefined };
      if (a["stroke-dasharray"]) Object.assign(st, { dashed: 1, dashPattern: a["stroke-dasharray"].split(/[ ,]+/).map((v) => num(v) / num(a["stroke-width"] || 1)).join(" ") });
      // a DFD process box: the rounded box plus its blue number band become one swimlane shape
      const next = els[i + 1];
      if (next && next[1] === "path" && /Q/.test(attrs(next[2]).d)) {
        const band = pathPoints(attrs(next[2]).d), bb = box(band.pts);
        if (near(bb.x, num(a.x)) && near(bb.y, num(a.y)) && near(bb.w, num(a.width))) {
          const ba = attrs(next[2]);
          vertex({ swimlane: true, startSize: bb.h, rounded: 1, absoluteArcSize: 1, arcSize: 2 * num(a.rx || 10), html: 1, fillColor: ba.fill, swimlaneFillColor: a.fill, ...stroke(a), horizontal: 1, collapsible: 0 },
            { x: num(a.x), y: num(a.y), w: num(a.width), h: num(a.height) });
          used.add(i + 1);
          return;
        }
      }
      vertex(st, { x: num(a.x), y: num(a.y), w: num(a.width), h: num(a.height) });
    } else if (tag === "polyline") {
      edge(lineStyle(a), a.points.trim().split(/\s+/).map((p) => p.split(",").map(num)));
    } else if (tag === "line") {
      edge(lineStyle(a), [[num(a.x1), num(a.y1)], [num(a.x2), num(a.y2)]]);
    } else if (tag === "circle") {
      const r = num(a.r);
      vertex({ ellipse: true, html: 1, fillColor: a.fill || "#000000", ...stroke(a) }, { x: num(a.cx) - r, y: num(a.cy) - r, w: 2 * r, h: 2 * r });
    } else if (tag === "path") {
      const p = pathPoints(a.d);
      if (!p.closed) { edge(lineStyle(a), p.pts); return; }
      const pts = p.pts.slice(0, p.pts.length - (near(p.pts[0][0], p.pts.at(-1)[0]) && near(p.pts[0][1], p.pts.at(-1)[1]) ? 1 : 0));
      const b = box(pts), base = { html: 1, fillColor: a.fill || "#000000", ...stroke(a) };
      if (pts.length === 3) {
        const dir = triangleDirection(pts);
        if (!dir) throw new Error(`${file}: a triangle that is not axis-aligned: ${a.d}`);
        vertex({ triangle: true, direction: dir === "east" ? undefined : dir, ...base }, b);
      } else if (isRhombus(pts)) vertex({ rhombus: true, ...base }, b);
      else throw new Error(`${file}: a closed shape that is not a triangle or diamond: ${a.d}`);
    }
  });
  const name = file.replace(/^.*[\\/]/, "").replace(/\.svg$/, "");
  const out = `<mxfile host="app.diagrams.net" type="device">\n  <diagram id="${name}" name="${name}">\n    <mxGraphModel dx="${width}" dy="${height}" grid="0" gridSize="10" page="1" pageScale="1" pageWidth="${width}" pageHeight="${height}" background="#ffffff">\n      <root>\n        <mxCell id="0" />\n        <mxCell id="1" parent="0" />\n${cells.join("\n")}\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n`;
  fs.writeFileSync(file.replace(/\.svg$/, ".drawio"), out);
  console.log(`wrote ${name}.drawio (${cells.length} shapes)`);
}

for (const f of process.argv.slice(2)) convert(f);
