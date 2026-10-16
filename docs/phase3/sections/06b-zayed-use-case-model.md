# 7. Use-Case Model

This section shows how people use the features specified in sections 4 to 6. Each use case lists the requirements it covers.



## 7.1 Actors

The nine roles in section 2.3 can initiate use cases within their assigned permissions. For each main flow, we name one primary actor: the role that starts that scenario. Other authorised starters appear in the alternative flows, and secondary actors help complete the goal. Every role can sign in, view its authorised dashboard and notifications, search permitted published listings, and use the desirable assistant when available, while retaining its own department and record restrictions. The diagram shows the roles that initiate each use case; other participants and approval stages are explained in the descriptions below. One person can perform several roles, but BR-02 still prevents self-approval. The external AI service is a supporting actor; it returns suggestions and never authorises a business action. KU EHS consultation is recorded evidence in the end-of-life workflow, not a tenth application role.

<!-- widths: 2200,3000,4160 -->
| Actor | Type and use cases started | Goal in the system |
|---|---|---|
| Department representative | Primary when starting: UC-02, UC-03, UC-08, UC-10, UC-11 | Confirm records and decide the assigned department stages for listings, requests, transfers and spending. |
| Asset custodian | Primary when starting: UC-02, UC-03, UC-08 (assigned confirmations), UC-09, UC-10, UC-11, UC-14 | Maintain assets and listings, confirm holds, record handover/receipt and support maintenance and retirement records. |
| Requester | Primary when starting: UC-04, UC-05, UC-06, UC-07, UC-12 | Find an eligible resource, obtain request approval and seek a reservation and transfer. |
| Business administrator | Primary when starting: UC-01, UC-08 (role authorisation), UC-13, UC-14 | Authorise role assignments, maintain business settings, route exceptions and review operational reports and audit records. |
| Procurement officer | Primary when starting: UC-08, UC-13 (authorised report view) | Decide procurement-controlled transfer stages and inspect relevant policy and reuse reports. |
| Finance officer | Primary when starting: UC-08, UC-13 | Decide required financial stages and review financial reports and write-offs. |
| Maintenance staff | Primary when starting: UC-10 | Inspect assigned assets and complete approved maintenance with recorded costs and outcomes. |
| Sustainability officer | Primary when starting: UC-08 (assigned review), UC-11, UC-13 | Review reuse-first end-of-life decisions and verify sustainability reporting. |
| System administrator | Primary when starting: UC-01 (account maintenance and authorised role application) | Maintain accounts and apply authorised roles while preserving the business-approval boundary. |
| AI service | Secondary external system; starts none; supports UC-02, UC-06, UC-11, UC-12, UC-13 | Return category suggestions, eligible-match rankings, optional action advice and assistant answers, and draft report text when requested. |

Every staff role can also start UC-05 and UC-12 within its access rights. UC-08 is started only for an assigned stage in Table 5.2. Listing a role here does not grant additional approval rights; the diagram shows the principal entry points, while the alternatives describe other authorised starters.

<!-- pagebreak -->
## 7.2 Use-Case Diagram


![Figure 1. Dawra Campus use-case diagram](images/use-case-diagram.png)

Every role can also search (UC-05) and use the assistant (UC-12); to keep the diagram readable these are shown for the Requester only.

The rectangle is the Dawra Campus system boundary; staff actors and the external AI service are outside it. Solid lines show initiating roles or external-system participation, not unrestricted permission. Approval-stage participation is represented through UC-08 rather than extra connections to each workflow. Other participants remain documented in the use-case descriptions. Check eligibility is always included when ranking or reserving; Send notification is included when an approval decision changes the workflow. Review ranked matches optionally extends an approved resource request. AI classification can fall back to manual entry, and sustainable-action advice is desirable, so neither is modelled as a mandatory AI dependency.

<!-- pagebreak -->
## 7.3 Use-Case Descriptions


