# 4. System Features

Section 4.1 shows the use-case model, section 4.2 defines the states that records move through, and sections 4.3 to 4.23 specify the requirements feature by feature.

## 4.1 Use-Case Model



### 4.1.1 Actors

The nine roles in section 2.3 are primary actors. Staff user is their common, general actor: every role can sign in, view its authorised dashboard and notifications, search permitted published listings, and use the desirable assistant when available. The specialist roles inherit those common interactions while retaining their own department and record restrictions. One person can perform several roles, but BR-02 still prevents self-approval. The external AI service is a supporting actor; it returns suggestions and never authorises a business action. KU EHS consultation is recorded evidence in the end-of-life workflow, not a tenth application role.

<!-- widths: 2200,1500,5660 -->
| Actor | Type | Goal in the system |
|---|---|---|
| Staff user | General actor | Access common staff functions using an active account and authorised department assignment. |
| Department representative | Primary; specialises Staff user | Confirm records and decide the assigned department stages for listings, requests, transfers and spending. |
| Asset custodian | Primary; specialises Staff user | Maintain assets and listings, confirm holds, record handover/receipt and support maintenance and retirement records. |
| Requester | Primary; specialises Staff user | Find an eligible resource, obtain request approval and seek a reservation and transfer. |
| Business administrator | Primary; specialises Staff user | Authorise role assignments, maintain business settings, route exceptions and review operational reports and audit records. |
| Procurement officer | Primary; specialises Staff user | Decide procurement-controlled transfer stages and inspect relevant policy and reuse reports. |
| Finance officer | Primary; specialises Staff user | Decide required financial stages and review financial reports and write-offs. |
| Maintenance staff | Primary; specialises Staff user | Inspect assigned assets and complete approved maintenance with recorded costs and outcomes. |
| Sustainability officer | Primary; specialises Staff user | Review reuse-first end-of-life decisions and verify sustainability reporting. |
| System administrator | Primary; specialises Staff user | Maintain accounts and apply authorised roles while preserving the business-approval boundary. |
| AI service | Secondary; external system | Return category suggestions, eligible-match rankings, optional action advice and assistant answers, and draft report text when requested. |

<!-- pagebreak -->
### 4.1.2 Use-Case Diagram


![Figure 1. Dawra Campus use-case diagram](images/use-case-diagram.png)

The rectangle is the Dawra Campus system boundary; staff actors and the external AI service are outside it. Solid association lines show participation, not unrestricted permission. Staff user represents the common interactions inherited by all nine roles; the role-specific associations are summarised in the table below. The two supporting use cases are Check eligibility and Send notification. Check eligibility is always included when ranking or reserving; Send notification is included when an approval decision changes the workflow. Review ranked matches optionally extends an approved resource request. AI classification can fall back to manual entry, and sustainable-action advice is desirable, so neither is modelled as a mandatory AI dependency.

<!-- pagebreak -->
### 4.1.3 Use-Case Descriptions


<!-- widths: 900,2700,2700,3060 -->
| ID | Use case | Main actors | Related requirements |
|---|---|---|---|
| UC-01 | Manage accounts and roles | Business administrator, System administrator | 4.3 (FR-01, FR-02), BR-01, BR-02 |
| UC-02 | Register asset | Asset custodian, Department representative, AI service | 4.5 (FR-04, FR-05), 4.17 (AI-01) |
| UC-03 | Publish asset listing | Department representative, Asset custodian | 4.6 (FR-06), BR-04 |
| UC-04 | Submit resource request | Requester, Department representative | 4.7 (FR-07), BR-03 |
| UC-05 | Search and filter assets | Requester, all staff users | 4.8 (FR-08) |
| UC-06 | Review ranked matches | Requester, AI service | 4.18–4.19 (AI-02 to AI-05) |
| UC-07 | Reserve asset | Requester, Asset custodian | 4.9 (FR-09), BR-11, BR-12 |
| UC-08 | Approve workflow step | Department representative, Finance officer, Procurement officer, Sustainability officer; Business administrator and Asset custodian for their assigned stages | 4.10 (FR-10), BR-01 to BR-10 |
| UC-09 | Confirm handover and receipt | Asset custodian, Department representative | 4.11 (FR-11), BR-13 |
| UC-10 | Manage maintenance work | Asset custodian, Maintenance staff, Department representative; Finance officer when required | 4.12 (FR-12, FR-13), BR-07 |
| UC-11 | Decide end-of-life action | Sustainability officer, Finance officer, Department representative, Asset custodian, AI service | 4.13 (FR-14), 4.20 (AI-06), BR-08, BR-09 |
| UC-12 | Ask the campus assistant | All staff users, AI service | 4.21 (AI-07, AI-08) |
| UC-13 | Generate and review report | Business administrator, Finance officer, Procurement officer, Sustainability officer, AI service | 4.16 (FR-17), 4.22 (AI-09, AI-10), 6.1 |
| UC-14 | View asset history and audit log | Asset custodian, Business administrator | 4.14 (FR-15, FR-18) |

