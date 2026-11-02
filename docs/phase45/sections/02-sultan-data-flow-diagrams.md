# 2. Data-Flow Diagrams

## 2.1 Level 1

Level 1 splits process 0 into seven processes, one for each main job of the system. Each process name is a verb and a noun, and each data store is named after the entities in our ER diagram (section 8). Figure 2.1 shows processes 1.0 to 4.0 and Figure 2.2 shows processes 5.0 to 7.0. We split Level 1 into two figures so the labels stay readable on A4. When a store or an external entity appears more than once, the copy has an extra line: a line on the left side of a store, or a corner line on an external entity.

![Figure 2.1 Level 1 data-flow diagram, part 1: processes 1.0 to 4.0](images/dfd-level1-a.png)

![Figure 2.2 Level 1 data-flow diagram, part 2: processes 5.0 to 7.0](images/dfd-level1-b.png)

**Table 2.1 Level 1 processes**

<!-- widths: 600,2300,3960,2500 -->
| # | Process | What it does | SRS links |
|---|---|---|---|
| 1.0 | Manage Accounts and Settings | Creates accounts, applies authorised roles, and keeps departments, categories and thresholds. | FR-01 to FR-03, UC-01 |
| 2.0 | Register and Publish Assets | Registers assets with AI category suggestions and publishes a listing once its release is approved. | FR-04 to FR-06, AI-01, UC-02, UC-03 |
| 3.0 | Request, Match and Reserve Assets | Records requests, finds eligible listings, ranks them with AI and holds the chosen item. | FR-07 to FR-09, AI-02 to AI-05, UC-04 to UC-07 |
| 4.0 | Answer Assistant Questions | Answers questions using only the records the user may see. | AI-07, AI-08, UC-12 |
| 5.0 | Approve and Transfer Assets | Routes every approval stage, sends tasks, and records handover, receipt and the new owner. | FR-10, FR-11, FR-16, BR-01 to BR-10, UC-08, UC-09 |
| 6.0 | Maintain and Retire Assets | Handles defects, inspections, repairs and end-of-life actions, with optional AI advice. | FR-12 to FR-14, AI-06, UC-10, UC-11 |
| 7.0 | Report Impact and History | Builds reports, the asset history and the audit view, with optional AI drafts. | FR-15, FR-17, FR-18, AI-09, AI-10, SU-01 to SU-09, UC-13, UC-14 |

**Table 2.2 Data stores**

<!-- widths: 2300,3060,1900,2100 -->
| Store | Entities (section 8) | Written by | Read by |
|---|---|---|---|
| D1 Users and Settings | Department, User, Role, UserRole, Category | 1.0 | 5.0 |
| D2 Assets and Listings | Asset, Listing, Attachment | 2.0, 5.0, 6.0 | 3.0, 4.0, 6.0 |
| D3 Requests and Holds | ResourceRequest, Reservation | 3.0 | 5.0 |
| D4 AI Records | MatchRecommendation, AiSuggestion, ModelVersion | 2.0, 3.0, 4.0 | 7.0 |
| D5 Approvals and Transfers | Approval, Transfer | 5.0 | 2.0, 3.0, 6.0, 7.0 |
| D6 Maintenance Records | Inspection, MaintenanceRecord, EndOfLifeAction | 6.0 | 5.0, 7.0 |
| D7 Sustainability Impacts | SustainabilityImpact | 5.0, 6.0 | 7.0 |
| D8 Audit Log | AuditLog | 1.0, 5.0 and every other process | 7.0 |

Every process writes audit entries to D8 (FR-18.1). To keep the figures readable, we draw this flow for 1.0 and 5.0 only. The tasks sent to users, such as approval tasks and work orders, are the notifications in FR-16, and the Notification entity keeps them for each user.

## 2.2 Level 2 of 3.0 Request, Match and Reserve Assets

We opened 3.0 because it holds the main AI call and decides which items a requester sees, so a mistake here reaches every later step.

![Figure 2.3 Level 2 data-flow diagram of 3.0 Request, Match and Reserve Assets](images/dfd-level2-3.png)

