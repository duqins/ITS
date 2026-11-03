# 2. Data-Flow Diagrams

## 2.1 Level 1

Level 1 splits process 0 into seven processes, one for each main job of the system. Each process name is a verb and a noun, and each data store is named after the entities in our ER diagram (section 8). Figure 2.1 shows all of Level 1 in one diagram on an A3 page. Each external entity and each data store appears once, and lines join it to every process that uses it. Processes 1.0 to 4.0 are in the top row and 7.0, 5.0 and 6.0 are in the bottom row, with the data stores between the rows. D6 and D7 sit under the bottom row because only 5.0, 6.0 and 7.0 use them.

<!-- page: a3-landscape -->
![Figure 2.1 Level 1 data-flow diagram](images/dfd-level1.png)

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
| D1 Users and Settings | Department, User, Role, UserRole, Category, Notification | 1.0; Notification records from every process that sends a task | 2.0, 5.0, 6.0 |
| D2 Assets and Listings | Asset, Listing, Attachment | 2.0, 5.0, 6.0 | 3.0, 4.0, 5.0, 6.0, 7.0 |
| D3 Requests and Holds | ResourceRequest, Reservation | 3.0, 5.0 | 5.0, 7.0 |
| D4 AI Records | MatchRecommendation, AiSuggestion, ModelVersion | 2.0, 3.0, 4.0, 6.0, 7.0 | 7.0 |
| D5 Approvals and Transfers | Approval, Transfer | 5.0 | 2.0, 3.0, 6.0, 7.0 |
| D6 Maintenance Records | Inspection, MaintenanceRecord, EndOfLifeAction | 6.0 | 5.0, 7.0 |
| D7 Sustainability Impacts | SustainabilityImpact | 5.0, 6.0 | 7.0 |
| D8 Audit Log | AuditLog | 1.0, 5.0 and every other process | 7.0 |

Every process writes audit entries to D8 (FR-18.1). To keep the figure readable, we draw this flow for 1.0 and 5.0 only. Two more flows are left out for the same reason. Every process checks the signed-in user's roles in D1 before it acts (FR-02.2), and every process that sends a task, such as an approval task or a work order, writes it to D1 as a Notification record for that user (FR-16).

## 2.2 Balancing the Context Diagram and Level 1

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
| 14 | AI output | AI Provider | in | 2.0, 3.0, 4.0, 6.0, 7.0 | category and tags (2.0); embedding vectors (3.0); draft answer (4.0); action advice (6.0); draft report text (7.0) |

All 14 context flows match. Level 1 adds no new flows to or from an external entity.

## 2.3 Level 2 Diagrams

Every Level 1 process has its own Level 2. In each one, the sub-processes sit inside the dashed line, every external entity and data store appears once, and the flows that cross the dashed line are exactly the flows of that process on Level 1, as its balancing table shows. As on Level 1, the audit-log flow to D8 is drawn only where Level 1 draws it.

<!-- pagebreak -->
### 2.3.1 Level 2 of 1.0 Manage Accounts and Settings

![Figure 2.2 Level 2 data-flow diagram of 1.0 Manage Accounts and Settings](images/dfd-level2-1.png)

- **1.1 Check Account Details** checks the name, staff email, department and status that the System administrator enters to create, update or deactivate an account, and refuses conflicting details (FR-01.1, UC-01).
- **1.2 Authorise Role Assignments** lets the System administrator apply a role only after a Business administrator has authorised it, and the authoriser cannot be the person who asked for the role (FR-01.3, BR-01, BR-02). One user can hold several roles, each tied to departments (FR-01.2). Refused assignments are passed on too, so they are logged.
- **1.3 Check Setting Changes** checks changes to departments, categories, control flags and thresholds. It refuses to delete a department or category that records still use and offers to deactivate it instead (FR-03.1 to FR-03.5).
- **1.4 Save Changes** saves the checked changes in D1 and writes an audit entry for each change and each refused attempt to D8 (FR-18.1, FR-02.3, BR-17). It returns the account status. After a deactivation, the status says the sessions have ended and lists the account's open approval tasks for reassignment (FR-01.4).

