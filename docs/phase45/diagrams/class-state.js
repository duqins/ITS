// Draws the section 10 class diagrams and state diagrams as SVG files.
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

// ---------- shared routing (same rules as the ER diagrams) ----------
function pt(b, side, f) {
  const along = (len, start) => (typeof f === "object" ? f.abs : start + len * f);
  if (side === "top") return { x: along(b.w, b.x), y: b.y };
  if (side === "bottom") return { x: along(b.w, b.x), y: b.y + b.h };
  if (side === "left") return { x: b.x, y: along(b.h, b.y) };
  return { x: b.x + b.w, y: along(b.h, b.y) };
}
const horiz = (s) => s === "left" || s === "right";
function route(a, as, b, bs, mid) {
  if (horiz(as) && horiz(bs)) {
    if (a.y === b.y && as !== bs) return [a, b];
    const mx = mid !== undefined ? mid : (a.x + b.x) / 2;
    return [a, { x: mx, y: a.y }, { x: mx, y: b.y }, b];
  }
  if (!horiz(as) && !horiz(bs)) {
    if (a.x === b.x && as !== bs) return [a, b];
    const my = mid !== undefined ? mid : (a.y + b.y) / 2;
    return [a, { x: a.x, y: my }, { x: b.x, y: my }, b];
  }
  if (horiz(as)) return [a, { x: b.x, y: a.y }, b];
  return [a, { x: a.x, y: b.y }, b];
}
const poly = (pts, extra = "") => `<polyline points="${pts.map((p) => `${p.x},${p.y}`).join(" ")}" fill="none" stroke="#333" stroke-width="1.6"${extra}/>`;

