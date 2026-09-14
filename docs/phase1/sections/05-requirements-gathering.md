# 5. Requirements Gathering

## 5.1 Methodology

Requirements gathering will continue throughout the project. Phase 1 creates an initial list from the supplied documents, Phases 2 and 3 validate it with the client and stakeholders, and later prototypes and tests help identify missing or unclear requirements. Using several techniques reduces the risk of relying on one person's assumptions.


| Technique | Purpose | Participants or sources | Timing |
|---|---|---|---|
| Document analysis | Identify required roles, features, constraints, deliverables, and open questions. | Project description, Phase 1 slides, course announcements | Phase 1 and whenever documents change |
| Client Q&A | Clarify scope, deadlines, priorities, approval rules, and prototype expectations. | Lab instructors and project team | Weekly during Phases 1-3 |
| Stakeholder interviews | Understand real tasks, data, decisions, permissions, exceptions, and problems. | Representatives of the nine system roles | Phases 2-3 |
| Short survey | Collect and rank common problems and desired features from a wider group. | Potential requesters, custodians, and department staff | Phases 2-3 |
| Process workshop | Walk through the complete process and agree on states, approvals, and required evidence. | Operational users, decision makers, instructors, project team | Phase 3 |
| Prototype review | Validate forms, navigation, wording, status information, and AI explanations before implementation. | Selected users and instructors | Phases 3-5 |
| Testing and acceptance feedback | Confirm that the requirements are testable and that the implemented system meets stakeholder needs. | Client, developers, testers, selected users | Every sprint; formally in Phases 6-7 |

Interview and workshop results will be recorded with their source, affected role, priority, and open questions. A requirement will only be treated as validated after the client or an appropriate stakeholder representative confirms it.

## 5.2 Summary of Gathered Requirements

The information gathered so far can be summarised into six areas. Detailed numbered requirements will be provided in Section 6.

- **Assets and inventory:** Register assets with complete information, publish available items, update condition and location, and keep a full life-cycle history.
- **Marketplace and requests:** Allow departments to search, filter, reserve, request, and track available resources.
- **Approvals and transfers:** Define clear approval steps, decision owners, handover information, custody and location changes, notifications, and audit records.
- **Maintenance and end-of-life:** Record defects, inspections, repairs, costs, and outcomes, then control donation, recycling, retirement, or disposal.
- **AI services:** Suggest classifications, match assets with requests, rank and explain recommendations, support natural-language interaction, and create report summaries. Humans must approve important actions.
- **Security, sustainability, and reporting:** Use role-based access, protect information, measure savings and environmental benefits, show assumptions, and provide operational dashboards and reports.

## 5.3 Prioritisation of Requirements

The requirements are prioritised using MoSCoW because the semester has a fixed deadline and the team has limited time. “Must” features are built first; “Should” and “Could” features are attempted only after the core system is stable.


| Priority | Meaning | Requirement groups |
|---|---|---|
| Must have | Required for the minimum working prototype or explicitly required by the project description. | Accounts and nine roles; authentication and role-based access; departments; asset registration and publication; requests; search and filtering; reservations; approvals and transfers; custody/location updates; maintenance history; notifications and audit trail; AI classification and explainable matching; human review and classic fallback; basic sustainability indicators and reports; synthetic data and reproducible setup. |
| Should have | Important, but the prototype can work temporarily without it or use a simpler manual process. | production hosting and deployment; Sustainable-action recommendations; LLM assistant; configurable approval limits; advanced matching factors; richer sustainability dashboard; report export; improved accessibility and exception handling. |
| Could have | Useful enhancement attempted only if the Must and Should features are stable. | Demand forecasting; advanced image/document extraction; map view; saved searches and alerts; advanced analytics and AI feedback monitoring. |
| Won't have (this semester) | Explicitly outside the prototype scope and recorded for possible future work. | Live university ERP, finance, procurement, or identity integration; payments or purchasing; transport scheduling; barcode/RFID hardware; real university data; custom model training; native mobile apps; fully autonomous AI approvals. |

The priorities will be reviewed after the Phase 2 feasibility study and confirmed with the instructors. Any change to a Must requirement should record the reason, effect on the schedule, and client decision.
