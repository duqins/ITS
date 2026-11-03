// Draws the section 8 ER diagram (Figure 8.1) as one SVG file, erd-full.svg.
// Usage from the repository root: node docs/phase45/diagrams/er-diagrams.js docs/phase45/images
// Every entity appears once and every relationship of Table 8.1 is drawn once, in the same order.
// Each box shows the primary key, all foreign keys and a few main attributes. Table 8.2 lists every attribute.
const fs = require("fs");
const path = require("path");

const W = 2800, H = 1645;
const FONT = "Segoe UI, Arial, sans-serif";
const TITLE = 21, TEXT = 19, HEAD = 38, ROW = 26, PADB = 9;
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

// ---------- entities: name, left, top, width, rows ----------
const ENT = [
  ["AiSuggestion", 30, 100, 210, ["PK suggestionId", "FK modelVersionId", "FK assetId", "task", "suggestion", "confidence"]],
  ["ModelVersion", 330, 100, 200, ["PK modelVersionId", "task", "modelName", "version"]],
  ["MatchRecommendation", 640, 100, 265, ["PK matchId", "FK assetId", "FK requestId", "FK modelVersionId", "score", "confidence", "explanation"]],
  ["Category", 990, 100, 225, ["PK categoryId", "name", "unit", "emissionFactorLow", "emissionFactorHigh"]],
  ["ResourceRequest", 1700, 100, 230, ["PK requestId", "FK requesterId", "FK categoryId", "quantity", "requiredBy", "status"]],
  ["Reservation", 2010, 100, 200, ["PK reservationId", "FK requestId", "FK listingId", "quantity", "expiresAt", "status"]],
  ["Listing", 2300, 100, 160, ["PK listingId", "FK assetId", "quantity", "availableFrom", "status"]],
  ["Approval", 2570, 100, 220, ["PK approvalId", "FK approverId", "FK requestId", "FK listingId", "FK transferId", "FK maintenanceId", "FK endOfLifeId", "stage", "decision", "status"]],
  ["Asset", 330, 680, 250, ["PK assetId", "FK ownerDepartmentId", "FK categoryId", "FK custodianId", "name", "condition", "status", "location (composite)", "assetAge (derived)"]],
  ["AuditLog", 690, 560, 200, ["PK auditId", "FK userId", "action", "recordType", "createdAt"]],
  ["Role", 990, 650, 170, ["PK roleId", "name"]],
  ["UserRole", 1300, 580, 200, ["PK userRoleId", "FK userId", "FK roleId", "FK departmentId", "status"]],
  ["User", 1700, 440, 230, ["PK userId", "FK departmentId", "name", "email"]],
  ["Notification", 2000, 620, 200, ["PK notificationId", "FK userId", "message", "sentAt", "readAt"]],
  ["Department", 1700, 800, 230, ["PK departmentId", "name", "code"]],
  ["Transfer", 2280, 660, 250, ["PK transferId", "FK assetId", "FK requestId", "FK reservationId", "FK approverId", "FK fromDepartmentId", "FK toDepartmentId", "FK toCustodianId", "quantity", "status"]],
  ["Inspection", 790, 1040, 220, ["PK inspectionId", "FK assetId", "FK inspectorId", "inspectedOn", "conditionFound", "safeToUse"]],
  ["Attachment", 1240, 1030, 210, ["PK attachmentId", "FK assetId", "FK transferId", "FK inspectionId", "FK maintenanceId", "FK endOfLifeId", "fileName", "fileType"]],
  ["MaintenanceRecord", 1230, 1350, 230, ["PK maintenanceId", "FK assetId", "FK inspectionId", "estimatedCost", "actualCost", "status"]],
  ["SustainabilityImpact", 1700, 1350, 230, ["PK impactId", "FK transferId", "FK maintenanceId", "FK endOfLifeId", "wasteDivertedKg", "co2eLowKg", "co2eHighKg"]],
  ["EndOfLifeAction", 2300, 1350, 210, ["PK endOfLifeId", "FK assetId", "action", "quantity", "status"]],
];
const B = {};
for (const [name, x, y, w, rows] of ENT) B[name] = { name, x, y, w, h: HEAD + rows.length * ROW + PADB, rows };

