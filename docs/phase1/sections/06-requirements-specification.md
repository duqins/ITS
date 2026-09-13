# 6. Initial Requirements Specification

<!-- OWNER: Ghith. Delete the guidance lines starting with ">" when you are done.
     What the slides require (slide 10): "Detailed description of functional/operational requirements."
     The project description, Objective 1 (pages 3–4), lists the classic functions; Objective 2 (page 4) lists the AI
     functions; the appendix explains functional vs non-functional requirements. -->

> Short intro paragraph: say that IDs are stable and will be expanded in the Phase 3 SRS, and that priority uses MoSCoW (M/S/C).

## 6.1 Functional Requirements – Classic Baseline

> Write each requirement as "The system shall ...". One row per requirement. Cover at least: user accounts and roles, authentication and role-based access, departments, asset registration (all the fields listed in the description), life-cycle status, publishing surplus, resource requests, search and filtering, reservation, approval workflows, transfer records, maintenance and repair, life-cycle history, notifications, reports, audit log.

<!-- widths: 900,7860,600 -->
| ID | Requirement | Pri. |
|---|---|---|
| FR-01 |  |  |
| FR-02 |  |  |
| FR-03 |  |  |

## 6.2 Functional Requirements – AI-Enhanced Extension

> Cover: AI classification on registration, semantic matching, the factors the matching engine must consider, compatibility score and explanation, ranking/prioritisation, sustainable-action recommendation, LLM assistant, generative reports. Add requirements that AI is recommendation-only (humans approve), that confidence and model version are shown/recorded, and that the system falls back to classic behaviour when AI is unavailable.

<!-- widths: 900,7860,600 -->
| ID | Requirement | Pri. |
|---|---|---|
| AI-01 |  |  |
| AI-02 |  |  |
| AI-03 |  |  |

## 6.3 Sustainability Measurement Requirements

> The description asks for waste diversion, avoided purchases, asset-life extension, reuse rate, financial savings and estimated carbon-emission reductions. Say how they are shown and that assumptions/uncertainty must be stated.

<!-- widths: 900,7860,600 -->
| ID | Requirement | Pri. |
|---|---|---|
| SU-01 |  |  |
| SU-02 |  |  |

## 6.4 Non-Functional Requirements

> Categories to cover: usability, performance, security, privacy, auditability, explainability, reliability/fallback, maintainability, portability (must run on a grader's machine from the repo), data integrity, scalability, fairness/ethics. Make them measurable where you can (e.g. "search returns in under 2 seconds").

<!-- widths: 1000,1600,6160,600 -->
| ID | Category | Requirement | Pri. |
|---|---|---|---|
| NFR-01 |  |  |  |
| NFR-02 |  |  |  |
| NFR-03 |  |  |  |