The descriptions below define proposed prototype behaviour using the existing requirement IDs and states. They do not report an implemented or observed KU workflow. Approval owners are defined in Table 5.2; thresholds and special-handling rules retain their Appendix C status. Each alternative is numbered after the main step from which it branches.

<!-- pagebreak -->
#### UC-01 Manage accounts and roles

**Actors:** System administrator, Business administrator; affected Staff user.

**Related requirements:** FR-01.1 to FR-01.4, FR-02.1 to FR-02.4, FR-03.1 to FR-03.5; BR-01, BR-02.

**Precondition:** The administrators are signed in with the relevant assignments. Any department and role being assigned exist in the configuration.

**Main success scenario:**
1. The System administrator opens UI-14 and creates or updates an account with its name, staff email, department and account status.
2. A Business administrator requests the required role assignments for named departments.
3. The system checks the assignment and presents it to an eligible Business administrator for authorisation. The creator cannot decide their own approval task (BR-02).
4. The authorised Business administrator confirms the assignment. The system records the decision and makes it available for application.
5. The System administrator applies the authorised roles. The system records who authorised and applied them without adding unrelated business permissions.
6. The staff user signs in through UI-01. The system checks the active account and shows UI-02 with only permitted functions.

**Alternative and exception flows:**
1a. An account field is invalid or already identifies another account: the system explains the issue and saves no conflicting account.
1b. The Business administrator chooses business settings in UI-14: they maintain departments, categories and control flags under FR-03. Where configurable settings are available, changes record an effective date without changing approvals in progress. Referenced departments or categories can be deactivated instead of deleted.
3a. The authoriser is the creator or lacks the required role: the system blocks the decision and routes it to an eligible alternate under BR-02 and TBD-9.
4a. The assignment is rejected: the system closes the assignment request with a reason and does not activate the role.
5a. The System administrator attempts an unauthorised assignment: the system refuses and logs the attempt.
6a. The account is deactivated: the system refuses sign-in, ends active sessions and lists open approval tasks for reassignment. Five consecutive failed sign-in attempts trigger the lock in FR-02.4.

**Postcondition:** The account and approved roles are recorded and active where authorised, with an audit trail. Failed or rejected assignments grant no additional access. Business settings under FR-03 remain restricted to the Business administrator.

<!-- pagebreak -->
#### UC-02 Register asset

**Actors:** Asset custodian, Department representative; AI service supports classification when available.

**Related requirements:** FR-04.1 to FR-04.6, FR-05.1 to FR-05.4; AI-01, AI-12, AI-13; BR-02, BR-11, BR-15.

**Precondition:** The user is signed in and may maintain assets for the owning department. The department and relevant categories exist.

**Main success scenario:**
1. The Asset custodian or Department representative opens UI-03 and enters the fields in FR-04.1, including quantity, unit, ownership, custody, condition, specifications and available evidence.
2. The system assigns an asset ID, checks required fields and upload limits, warns about possible duplicates and keeps the unconfirmed record in Draft (AS-01).
3. When AI is available, the system requests classification and description suggestions and labels the response as AI suggestion, with provenance and confidence information where available.
4. The user accepts, edits or rejects the suggestions and checks the entered information.
5. An eligible Asset custodian or Department representative who did not create or request the record confirms it under Table 5.2 and BR-02.
6. The system saves the confirmed asset as In service (AS-02) or In storage (AS-03), records the confirming user and verification date, and keeps the available, reserved and allocated quantities consistent.

**Alternative and exception flows:**
2a. Required information or an upload is invalid: the system retains Draft and identifies the fields or files to correct.
2b. A possible duplicate exists: the user reviews the existing record and explicitly confirms a distinct asset before saving.
3a. AI is unavailable or produces an unusable suggestion: the system preserves the form and allows manual category and description entry; no AI result is invented.
5a. Confirmation is rejected or the user cannot decide the task: the record remains Draft and is sent to an eligible confirmer where required.

