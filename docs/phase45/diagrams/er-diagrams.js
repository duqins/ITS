// Generates the Phase 4-5 ER diagrams as SVG files.
// Usage from the repository root: node docs/phase45/diagrams/er-diagrams.js docs/phase45/images
const fs = require("fs");
const path = require("path");
const outDir = process.argv[2];

const W = 230, HEAD = 32, ROW = 21, PADB = 8;
const FONT = "Segoe UI, Arial, sans-serif";

function box(name, x, y, rows, opts = {}) {
  const h = HEAD + rows.length * ROW + PADB;
  return { name, x, y, w: opts.w || W, h, rows, ref: !!opts.ref };
}

function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

function drawBox(b) {
  const stroke = b.ref ? "#9a9a9a" : "#333";
  const dash = b.ref ? ' stroke-dasharray="6 4"' : "";
  const headFill = b.ref ? "#f4f4f4" : "#e3ecf7";
  const text = b.ref ? "#777" : "#111";
  let s = `<g>`;
  s += `<rect x="${b.x}" y="${b.y}" width="${b.w}" height="${b.h}" rx="3" fill="#fff" stroke="${stroke}" stroke-width="1.5"${dash}/>`;
  s += `<rect x="${b.x}" y="${b.y}" width="${b.w}" height="${HEAD}" rx="3" fill="${headFill}" stroke="${stroke}" stroke-width="1.5"${dash}/>`;
  s += `<text x="${b.x + b.w / 2}" y="${b.y + 21}" text-anchor="middle" font-family="${FONT}" font-size="16" font-weight="700" fill="${text}">${esc(b.name)}</text>`;
  b.rows.forEach((r, i) => {
    const yy = b.y + HEAD + 16 + i * ROW;
    const m = r.match(/^(PK|FK) (.*)$/);
    if (m) {
      s += `<text x="${b.x + 10}" y="${yy}" font-family="${FONT}" font-size="14" fill="${text}"><tspan font-weight="700">${m[1]}</tspan> ${esc(m[2])}</text>`;
    } else {
      s += `<text x="${b.x + 10}" y="${yy}" font-family="${FONT}" font-size="14" fill="${text}">${esc(r)}</text>`;
    }
  });
  return s + `</g>`;
}

