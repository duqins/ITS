# 6. Other Requirements

## 6.1 Sustainability Measurement Requirements

The project description asks us to measure waste diversion, avoided purchases, asset-life extension, reuse, repair, money saved and carbon saved. Table 6.1 shows how each number is calculated. Only finished and approved actions count, never AI suggestions nobody accepted. Since our data is made up, the numbers show how the method works, not real KU savings. Based on Phase 1 SU-01 to SU-08. **Priority: Essential (Must, High)** for SU-01 to SU-09.

**Table 6.1 Indicator definitions**

<!-- widths: 1900,4500,1500,1460 -->
| Indicator | Calculation for a reporting period | Unit | Source events |
|---|---|---|---|
| Waste diverted | Sum of quantities that left service through reuse, repair returned to service, donation, disassembly or recycling instead of disposal; each item counted once per period; shown by route | Items (kg only where mass is recorded) | TR-06, MW-06, EL-05 |
| Avoided purchases | Number of fulfilled requests confirmed under BR-18, and their value = quantity × replacement cost | Count, AED | TR-06 + reviewer confirmation |
| Net financial savings | Avoided replacement value − attributable transfer, inspection, repair and refurbishment costs | AED | Avoided purchases, MW-06, TR-06 |
| Reuse rate | Quantity from a defined cohort of listed assets transferred and received by period end ÷ total quantity in that cohort × 100; N/A when the cohort is empty | % | LS-03, TR-06 |
| Repair success rate | Work orders Completed with the asset returned to service ÷ work orders closed as Completed or Not repairable × 100; N/A when none closed | % | MW-06, MW-07 |
| Asset-life extension | Revised retirement date − planned retirement date after reuse, repair or refurbishment, per asset; reported as total and average | Months (estimated) | MW-06, TR-06 |
| Estimated carbon reduction | Σ (avoided quantity × embodied emission factor of the category) − emissions attributed to transport and replacement parts; negative results kept; N/A when no defensible factor exists | kg CO2e (estimated) | Avoided purchases, category factors |

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| SU-01 | The system shall display waste diverted, avoided purchases, reuse rate, repair success rate, asset-life extension, net financial savings and estimated carbon reduction on a sustainability dashboard and in the conventional reports, filtered by period and department. |
| SU-02 | The system shall calculate waste diverted as defined in Table 6.1, show the result by route (reuse, repair, donation, disassembly, recycling) and count each item or batch quantity once per period. |
| SU-03 | The system shall count an avoided purchase only under BR-18, recording the reviewer, the quantity and the replacement-cost estimate with its source. |
| SU-04 | The system shall calculate net financial savings as defined in Table 6.1, keeping every input value and never counting the same cost or benefit twice. |
| SU-05 | The system shall calculate the reuse rate for a cohort chosen by the user and show the cohort definition, numerator and denominator. |
| SU-06 | The system shall record a planned retirement date for each asset and, after reuse, repair or refurbishment, an estimated revised date, and shall label the resulting life extension as an estimate. |
| SU-07 | The system shall estimate carbon reduction as defined in Table 6.1 using the emission factor recorded for each category, and shall show N/A rather than a figure when a required factor is missing (TBD-6). |
| SU-08 | The system shall show, for each indicator, its formula, source records, factor source and version, assumptions, the reviewing user and whether values are measured, estimated or synthetic. |
| SU-09 | The system shall calculate the repair success rate as defined in Table 6.1 from closed work orders. |

## 6.2 Data Requirements

These are the main things the system stores. We will draw the full entity-relationship diagram in Phase 5.

<!-- widths: 2200,7160 -->
| Record | Main data |
|---|---|
| User and role assignment | Name, staff email, department, roles per department, account status, authorisation and application of each role |
| Department and category | Name, code, representatives, custodians; category, subcategory, unit, flags (procurement-controlled, special handling), emission factor reference |
| Asset | Fields in FR-04.1, life-cycle state, available/reserved/allocated quantities, verification date, planned retirement date |
| Listing, request, reservation | Fields in FR-06.1, FR-07.1 and FR-09.1, state, links to each other |
| Transfer | Fields in FR-11.1, approvals, handover and receipt confirmations, dispute notes |
| Inspection and work order | Fields in FR-12.1 and FR-13.4, approvals, costs, outcome |
| End-of-life action | Fields in FR-14.1 and FR-14.5, evidence, EHS consultation, data-erasure record |
| Approval task, notification, audit entry | Fields in FR-10.6, FR-16 and FR-18.1 |
| AI output record | Task type, input reference, output, score, confidence, model and version, time, user response (Ghaith, section 4.23) |
| Sustainability factor | Category, factor value, unit, source, version, date |

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| DR-01 | The system shall include a synthetic data set of at least 500 assets in 10 departments, 50 requests and 20 labelled matching cases, which can be loaded with one command for demonstration and testing. |
| DR-02 | The system shall store no real KU staff personal data or real asset records in this release (C-03). |
| DR-03 | The system shall keep records and audit entries for the retention period (TBD-7) and shall allow a full backup and restore of the database and uploaded files. |

