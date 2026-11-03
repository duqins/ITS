# Zayed diagram and section sources

This folder supports Zayed's Section 7 mockups and Section 9 diagrams. It does not generate or edit teammates' sections.

- `design-data.json` contains the synthetic screen examples, plain-language explanations, approved sequence messages and shared UI-13 `snapshot` object. The snapshot records the two-monitor money and carbon calculations, including the synthetic fan mass and material proxy; see the [mockup README](../../mockups/zayed/README.md) for assumptions and Section 12 provenance.
- `build_sections.py` writes only `sections/07-zayed-mockups.md` and `sections/09-zayed-use-case-sequence-activity.md`, placing explanations beside the shorter sequence parts and grouping the activity descriptions. Section 7 pairs the print halves as Figures 7.1a/7.1b through 7.9a/7.9b, with Tables 7.1–7.9; Section 9 captions its role table as Table 9.1. The report view has its own fields heading and short notes. Generated sections omit the removed Sources/AI-use author block and report-guide or self-check sections.
- `build_activities.py` regenerates the complete activity sources before the print parts are built.
- `build_figures.py` regenerates the complete canonical sequence SVG and draw.io sources alongside the enlarged sequence parts and activity parts used by the portrait Word build. Each pair is one diagram, with the same message numbers or connector A continuing into the second part.
- `drawing.py` draws editable SVG and draw.io shapes without internal titles or author-ID footers; report captions identify each figure. `render_figures.cjs` exports the print parts to PNG.
- The complete sequence and activity `.drawio` files are retained alongside their SVG sources. Each sequence print part also has its own editable `.drawio` source.
- The use-case PNG, SVG and DOT are the original Phase 3 files. Keep their content unchanged unless a change is agreed.

From the repository root, using Python and Node with the required packages:

```
python docs/phase45/diagrams/zayed/build_activities.py
python docs/phase45/diagrams/zayed/build_figures.py
node docs/phase45/diagrams/zayed/render_figures.cjs
python docs/phase45/diagrams/zayed/build_sections.py
npm run build:phase45
```

The Node exporter uses `sharp`. Set `DAWRA_NODE_MODULES` to the bundled Node package directory when using the Codex runtime. Run the [mockup capture instructions](../../mockups/zayed/README.md#rerender-the-figures) before `build_sections.py` when regenerating Section 7's eighteen print halves. These halves replace the obsolete whole-screen repository PNGs; optional normal overviews belong in `DAWRA_QA_DIR`. The capture instructions also cover targeted UI recaptures and merged QA checks. The established navy/teal styling, supplied logo and Manrope remain governed by the mockup's `styles.css`; this export work does not replace the visual system.