<!-- widths: 900,2700,2700,3060 -->
| ID | Use case | Primary actor | Related requirements |
|---|---|---|---|
| UC-01 | Manage accounts and roles | Business administrator | 4.2 (FR-01, FR-02), BR-01, BR-02 |
| UC-02 | Register asset | Asset custodian | 4.4 (FR-04, FR-05), 4.16 (AI-01) |
| UC-03 | Publish asset listing | Asset custodian | 4.5 (FR-06), BR-04 |
| UC-04 | Submit resource request | Requester | 4.6 (FR-07.1 to FR-07.9), BR-03 |
| UC-05 | Search and filter assets | Requester | 4.7 (FR-08) |
| UC-06 | Review ranked matches | Requester | 4.17–4.18 (AI-02 to AI-05) |
| UC-07 | Reserve asset | Requester | 4.8 (FR-09), BR-11, BR-12 |
| UC-08 | Approve workflow step | Department representative | 4.9 (FR-10), BR-01 to BR-10 |
| UC-09 | Confirm handover and receipt | Asset custodian | 4.10 (FR-11), BR-13 |
| UC-10 | Manage maintenance work | Asset custodian | 4.11 (FR-12, FR-13), BR-07 |
| UC-11 | Decide end-of-life action | Department representative | 4.12 (FR-14), 4.19 (AI-06), BR-08, BR-09 |
| UC-12 | Ask the campus assistant | Requester | 4.20 (AI-07, AI-08) |
| UC-13 | Generate and review report | Business administrator | 4.15 (FR-17), 4.21 (AI-09, AI-10), 6.1 |
| UC-14 | View asset history and audit log | Asset custodian | 4.13 (FR-15, FR-18) |

We describe proposed prototype behaviour using the existing requirement IDs and section 4.1 state names, rather than an observed KU workflow. Table 5.2 defines approval owners, and Appendix C retains proposed thresholds and special-handling rules. Each description gives one primary actor, a trigger, a main flow, separate alternative and exception flows, and success and failure outcomes. Branch numbers refer to the main step where they occur. Other authorised starters follow the same permissions and approvals.

<!-- pagebreak -->
### UC-01 Manage accounts and roles

**Description:** A Business administrator requests staff access. Independent authorisation and technical application activate only the approved roles.

**Primary actor:** Business administrator

**Secondary actors:** Another Business administrator (authoriser); System administrator (account maintenance and application).

**Preconditions:** The administrators are signed in; the departments and roles exist.

**Trigger:** The Business administrator requests a role assignment in UI-14.

**Main flow:**
1. The Business administrator selects the staff account, departments and requested roles.
2. The system validates the request and routes it to an independent Business administrator.
3. The independent Business administrator checks the request and authorises the roles through UC-08.
4. The system records the authorisation and presents the assignment to the System administrator.
5. The System administrator applies the authorised roles to the account.
6. The system activates the assignment, records both users and limits the account's functions to its approved scope.

**Alternative flows:**
1a. The administrator maintains departments, categories or control flags instead. Configurable changes, where enabled, record an effective date without changing approvals in progress.
5a. The System administrator creates or updates the account first. Deactivation ends sessions and lists pending tasks for reassignment.
6a. The staff member signs in through UI-01; the system checks account status and shows permitted functions in UI-02.

**Exception flows:**
2a. Conflicting details or deletion of a referenced department/category are refused; referenced entries can be deactivated.
3a. The authoriser created the request or rejects it: the system blocks self-approval or records the rejection reason; no role becomes active.
5b. The assignment lacks authorisation: the system refuses it and logs the attempt.
6b. An inactive account cannot sign in. Five consecutive failed sign-ins block that account for 15 minutes under FR-02.4.

**Postconditions:**

Success: authorised accounts, roles or settings are saved with an audit trail.

Failure: invalid or rejected changes grant no extra access.

**Rules:** BR-01 technical administration grants no business approval; BR-02 no self-approval.

**Related requirements:** FR-01.1 to FR-01.4, FR-02.1 to FR-02.4, FR-03.1 to FR-03.5.


### UC-02 Register asset

**Description:** A custodian registers an asset. Independent confirmation makes the checked record available for authorised use.

**Primary actor:** Asset custodian

**Secondary actors:** Another Asset custodian or Department representative (confirmer); AI service (optional classification).

**Preconditions:** The custodian is signed in for the owning department; its categories exist.

**Trigger:** The custodian selects asset registration in UI-03.

