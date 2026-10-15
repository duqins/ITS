## 4.2 User Accounts and Access Control

### 4.2.1 Description and Priority

Staff log in and only see what their roles allow. A person can have more than one role, each tied to a department. Giving someone a role takes two people: a Business administrator approves it and a System administrator sets it up, so IT access never turns into approval power. Based on Phase 1 FR-01 and FR-02. Use case UC-01. **Priority: Essential (Must, High).**

### 4.2.2 Stimulus/Response Sequences

1. *Business administrator* requests a role for a user in a department. *System* records the request as waiting for authorisation.
2. *Business administrator* authorises; *System administrator* applies it. *System* activates the role and writes an audit entry.
3. *User* signs in. *System* shows the dashboard with the user's tasks and notifications for all their roles.
4. *User* attempts an action their roles do not allow. *System* refuses it, names the role required and logs the attempt.

### 4.2.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-01.1 | The system shall allow the System administrator to create, update and deactivate user accounts with name, staff email, department and account status. |
| FR-01.2 | The system shall allow one user to hold several of the nine roles, each limited to one or more named departments. |
| FR-01.3 | When a role assignment is requested, the system shall require authorisation by a Business administrator before a System administrator can apply it (BR-01). |
| FR-01.4 | When an account is deactivated, the system shall end its active sessions and list its open approval tasks for reassignment by the Business administrator. |
| FR-02.1 | The system shall require authentication before showing any page other than the sign-in page. |
| FR-02.2 | The system shall check the user's role and department on the server for every protected action, including actions proposed through the campus assistant. |
| FR-02.3 | If a user attempts an action their roles do not permit, then the system shall refuse it, state the role required and record the attempt in the audit log. |
| FR-02.4 | If five consecutive sign-in attempts fail for one account, then the system shall block further attempts on that account for 15 minutes. |

## 4.3 Departments, Categories and Approval Settings

### 4.3.1 Description and Priority

Business administrators keep the basic lists up to date: departments and who represents them, asset categories, and the limits used for approvals and reservations. Based on Phase 1 FR-03. Use case UC-01. **Priority: Essential (Must, High)**, except FR-03.3, which is Desirable. Until it's built, the proposed values in Appendix C are set in the configuration.

### 4.3.2 Stimulus/Response Sequences

1. *Business administrator* adds a department and names its representatives and custodians. *System* makes the department available for assets, requests and approval routing.
2. *Business administrator* adds or deactivates a category. *System* updates the category list used by forms, search and AI classification.

### 4.3.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-03.1 | The system shall allow a Business administrator to create and update departments with a name, a code, department representatives and asset custodians. |
| FR-03.2 | The system shall allow a Business administrator to maintain categories and subcategories, each with a counting unit (item, set or kilogram) and an optional emission-factor reference (SU-08). |
| FR-03.3 | The system shall allow a Business administrator to change the approval thresholds (TBD-1, TBD-2), the reservation hold period (TBD-3), the verification period (TBD-4) and the reminder period (TBD-5), recording each change with an effective date; a change shall not alter approvals already in progress. **Desirable (Should).** |
| FR-03.4 | The system shall allow a Business administrator to mark a category as procurement-controlled (BR-06) or as requiring special handling (BR-09). |
| FR-03.5 | If a Business administrator tries to delete a category or department that existing records use, then the system shall refuse and offer to deactivate it instead. |

## 4.4 Asset Registration and Records

### 4.4.1 Description and Priority

Custodians and department representatives register assets with all the details the project description asks for, confirm them and keep them up to date. Each asset has a state and, separately, counts of how many units are available, reserved and allocated. The AI suggestions for category and description are in 4.16. Based on Phase 1 FR-04 and FR-05. Use case UC-02. **Priority: Essential (Must, High).**

### 4.4.2 Stimulus/Response Sequences

1. *Custodian* enters the asset details, photographs and documents. *System* validates the fields and requests AI suggestions (4.16).
2. *Custodian* accepts, edits or rejects each suggestion and confirms the record. *System* saves it as In service or In storage and records who confirmed it.
3. *Custodian* updates the condition or location later. *System* keeps the previous values in the asset history.