The flows that cross the dashed line in Figure 2.2 are exactly the four flows of 1.0 on Level 1, as Table 2.4 shows.

**Table 2.4 Balancing Level 1 process 1.0 and its Level 2**

<!-- widths: 3000,2000,4360 -->
| Flow of 1.0 on Level 1 | From or to | Level 2 process |
|---|---|---|
| account details, role assignments, settings | from Administrators | 1.1 (account details); 1.2 (role assignments); 1.3 (settings) |
| account status | to Administrators | 1.4 |
| user, role and setting records | to D1 | 1.4 |
| audit entries | to D8 | 1.4 |

<!-- pagebreak -->
### 2.3.2 Level 2 of 2.0 Register and Publish Assets

![Figure 2.3 Level 2 data-flow diagram of 2.0 Register and Publish Assets](images/dfd-level2-2.png)

- **2.1 Check Asset Details** takes the details the custodian enters, gives the asset a unique ID, checks the required fields and uploads, and warns about a possible duplicate (FR-04.1, FR-04.2, FR-04.5). It sends the description to 2.2 and the checked details to 2.3.
- **2.2 Suggest Category** sends the asset text to the AI Provider and gets back a category and tags. It checks that the category is one of the categories in D1 and applies the 0.60 confidence threshold, so a weaker suggestion is shown only as an option (AI-01.1 to AI-01.3, AI-05.4). It shows the suggestion to the custodian and stores it in D4 with its model version and confidence (AI-12.1). If the AI does not answer, the custodian picks the category by hand (AI-13).
- **2.3 Save Asset Record** saves the asset once a custodian or department representative other than the creator confirms it. The record is saved as In service or In storage, with the confirming user and the verification date (FR-04.3, FR-04.4, BR-02). Only the suggestions the custodian accepted go into the record (AI-01.4), and a later edit keeps the old values in the history (FR-04.6). The confirmed asset, with any listing offer the custodian made, goes to 2.4.
- **2.4 Publish Listing** makes a listing for a confirmed asset with the quantity offered, condition, location, available-from date, restrictions and reason, and saves it as Pending release approval (FR-06.1, FR-06.2). Once D5 holds the owning department representative's release decision, it publishes the listing (FR-06.3, BR-04).

The flows that cross the dashed line in Figure 2.3 are exactly the eight flows of 2.0 on Level 1, as Table 2.5 shows.

**Table 2.5 Balancing Level 1 process 2.0 and its Level 2**

<!-- widths: 3000,2000,4360 -->
| Flow of 2.0 on Level 1 | From or to | Level 2 process |
|---|---|---|
| asset details | from Asset Custodian | 2.1 |
| suggested category | to Asset Custodian | 2.2 |
| asset text | to AI Provider | 2.2 |
| category and tags | from AI Provider | 2.2 |
| categories | from D1 | 2.2 |
| release decisions | from D5 | 2.4 |
| asset and listing records | to D2 | 2.3 (asset records); 2.4 (listing records) |
| AI suggestions | to D4 | 2.2 |

<!-- pagebreak -->
### 2.3.3 Level 2 of 3.0 Request, Match and Reserve Assets

3.0 holds the main AI call and decides which items a requester sees, so a mistake here reaches every later step.

![Figure 2.4 Level 2 data-flow diagram of 3.0 Request, Match and Reserve Assets](images/dfd-level2-3.png)

