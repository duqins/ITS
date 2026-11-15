# Dawra Campus

**ITS: Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System**

COSC 336 Introduction to Software Engineering, Khalifa University, Fall 2026. Lab B2, Group 4.

Dawra (دورة) means "cycle". Departments register the furniture, computers and equipment they no longer need. Other departments find and request them, both sides approve, and the item moves to its new owner instead of the university buying a new one. A rule-based core runs the process. AI helps with classification, matching and reports, and a person always makes the decision.

## Team

| Member | Student ID | Primary role |
|---|---|---|
| Sultan Almheiri | 100065654 | Project lead / Scrum master, backend lead |
| Zayed Alfadli | 100064657 | Requirements, UX and QA lead |
| Ghaith Alhinaai | 100066185 | Architecture and AI integration lead |

## Project phases

| Phase | Deliverable | Where to find it |
|---|---|---|
| 1 | Initial plan and requirement gathering | [Word document](docs/phase1/Phase1_Initial_Plan_and_Requirements.docx), [team pitch](docs/phase1/presentation/ITS_Phase1_Team_Pitch.pptx), [sections](docs/phase1/README.md) |
| 2 | Feasibility study | [Word report](docs/phase2/final/Dawra_Campus_Phase2_Feasibility_Study.docx), [read on GitHub](docs/phase2/final/Dawra_Campus_Phase2_Feasibility_Study.md), [slides](docs/phase2/final/Dawra_Campus_Phase2_Presentation.pptx), [contributions and sources](docs/phase2/README.md) |
| 3 | Requirements document (SRS) | [PDF](docs/phase3/Dawra_Campus_Phase3_SRS.pdf), [Word](docs/phase3/Dawra_Campus_Phase3_SRS.docx), [slides](docs/phase3/presentation/Dawra_Campus_Phase3_Presentation.pptx), [sections and owners](docs/phase3/README.md) |
| 4 and 5 | Design document (architecture and detailed design) | [Sections, diagrams and mockups](docs/phase45/README.md) |
| 6 | Draft implementation: the working app | [`src/`](src/README.md) |
| 7 | Test cases | Coming next |
| 8 | Final project, presentation and demo | Coming next |

The course project description and the lab slides are in [`docs/reference/`](docs/reference/).

## The app (Phase 6)

A Django web app that follows our design: Python and Django, PostgreSQL on Neon, hosted on Render, with the Claude API for the AI features. It covers:

- **Core features C1 to C9:** sign-in with roles and server-side permission checks, asset registration with a second-person check, publishing and search, resource requests, approvals with holds and transfers, record states with a full history, the sustainability dashboard, notifications and reports.
- **AI features 1, 2 and 5:** suggesting an asset's category, condition and tags, ranking matching items for a request, and drafting the sustainability summary. Every AI result is a suggestion that a person accepts or rejects, and the app still works when the AI is unavailable.

Not part of this draft yet: maintenance and repair tracking, the end-of-life review, the campus assistant and sustainable-action advice.

To run it on your laptop, follow [`src/README.md`](src/README.md). All demo data is synthetic.

## Repository layout

```
.github/        Pull request template and the Phase 2 document check
docs/
  phase1/       Phase 1 plan and requirement gathering
  phase2/       Phase 2 feasibility study (final submission in final/)
  phase3/       Phase 3 requirements document (SRS)
  phase45/      Phase 4 and 5 design document
  reference/    Course project description and lab slides
scripts/        Check for the Phase 2 documents
src/            The Django app (Phase 6)
package.json    Builds the Word documents from the Markdown sections
```

Each document is written in Markdown, one file per section, under `docs/phaseN/sections/`. To rebuild a Word file, run `npm install` once, then `npm run build:phase1`, `npm run build:phase3` or `npm run build:phase45`.

## How we work

- No direct commits to `main`. Each change goes on its own branch and is merged by a pull request that a teammate reviews.
- Merge with **Create a merge commit**, so every person's commits stay in the history, then delete the branch.
- Each of us commits from our own GitHub account. Commit history is 10% of each phase grade.
- Small commits with [Conventional Commits](https://www.conventionalcommits.org/) messages: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`.
- Never force-push, and never commit secrets. Keys and passwords go in `src/.env`, which Git ignores.
