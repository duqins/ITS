# Phase 1 – Initial Plan and Requirement Gathering Document

The document is written in Markdown, one file per section, in `sections/`. Git merges text files cleanly, so everyone can edit their own sections at the same time without conflicts.

## Section ownership

| File | Section | Owner |
|---|---|---|
| `00-title.md` | Title page | Sultan |
| `01-introduction.md` | 1. Introduction | Sultan |
| `02-project-overview.md` | 2. Project Overview | Sultan |
| `03-stakeholder-analysis.md` | 3. Stakeholder Analysis | Zayed |
| `04-as-is-process.md` | 4. As-Is Process | Zayed |
| `05-requirements-gathering.md` | 5. Requirements Gathering | Zayed |
| `06-requirements-specification.md` | 6. Requirements Specification | Ghith |
| `07-success-criteria.md` | 7. Success Criteria | Ghith |
| `08-project-plan.md` | 8. Project Plan | Sultan |
| `09-classic-vs-ai.md` | 9. Classic vs AI | Ghith |
| `10-open-questions-references.md` | 10–11. Open questions, references | all |

All sections are complete for the Phase 1 submission. The section files remain the source of truth; each owner reviews any substantive change to their contribution.

## Editing

Open the `.md` file in VS Code (press `Ctrl+Shift+V` for a live preview). Plain text is a paragraph, `- ` starts a bullet, `**text**` is bold, and tables use `| pipes |`. Keep the `<!-- widths: ... -->` comment above a table if you change its columns.

## Generating the Word / PDF file

From the repository root, once:

```
npm install
```

Then whenever you want the `.docx`:

```
npm run build:phase1
```

This writes `Phase1_Initial_Plan_and_Requirements.docx` next to this file. Open it in Word, right-click the table of contents and choose **Update Field**, then **File → Save As → PDF** for the submission copy. The final Word submission file is explicitly included by `.gitignore`; other generated Word/PDF files remain ignored. Review the generated document, then commit the final file together with its source changes through your own GitHub account. The checked-in submission copy has its contents and page fields updated; rebuilds should be opened in Word and updated before submission.
