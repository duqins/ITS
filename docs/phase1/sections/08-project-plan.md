# 8. Initial Project Plan

## 8.1 Proposed Methodology

The team will follow an Agile approach (Scrum-style) constrained by the course's phase gates: each course phase is treated as one or more sprints with a defined deliverable, a sprint planning session in the first lab of the phase, a mid-phase check-in, and a review with the instructors at submission. Agile is preferred over Waterfall because AI features carry technical uncertainty (API availability, match quality) that requires early prototyping and iteration, while the fixed course deadlines and document deliverables still give the overall project a milestone-driven backbone. Requirements and design documents will be versioned in the repository and updated as learning occurs.

## 8.2 Preliminary Timeline and Milestones

<!-- widths: 700,1500,2600,800,3760 -->
| Phase | Due (labs of week of) | Milestone / deliverable | Weight | Key tasks |
|---|---|---|---|---|
| 1 | 14 Sep 2026 | Initial Plan and Requirement Gathering Document | 10 % | Problem, scope, stakeholders, as-is study, initial requirements, plan. Repo created and collaborators added by 15 Sep. |
| 2 | 21 Sep 2026 | Feasibility Document | 10 % | Technical, financial, operational, schedule, data/AI and legal/ethical feasibility; technology stack decision; LLM/embedding API selection and fallback. |
| 3 | 5 Oct 2026 | Requirements Document | 10 % | Full SRS (template in appendix): actors, states, business rules, FR/NFR, AI and sustainability requirements, use-case diagram and descriptions, prioritisation. |
| 4 & 5 | 26 Oct 2026 | Design Document (Architecture and Detailed Design) | 20 % | Layered architecture, component/deployment diagrams, DFDs, ERD, class/sequence/activity/state diagrams, AI workflow diagrams, interface contracts, mockups, security boundaries. |
| 6 | 16 Nov 2026 | Draft Implementation with Major Features | 20 % | Working prototype: auth/RBAC, departments, assets, marketplace, requests, search, AI classification and matching, approvals, transfers, maintenance, sustainability dashboard, reports. |
| 7 | 23 Nov 2026 | Details of Test Cases | 10 % | Unit, integration, system, AI-quality, sustainability-calculation and user-acceptance tests; limitations of test data reported honestly. |
| 8 | 23 Nov 2026 | Final Project, Presentation and Demonstration | 20 % | Final code, configuration, documentation across all phases, presentation and live demo. |

> Note: the project description lists a tentative schedule starting one week later (Phase 1 in the week of 20 September 2026). This plan follows the Phase 1 lab slides, which are the more recent instruction; the team will confirm the dates with the instructors.

## 8.3 Team Structure and Roles

Roles rotate partially so that every member gains experience across the SDLC, but each member owns one area for accountability and for clear individual authorship in the commit history.

<!-- widths: 1800,2200,3560,1800 -->
| Team member | Primary role | Owns (modules / documents) | Secondary role |
|---|---|---|---|
| Sultan Almheiri | Project lead / Scrum master and backend lead | Planning documents, sprint coordination, repository administration, data model, workflow engine (approvals, transfers), integration | Sustainability calculations and reporting |
| Zayed Alfadli | Requirements, UX and QA lead | Requirements documents, use cases, mockups, UI implementation, test plan and test cases, UAT, user documentation | Frontend developer |
| Ghith Alhinaai | Architecture and AI integration lead | System architecture, security, classification, semantic matching, recommendation, LLM assistant, generative reporting, AI evaluation | DevOps / documentation |

## 8.4 Task Assignments for Phases 1–3