**Main flow:**
1. The custodian enters the details, quantities, ownership, condition, specifications and evidence in FR-04.1.
2. The system assigns an ID, validates fields and uploads, checks duplicates and keeps Draft (AS-01).
3. The custodian accepts, corrects or rejects optional AI suggestions and submits the completed record.
4. The system records the reviewed values and routes confirmation to an eligible user other than the creator.
5. The independent custodian or Department representative checks the evidence and confirms the record through UC-08.
6. The system saves In service (AS-02) or In storage (AS-03), with the confirmer, verification date, consistent quantities and history.

**Alternative flows:**
1a. A Department representative starts registration; confirmation still requires a separate eligible user.
2a. A duplicate warning prompts comparison and explicit confirmation of a distinct asset.
3a. AI is unusable: the form is preserved for manual entry; responses to suggestions are recorded.

**Exception flows:**
2b. Invalid fields and uploads retain Draft with correction messages.
5a. Ineligible or rejected confirmation leaves Draft, with the reason or eligible rerouting.
6a. Saving fails: the system reports failure without presenting the asset as confirmed or available.

**Postconditions:**

Success: the confirmed asset has an ID, verification, consistent quantities and history.

Failure: the record is unconfirmed or unsaved; it cannot be published or reserved.

**Rules:** BR-02 no self-approval; BR-11 no duplicate allocation; BR-15 AI suggests and humans confirm.

**Related requirements:** FR-04.1 to FR-04.6, FR-05.1 to FR-05.4, AI-01, AI-12, AI-13.


### UC-03 Publish asset listing

**Description:** A custodian offers surplus assets. Department release approval makes the listing visible for reuse.

**Primary actor:** Asset custodian

**Secondary actors:** Owning Department representative (release approver).

**Preconditions:** The custodian is signed in; the confirmed asset is In service (AS-02) or In storage (AS-03), with eligible quantity.

**Trigger:** The custodian chooses listing publication in UI-04.

**Main flow:**
1. The custodian prepares a Draft listing (LS-01) with quantity, condition, location, availability date, restrictions and release reason.
2. The system checks the asset state and quantity and shows the listing for review.
3. The custodian confirms submission for release approval.
4. The system sets Pending release approval (LS-02) and notifies the owning Department representative.
5. An independent Department representative reviews the listing and approves release through UC-08.
6. The system sets Published (LS-03), displays permitted details in UI-05 and notifies the custodian.

**Alternative flows:**
1a. A representative prepares the listing; another eligible representative decides its release.
5a. Requested changes return the listing to Draft with a reason for editing and resubmission.
6a. Stale verification shows Verification needed; confirmation waits for re-verification under TBD-4.
6b. Permitted withdrawal sets Withdrawn (LS-05), cancels pending reservations and notifies requesters.

**Exception flows:**
2a. Invalid quantity or an asset Under maintenance, In transfer or Retired blocks submission.
5b. Rejected release returns Draft with a reason; other departments cannot see it.
6c. An approved transfer is in progress: the system refuses withdrawal under BR-19.

**Postconditions:**

Success: an approved listing is visible with its quantity, restrictions and verification status.

Failure: unapproved listings remain hidden; blocked withdrawal leaves the transfer intact.

**Rules:** BR-02 no self-approval; BR-04 release before publication; BR-16 verification; BR-19 approved-transfer protection; BR-20 reasons and release.

**Related requirements:** FR-06.1 to FR-06.6, FR-05.4, FR-10.1 to FR-10.4.


### UC-04 Submit resource request

**Description:** A Requester describes a department need. Approval opens the request for matching and reservation.

**Primary actor:** Requester

**Secondary actors:** Receiving Department representative (request approver).

**Preconditions:** The Requester is signed in for an authorised department and the needed category exists.

**Trigger:** The Requester selects New request in UI-02, opening UI-06, or reviews an assistant draft there.

**Main flow:**
1. The Requester enters purpose, category, specifications, quantity, minimum condition, urgency, delivery location, required-by date and optional description.
2. The system checks the information and shows a Draft request (RQ-01).
3. The Requester confirms submission.
4. The system assigns the FR-07.9 unique ID, sets Pending department approval (RQ-02) and sends an identified approval task.
5. An independent receiving Department representative approves the need through UC-08.
6. The system sets Open (RQ-03), notifies the Requester with the same ID and offers search, matches and reservation.

