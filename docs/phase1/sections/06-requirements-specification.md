# 6. Initial Requirements Specification

This section gives the initial functional and non-functional requirements. Identifiers are stable and will be carried into the Phase 3 Requirements Document, where they will be expanded with use cases, business rules and acceptance criteria using the SRS template provided in the project appendix. Priority uses MoSCoW (M/S/C).

## 6.1 Functional Requirements – Classic Baseline

<!-- widths: 900,7860,600 -->
| ID | Requirement | Pri. |
|---|---|---|
| FR-01 | The system shall allow the system administrator to create accounts and assign one or more of the nine roles (department representative, asset custodian, requester, administrator, procurement officer, finance officer, maintenance staff, sustainability officer, system administrator). | M |
| FR-02 | The system shall authenticate users and enforce role-based access control on every function and data item. | M |
| FR-03 | The system shall allow administrators to create and manage departments and assign users and assets to them. | M |
| FR-04 | The system shall allow authorised users to register an asset with name, description, category, quantity, owner, department, location, purchase date, estimated value, condition, availability, photographs and supporting documents. | M |
| FR-05 | The system shall maintain a life-cycle status for each asset (e.g., registered, in use, published, reserved, in transfer, under maintenance, donated, recycled, disposed, retired) and record every status change with user and timestamp. | M |
| FR-06 | The system shall allow a department representative to publish an asset as surplus, underutilised or unwanted so that it is visible to authorised campus users. | M |
| FR-07 | The system shall allow users to submit a resource request specifying category, purpose, specifications, quantity, preferred condition, urgency, location and required date, and to track its status. | M |
| FR-08 | The system shall provide structured search and filtering by category, condition, department, location, quantity, availability, asset age, estimated value and life-cycle status. | M |
| FR-09 | The system shall allow a requester to reserve an available asset and shall prevent conflicting reservations. | M |
| FR-10 | The system shall implement approval workflows for asset release, reservation, transfer, receipt, donation, recycling and disposal, with configurable approver roles per step. | M |
| FR-11 | The system shall record for each transfer: approval, collection or delivery arrangements, custody change, new location, receiving confirmation and supporting documents. | M |
| FR-12 | The system shall allow authorised users to report defects, request inspection, record inspection, maintenance, repair and refurbishment actions with costs, and update the asset's condition after service. | M |
| FR-13 | The system shall maintain a complete asset life-cycle history (acquisition, allocation, utilisation, inspection, maintenance, repair, transfer, refurbishment, donation, recycling, retirement, disposal). | M |
| FR-14 | The system shall send notifications (in-app and/or e-mail) to relevant stakeholders on request submission, match found, approval decision, transfer step, maintenance update and end-of-life action. | M |
| FR-15 | The system shall generate conventional reports on available assets, open requests, completed transfers, maintenance history, ownership changes, approvals and asset status. | M |
| FR-16 | The system shall keep an immutable audit log of all create, update, approve, override and delete actions. | S |

## 6.2 Functional Requirements – AI-Enhanced Extension

<!-- widths: 900,7860,600 -->
| ID | Requirement | Pri. |
|---|---|---|
| AI-01 | On asset registration the system shall analyse title, description, specifications and (where available) images and documents to recommend a category, subcategory, standardised tags, possible material type and missing metadata; the user may accept, edit or reject each suggestion. | M |
| AI-02 | The system shall semantically match available asset listings with open requests based on meaning rather than exact keywords. | M |
| AI-03 | The matching engine shall consider category compatibility, functional purpose, technical specifications, quantity, asset condition, requested condition, physical location, urgency, required date, transfer cost and repair cost. | M |
| AI-04 | For each recommended asset–request pair the system shall produce a compatibility score (0–100) and a human-readable explanation of the main contributing factors. | M |
| AI-05 | The system shall rank suitable matches by functional suitability, urgency, transfer cost, repair requirements, waste-diversion benefit and estimated carbon-emission reduction. | S |
| AI-06 | The system shall recommend a sustainable action for an asset (retain, transfer, repair, refurbish, donate, disassemble for components, recycle, or dispose as a last option) with a confidence level and rationale. | S |
| AI-07 | The system shall provide an LLM-powered assistant supporting natural-language asset search, request submission, asset-history and status questions, policy guidance, sustainability questions and navigation of system functions, scoped to the user's permissions. | S |
| AI-08 | The system shall apply generative AI to produce summarised monthly reports, sustainability updates, management bulletins, high-demand-category summaries, maintenance insights and lists of recommended actions from operational data. | M (basic) / S (full) |
| AI-09 | All AI outputs shall be recommendations only; approval of transfers, donations, recycling and disposal shall require an authorised human decision, and users shall be able to override any recommendation with a recorded justification. | M |
| AI-10 | The system shall display confidence information for AI outputs, record the model/service version used for each recommendation, and fall back to classic rule-based behaviour when an AI service is unavailable or returns low confidence. | S |

## 6.3 Sustainability Measurement Requirements

<!-- widths: 900,7860,600 -->
| ID | Requirement | Pri. |
|---|---|---|
| SU-01 | The system shall compute and display waste diverted (kg or item count), reuse rate, asset-life extension, number and value of avoided purchases, financial savings and estimated carbon-emission reductions. | M |
| SU-02 | Sustainability calculations shall use configurable factors (e.g., emission factor per category, average replacement cost) maintained by the sustainability officer, and each figure shall state its assumptions and uncertainty range. | S |
| SU-03 | The system shall present sustainability indicators on a dashboard and include them in generated reports. | M |

## 6.4 Non-Functional Requirements

<!-- widths: 1000,1600,6160,600 -->
| ID | Category | Requirement | Pri. |
|---|---|---|---|
| NFR-01 | Usability | Core tasks (publish asset, submit request, approve transfer) shall be completable by a new user in under 5 minutes with no training; the UI shall follow consistent layouts and provide accessible contrast and keyboard navigation. | M |
| NFR-02 | Performance | Structured search shall return results within 2 s and AI matching within 10 s for a catalogue of at least 1,000 assets and 200 open requests. | S |
| NFR-03 | Security | Passwords hashed; sessions expire; all access checked server-side against role; financial and operational data visible only to authorised roles; protection against common web vulnerabilities (injection, XSS, CSRF). | M |
| NFR-04 | Privacy | Data minimisation: personal data limited to what is needed for accountability; audit logs and reports avoid exposing personal data beyond role scope. | M |
| NFR-05 | Auditability | Every approval, override and life-cycle change is traceable to a user, timestamp and (for AI) model version. | M |
| NFR-06 | Explainability | Every AI recommendation is accompanied by an explanation understandable by a non-technical administrator. | M |
| NFR-07 | Reliability / fallback | If AI services fail, all classic functions remain available and the UI indicates that AI features are degraded. | M |
| NFR-08 | Maintainability | Modular, layered architecture with clear separation between UI, application logic, data and AI services; documented APIs; automated tests for core modules. | M |
| NFR-09 | Portability / deployability | The prototype runs from the repository on a clean machine following the README setup in under 15 minutes. | M |
| NFR-10 | Data integrity | Validation of all inputs; referential integrity between assets, requests, transfers and history; backup/restore procedure documented. | S |
| NFR-11 | Scalability | Design supports growth to campus scale (tens of thousands of assets) without architectural change, even if the prototype is not load-tested at that scale. | C |
| NFR-12 | Fairness and ethics | Matching and recommendations shall not systematically disadvantage any department; recommendation logic is documented and reviewable. | S |