### 4.4.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-04.1 | The system shall allow a custodian or department representative to register an asset with a system-generated unique ID, name, description, category and subcategory, quantity and unit, owning department, custodian, location (building and room), purchase date, purchase or estimated value, condition (New, Good, Fair, Poor, Not working), technical specifications, up to five photographs (JPG or PNG, 5 MB each) and supporting documents (PDF, 10 MB each). |
| FR-04.2 | If a mandatory field is missing or invalid, then the system shall keep the asset in Draft (AS-01) and show which fields need correction. |
| FR-04.3 | When the custodian or department representative confirms the record, the system shall save it as In service (AS-02) or In storage (AS-03) and record the confirming user and time. |
| FR-04.4 | The system shall record the date and the user of each asset's most recent availability and condition verification. |
| FR-04.5 | When a new asset has the same department, category, name and specifications as an existing asset, the system shall warn of a possible duplicate and require confirmation before saving. |
| FR-04.6 | When a confirmed asset record is edited, the system shall keep the previous values in the asset's history (FR-15.1). |
| FR-05.1 | The system shall keep each asset in exactly one life-cycle state from section 4.1.1. |
| FR-05.2 | If a user or process attempts a state change that section 4.1 does not allow, then the system shall reject it and record the attempt in the audit log. |
| FR-05.3 | The system shall track the available, reserved and allocated quantity of each asset so that their sum never exceeds the total quantity (BR-11). |
| FR-05.4 | While an asset is Under maintenance, In transfer or Retired, the system shall not allow its quantity to be published or reserved. |

## 4.5 Resource Publication

### 4.5.1 Description and Priority

A department offers an item it doesn't need to the rest of campus by listing it. The department representative has to approve the listing before anyone else can see it. Based on Phase 1 FR-06. Use case UC-03. **Priority: Essential (Must, High).**

### 4.5.2 Stimulus/Response Sequences

1. *Custodian* creates a listing for an asset in service or in storage. *System* checks the quantity and sends the listing for release approval.
2. *Department representative* approves. *System* publishes the listing to all authorised staff and notifies the custodian.
3. *Custodian* withdraws the listing. *System* cancels pending reservations and notifies the requesters.

### 4.5.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-06.1 | The system shall allow a custodian or department representative to create a listing for an asset that is In service or In storage, stating the quantity offered, condition, location, available-from date, restrictions (for example "collection required") and reason (surplus, underutilised or unwanted). |
| FR-06.2 | When a listing is submitted, the system shall create a release-approval task for the owning department's representative and set the listing to Pending release approval (LS-02, BR-04). |
| FR-06.3 | When the release is approved, the system shall publish the listing (LS-03) to authorised staff, showing quantity, condition, location, restrictions, custodian and the last verification date. |
| FR-06.4 | If the asset's last verification is older than the verification period (TBD-4), then the system shall show "Verification needed" on the listing and block reservation confirmation until the custodian re-verifies it (BR-16). |
| FR-06.5 | The system shall allow the owning department to withdraw a listing (LS-05) unless an approved transfer for it is in progress (BR-19); withdrawal shall cancel its pending reservations and notify the requesters. |
| FR-06.6 | When the whole offered quantity has been transferred, the system shall close the listing (LS-06). |

## 4.6 Resource Requests

### 4.6.1 Description and Priority

A requester describes what their department needs. Once the department representative approves it, the requester can search, look at matches and reserve an item. The request always shows its status and who has to act next. Based on Phase 1 FR-07. Use case UC-04. **Priority: Essential (Must, High).**

### 4.6.2 Stimulus/Response Sequences

1. *Requester* fills in the request form or confirms an assistant draft. *System* validates it and sends it for department approval.
2. *Department representative* approves. *System* opens the request and shows eligible matches (4.17–4.18).
3. *Requester* changes the quantity, specification or date of an open request. *System* returns it for department approval.
4. *Requester* finds no suitable item and closes the request. *System* records the outcome as No suitable item.