**Alternative flows:**
5a. Changes are requested: the request returns to Draft with the reason; the Requester edits and resubmits it.
6a. Approved quantity, specifications or date change: the request returns to Pending department approval.
6b. No eligible item: close as No suitable item (RQ-07); external purchasing remains outside the system and no avoided purchase counts.
6c. Permitted cancellation sets Cancelled (RQ-09), records the reason and releases holds.

**Exception flows:**
2a. A past date or quantity that is not a positive whole number: preserve the form, explain the error and submit nothing.
5b. Approval is rejected: the request becomes Rejected (RQ-08), with the reason and notification.
6d. The date passes before fulfilment: set Expired (RQ-10), release holds and notify the Requester.

**Postconditions:**

Success: the request is Open with a stable unique ID and a recorded department approval.

Failure: nothing is submitted, or the request is Rejected or Expired; no reservation or transfer approval is granted.

**Rules:** BR-02 no self-approval; BR-03 approval before Open; BR-15 no implied approval; BR-18 verified avoided purchases; BR-20 reasons and release.

**Related requirements:** FR-07.1 to FR-07.9, FR-10.1 to FR-10.4.


### UC-05 Search and filter assets

**Description:** A Requester searches authorised listings and inspects suitable assets. The results help select a candidate without creating a reservation.

**Primary actor:** Requester

**Secondary actors:** None required for the search itself; every other staff role can start the same search within its permissions.

**Preconditions:** The Requester is signed in and the system knows the records their roles and departments permit them to view.

**Trigger:** The Requester opens UI-05 and runs a keyword search or applies filters.

**Main flow:**
1. The Requester enters keywords and filters such as category, condition, department, location and quantity.
2. The system combines the criteria, checks access and returns matching listings, result count and sort options.
3. The Requester chooses a sort order or refines the criteria.
4. The system refreshes the authorised results using the selected criteria.
5. The Requester opens a listing to inspect its details.
6. The system shows specifications, condition, quantity, restrictions and verification date; reservation remains a separate action under UC-07.

**Alternative flows:**
2a. No item matches: the system explains the empty result and offers a new request with the same criteria.
3a. AI is unavailable: keyword search, filters and sorting continue normally.
6a. A suitable result is found for an Open request: the Requester starts UC-07, which rechecks mandatory constraints.

**Exception flows:**
2b. A record is outside the user's scope or unpublished in another department: the system excludes it and refuses direct access.
6b. Verification is stale: the system shows Verification needed and blocks reservation confirmation until re-verification.
6c. Availability changed after searching: the system displays the current quantity rather than accepting the old result as a hold.

**Postconditions:**

Success: the Requester has reviewed authorised results or a clear no-match outcome.

Failure: restricted or outdated data cannot be used to confirm a hold; no reservation, approval or ownership change occurs.

**Rules:** BR-14 mandatory eligibility before action; BR-16 re-verification before confirming a stale listing.

**Related requirements:** FR-08.1 to FR-08.6, FR-02.2, FR-06.3, FR-06.4, AI-13.


### UC-06 Review ranked matches

**Description:** A Requester compares AI-ranked resources for an approved need. Only eligible items can be selected for a separate reservation request.

**Primary actor:** Requester

**Secondary actors:** AI service (ranking and explanations).

**Preconditions:** The Requester is signed in, has an Open request (RQ-03) and may view its candidate listings.

**Trigger:** The Requester asks for ranked matches in UI-07 after department approval.

**Main flow:**
1. The Requester opens the approved request and asks to review matching resources.
2. The system includes Check eligibility, applying access, availability, quantity, condition, compatibility and date rules before AI ranking.
3. The Requester confirms the approved criteria for comparison.
4. The system obtains the AI ranking and displays scores, explanations, missing information and separate confidence information, recording model details and response time.
5. The Requester checks the evidence and selects an eligible candidate, recording a reason if overriding the ranking.
6. The system records the recommendation and response and offers UC-07 with a fresh eligibility check when a hold is requested.

**Alternative flows:**
2a. No eligible candidate remains: the system explains the result and offers classic search or the No suitable item option in UC-04.
5a. The Requester rejects all suggestions and uses classic search, or revises the request through its normal approval path; nothing is held.

