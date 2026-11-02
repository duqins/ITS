# Zayed's Phase 4/5 static mockups

Open [index.html](index.html) directly in a browser. The preview is self-contained and works offline; keep its HTML, JavaScript, stylesheet and `assets/` folder together. No server or package installation is needed to view it.

Use **Screen** to switch among the eight required UI IDs. UI-13 has two views for the dashboard and report headings:

- [Sustainability dashboard](index.html?screen=UI-13&view=dashboard)
- [Report draft](index.html?screen=UI-13&view=report)

The **AI state** control selects Available, Low or unavailable confidence, or Unavailable. Direct links also accept `state=normal`, `state=low` or `state=down`, for example `index.html?screen=UI-13&view=report&state=down`. These are scripted examples, not live AI responses. Ordinary edited form values persist only within the current page session. The applied UI-13 report scope persists in the URL across dashboard/report links, AI states and page reloads.

UI-13 provides **From**, **To** and **Department** filters. **Apply filters** updates both views; an invalid date range is rejected. Only snapshot S06, covering 1–31 October 2026 for Engineering and Computing together, contains synthetic figures and AI text. Other scopes show an explicit empty state. **Reset to example** restores S06. Direct links accept ISO dates in `from` and `to`, and `department=both`, `department=engineering` or `department=computing`; for example [the S06 report](index.html?screen=UI-13&view=report&from=2026-10-01&to=2026-10-31&department=both).

Both UI-13 views use the same two fulfilled requests, each for one 24-inch Dell P2422H monitor. The synthetic replacement price is AED 345 each: AED 690 avoided less AED 180 related costs gives AED 510 net savings. The AED 250 used-monitor value is separate from the replacement price. Carbon factors of 128–327 kg CO2e per monitor give 256–654 kg gross; subtracting a synthetic 0.10 kg fan mass × the F1 IT material proxy of 24.86548 kg CO2e/kg (2.486548 kg CO2e) gives about 253.5–651.5 kg CO2e net. The mass and proxy are assumptions, not measurements; same-building collection has no van trip. Factors follow Section 12 Tables 12.1–12.3 at `origin/phase45/sultan`, commit `7691fcf85de7eb3c5625e7688562f6a9a1856230`; this working branch's Section 12 is still a placeholder.

## Evidence and boundaries

The preview preserves the established navy/teal palette, self-hosted Manrope, supplied logo, grouped forms, visible evidence, text status indicators and responsive workspace. The UI-13 report view uses the same patterns and synthetic S06 totals. The included [styles.css](styles.css) remains the visual authority, and all runtime assets are kept in this folder. The print capture adjustments are export-only; the normal offline preview remains responsive.

Requirement IDs and human/fallback boundaries follow the existing [UI SRS](../../../phase3/sections/03a-zayed-user-interfaces.md) and [AI SRS](../../../phase3/sections/04d-ghaith-ai-features.md). AI suggestions and report drafts require human review; compatibility remains separate from confidence, and missing inputs remain explicit. Unavailable examples retain conventional forms, search or source totals. The 15-second fallback deadline is a product requirement, not a measured guarantee of this preview.

The UI-07 fallback alternative and workflow details omit AI scores. The UI-13 report retains its source table without repeating the same source records in a second group.

All records, people, figures and AI outputs are synthetic. Controls illustrate selected browser interactions and change no business records. There is no backend, authentication, database or AI service. Production authorisation, audit trails, workflow enforcement, fallback timing and WCAG 2.2 AA conformance require implementation and testing beyond this static artifact. Desktop/mobile and low/unavailable-state review found no blocking defects in the added UI-13 views; that is a preview review, not a production conformance claim.

## Asset provenance

- [assets/dawra-campus-logo.png](assets/dawra-campus-logo.png) is byte-identical to the original [Dawra Campus logo concept](../../../phase2/progress/2026-09-22/assets/Dawra_Campus_Logo_Concept.png). CSS scales and positions the bitmap; it has not been recoloured or redrawn. Both SHA-256 hashes are `fc49865a258d0e5d2be05590895ade610feb20bf709eaa1179633cd07191be07`.
- [assets/Manrope.ttf](assets/Manrope.ttf) is the bundled variable font from the [Google Fonts Manrope source](https://github.com/google/fonts/tree/main/ofl/manrope), with weights 200–800 and an Arial/sans-serif fallback. Its licence is included in [assets/Manrope-OFL.txt](assets/Manrope-OFL.txt).

## Rerender the figures

From the repository root, with Node.js, Playwright and Google Chrome available:

```powershell
# Required for check-review-fixes.cjs; optional for capture.cjs.
$env:DAWRA_NODE_MODULES = 'C:\path\to\node_modules'
# Optional: an existing directory for normal overviews, UI-13 states and checks.
$env:DAWRA_QA_DIR = 'C:\path\to\qa-output'
node docs/phase45/mockups/zayed/capture.cjs
node docs/phase45/mockups/zayed/check-review-fixes.cjs
```

Omit either environment variable when unnecessary. `DAWRA_NODE_MODULES` must contain the `playwright` package; without it, normal Node package resolution applies. Create `DAWRA_QA_DIR` before running if used. [capture.cjs](capture.cjs) writes eighteen `-top.png`/`-bottom.png` print halves across the eight headings to `docs/phase45/images/` for Section 7. The nine obsolete whole-screen repository PNGs have been retired. With `DAWRA_QA_DIR` set, the script saves nine full normal overviews there as `-normal.png` after the full-height viewport settles, alongside the extra UI-13 down/low/mobile captures and `browser-checks.json`. It checks browser errors and page overflow at 1180px and 390px; the JSON also includes print geometry and minimum type size for all nine views.

For a targeted recapture, set `DAWRA_CAPTURE_SCREENS` to comma-separated UI IDs, for example `$env:DAWRA_CAPTURE_SCREENS = 'UI-07,UI-13'`. UI-13 captures both views. A partial run merges its checks into the QA directory's existing `browser-checks.json`, preserving the other cases. Omit this variable for a complete run.

[print-capture.cjs](print-capture.cjs) applies [print-capture.css](print-capture.css) at an export width of 760 CSS px, hides the sidebar and wraps form values without truncation. It clears a horizontal seam between text lines, then captures each half with a viewport tall enough for the full page. A minimum of 15 CSS px yields about 9.18 pt at the report's 465 pt image width. Capture fails if a half exceeds 1030 CSS px tall or its printed type falls below 9 pt.

[check-review-fixes.cjs](check-review-fixes.cjs) checks that the fallback alternative and workflow details hide AI scores, and verifies filters, empty states, scope persistence, reset and invalid date ranges. Set `DAWRA_NODE_MODULES` to the directory containing Playwright for this check.
