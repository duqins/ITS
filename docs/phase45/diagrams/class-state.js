// Draws the section 10 class diagram and state diagrams as SVG files.
// Usage from the repository root: node docs/phase45/diagrams/class-state.js docs/phase45/images
const fs = require("fs");
const path = require("path");
const outDir = process.argv[2];
const FONT = "Segoe UI, Arial, sans-serif";
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

function write(file, w, h, body) {
  fs.writeFileSync(path.join(outDir, file), `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">\n<rect width="100%" height="100%" fill="#fff"/>\n${body}\n</svg>\n`);
  console.log("wrote " + file);
}

// line helper used by the state diagrams
const poly = (pts, extra = "") => `<polyline points="${pts.map((p) => `${p.x},${p.y}`).join(" ")}" fill="none" stroke="#333" stroke-width="1.6"${extra}/>`;

// ---------- class diagram (Figure 10.1) ----------
// One figure: every class appears once and every relationship of Table 8.1 is drawn,
// plus the composition ResourceRequest-RequestSpecification and the generalization of Asset.
// Printed alone on an A3 landscape page, so 19 px text prints at about 7 pt.
const CW = 2810, CHT = 1650, CF = 19, CN = 23, CR = 25, CH = 38;
// name: [x, y, width, attributes, operations]
const CLASSES = {
  Department: [1360, 680, 190, ["- name: String","- code: String"], ["+ deactivate(): void"]],
  User: [860, 490, 360, ["- name: String","- email: String","- accountStatus: AccountStatus"], ["+ signIn(password: String): bool","+ hasRole(r: Role, d: Department): bool","+ deactivate(): void"]],
  Role: [1480, 160, 270, ["- name: String"], ["+ allows(action: String): bool"]],
  UserRole: [1380, 390, 250, ["- status: RoleStatus"], ["+ authorise(by: User): void","+ apply(by: User): void","+ remove(): void"]],
  Notification: [1090, 220, 190, ["- message: String","- sentAt: DateTime","- readAt: DateTime"], ["+ markRead(): void"]],
  AuditLog: [650, 150, 370, ["- action: String","- recordType: String","- recordId: int","- role: String","- createdAt: DateTime"], ["+ record(actor: User, action: String): void"]],
  Category: [1790, 380, 260, ["- name: String","- unit: String","- emissionFactor: Range"], ["+ isSpecialHandling(): bool"]],
  ModelVersion: [2150, 420, 210, ["- modelName: String","- version: String"], []],
  Listing: [260, 1420, 300, ["- quantity: int","- availableFrom: Date","- status: ListingStatus"], ["+ submitForRelease(): void","+ publish(): void","+ withdraw(reason: String): void"]],
  Asset: [1820, 740, 340, ["- name: String","- condition: Condition","- status: AssetStatus","- quantity: int","- location: Location","- purchaseDate: Date","- /assetAge: int"], ["+ register(): void","+ confirm(by: User): void","+ changeStatus(to: AssetStatus): void","+ reserve(qty: int): void","+ release(qty: int): void"]],
  ITAsset: [2230, 1290, 260, ["- serialNumber: String","- storesData: bool"], ["+ needsDataErasure(): bool"]],
  FurnitureAsset: [2570, 1290, 200, ["- material: String","- dimensions: String"], []],
  AiSuggestion: [2240, 710, 270, ["- task: String","- suggestion: String","- confidence: Decimal","- userResponse: String"], ["+ accept(): void","+ correct(value: String): void","+ reject(reason: String): void"]],
  Attachment: [1400, 1300, 260, ["- fileName: String","- fileType: String","- sizeKB: int"], ["+ openLink(by: User): String"]],
  MatchRecommendation: [2020, 20, 290, ["- score: Decimal","- confidence: Decimal","- explanation: String"], ["+ accept(): void","+ override(reason: String): void","+ summarize(): String"]],
  ResourceRequest: [450, 450, 270, ["- status: RequestStatus","- requiredBy: Date"], ["+ submit(): void","+ approve(by: User): void","+ cancel(reason: String): void","+ expire(): void"]],
  RequestSpecification: [60, 450, 260, ["- specifications: String","- quantity: int","- minCondition: Condition","- urgency: Urgency"], []],
  Reservation: [100, 670, 270, ["- quantity: int","- expiresAt: DateTime","- status: ReservationStatus"], ["+ confirm(by: User): void","+ cancel(reason: String): void","+ expire(): void"]],
  Transfer: [880, 820, 270, ["- quantity: int","- toLocation: Location","- plannedDate: Date","- status: TransferStatus"], ["+ handOver(): void","+ confirmReceipt(): void","+ dispute(note: String): void","+ cancel(reason: String): void"]],
  Approval: [370, 970, 380, ["- stage: String","- decision: Decision","- reason: String","- approverRole: String","- recordVersion: int","- status: ApprovalStatus"], ["+ approve(by: User): void","+ reject(by: User, reason: String): void","+ requestChanges(by: User, r: String): void","+ withdraw(): void"]],
  MaintenanceRecord: [1780, 1380, 310, ["- estimatedCost: Decimal","- actualCost: Decimal","- conditionAfter: Condition","- status: WorkOrderStatus"], ["+ assess(cost: Decimal): void","+ start(): void","+ complete(after: Condition): void"]],
  EndOfLifeAction: [1080, 1160, 240, ["- action: EndOfLifeType","- destination: String","- status: EndOfLifeStatus"], ["+ propose(): void","+ complete(): void"]],
  SustainabilityImpact: [700, 1350, 300, ["- wasteDivertedKg: Decimal","- avoidedPurchaseAED: Decimal","- co2eLowKg: Decimal","- co2eHighKg: Decimal"], ["+ calculate(): void"]],
  Inspection: [1410, 990, 270, ["- inspectedOn: DateTime","- conditionFound: Condition","- safeToUse: bool"], ["+ record(): void"]],
};
// [Table 8.1 row, class 1, name, multiplicity 1, multiplicity 2, class 2, kind, line from class 1 to class 2,
//  multiplicity 1 label, multiplicity 2 label, name label]; a label is [x, y, anchor] with s = start, e = end, m = middle.
// The arrow (or the diamond of an aggregation or composition) sits at class 1, the class the other one refers to.
const ASSOC = [
  [1, "Department", "employs", "1", "0..*", "User", "aggr", [[1390, 680], [1390, 620], [1220, 620]], [1399, 643, "s"], [1228, 641, "s"], [1305, 641, "m"]],
  [2, "Department", "owns", "1", "0..*", "Asset", "aggr", [[1550, 770], [1820, 770]], [1590, 791, "s"], [1812, 791, "e"], [1685, 791, "m"]],
  [3, "Department", "scopes", "1", "0..*", "UserRole", "", [[1460, 680], [1460, 548]], [1469, 667, "s"], [1469, 571, "s"], [1468, 640, "s"]],
  [4, "User", "holds", "1", "0..*", "UserRole", "comp", [[1220, 520], [1380, 520]], [1260, 541, "s"], [1372, 541, "e"], [1300, 541, "m"]],
  [5, "Role", "used in", "1", "0..*", "UserRole", "", [[1600, 268], [1600, 390]], [1609, 291, "s"], [1609, 377, "s"], [1608, 335, "s"]],
  [6, "User", "submits", "1", "0..*", "ResourceRequest", "", [[860, 590], [720, 590]], [834, 611, "e"], [728, 611, "s"], [790, 583, "m"]],
  [7, "User", "is custodian of", "1", "0..*", "Asset", "", [[1220, 570], [1390, 570], [1390, 610], [1850, 610], [1850, 740]], [1246, 591, "s"], [1859, 727, "s"], [1620, 631, "m"]],
  [8, "User", "gives final approval", "0..1", "0..*", "Transfer", "", [[1040, 698], [1040, 820]], [1049, 721, "s"], [1049, 807, "s"], [1048, 747, "s"]],
  [9, "User", "decides", "0..1", "0..*", "Approval", "", [[860, 670], [720, 670], [720, 970]], [834, 691, "e"], [729, 957, "s"], [728, 826, "s"]],
  [10, "User", "receives", "1", "0..*", "Notification", "", [[1120, 490], [1120, 378]], [1129, 477, "s"], [1129, 401, "s"], [1128, 440, "s"]],
  [11, "User", "performs", "0..1", "0..*", "AuditLog", "", [[950, 490], [950, 358]], [959, 477, "s"], [959, 381, "s"], [958, 430, "s"]],
  [12, "Category", "classifies", "1", "0..*", "Asset", "", [[1950, 538], [1950, 740]], [1959, 561, "s"], [1959, 727, "s"], [1958, 645, "s"]],
  [13, "Category", "classifies", "1", "0..*", "ResourceRequest", "", [[1820, 380], [1820, 110], [610, 110], [610, 450]], [1829, 367, "s"], [619, 437, "s"], [1215, 131, "m"]],
  [14, "Asset", "is offered in", "1", "0..*", "Listing", "", [[1990, 1098], [1990, 1340], [2150, 1340], [2150, 1630], [620, 1630], [620, 1600], [560, 1600]], [1999, 1121, "s"], [568, 1621, "s"], [2158, 1491, "s"]],
  [15, "Listing", "is held by", "1", "0..*", "Reservation", "", [[330, 1420], [330, 878]], [339, 1407, "s"], [339, 901, "s"], [322, 1155, "e"]],
  [16, "ResourceRequest", "places", "1", "0..*", "Reservation", "", [[480, 658], [480, 710], [370, 710]], [489, 681, "s"], [378, 731, "s"], [442, 731, "m"]],
  [17, "Reservation", "becomes", "1", "0..1", "Transfer", "", [[370, 850], [880, 850]], [396, 871, "s"], [872, 871, "e"], [625, 871, "m"]],
  [18, "Asset", "is matched in", "1", "0..*", "MatchRecommendation", "", [[2090, 740], [2090, 228]], [2099, 727, "s"], [2099, 251, "s"], [2098, 567, "s"]],
  [19, "ResourceRequest", "receives", "1", "0..*", "MatchRecommendation", "", [[540, 450], [540, 90], [2020, 90]], [549, 437, "s"], [2012, 111, "e"], [532, 276, "e"]],
  [20, "ModelVersion", "produces", "1", "0..*", "MatchRecommendation", "", [[2250, 420], [2250, 228]], [2259, 407, "s"], [2259, 251, "s"], [2258, 330, "s"]],
  [21, "Asset", "is moved by", "1", "0..*", "Transfer", "", [[1820, 920], [1150, 920]], [1794, 941, "e"], [1158, 941, "s"], [1485, 941, "m"]],
  [22, "ResourceRequest", "is fulfilled by", "1", "0..*", "Transfer", "", [[690, 658], [690, 780], [900, 780], [900, 820]], [699, 681, "s"], [909, 807, "s"], [795, 773, "m"]],
  [23, "ResourceRequest", "needs", "0..1", "0..*", "Approval", "", [[580, 658], [580, 970]], [589, 681, "s"], [589, 957, "s"], [588, 820, "s"]],
  [24, "Listing", "needs", "0..1", "0..*", "Approval", "", [[410, 1420], [410, 1278]], [419, 1407, "s"], [419, 1301, "s"], [418, 1355, "s"]],
  [25, "Transfer", "needs", "0..1", "0..*", "Approval", "", [[880, 1050], [750, 1050]], [854, 1071, "e"], [758, 1071, "s"], [815, 1043, "m"]],
  [26, "MaintenanceRecord", "needs", "0..1", "0..*", "Approval", "", [[1780, 1570], [660, 1570], [660, 1278]], [1754, 1591, "e"], [669, 1301, "s"], [1220, 1591, "m"]],
  [27, "EndOfLifeAction", "needs", "0..1", "0..*", "Approval", "", [[1080, 1250], [750, 1250]], [1054, 1271, "e"], [758, 1271, "s"], [915, 1271, "m"]],
  [28, "Asset", "checks", "1", "0..*", "Inspection", "", [[1820, 1020], [1680, 1020]], [1794, 1013, "e"], [1688, 1013, "s"], [1750, 1013, "m"]],
  [29, "Asset", "has", "1", "0..*", "MaintenanceRecord", "", [[1910, 1098], [1910, 1380]], [1919, 1121, "s"], [1919, 1367, "s"], [1918, 1245, "s"]],
  [30, "Inspection", "leads to", "0..1", "0..*", "MaintenanceRecord", "", [[1680, 1120], [1810, 1120], [1810, 1380]], [1706, 1141, "s"], [1819, 1367, "s"], [1818, 1256, "s"]],
  [31, "Asset", "ends with", "1", "0..*", "EndOfLifeAction", "", [[1820, 970], [1270, 970], [1270, 1160]], [1794, 991, "e"], [1279, 1147, "s"], [1278, 1071, "s"]],
  [32, "Transfer", "creates", "0..1", "0..1", "SustainabilityImpact", "", [[970, 1078], [970, 1350]], [979, 1101, "s"], [979, 1337, "s"], [978, 1220, "s"]],
  [33, "MaintenanceRecord", "creates", "0..1", "0..1", "SustainabilityImpact", "", [[1780, 1490], [1000, 1490]], [1754, 1511, "e"], [1008, 1511, "s"], [1390, 1511, "m"]],
  [34, "EndOfLifeAction", "creates", "0..1", "0..1", "SustainabilityImpact", "", [[1110, 1343], [1110, 1400], [1000, 1400]], [1119, 1366, "s"], [1008, 1421, "s"], [1088, 1421, "m"]],
  [35, "Department", "releases", "1", "0..*", "Transfer", "", [[1360, 760], [1120, 760], [1120, 820]], [1334, 781, "e"], [1129, 807, "s"], [1240, 781, "m"]],
  [36, "Department", "receives", "1", "0..*", "Transfer", "", [[1390, 813], [1390, 870], [1150, 870]], [1399, 836, "s"], [1158, 891, "s"], [1234, 891, "m"]],
  [37, "User", "receives as custodian", "1", "0..*", "Transfer", "", [[970, 698], [970, 820]], [979, 721, "s"], [979, 807, "s"], [962, 747, "e"]],
  [38, "User", "inspects", "1", "0..*", "Inspection", "", [[1220, 670], [1290, 670], [1290, 1020], [1410, 1020]], [1246, 691, "s"], [1402, 1041, "e"], [1298, 851, "s"]],
  [39, "ModelVersion", "produces", "1", "0..*", "AiSuggestion", "", [[2270, 518], [2270, 710]], [2279, 541, "s"], [2279, 697, "s"], [2278, 620, "s"]],
  [40, "Asset", "gets", "0..1", "0..*", "AiSuggestion", "", [[2160, 1000], [2270, 1000], [2270, 943]], [2186, 1021, "s"], [2279, 966, "s"], [2248, 1021, "m"]],
  [41, "Asset", "has", "0..1", "0..*", "Attachment", "comp", [[1820, 1070], [1750, 1070], [1750, 1330], [1660, 1330]], [1788, 1063, "e"], [1668, 1351, "s"], [1742, 1206, "e"]],
  [42, "Transfer", "has", "0..1", "0..*", "Attachment", "", [[1150, 1050], [1370, 1050], [1370, 1240], [1430, 1240], [1430, 1300]], [1176, 1071, "s"], [1439, 1287, "s"], [1227, 1071, "m"]],
  [43, "Inspection", "has", "0..1", "0..*", "Attachment", "", [[1530, 1148], [1530, 1300]], [1539, 1171, "s"], [1539, 1287, "s"], [1538, 1230, "s"]],
  [44, "MaintenanceRecord", "has", "0..1", "0..*", "Attachment", "", [[1780, 1430], [1660, 1430]], [1754, 1451, "e"], [1668, 1451, "s"], [1720, 1423, "m"]],
  [45, "EndOfLifeAction", "has", "0..1", "0..*", "Attachment", "", [[1290, 1343], [1290, 1400], [1400, 1400]], [1299, 1366, "s"], [1392, 1421, "e"], [1329, 1421, "m"]],
  ["c1", "ResourceRequest", "owns", "1", "1", "RequestSpecification", "comp", [[450, 550], [320, 550]], [410, 571, "e"], [328, 571, "s"], [366, 571, "m"]],
];
// generalization: one hollow triangle under Asset, joined to both subclasses
const GEN = { x: 2080, joinY: 1220, subs: ["ITAsset", "FurnitureAsset"] };
{
  const box = (n) => { const [x, y, w, a, op] = CLASSES[n]; return { x, y, w, h: CH + a.length * CR + 10 + (op.length ? op.length * CR + 10 : 0), a, op }; };
  const line = (pts) => `<polyline points="${pts.map((p) => p.join(",")).join(" ")}" fill="none" stroke="#333" stroke-width="2"/>`;
  const side = (b, p) => (p[1] === b.y ? [0, -1] : p[1] === b.y + b.h ? [0, 1] : p[0] === b.x ? [-1, 0] : [1, 0]);
  const ANCH = { s: "start", e: "end", m: "middle" };
  const label = (l, text, style) => `<text x="${l[0]}" y="${l[1]}" text-anchor="${ANCH[l[2]]}" font-family="${FONT}" font-size="${CF}" ${style}>${esc(text)}</text>`;
  let lines = "", marks = "", labels = "", boxes = "";
  for (const [row, a, name, ma, mb, b, kind, pts, la, lb, ln] of ASSOC) {
    lines += line(pts);
    const p = pts[0], [dx, dy] = side(box(a), p), px = -dy, py = dx;
    if (kind) {
      // diamond at the whole: hollow for aggregation, filled for composition
      const m = [p[0] + dx * 12, p[1] + dy * 12], e = [p[0] + dx * 24, p[1] + dy * 24];
      marks += `<path d="M${p[0]} ${p[1]} L${m[0] + px * 9} ${m[1] + py * 9} L${e[0]} ${e[1]} L${m[0] - px * 9} ${m[1] - py * 9} Z" fill="${kind === "comp" ? "#333" : "#fff"}" stroke="#333" stroke-width="2"/>`;
    } else {
      // open arrowhead: the association is navigable toward class 1
      const q = [p[0] + dx * 16, p[1] + dy * 16];
      marks += `<polyline points="${q[0] + px * 8},${q[1] + py * 8} ${p[0]},${p[1]} ${q[0] - px * 8},${q[1] - py * 8}" fill="none" stroke="#333" stroke-width="2"/>`;
    }
    labels += label(la, ma, 'font-weight="700" fill="#1F3864"') + label(lb, mb, 'font-weight="700" fill="#1F3864"') + label(ln, name, 'font-style="italic" fill="#444"');
  }
  const A = box("Asset"), base = A.y + A.h;
  marks += `<path d="M${GEN.x} ${base} L${GEN.x - 13} ${base + 20} L${GEN.x + 13} ${base + 20} Z" fill="#fff" stroke="#333" stroke-width="2"/>`;
  lines += line([[GEN.x, base + 20], [GEN.x, GEN.joinY]]);
  for (const s of GEN.subs) { const b = box(s), cx = b.x + b.w / 2; lines += line([[cx, b.y], [cx, GEN.joinY], [GEN.x, GEN.joinY]]); }
  for (const n of Object.keys(CLASSES)) {
    const b = box(n);
    boxes += `<rect x="${b.x}" y="${b.y}" width="${b.w}" height="${b.h}" fill="#fff" stroke="#333" stroke-width="2"/>`;
    boxes += `<rect x="${b.x}" y="${b.y}" width="${b.w}" height="${CH}" fill="#eaf2e3" stroke="#333" stroke-width="2"/>`;
    boxes += `<text x="${b.x + b.w / 2}" y="${b.y + 27}" text-anchor="middle" font-family="${FONT}" font-size="${CN}" font-weight="700" fill="#111">${esc(n)}</text>`;
    let y = b.y + CH + 4;
    b.a.forEach((t) => { y += CR; boxes += `<text x="${b.x + 12}" y="${y - 6}" font-family="${FONT}" font-size="${CF}" fill="#111">${esc(t)}</text>`; });
    if (b.op.length) {
      y += 6;
      boxes += `<line x1="${b.x}" y1="${y}" x2="${b.x + b.w}" y2="${y}" stroke="#333" stroke-width="1.5"/>`;
      y += 4;
      b.op.forEach((t) => { y += CR; boxes += `<text x="${b.x + 12}" y="${y - 6}" font-family="${FONT}" font-size="${CF}" fill="#111">${esc(t)}</text>`; });
    }
  }
  write("class-diagram.svg", CW, CHT, [lines, marks, boxes, labels].join("\n"));
}