// ---------- relationships, in the order of Table 8.1 ----------
// [first entity, name, cardinality at the first entity, cardinality at the second entity, second entity, route]
// route: a/b = [side, place] for each end (place is a fraction of the side, or an absolute x or y),
// via = coordinates of the corners in between (the line turns at each one), n = [segment, side, along] for the name,
// ma/mb = side of the multiplicity at each end (a/b above or below a horizontal line, l/r beside a vertical one).
const REL = [
  ["Department", "employs", "1", "0..*", "User", { a: ["top", 1815], b: ["bottom", 1815], n: [0, "r", 0.3], ma: "r", mb: "r" }],
  ["Department", "owns", "1", "0..*", "Asset", { a: ["left", 890], b: ["right", 890], n: [0, "a", 0.5], ma: "a", mb: "a" }],
  ["Department", "scopes", "1", "0..*", "UserRole", { a: ["left", 830], b: ["bottom", 1420], n: [0, "b", 0.5], ma: "a", mb: "r" }],
  ["User", "holds", "1", "0..*", "UserRole", { a: ["bottom", 1730], b: ["right", 680], n: [1, "b", 0.5], ma: "r", mb: "a" }],
  ["Role", "used in", "1", "0..*", "UserRole", { a: ["right", 700], b: ["left", 700], n: [0, "b", 0.5], ma: "a", mb: "a" }],
  ["User", "submits", "1", "0..*", "ResourceRequest", { a: ["top", 1815], b: ["bottom", 1815], n: [0, "r", 0.5], ma: "r", mb: "r" }],
  ["User", "is custodian of", "1", "0..*", "Asset", { a: ["left", 465], b: ["right", 730], via: [640], n: [0, "a", 0.5], ma: "a", mb: "a" }],
  ["User", "gives final approval", "0..1", "0..*", "Transfer", { a: ["right", 495], b: ["top", 2345], n: [0, "a", 0.5], ma: "a", mb: "r" }],
  ["User", "decides", "0..1", "0..*", "Approval", { a: ["right", 455], b: ["bottom", 2598], n: [0, "a", 0.5], ma: "a", mb: "r" }],
  ["User", "receives", "1", "0..*", "Notification", { a: ["bottom", 1905], b: ["left", 690], n: [0, "r", 0.5], ma: "r", mb: "a" }],
  ["User", "performs", "0..1", "0..*", "AuditLog", { a: ["left", 505], b: ["top", 850], n: [0, "a", 0.6], ma: "a", mb: "r" }],
  ["Category", "classifies", "1", "0..*", "Asset", { a: ["bottom", 1020], b: ["top", 530], via: [410], n: [1, "a", 0.5], ma: "r", mb: "r" }],
  ["Category", "classifies", "1", "0..*", "ResourceRequest", { a: ["right", 190], b: ["left", 190], n: [0, "b", 0.5], ma: "a", mb: "a" }],
  ["Asset", "is offered in", "1", "0..*", "Listing", { a: ["left", 900], b: ["top", 2410], via: [12, 25], n: [2, "b", 0.12], ma: "a", mb: "r" }],
  ["Listing", "is held by", "1", "0..*", "Reservation", { a: ["left", 190], b: ["right", 190], n: [0, "b", 0.5], ma: "a", mb: "a" }],
  ["ResourceRequest", "places", "1", "0..*", "Reservation", { a: ["right", 190], b: ["left", 190], n: [0, "b", 0.5], ma: "a", mb: "a" }],
  ["Reservation", "becomes", "1", "0..1", "Transfer", { a: ["bottom", 2200], b: ["top", 2480], via: [340], n: [2, "rr", 0.5], ma: "r", mb: "r" }],
  ["Asset", "is matched in", "1", "0..*", "MatchRecommendation", { a: ["top", 450], b: ["bottom", 690], via: [370], n: [1, "a", 0.5], ma: "r", mb: "r" }],
  ["ResourceRequest", "receives", "1", "0..*", "MatchRecommendation", { a: ["top", 1750], b: ["top", 760], via: [60], n: [1, "a", 0.5], ma: "r", mb: "r" }],
  ["ModelVersion", "produces", "1", "0..*", "MatchRecommendation", { a: ["right", 180], b: ["left", 180], n: [0, "b", 0.5], ma: "a", mb: "a" }],
  ["Asset", "is moved by", "1", "0..*", "Transfer", { a: ["right", 945], b: ["left", 945], n: [0, "b", 0.5], ma: "a", mb: "a" }],
  ["ResourceRequest", "is fulfilled by", "1", "0..*", "Transfer", { a: ["bottom", 1900], b: ["top", 2420], via: [370], n: [1, "a", 0.3], ma: "r", mb: "r" }],
  ["ResourceRequest", "needs", "0..1", "0..*", "Approval", { a: ["top", 1880], b: ["top", 2620], via: [60], n: [1, "a", 0.3], ma: "r", mb: "r" }],
  ["Listing", "needs", "0..1", "0..*", "Approval", { a: ["right", 190], b: ["left", 190], n: [0, "b", 0.5], ma: "a", mb: "a" }],
  ["Transfer", "needs", "0..1", "0..*", "Approval", { a: ["right", 720], b: ["bottom", 2652], n: [0, "b", 0.5], ma: "a", mb: "r" }],
  ["MaintenanceRecord", "needs", "0..1", "0..*", "Approval", { a: ["bottom", 1300], b: ["bottom", 2760], via: [1630], n: [2, "rl", 0.5], ma: "r", mb: "r" }],
  ["EndOfLifeAction", "needs", "0..1", "0..*", "Approval", { a: ["right", 1430], b: ["bottom", 2706], n: [0, "b", 0.5], ma: "a", mb: "r" }],
  ["Asset", "checks", "1", "0..*", "Inspection", { a: ["bottom", 470], b: ["left", 1140], n: [1, "a", 0.5], ma: "r", mb: "a" }],
  ["Asset", "has", "1", "0..*", "MaintenanceRecord", { a: ["bottom", 410], b: ["left", 1450], n: [1, "a", 0.3], ma: "r", mb: "a" }],
  ["Inspection", "leads to", "0..1", "0..*", "MaintenanceRecord", { a: ["bottom", 900], b: ["left", 1400], n: [1, "a", 0.5], ma: "r", mb: "a" }],
  ["Asset", "ends with", "1", "0..*", "EndOfLifeAction", { a: ["bottom", 350], b: ["bottom", 2400], via: [1605], n: [1, "a", 0.25], ma: "r", mb: "r" }],
  ["Transfer", "creates", "0..1", "0..1", "SustainabilityImpact", { a: ["bottom", 2350], b: ["top", 1850], via: [1025], n: [2, "r", 0.4], ma: "r", mb: "r" }],
  ["MaintenanceRecord", "creates", "0..1", "0..1", "SustainabilityImpact", { a: ["right", 1450], b: ["left", 1450], n: [0, "b", 0.5], ma: "a", mb: "a" }],
  ["EndOfLifeAction", "creates", "0..1", "0..1", "SustainabilityImpact", { a: ["left", 1440], b: ["right", 1440], n: [0, "b", 0.5], ma: "a", mb: "a" }],
  ["Department", "releases", "1", "0..*", "Transfer", { a: ["right", 845], b: ["left", 845], n: [0, "a", 0.5], ma: "a", mb: "a" }],
  ["Department", "receives", "1", "0..*", "Transfer", { a: ["right", 895], b: ["left", 895], n: [0, "b", 0.5], ma: "a", mb: "a" }],
  ["User", "receives as custodian", "1", "0..*", "Transfer", { a: ["right", 535], b: ["top", 2300], n: [0, "a", 0.5], ma: "a", mb: "r" }],
  ["User", "inspects", "1", "0..*", "Inspection", { a: ["left", 545], b: ["top", 950], n: [0, "a", 0.45], ma: "a", mb: "r" }],
  ["ModelVersion", "produces", "1", "0..*", "AiSuggestion", { a: ["left", 180], b: ["right", 180], n: [0, "b", 0.5], ma: "a", mb: "a" }],
  ["Asset", "gets", "0..1", "0..*", "AiSuggestion", { a: ["left", 720], b: ["bottom", 135], n: [1, "r", 0.5], ma: "a", mb: "r" }],
  ["Asset", "has", "0..1", "0..*", "Attachment", { a: ["bottom", 540], b: ["top", 1300], via: [995], n: [1, "b", 0.25], ma: "r", mb: "l" }],
  ["Transfer", "has", "0..1", "0..*", "Attachment", { a: ["bottom", 2300], b: ["top", 1400], via: [1000], n: [1, "a", 0.3], ma: "l", mb: "r" }],
  ["Inspection", "has", "0..1", "0..*", "Attachment", { a: ["right", 1140], b: ["left", 1140], n: [0, "b", 0.5], ma: "a", mb: "a" }],
  ["MaintenanceRecord", "has", "0..1", "0..*", "Attachment", { a: ["top", 1345], b: ["bottom", 1345], n: [0, "l", 0.5], ma: "r", mb: "r" }],
  ["EndOfLifeAction", "has", "0..1", "0..*", "Attachment", { a: ["top", 2350], b: ["right", 1250], n: [1, "a", 0.3], ma: "r", mb: "a" }],
];