**Postcondition:** A valid confirmed asset is available to its authorised department users, with quantities, confirmation and history recorded. A draft asset cannot be published or reserved.

<!-- pagebreak -->
#### UC-03 Publish asset listing

**Actors:** Asset custodian, Department representative of the owning department.

**Related requirements:** FR-06.1 to FR-06.6, FR-05.4, FR-10.1 to FR-10.4; BR-02, BR-04, BR-16, BR-19, BR-20.

**Precondition:** The asset is confirmed, is In service or In storage, and has an eligible quantity the owning department can offer.

**Main success scenario:**
1. The Asset custodian or Department representative prepares a Draft listing (LS-01) with offered quantity, condition, location, available-from date, restrictions and reason for release.
2. The system validates the quantity and asset state and records the listing when the user submits it.
3. The system sets Pending release approval (LS-02) and notifies an eligible owning-department representative through UI-08.
4. The representative reviews the listing and independently approves release under BR-04 and BR-02.
5. The system sets Published (LS-03), shows the listing to authorised staff through UI-05 and notifies the custodian.

**Alternative and exception flows:**
2a. The quantity is invalid or the asset is Under maintenance, In transfer or Retired: the system blocks submission and explains the restriction.
4a. Changes are requested or release is rejected: the listing returns to Draft with the decision reason and remains hidden from other departments.
5a. Verification is older than TBD-4: the published listing shows Verification needed, and reservation confirmation is blocked until the custodian verifies it again.
5b. The owning department withdraws the listing: it becomes Withdrawn (LS-05), pending reservations are cancelled and requesters are notified. BR-19 blocks withdrawal during an approved transfer.

**Postcondition:** Only an approved listing is visible for reuse. Its quantity, restrictions and verification status are shown, while release evidence and decisions remain traceable.

<!-- pagebreak -->
#### UC-04 Submit resource request

**Actors:** Requester (initiator), receiving Department representative.

**Related requirements:** FR-07.1 to FR-07.8, FR-10.1 to FR-10.4; BR-02, BR-03, BR-18, BR-20.

**Precondition:** The Requester is signed in with an authorised department. The required category exists; an assistant draft, if used, has not yet submitted the request.

**Main success scenario:**
1. The Requester opens UI-06 and enters the purpose, category, specifications, quantity, minimum condition, urgency, delivery location, required-by date and optional description.
2. The system validates the information and lets the Requester review the draft (RQ-01).
3. The Requester confirms submission. The system sets Pending department approval (RQ-02) and creates the department approval task.
4. An eligible receiving Department representative reviews the need and approves it through UC-08.
5. The system sets Open (RQ-03), notifies the Requester and shows the next available actions: classic search, optional ranked-match review and reservation of an eligible listing.

**Alternative and exception flows:**
2a. The date is in the past or the quantity is not a positive whole number: the system preserves the form and explains the correction.
4a. Changes are requested: the request returns to Draft with the reason. A rejection sets Rejected (RQ-08) and records the reason.
5a. The Requester changes approved quantity, specifications or date: the system returns the request to Pending department approval before further fulfilment.
5b. The Requester cancels before fulfilment: the request becomes Cancelled (RQ-09) and any linked hold is released as required by BR-20.
5c. No eligible resource exists: the Requester may close the request as No suitable item (RQ-07); purchasing remains outside the system and no avoided purchase is counted.
5d. The required-by date passes before fulfilment: the system sets Expired (RQ-10), releases a linked reservation and notifies the Requester.

**Postcondition:** A submitted request has a traceable department decision. Matching and reservation require department approval; fulfilment requires an approved transfer and confirmed receipt through UC-09. Submission or an AI suggestion alone grants no approval.

<!-- pagebreak -->
#### UC-05 Search and filter assets

**Actors:** Staff user, especially Requester.

**Related requirements:** FR-08.1 to FR-08.6, FR-02.2, FR-06.3, FR-06.4; AI-13; BR-14, BR-16.

**Precondition:** The user is signed in. The system knows which published summaries and department records the user may view.

