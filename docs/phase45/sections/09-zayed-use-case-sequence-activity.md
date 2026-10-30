<!-- pagebreak -->
# 9. Use-Case, Sequence and Activity Diagrams

The diagrams keep the Phase 3 roles, use-case IDs, state codes and approval rules. The use-case diagram shows tasks and their participants. Sequence diagrams show messages in time order. Activity diagrams show process steps and choices. The names Asset, ResourceRequest, MatchRecommendation, Reservation, Approval, Transfer and AuditLog follow the data model in section 8.

## 9.1 Use-Case Diagram

A use case is a task the system helps someone complete. An actor is a staff role or outside service involved in a task. Figure 9.1 is the original Phase 3 diagram, with its nine staff roles and fourteen use-case IDs. Its actor links and include and extend links are preserved.

![Figure 9.1 Dawra Campus use-case diagram from Phase 3](images/figure-9-1-use-case-diagram.png)

An include link identifies a step used as part of another task. Check eligibility is included in UC-06 and UC-07; Send notification is included in UC-08. An extend link identifies additional behaviour under a condition. The existing extend link from UC-06 to UC-04 is retained.

Every staff role may also search (UC-05) and use the assistant (UC-12) within its access rights. Phase 3 draws these shared tasks for the Requester to keep the figure readable. Other permitted participants and approval stages stay in the Phase 3 use-case descriptions. AI supplies advice and drafts; it cannot approve a task.

**Phase 3 references:** SRS sections 2.3 and 7; UC-01 to UC-14; BR-01, BR-02, BR-15.

### 9.1.1 Use cases and responsible roles

<!-- widths: 900,2700,5760 -->
| ID | Existing use case | Who may act |
|---|---|---|
| UC-01 | Manage accounts and roles | Business administrator authorises; System administrator applies |
| UC-02 | Register asset | Asset custodian or Department representative; AI supports |
| UC-03 | Publish asset listing | Custodian prepares; Department representative releases |
| UC-04 | Submit resource request | Requester submits; department decides independently |
| UC-05 | Search and filter assets | All nine staff roles within permitted listings |
| UC-06 | Review ranked matches | Requester; AI ranks eligible results only |
| UC-07 | Reserve asset | Requester; independent releasing custodian or representative confirms |
| UC-08 | Approve workflow step | Assigned approver for the current stage; Business administration for authorised role tasks |
| UC-09 | Confirm handover and receipt | Releasing and receiving custodians |
| UC-10 | Manage maintenance work | Custodian, Maintenance staff and spending approvers |
| UC-11 | Decide end-of-life action | Department/custodian; Sustainability and Finance; optional AI advice |
| UC-12 | Ask the campus assistant | All nine staff roles within their permissions |
| UC-13 | Generate and review report | Business, Finance and Sustainability owners; Procurement view |
| UC-14 | View asset history and audit log | Custodian history; Business administrator audit access |



<!-- pagebreak -->
## 9.2 Sequence Diagrams

We use four sequences for the four assigned scenarios. Their participants are people and parts of one Django application, not new separately deployed services. Django is the framework used to build the web application. PostgreSQL is the database that stores its records. The server runs the application and contacts the outside AI service. Section 11 defines the detailed architecture, meaning how the software parts fit together.

Solid arrows show requests or decisions; dashed open arrows show replies. A lifeline is the dashed vertical line under a participant. Narrow boxes show when a participant handles a message. An alt frame separates alternative paths. An opt frame contains steps used only when its condition applies. Each sequence is enlarged in two consecutive printed parts so its labels remain readable.

A transaction saves related changes together. An atomic transaction saves all of them or none. State, quantity and AuditLog evidence must save successfully together. Otherwise, rollback undoes the attempted changes. Repeating a confirmation returns the saved result without creating a second receipt or hold. The application also checks access, approval independence and the latest record version before changes.

The normal form, search or review becomes available within 15 seconds of the original failed or unanswered AI request, including retries (AI-13.2, NFR-07). NFR-16 separately targets matching results within 5 seconds for 95 of 100 measured requests. Matching confidence follows SRS Table 4.2. Compatibility measures fit to the request; confidence reports the AI's certainty.

Reservation expiry is the deadline for a temporary hold. It still applies after a pending transfer is created (BR-12). If approval misses the deadline, release the units once, cancel the transfer with a reason, withdraw pending tasks and return the request to Open. Approval and expiry use a lock to check and update the same reservation one at a time, preventing conflicting quantity changes (FR-09.4, FR-09.5, FR-11.6, BR-11, BR-12, BR-20).

<!-- pagebreak -->
### 9.2.1 Register with AI classification

![Figure 9.2a Register with AI classification part 1 of 2](images/figure-9-2-register-part-1.png)

<!-- pagebreak -->
![Figure 9.2b Register with AI classification part 2 of 2](images/figure-9-2-register-part-2.png)

The custodian, who is responsible for the item, checks and confirms the values. Suggested values stay separate from confirmed values. Unsupported input means content the AI cannot process. Unsupported inputs, confidence below 0.60 and AI service failure preserve manual entry. A transaction saves related changes as one unit, so a failed save cannot leave half of the asset update applied. The audit record stores who acted, their role, time, reason and values before and after the change (FR-18.1). Model and version identify the AI system used, when that information is available.

**Phase 3 references:** UC-02; UI-03; FR-04; AI-01, AI-12, AI-13; AS-01 to AS-03.

<!-- pagebreak -->
### 9.2.2 Request and department approval

![Figure 9.3a Request and department approval part 1 of 2](images/figure-9-3-request-approval-part-1.png)