// ---------- drawing ----------
function anchor(b, [side, f]) {
  const along = (start, len) => (f > 1 ? f : start + len * f);
  if (side === "top") return { x: along(b.x, b.w), y: b.y };
  if (side === "bottom") return { x: along(b.x, b.w), y: b.y + b.h };
  if (side === "left") return { x: b.x, y: along(b.y, b.h) };
  return { x: b.x + b.w, y: along(b.y, b.h) };
}
const horiz = (s) => s === "left" || s === "right";

// orthogonal line: it leaves the first box straight out of its side, turns at each via coordinate
// (moves alternate between horizontal and vertical) and makes one last turn, if needed, to reach the second end
function points(r) {
  const p1 = anchor(B[r.from], r.a), p2 = anchor(B[r.to], r.b);
  const pts = [p1];
  let cur = p1, h = horiz(r.a[0]);
  for (const v of r.via || []) { cur = h ? { x: v, y: cur.y } : { x: cur.x, y: v }; pts.push(cur); h = !h; }
  pts.push(h ? { x: p2.x, y: cur.y } : { x: cur.x, y: p2.y }, p2);
  return pts.filter((p, i) => i === 0 || p.x !== pts[i - 1].x || p.y !== pts[i - 1].y);
}

const text = (x, y, s, extra) => `<text x="${x}" y="${y}" font-family="${FONT}" ${extra}>${esc(s)}</text>`;