**Exception flows:**
2b. Mandatory evidence is missing: the system identifies it and withholds the affected item as actionable.
4a. AI fails, times out, returns invalid output or has insufficient confidence: the system preserves the request and offers classic search under AI-13.
4b. Supported model or confidence details are unavailable: the system marks them unavailable rather than inventing values.

**Postconditions:**

Success: eligible recommendations and the user's response are recorded, or the Requester continues with classic search.

Failure: no usable AI ranking is accepted; no quantity is reserved and no approval is bypassed.

**Rules:** BR-14 eligibility before ranking; BR-15 recommendations do not reserve or approve assets. This optionally extends UC-04 after request approval.

**Related requirements:** AI-02 to AI-05, AI-11 to AI-13, FR-08.6, FR-09.1.


### UC-07 Reserve asset

**Description:** A Requester seeks a temporary hold. Independent confirmation reserves quantity without approving transfer.

**Primary actor:** Requester

**Secondary actors:** Releasing Asset custodian or Department representative (hold confirmer).

**Preconditions:** The Requester is signed in, has an Open request (RQ-03) and has selected a Published listing (LS-03).

**Trigger:** The Requester selects the reservation action for the chosen listing and quantity.

**Main flow:**
1. The Requester selects the quantity and submits a reservation request.
2. The system includes Check eligibility, checks current quantity, creates Requested (RV-01) and sets the request to Reservation requested (RQ-04).
3. The releasing custodian checks stock, condition and verification evidence.
4. The system checks the confirmer's permissions, independence and current verification.
5. The eligible releasing custodian or representative confirms the hold.
6. The system atomically holds units, reduces availability, sets Confirmed (RV-02) and, if needed, Fully reserved (LS-04), then notifies both sides of TBD-3 expiry and outstanding transfer approval.

**Alternative flows:**
3a. Verification is stale: the custodian re-verifies condition and availability before confirmation.
6a. Proceeding to transfer creates TR-01, links Converted to transfer (RV-04) and sets In transfer (RQ-05); UC-08 supplies approvals.
6b. A permitted cancellation sets Cancelled (RV-06), records a reason and releases the hold.

**Exception flows:**
2a. Invalid or unavailable quantity or failed eligibility blocks the request with an explanation.
5a. Declining sets Declined (RV-03) with a reason; the request returns to Open.
6c. Another user already held the last units: confirmation fails without duplicate allocation.
6d. The hold expires without approved transfer: it becomes Expired (RV-05); quantity is released and both sides are notified.

**Postconditions:**

Success: the quantity is held for the configured period, or passed into the separate transfer workflow.

Failure: a declined, expired, cancelled or conflicting hold leaves no duplicate allocation or transfer approval.

**Rules:** BR-02 independent confirmation; BR-11 no double allocation; BR-12 hold expiry; BR-14 eligibility; BR-15 hold is not approval; BR-16 current verification; BR-20 reasons and release.

**Related requirements:** FR-09.1 to FR-09.7, FR-11.1, FR-06.4, FR-05.3.


### UC-08 Approve workflow step

**Description:** An assigned approver decides one stage. The recorded decision controls the parent record's permitted transition.

**Primary actor:** Department representative

**Secondary actors:** Finance officer, Procurement officer, Sustainability officer, Asset custodian (other stages); Business administrator (role authorisation/reassignment).

**Preconditions:** A Pending task (AT-01) exists for the signed-in representative, who is not its creator/requester.

**Trigger:** The representative opens an assigned approval task in UI-08.

**Main flow:**
1. The representative selects a pending task.
2. The system checks eligibility and prior approvals and shows the current version, evidence, quantities, costs and AI suggestions.
3. The representative reviews the evidence and chooses Approve.
4. The system validates the decision and records Approved (AT-02) with user, role, time and record version.
5. The representative reviews the recorded decision and next-stage status.
6. The system advances the parent under section 4.1 and Table 5.2, includes Send notification and creates the next task.

**Alternative flows:**
1a. Another Table 5.2 role starts its assigned stage with the same checks.
3a. Changes requested (AT-04) requires a reason; the parent returns for revision and a new task on resubmission.
6a. Where enabled, TBD-5 reminders flag overdue tasks without approving them; eligible alternates can receive reassigned tasks.