// ---------- class diagrams ----------
const CH = 32, CR = 21;
function cls(name, x, y, attrs, ops, opts = {}) {
  const w = opts.w || 270;
  const h = CH + attrs.length * CR + 10 + (ops.length ? ops.length * CR + 10 : 0);
  return { name, x, y, w, h, attrs, ops, ref: !!opts.ref, stereo: opts.stereo };
}
function drawCls(c) {
  const stroke = c.ref ? "#9a9a9a" : "#333", dash = c.ref ? ' stroke-dasharray="6 4"' : "", text = c.ref ? "#666" : "#111";
  let s = `<rect x="${c.x}" y="${c.y}" width="${c.w}" height="${c.h}" fill="#fff" stroke="${stroke}" stroke-width="1.6"${dash}/>`;
  s += `<rect x="${c.x}" y="${c.y}" width="${c.w}" height="${CH}" fill="${c.ref ? "#f4f4f4" : "#eaf2e3"}" stroke="${stroke}" stroke-width="1.6"${dash}/>`;
  s += `<text x="${c.x + c.w / 2}" y="${c.y + 22}" text-anchor="middle" font-family="${FONT}" font-size="17" font-weight="700" fill="${text}">${esc(c.name)}</text>`;
  let y = c.y + CH + 4;
  c.attrs.forEach((a) => { y += CR; s += `<text x="${c.x + 9}" y="${y - 5}" font-family="${FONT}" font-size="15" fill="${text}">${esc(a)}</text>`; });
  if (c.ops.length) {
    y += 6;
    s += `<line x1="${c.x}" y1="${y}" x2="${c.x + c.w}" y2="${y}" stroke="${stroke}" stroke-width="1.2"${dash}/>`;
    y += 4;
    c.ops.forEach((o) => { y += CR; s += `<text x="${c.x + 9}" y="${y - 5}" font-family="${FONT}" font-size="15" fill="${text}">${esc(o)}</text>`; });
  }
  return s;
}
function mult(p, side, text, below) {
  let x = p.x, y = p.y, anchor = "start";
  if (side === "right") { x = p.x + 7; y = below ? p.y + 19 : p.y - 8; }
  if (side === "left") { x = p.x - 7; y = below ? p.y + 19 : p.y - 8; anchor = "end"; }
  if (side === "top") { x = p.x + 8; y = p.y - 9; }
  if (side === "bottom") { x = p.x + 8; y = p.y + 21; }
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="${FONT}" font-size="15" font-weight="700" fill="#1F3864">${esc(text)}</text>`;
}
function diamond(p, side, filled) {
  const d = { top: [0, -1], bottom: [0, 1], left: [-1, 0], right: [1, 0] }[side];
  const L = 22, W = 8;
  const tip = p, mid = { x: p.x + d[0] * L / 2, y: p.y + d[1] * L / 2 }, end = { x: p.x + d[0] * L, y: p.y + d[1] * L };
  const px = -d[1], py = d[0];
  return { svg: `<path d="M${tip.x} ${tip.y} L${mid.x + px * W} ${mid.y + py * W} L${end.x} ${end.y} L${mid.x - px * W} ${mid.y - py * W} Z" fill="${filled ? "#333" : "#fff"}" stroke="#333" stroke-width="1.6"/>`, end };
}
function assoc(boxes, e) {
  const A = boxes[e.a], B = boxes[e.b];
  let p1 = pt(A, e.as, e.af);
  const p2 = pt(B, e.bs, e.bf);
  let s = "";
  if (e.kind === "aggr" || e.kind === "comp") {
    const dm = diamond(p1, e.as, e.kind === "comp");
    s += dm.svg;
    p1 = dm.end;
  }
  const pts = route(p1, e.as, p2, e.bs, e.mid);
  s += poly(pts);
  const q = pt(A, e.as, e.af);
  // a plain association is navigable toward A, the class the other one refers to
  if (!e.kind) s += navArrow(q, e.as);
  s += mult(e.kind ? dm2(q, e.as) : nudge(q, e.as, e.belowA), e.as, e.ma, e.belowA) + mult(p2, e.bs, e.mb, e.belowB);
  if (e.name) {
    let best = -1, bi = 0;
    for (let i = 0; i < pts.length - 1; i++) {
      const len = Math.abs(pts[i + 1].x - pts[i].x) + Math.abs(pts[i + 1].y - pts[i].y);
      if (len > best) { best = len; bi = i; }
    }
    if (e.seg !== undefined) bi = e.seg;
    const q1 = pts[bi], q2 = pts[bi + 1], vertical = q1.x === q2.x;
    const mx = (q1.x + q2.x) / 2, my = (q1.y + q2.y) / 2;
    if (vertical && e.rot) s += `<text x="${mx - 6}" y="${my}" transform="rotate(-90 ${mx - 6} ${my})" text-anchor="middle" font-family="${FONT}" font-size="14" font-style="italic" fill="#444">${esc(e.name)}</text>`;
    else s += `<text x="${vertical ? mx + 7 : mx}" y="${vertical ? my + 5 : my + 18}" text-anchor="${vertical ? "start" : "middle"}" font-family="${FONT}" font-size="14" font-style="italic" fill="#444">${esc(e.name)}</text>`;
  }
  return s;
}
// multiplicity next to a diamond sits a little further out
function dm2(p, side) {
  const d = { top: [0, -1], bottom: [0, 1], left: [-1, 0], right: [1, 0] }[side];
  return { x: p.x + d[0] * 22, y: p.y + d[1] * 22 };
}
// open arrowhead touching the box edge (navigability)
function navArrow(p, side) {
  const d = { top: [0, -1], bottom: [0, 1], left: [-1, 0], right: [1, 0] }[side];
  const L = 14, W = 7, px = -d[1], py = d[0];
  const b = { x: p.x + d[0] * L, y: p.y + d[1] * L };
  return `<polyline points="${b.x + px * W},${b.y + py * W} ${p.x},${p.y} ${b.x - px * W},${b.y - py * W}" fill="none" stroke="#333" stroke-width="1.6"/>`;
}
// multiplicity next to an arrowhead moves clear of it
function nudge(p, side, below) {
  if (side === "top" || side === "bottom") return { x: p.x + 5, y: p.y };
  return { x: p.x, y: p.y + (below ? 5 : -5) };
}
// generalization: subclasses joined to one hollow triangle under the superclass
function generalization(sup, subs, joinY) {
  const cx = sup.x + sup.w / 2, base = sup.y + sup.h;
  let s = `<path d="M${cx} ${base} L${cx - 11} ${base + 18} L${cx + 11} ${base + 18} Z" fill="#fff" stroke="#333" stroke-width="1.6"/>`;
  s += poly([{ x: cx, y: base + 18 }, { x: cx, y: joinY }]);
  for (const c of subs) s += poly([{ x: c.x + c.w / 2, y: c.y }, { x: c.x + c.w / 2, y: joinY }, { x: cx, y: joinY }]);
  return s;
}
function classFigure(file, w, h, list, edges, extra = "") {
  const boxes = Object.fromEntries(list.map((b) => [b.name, b]));
  write(file, w, h, edges.map((e) => assoc(boxes, e)).join("\n") + extra + list.map(drawCls).join("\n"));
}
const bottom = (b) => b.y + b.h;
const C1 = 20, C2 = 350, C3 = 680;

