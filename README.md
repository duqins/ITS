# ITS – Intelligent, AI-Powered Circular Campus Resource Exchange and Asset Life Cycle Management System

COSC 336 – Introduction to Software Engineering, Khalifa University, Fall 2026. Lab-based running project, **Group 4**.

## Team
| Member | Primary role |
|---|---|
| Sultan Almheiri | Project lead / Scrum master, backend lead |
| Zayed Alfadli | Requirements, UX and QA lead |
| Ghith Alhinaai | Architecture and AI integration lead |

## What the system does
An internal campus platform that registers, publishes, matches, transfers, maintains and tracks campus assets through their life cycle, with a classic rule-based core and AI-enhanced services (classification, semantic matching, sustainable-action recommendations, LLM assistant, generative reporting).

## Repository layout
```
docs/
  phase1/            Phase 1 deliverable
    sections/        The document, one Markdown file per section (edit these)
    build.js         Generates the .docx from the sections (npm run build:phase1)
  reference/         Course project description and lab slides
src/                 Application source (from Phase 6)
```

## Phase schedule
| Phase | Due (labs of week of) | Deliverable |
|---|---|---|
| 1 | 14 Sep 2026 | Initial Plan and Requirement Gathering Document |
| 2 | 21 Sep 2026 | Feasibility Document |
| 3 | 5 Oct 2026 | Requirements Document |
| 4 & 5 | 26 Oct 2026 | Design Document |
| 6 | 16 Nov 2026 | Draft Implementation |
| 7 | 23 Nov 2026 | Test Cases |
| 8 | 23 Nov 2026 | Final Project, Presentation and Demo |

## Documents
All phase documents are written in Markdown under `docs/phaseN/sections/` so that everyone can edit at the same time and git can merge the changes. The Word/PDF versions are generated for submission — see `docs/phase1/README.md`.

## Working agreement
- No direct commits to `main`; work on a branch and open a pull request.
- Conventional Commits (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`), one logical change per commit.
- Everyone commits under their own GitHub account – commit history is 10 % of each phase grade.
- Never commit secrets; API keys go in `.env` (ignored).
