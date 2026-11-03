// Turns the hand-written draw.io files in docs/phase45/images into SVG files that render-svg.ps1 can render.
// It covers the parts those files use: rectangles, cubes, ellipses, diamonds, text and straight-line edges.
// Usage from the repository root: node docs/phase45/diagrams/drawio-svg.js docs/phase45/images/figure-11-3-ai-workflow.drawio
const fs = require("fs");

const unescape = (s) => s.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&amp;/g, "&");
const attr = (s, name) => { const m = s.match(new RegExp(`\\b${name}="([^"]*)"`)); return m ? m[1] : undefined; };
const num = (s, name) => Number(attr(s, name) || 0);

function parseStyle(s) {
  const st = {};
  for (const part of (s || "").split(";")) {
    if (!part) continue;
    const i = part.indexOf("=");
    if (i < 0) st[part] = true; else st[part.slice(0, i)] = part.slice(i + 1);
  }
  return st;
}

function readCells(xml) {
  const cells = [];
  for (const m of xml.matchAll(/<mxCell([^>]*?)(\/>|>([\s\S]*?)<\/mxCell>)/g)) {
    const a = m[1], inner = m[3] || "";
    const cell = { id: attr(a, "id"), value: unescape(attr(a, "value") || ""), style: parseStyle(attr(a, "style")), edge: /\bedge="1"/.test(a), vertex: /\bvertex="1"/.test(a) };
    const g = inner.match(/<mxGeometry([^>]*)/);
    if (g) cell.geo = { x: num(g[1], "x"), y: num(g[1], "y"), w: num(g[1], "width"), h: num(g[1], "height") };
    const pt = (as) => { const p = inner.match(new RegExp(`<mxPoint([^>]*)as="${as}"`)); return p ? { x: num(p[1], "x"), y: num(p[1], "y") } : null; };
    cell.source = pt("sourcePoint");
    cell.target = pt("targetPoint");
    const arr = inner.match(/<Array as="points">([\s\S]*?)<\/Array>/);
    cell.points = arr ? [...arr[1].matchAll(/<mxPoint([^>]*)\/>/g)].map((p) => ({ x: num(p[1], "x"), y: num(p[1], "y") })) : [];
    cells.push(cell);
  }
  return cells;
}

const color = (c, fallback) => (c === undefined ? fallback : c === "none" ? "none" : c);

function edgeSvg(c) {
  const st = c.style, sw = Number(st.strokeWidth || 1), stroke = color(st.strokeColor, "#000");
  const pts = [c.source, ...c.points, c.target];
  const dash = st.dashed === "1" ? ` stroke-dasharray="${(st.dashPattern || "3 3").split(" ").map((d) => d * sw).join(" ")}"` : "";
  let s = `<polyline points="${pts.map((p) => `${p.x},${p.y}`).join(" ")}" fill="none" stroke="${stroke}" stroke-width="${sw}"${dash}/>`;
  // "open" is a V-shaped head; "block" and "classic" are filled triangles
  const head = (kind, a, b) => {
    if (!kind || kind === "none") return "";
    const len = Math.hypot(b.x - a.x, b.y - a.y), ux = (b.x - a.x) / len, uy = (b.y - a.y) / len;
    const L = 12, W = 6, bx = b.x - ux * L, by = b.y - uy * L;
    const p = `${bx - uy * W},${by + ux * W} ${b.x},${b.y} ${bx + uy * W},${by - ux * W}`;
    return kind === "open" ? `<polyline points="${p}" fill="none" stroke="${stroke}" stroke-width="${sw}"/>` : `<polygon points="${p}" fill="${stroke}" stroke="${stroke}" stroke-width="1"/>`;
  };
  s += head(st.endArrow, pts[pts.length - 2], pts[pts.length - 1]);
  s += head(st.startArrow, pts[1], pts[0]);
  return s;
}