- **3.1 Record Request** saves the request and gives it a unique ID (FR-07.9).
- **3.2 Check Eligibility** keeps only listings that pass the classic rules for access, quantity, condition, compatibility and date (BR-14, AI-03.1), and only for requests the department has approved (BR-03).
- **3.3 Rank and Explain Matches** sends the request text to the AI Provider, scores each eligible listing with the weights in SRS Table 4.1, and stores each recommendation with its model version and its confidence, which is "unavailable" with the current embedding model (AI-04, AI-05, AI-12). If the AI does not answer in time, 3.3 returns the eligible listings in classic order instead (AI-13).
- **3.4 Record Choice and Hold** records the chosen item in D4, with the reason when the requester does not pick the top match, then creates the hold in D3 (FR-09, AI-05.2).

The flows that cross the dashed line in Figure 2.4 are exactly the eight flows of 3.0 on Level 1, as Table 2.6 shows.

**Table 2.6 Balancing Level 1 process 3.0 and its Level 2**

<!-- widths: 3000,2000,4360 -->
| Flow of 3.0 on Level 1 | From or to | Level 2 process |
|---|---|---|
| resource request, match choice | from Requester | 3.1 (resource request); 3.4 (match choice) |
| ranked matches, request status | to Requester | 3.3 (ranked matches); 3.1 and 3.4 (request status) |
| request text | to AI Provider | 3.3 |
| embedding vectors | from AI Provider | 3.3 |
| published listings | from D2 | 3.2 |
| request decisions | from D5 | 3.2 |
| request and hold records | to D3 | 3.1 (request record); 3.4 (hold record) |
| match records | to D4 | 3.3 (match recommendations); 3.4 (match response) |

<!-- pagebreak -->
### 2.3.4 Level 2 of 4.0 Answer Assistant Questions

![Figure 2.5 Level 2 data-flow diagram of 4.0 Answer Assistant Questions](images/dfd-level2-4.png)

- **4.1 Check Question Access** reads the question and works out what kind it is: a resource search, asset history, request status, guidance or a draft request. It limits the question to the records the user's roles and departments allow (AI-07.1, AI-07.2, FR-02.2). A question about records the user may not see gets no records, so the answer cannot reveal them (UC-12).
- **4.2 Gather Permitted Records** reads only the permitted listings in D2 that fit the question. It sends the question and those listings' approved fields to the AI Provider, and passes the same records to 4.3 as sources (AI-07.2, AI-07.3).
- **4.3 Check and Return Answer** checks the draft answer against the source records and adds references. If no permitted record supports a claim, the answer says it cannot confirm it (AI-07.3, AI-07.4). When the answer is a draft request, it only shows the proposed fields. Nothing is submitted until the user confirms it, and then it follows the normal request steps in 3.0 (AI-08.1, AI-08.2, BR-15). 4.3 saves the question, sources, answer and model version in D4 (AI-12.1). If the AI does not answer in time, it offers classic search instead (AI-13).

The flows that cross the dashed line in Figure 2.5 are exactly the six flows of 4.0 on Level 1, as Table 2.7 shows.

**Table 2.7 Balancing Level 1 process 4.0 and its Level 2**

<!-- widths: 3000,2000,4360 -->
| Flow of 4.0 on Level 1 | From or to | Level 2 process |
|---|---|---|
| assistant question | from Requester | 4.1 |
| assistant answer | to Requester | 4.3 |
| question context | to AI Provider | 4.2 |
| draft answer | from AI Provider | 4.3 |
| permitted listings | from D2 | 4.2 |
| assistant records | to D4 | 4.3 |

<!-- pagebreak -->
### 2.3.5 Level 2 of 5.0 Approve and Transfer Assets

![Figure 2.6 Level 2 data-flow diagram of 5.0 Approve and Transfer Assets](images/dfd-level2-5.png)