**Main success scenario:**
1. The user opens UI-05, enters keywords and selects filters such as category, condition, department, location and available quantity.
2. The system searches authorised records using the combined criteria and returns the result count and permitted sort options.
3. The user opens a listing to inspect its specifications, condition, quantity, restrictions and last verification date.
4. The user refines the criteria or chooses a listing for an Open request. The reservation workflow rechecks all mandatory constraints before confirming a hold.

**Alternative and exception flows:**
2a. No listing matches: the system explains the empty result and offers to start a request using the same criteria.
2b. AI is unavailable: classic keyword search, filters and sorting still work.
3a. The listing is unpublished: another department cannot view it. An expired verification displays Verification needed and prevents an unverified reservation confirmation.
4a. Availability changes after the results were displayed: the system shows the current quantity and requires a fresh eligibility check instead of relying on an old search result.

**Postcondition:** The user has inspected authorised results. Searching or selecting a result does not create a reservation, approval or ownership change.

<!-- pagebreak -->
#### UC-06 Review ranked matches

**Actors:** Requester; AI service (supporting).

**Related requirements:** AI-02 to AI-05, AI-11 to AI-13; FR-08.6, FR-09.1; BR-14, BR-15.

**Precondition:** The Requester has an Open request and may view its candidate listings. Ranked matching is available, or a classic alternative can be used.

**Main success scenario:**
1. The Requester opens UI-07 from an approved request and asks to review matching resources.
2. The system performs Check eligibility using access rights, availability, quantity, required condition, compatibility and required date before sending eligible candidates for AI ranking.
3. The AI service ranks the eligible candidates. The system records the task, model identifier/version where available and response time.
4. The system displays ranked matches with compatibility scores, explanations, unresolved information and separate confidence information or its unavailability.
5. The Requester reviews the evidence and selects a preferred eligible result, including another eligible result instead of the first-ranked one. The system records the user's response to the recommendation.
6. The system offers UC-07 for the selected listing and rechecks eligibility when a hold is requested.

**Alternative and exception flows:**
2a. No eligible candidate remains: the system gives an empty-result explanation and offers classic search or the No suitable item outcome in UC-04.
3a. AI fails, times out or returns invalid or insufficiently confident output: the system preserves the request and makes classic search and filters available under AI-13.
4a. Evidence is incomplete: the system identifies missing information and does not make a candidate actionable unless the mandatory constraints can be confirmed.
5a. The user rejects all suggestions: no quantity is held; the user may refine the request or continue with classic search.

**Postcondition:** The reviewed recommendation and user response are recorded. Selecting a result does not reserve it or bypass approval. This use case optionally extends UC-04 after department approval.

<!-- pagebreak -->
#### UC-07 Reserve asset

**Actors:** Requester, releasing Asset custodian or Department representative.

**Related requirements:** FR-09.1 to FR-09.7, FR-11.1, FR-06.4, FR-05.3; BR-02, BR-11, BR-12, BR-14 to BR-16, BR-20.

**Precondition:** The Requester has an Open request (RQ-03) and has selected a Published listing (LS-03) with a suitable quantity.

**Main success scenario:**
1. The Requester chooses the listing and quantity and confirms a reservation request.
2. The system checks permissions, quantity and mandatory constraints, creates Requested (RV-01) and sets the request to Reservation requested (RQ-04).
3. The releasing Asset custodian or Department representative checks the stock and confirms current condition and availability. If verification is stale, the custodian verifies the asset before confirmation.
4. An eligible releasing user confirms the hold independently of the requester under Table 5.2.
5. The system records the hold and updates the available quantity together, preventing another user from receiving the same units, and sets Confirmed (RV-02). A listing with no remaining offered quantity becomes Fully reserved (LS-04).
6. The system shows the hold expiry from TBD-3 and notifies both sides that transfer approval is still required.

**Alternative and exception flows:**
2a. The requested quantity is invalid or unavailable: the system refuses it and shows the current quantity.
4a. The releasing side declines: the reservation becomes Declined (RV-03), a reason is recorded and the request returns to Open.
5a. Two users attempt to hold the last units simultaneously: only one confirmation succeeds; the other is told that the quantity is no longer available.
6a. The hold expires without an approved transfer: the system sets Expired (RV-05), releases the quantity and notifies both sides. A permitted cancellation uses RV-06 and also releases the hold.
6b. The Requester proceeds with the confirmed hold: the system creates a transfer in Pending release approval (TR-01), links the reservation as Converted to transfer (RV-04) and sets the request to In transfer (RQ-05). UC-08 carries out the required approvals before UC-09.

