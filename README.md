# ITS – Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System

COSC 336 – Introduction to Software Engineering, Khalifa University, Fall 2026. Lab-based running project, **Group 4**.

## Team
| Member | Student ID | Primary role |
|---|---|---|
| Sultan Almheiri | 100065654 | Project lead / Scrum master, backend lead |
| Zayed Alfadli | 100064657 | Requirements, UX and QA lead |
| Ghaith Alhinaai | 100066185 | Architecture and AI integration lead |

## What the system does
An internal campus platform that registers, publishes, matches, transfers, maintains and tracks campus assets through their life cycle, with a classic rule-based core and AI-enhanced services (classification, semantic matching, sustainable-action recommendations, LLM assistant, generative reporting).

## Repository layout
```
docs/
  phase1/            Phase 1: initial plan and requirement gathering
    sections/        The document, one Markdown file per section (edit these)
    build.js         Generates the .docx from the sections (npm run build:phase1)
  phase2/            Phase 2: feasibility study (final report and slides in final/)
  phase3/            Phase 3: requirements document (SRS)
    sections/        One Markdown file per section (edit these)
    build.js         Generates the .docx from the sections (npm run build:phase3)
    presentation/    Phase 3 class presentation
  reference/         Course project description and lab slides
src/                 Application source (from Phase 6)
```

## Phase schedule
| Phase | Due | Deliverable |
|---|---|---|
| 1 | Labs of the week of 14 Sep 2026 | Initial Plan and Requirement Gathering Document |
| 2 | Tue 29 Sep 2026 | Feasibility Document |
| 3 | Tue 13 Oct 2026, resubmission Fri 16 Oct 2026, 6 PM | Requirements Document |
| 4 & 5 | Labs of the week of 26 Oct 2026 | Design Document |
| 6 | Labs of the week of 16 Nov 2026 | Draft Implementation |
| 7 | Labs of the week of 23 Nov 2026 | Test Cases |
| 8 | Labs of the week of 23 Nov 2026 | Final Project, Presentation and Demo |

Phases 2 and 3 show the Blackboard due dates. The other dates come from the [lab slides](docs/reference/COSC336_Circular_Campus_Project_Fall2026.pdf) (p. 4) and may change, so we confirm each one with the lab instructors.

## Documents
Each member's contribution is written in Markdown under `docs/phaseN/sections/`. The team combines the reviewed sections into the submission files. Phase 1 build instructions are in `docs/phase1/README.md`, the Phase 2 report and slides are in `docs/phase2/final/`, and the Phase 3 instructions are in `docs/phase3/README.md`.

## Working agreement
- No direct commits to `main`; work on a branch and open a pull request.
- Conventional Commits (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`), one logical change per commit.
- Everyone commits under their own GitHub account – commit history is 10 % of each phase grade.
- Never commit secrets; API keys go in `.env` (ignored).

## Phase 3 requirements document (SRS)

Our Software Requirements Specification, updated for the resubmission after TA feedback (due 16 October 2026).

- [SRS (Word)](docs/phase3/Dawra_Campus_Phase3_SRS.docx)
- [SRS (PDF)](docs/phase3/Dawra_Campus_Phase3_SRS.pdf)
- [Class presentation](docs/phase3/presentation/Dawra_Campus_Phase3_Presentation.pptx)
- [Section files and who wrote each one](docs/phase3/README.md)

It covers actors and permissions, record states, the classic and AI features with numbered requirements, non-functional requirements, business rules, priorities checked against our Phase 2 plan, and the use-case model (diagram and use-case descriptions).

## Phase 2 feasibility study

The **29 September final submission** includes the three reviewed individual contributions and two clearly labelled AI stakeholder simulations.

- [Final Word report for Blackboard](docs/phase2/final/Dawra_Campus_Phase2_Feasibility_Study.docx)
- [Final PowerPoint presentation](docs/phase2/final/Dawra_Campus_Phase2_Presentation.pptx)
- [Read the report on GitHub](docs/phase2/final/Dawra_Campus_Phase2_Feasibility_Study.md)
- [Member contributions, sources and review status](docs/phase2/README.md)

The report includes scope, stakeholders, market research, all six feasibility areas, costs, benefits, ROI, payback, quantified risks and the recommendation. Financial figures are labelled scenarios. The simulated interviews support the classroom analysis but do not establish actual KU procedures or measured benefits. The earlier progress package remains available as an archive.