### 4.6.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-07.1 | The system shall allow a requester to create a request with category, purpose, technical specifications, quantity, minimum acceptable condition, urgency (Low, Normal, High), delivery location, required-by date and an optional plain-language description. |
| FR-07.2 | If the required-by date is in the past or the quantity is not a positive whole number, then the system shall refuse submission and explain the error. |
| FR-07.3 | When a request is submitted, the system shall set it to Pending department approval (RQ-02) and create an approval task for the requester's department representative (BR-03). |
| FR-07.4 | If the quantity, specifications or required-by date of an approved request change, then the system shall return the request to Pending department approval (RQ-02). |
| FR-07.5 | The system shall show the requester the current state, the role responsible for the next step and every decision taken on the request. |
| FR-07.6 | The system shall allow the requester to cancel a request before it is Fulfilled; cancellation shall release any reservation linked to it (BR-20). |
| FR-07.7 | When the required-by date passes before fulfilment, the system shall set the request to Expired (RQ-10), release any linked reservation and notify the requester. |
| FR-07.8 | When the requester closes a request because no eligible asset exists, the system shall record it as No suitable item (RQ-07), state that the normal purchasing process may proceed outside Dawra Campus, and exclude it from avoided-purchase figures (BR-18). |
| FR-07.9 | When a request is submitted, the system shall give it a unique request ID that stays the same for the life of the request and appears on every notification and approval task about it. |

## 4.7 Search and Filtering

### 4.7.1 Description and Priority

Staff search listed items by keyword and filters. This normal search always works, with or without AI (AI-13). The AI matching is in 4.17. Based on Phase 1 FR-08. Use case UC-05. **Priority: Essential (Must, High).**

### 4.7.2 Stimulus/Response Sequences

1. *User* enters keywords and selects filters. *System* returns the authorised listings that match, with the number of results.
2. *User* finds nothing. *System* says no listing matches and offers to start a request with the same criteria.

### 4.7.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-08.1 | The system shall search the name, description, category, tags and specifications of published listings by keyword. |
| FR-08.2 | The system shall filter results by category, condition, department, location, available quantity, asset age, estimated value and life-cycle state, and shall allow filters to be combined. |
| FR-08.3 | The system shall sort results by newest listing, condition or available quantity. |
| FR-08.4 | The system shall return only records the user is authorised to see; unpublished listings shall be visible only to the owning department. |
| FR-08.5 | When no listing matches, the system shall say so and offer to create a request with the same criteria. |
| FR-08.6 | The keyword search and filters shall remain available while the AI services are unavailable. |

## 4.8 Reservations

### 4.8.1 Description and Priority

A requester asks to hold some units of a listed item. The releasing department confirms the hold, which lasts a set time and then runs out unless a transfer gets approved. Reserving an item is not the same as approving the transfer. Based on Phase 1 FR-09. Use case UC-07. **Priority: Essential (Must, High).**

### 4.8.2 Stimulus/Response Sequences

1. *Requester* selects a listing and a quantity for an open request. *System* checks availability and records the reservation as Requested.
2. *Custodian or department representative* confirms. *System* holds the quantity and shows the expiry date to both sides.
3. The hold period ends without a transfer. *System* releases the quantity and notifies both sides.

### 4.8.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-09.1 | The system shall allow a requester with an Open request to request a reservation of a quantity from a Published listing (RV-01). |
| FR-09.2 | If the quantity requested exceeds the available quantity, then the system shall refuse the reservation and show the quantity available (BR-11). |
| FR-09.3 | When the releasing custodian or department representative confirms a reservation, the system shall hold the quantity until the end of the hold period (TBD-3) and reduce the available quantity (RV-02). |
| FR-09.4 | When a hold period ends without an approved transfer, the system shall release the quantity (RV-05) and notify the requester and the custodian (BR-12). |
| FR-09.5 | When two users try to reserve the last available units at the same time, the system shall confirm only one reservation and tell the other user that the quantity is no longer available. |
| FR-09.6 | When a confirmed reservation becomes a transfer, the system shall link the two records and set the reservation to Converted to transfer (RV-04). |
| FR-09.7 | The system shall state on every reservation that the item is held, not yet approved for transfer (BR-15). |