**Postcondition:** A successful reservation holds the quantity for the configured period; it is not transfer approval. Rejected, expired or cancelled holds leave no duplicate allocation.

<!-- pagebreak -->
#### UC-08 Approve workflow step

**Actors:** Department representative, Finance officer, Procurement officer, Sustainability officer; Business administrator for role authorisation; Asset custodian for record/hold confirmations in Table 5.2.

**Related requirements:** FR-10.1 to FR-10.8, FR-16.1 to FR-16.5; BR-01 to BR-10, BR-20.

**Precondition:** A Pending task (AT-01) exists for an allowed stage in Table 5.2. The user has the assigned role and department and is not the requester or creator of that approval record.

**Main success scenario:**
1. The approver opens the assigned task in UI-08.
2. The system shows the record version, creator, relevant asset and quantity, costs, evidence, prior decisions and any AI suggestion.
3. The system checks that the user may decide this stage and that earlier required stages have been completed.
4. The approver reviews the evidence and confirms Approve.
5. The system records Approved (AT-02) with the user, role, time and approved record version, and advances the parent record according to section 4.2 and Table 5.2.
6. The system performs Send notification to the users involved and creates the next required task where applicable. A transfer reaches Approved (TR-04) only after both department stages and any required policy stages.

**Alternative and exception flows:**
3a. The user lacks the assigned role or is the creator/requester: the system refuses the decision. The Business administrator may reassign it only to an eligible user.
4a. The approver rejects or requests changes: the system requires a reason, saves AT-03 or AT-04 and uses the parent's defined rejection or revision path. Held quantity is released where the rejected workflow requires it.
5a. The record version or decision has changed: the system refuses a stale or duplicate decision and shows the current task. Changes affecting an existing approval create a new task under FR-10.7.
6a. The task stays pending beyond TBD-5: the system marks it overdue and reminds the assigned approvers; overdue status does not automatically approve it.

**Postcondition:** One authorised decision is recorded and the parent follows its allowed transition. No earlier stage, required approver or human decision is bypassed.

<!-- pagebreak -->
#### UC-09 Confirm handover and receipt

**Actors:** Releasing and receiving Asset custodians; Department representatives inspect decisions and resolve disputes.

**Related requirements:** FR-11.1 to FR-11.7, FR-05.3, FR-05.4; BR-05, BR-06, BR-11, BR-13, BR-20.

**Precondition:** The linked transfer is Approved (TR-04). Both department approvals and any Finance/Procurement stage required by BR-06 are complete; the agreed quantity remains allocated to this transfer.

**Main success scenario:**
1. The releasing and receiving custodians open UI-09 and confirm the collection or delivery arrangement and planned date.
2. The releasing custodian records actual quantity, condition and handover evidence and confirms handover.
3. The system sets Handed over (TR-05) and the asset to In transfer (AS-05). Ownership remains with the releasing department while receipt is outstanding.
4. The receiving custodian checks the delivered quantity and condition against the agreed transfer and confirms receipt.
5. The system sets Completed (TR-06), updates the owning department, custodian and location under BR-13, moves the received asset to In service or In storage, and sets the linked request to Fulfilled (RQ-06).
6. The system records both confirmations in the history, notifies the parties and provides the transfer record for reconciliation with the existing register.

**Alternative and exception flows:**
1a. A required approval is missing: the system blocks handover and identifies the outstanding stage.
2a. The transfer is cancelled before handover: the system sets Cancelled (TR-09), releases the held quantity and records the reason.
4a. Quantity or condition differs: the system sets Disputed (TR-07), retains the existing ownership and notifies both department representatives. Resolution follows the TR-07 paths: receipt and completion, or return and cancellation.
5a. Another user has already confirmed receipt: the system displays the completed record and does not apply ownership or quantity changes twice.

**Postcondition:** Ownership, custody and location change only after a valid receipt. An unresolved dispute leaves ownership unchanged and remains visible to the responsible users.

<!-- pagebreak -->
#### UC-10 Manage maintenance work

**Actors:** Asset custodian, Maintenance staff, owning Department representative; Finance officer where the spending threshold applies.

**Related requirements:** FR-12.1, FR-12.2, FR-13.1 to FR-13.7; BR-02, BR-07, BR-20.

**Precondition:** The asset exists and the user may report or maintain it. Approval thresholds retain their Appendix C status.