// ---------- state diagrams ----------
function state(code, name, x, y, w = 190, h = 62, opts = {}) {
  return { code, name, x, y, w, h, final: !!opts.final };
}
function drawState(s) {
  let out = `<rect x="${s.x}" y="${s.y}" width="${s.w}" height="${s.h}" rx="16" fill="${s.final ? "#f3f3f3" : "#fff7e6"}" stroke="#7a5200" stroke-width="${s.final ? 2.6 : 1.8}"/>`;
  out += `<text x="${s.x + s.w / 2}" y="${s.y + 24}" text-anchor="middle" font-family="${FONT}" font-size="15" font-weight="700" fill="#5a3c00">${esc(s.code)}</text>`;
  const words = s.name.split(" ");
  const lines = [];
  let cur = "";
  for (const w of words) { if ((cur + " " + w).trim().length > Math.floor((s.w - 16) / 8.2) && cur) { lines.push(cur); cur = w; } else cur = (cur + " " + w).trim(); }
  lines.push(cur);
  lines.forEach((l, i) => { out += `<text x="${s.x + s.w / 2}" y="${s.y + 44 + i * 17}" text-anchor="middle" font-family="${FONT}" font-size="15" fill="#111">${esc(l)}</text>`; });
  return out;
}
function arrowHead(p1, p2) {
  const a = Math.atan2(p2.y - p1.y, p2.x - p1.x), L = 11, W = 5.5;
  const bx = p2.x - L * Math.cos(a), by = p2.y - L * Math.sin(a);
  return `<path d="M${p2.x} ${p2.y} L${bx + W * Math.sin(a)} ${by - W * Math.cos(a)} L${bx - W * Math.sin(a)} ${by + W * Math.cos(a)} Z" fill="#333"/>`;
}
// transition label; "\n" splits it into lines centred on (x, y)
function tlabel(text, x, y) {
  const lines = text.split("\n"), lh = 17;
  const w = Math.max(...lines.map((l) => l.length)) * 7.3 + 10, h = lines.length * lh + 3;
  const top = y - h / 2;
  let s = `<rect x="${x - w / 2}" y="${top}" width="${w}" height="${h}" rx="4" fill="#fff" opacity="0.92"/>`;
  lines.forEach((l, i) => { s += `<text x="${x}" y="${top + 14 + i * lh}" text-anchor="middle" font-family="${FONT}" font-size="14" font-style="italic" fill="#333">${esc(l)}</text>`; });
  return s;
}
function choice(x, y) {
  return `<path d="M${x} ${y - 14} L${x + 14} ${y} L${x} ${y + 14} L${x - 14} ${y} Z" fill="#fff" stroke="#333" stroke-width="1.6"/>`;
}
function history(x, y) {
  return `<circle cx="${x}" cy="${y}" r="12" fill="#fff" stroke="#333" stroke-width="1.6"/><text x="${x}" y="${y + 5}" text-anchor="middle" font-family="${FONT}" font-size="14" font-weight="700" fill="#111">H</text>`;
}
class StateDiagram {
  constructor() { this.lines = ""; this.boxes = ""; this.labels = ""; }
  add(svg) { this.boxes += svg; }
  // transition along explicit points; label at index or point
  t(points, label, at) {
    this.lines += poly(points) + arrowHead(points[points.length - 2], points[points.length - 1]);
    if (label) {
      const p = at || { x: (points[0].x + points[1].x) / 2, y: (points[0].y + points[1].y) / 2 };
      this.labels += tlabel(label, p.x, p.y);
    }
  }
  initial(x, y) { this.boxes += `<circle cx="${x}" cy="${y}" r="10" fill="#111"/>`; }
  finalNode(x, y) { this.boxes += `<circle cx="${x}" cy="${y}" r="12" fill="#fff" stroke="#111" stroke-width="2"/><circle cx="${x}" cy="${y}" r="7" fill="#111"/>`; }
  composite(x, y, w, h, title, tx = 16) {
    this.lines = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="22" fill="#fffdf6" stroke="#7a5200" stroke-width="1.8"/><text x="${x + tx}" y="${y + 24}" font-family="${FONT}" font-size="15" font-weight="700" fill="#5a3c00">${esc(title)}</text>` + this.lines;
  }
  write(file, w, h) { write(file, w, h, this.lines + this.boxes + this.labels); }
}

// Figure 10.2 asset states
{
  const g = new StateDiagram();
  const s1 = state("AS-01", "Draft", 40, 80);
  const s2 = state("AS-02", "In service", 360, 100, 180);
  const s3 = state("AS-03", "In storage", 680, 100, 180);
  const s4 = state("AS-04", "Under maintenance", 40, 375);
  const s6 = state("AS-06", "Retired", 380, 375);
  const s5 = state("AS-05", "In transfer", 710, 375);
  const f = [state("AS-07", "Donated", 30, 620, 170, 62, { final: true }), state("AS-08", "Recycled", 260, 620, 170, 62, { final: true }), state("AS-09", "Disassembled", 490, 620, 170, 62, { final: true }), state("AS-10", "Disposed", 720, 620, 170, 62, { final: true })];
  const B = 215; // bottom edge of the Active composite
  g.composite(330, 30, 560, B - 30, "Active");
  g.initial(135, 35);
  g.t([{ x: 135, y: 45 }, { x: 135, y: 80 }]);
  // entering Active: a choice puts the asset in service or in storage (SRS section 4.1.1)
  g.initial(610, 42);
  g.t([{ x: 610, y: 52 }, { x: 610, y: 62 }]);
  g.add(choice(610, 76));
  g.t([{ x: 596, y: 76 }, { x: 450, y: 76 }, { x: 450, y: 100 }], "[in use]", { x: 523, y: 76 });
  g.t([{ x: 624, y: 76 }, { x: 770, y: 76 }, { x: 770, y: 100 }], "[stored]", { x: 697, y: 76 });
  // a cancelled transfer or a resolved dispute returns to the previous state, shown by the history state H
  g.add(history(600, 190));
  g.t([{ x: 230, y: 110 }, { x: 330, y: 110 }], "confirmed", { x: 280, y: 94 });
  g.t([{ x: 540, y: 120 }, { x: 680, y: 120 }], "put into storage", { x: 610, y: 107 });
  g.t([{ x: 680, y: 148 }, { x: 540, y: 148 }], "put into use", { x: 610, y: 162 });
  // between Active and the middle row
  g.t([{ x: 380, y: B }, { x: 380, y: 295 }, { x: 135, y: 295 }, { x: 135, y: 375 }], "repair approved", { x: 255, y: 295 });
  g.t([{ x: 200, y: 375 }, { x: 200, y: 325 }, { x: 410, y: 325 }, { x: 410, y: B }], "repair completed", { x: 300, y: 325 });
  g.t([{ x: 450, y: B }, { x: 450, y: 375 }], "end of life\nproposed", { x: 472, y: 270 });
  g.t([{ x: 530, y: 375 }, { x: 530, y: B }], "action\nrejected", { x: 530, y: 320 });
  g.t([{ x: 740, y: B }, { x: 740, y: 375 }], "handed over", { x: 740, y: 255 });
  g.t([{ x: 800, y: 375 }, { x: 800, y: 190 }, { x: 612, y: 190 }], "cancelled or\nresolved", { x: 800, y: 320 });
  g.t([{ x: 860, y: 375 }, { x: 860, y: B }], "received", { x: 860, y: 255 });
  g.t([{ x: 230, y: 407 }, { x: 380, y: 407 }], "not repairable", { x: 305, y: 427 });
  // retired: one choice point, then one guarded branch for each final action
  const cy = 520;
  g.t([{ x: 475, y: 437 }, { x: 475, y: cy - 14 }], "action completed", { x: 560, y: 472 });
  g.add(choice(475, cy));
  const guards = ["[donate]", "[recycle]", "[disassemble]", "[dispose]"];
  f.forEach((st, i) => {
    const sx = st.x + st.w / 2, from = sx < 475 ? 461 : 489;
    g.t([{ x: from, y: cy }, { x: sx, y: cy }, { x: sx, y: st.y }], guards[i], { x: sx, y: 575 });
    g.t([{ x: sx, y: st.y + st.h }, { x: sx, y: st.y + st.h + 22 }]);
    g.finalNode(sx, st.y + st.h + 34);
  });
  [s1, s2, s3, s4, s6, s5, ...f].forEach((st) => g.add(drawState(st)));
  g.write("state-asset.svg", 920, 740);
}

// Figure 10.3 resource request states
{
  const g = new StateDiagram();
  const X = 340, W = 230;
  const s = {
    1: state("RQ-01", "Draft", X, 50, W), 2: state("RQ-02", "Pending department approval", X, 175, W, 70), 3: state("RQ-03", "Open", X, 310, W),
    4: state("RQ-04", "Reservation requested", X, 440, W), 5: state("RQ-05", "In transfer", X, 570, W), 6: state("RQ-06", "Fulfilled", X, 700, W, 62, { final: true }),
    8: state("RQ-08", "Rejected", 760, 179, 150, 62, { final: true }), 7: state("RQ-07", "No suitable item", 760, 270, 150, 62, { final: true }),
    10: state("RQ-10", "Expired", 760, 360, 150, 62, { final: true }), 9: state("RQ-09", "Cancelled", 760, 450, 150, 62, { final: true }),
  };
  g.initial(X + W / 2, 18);
  g.t([{ x: X + W / 2, y: 28 }, { x: X + W / 2, y: 50 }]);
  const cx = X + W / 2 + 40, bx = X + W / 2 - 40;
  g.t([{ x: cx, y: 112 }, { x: cx, y: 175 }], "submitted", { x: cx + 48, y: 142 });
  g.t([{ x: cx, y: 245 }, { x: cx, y: 310 }], "approved (BR-03)", { x: cx + 72, y: 290 });
  g.t([{ x: cx, y: 372 }, { x: cx, y: 440 }], "hold requested", { x: cx + 60, y: 405 });
  g.t([{ x: cx, y: 502 }, { x: cx, y: 570 }], "transfer created", { x: cx + 62, y: 535 });
  g.t([{ x: cx, y: 632 }, { x: cx, y: 700 }], "receipt confirmed", { x: cx + 68, y: 665 });
  // back transitions on the left
  g.t([{ x: bx, y: 175 }, { x: bx, y: 112 }], "changes requested", { x: bx - 72, y: 142 });
  g.t([{ x: X, y: 330 }, { x: 290, y: 330 }, { x: 290, y: 220 }, { x: X, y: 220 }], "changed after approval", { x: 200, y: 275 });
  g.t([{ x: X, y: 470 }, { x: 290, y: 470 }, { x: 290, y: 355 }, { x: X, y: 355 }], "hold\nended", { x: 290, y: 412 });
  g.t([{ x: X, y: 600 }, { x: 240, y: 600 }, { x: 240, y: 342 }, { x: X, y: 342 }], "transfer rejected\nor cancelled", { x: 240, y: 540 });
  // RQ-03 and RQ-04 sit inside one composite state, so one "cancelled" transition covers both
  g.composite(315, 266, 300, 256, "Active request");
  g.t([{ x: X + W, y: 210 }, { x: 760, y: 210 }], "rejected", { x: 665, y: 196 });
  g.t([{ x: X + W, y: 322 }, { x: 650, y: 322 }, { x: 650, y: 301 }, { x: 760, y: 301 }], "no suitable\nitem", { x: 705, y: 301 });
  g.t([{ x: X + W, y: 352 }, { x: 650, y: 352 }, { x: 650, y: 391 }, { x: 760, y: 391 }], "date passed", { x: 705, y: 391 });
  g.t([{ x: 615, y: 490 }, { x: 760, y: 490 }], "cancelled", { x: 687, y: 474 });
  // deleted draft and final nodes
  g.t([{ x: X + W, y: 80 }, { x: 760, y: 80 }], "deleted", { x: 660, y: 66 });
  g.finalNode(772, 80);
  for (const k of [8, 7, 10, 9]) { const st = s[k]; g.t([{ x: st.x + st.w, y: st.y + 31 }, { x: st.x + st.w + 22, y: st.y + 31 }]); g.finalNode(st.x + st.w + 34, st.y + 31); }
  g.t([{ x: X + W / 2, y: 762 }, { x: X + W / 2, y: 784 }]);
  g.finalNode(X + W / 2, 796);
  Object.values(s).forEach((st) => g.add(drawState(st)));
  g.write("state-request.svg", 970, 820);
}

// Figure 10.4 transfer states
{
  const g = new StateDiagram();
  const s1 = state("TR-01", "Pending release approval", 360, 80, 230, 66);
  const s2 = state("TR-02", "Pending receipt approval", 360, 210, 230, 66);
  const s3 = state("TR-03", "Pending policy approval", 650, 210, 230, 66);
  const s4 = state("TR-04", "Approved", 360, 400, 230);
  const s5 = state("TR-05", "Handed over", 360, 530, 230);
  const s6 = state("TR-06", "Completed", 360, 670, 230, 62, { final: true });
  const s7 = state("TR-07", "Disputed", 680, 530, 200);
  const s8 = state("TR-08", "Rejected", 30, 150, 190, 62, { final: true });
  const s9 = state("TR-09", "Cancelled", 30, 400, 190, 62, { final: true });
  g.composite(320, 40, 600, 270, "Waiting for approvals", 300);
  g.initial(475, 14);
  g.t([{ x: 475, y: 24 }, { x: 475, y: 80 }]);
  g.t([{ x: 475, y: 146 }, { x: 475, y: 210 }], "release approved", { x: 545, y: 178 });
  g.t([{ x: 475, y: 276 }, { x: 475, y: 321 }], "receipt approved", { x: 395, y: 298 });
  g.add(choice(475, 335));
  g.t([{ x: 489, y: 335 }, { x: 700, y: 335 }, { x: 700, y: 276 }], "[BR-06 applies]", { x: 600, y: 335 });
  g.t([{ x: 475, y: 349 }, { x: 475, y: 400 }], "[BR-06 does not apply]", { x: 380, y: 375 });
  g.t([{ x: 830, y: 276 }, { x: 830, y: 365 }, { x: 540, y: 365 }, { x: 540, y: 400 }], "policy approved", { x: 690, y: 365 });
  g.t([{ x: 320, y: 181 }, { x: 220, y: 181 }], "rejected", { x: 270, y: 165 });
  g.t([{ x: 320, y: 280 }, { x: 125, y: 280 }, { x: 125, y: 400 }], "cancelled", { x: 220, y: 265 });
  g.t([{ x: 360, y: 431 }, { x: 220, y: 431 }], "cancelled", { x: 290, y: 448 });
  g.t([{ x: 475, y: 462 }, { x: 475, y: 530 }], "handed over", { x: 530, y: 496 });
  g.t([{ x: 590, y: 561 }, { x: 680, y: 561 }], "difference\nrecorded", { x: 635, y: 541 });
  g.t([{ x: 475, y: 592 }, { x: 475, y: 670 }], "receipt confirmed", { x: 545, y: 632 });
  g.t([{ x: 740, y: 592 }, { x: 740, y: 701 }, { x: 590, y: 701 }], "resolved and\nreceived", { x: 740, y: 650 });
  g.t([{ x: 820, y: 592 }, { x: 820, y: 770 }, { x: 125, y: 770 }, { x: 125, y: 462 }], "returned", { x: 470, y: 770 });
  g.t([{ x: s8.x + s8.w / 2, y: s8.y }, { x: s8.x + s8.w / 2, y: s8.y - 24 }]);
  g.finalNode(s8.x + s8.w / 2, s8.y - 36);
  g.t([{ x: 60, y: s9.y + s9.h }, { x: 60, y: s9.y + s9.h + 24 }]);
  g.finalNode(60, s9.y + s9.h + 36);
  g.t([{ x: 360, y: 701 }, { x: 330, y: 701 }]);
  g.finalNode(318, 701);
  [s1, s2, s3, s4, s5, s6, s7, s8, s9].forEach((st) => g.add(drawState(st)));
  g.write("state-transfer.svg", 940, 800);
}

// Figure 10.5 approval task states
{
  const g = new StateDiagram();
  const p = state("AT-01", "Pending", 360, 60, 210);
  const f = [state("AT-02", "Approved", 20, 300, 200, 62, { final: true }), state("AT-03", "Rejected", 255, 300, 200, 62, { final: true }), state("AT-04", "Changes requested", 490, 300, 200, 62, { final: true }), state("AT-05", "Withdrawn", 725, 300, 200, 62, { final: true })];
  const labels = ["approve", "reject with a reason", "request changes with a reason", "parent record cancelled"];
  g.initial(465, 20);
  g.t([{ x: 465, y: 30 }, { x: 465, y: 60 }]);
  f.forEach((st, i) => {
    const x0 = 405 + i * 30;
    // outer branches turn higher than inner ones, so no two lines cross
    const turnY = i === 0 || i === 3 ? 180 : 230;
    g.t([{ x: x0, y: 122 }, { x: x0, y: turnY }, { x: st.x + st.w / 2, y: turnY }, { x: st.x + st.w / 2, y: 300 }], labels[i], { x: st.x + st.w / 2, y: 270 });
    g.t([{ x: st.x + st.w / 2, y: 362 }, { x: st.x + st.w / 2, y: 384 }]);
    g.finalNode(st.x + st.w / 2, 396);
  });
  [p, ...f].forEach((st) => g.add(drawState(st)));
  g.write("state-approval.svg", 945, 420);
}
