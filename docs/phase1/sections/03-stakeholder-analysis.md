# 3. Stakeholder Analysis

## 3.1 Identification of Stakeholders

Stakeholders were identified from the project description (nine system roles), the lab slides and a walkthrough of the as-is process (Section 4). They fall into four groups: end users, decision makers, the client/oversight group, and the development team.

<!-- widths: 1800,3000,4560 -->
| Group | Stakeholder | Interest in the system |
|---|---|---|
| End users | Department representatives | Publish surplus assets and request resources on behalf of their department. |
| End users | Requesters (staff, faculty, lab coordinators) | Find, reserve and request assets that meet a specific need. |
| End users | Asset custodians | Maintain asset records, condition and location; release and receive assets. |
| End users | Maintenance staff | Receive defect reports, record inspections, repairs and costs, update condition. |
| Decision makers | Administrators (department/college level) | Approve releases, reservations and transfers; resolve conflicts. |
| Decision makers | Procurement officers | Confirm reuse before new purchase; validate ownership changes. |
| Decision makers | Finance officers | Track asset value, savings, transfer cost and write-offs. |
| Decision makers | Sustainability officers | Define sustainability metrics; review recommendations for donation/recycling/disposal; consume reports. |
| System | System administrators | Manage accounts, roles, configuration, AI service settings, audit logs and backups. |
| Client / oversight | Lab instructors (client, sponsor) | Define requirements, evaluate deliverables and prototype. |
| Client / oversight | University management (indirect) | Receive management bulletins and sustainability updates. |
| Development | Project team | Design, build, test, document and demonstrate the system. |

## 3.2 Stakeholder Roles and Responsibilities

<!-- widths: 2200,3800,3360 -->
| Stakeholder | Responsibilities in the process | Permissions in the system |
|---|---|---|
| Department representative | Register department assets; flag surplus; submit and track requests; confirm receipt of transferred assets. | Create/edit own department's assets and requests; publish listings; view marketplace; view own department reports. |
| Requester | Search marketplace; reserve or request assets; use the assistant; provide feedback on match usefulness. | Read marketplace; create reservations/requests; view own request status. |
| Asset custodian | Keep asset record accurate; perform hand-over and hand-back; record location and custody changes. | Edit assigned assets' condition, location, photos, documents; confirm release and receipt. |
| Maintenance staff | Inspect, repair, refurbish; record actions, parts and costs; update condition after service. | Create inspection/maintenance/repair records for any asset; change condition status. |
| Administrator | Approve or reject release, reservation, transfer, donation, recycling, disposal within their scope; override AI recommendations with justification. | Approve/reject workflow steps; view department-wide data; view recommendation explanations. |
| Procurement officer | Check marketplace before approving new purchases; validate asset acquisition data. | Read all listings and requests; annotate requests as 'purchase avoided'; view savings reports. |
| Finance officer | Maintain estimated value, depreciation and transfer cost; approve write-offs. | Edit financial fields; approve disposal from a financial perspective; view financial reports. |
| Sustainability officer | Define carbon/waste factors; review end-of-life recommendations; publish sustainability reports. | Configure sustainability parameters; approve donation/recycling; generate sustainability reports. |
| System administrator | Account provisioning, role assignment, configuration, AI model version tracking, backup, audit. | Full administrative access; cannot approve business workflows unless also holding a business role. |

## 3.3 Stakeholder Needs and Expectations

<!-- widths: 2200,3400,3760 -->
| Stakeholder | Needs | Expectations of the system |
|---|---|---|
| Department representative | Quick publication of surplus; simple request form; status visibility. | Publishing an asset takes minutes; AI suggests category and description; clear notifications on every status change. |
| Requester | Find functionally suitable items even with different terminology. | Semantic search returns relevant items; ranked matches with an explanation; can ask the assistant in plain language. |
| Asset custodian | Accurate, single record per asset; minimal duplicate data entry. | Life-cycle history is complete and auditable; custody hand-over is confirmed by both parties. |
| Maintenance staff | Structured defect reports and repair logs with cost capture. | Defect-to-repair workflow with status tracking and condition update. |
| Administrator | Clear approval queue and decision context. | Approval screen shows request, asset, match score, explanation and sustainability impact; decisions are logged. |
| Procurement / Finance | Evidence of avoided purchases and savings. | Reports quantify avoided purchases, transfer cost and financial savings with traceable calculations. |
| Sustainability officer | Reliable, explainable sustainability indicators. | Waste diversion, reuse rate, asset-life extension and carbon estimates with stated assumptions and uncertainty. |
| System administrator | Secure, maintainable configuration. | Role management, audit logs, AI service configuration and fallback settings. |
| Lab instructors | Evidence of SDLC practice and responsible AI reflection. | Professional documentation, regular commits by every member, working prototype, explicit classic-vs-AI comparison. |

## 3.4 Stakeholder-to-Feature Mapping

The table maps each stakeholder to the features they use, the data they need, and the approval decisions they own. This mapping drives the role-based access design in later phases.

<!-- widths: 2300,2000,3260,1800 -->
| Feature | Primary users | Data needs | Approval decision owner |
|---|---|---|---|
| Asset registration and inventory | Dept. representative, custodian | Name, description, category, quantity, owner, department, location, purchase date, value, condition, availability, photos, documents | — (custodian confirms record) |
| Surplus publication (marketplace) | Dept. representative | Asset record, reason for surplus, availability window | Administrator approves release |
| Resource request | Requester, dept. representative | Category, purpose, specifications, quantity, preferred condition, urgency, location, required date | Administrator (requesting side) validates need |
| Search and filtering | All users | Category, condition, department, location, quantity, availability, age, value, life-cycle status | — |
| AI matching and ranking | Requester, administrator | Listings, requests, compatibility score, explanation, transfer/repair cost, sustainability benefit | Administrator accepts or overrides match |
| Reservation | Requester | Asset, requester, period, request link | Custodian / administrator confirms |
| Transfer management | Custodian, administrator | Approval, collection/delivery arrangements, custody change, new location, confirmation, documents | Releasing and receiving administrators; custodians confirm hand-over |
| Maintenance and repair | Maintenance staff, custodian | Defect report, inspection, repair actions, parts, cost, condition after service | Maintenance lead approves repair spend above threshold (TBD) |
| Sustainable-action recommendation | Sustainability officer, administrator | Asset condition, age, repair cost, demand, waste-diversion benefit, carbon estimate | Sustainability officer + finance officer approve donation/recycling/disposal |
| LLM assistant | All users | Read access to listings, requests, status, policies scoped by role | — (assistant cannot approve anything) |
| Reports (classic and generative) | Administrators, finance, procurement, sustainability | Aggregated operational and sustainability data | — |
| User and access management | System administrator | Accounts, roles, departments, audit logs, AI configuration | System administrator |