**Main success scenario:**
1. The custodian or department representative records a defect through UI-10. The system opens Reported (MW-01) and notifies Maintenance staff.
2. Maintenance staff inspect the asset, record findings, condition and evidence, and assess the work and estimated cost in Under assessment (MW-02).
3. The system sends the estimate to Awaiting cost approval (MW-03). The owning Department representative decides first; Finance also decides when BR-07 applies.
4. After the required approvals, the system sets Approved (MW-04) and keeps the asset Under maintenance (AS-04), unavailable for publication or reservation.
5. Maintenance staff carry out the approved work in In progress (MW-05) and record parts, labour, actual cost, outcome and resulting condition.
6. The system checks spending approval before setting Completed (MW-06), restores the asset to its previous In service or In storage state, and records the result in its history.

**Alternative and exception flows:**
2a. Inspection identifies an unsafe or Not working item: publication and reservation are blocked under FR-12.2.
3a. Spending is rejected: the system sets Rejected (MW-08), records the reason and allows no unapproved work.
5a. Actual cost would exceed the approved amount: the work order returns for cost approval under BR-07; it cannot be completed until the difference is approved.
5b. The item is Not repairable: the system records MW-07, sets the asset to Retired (AS-06) and opens an end-of-life proposal (EL-01) for UC-11.
5c. A permitted withdrawal cancels the work order: the system records MW-09 with a reason and follows the allowed asset transition without treating unfinished work as a completed repair.

**Postcondition:** Completed work has approved spending, recorded costs and a resulting condition. An unrepairable item moves to a reviewed end-of-life process rather than being disposed of automatically.

<!-- pagebreak -->
#### UC-11 Decide end-of-life action

**Actors:** Department representative or Asset custodian proposes and records completion; Sustainability officer reviews; Finance officer approves write-off; AI service optionally provides advice.

**Related requirements:** FR-14.1 to FR-14.7, AI-06, AI-11 to AI-13; BR-02, BR-08, BR-09, BR-15.

**Precondition:** An authorised user has identified an asset for an end-of-life review or UC-10 has opened a proposal. Its previous state is recorded for restoration if the proposal is rejected.

**Main success scenario:**
1. The department representative or custodian opens UI-11 and prepares Proposed (EL-01) with the action, quantity, recipient/destination, reason and evidence. The reviewed asset is Retired (AS-06).
2. The system shows the reuse-first order and collects reasons why earlier options are unsuitable. If the desirable AI advice feature is used, its output is shown as a recommendation for review.
3. The proposal moves to Under sustainability review (EL-02). The Sustainability officer checks the evidence and any special-handling/EHS consultation and data-erasure record required by BR-09.
4. The eligible Sustainability officer approves the review, and the system sends the proposal to Awaiting finance approval (EL-03).
5. The eligible Finance officer approves the write-off. The system sets Approved (EL-04) and enables completion recording.
6. After the approved donation, disassembly, recycling or disposal is carried out, the custodian records date, responsible person, quantity, destination and evidence. The system sets Completed (EL-05), the appropriate final asset state AS-07 to AS-10, and removes that quantity from availability.

**Alternative and exception flows:**
2a. AI advice is unavailable or rejected: the authorised staff continue the classic evidence-based review; no recommendation is treated as permission.
3a. Required evidence is missing: the reviewer requests changes, returning the proposal to EL-01. Approval remains blocked until the required records are present.
4a. The action is rejected: the system sets Rejected (EL-06), records the reason and restores the previous asset state. If reuse or repair remains suitable, the appropriate transfer or maintenance workflow can then be used.
5a. Finance rejects the write-off: the proposal follows EL-06 and no final action is authorised.
6a. The action is disassembly: usable parts are registered through UC-02 as new assets linked to the original record.

**Postcondition:** A completed final action has independent Sustainability and Finance decisions and completion evidence. Rejected proposals do not authorise disposal and restore the asset's previous state.

<!-- pagebreak -->
#### UC-12 Ask the campus assistant

**Actors:** Staff user; AI service (supporting).

**Related requirements:** AI-07, AI-08, AI-11 to AI-13; FR-02.2, FR-07.1 to FR-07.3; BR-01, BR-03, BR-15.

**Precondition:** The user is signed in with an authorised department. The desirable assistant feature is enabled and the AI service is available for the main path.