**Exception flows:**
2a. The user is ineligible, is the creator/requester or an earlier stage is incomplete: the system blocks the decision.
3b. Rejection requires a reason, sets Rejected (AT-03) and applies the parent's rejection and quantity-release rules.
4a. Stale decisions are refused; material changes require a new task under FR-10.7.

**Postconditions:**

Success: one authorised decision is saved and the parent advances only when all required stages are complete.

Failure: a refused or stale decision grants no approval; a recorded rejection follows the parent's rejection path.

**Rules:** BR-01 business authority is separate from IT access; BR-02 no self-approval; BR-03 to BR-10 define stage owners and order; BR-20 reasons and held-quantity release.

**Related requirements:** FR-10.1 to FR-10.8, FR-16.1 to FR-16.5.


### UC-09 Confirm handover and receipt

**Description:** The releasing custodian hands over the asset; receiving confirmation completes transfer and changes ownership.

**Primary actor:** Asset custodian (releasing department)

**Secondary actors:** Asset custodian (receiving department); Department representatives (dispute resolution).

**Preconditions:** The custodians are signed in; the transfer is Approved (TR-04), including BR-05/BR-06 stages, with quantity allocated.

**Trigger:** The releasing custodian opens the approved transfer in UI-09 to record handover.

**Main flow:**
1. The releasing custodian confirms arrangements and records the actual quantity, condition and handover evidence.
2. The system records Handed over (TR-05), sets the asset to In transfer (AS-05) and keeps ownership with the releasing department.
3. The receiving custodian compares the delivery with the agreed quantity and condition and confirms receipt.
4. The system sets Completed (TR-06), updates ownership, custody and location, restores In service or In storage and sets Fulfilled (RQ-06).
5. The releasing custodian reviews the completed transfer record.
6. The system retains both confirmations, notifies the parties and provides a printable/exportable reconciliation record.

**Alternative flows:**
1a. The parties reschedule before handover; the arrangement history is retained.
1b. A permitted pre-handover cancellation records Cancelled (TR-09), its reason and release of the held quantity.

**Exception flows:**
2a. A required approval is missing: handover is blocked and the outstanding stage is identified.
3a. A delivery difference sets Disputed (TR-07); ownership stays unchanged and representatives are notified. Resolution leads to receipt and completion or return and cancellation.
4a. Duplicate receipt or save failure applies no duplicate changes; the stored status is reported.

**Postconditions:**

Success: valid receipt completes the transfer, updates the responsible department and fulfils the request exactly once.

Failure: missing approval or an unresolved dispute prevents ownership change; cancellation releases quantity.

**Rules:** BR-05 both department approvals; BR-06 conditional policy approvals; BR-11 quantity consistency; BR-13 ownership only on receipt; BR-20 cancellation reasons and release.

**Related requirements:** FR-11.1 to FR-11.7, FR-05.3, FR-05.4.


### UC-10 Manage maintenance work

**Description:** A custodian reports a defect. Approved maintenance records the repair, actual cost and resulting condition.

**Primary actor:** Asset custodian

**Secondary actors:** Maintenance staff; owning Department representative; Finance officer when the spending threshold applies.

**Preconditions:** The custodian is signed in for an existing asset; Appendix C spending thresholds apply.

**Trigger:** The custodian reports a defect in UI-10.

**Main flow:**
1. The custodian enters the defect, inspection evidence and requested follow-up.
2. The system opens Reported (MW-01) and notifies Maintenance staff.
3. Maintenance staff assess the asset in Under assessment (MW-02), recording findings, condition, planned work and estimated cost.
4. The system sets Awaiting cost approval (MW-03), routes required department and required Finance decisions through UC-08, then sets Approved (MW-04) and Under maintenance (AS-04).
5. Maintenance staff record In progress (MW-05), perform approved work and enter parts, labour, cost, outcome and condition.
6. The system checks spending approval, records Completed (MW-06), restores In service or In storage and saves the maintenance history.

**Alternative flows:**
1a. A representative reports the defect, or Maintenance staff open an assigned assessment; the same stages apply.
3a. Unsafe or Not working findings block publication and reservation while maintenance continues.
5a. Actual cost exceeds approval: the work order returns to MW-03 for the difference before completion.
5b. Permitted pre-work withdrawal sets Cancelled (MW-09) with a reason from an allowed state.