// Figure 10.1 people and access
{
  const Role = cls("Role", C1, 30, ["- name: String"], ["+ allows(action: String): bool"]);
  const UR = cls("UserRole", C2, 30, ["- status: RoleStatus"], ["+ authorise(by: User): void", "+ apply(by: User): void", "+ remove(): void"]);
  const D = cls("Department", C3, 30, ["- name: String", "- code: String"], ["+ deactivate(): void"]);
  const N = cls("Notification", C1, 320, ["- message: String", "- sentAt: DateTime", "- readAt: DateTime"], ["+ markRead(): void"]);
  const U = cls("User", C2, 320, ["- name: String", "- email: String", "- accountStatus: AccountStatus"], ["+ signIn(password: String): bool", "+ hasRole(r: Role, d: Department): bool", "+ deactivate(): void"]);
  const AL = cls("AuditLog", C2, 620, ["- action: String", "- recordType: String", "- recordId: int", "- role: String", "- beforeValue: String", "- afterValue: String", "- reason: String", "- createdAt: DateTime"], ["+ record(actor: User, action: String): void"], { w: 315 });
  classFigure("class-people.svg", 970, bottom(AL) + 25, [Role, UR, D, N, U, AL], [
    { a: "Role", as: "right", af: { abs: 80 }, b: "UserRole", bs: "left", bf: { abs: 80 }, ma: "1", mb: "0..*", name: "used in" },
    { a: "Department", as: "left", af: { abs: 80 }, b: "UserRole", bs: "right", bf: { abs: 80 }, ma: "1", mb: "0..*", name: "scopes" },
    { a: "User", as: "top", af: 0.5, b: "UserRole", bs: "bottom", bf: 0.5, ma: "1", mb: "0..*", name: "holds", kind: "comp" },
    { a: "Department", as: "bottom", af: 0.3, b: "User", bs: "right", bf: { abs: 370 }, ma: "1", mb: "0..*", name: "employs", kind: "aggr", seg: 0 },
    { a: "User", as: "left", af: { abs: 370 }, b: "Notification", bs: "right", bf: { abs: 370 }, ma: "1", mb: "0..*", name: "receives" },
    { a: "User", as: "bottom", af: 0.5, b: "AuditLog", bs: "top", bf: 0.5, ma: "0..1", mb: "0..*", name: "performs" },
  ]);
}

// Figure 10.2 assets and listings
{
  const D = cls("Department", C1, 30, ["- name: String", "- code: String"], []);
  const Cat = cls("Category", C2, 30, ["- name: String", "- unit: String", "- emissionFactor: Range"], ["+ isSpecialHandling(): bool"]);
  const MV = cls("ModelVersion", 720, 30, ["- modelName: String", "- version: String"], [], { w: 250 });
  const L = cls("Listing", 10, 330, ["- quantity: int", "- availableFrom: Date", "- status: ListingStatus"], ["+ submitForRelease(): void", "+ publish(): void", "+ withdraw(reason: String): void"], { w: 240 });
  const A = cls("Asset", C2, 330, ["- name: String", "- condition: Condition", "- status: AssetStatus", "- quantity: int", "- location: Location", "- purchaseDate: Date", "- /assetAge: int"], ["+ register(): void", "+ confirm(by: User): void", "+ changeStatus(to: AssetStatus): void", "+ reserve(qty: int): void", "+ release(qty: int): void"]);
  const AS = cls("AiSuggestion", 720, 330, ["- task: String", "- suggestion: String", "- confidence: Decimal", "- userResponse: String"], ["+ accept(): void", "+ correct(value: String): void", "+ reject(reason: String): void"], { w: 250 });
  const IT = cls("ITAsset", C1, 820, ["- serialNumber: String", "- storesData: bool"], ["+ needsDataErasure(): bool"]);
  const FU = cls("FurnitureAsset", C2, 820, ["- material: String", "- dimensions: String"], []);
  const AT = cls("Attachment", 720, 570, ["- fileName: String", "- fileType: String", "- sizeKB: int"], ["+ openLink(by: User): String"], { w: 250 });
  const joinY = 790;
  classFigure("class-assets.svg", 990, bottom(IT) + 25, [D, Cat, MV, L, A, AS, IT, FU, AT], [
    { a: "Department", as: "bottom", af: 0.8, b: "Asset", bs: "top", bf: 0.2, mid: 260, ma: "1", mb: "0..*", name: "owns", kind: "aggr", seg: 1 },
    { a: "Category", as: "bottom", af: 0.6, b: "Asset", bs: "top", bf: 0.6, ma: "1", mb: "0..*", name: "classifies" },
    { a: "Asset", as: "left", af: { abs: 380 }, b: "Listing", bs: "right", bf: { abs: 380 }, ma: "1", mb: "0..*", name: "offered in" },
    { a: "Asset", as: "right", af: { abs: 380 }, b: "AiSuggestion", bs: "left", bf: { abs: 380 }, ma: "0..1", mb: "0..*", name: "gets" },
    { a: "ModelVersion", as: "bottom", af: 0.5, b: "AiSuggestion", bs: "top", bf: 0.5, ma: "1", mb: "0..*", name: "produces" },
    { a: "Asset", as: "right", af: { abs: 600 }, b: "Attachment", bs: "left", bf: { abs: 600 }, ma: "0..1", mb: "0..*", name: "has", kind: "comp" },
  ], generalization(A, [IT, FU], joinY));
}

