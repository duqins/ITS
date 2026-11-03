# Phase 4 and 5: Design Document

Architecture (Phase 4) and detailed design (Phase 5) for Dawra Campus. Worth 20% of the project.

## Who writes what

Each file in `sections/` has one owner, shown in the file name. Write only in your own files.

The section numbers 1 to 7 come from the Phase 4 lab slides (slide 23), so the grader can find each part. Sections 8 to 12 are Phase 5 and may change after the Phase 5 lab.

| Section | File | Owner |
| --- | --- | --- |
| Title page | `00-sultan-title.md` | Sultan |
| Introduction and references (no number) | `00a-sultan-introduction.md` | Sultan |
| 1 Context diagram | `01-sultan-context-diagram.md` | Sultan |
| 2 Data-flow diagrams (Level 1, Level 2, balancing table) | `02-sultan-data-flow-diagrams.md` | Sultan |
| 3 Architecture (decision record, architecture view) | `03-ghaith-architecture.md` | **Ghaith** |
| 4 AI services | `04-ghaith-ai-services.md` | **Ghaith** |
| 5 Human approval points | `05-ghaith-human-approval.md` | **Ghaith** |
| 6 Security (access matrix, audit log, storage, backup and restore) | `06-sultan-security.md` | Sultan |
| 7 Mockups (the eight screens) | `07-zayed-mockups.md` | **Zayed** |
| 8 Data model and ER diagram | `08-sultan-data-model.md` | Sultan |
| 9 Use-case, sequence and activity diagrams | `09-zayed-use-case-sequence-activity.md` | **Zayed** |
| 10 Class and state diagrams | `10-sultan-class-and-state.md` | Sultan |
| 11 Component, deployment and AI design | `11-ghaith-components-deployment-ai.md` | **Ghaith** |
| 12 Sustainability calculations | `12-sultan-sustainability-calculations.md` | Sultan |
| Appendix A Team contributions and AI use | `13-sultan-appendix.md` | Sultan |

## Diagrams

- Put images in `images/` as PNG and add them with `![Figure 3.1 Caption](images/file.png)`. Number figures by section (Figure 3.1, 3.2, and so on).
- Use the entity names from the ER diagram in section 8 (for example ResourceRequest, MatchRecommendation).
- The diagrams in sections 1, 2, 8 and 10 are SVG files in `images/`. They are drawn by the scripts in `diagrams/` (for example `er-diagrams.js`) and turned into PNG by `diagrams/render-svg.ps1`.

## Build the Word file

From the repository root:

```
npm run build:phase45
```

This writes `docs/phase45/Dawra_Campus_Phase4-5_Design_Document.docx`.