- **5.1 Plan Approval Stages** finds the records that wait for a decision: listings waiting for release in D2, requests and holds in D3, and repair estimates and end-of-life proposals in D6. For each record it works out the stages in SRS Table 5.2, including Finance or Procurement when BR-06 or BR-07 applies. It reads D1 to find the users who hold the required role (FR-10.1, BR-03 to BR-09).
- **5.2 Record Approval Decisions** sends each approval task to the Approvers and each review task to the Sustainability Officer, one stage at a time (FR-10.2, FR-14.3, FR-16.1). It refuses a decision by the record's own creator or requester (FR-10.4, BR-02) and asks for a reason on every rejection or request for changes (FR-10.3, BR-20). It saves each decision in D5 with the approver, role, time, reason and record version (FR-10.6), and writes an audit entry (FR-18.1). It also sets the new request or hold state in D3, for example Open after department approval (BR-03), and releases the held quantity after a rejection (BR-20). When every stage of a transfer is approved, it passes the transfer to 5.3 (BR-05, BR-06).
- **5.3 Confirm Handover and Receipt** sends transfer tasks to the asset custodians and records the handover and the receipt with quantity and condition (FR-11.3, FR-11.4, UC-09). It saves the transfer record in D5. If the receipt does not match the handover, the transfer becomes Disputed and the owner does not change (FR-11.5).
- **5.4 Complete Transfer** changes the owning department, custodian and location in D2 only after a matching receipt (FR-11.4, BR-13). It reads the category's emission factors in D1 and saves the impact of the transfer in D7, using the formulas in section 12 (SU-02, SU-07).

As on Level 1, we draw the audit flow once, from 5.2. The flows that cross the dashed line in Figure 2.6 are exactly the 15 flows of 5.0 on Level 1, as Table 2.8 shows.

**Table 2.8 Balancing Level 1 process 5.0 and its Level 2**

<!-- widths: 3000,2000,4360 -->
| Flow of 5.0 on Level 1 | From or to | Level 2 process |
|---|---|---|
| approval decisions | from Approvers | 5.2 |
| approval tasks | to Approvers | 5.2 |
| end-of-life reviews | from Sustainability Officer | 5.2 |
| review tasks | to Sustainability Officer | 5.2 |
| handover records | from Asset Custodian | 5.3 |
| transfer tasks | to Asset Custodian | 5.3 |
| roles and emission factors | from D1 | 5.1 (roles); 5.4 (emission factors) |
| holds and requests | from D3 | 5.1 |
| hold and request states | to D3 | 5.2 |
| end-of-life and repair cases | from D6 | 5.1 |
| approval and transfer records | to D5 | 5.2 (approval records); 5.3 (transfer records) |
| listings to approve | from D2 | 5.1 |
| new owner and location | to D2 | 5.4 |
| transfer impacts | to D7 | 5.4 |
| audit entries | to D8 | 5.2 |

<!-- pagebreak -->
### 2.3.6 Level 2 of 6.0 Maintain and Retire Assets

![Figure 2.7 Level 2 data-flow diagram of 6.0 Maintain and Retire Assets](images/dfd-level2-6.png)

- **6.1 Open Work Order** takes a defect report from the asset custodian, opens a work order in state Reported (MW-01) and sends it to the maintenance staff (FR-13.1, FR-16.2, UC-10).
- **6.2 Prepare End-of-Life Proposal** takes an end-of-life report and reads the asset details from D2 (FR-14.1, UC-11). When advice is asked for, it sends the asset condition text to the AI Provider and saves the action advice in D4 with its model version (AI-06, AI-12). The advice follows the reuse-first order and is only a suggestion (BR-08, BR-15). If the AI does not answer, the proposal goes on without advice (AI-13). 6.2 asks for a reason when recycling or disposal is proposed, and for the EHS and data-erasure evidence where BR-09 applies (FR-14.2, FR-14.4).
- **6.3 Update Maintenance Records** saves inspections, repairs and end-of-life proposals in D6 (FR-12.1, FR-13.2, FR-13.4, FR-14.1). It reads the approval decisions in D5, so repair work starts only after its cost is approved and an end-of-life action is carried out only after both reviews (BR-07, BR-08, FR-13.5). It writes the asset's new condition and state to D2: Under maintenance, back in service, Retired when not repairable, or the final state after an approved action (FR-12.2, FR-13.3, FR-13.6, FR-13.7, FR-14.5, FR-14.6).
- **6.4 Calculate Life-Cycle Impact** takes each completed repair or end-of-life action, reads the emission factors in D1 and saves the impact in D7, using the formulas in section 12 (SU-02, SU-06, SU-07, SU-09).