// Figure 10.3 requests, matching and transfers
{
  const Ar = cls("Asset", C1, 30, [], [], { ref: true });
  const MV = cls("ModelVersion", C2, 30, [], [], { ref: true });
  const Ur = cls("User", C3, 30, [], [], { ref: true });
  const M = cls("MatchRecommendation", C2, 190, ["- score: Decimal", "- confidence: Decimal", "- explanation: String"], ["+ accept(): void", "+ override(reason: String): void", "+ summarize(): String"]);
  const R = cls("ResourceRequest", C3, 190, ["- status: RequestStatus", "- requiredBy: Date"], ["+ submit(): void", "+ approve(by: User): void", "+ cancel(reason: String): void", "+ expire(): void"]);
  const T = cls("Transfer", C2, 480, ["- quantity: int", "- toLocation: Location", "- plannedDate: Date", "- status: TransferStatus"], ["+ handOver(): void", "+ confirmReceipt(): void", "+ dispute(note: String): void", "+ cancel(reason: String): void"]);
  const RS = cls("RequestSpecification", C3, 480, ["- specifications: String", "- quantity: int", "- minCondition: Condition", "- urgency: Urgency"], []);
  const Lr = cls("Listing", C1, 820, [], [], { ref: true, w: 230 });
  const Res = cls("Reservation", C2, 820, ["- quantity: int", "- expiresAt: DateTime", "- status: ReservationStatus"], ["+ confirm(by: User): void", "+ cancel(reason: String): void", "+ expire(): void"]);
  classFigure("class-requests.svg", 1010, bottom(Res) + 25, [Ar, MV, Ur, M, R, T, RS, Lr, Res], [
    { a: "Asset", as: "bottom", af: 0.5, b: "MatchRecommendation", bs: "left", bf: { abs: 250 }, ma: "1", mb: "0..*", name: "matched in", seg: 0 },
    { a: "ModelVersion", as: "bottom", af: 0.5, b: "MatchRecommendation", bs: "top", bf: 0.5, ma: "1", mb: "0..*", name: "produces" },
    { a: "User", as: "bottom", af: 0.5, b: "ResourceRequest", bs: "top", bf: 0.5, ma: "1", mb: "0..*", name: "submits" },
    { a: "ResourceRequest", as: "left", af: { abs: 250 }, b: "MatchRecommendation", bs: "right", bf: { abs: 250 }, ma: "1", mb: "0..*", name: "receives" },
    { a: "ResourceRequest", as: "bottom", af: 0.5, b: "RequestSpecification", bs: "top", bf: 0.5, ma: "1", mb: "1", name: "owns", kind: "comp" },
    { a: "Asset", as: "bottom", af: 0.25, b: "Transfer", bs: "left", bf: { abs: 560 }, ma: "1", mb: "0..*", name: "moved by", seg: 0 },
    { a: "ResourceRequest", as: "left", af: { abs: 335 }, b: "Transfer", bs: "right", bf: { abs: 560 }, mid: 650, ma: "1", mb: "0..*", name: "fulfilled by", seg: 1, rot: true },
    { a: "Reservation", as: "top", af: 0.5, b: "Transfer", bs: "bottom", bf: 0.5, ma: "1", mb: "0..1", name: "becomes" },
    { a: "Listing", as: "right", af: { abs: 845 }, b: "Reservation", bs: "left", bf: { abs: 845 }, ma: "1", mb: "0..*", name: "held by" },
    { a: "ResourceRequest", as: "right", af: { abs: 300 }, b: "Reservation", bs: "right", bf: { abs: 900 }, mid: 985, ma: "1", mb: "0..*", name: "places", seg: 1, rot: true },
  ]);
}

