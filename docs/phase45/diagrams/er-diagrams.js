// Draws the section 8 ER diagrams as SVG files.
// Usage from the repository root: node docs/phase45/diagrams/er-diagrams.js docs/phase45/images
const fs = require("fs");
const path = require("path");
const outDir = process.argv[2];

const HEAD = 34, ROW = 23, PADB = 8, FONT = "Segoe UI, Arial, sans-serif";
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

function box(name, x, y, rows, opts = {}) {
  return { name, x, y, w: opts.w || 250, h: HEAD + rows.length * ROW + PADB, rows, ref: !!opts.ref };
}

function drawBox(b) {
  const stroke = b.ref ? "#9a9a9a" : "#333", dash = b.ref ? ' stroke-dasharray="6 4"' : "";
  const head = b.ref ? "#f4f4f4" : "#e3ecf7", text = b.ref ? "#666" : "#111";
  let s = `<rect x="${b.x}" y="${b.y}" width="${b.w}" height="${b.h}" rx="3" fill="#fff" stroke="${stroke}" stroke-width="1.6"${dash}/>`;
  s += `<rect x="${b.x}" y="${b.y}" width="${b.w}" height="${HEAD}" rx="3" fill="${head}" stroke="${stroke}" stroke-width="1.6"${dash}/>`;
  s += `<text x="${b.x + b.w / 2}" y="${b.y + 23}" text-anchor="middle" font-family="${FONT}" font-size="18" font-weight="700" fill="${text}">${esc(b.name)}</text>`;
  b.rows.forEach((r, i) => {
    const yy = b.y + HEAD + 17 + i * ROW;
    const m = r.match(/^(PK|FK) (.*)$/);
    s += m
      ? `<text x="${b.x + 10}" y="${yy}" font-family="${FONT}" font-size="16" fill="${text}"><tspan font-weight="700">${m[1]}</tspan> ${esc(m[2])}</text>`
      : `<text x="${b.x + 10}" y="${yy}" font-family="${FONT}" font-size="16" fill="${text}">${esc(r)}</text>`;
  });
  return s;
}

// anchor on a side: f is a fraction along the side, or {abs: coordinate}
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

function endLabel(p, side, text, below) {
  let x = p.x, y = p.y, anchor = "start";
  if (side === "right") { x = p.x + 7; y = below ? p.y + 19 : p.y - 8; }
  if (side === "left") { x = p.x - 7; y = below ? p.y + 19 : p.y - 8; anchor = "end"; }
  if (side === "top") { x = p.x + 8; y = p.y - 9; }
  if (side === "bottom") { x = p.x + 8; y = p.y + 21; }
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="${FONT}" font-size="16" font-weight="700" fill="#1F3864">${esc(text)}</text>`;
}

function drawEdge(boxes, e) {
  const A = boxes[e.a], B = boxes[e.b];
  const p1 = pt(A, e.as, e.af), p2 = pt(B, e.bs, e.bf);
  const pts = route(p1, e.as, p2, e.bs, e.mid);
  let s = `<polyline points="${pts.map((p) => `${p.x},${p.y}`).join(" ")}" fill="none" stroke="#333" stroke-width="1.6"/>`;
  s += endLabel(p1, e.as, e.ca, e.belowA) + endLabel(p2, e.bs, e.cb, e.belowB);
  if (e.name) {
    let best = -1, bi = 0;
    for (let i = 0; i < pts.length - 1; i++) {
      const len = Math.abs(pts[i + 1].x - pts[i].x) + Math.abs(pts[i + 1].y - pts[i].y);
      if (len > best) { best = len; bi = i; }
    }
    if (e.seg !== undefined) bi = e.seg;
    const q1 = pts[bi], q2 = pts[bi + 1];
    const vertical = q1.x === q2.x;
    const mx = (q1.x + q2.x) / 2, my = (q1.y + q2.y) / 2;
    if (vertical && e.rot) {
      s += `<text x="${mx - 6}" y="${my}" transform="rotate(-90 ${mx - 6} ${my})" text-anchor="middle" font-family="${FONT}" font-size="15" font-style="italic" fill="#444">${esc(e.name)}</text>`;
    } else {
      const lx = vertical ? mx + 7 : mx, ly = vertical ? my + 5 : my + 19;
      s += `<text x="${lx}" y="${ly}" text-anchor="${vertical ? "start" : "middle"}" font-family="${FONT}" font-size="15" font-style="italic" fill="#444">${esc(e.name)}</text>`;
    }
  }
  return s;
}

function svg(file, width, height, list, edges) {
  const boxes = Object.fromEntries(list.map((b) => [b.name + (b.key || ""), b]));
  const body = edges.map((e) => drawEdge(boxes, e)).join("\n") + "\n" + list.map(drawBox).join("\n");
  fs.writeFileSync(path.join(outDir, file), `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">\n<rect width="100%" height="100%" fill="#fff"/>\n${body}\n</svg>\n`);
  console.log("wrote " + file);
}