The flows that cross the dashed line in Figure 2.7 are exactly the 12 flows of 6.0 on Level 1, as Table 2.9 shows.

**Table 2.9 Balancing Level 1 process 6.0 and its Level 2**

<!-- widths: 3000,2000,4360 -->
| Flow of 6.0 on Level 1 | From or to | Level 2 process |
|---|---|---|
| defect and end-of-life reports | from Asset Custodian | 6.1 (defect reports); 6.2 (end-of-life reports) |
| inspection and repair records | from Maintenance Staff | 6.3 |
| work orders | to Maintenance Staff | 6.1 |
| asset condition text | to AI Provider | 6.2 |
| action advice | from AI Provider | 6.2 |
| emission factors | from D1 | 6.4 |
| asset details | from D2 | 6.2 |
| condition and state | to D2 | 6.3 |
| approval decisions | from D5 | 6.3 |
| maintenance records | to D6 | 6.3 |
| AI suggestions | to D4 | 6.2 |
| impact records | to D7 | 6.4 |

<!-- pagebreak -->
### 2.3.7 Level 2 of 7.0 Report Impact and History

![Figure 2.8 Level 2 data-flow diagram of 7.0 Report Impact and History](images/dfd-level2-7.png)

- **7.1 Calculate Report Totals** takes a report request with its period and departments, reads the records of that period from D2 to D7 and works out the counts, totals and sustainability indicators with the formulas in section 12 (FR-17.1, FR-17.2, SU-01 to SU-09). The same totals go to 7.2 and 7.3, so the AI text and the normal report use the same figures (AI-09.2).
- **7.2 Draft Report Summary** sends the report figures to the AI Provider and gets back draft text. It labels the text as an AI draft, links each claim to a total and saves it in D4 with its model version (AI-09.3, AI-10.1, AI-12). If the AI is not available, the report goes out without a summary (AI-13).
- **7.3 Issue Reports** puts the totals, the draft summary and the audit results into the operational and audit reports for the administrators, the finance and reuse reports for the approvers and the impact report for the Sustainability Officer (FR-17.1, UC-13). Each report stays Draft until its data owner reviews it (FR-17.4, BR-10, AI-10.2), and each indicator shows its formula and sources (SU-08).
- **7.4 Trace Asset History** reads the audit entries in D8 and lists the events of one asset in time order for the asset custodian (FR-15.1, UC-14). It also passes audit search results to 7.3 for the audit report (FR-18.3). It never changes an entry (FR-18.2, BR-17).

The flows that cross the dashed line in Figure 2.8 are exactly the 15 flows of 7.0 on Level 1, as Table 2.10 shows.

**Table 2.10 Balancing Level 1 process 7.0 and its Level 2**

<!-- widths: 3000,2000,4360 -->
| Flow of 7.0 on Level 1 | From or to | Level 2 process |
|---|---|---|
| report requests | from Administrators | 7.1 |
| operational and audit reports | to Administrators | 7.3 |
| finance and reuse reports | to Approvers | 7.3 |
| impact report | to Sustainability Officer | 7.3 |
| asset history | to Asset Custodian | 7.4 |
| report figures | to AI Provider | 7.2 |
| draft report text | from AI Provider | 7.2 |
| asset and listing records | from D2 | 7.1 |
| request and hold records | from D3 | 7.1 |
| AI records | from D4 | 7.1 |
| AI suggestions | to D4 | 7.2 |
| transfer records | from D5 | 7.1 |
| maintenance records | from D6 | 7.1 |
| impact records | from D7 | 7.1 |
| audit entries | from D8 | 7.4 |
