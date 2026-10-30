# Zayed diagram and section sources

This folder supports Zayed's Section 7 mockups and Section 9 diagrams. It does not generate or edit teammates' sections.

- `design-data.json` contains the synthetic screen examples, plain-language explanations and approved sequence messages.
- `build_sections.py` writes only `sections/07-zayed-mockups.md` and `sections/09-zayed-use-case-sequence-activity.md`, placing explanations beside the shorter sequence parts and grouping the activity descriptions.
- `build_activities.py` regenerates the complete activity sources before the print parts are built.
- `build_figures.py` regenerates the complete canonical sequence SVG and draw.io sources alongside the enlarged sequence parts and activity parts used by the portrait Word build. Each pair is one diagram, with the same message numbers or connector A continuing into the second part.
- `drawing.py` draws editable SVG and draw.io shapes. `render_figures.cjs` exports the print parts to PNG.
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

The Node exporter uses `sharp`. Set `DAWRA_NODE_MODULES` to the bundled Node package directory when using the Codex runtime. The offline mockup preview and its capture instructions are in `docs/phase45/mockups/zayed/`.