const C1 = 20, C2 = 340, C3 = 660;
const bottom = (b) => b.y + b.h;
const ref = (name, x, y, pk, w) => box(name, x, y, ["PK " + pk], { ref: true, w });

// ---------- Figure 8.1: core ER diagram from the lab ----------
{
  const D = box("Department", C1, 30, ["PK departmentId", "name"]);
  const U = box("User", C2, 30, ["PK userId", "FK departmentId", "name"]);
  const R = box("ResourceRequest", C3, 30, ["PK requestId", "FK requesterId", "quantity", "status"]);
  const A = box("Asset", C1, 300, ["PK assetId", "FK ownerDepartmentId", "name", "condition", "status"]);
  const T = box("Transfer", C3, 300, ["PK transferId", "FK assetId", "FK requestId", "FK approverId", "status"]);
  const M = box("MatchRecommendation", C2, 540, ["PK matchId", "FK assetId", "FK requestId", "FK modelVersionId", "score", "explanation"]);
  const MV = box("ModelVersion", C2, 850, ["PK modelVersionId", "modelName", "version"]);
  svg("erd-core.svg", 990, bottom(MV) + 25, [D, U, R, A, T, M, MV], [
    { a: "Department", as: "right", af: { abs: 95 }, b: "User", bs: "left", bf: { abs: 95 }, ca: "1", cb: "0..*", name: "employs" },
    { a: "User", as: "right", af: { abs: 95 }, b: "ResourceRequest", bs: "left", bf: { abs: 95 }, ca: "1", cb: "0..*", name: "submits" },
    { a: "Department", as: "bottom", af: 0.5, b: "Asset", bs: "top", bf: 0.5, ca: "1", cb: "0..*", name: "owns" },
    { a: "ResourceRequest", as: "bottom", af: 0.75, b: "Transfer", bs: "top", bf: 0.75, ca: "1", cb: "0..*", name: "is fulfilled by" },
    { a: "User", as: "bottom", af: 0.5, b: "Transfer", bs: "top", bf: 0.25, mid: 230, ca: "0..1", cb: "0..*", name: "gives final approval", seg: 1 },
    { a: "Asset", as: "right", af: { abs: 380 }, b: "Transfer", bs: "left", bf: { abs: 380 }, ca: "1", cb: "0..*", name: "is moved by" },
    { a: "Asset", as: "bottom", af: 0.5, b: "MatchRecommendation", bs: "left", bf: { abs: 620 }, ca: "1", cb: "0..*", name: "is matched in" },
    { a: "MatchRecommendation", as: "right", af: { abs: 620 }, b: "ResourceRequest", bs: "right", bf: { abs: 140 }, mid: 960, ca: "0..*", cb: "1", name: "receives", seg: 0 },
    { a: "ModelVersion", as: "top", af: 0.5, b: "MatchRecommendation", bs: "bottom", bf: 0.5, ca: "1", cb: "0..*", name: "produces" },
  ]);
}