A request becomes Open only after an independent department decision: the approver cannot be its requester or creator. Notifications go only to people allowed to see the record. Material changes are changes to important fields, such as quantity, specifications or the required-by date. These return an approved request to RQ-02 for department review. A stale version is an older saved revision; it cannot be used to approve a record that has since changed. Optional assistant drafting follows the same stages.

**Phase 3 references:** UC-04, UC-08; FR-07, FR-10, FR-16, FR-18; BR-02, BR-03.

<!-- pagebreak -->
![Figure 9.3b Request and department approval part 2 of 2](images/figure-9-3-request-approval-part-2.png)

<!-- pagebreak -->
### 9.2.3 Review matches and reserve with fallback

![Figure 9.4a Review matches and reserve with fallback part 1 of 2](images/figure-9-4-match-reserve-part-1.png)

<!-- pagebreak -->
![Figure 9.4b Review matches and reserve with fallback part 2 of 2](images/figure-9-4-match-reserve-part-2.png)

The alt frame shows two alternative paths. A usable AI result follows the first. Disabled AI, service failure, timeout, unusable output, rate limiting or confidence below 0.50 selects classic keyword search and filters. A timeout means the waiting limit has been reached. Rate limiting means the AI service restricts how many requests it accepts. Fallback uses the same eligibility checks and does not need an AI reply. It warns the requester and appears within 15 seconds of the original attempt, including retries. Classic results have no invented AI score. Confidence from 0.50 to below 0.75 needs a Check carefully warning; missing confidence is labelled unavailable. The separate 5-second matching target in NFR-16 remains unchanged. Missing required data removes an item from the results. The requester selects an item, then an independent releasing-side person confirms the hold. A hold sets units aside temporarily. A locked quantity check prevents two requests from holding the same units. If stock has changed or saving fails, no extra units are held.

**Phase 3 references:** UC-05 to UC-07; FR-09; AI-02 to AI-05, AI-13; BR-11 to BR-16.

<!-- pagebreak -->
### 9.2.4 Transfer approvals handover and receipt

![Figure 9.5a Transfer approvals handover and receipt part 1 of 2](images/figure-9-5-transfer-part-1.png)

The opt frame contains extra steps that apply only when their condition is met. Finance and Procurement approvals are conditional; both are needed when both rules apply. An unresolved rule stays pending. Handover records the releasing custodian giving the item to the receiving side. Receipt records the receiving custodian checking and accepting it. Ownership changes only on valid receipt, once. Repeated receipt confirmation returns the saved result without changing ownership or quantity again. If a related save fails, rollback undoes the attempted changes so quantity and ownership stay consistent. Each decision records the person, role, time, saved version, reason and audit evidence. Valid receipt also restores the asset from AS-05 to In service (AS-02) or In storage (AS-03) under the receiving owner, as UC-09 requires. A discrepancy records TR-07 and notifies both department representatives without changing the owner.

**Phase 3 references:** UC-08, UC-09; FR-10, FR-11; BR-02, BR-05, BR-06, BR-13.

<!-- pagebreak -->
![Figure 9.5b Transfer approvals handover and receipt part 2 of 2](images/figure-9-5-transfer-part-2.png)

<!-- pagebreak -->
## 9.3 Activity Diagrams

An activity diagram shows the steps in a process and the choices between them. Each action names the responsible role. Filled circles start the process; a circle with a filled centre ends it. Rounded boxes are actions. Diamonds are decisions. A guard is a written condition, such as [approve], that selects the next path. Connector A joins the two printed parts of each activity.

### 9.3.1 Request to transfer

Each action names the responsible role. Connector A joins the two printed parts of this one activity. A confirmed reservation temporarily holds the item. The required department and policy approvals must finish before the transfer reaches TR-04. Exception paths handle rejection, cancellation or other problems. They release held units once and notify people allowed to see the record. A dispute is an unresolved disagreement about the handover or receipt; ownership stays unchanged until it is resolved. RQ-07 means the requester explicitly closed the request. AI cannot close it automatically. Valid receipt restores AS-02 or AS-03 under the new owner, alongside TR-06 and RQ-06.

**Phase 3 references:** UC-04 to UC-09; FR-07 to FR-11; BR-02, BR-11 to BR-16.

### 9.3.2 Maintenance to end of life

Maintenance means inspecting or repairing an item. Unsafe or Not working items cannot be published or reserved. The same block applies in AS-04 Under maintenance and AS-06 Retired. A higher repair cost needs new approval before completion. End-of-life review decides what happens to an item no longer suitable for its current use. Every final action needs Sustainability review and Finance write-off, which authorises removing its recorded value from the accounts. Required environmental, health and safety (EHS) checks must be complete. Where data erasure is required, evidence must show that stored data was securely removed. Recycling or disposal records why earlier reuse-first options do not work. Retain means keeping the asset. EL-06 rejects the retirement proposal, not the decision to keep the item. Record that reason and restore the previous AS-02 or AS-03 state. This uses the existing SRS rejection path because the SRS has no separate completed-retention state. EL-05 and AS-07 to AS-10 apply only after a final action is completed.

**Phase 3 references:** UC-10, UC-11; FR-12 to FR-14; AI-06; BR-07 to BR-09.

<!-- pagebreak -->
![Figure 9.6a Request to transfer part 1 of 2](images/figure-9-6-request-activity-part-1.png)

<!-- pagebreak -->
![Figure 9.6b Request to transfer part 2 of 2](images/figure-9-6-request-activity-part-2.png)

<!-- pagebreak -->
![Figure 9.7a Maintenance to end of life part 1 of 2](images/figure-9-7-maintenance-activity-part-1.png)

<!-- pagebreak -->
![Figure 9.7b Maintenance to end of life part 2 of 2](images/figure-9-7-maintenance-activity-part-2.png)