## 6.3 Policy, Legal and Ethical Requirements

These come from the checks we listed in Phase 2 (section 15). They are things we still need to confirm, not a claim that KU has approved the system.

- PL-01: Approval stages, thresholds and special-handling rules shall follow KU asset, procurement and environmental policy once confirmed; until then the proposed values in Appendix C apply and are shown as proposed.
- PL-02: Use of any AI service shall comply with the provider's terms and with KU data rules; no data beyond C-06 shall be sent.
- PL-03: All third-party software shall have a licence that allows academic use and publication of the source code.
- PL-04: The interface and documentation shall state that AI outputs are recommendations and that authorised staff remain accountable for decisions.

## 6.4 Prioritisation Summary

The project description asks us to group requirements into essential, desirable and future. Everything the description lists as the Phase 6 minimum is essential.

<!-- widths: 2000,7360 -->
| Tier | Features and requirements |
|---|---|
| Essential prototype functions (Must) | Accounts, roles and access control (4.3); departments and categories (4.4, except FR-03.3); asset registration and states (4.5); publication (4.6); requests (4.7); search and filtering (4.8); reservations (4.9); approval workflow (4.10); transfers (4.11); inspection and maintenance (4.12); end-of-life actions (4.13); history and audit (4.14); notifications (4.15, except FR-16.6); conventional reports and dashboards (4.16, except FR-17.3); AI classification (4.17); semantic matching, ranking, explanations and confidence (4.18–4.19); basic generative reports (4.22); AI tracking, overrides and fallback (4.23); sustainability indicators and dashboard (6.1); synthetic data and documented local setup (DR-01, C-07) |
| Desirable extensions (Should) | Sustainable-action recommendation (4.20); campus assistant (4.21); configurable approval values (FR-03.3); report export (FR-17.3); hosted deployment (DEP-02); richer sustainability dashboard |
| Future enhancements (Could / Won't this semester) | Email notifications (FR-16.6); demand forecasting; map view; saved searches and alerts; Arabic interface; live KU ERP, finance, procurement or identity integration; barcode or RFID hardware; payments; native mobile apps; custom model training |

## 6.5 Traceability

Table 6.5 links each feature to its Phase 1 requirement, its use cases and the roles involved, so we can see that nothing from Phase 1 was dropped. Our Phase 7 test cases will use the same IDs.

**Table 6.5 Feature traceability**

<!-- widths: 2900,1600,1500,3360 -->
| Feature (section) | Phase 1 IDs | Use cases | Main roles |
|---|---|---|---|
| Accounts and access control (4.3) | FR-01, FR-02 | UC-01 | Business administrator, System administrator |
| Departments, categories and settings (4.4) | FR-03 | UC-01 | Business administrator |
| Asset registration and records (4.5) | FR-04, FR-05 | UC-02 | Asset custodian, Department representative |
| Resource publication (4.6) | FR-06 | UC-03 | Department representative, Asset custodian |
| Resource requests (4.7) | FR-07 | UC-04 | Requester, Department representative |
| Search and filtering (4.8) | FR-08 | UC-05 | Requester |
| Reservations (4.9) | FR-09 | UC-07 | Requester, Asset custodian |
| Approval workflow (4.10) | FR-10 | UC-08 | All approving roles |
| Transfer, handover and receipt (4.11) | FR-11 | UC-09 | Department representatives, Asset custodians, Finance and Procurement officers |
| Inspection, maintenance and repair (4.12) | FR-12, FR-13 | UC-10 | Asset custodian, Maintenance staff, Department representative, Finance officer |
| End-of-life actions (4.13) | FR-14 | UC-11 | Sustainability officer, Finance officer, Department representative |
| History and audit (4.14) | FR-15, FR-18 | UC-14 | Asset custodian, Business administrator |
| Notifications (4.15) | FR-16 | All (included in UC-08) | All roles |
| Conventional reports (4.16) | FR-17 | UC-13 | Business administrator, Finance, Procurement and Sustainability officers |
| AI classification (4.17) | AI-01 | UC-02 | Asset custodian |
| Semantic matching, ranking and explanations (4.18–4.19) | AI-02 to AI-05 | UC-06 | Requester |
| Sustainable-action recommendation (4.20) | AI-06 | UC-11 | Sustainability officer |
| Campus assistant (4.21) | AI-07, AI-08 | UC-12 | All roles |
| Generative reporting (4.22) | AI-09, AI-10 | UC-13 | Report data owners |
| AI tracking, overrides and fallback (4.23) | AI-11 to AI-13 | UC-06, UC-12 | All roles |
| Sustainability indicators (6.1) | SU-01 to SU-08 | UC-13 | Sustainability officer, Finance officer |
