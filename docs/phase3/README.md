# Phase 3 – Software Requirements Specification (SRS)

Due: Tuesday 13 October 2026, 3:00 PM (Blackboard). Weight: 10%.

The document follows the course SRS template (project description appendix, pp. 13–19) and covers everything Phase 3 asks for on p. 8: actors and permissions, business rules and approval stages, asset/request/transfer/maintenance states, functional and non-functional requirements, AI and sustainability requirements, a use-case diagram with detailed use-case descriptions, and prioritisation.

## Who writes what

Each file in `sections/` has one owner. Write only your own files. The file name shows the owner.

| Section | File | Owner |
| --- | --- | --- |
| Title page, revision history | `00-sultan-title.md` | Sultan |
| 1 Introduction | `01-sultan-introduction.md` | Sultan |
| 2.1–2.2 Product perspective and functions | `02a-sultan-overall-description.md` | Sultan |
| 2.3 User classes, roles and permissions | `02b-zayed-user-classes.md` | **Zayed** |
| 2.4 Operating environment | `02c-ghaith-operating-environment.md` | **Ghaith** |
| 2.5–2.7 Constraints, user documentation, assumptions | `02d-sultan-constraints-assumptions.md` | Sultan |
| 3.1 User interfaces | `03a-zayed-user-interfaces.md` | **Zayed** |
| 3.2–3.4 Hardware, software and communication interfaces | `03b-ghaith-system-interfaces.md` | **Ghaith** |
| 4.1 Use-case model (diagram and descriptions) | `04a-zayed-use-case-model.md` | **Zayed** |
| 4.2 Record states | `04b-sultan-record-states.md` | Sultan |
| 4.3–4.16 Classic system features | `04c-sultan-classic-features.md` | Sultan |
| 4.17–4.23 AI features | `04d-ghaith-ai-features.md` | **Ghaith** |
| 5.1–5.4 Non-functional requirements | `05a-ghaith-nonfunctional.md` | **Ghaith** |
| 5.5 Business rules and approval stages | `05b-sultan-business-rules.md` | Sultan |
| 6 Sustainability, data, prioritisation, traceability | `06-sultan-other-requirements.md` | Sultan |
| Appendices: glossary, TBD list, AI use | `07-sultan-appendices.md` | Sultan |

Your file already has the headings and table columns. Grey `<!-- ... -->` comments explain what to write; they are never printed. Lines starting with `TODO` are not printed either. Delete them as you finish each part.

## Steps for each member

1. Get the project: `git fetch`
2. Make your branch from the Phase 3 setup: `git switch -c phase3/zayed origin/phase3/setup` (Ghaith uses `phase3/ghaith`).
3. Open your files in VS Code (`Ctrl+Shift+V` shows a preview) and write your parts.
4. After each finished part: `git add docs/phase3` then `git commit -m "docs(phase3): write use-case descriptions"`
5. Send it: `git push -u origin phase3/zayed`
6. On GitHub click **Compare & pull request**, target `main`, and ask a teammate to review.

Run one command at a time. PowerShell does not accept `&&`.

## Rules that keep the document consistent

- Use the requirement IDs already given in your file. Do not renumber other people's IDs.
- Write requirements as "The system shall …" using the EARS patterns from the Chapter 3 slides (slide 23): *When* (event), *While* (state), *If … then* (unwanted behaviour), *Where* (optional feature).
- Approval owners, states and business rules are defined once, in sections 4.2 and 5.5. Refer to them by ID (for example "BR-05", "TR-04") instead of writing different rules.
- Put images in `docs/phase3/images/` as PNG and insert them with `![Figure 1. Caption](images/file.png)`.
- Add any outside source you use to the References list in section 1.5 by telling Sultan, and keep the AI-use statement accurate (Appendix D).

## Build the Word file

From the repository root:

```
npm install
npm run build:phase3
```

This writes `docs/phase3/Dawra_Campus_Phase3_SRS.docx` and lists any `TODO` lines that are still open. Open it in Word, right-click the table of contents, choose **Update Field**, then save as PDF for Blackboard. Publishing on GitHub does not submit the assignment.