// ---------- Figure 8.2: users, roles and access (4 columns) ----------
{
  const WW = 195, K1 = 15, K2 = 280, K3 = 545, K4 = 810;
  const Role = box("Role", K1, 30, ["PK roleId", "name"], { w: WW });
  const UR = box("UserRole", K2, 30, ["PK userRoleId", "FK userId", "FK roleId", "FK departmentId", "status"], { w: WW });
  const D = box("Department", K3, 30, ["PK departmentId", "name", "code"], { w: WW });
  const A = ref("Asset", K4, 30, "assetId", WW);
  const N = box("Notification", K1, 300, ["PK notificationId", "FK userId", "recordType", "recordId", "message", "sentAt", "readAt"], { w: WW });
  const U = box("User", K2, 300, ["PK userId", "FK departmentId", "name", "email", "accountStatus"], { w: WW });
  const AL = box("AuditLog", K1, 640, ["PK auditId", "FK userId", "action", "recordType", "recordId", "createdAt"], { w: WW });
  const R = ref("ResourceRequest", K2, 640, "requestId", WW);
  const T = ref("Transfer", K3, 640, "transferId", WW);
  const Ap = ref("Approval", K4, 640, "approvalId", WW);
  svg("erd-users.svg", 1020, bottom(AL) + 25, [Role, UR, D, A, N, U, AL, R, T, Ap], [
    { a: "Role", as: "right", af: { abs: 90 }, b: "UserRole", bs: "left", bf: { abs: 90 }, ca: "1", cb: "0..*", name: "used in" },
    { a: "Department", as: "left", af: { abs: 90 }, b: "UserRole", bs: "right", bf: { abs: 90 }, ca: "1", cb: "0..*", name: "scopes" },
    { a: "User", as: "top", af: 0.5, b: "UserRole", bs: "bottom", bf: 0.5, ca: "1", cb: "0..*", name: "holds" },
    { a: "Department", as: "bottom", af: 0.3, b: "User", bs: "right", bf: { abs: 345 }, ca: "1", cb: "0..*", name: "employs" },
    { a: "Department", as: "right", af: { abs: 75 }, b: "Asset", bs: "left", bf: { abs: 75 }, ca: "1", cb: "0..*", name: "owns" },
    { a: "User", as: "right", af: { abs: 415 }, b: "Asset", bs: "bottom", bf: 0.5, ca: "1", cb: "0..*", name: "is custodian of", seg: 0 },
    { a: "User", as: "left", af: { abs: 350 }, b: "Notification", bs: "right", bf: { abs: 350 }, ca: "1", cb: "0..*", name: "receives" },
    { a: "User", as: "left", af: { abs: 440 }, b: "AuditLog", bs: "right", bf: { abs: 690 }, mid: 250, ca: "0..1", cb: "0..*", belowB: true, name: "performs", seg: 1 },
    { a: "User", as: "bottom", af: 0.3, b: "ResourceRequest", bs: "top", bf: 0.3, ca: "1", cb: "0..*", name: "submits" },
    { a: "User", as: "bottom", af: 0.68, b: "Transfer", bs: "top", bf: 0.3, mid: 590, ca: "0..1", cb: "0..*", name: "gives final approval", seg: 1 },
    { a: "User", as: "bottom", af: 0.9, b: "Approval", bs: "top", bf: 0.3, mid: 540, ca: "0..1", cb: "0..*", name: "decides", seg: 1 },
  ]);
}

// ---------- Figure 8.3: assets, requests and matching ----------
{
  const Cat = box("Category", C2, 30, ["PK categoryId", "name", "unit", "emissionFactor"]);
  const A = box("Asset", C1, 240, ["PK assetId", "FK ownerDepartmentId", "FK categoryId", "FK custodianId", "name", "condition", "status", "quantity", "location (composite)", "assetAge (derived)"]);
  const MV = box("ModelVersion", C2, 240, ["PK modelVersionId", "task", "modelName", "version"]);
  const R = box("ResourceRequest", C3, 240, ["PK requestId", "FK requesterId", "FK categoryId", "quantity", "requiredBy", "status"]);
  const M = box("MatchRecommendation", C2, 480, ["PK matchId", "FK assetId", "FK requestId", "FK modelVersionId", "score", "confidence", "explanation"]);
  const T = box("Transfer", C2, 790, ["PK transferId", "FK assetId", "FK requestId", "FK reservationId", "FK approverId", "FK fromDepartmentId", "FK toDepartmentId", "FK toCustodianId", "status"]);
  const L = box("Listing", C1, 1150, ["PK listingId", "FK assetId", "quantity", "availableFrom", "status"]);
  const Res = box("Reservation", C2, 1150, ["PK reservationId", "FK requestId", "FK listingId", "quantity", "expiresAt", "status"]);
  svg("erd-assets-requests.svg", 930, bottom(Res) + 25, [Cat, A, MV, R, M, T, L, Res], [
    { a: "Category", as: "left", af: { abs: 90 }, b: "Asset", bs: "top", bf: 0.5, ca: "1", cb: "0..*", name: "classifies", seg: 0 },
    { a: "Category", as: "right", af: { abs: 90 }, b: "ResourceRequest", bs: "top", bf: 0.5, ca: "1", cb: "0..*", name: "classifies", seg: 0 },
    { a: "ModelVersion", as: "bottom", af: 0.5, b: "MatchRecommendation", bs: "top", bf: 0.5, ca: "1", cb: "0..*", name: "produces" },
    { a: "Asset", as: "right", af: { abs: 440 }, b: "MatchRecommendation", bs: "left", bf: { abs: 560 }, ca: "1", cb: "0..*", name: "is matched in", seg: 1, rot: true },
    { a: "ResourceRequest", as: "left", af: { abs: 380 }, b: "MatchRecommendation", bs: "right", bf: { abs: 560 }, ca: "1", cb: "0..*", name: "receives", seg: 1, rot: true },
    { a: "Asset", as: "bottom", af: 0.8, b: "Transfer", bs: "left", bf: { abs: 900 }, ca: "1", cb: "0..*", name: "is moved by", seg: 0 },
    { a: "ResourceRequest", as: "bottom", af: 0.2, b: "Transfer", bs: "right", bf: { abs: 900 }, ca: "1", cb: "0..*", name: "is fulfilled by", seg: 0 },
    { a: "Reservation", as: "top", af: 0.5, b: "Transfer", bs: "bottom", bf: 0.5, ca: "1", cb: "0..1", name: "becomes" },
    { a: "Asset", as: "bottom", af: 0.3, b: "Listing", bs: "top", bf: 0.3, ca: "1", cb: "0..*", name: "is offered in" },
    { a: "Listing", as: "right", af: { abs: 1215 }, b: "Reservation", bs: "left", bf: { abs: 1215 }, ca: "1", cb: "0..*", name: "is held by" },
    { a: "ResourceRequest", as: "bottom", af: 0.7, b: "Reservation", bs: "right", bf: { abs: 1215 }, ca: "1", cb: "0..*", name: "places", seg: 0 },
  ]);
}