**Main success scenario:**
1. The user opens UI-12 and asks a resource, authorised asset-history, request-status or guidance question.
2. The system limits the available context to records and approved guidance the user's role and department may access.
3. The AI service returns an answer. The system labels it as generated, shows supporting records where available and identifies missing information or uncertainty.
4. The user inspects the answer and may ask a follow-up question. The system records the interaction and user response as required by the AI tracking requirements.

**Alternative and exception flows:**
2a. The question asks for restricted data: the system declines to disclose it and explains the permitted scope without revealing the protected record.
3a. The service is unavailable, times out or returns an unsupported answer: the system preserves the user's input and offers classic search, forms or help.
3b. The assistant proposes a resource request or record change: the system shows the exact proposed fields. The user accepts, corrects or cancels them; only explicit confirmation passes them to the normal validated workflow. A submitted request still becomes Pending department approval under UC-04.
4a. The user asks the assistant to approve a transfer or dispose of an item: the system offers guidance only and leaves the decision to the assigned human role through UC-08 or UC-11.

**Postcondition:** The user receives a reviewable answer or a classic alternative. An assistant response alone changes no record, role, ownership or approval state.

<!-- pagebreak -->
#### UC-13 Generate and review report

**Actors:** Business administrator, Finance officer, Procurement officer, Sustainability officer; AI service supports generated narrative.

**Related requirements:** FR-17.1 to FR-17.5, AI-09 to AI-13, SU-01 to SU-09; BR-10, BR-15, BR-18.

**Precondition:** The user is signed in and may view the chosen departments and report data. Source transactions and any indicator inputs are available or their absence can be reported.

**Main success scenario:**
1. The user opens UI-13 and selects a report type, period and authorised departments.
2. The system produces the conventional report with its filters, record counts, totals, units, source records and limitations, marked Draft.
3. If a narrative summary is requested, the system sends authorised report data to the AI service and displays the generated text as a draft with supporting sources, model information and uncertainty where available.
4. The relevant data owner checks the figures and any narrative against the conventional totals and records corrections. Finance reviews costs/savings, Sustainability reviews sustainability figures, and the Business administrator reviews operational figures.
5. After the required data-owner review, the system marks the report Reviewed by with the reviewing user and date. A report covering several data domains remains Draft until each responsible owner has checked their figures.

**Alternative and exception flows:**
2a. An indicator input or defensible factor is missing: the system shows N/A or an explicitly identified estimate, not an invented saving or carbon result.
3a. AI is unavailable: the conventional report remains usable and no generated narrative is required to view its totals.
4a. A generated claim is unsupported or its total differs: the data owner rejects or corrects the draft; it cannot become an official summary while the inconsistency remains.
4b. A Procurement officer or other viewer is not the required data owner: they may inspect authorised data and provide comments, but cannot substitute for the BR-10 review.
5a. Desirable export is available: the user may obtain the authorised CSV or printable report with its filters and review status.

**Postcondition:** A traceable report is available with its actual review status. Official figures derive from the defined records and formulas; unaccepted AI suggestions and unfulfilled requests do not count as realised benefits.

<!-- pagebreak -->
#### UC-14 View asset history and audit log

**Actors:** Asset custodian, Business administrator; other staff only where their role permits access to the underlying record.

**Related requirements:** FR-15.1, FR-15.2, FR-18.1 to FR-18.4, FR-02.2; BR-17.

**Precondition:** The user is signed in and may view the asset history or, for the Business administrator, the audit records within their assigned scope.

**Main success scenario:**
1. The custodian opens an authorised asset's history in UI-04, or the Business administrator opens the audit view.
2. The system displays the recorded events with date, actor, action, state changes, approvals, costs and available evidence; the audit view also shows reasons and before/after values.
3. The user filters the history by event type and period. The Business administrator may search audit records by user, record, action and period.
4. The user opens a supporting record. The system checks access again before displaying its details.
5. The Business administrator may export the authorised audit results as CSV under FR-18.3. The system retains the original entries for the TBD-7 period.

**Alternative and exception flows:**
2a. No events match: the system explains the empty result and keeps the filters available.
4a. A supporting record is outside the user's access: the system refuses disclosure even if a link is visible elsewhere.
5a. Any user tries to edit or delete an audit entry: the system refuses. A correction is a new traceable entry referring to the original under BR-17.

**Postcondition:** The user has inspected permitted history or audit evidence. Reading or exporting it does not alter the underlying asset, decisions or original audit entries.