## 4.9 Approval Workflow

### 4.9.1 Description and Priority

Every approval in section 5.5 becomes a task sent to the people with the right role in that department. Approvers see everything they need in one inbox, and every decision is saved with its reason. Based on Phase 1 FR-10. Use case UC-08. **Priority: Essential (Must, High)**, except FR-10.5 and FR-10.8, which are Desirable.

### 4.9.2 Stimulus/Response Sequences

1. A record reaches an approval stage. *System* creates a task for the required role and notifies the approvers.
2. *Approver* opens the task. *System* shows the record summary, the requester, the asset, costs, any AI score and explanation, and the sustainability effect.
3. *Approver* approves, rejects or requests changes. *System* records the decision and moves the record to its next state.

### 4.9.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-10.1 | The system shall create an approval task for each stage in Table 5.2 and assign it to the users holding the required role for the relevant department. |
| FR-10.2 | The system shall show each approver one inbox listing pending tasks with the record summary, requester, asset, quantity, costs, any AI score and explanation, and sustainability effect. |
| FR-10.3 | The system shall allow an approver to approve, reject or request changes; if the approver rejects or requests changes, then the system shall require a reason (BR-20). |
| FR-10.4 | If a user is the requester or creator of the record being approved, then the system shall not allow that user to approve it (BR-02). |
| FR-10.5 | When an approval task has been pending for longer than the reminder period (TBD-5), the system shall remind the approvers and mark the task as overdue on their dashboard. **Desirable (Should).** |
| FR-10.6 | The system shall record each decision with the approver, role, date and time, reason and the version of the record approved. |
| FR-10.7 | If an approved record is changed in a way that affects the decision (quantity, value, recipient or action), then the system shall withdraw the approval and create a new task. |
| FR-10.8 | The system shall allow a Business administrator to reassign a task to another user who holds the required role, without granting the administrator approval authority (BR-01). **Desirable (Should).** |

## 4.10 Transfer, Handover and Receipt

### 4.10.1 Description and Priority

A transfer moves an item from one department to another. Both departments have to approve it, plus Finance or Procurement when a limit applies. The owner and location only change once the receiving custodian confirms they got the item. Based on Phase 1 FR-11. Use case UC-09. **Priority: Essential (Must, High).**

### 4.10.2 Stimulus/Response Sequences

1. A reservation is confirmed and the requester proceeds. *System* creates the transfer and starts the approvals in Table 5.2.
2. All approvals are given. *System* asks both custodians to arrange collection or delivery.
3. *Releasing custodian* confirms handover, quantity and condition. *System* marks the asset In transfer.
4. *Receiving custodian* confirms receipt. *System* updates ownership, custody and location, completes the transfer and fulfils the request.
5. *Receiving custodian* reports a difference. *System* marks the transfer Disputed and notifies both department representatives.

### 4.10.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-11.1 | When a requester proceeds with a confirmed reservation, the system shall create a transfer record with the asset, quantity, releasing and receiving departments and custodians, collection or delivery arrangement, planned date and supporting documents. |
| FR-11.2 | The system shall require release approval and receipt approval (BR-05), and policy approval where BR-06 applies, before setting a transfer to Approved (TR-04). |
| FR-11.3 | When the releasing custodian confirms handover with quantity and condition, the system shall set the transfer to Handed over (TR-05) and the asset to In transfer (AS-05). |
| FR-11.4 | When the receiving custodian confirms receipt of the agreed quantity and condition, the system shall set the transfer to Completed (TR-06), change the owning department, custodian and location, and set the linked request to Fulfilled (BR-13). |
| FR-11.5 | If the receiving custodian records a quantity or condition different from the handover record, then the system shall set the transfer to Disputed (TR-07), keep ownership unchanged and notify both department representatives. |
| FR-11.6 | The system shall allow a transfer to be cancelled before handover and shall then return the held quantity to the listing (TR-09). |
| FR-11.7 | The system shall produce a printable and exportable transfer record with all approvals and confirmations, for reconciliation with the existing KU asset register. |

## 4.11 Inspection, Maintenance and Repair