// ---------- Figure 8.4: approvals, maintenance and end of life ----------
{
  const R = ref("ResourceRequest", C1, 30, "requestId");
  const Ap = box("Approval", C2, 30, ["PK approvalId", "FK approverId", "FK requestId", "FK listingId", "FK transferId", "FK maintenanceId", "FK endOfLifeId", "stage", "decision", "status"]);
  const L = ref("Listing", C3, 30, "listingId");
  const MR = box("MaintenanceRecord", C1, 400, ["PK maintenanceId", "FK assetId", "FK inspectionId", "estimatedCost", "actualCost", "conditionAfter", "status"]);
  const T = ref("Transfer", C2, 400, "transferId");
  const EL = box("EndOfLifeAction", C3, 400, ["PK endOfLifeId", "FK assetId", "action", "quantity", "destination", "status"]);
  const SI = box("SustainabilityImpact", C2, 660, ["PK impactId", "FK transferId", "FK maintenanceId", "FK endOfLifeId", "wasteDivertedKg", "avoidedPurchaseAED", "co2eLowKg", "co2eHighKg", "dataStatus"]);
  const I = box("Inspection", C1, 1010, ["PK inspectionId", "FK assetId", "FK inspectorId", "inspectedOn", "conditionFound", "safeToUse"]);
  const A = ref("Asset", C2, 1010, "assetId");
  const sib = bottom(SI) + 42;
  svg("erd-approvals-lifecycle.svg", 930, bottom(I) + 25, [R, Ap, L, MR, T, EL, SI, I, A], [
    { a: "ResourceRequest", as: "right", af: { abs: 80 }, b: "Approval", bs: "left", bf: { abs: 80 }, ca: "0..1", cb: "0..*", name: "needs" },
    { a: "Listing", as: "left", af: { abs: 80 }, b: "Approval", bs: "right", bf: { abs: 80 }, ca: "0..1", cb: "0..*", name: "needs" },
    { a: "Transfer", as: "top", af: 0.5, b: "Approval", bs: "bottom", bf: 0.5, ca: "0..1", cb: "0..*", name: "needs" },
    { a: "MaintenanceRecord", as: "top", af: 0.5, b: "Approval", bs: "bottom", bf: 0.15, mid: 355, ca: "0..1", cb: "0..*", name: "needs", seg: 1 },
    { a: "EndOfLifeAction", as: "top", af: 0.5, b: "Approval", bs: "bottom", bf: 0.85, mid: 355, ca: "0..1", cb: "0..*", name: "needs", seg: 1 },
    { a: "Transfer", as: "bottom", af: 0.5, b: "SustainabilityImpact", bs: "top", bf: 0.5, ca: "0..1", cb: "0..1", name: "creates" },
    { a: "MaintenanceRecord", as: "bottom", af: 0.8, b: "SustainabilityImpact", bs: "left", bf: { abs: 770 }, ca: "0..1", cb: "0..1", name: "creates", seg: 0 },
    { a: "EndOfLifeAction", as: "bottom", af: 0.2, b: "SustainabilityImpact", bs: "right", bf: { abs: 770 }, ca: "0..1", cb: "0..1", name: "creates", seg: 0 },
    { a: "Inspection", as: "top", af: 0.2, b: "MaintenanceRecord", bs: "bottom", bf: 0.2, ca: "0..1", cb: "0..*", name: "leads to" },
    { a: "Asset", as: "top", af: 0.2, b: "MaintenanceRecord", bs: "bottom", bf: 0.5, mid: sib, ca: "1", cb: "0..*", name: "has", seg: 1 },
    { a: "Asset", as: "top", af: 0.8, b: "EndOfLifeAction", bs: "bottom", bf: 0.8, mid: sib, ca: "1", cb: "0..*", name: "ends with", seg: 1 },
    { a: "Asset", as: "left", af: { abs: 1050 }, b: "Inspection", bs: "right", bf: { abs: 1050 }, ca: "1", cb: "0..*", name: "checks" },
  ]);
}