<!-- widths: 5400,2600,1360 -->
| Task | Owner | Due |
|---|---|---|
| Finalise Phase 1 document and submit | Project lead (Sultan); all contribute sections | Week of 14 Sep |
| Create GitHub repository, add instructor and lab engineer as collaborators, add README, .gitignore, licence, branch protection on main | Project lead (Sultan) | 15 Sep |
| Set up Git identity and first commit for every member | Each member | 15 Sep |
| Technology stack proposal and AI API evaluation (free tiers, rate limits, fallback) | AI/architecture lead (Ghith) | Week of 21 Sep |
| Feasibility document (six feasibility dimensions) | Requirements lead (Zayed) drafts, all review | Week of 21 Sep |
| Stakeholder interviews and survey | Requirements/UX lead (Zayed) | Weeks of 21 Sep – 28 Sep |
| Use-case diagram and detailed use-case descriptions | Requirements lead (Zayed) | Week of 5 Oct |
| Full SRS using appendix template | Requirements lead (Zayed) owns, all contribute | Week of 5 Oct |
| Synthetic data set design (assets, departments, requests) | Project lead (Sultan) + AI lead (Ghith) | Week of 5 Oct |

## 8.5 Dependencies

- Phase 2 stack decision depends on confirmation of available LLM/embedding API access (free tier or instructor-provided key).
- Phase 3 SRS depends on interview/survey results and instructor answers on approval thresholds and sustainability factors.
- Phase 4–5 design depends on the finalised data model and the chosen AI service interfaces.
- Phase 6 implementation depends on the synthetic data set and on all members having a working local environment.
- Phase 7 AI-quality testing depends on a labelled test set created during Phase 6.
- All phases depend on continuous, individually-authored commits to satisfy the GitHub grading criterion.

## 8.6 Risks and Mitigation

<!-- widths: 500,2800,1100,900,4060 -->
| # | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | LLM/embedding API unavailable, rate-limited or paid | Medium | High | Evaluate two providers in Phase 2; design AI as a pluggable service; keep a small open-source model or keyword fallback. |
| R2 | Scope too large for the semester | High | High | Strict MoSCoW; Must-have items first; Should/Could only after prototype is stable. |
| R3 | Uneven contribution / commit history flagged | Medium | High | Module ownership per member; PR-based workflow; weekly commit check by project lead. |
| R4 | Match quality poor on synthetic data | Medium | Medium | Build a labelled test set early; iterate on prompts/embeddings; report limitations honestly. |
| R5 | Sustainability figures unreliable | Medium | Medium | Use published factors; state assumptions and uncertainty ranges; sustainability officer role can edit factors. |
| R6 | Security weaknesses in RBAC | Medium | High | Server-side authorisation on every endpoint; security test cases in Phase 7. |
| R7 | Team member unavailable (illness, exams) | Medium | Medium | Secondary role for every area; documentation in repo so work can be picked up. |
| R8 | Schedule ambiguity between slides and description | Low | Medium | Confirm with instructors in the first lab; plan to the earlier date. |
| R9 | Secrets (API keys) committed to repository | Medium | High | .gitignore from day one; .env files; rotate key immediately if leaked. |

## 8.7 Resource Allocation

- **People:** Three students, approximately 6–8 hours per member per week, rising to 10+ in Phases 6–8.
- **Tools:** GitHub (repository, issues, pull requests, projects board); VS Code with GitHub Copilot (student plan); draw.io/PlantUML for UML; a web framework and relational database chosen in Phase 2; hosted LLM/embedding API (free tier); LibreOffice/Word for documents.
- **Infrastructure:** local development machines; university lab computers; optional free-tier cloud hosting for the demo.
- **Data:** team-generated synthetic asset, department, request and maintenance data; published sustainability factors.
- **Budget:** AED 0 – all tools on free or student tiers.

## 8.8 Version Control and Collaboration Workflow

- One repository, created on GitHub with README, .gitignore and licence; instructor and lab engineer added as collaborators.
- Branch protection on main: no direct commits; every change via a feature branch and pull request with at least one reviewer.
- Conventional Commits messages (feat, fix, docs, test, refactor, chore); one logical change per commit.
- Each member commits under their own verified GitHub identity so authorship is visible.
- Documents for every phase are written in Markdown in the repository (docs/phaseN/sections) and committed incrementally as they are written; the Word/PDF versions are generated from them for submission.
- Secrets are never committed; API keys live in .env files excluded by .gitignore.