**Exception flows:**
4a. Spending is rejected: the system records Rejected (MW-08), with the reason; no unapproved work is authorised.
3b. Not repairable at assessment or repair (step 5) sets MW-07, Retired (AS-06) and Proposed (EL-01).
6a. Missing cost approval or save failure prevents completion; stored states remain authoritative.

**Postconditions:**

Success: completed maintenance has approved costs, an updated condition and a traceable asset history.

Failure: unfinished or rejected work is not Completed; unrepairable items enter end-of-life review.

**Rules:** BR-02 independent spending approval; BR-07 department approval and conditional Finance approval; BR-20 reasons and quantity release where applicable.

**Related requirements:** FR-12.1, FR-12.2, FR-13.1 to FR-13.7.


### UC-11 Decide end-of-life action

**Description:** A department proposes an asset's final action. Sustainability review and Finance approval precede completion.

**Primary actor:** Department representative

**Secondary actors:** Sustainability officer; Finance officer; Asset custodian; AI service (optional advice).

**Preconditions:** The representative is signed in; the workflow is enabled and the previous asset state is retained.

**Trigger:** The representative opens an action proposal in UI-11, including one from UC-10.

**Main flow:**
1. The representative enters the proposed action, quantity, destination, reason and evidence.
2. The system records Proposed (EL-01) and Retired (AS-06), showing reuse-first options and requested AI advice.
3. The representative justifies bypassed options and supplies required EHS consultation and data-erasure evidence.
4. The system routes Under sustainability review (EL-02), then Awaiting finance approval (EL-03), through UC-08; both approvals enable Approved (EL-04).
5. After the approved action is carried out, the custodian records its date, responsible person, quantity, destination and evidence.
6. The system records Completed (EL-05), sets the appropriate final asset state (AS-07 to AS-10) and removes that quantity from availability.

**Alternative flows:**
1a. A custodian prepares the proposal or Sustainability starts an existing review; the same approvals apply.
3a. Unusable AI advice is replaced by classic evidence-based review.
4a. Changes are requested: the proposal returns to EL-01 for correction and resubmission.
6a. Disassembly parts are registered through UC-02, linked to the original asset.

**Exception flows:**
3b. Required evidence is missing: approval remains blocked until it is supplied.
4b. Either reviewer rejects: record Rejected (EL-06) and the reason, restore the previous asset state and authorise no action.
5a. Missing completion evidence or an unfinished action leaves Approved; no final asset state is recorded.

**Postconditions:**

Success: the completed final action has independent decisions, required evidence and the correct asset state.

Failure: incomplete proposals authorise no action; rejection restores the previous state.

**Rules:** BR-02 no self-approval; BR-08 reuse-first review and Finance write-off; BR-09 special-handling evidence; BR-15 AI advice is not permission.

**Related requirements:** FR-14.1 to FR-14.7, AI-06, AI-11 to AI-13.


### UC-12 Ask the campus assistant

**Description:** A Requester asks for guidance or permitted records. The assistant answers without bypassing access or approvals.

**Primary actor:** Requester

**Secondary actors:** AI service. Other staff roles may start the same interaction within their own permissions.

**Preconditions:** The Requester is signed in; the desirable assistant is enabled and available.

**Trigger:** The Requester opens UI-12 and sends a question.

**Main flow:**
1. The Requester enters a question about resources, permitted history, request status or guidance.
2. The system limits context to records and approved guidance the Requester can access and identifies needed clarification.
3. The Requester supplies any requested clarification.
4. The system shows an AI-labelled answer, supporting records, uncertainty and missing information.
5. The Requester accepts, corrects or rejects the answer, with reasons for corrections or rejections.
6. The system records the interaction, available model details and response; the answer alone changes no business record.

**Alternative flows:**
5a. A follow-up question returns to step 1 with the same access checks.
4a. Proposed changes show exact fields for confirmation, correction or cancellation before the normal workflow. UC-04 still requires department approval.

**Exception flows:**
2a. Restricted questions are refused without disclosing protected records.
4b. AI failure, timeout or unsupported answers preserve input and offer classic search, forms or help under AI-13.
5b. Requests to approve, transfer or dispose receive guidance only; assigned humans must use UC-08 or UC-11.

