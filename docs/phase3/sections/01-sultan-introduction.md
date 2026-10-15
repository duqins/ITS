# Revision History

<!-- widths: 2000,1500,4860,1000 -->
| Name | Date | Reason for changes | Version |
|---|---|---|---|
| Group 4 | 15 Sep 2026 | First requirements, in the Phase 1 planning document | 0.1 |
| Group 4 | 29 Sep 2026 | Scope, roles and tools confirmed in the Phase 2 feasibility study | 0.2 |
| Group 4 | 13 Oct 2026 | Full SRS for Phase 3: use cases, states, business rules and detailed requirements | 1.0 |

# 1. Introduction

## 1.1 Purpose

This is the Software Requirements Specification (SRS) for Dawra Campus, the campus asset-reuse system our group is building for COSC 336. It lists what the system has to do, so we can design it in Phases 4 and 5, build it in Phase 6 and test it in Phase 7.

It covers the whole prototype: the normal (classic) features such as accounts, assets, requests, approvals, transfers and maintenance; the AI features; and the sustainability numbers. It builds on the requirements we wrote in Phase 1 and the decisions we made in the Phase 2 feasibility study. It says what the system should do, not how we will build it.

## 1.2 Document Conventions

We follow the SRS template from the project description. Every requirement has an ID. If a requirement comes from Phase 1, it keeps the Phase 1 number, so FR-07.3 is the third detailed requirement under Phase 1's FR-07 (resource requests).

<!-- widths: 2000,7360 -->
| ID | What it is |
|---|---|
| FR-nn.m | Classic functional requirement (sections 4.2–4.15) |
| AI-nn.m | AI requirement (sections 4.16–4.22) |
| SU-nn | Sustainability requirement (section 6.1) |
| NFR-nn | Non-functional requirement (section 5) |
| BR-nn | Business rule (section 5.5) |
| UC-nn, UI-nn, SI-nn | Use case (7.3), screen (3.1), software interface (3.3) |
| AS, LS, RQ, RV, TR, MW, EL, AT | States of assets, listings, requests, reservations, transfers, maintenance jobs, end-of-life actions and approvals (section 4.1) |
| TBD-n | Something we still need the instructors to confirm (Appendix C) |

**How requirements are written.** "Shall" means the system must do it. We use the EARS patterns from the Chapter 3 slides: *The system shall …*, *When …*, *While …*, *If … then …* and *Where …*.

**Priorities.** The project description asks us to split requirements into essential prototype functions, desirable extensions and future enhancements. The table shows how these match the Must/Should/Could labels we used in Phase 1 and the High/Medium/Low labels in the template. Each feature has a priority, and its requirements share it unless a row says otherwise.

<!-- widths: 2600,1700,1300,3760 -->
| Course tier | Phase 1 label | Template | Meaning |
|---|---|---|---|
| Essential prototype function | Must | High | Has to work in the Phase 6 prototype and the final demo |
| Desirable extension | Should | Medium | We build it once the essential parts work |
| Future enhancement | Could / Won't | Low | Not this semester unless we finish everything else |

**Numbers and data.** The numbers here are targets, not results, because nothing is built yet. All our test data is made up (synthetic). Anything that depends on KU policy is marked TBD and listed in Appendix C.

## 1.3 Intended Audience and Reading Suggestions

<!-- widths: 2600,3400,3360 -->
| Reader | Why they read it | Where to start |
|---|---|---|
| Lab instructors (our client) | Check the scope, priorities and open questions | 1.4, 2, 6.4, 7, Appendix C |
| Our team as developers | Design and build the system | 2, 4.1, 5.5, then 4.2–4.22 and 5.1–5.4 |
| Our team as testers (Phase 7) | Write test cases; every "shall" is something to test | 4.1, 4.2–4.22, 5, 6.1 |
| Whoever designs the screens | Plan the pages and user journeys | 2.3, 3.1, 7 |

Section 2 describes the product. Section 3 covers its interfaces. Section 4 has the states and the requirements for each feature. Section 5 has the quality requirements and the business rules, including who approves what. Section 6 covers sustainability, data, priorities and traceability. Section 7 has the use-case diagram and the use-case descriptions. The appendices have the glossary, the open questions and our AI-use note.

## 1.4 Product Scope

Departments at KU keep buying things like chairs, monitors and lab equipment while the same items sit unused in another building. The asset register records who owns what, but it doesn't help anyone find, match or move these items (Phase 1, section 1.2).

Dawra Campus is a website for KU staff that fixes this. Departments register their assets and list the ones they don't need. Other departments search, request and reserve items, and the right people approve the transfer. The system also tracks repairs and what happens to items at the end of their life, and reports how much money and waste was saved. AI helps sort items into categories, match requests to items, suggest what to do with old items, answer questions and summarise reports, but people always make the final decision.

Our goals are the same as in Phase 1: fewer unnecessary purchases, longer asset life, better matching, clear approvals, measurable sustainability results, responsible AI, and a comparison of classic and AI-based approaches. What's left out is the same as in Phase 2: connecting to KU's real finance, procurement or ERP systems, payments, barcode or RFID scanners, training our own AI models, AI approving things on its own, and phone apps. This is a student prototype. Using it for real at KU would need proper evidence and a decision from the university.

## 1.5 References

<!-- widths: 700,5560,1600,1500 -->
| ID | Document | Date | Location |
|---|---|---|---|
| R1 | COSC 336 Lab-based Running Project – Project Description, including the SRS template in the appendix | Fall 2026 | docs/reference |
| R2 | COSC 336 Lab Phase 1 slides – Initial Plan and Requirement Gathering | Fall 2026 | docs/reference |
| R3 | Group 4, Phase 1 Initial Plan and Requirement Gathering Document | 15 Sep 2026 | docs/phase1 |
| R4 | Group 4, Dawra Campus Phase 2 Feasibility Study | 29 Sep 2026 | docs/phase2/final |
| R5 | COSC 336 lecture slides, Chapter 3 Requirements Engineering (use cases, UML use-case diagrams, EARS) | Fall 2026 | Blackboard |
| R6 | ISO/IEC/IEEE 29148:2018 Systems and software engineering – Requirements engineering | 2018 | iso.org |
| R7 | A. Mavin et al., "Easy Approach to Requirements Syntax (EARS)", IEEE International Requirements Engineering Conference | 2009 | IEEE Xplore |
| R8 | I. Sommerville, Software Engineering, 10th edition, Pearson, chapter 4 | 2016 | Course reference |