// ---------- Figure 8.5: AI suggestions, attachments and transfer details ----------
{
  const MV = ref("ModelVersion", C1, 60, "modelVersionId");
  const AS = box("AiSuggestion", C2, 30, ["PK suggestionId", "FK modelVersionId", "FK assetId", "task", "suggestion", "confidence", "explanation", "userResponse", "createdAt"]);
  const D = ref("Department", C3, 60, "departmentId");
  const A = ref("Asset", C1, 380, "assetId");
  const AT = box("Attachment", C2, 350, ["PK attachmentId", "FK assetId", "FK transferId", "FK inspectionId", "FK maintenanceId", "FK endOfLifeId", "fileName", "fileType", "sizeKB", "storageKey"]);
  const T = ref("Transfer", C3, 380, "transferId");
  const I = ref("Inspection", C1, 760, "inspectionId");
  const MR = ref("MaintenanceRecord", C2, 760, "maintenanceId");
  const EL = ref("EndOfLifeAction", C3, 760, "endOfLifeId");
  const U = ref("User", C1, 910, "userId");
  const gap1 = bottom(AS) + 22, gap2 = bottom(AT) + 40;
  svg("erd-ai-attachments.svg", 990, bottom(U) + 25, [MV, AS, D, A, AT, T, I, MR, EL, U], [
    { a: "ModelVersion", as: "right", af: { abs: 95 }, b: "AiSuggestion", bs: "left", bf: { abs: 95 }, ca: "1", cb: "0..*", name: "produces" },
    { a: "Asset", as: "top", af: 0.8, b: "AiSuggestion", bs: "bottom", bf: 0.15, mid: gap1, ca: "0..1", cb: "0..*", name: "gets", seg: 1 },
    { a: "Asset", as: "right", af: { abs: 410 }, b: "Attachment", bs: "left", bf: { abs: 410 }, ca: "0..1", cb: "0..*", name: "has" },
    { a: "Transfer", as: "left", af: { abs: 410 }, b: "Attachment", bs: "right", bf: { abs: 410 }, ca: "0..1", cb: "0..*", name: "has" },
    { a: "MaintenanceRecord", as: "top", af: 0.5, b: "Attachment", bs: "bottom", bf: 0.5, ca: "0..1", cb: "0..*", name: "has" },
    { a: "Inspection", as: "top", af: 0.8, b: "Attachment", bs: "bottom", bf: 0.15, mid: gap2, ca: "0..1", cb: "0..*", name: "has", seg: 1 },
    { a: "EndOfLifeAction", as: "top", af: 0.2, b: "Attachment", bs: "bottom", bf: 0.85, mid: gap2, ca: "0..1", cb: "0..*", name: "has", seg: 1 },
    { a: "Department", as: "bottom", af: 0.25, b: "Transfer", bs: "top", bf: 0.25, ca: "1", cb: "0..*", name: "releases" },
    { a: "Department", as: "bottom", af: 0.75, b: "Transfer", bs: "top", bf: 0.75, ca: "1", cb: "0..*", name: "receives" },
    { a: "User", as: "top", af: 0.5, b: "Inspection", bs: "bottom", bf: 0.5, ca: "1", cb: "0..*", name: "inspects" },
    { a: "User", as: "right", af: 0.5, b: "Transfer", bs: "right", bf: 0.5, mid: 960, ca: "1", cb: "0..*", name: "receives as custodian", seg: 0 },
  ]);
}