// side point: side is "top" | "bottom" | "left" | "right"; at is the x (top/bottom) or y (left/right) coordinate
function pt(b, side, at) {
  if (side === "top") return { x: at, y: b.y };
  if (side === "bottom") return { x: at, y: b.y + b.h };
  if (side === "left") return { x: b.x, y: at };
  return { x: b.x + b.w, y: at };
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

// label near an end point: placed along the line, slightly to the side
function endLabel(p, side, text, below) {
  const d = 8, along = 6;
  let x = p.x, y = p.y, anchor = "start";
  if (side === "right") { x = p.x + along; y = below ? p.y + 18 : p.y - d; anchor = "start"; }
  if (side === "left") { x = p.x - along; y = below ? p.y + 18 : p.y - d; anchor = "end"; }
  if (side === "top") { x = p.x + d; y = p.y - along - 2; anchor = "start"; }
  if (side === "bottom") { x = p.x + d; y = p.y + along + 12; anchor = "start"; }
  return `<text x="${x}" y="${y}" text-anchor="${anchor}" font-family="${FONT}" font-size="14" font-weight="600" fill="#1F3864">${esc(text)}</text>`;
}

function drawEdge(boxes, e) {
  const A = boxes[e.a], B = boxes[e.b];
  const p1 = pt(A, e.as, e.aat), p2 = pt(B, e.bs, e.bat);
  const pts = route(p1, e.as, p2, e.bs, e.mid);
  let s = `<polyline points="${pts.map((p) => `${p.x},${p.y}`).join(" ")}" fill="none" stroke="#333" stroke-width="1.5"/>`;
  s += endLabel(p1, e.as, e.ca, e.belowA) + endLabel(p2, e.bs, e.cb, e.belowB);
  if (e.label) {
    // put the role label on the longest segment
    let best = 0, bi = 0;
    for (let i = 0; i < pts.length - 1; i++) {
      const len = Math.abs(pts[i + 1].x - pts[i].x) + Math.abs(pts[i + 1].y - pts[i].y);
      if (len > best) { best = len; bi = i; }
    }
    const q1 = pts[bi], q2 = pts[bi + 1];
    const mx = (q1.x + q2.x) / 2, my = (q1.y + q2.y) / 2;
    const vertical = q1.x === q2.x;
    const lx = vertical ? mx + 6 : mx, ly = vertical ? my + 4 : my + 17;
    s += `<text x="${lx}" y="${ly}" text-anchor="${vertical ? "start" : "middle"}" font-family="${FONT}" font-size="13" font-style="italic" fill="#555">${esc(e.label)}</text>`;
  }
  return s;
}

function svg(file, width, height, boxList, edges) {
  const boxes = Object.fromEntries(boxList.map((b) => [b.name, b]));
  let body = edges.map((e) => drawEdge(boxes, e)).join("\n") + "\n" + boxList.map(drawBox).join("\n");
  const out = `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">\n<rect width="100%" height="100%" fill="#fff"/>\n${body}\n</svg>\n`;
  fs.writeFileSync(path.join(outDir, file), out);
  console.log("wrote " + file);
  return boxes;
}

const C1 = 40, C2 = 360, C3 = 680;
const cx = (c, f) => c + W * f; // x position along a box in column c

// ---------- Figure 4.1: core ER diagram from the lab ----------
{
  const D = box("Department", C1, 40, ["PK departmentId", "name"]);
  const U = box("User", C2, 40, ["PK userId", "FK departmentId", "name"]);
  const R = box("ResourceRequest", C3, 40, ["PK requestId", "FK requesterId", "quantity", "status"]);
  const A = box("Asset", C1, 330, ["PK assetId", "FK ownerDepartmentId", "name", "condition", "status"]);
  const T = box("Transfer", C3, 330, ["PK transferId", "FK assetId", "FK requestId", "FK approverId", "status"]);
  const M = box("MatchRecommendation", C2, 560, ["PK matchId", "FK assetId", "FK requestId", "FK modelVersionId", "score", "explanation"]);
  svg("erd-core.svg", 990, 760, [D, U, R, A, T, M], [
    { a: "Department", as: "right", aat: 100, b: "User", bs: "left", bat: 100, ca: "1", cb: "0..*" },
    { a: "User", as: "right", aat: 100, b: "ResourceRequest", bs: "left", bat: 100, ca: "1", cb: "0..*", label: "requester" },
    { a: "Department", as: "bottom", aat: cx(C1, 0.5), b: "Asset", bs: "top", bat: cx(C1, 0.5), ca: "1", cb: "0..*", label: "owner" },
    { a: "ResourceRequest", as: "bottom", aat: cx(C3, 0.7), b: "Transfer", bs: "top", bat: cx(C3, 0.7), ca: "1", cb: "0..*" },
    { a: "User", as: "bottom", aat: cx(C2, 0.5), b: "Transfer", bs: "top", bat: cx(C3, 0.25), mid: 240, ca: "0..1", cb: "0..*", label: "final approver" },
    { a: "Asset", as: "right", aat: 400, b: "Transfer", bs: "left", bat: 400, ca: "1", cb: "0..*" },
    { a: "Asset", as: "bottom", aat: cx(C1, 0.5), b: "MatchRecommendation", bs: "left", bat: 640, ca: "1", cb: "0..*" },
    { a: "MatchRecommendation", as: "right", aat: 640, b: "ResourceRequest", bs: "right", bat: 120, mid: 950, ca: "0..*", cb: "1" },
  ]);
}

// ---------- Figure 4.2: users, roles and access (4 columns) ----------
{
  const K1 = 30, K2 = 290, K3 = 550, K4 = 850, WW = 210;
  const kx = (c, f) => c + WW * f;
  const Role = box("Role", K1, 40, ["PK roleId", "name"], { w: WW });
  const UR = box("UserRole", K2, 40, ["PK userRoleId", "FK userId", "FK roleId", "FK departmentId", "status"], { w: WW });
  const D = box("Department", K3, 40, ["PK departmentId", "name", "code"], { w: WW });
  const A = box("Asset", K4, 40, ["PK assetId"], { w: WW, ref: true });
  const N = box("Notification", K1, 280, ["PK notificationId", "FK userId", "message", "sentAt", "readAt"], { w: WW });
  const U = box("User", K2, 280, ["PK userId", "FK departmentId", "name", "email", "accountStatus"], { w: WW });
  const AL = box("AuditLog", K1, 560, ["PK auditId", "FK userId", "action", "recordType", "recordId", "createdAt"], { w: WW });
  const R = box("ResourceRequest", K2, 560, ["PK requestId"], { w: WW, ref: true });
  const T = box("Transfer", K3, 560, ["PK transferId"], { w: WW, ref: true });
  const Ap = box("Approval", K4, 560, ["PK approvalId"], { w: WW, ref: true });
  svg("erd-users.svg", 1100, 760, [Role, UR, D, A, N, U, AL, R, T, Ap], [
    { a: "Role", as: "right", aat: 90, b: "UserRole", bs: "left", bat: 90, ca: "1", cb: "0..*" },
    { a: "Department", as: "left", aat: 90, b: "UserRole", bs: "right", bat: 90, ca: "1", cb: "0..*" },
    { a: "User", as: "top", aat: kx(K2, 0.5), b: "UserRole", bs: "bottom", bat: kx(K2, 0.5), ca: "1", cb: "0..*" },
    { a: "Department", as: "bottom", aat: kx(K3, 0.3), b: "User", bs: "right", bat: 320, ca: "1", cb: "0..*" },
    { a: "Department", as: "right", aat: 90, b: "Asset", bs: "left", bat: 90, ca: "1", cb: "0..*", label: "owner" },
    { a: "User", as: "right", aat: 380, b: "Asset", bs: "bottom", bat: kx(K4, 0.5), ca: "1", cb: "0..*", label: "custodian" },
    { a: "User", as: "left", aat: 330, b: "Notification", bs: "right", bat: 330, ca: "1", cb: "0..*" },
    { a: "User", as: "left", aat: 400, b: "AuditLog", bs: "right", bat: 610, mid: 265, ca: "0..1", cb: "0..*", belowB: true },
    { a: "User", as: "bottom", aat: kx(K2, 0.35), b: "ResourceRequest", bs: "top", bat: kx(K2, 0.35), ca: "1", cb: "0..*", label: "requester" },
    { a: "User", as: "bottom", aat: kx(K2, 0.7), b: "Transfer", bs: "top", bat: kx(K3, 0.35), mid: 510, ca: "0..1", cb: "0..*", label: "final approver" },
    { a: "User", as: "bottom", aat: kx(K2, 0.9), b: "Approval", bs: "top", bat: kx(K4, 0.35), mid: 470, ca: "0..1", cb: "0..*", label: "approver" },
  ]);
}

// ---------- Figure 4.3: assets, requests and matching ----------
{
  const Cat = box("Category", C2, 40, ["PK categoryId", "name", "unit", "emissionFactor"]);
  const A = box("Asset", C1, 250, ["PK assetId", "FK ownerDepartmentId", "FK categoryId", "FK custodianId", "name", "condition", "status", "quantity"]);
  const MV = box("ModelVersion", C2, 250, ["PK modelVersionId", "task", "modelName", "version"]);
  const R = box("ResourceRequest", C3, 250, ["PK requestId", "FK requesterId", "FK categoryId", "quantity", "requiredBy", "status"]);
  const M = box("MatchRecommendation", C2, 460, ["PK matchId", "FK assetId", "FK requestId", "FK modelVersionId", "score", "confidence", "explanation"]);
  const T = box("Transfer", C2, 730, ["PK transferId", "FK assetId", "FK requestId", "FK reservationId", "FK approverId", "quantity", "status"]);
  const L = box("Listing", C1, 1000, ["PK listingId", "FK assetId", "quantity", "availableFrom", "status"]);
  const Res = box("Reservation", C2, 1000, ["PK reservationId", "FK requestId", "FK listingId", "quantity", "expiresAt", "status"]);
  svg("erd-assets-requests.svg", 990, 1220, [Cat, A, MV, R, M, T, L, Res], [
    { a: "Category", as: "left", aat: 90, b: "Asset", bs: "top", bat: cx(C1, 0.5), ca: "1", cb: "0..*" },
    { a: "Category", as: "right", aat: 90, b: "ResourceRequest", bs: "top", bat: cx(C3, 0.5), ca: "1", cb: "0..*" },
    { a: "ModelVersion", as: "bottom", aat: cx(C2, 0.5), b: "MatchRecommendation", bs: "top", bat: cx(C2, 0.5), ca: "1", cb: "0..*" },
    { a: "Asset", as: "right", aat: 430, b: "MatchRecommendation", bs: "left", bat: 520, ca: "1", cb: "0..*" },
    { a: "ResourceRequest", as: "left", aat: 400, b: "MatchRecommendation", bs: "right", bat: 540, ca: "1", cb: "0..*" },
    { a: "Asset", as: "bottom", aat: cx(C1, 0.8), b: "Transfer", bs: "left", bat: 810, ca: "1", cb: "0..*" },
    { a: "ResourceRequest", as: "bottom", aat: cx(C3, 0.2), b: "Transfer", bs: "right", bat: 810, ca: "1", cb: "0..*" },
    { a: "Reservation", as: "top", aat: cx(C2, 0.5), b: "Transfer", bs: "bottom", bat: cx(C2, 0.5), ca: "1", cb: "0..1" },
    { a: "Asset", as: "bottom", aat: cx(C1, 0.3), b: "Listing", bs: "top", bat: cx(C1, 0.3), ca: "1", cb: "0..*" },
    { a: "Listing", as: "right", aat: 1060, b: "Reservation", bs: "left", bat: 1060, ca: "1", cb: "0..*" },
    { a: "ResourceRequest", as: "bottom", aat: cx(C3, 0.7), b: "Reservation", bs: "right", bat: 1060, ca: "1", cb: "0..*" },
  ]);
}

// ---------- Figure 4.4: approvals, maintenance and end of life ----------
{
  const R = box("ResourceRequest", C1, 40, ["PK requestId"], { ref: true });
  const Ap = box("Approval", C2, 40, ["PK approvalId", "FK approverId", "FK requestId", "FK listingId", "FK transferId", "FK maintenanceId", "FK endOfLifeId", "stage", "decision", "status"]);
  const L = box("Listing", C3, 40, ["PK listingId"], { ref: true });
  const MR = box("MaintenanceRecord", C1, 380, ["PK maintenanceId", "FK assetId", "FK inspectionId", "estimatedCost", "actualCost", "status"]);
  const T = box("Transfer", C2, 380, ["PK transferId"], { ref: true });
  const EL = box("EndOfLifeAction", C3, 380, ["PK endOfLifeId", "FK assetId", "action", "quantity", "destination", "status"]);
  const SI = box("SustainabilityImpact", C2, 600, ["PK impactId", "FK transferId", "FK maintenanceId", "FK endOfLifeId", "wasteDivertedKg", "avoidedPurchaseAED", "co2eSavedKg"]);
  const I = box("Inspection", C1, 900, ["PK inspectionId", "FK assetId", "inspectedOn", "conditionFound", "safeToUse"]);
  const A = box("Asset", C2, 900, ["PK assetId"], { ref: true });
  svg("erd-approvals-lifecycle.svg", 990, 1070, [R, Ap, L, MR, T, EL, SI, I, A], [
    { a: "ResourceRequest", as: "right", aat: 90, b: "Approval", bs: "left", bat: 90, ca: "0..1", cb: "0..*" },
    { a: "Listing", as: "left", aat: 90, b: "Approval", bs: "right", bat: 90, ca: "0..1", cb: "0..*" },
    { a: "Transfer", as: "top", aat: cx(C2, 0.5), b: "Approval", bs: "bottom", bat: cx(C2, 0.5), ca: "0..1", cb: "0..*" },
    { a: "MaintenanceRecord", as: "top", aat: cx(C1, 0.5), b: "Approval", bs: "bottom", bat: cx(C2, 0.15), mid: 330, ca: "0..1", cb: "0..*" },
    { a: "EndOfLifeAction", as: "top", aat: cx(C3, 0.5), b: "Approval", bs: "bottom", bat: cx(C2, 0.85), mid: 330, ca: "0..1", cb: "0..*" },
    { a: "Transfer", as: "bottom", aat: cx(C2, 0.5), b: "SustainabilityImpact", bs: "top", bat: cx(C2, 0.5), ca: "0..1", cb: "0..1" },
    { a: "MaintenanceRecord", as: "bottom", aat: cx(C1, 0.8), b: "SustainabilityImpact", bs: "left", bat: 690, ca: "0..1", cb: "0..1" },
    { a: "EndOfLifeAction", as: "bottom", aat: cx(C3, 0.2), b: "SustainabilityImpact", bs: "right", bat: 690, ca: "0..1", cb: "0..1" },
    { a: "Inspection", as: "top", aat: cx(C1, 0.2), b: "MaintenanceRecord", bs: "bottom", bat: cx(C1, 0.2), ca: "0..1", cb: "0..*" },
    { a: "Asset", as: "top", aat: cx(C2, 0.2), b: "MaintenanceRecord", bs: "bottom", bat: cx(C1, 0.5), mid: 860, ca: "1", cb: "0..*" },
    { a: "Asset", as: "top", aat: cx(C2, 0.8), b: "EndOfLifeAction", bs: "bottom", bat: cx(C3, 0.8), mid: 860, ca: "1", cb: "0..*" },
    { a: "Asset", as: "left", aat: 950, b: "Inspection", bs: "right", bat: 950, ca: "1", cb: "0..*" },
  ]);
}