// multiplicity beside the end of a line: a/b = above/below a horizontal line, l/r = left/right of a vertical line
function mult(p, side, s, pos) {
  const st = `font-size="${TEXT}" font-weight="700" fill="#1F3864"`;
  if (side === "top" || side === "bottom") {
    const y = side === "top" ? p.y - 8 : p.y + 22;
    return pos === "l" ? text(p.x - 7, y, s, `text-anchor="end" ${st}`) : text(p.x + 7, y, s, st);
  }
  const y = pos === "b" ? p.y + 21 : p.y - 7;
  return side === "left" ? text(p.x - 7, y, s, `text-anchor="end" ${st}`) : text(p.x + 7, y, s, st);
}

// relationship name beside one segment: a/b for horizontal segments, l/r (or rl/rr rotated) for vertical ones
function relName(pts, s, [seg, pos, t]) {
  const q1 = pts[seg], q2 = pts[seg + 1];
  const st = `font-size="${TEXT}" font-style="italic" fill="#444"`;
  const x = q1.x + (q2.x - q1.x) * t, y = q1.y + (q2.y - q1.y) * t;
  if (q1.y === q2.y) return text(x, pos === "b" ? y + 22 : y - 8, s, `text-anchor="middle" ${st}`);
  if (pos === "rl" || pos === "rr") {
    const xx = pos === "rl" ? x - 8 : x + 21;
    return text(xx, y, s, `text-anchor="middle" transform="rotate(-90 ${xx} ${y})" ${st}`);
  }
  return pos === "l" ? text(x - 8, y + 7, s, `text-anchor="end" ${st}`) : text(x + 8, y + 7, s, st);
}

function drawRel(r) {
  const pts = points(r);
  let s = `<g class="rel"><polyline points="${pts.map((p) => `${p.x},${p.y}`).join(" ")}" fill="none" stroke="#333" stroke-width="2"/>`;
  s += mult(pts[0], r.a[0], r.ca, r.ma) + mult(pts[pts.length - 1], r.b[0], r.cb, r.mb);
  s += relName(pts, r.name, r.n) + "</g>";
  return s;
}

function drawBox(b) {
  let s = `<g class="entity"><rect x="${b.x}" y="${b.y}" width="${b.w}" height="${b.h}" rx="3" fill="#fff" stroke="#333" stroke-width="2"/>`;
  s += `<rect x="${b.x}" y="${b.y}" width="${b.w}" height="${HEAD}" rx="3" fill="#e3ecf7" stroke="#333" stroke-width="2"/>`;
  s += text(b.x + b.w / 2, b.y + 26, b.name, `text-anchor="middle" font-size="${TITLE}" font-weight="700" fill="#111"`);
  b.rows.forEach((row, i) => {
    const y = b.y + HEAD + 19 + i * ROW, m = row.match(/^(PK|FK) (.*)$/);
    s += m
      ? `<text x="${b.x + 11}" y="${y}" font-family="${FONT}" font-size="${TEXT}" fill="#111"><tspan font-weight="700">${m[1]}</tspan> ${esc(m[2])}</text>`
      : text(b.x + 11, y, row, `font-size="${TEXT}" fill="#111"`);
  });
  return s + "</g>";
}

const outDir = process.argv[2];
const rels = REL.map(([from, name, ca, cb, to, route]) => ({ from, name, ca, cb, to, ...route }));
const body = rels.map(drawRel).join("\n") + "\n" + Object.values(B).map(drawBox).join("\n");
fs.writeFileSync(path.join(outDir, "erd-full.svg"), `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">\n<rect width="100%" height="100%" fill="#fff"/>\n${body}\n</svg>\n`);
console.log("wrote erd-full.svg");