// Figure 10.4 approvals and life cycle
{
  const Ap = cls("Approval", C2, 30, ["- stage: String", "- decision: Decision", "- reason: String", "- approverRole: String", "- recordVersion: int", "- status: ApprovalStatus"], ["+ approve(by: User): void", "+ reject(by: User, reason: String): void", "+ requestChanges(by: User, r: String): void", "+ withdraw(): void"], { w: 300 });
  const Rr = cls("ResourceRequest", C1, 60, [], [], { ref: true, w: 230 });
  const Lr = cls("Listing", C3 + 50, 60, [], [], { ref: true, w: 225 });
  const MR = cls("MaintenanceRecord", C1, 390, ["- estimatedCost: Decimal", "- actualCost: Decimal", "- conditionAfter: Condition", "- status: WorkOrderStatus"], ["+ assess(cost: Decimal): void", "+ start(): void", "+ complete(after: Condition): void"]);
  const Tr = cls("Transfer", C2, 390, [], [], { ref: true, w: 300 });
  const EL = cls("EndOfLifeAction", C3, 390, ["- action: EndOfLifeType", "- destination: String", "- status: EndOfLifeStatus"], ["+ propose(): void", "+ complete(): void"]);
  const SI = cls("SustainabilityImpact", C2, 640, ["- wasteDivertedKg: Decimal", "- avoidedPurchaseAED: Decimal", "- co2eLowKg: Decimal", "- co2eHighKg: Decimal"], ["+ calculate(): void"], { w: 300 });
  const I = cls("Inspection", C1, 900, ["- inspectedOn: DateTime", "- conditionFound: Condition", "- safeToUse: bool"], ["+ record(): void"]);
  const Ar = cls("Asset", C2, 960, [], [], { ref: true, w: 300 });
  const sib = bottom(SI) + 30;
  classFigure("class-lifecycle.svg", 980, bottom(I) + 25, [Ap, Rr, Lr, MR, Tr, EL, SI, I, Ar], [
    { a: "ResourceRequest", as: "right", af: { abs: 76 }, b: "Approval", bs: "left", bf: { abs: 76 }, ma: "0..1", mb: "0..*", name: "needs" },
    { a: "Listing", as: "left", af: { abs: 76 }, b: "Approval", bs: "right", bf: { abs: 76 }, ma: "0..1", mb: "0..*", name: "needs" },
    { a: "Transfer", as: "top", af: 0.5, b: "Approval", bs: "bottom", bf: 0.5, ma: "0..1", mb: "0..*", name: "needs" },
    { a: "MaintenanceRecord", as: "top", af: 0.5, b: "Approval", bs: "bottom", bf: 0.12, mid: 350, ma: "0..1", mb: "0..*", name: "needs", seg: 1 },
    { a: "EndOfLifeAction", as: "top", af: 0.5, b: "Approval", bs: "bottom", bf: 0.88, mid: 350, ma: "0..1", mb: "0..*", name: "needs", seg: 1 },
    { a: "Transfer", as: "bottom", af: 0.5, b: "SustainabilityImpact", bs: "top", bf: 0.5, ma: "0..1", mb: "0..1", name: "creates" },
    { a: "MaintenanceRecord", as: "bottom", af: 0.8, b: "SustainabilityImpact", bs: "left", bf: { abs: 740 }, ma: "0..1", mb: "0..1", name: "creates", seg: 0 },
    { a: "EndOfLifeAction", as: "bottom", af: 0.2, b: "SustainabilityImpact", bs: "right", bf: { abs: 740 }, ma: "0..1", mb: "0..1", name: "creates", seg: 0 },
    { a: "Inspection", as: "top", af: 0.2, b: "MaintenanceRecord", bs: "bottom", bf: 0.2, ma: "0..1", mb: "0..*", name: "leads to" },
    { a: "Asset", as: "top", af: 0.25, b: "MaintenanceRecord", bs: "bottom", bf: 0.55, mid: sib, ma: "1", mb: "0..*", name: "has", seg: 1 },
    { a: "Asset", as: "top", af: 0.75, b: "EndOfLifeAction", bs: "bottom", bf: 0.75, mid: sib, ma: "1", mb: "0..*", name: "ends with", seg: 1 },
    { a: "Asset", as: "left", af: { abs: 990 }, b: "Inspection", bs: "right", bf: { abs: 990 }, ma: "1", mb: "0..*", name: "checks" },
  ]);
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

// Figure 10.5 asset states
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

// Figure 10.6 resource request states
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

// Figure 10.7 transfer states
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

// Figure 10.8 approval task states
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