### 4.11.1 Description and Priority

Staff report problems and record inspections. Maintenance staff check the item, estimate the cost, do the approved work and record what happened. If an item can't be fixed, it goes to the end-of-life review. Based on Phase 1 FR-12 and FR-13. Use case UC-10. **Priority: Essential (Must, High).**

### 4.11.2 Stimulus/Response Sequences

1. *Custodian* reports a defect. *System* opens a work order and notifies maintenance staff.
2. *Maintenance staff* record the assessment and estimated cost. *System* sends the estimate for cost approval (BR-07).
3. *Maintenance staff* complete the work. *System* records the cost and outcome, updates the condition and returns the asset to service.
4. *Maintenance staff* mark the asset not repairable. *System* starts an end-of-life review.

### 4.11.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-12.1 | The system shall allow authorised staff to record an inspection with the asset, date, inspector, findings, condition rating, photographs and recommended follow-up (no action, repair, refurbish or end-of-life review). |
| FR-12.2 | When an inspection rates an asset Not working or unsafe, the system shall block its publication and reservation until it is repaired or an end-of-life decision is made. |
| FR-13.1 | The system shall allow a custodian or department representative to report a defect, which opens a work order in state Reported (MW-01). |
| FR-13.2 | The system shall allow maintenance staff to record the assessment, the estimated cost and the planned work, and shall then route the estimate for approval under BR-07 (MW-03). |
| FR-13.3 | While a work order is Approved or In progress, the system shall keep the asset Under maintenance (AS-04). |
| FR-13.4 | The system shall allow maintenance staff to record the work performed, parts, labour hours, actual cost, outcome and resulting condition. |
| FR-13.5 | If the actual cost exceeds the approved amount, then the system shall require approval of the difference under BR-07 before the work order can be completed. |
| FR-13.6 | When a work order is completed, the system shall update the asset's condition and return it to its previous state (In service or In storage). |
| FR-13.7 | When maintenance staff mark an asset Not repairable, the system shall close the work order (MW-07), set the asset to Retired (AS-06) and open an end-of-life proposal (EL-01). |

## 4.12 Donation, Recycling, Retirement and Disposal

### 4.12.1 Description and Priority

When an item leaves service, the department suggests what to do with it. The Sustainability officer checks that reuse and repair were considered first, and the Finance officer approves the write-off. Throwing it away is the last option. The AI suggestion in 4.19 can help, but it never decides. Based on Phase 1 FR-14. Use case UC-11. **Priority: Desirable (Should, Medium).** It is not in the course's Phase 6 minimum, so we build it right after the essential set (section 6.4). Until then, retired items stay Retired (AS-06) and unavailable.

### 4.12.2 Stimulus/Response Sequences

1. *Department representative* proposes an action with a reason and evidence. *System* shows any AI recommendation and sends the proposal for sustainability review.
2. *Sustainability officer* approves the review. *System* sends it to the Finance officer.
3. *Finance officer* approves. *System* allows the action and asks for evidence when it is done.
4. *Custodian* records completion with evidence. *System* sets the asset's final state and removes it from availability.

### 4.12.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-14.1 | The system shall allow a department representative or custodian to propose an end-of-life action (retain, donate, disassemble for parts, recycle or dispose) with the reason, quantity, proposed recipient or destination and evidence (EL-01). |
| FR-14.2 | If the proposed action is recycling or disposal, then the system shall require a recorded reason why reuse, repair and donation are not suitable (BR-08). |
| FR-14.3 | The system shall route each proposal to the Sustainability officer for review and then to the Finance officer for write-off approval (Table 5.2). |
| FR-14.4 | Where the asset's category requires special handling, the system shall require a recorded EHS consultation and, for devices that store data, a data-erasure record before approval (BR-09). |
| FR-14.5 | When an approved action is carried out, the system shall record the date, responsible person, recipient or destination, quantity and evidence, set the asset's final state (AS-07 to AS-10) and remove the quantity from availability. |
| FR-14.6 | If a proposal is rejected, then the system shall return the asset to the state it had before it was retired (EL-06). |
| FR-14.7 | When an asset is disassembled, the system shall allow its usable parts to be registered as new assets linked to the original record. |