**Postconditions:**

Success: the user receives a reviewable answer or classic alternative; any confirmed proposal follows the normal workflow.

Failure: no unsupported answer, unauthorised change or approval is treated as valid; input is preserved for another route.

**Rules:** BR-01 no extra authority; BR-03 request approval before Open; BR-15 user confirmation and normal approvals still apply.

**Related requirements:** AI-07, AI-08, AI-11 to AI-13, FR-02.2, FR-07.1 to FR-07.3.


### UC-13 Generate and review report

**Description:** A Business administrator generates a report. Conventional figures and AI summaries need data-owner review before official use.

**Primary actor:** Business administrator

**Secondary actors:** Finance officer; Sustainability officer; Procurement officer (viewing/comments); AI service.

**Preconditions:** The administrator is signed in for the selected scope; source availability and limitations can be established.

**Trigger:** The administrator opens UI-13 and selects a report type, period and departments.

**Main flow:**
1. The administrator chooses the report and authorised filters.
2. The system produces a conventional Draft report with counts, totals, units, sources and limitations.
3. The administrator requests a narrative summary from those figures.
4. The system produces an AI-labelled draft using the same snapshot and totals, with sources and available model details.
5. The data owners check and correct their domains: Business administration for operations, Finance for money and Sustainability for sustainability.
6. The system marks Reviewed by with names and dates only after every required owner has checked their figures.

**Alternative flows:**
1a. Finance or Sustainability starts its domain report; Procurement may view authorised reports but cannot replace the data owner.
2a. Missing indicator inputs or factors produce N/A or labelled estimates, never invented savings or carbon results.
3a. Without a narrative or available AI, the conventional report follows the same owner review.
6a. Where enabled, export provides an authorised CSV or printable report with filters and review status.

**Exception flows:**
2b. Access checks or report generation fail: the system reports the failure and produces no official report.
5a. Unsupported claims, mismatched totals or missing owner review keep the report Draft.

**Postconditions:**

Success: the report shows its review status and uses traceable records and formulas.

Failure: missing evidence, mismatched AI text or incomplete review cannot produce an official report.

**Rules:** BR-10 data-owner review; BR-15 AI text grants no authority; BR-18 only fulfilled, verified reuse counts as avoided purchase.

**Related requirements:** FR-17.1 to FR-17.5, AI-09 to AI-13, SU-01 to SU-09.


### UC-14 View asset history and audit log

**Description:** A custodian inspects the permitted history of an asset. Business administrators can inspect the audit view within their scope; original entries remain unchanged.

**Primary actor:** Asset custodian

**Secondary actors:** Business administrator (audit view and, where enabled, search and export). Other staff may inspect underlying records only within their permissions.

**Preconditions:** The custodian is signed in and may view the selected asset; audit access requires the Business administrator role.

**Trigger:** The custodian opens the asset history in UI-04.

**Main flow:**
1. The custodian selects an authorised asset's history.
2. The system shows chronological events with dates, actors, actions, state changes, approvals, costs and evidence.
3. The custodian selects an event, using event-type or period filters where enabled.
4. The system displays the matching entries without changing them.
5. The custodian follows a link to a supporting record.
6. The system checks access again, displays permitted details and retains the original history and audit entries for TBD-7.

**Alternative flows:**
1a. A Business administrator starts the audit view instead; entries also show reasons and before/after values.
3a. Where desirable audit search is enabled, the administrator filters by user, record, action or period.
4a. No event matches: the system explains the empty result and keeps the filters available.
5a. Where desirable audit export is enabled, the administrator requests an authorised CSV instead; export leaves the stored entries unchanged.

**Exception flows:**
6a. A linked record is outside the user's access: the system refuses disclosure even if the link was obtained elsewhere.
6b. A user attempts to edit or delete an audit entry: the system refuses; a correction requires a new traceable entry referring to the original.

**Postconditions:**

Success: permitted history or audit evidence is reviewed or exported without altering its source.

Failure: restricted details remain undisclosed and refused edits leave original audit entries intact.

**Rules:** BR-17 audit entries cannot be edited or deleted; corrections refer to the original entry.

**Related requirements:** FR-15.1, FR-15.2, FR-18.1 to FR-18.4, FR-02.2.