- **3.1 Record Request** saves the request and gives it a unique ID (FR-07.9).
- **3.2 Check Eligibility** keeps only listings that pass the classic rules for access, quantity, condition, compatibility and date (BR-14, AI-03.1), and only for requests the department has approved (BR-03).
- **3.3 Rank and Explain Matches** sends the request text to the AI Provider, scores each eligible listing with the weights in SRS Table 4.1, and stores each recommendation with its confidence and model version (AI-04, AI-05, AI-12). If the AI does not answer in time, 3.3 returns the eligible listings in classic order instead (AI-13).
- **3.4 Record Choice and Hold** records the chosen item, and the reason when the requester does not pick the top match, then creates the hold (FR-09, AI-05.2).

The flows that cross the dashed line in Figure 2.3 are exactly the eight flows of 3.0 on Level 1, as Table 2.4 shows.

## 2.3 Balancing Table

Table 2.3 shows that every flow on the context diagram appears on Level 1 with the same name, the same direction and the same external entity. Grouped flows list their parts on Level 1.

**Table 2.3 Balancing the context diagram and Level 1**

<!-- widths: 400,2200,1500,700,1300,3260 -->
| # | Context flow | External entity | In or out | Level 1 process | Parts on Level 1 |
|---|---|---|---|---|---|
| 1 | resource request, match choice, assistant question | Requester | in | 3.0, 4.0 | resource request, match choice (3.0); assistant question (4.0) |
| 2 | ranked matches, request status, assistant answer | Requester | out | 3.0, 4.0 | ranked matches, request status (3.0); assistant answer (4.0) |
| 3 | asset details, handover records, defect and end-of-life reports | Asset Custodian | in | 2.0, 5.0, 6.0 | asset details (2.0); handover records (5.0); defect and end-of-life reports (6.0) |
| 4 | suggested category, transfer tasks, asset history | Asset Custodian | out | 2.0, 5.0, 7.0 | suggested category (2.0); transfer tasks (5.0); asset history (7.0) |
| 5 | inspection and repair records | Maintenance Staff | in | 6.0 | inspection and repair records (6.0) |
| 6 | work orders | Maintenance Staff | out | 6.0 | work orders (6.0) |
| 7 | approval decisions | Approvers | in | 5.0 | approval decisions (5.0) |
| 8 | approval tasks, finance and reuse reports | Approvers | out | 5.0, 7.0 | approval tasks (5.0); finance and reuse reports (7.0) |
| 9 | end-of-life reviews | Sustainability Officer | in | 5.0 | end-of-life reviews (5.0) |
| 10 | review tasks, impact report | Sustainability Officer | out | 5.0, 7.0 | review tasks (5.0); impact report (7.0) |
| 11 | account details, role assignments, settings, report requests | Administrators | in | 1.0, 7.0 | account details, role assignments, settings (1.0); report requests (7.0) |
| 12 | account status, operational and audit reports | Administrators | out | 1.0, 7.0 | account status (1.0); operational and audit reports (7.0) |
| 13 | approved text fields | AI Provider | out | 2.0, 3.0, 4.0, 6.0, 7.0 | asset text (2.0); request text (3.0); question context (4.0); asset condition text (6.0); report figures (7.0) |
| 14 | AI output | AI Provider | in | 2.0, 3.0, 4.0, 6.0, 7.0 | category and tags (2.0); vectors, rankings and reasons (3.0); draft answer (4.0); action advice (6.0); draft report text (7.0) |

All 14 context flows match. Level 1 adds no new flows to or from an external entity.

**Table 2.4 Balancing Level 1 process 3.0 and its Level 2**

<!-- widths: 3000,2000,4360 -->
| Flow of 3.0 on Level 1 | From or to | Level 2 process |
|---|---|---|
| resource request, match choice | from Requester | 3.1 (resource request); 3.4 (match choice) |
| ranked matches, request status | to Requester | 3.3 (ranked matches); 3.1 and 3.4 (request status) |
| request text | to AI Provider | 3.3 |
| vectors, rankings and reasons | from AI Provider | 3.3 |
| published listings | from D2 | 3.2 |
| request decisions | from D5 | 3.2 |
| request and hold records | to D3 | 3.1 (request record); 3.4 (hold record) |
| match recommendations | to D4 | 3.3 |