## 4.13 Life-Cycle History and Audit Trail

### 4.13.1 Description and Priority

Every asset has a full history you can read, and every important action goes into an audit log that nobody can change. Based on Phase 1 FR-15 and FR-18. Use case UC-14. **Priority: Essential (Must, High)**, except FR-15.2 and FR-18.3, which are Desirable.

### 4.13.2 Stimulus/Response Sequences

1. *Custodian* opens an asset. *System* shows its history from registration to the present, newest first.
2. *Business administrator* searches the audit log by user and period. *System* lists the matching entries and allows export.

### 4.13.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-15.1 | The system shall show each asset's chronological history: registration, edits, listings, reservations, transfers, inspections, maintenance and end-of-life actions, each with date, actor, approvals, costs and evidence. |
| FR-15.2 | The system shall allow the history to be filtered by event type and period. **Desirable (Should).** |
| FR-18.1 | The system shall write an audit entry for every creation, change, state change, approval decision, role change, refused action and response to an AI output, recording the actor, role, time, record, action, reason and the values before and after. |
| FR-18.2 | The system shall not allow any role to edit or delete an audit entry; corrections shall be recorded as new entries (BR-17). |
| FR-18.3 | The system shall allow a Business administrator to search the audit log by user, record, action and period, and to export the results as CSV. **Desirable (Should).** |
| FR-18.4 | The system shall keep audit entries for the retention period (TBD-7). |

## 4.14 Notifications

### 4.14.1 Description and Priority

Users get a notification in the app whenever something needs their action or something they're involved in changes. Based on Phase 1 FR-16. **Priority: Essential (Must, High)**; FR-16.3 is Desirable and FR-16.6 is a Future enhancement.

### 4.14.2 Stimulus/Response Sequences

1. A task is assigned to a user. *System* shows a notification on the user's dashboard with a link to the task.
2. *User* opens the notification. *System* opens the record and marks the notification as read.

### 4.14.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-16.1 | When an approval task is created or reassigned, the system shall notify the users who can decide it. |
| FR-16.2 | When a request, reservation, transfer, work order or end-of-life action changes state, the system shall notify the requester and the custodians and representatives involved. |
| FR-16.3 | When a reservation is one working day from expiry, the system shall notify the requester and the custodian. **Desirable (Should).** |
| FR-16.4 | The system shall show the number of unread notifications on every page, link each notification to its record and allow it to be marked as read. |
| FR-16.5 | The system shall show a notification only to users who are allowed to view the record it refers to. |
| FR-16.6 | Where email delivery is enabled, the system shall also send each notification by email. **Future enhancement (Could).** |

## 4.15 Conventional Reports and Dashboards

### 4.15.1 Description and Priority

The normal reports give exact numbers that come out the same every time. The AI summaries in 4.21 and the sustainability numbers in 6.1 use these figures. A report only becomes official after the person responsible for that data checks it. Based on Phase 1 FR-17. Use case UC-13. **Priority: Essential (Must, High)**; FR-17.3 is Desirable.

### 4.15.2 Stimulus/Response Sequences

1. *Finance officer* selects a report, a period and departments. *System* produces it with totals and the filters used, marked Draft.
2. *Finance officer* reviews it. *System* marks it "Reviewed by" with the name and date.

### 4.15.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| FR-17.1 | The system shall produce reports on: assets by department and state; available listings; open requests and their age; reservations; approvals (pending, overdue, decided); completed transfers and ownership changes; maintenance history and costs; end-of-life actions; and the sustainability indicators in section 6.1. |
| FR-17.2 | The system shall filter every report by period and department and show the filters, record counts and totals used. |
| FR-17.3 | The system shall export reports as CSV and provide a printable view. **Desirable (Should).** |
| FR-17.4 | The system shall mark each report Draft until its data owner reviews it, then show the reviewer's name and date (BR-10). |
| FR-17.5 | The system shall show each user a dashboard with their pending tasks, their requests, reservations close to expiry and assets needing verification. |