// A cube keeps its front face where the box was drawn before; the depth sits above and to the left,
// the way draw.io draws its cube shape.
function cubeFront(c) {
  const s = Number(c.style.size || 16), g = c.geo;
  return { x: g.x + s, y: g.y + s, w: g.w - s, h: g.h - s };
}
function cubeDepthSvg(c) {
  const s = Number(c.style.size || 16), g = c.geo, st = c.style;
  const fill = color(st.fillColor, "#fff"), stroke = color(st.strokeColor, "#000"), sw = Number(st.strokeWidth || 1);
  const top = `${g.x},${g.y} ${g.x + g.w - s},${g.y} ${g.x + g.w},${g.y + s} ${g.x + s},${g.y + s}`;
  const left = `${g.x},${g.y} ${g.x + s},${g.y + s} ${g.x + s},${g.y + g.h} ${g.x},${g.y + g.h - s}`;
  return [top, left].map((p, i) => `<polygon points="${p}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" stroke-linejoin="round"/><polygon points="${p}" fill="#000" fill-opacity="${i ? 0.1 : 0.05}" stroke="none"/>`).join("");
}

function vertexSvg(c) {
  const st = c.style, box = st.shape === "cube" ? cubeFront(c) : c.geo;
  const { x, y, w, h } = box;
  const sw = Number(st.strokeWidth || 1);
  const fill = color(st.fillColor, st.text ? "none" : "#fff"), stroke = color(st.strokeColor, st.text ? "none" : "#000");
  let s = "";
  if (st.ellipse) s += `<ellipse cx="${x + w / 2}" cy="${y + h / 2}" rx="${w / 2}" ry="${h / 2}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
  else if (st.rhombus) s += `<polygon points="${x + w / 2},${y} ${x + w},${y + h / 2} ${x + w / 2},${y + h} ${x},${y + h / 2}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
  else if (st.shape === "note") {
    // UML note: a rectangle with a folded top-right corner
    const k = Number(st.size || 14);
    s += `<path d="M${x} ${y} H${x + w - k} L${x + w} ${y + k} V${y + h} H${x} Z" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/><path d="M${x + w - k} ${y} V${y + k} H${x + w}" fill="none" stroke="${stroke}" stroke-width="${sw}"/>`;
  }
  else if (fill !== "none" || stroke !== "none") {
    const r = st.rounded === "1" ? Math.min(w, h) * Number(st.arcSize || 10) / 100 : 0;
    s += `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"/>`;
  }
  if (c.value.replace(/<[^>]+>/g, "").trim()) {
    const pad = Number(st.spacing || 2);
    const justify = { left: "flex-start", right: "flex-end" }[st.align] || "center";
    const items = { top: "flex-start", bottom: "flex-end" }[st.verticalAlign] || "center";
    const css = `display:flex;width:100%;height:100%;box-sizing:border-box;padding:${pad}px;justify-content:${justify};align-items:${items};text-align:${st.align || "center"};font-family:${st.fontFamily || "Arial"},Helvetica,sans-serif;font-size:${st.fontSize || 11}px;color:${st.fontColor || "#000"};font-weight:${(Number(st.fontStyle) & 1) ? "bold" : "normal"};line-height:1.2`;
    const html = c.value.replace(/<br\s*>/g, "<br/>");
    s += `<foreignObject x="${x}" y="${y}" width="${w}" height="${h}"><div xmlns="http://www.w3.org/1999/xhtml" style="${css}"><div>${html}</div></div></foreignObject>`;
  }
  return s;
}

const file = process.argv[2];
const xml = fs.readFileSync(file, "utf8");
const W = Number(attr(xml, "pageWidth")), H = Number(attr(xml, "pageHeight"));
const cells = readCells(xml).filter((c) => c.edge || (c.vertex && c.geo));
const depth = cells.filter((c) => c.vertex && c.style.shape === "cube").map(cubeDepthSvg).join("\n");
const body = cells.map((c) => (c.edge ? edgeSvg(c) : vertexSvg(c))).join("\n");
const out = file.replace(/\.drawio$/, ".svg");
fs.writeFileSync(out, `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">\n<rect width="100%" height="100%" fill="#fff"/>\n${depth}\n${body}\n</svg>\n`);
console.log("wrote " + out);
