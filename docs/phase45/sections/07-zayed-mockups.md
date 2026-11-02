<!-- pagebreak -->
# 7. Mockups

These mockups cover the eight screen areas in the project brief. Transfer approval includes the approval view (UI-08) and the handover and receipt view (UI-09). Sustainability Dashboard and Reports are two views of UI-13. Their Phase 3 IDs stay the same.

We use the supplied Dawra Campus logo, navy for main actions and teal for AI advice. Labelled forms keep entered details separate from AI suggestions. Each screen shows the active role, department, record state and the person's next decision. A state is the current step, such as Draft or Open. A version identifies the saved revision being reviewed.

Compatibility scores how well an item meets a request, from 0 to 100. Confidence is the AI's reported certainty; it does not prove that an answer is correct. Matching confidence of at least 0.75 is shown normally. From 0.50 to below 0.75, it is marked Check carefully. Below 0.50, the AI recommendation is withheld and ordinary keyword search and filters remain available. Classification confidence of at least 0.60 can fill suggestions for review; below 0.60, the suggestion is an option only. Missing confidence or model information is labelled unavailable (SRS Table 4.2; AI-01, AI-04, AI-05).

Fallback means using normal forms, search or review when AI cannot help. Input is kept and the alternative appears within 15 seconds of the original AI request, including repeated attempts (AI-13.2, NFR-07). People still decide every approval. Access, independent approval and the latest saved version are checked by the application (FR-02.2, FR-10.4, FR-10.7, BR-02, BR-20).

All shown records, scores and outputs are made-up examples, called synthetic data. Money uses AED and action times use Gulf Standard Time (GST, UTC+4). The design targets keyboard use, visible focus, labelled fields and readable phone and laptop layouts. Checks against the Web Content Accessibility Guidelines (WCAG) remain part of implementation (DR-02, NFR-01, NFR-04, SRS section 3.1.1).

<!-- pagebreak -->
## 7.1 Asset Registration

**Screen:** UI-03. **Role:** Asset custodian in Engineering. **Example state:** Draft (AS-01).

![Figure 7.1 Asset registration UI-03](images/figure-7-1-ui-03.png)

<!-- pagebreak -->
### UI-03 Fields and decisions

Verification records who checked the item and when. HDMI and DisplayPort are video connections used to check whether the monitor fits the request. FHD means Full HD, a screen resolution of 1920 x 1080. A duplicate is a possible second record for the same item.

<!-- widths: 2600,6760 -->
| Field | Synthetic example |
|---|---|
| Asset ID | AST-0042 (assigned on save) |
| Name * | Dell P2422H monitor |
| Description * | 24-inch monitor with stand and power cable |
| Category / subcategory * | Electronics / Monitors |
| Quantity / unit * | 1 / item |
| Owner / custodian * | Engineering / Demo Custodian A |
| Building / room * | Main Campus A / A-210 |
| Purchase date * | 15 Sep 2023 |
| Estimated value * | AED 450.00 |
| Condition * | Good |
| Technical specifications * | 24-inch, 1920 x 1080, HDMI, DisplayPort |
| Initial confirmed state * | In storage (AS-03) |
| Photos | monitor-front.jpg (1.2 MB); 1 of 5 |
| Supporting document | spec-sheet.pdf (240 KB) |
| Verification | 30 Oct 2026 / Demo Custodian A |

**AI result:** Category: Electronics / Monitors. Tags: display, HDMI, office. Description: 24-inch FHD monitor with stand.

**Confidence:** 0.86. Model/version unavailable in this example.

**Reason:** The title and specifications identify a monitor. Screen size and HDMI are stated in the supplied text.

**Human decision:** Accept, edit or reject each suggestion before confirming the asset. Confirmation records the user and time; it does not publish a listing.

**Low or unavailable confidence:** Confidence 0.54, below 0.60. Category is an option only. No suggested value is filled in; choose it manually.

**AI unavailable:** Classification unavailable. Your fields are preserved. Select category and enter description manually.

JPG/PNG: up to 5 files, 5 MB each. PDF: 10 MB each. A possible duplicate requires a separate confirmation. Invalid required fields keep AS-01.

**Phase 3 references:** UC-02; FR-04.1 to FR-04.6; FR-05.1; AI-01.1 to AI-01.4; AI-12.1 to AI-13.4; BR-15; AS-01, AS-03.

<!-- pagebreak -->
## 7.2 Request Submission

**Screen:** UI-06. **Role:** Requester in Computing. **Example state:** Draft (RQ-01).

![Figure 7.2 Request submission UI-06](images/figure-7-2-ui-06.png)

<!-- pagebreak -->
### UI-06 Fields and decisions

An assistant draft is a proposed set of fields that the requester must check. Submission sends the request to department approval; it does not approve the request. A required-by date is the date when the item is needed.

<!-- widths: 2600,6760 -->
| Field | Synthetic example |
|---|---|
| Request ID | REQ-0018 |
| Category * | Electronics / Monitors |
| Purpose * | Second display for a teaching workstation |
| Technical specifications * | 24-inch or larger, 1920 x 1080, HDMI |
| Quantity * | 1 item |
| Minimum condition * | Good |
| Urgency * | Normal |
| Delivery location * | Main Campus A / A-315 |
| Required by * | 12 Nov 2026 |
| Description | A monitor for the teaching assistant desk |
| Requester | Demo Requester B |
| Next responsible role | Computing Department representative |

**AI result:** Optional assistant draft: category Electronics / Monitors, quantity 1, minimum condition Good. Required-by date still needs your confirmation.

**Confidence:** Unavailable - check carefully. Model/version unavailable in this example.

**Reason:** The draft uses your stated monitor requirement. The assistant cannot infer a required-by date or approve department need.

**Human decision:** Check and correct the fields, then submit to the department. Submission creates RQ-02. Search and reservation do not bypass department approval.

**Low or unavailable confidence:** Confidence unavailable - check carefully. The draft cannot supply missing fields. Confirm the date and specifications yourself.

**AI unavailable:** Assistant unavailable. Continue with the normal request form; your entered fields remain.

Positive whole quantity and a future required-by date are required. Changes to quantity, specifications or date after approval return the request to RQ-02.

**Phase 3 references:** UC-04, UC-12; UI-06; FR-07.1 to FR-07.9; AI-08.1 to AI-08.3; BR-03, BR-15; RQ-01, RQ-02.

<!-- pagebreak -->
## 7.3 Recommendation Review

**Screen:** UI-07. **Role:** Requester in Computing. **Example state:** Open (RQ-03).

![Figure 7.3 Recommendation review UI-07](images/figure-7-3-ui-07.png)

<!-- pagebreak -->
### UI-07 Fields and decisions

Eligibility means passing every required check before an item can be offered. Similarity measures how closely the item description matches the request. Each factor contributes points to compatibility. Unknown optional details earn zero points. An override reason explains why the requester chose another eligible ranked item.

<!-- widths: 2600,6760 -->
| Field | Synthetic example |
|---|---|
| Required resource | 1 monitor, Good or better, HDMI |
| Required by | 12 Nov 2026 |
| Selected listing | LST-0024 / AST-0042 |
| Asset | Dell P2422H monitor |
| Owner / location | Engineering / A-210 |
| Listing / quantity | Published (LS-03) / 1 available |
| Condition / verified | Good / 30 Oct 2026 |
| Availability / restrictions | Available now / collection required |

**AI result:** Compatibility 87/100. Meaning 27/30; technical 20/20; condition 5/15; location 10/10; availability 10/10; useful life 10/10; repair 5/5.

**Confidence:** 0.82. Model/version unavailable in this example.

**Reason:** Similarity 0.90; all requested specifications met; condition equals minimum; same building; available now; estimated life 3 years; no repair needed.

**Human decision:** Inspect evidence and choose any eligible result. Selection alone holds nothing. Request reservation, then wait for independent releasing-side confirmation.

**Low or unavailable confidence:** Confidence 0.62: Check carefully. Below 0.50 the result is withheld as an AI recommendation; use classic search. Unsupported confidence is labelled unavailable.

**AI unavailable:** AI ranking unavailable. Eligible keyword and filter results remain available without AI scores. Current quantity is checked again when reserving.

All mandatory checks passed: access, quantity, condition, specifications and date. Missing mandatory data excludes an item. Optional unknowns are labelled and earn 0 factor points. Another eligible example: AST-0071, compatibility 83, confidence unavailable; choosing it requires an override reason.

**Phase 3 references:** UC-05 to UC-07; FR-08.1 to FR-09.7; AI-02 to AI-05; AI-13; NFR-07; BR-11 to BR-16; RQ-03, RV-01.

<!-- pagebreak -->
## 7.4 Transfer Approval

**Screen:** UI-08. **Role:** Department representative in Engineering. **Example state:** Pending release approval (TR-01).

![Figure 7.4 Assigned transfer approval UI-08](images/figure-7-4-ui-08.png)

<!-- pagebreak -->
### UI-08 Fields and decisions

A threshold is the value that makes an extra approval necessary. TBD-1 is the existing Phase 3 name for the transfer-value threshold that KU Finance must set. Procurement reviews categories controlled by purchasing rules. An independent approver is someone other than the requester or record creator. Version v3 means the third saved revision.

<!-- widths: 2600,6760 -->
| Field | Synthetic example |
|---|---|
| Assigned task | AT-0041 / Pending (AT-01) |
| Stage / version | Release approval / TRF-0009 v3 |
| Requester / creator | Demo Requester B / Demo Requester B |
| Approver | Demo Representative C (independent) |
| Asset / quantity | AST-0042 / 1 monitor |
| From / to | Engineering / Computing |
| Estimated asset value | AED 450.00 (synthetic estimate) |
| Transfer cost | AED 0.00 / collection within same building |
| Evidence | verification-0042.pdf; request REQ-0018 |
| Next stage | Computing receipt approval (TR-02) |
| Policy checks | Finance if value meets TBD-1; Procurement if flagged |
| Decision reason | Required for rejection or changes; optional for approval |

**AI result:** Linked match: compatibility 87/100. HDMI and date requirements met. This is advisory evidence attached to v3.

**Confidence:** 0.82. Model/version unavailable in this example.

**Reason:** The recommendation references AST-0042 and REQ-0018. It does not verify policy authority or decide the transfer.

**Human decision:** Review this version and decide only your assigned stage. Both departments must approve, with conditional Finance and Procurement stages before TR-04.

**Low or unavailable confidence:** Linked confidence 0.62: Check carefully. Confidence cannot remove a required approval or make an ineligible transfer valid.

**AI unavailable:** AI explanation unavailable. Review the asset, request, quantities and evidence directly. Approval rules are unchanged.

TBD-1 has no confirmed value in Phase 3. AED 450 is not evidence that Finance approval can be skipped. A required unresolved policy stage stays pending. Self-approval and stale record versions are refused.

**Phase 3 references:** UC-08; FR-10.1 to FR-10.7; FR-11.1, FR-11.2; BR-01, BR-02, BR-05, BR-06, BR-20; AT-01 to AT-04; TR-01 to TR-04.

<!-- pagebreak -->
### 7.4.1 Handover and receipt

**Screen:** UI-09. **Role:** Asset custodian in Computing. **Example state:** Handed over (TR-05).

![Figure 7.5 Handover and receipt UI-09](images/figure-7-5-ui-09.png)

<!-- pagebreak -->
#### UI-09 Fields and decisions

Handover records the releasing custodian giving the item to the receiving side. Receipt records the receiving custodian checking and accepting it. A discrepancy is a difference in quantity or condition. Ownership is the department recorded as owning the item; custody identifies the person responsible for it.

<!-- widths: 2600,6760 -->
| Field | Synthetic example |
|---|---|
| Asset / approved quantity | AST-0042 / 1 monitor |
| From / releasing custodian | Engineering / Demo Custodian A |
| To / receiving custodian | Computing / Demo Custodian D |
| Approval record | Release, receipt and applicable policy stages complete |
| Arrangement / planned date | Collection / 05 Nov 2026 |
| Handover evidence | 1 item, Good; 05 Nov 2026 10:00 GST |
| Actual received quantity * | 1 |
| Received condition * | Good |
| New location * | Main Campus A / A-315 |
| Receipt evidence * | receipt-photo.jpg; cable and stand checked |
| Current owner | Engineering until receipt confirmation |
| Discrepancy reason | Required if quantity or condition differs |

**AI result:** Earlier match evidence: compatibility 87/100. No AI assessment of the physical handover or receipt.

**Confidence:** 0.82 (earlier match only). Model/version unavailable in this example.

**Reason:** The earlier recommendation explained fit to the request. The receiving custodian must inspect actual quantity and condition.

**Human decision:** Releasing custodian records handover only after TR-04. Receiving custodian confirms receipt after TR-05, or records a discrepancy. Ownership changes at valid receipt. A valid receipt restores In service (AS-02) or In storage (AS-03) under the new owner, and completes TR-06 / RQ-06.

**Low or unavailable confidence:** Earlier match confidence 0.62: Check carefully. Receipt relies on inspection and evidence; no new AI confidence is invented.

**AI unavailable:** AI unavailable. Use recorded approvals, handover evidence and physical inspection to complete the normal transfer workflow.

This is the receiving view. Releasing users see Record handover at TR-04. A discrepancy creates TR-07 and retains the owner; resolution permits receipt or return with cancellation. Duplicate receipt makes no second update. Receipt saves the new owner, custody, location and AS-02 or AS-03 together with the transfer and request states.

**Phase 3 references:** UC-09; FR-11.1 to FR-11.7; BR-11, BR-13, BR-20; TR-04 to TR-09; AS-02, AS-03, AS-05; RQ-05, RQ-06.

<!-- pagebreak -->
## 7.5 Maintenance Tracking

**Screen:** UI-10. **Role:** Maintenance staff in Engineering. **Example state:** In progress (MW-05).

![Figure 7.6 Maintenance tracking UI-10](images/figure-7-6-ui-10.png)

<!-- pagebreak -->
### UI-10 Fields and decisions

A work order records the maintenance job, costs and outcome. Labour is the cost of staff time. TBD-2 is the existing Phase 3 repair-spending threshold that KU Finance must set. End-of-life review decides the next action for an item that is no longer suitable for its current use.

<!-- widths: 2600,6760 -->
| Field | Synthetic example |
|---|---|
| Asset | AST-0091 / desktop computer |
| Asset state | Under maintenance (AS-04) |
| Defect / inspection | Fan failure / INS-0012 dated 30 Oct 2026 |
| Assessment | Replace failed fan, clean vents and test |
| Assigned technician | Demo Technician E |
| Approved estimate | AED 180.00 / department decision recorded |
| Finance stage | Required if TBD-2 applies; must be resolved before work |
| Parts / labour | Fan: AED 80.00 / 1 hour: AED 100.00 |
| Actual total | AED 180.00 |
| Outcome / condition | Passed test / Good |
| Return state | In service (AS-02), previous state |
| Work evidence | fan-replacement.jpg; test-result.pdf |

**AI result:** Optional sustainable-action advice: repair. Inspect the fan before replacing the complete computer.

**Confidence:** Unavailable - check carefully. Model/version unavailable in this example.

**Reason:** The inspection identifies one replaceable part. Demand, repairability and the AED 180 estimate support a repair proposal; they do not approve spending.

**Human decision:** Record work only after required cost approvals. Save actual cost and outcome. Any increase returns to MW-03 before completion. Not repairable starts EL-01.

**Low or unavailable confidence:** Confidence unavailable - check carefully. The SRS defines no numeric cutoff for action advice; insufficient evidence requires manual assessment.

**AI unavailable:** Action advice unavailable. Continue inspection and approved work using the recorded assessment and costs.

The sample assumes all applicable cost approvals have been recorded, without inventing a TBD-2 value. The custodian reports defects; department and conditional Finance approvers use UI-08. Unsafe or Not working assets cannot be published or reserved.

**Phase 3 references:** UC-10, UC-11; FR-12.1, FR-12.2; FR-13.1 to FR-13.7; AI-06; BR-07; MW-01 to MW-09; EL-01.

<!-- pagebreak -->
## 7.6 Sustainability Dashboard

**Screen:** UI-13. **Role:** Sustainability officer in Authorised departments. **Example state:** Draft.

![Figure 7.7 Sustainability dashboard UI-13](images/figure-7-7-ui-13-dashboard.png)

<!-- pagebreak -->
### UI-13 Fields and decisions

Deduplicated means each item is counted once. The reuse cohort is the group of listed items used to calculate the reuse rate. Net savings means estimated avoided purchases minus related costs. Apply filters changes the period and department scope. Only October 2026 for Engineering and Computing has sample data; other scopes show no example snapshot.

<!-- widths: 2600,6760 -->
| Field | Synthetic example |
|---|---|
| Report type | Sustainability and resource exchange |
| Period | 01 Oct 2026 to 31 Oct 2026 |
| Department filter | Engineering and Computing (authorised) |
| Waste diverted | 3 items / reuse 2, repair 1; deduplicated |
| Avoided purchases | 2 confirmed fulfilled requests / AED 900.00 estimated |
| Net financial savings | AED 720.00 estimated / costs AED 180.00 |
| Reuse cohort | 2 of 4 listed items / 50% |
| Repair success | 1 of 1 closed work orders / 100% |
| Asset-life extension | N/A / retirement dates missing |
| Estimated carbon reduction | N/A / emission factors missing |
| Sources | Completed TRF-0007, TRF-0008; MWO-0012 |
| Owner review | Sustainability pending; Finance pending; Business administration pending |

**AI result:** AI-generated draft: Two confirmed fulfilled requests avoided an estimated AED 900 in purchases. After AED 180 attributable costs, estimated net savings are AED 720. Carbon is N/A.

**Confidence:** Unavailable - check carefully. Model/version unavailable in this example.

**Reason:** All claims use snapshot S06. Confidence unavailable; factual support is checked against the linked conventional totals, not a generated certainty score.

**Human decision:** Review only your own domain. Sustainability reviews indicators, Finance reviews money, Business administration reviews operations. A mixed report stays Draft until every owner reviews.

**Low or unavailable confidence:** Confidence unavailable - check carefully. Unsupported claims or totals that disagree with S06 keep the narrative in Draft; no numeric cutoff is defined.

**AI unavailable:** Narrative generation unavailable. Conventional totals and their sources remain available for the same owner review.

All values are synthetic, not KU outcomes. Money figures are estimates. Snapshot S06 contains 3 distinct diverted items, 2 confirmed fulfilled requests, 4 cohort items and 1 successful closed repair. Missing inputs show N/A. Applied period and department filters persist across views and AI states.

**Phase 3 references:** UC-13; FR-17.1 to FR-17.4; AI-09, AI-10, AI-12, AI-13; SU-01 to SU-09; BR-10, BR-18.

<!-- pagebreak -->
## 7.7 Reports

**Screen:** UI-13. **Role:** Sustainability officer in Authorised departments. **Example state:** Draft.

![Figure 7.8 Report draft and source review UI-13](images/figure-7-8-ui-13-reports.png)

<!-- pagebreak -->
### UI-13 Fields and decisions

Deduplicated means each item is counted once. The reuse cohort is the group of listed items used to calculate the reuse rate. Net savings means estimated avoided purchases minus related costs. Apply filters changes the period and department scope. Only October 2026 for Engineering and Computing has sample data; other scopes show no example snapshot.

<!-- widths: 2600,6760 -->
| Field | Synthetic example |
|---|---|
| Report type | Sustainability and resource exchange |
| Period | 01 Oct 2026 to 31 Oct 2026 |
| Department filter | Engineering and Computing (authorised) |
| Avoided purchases | 2 confirmed fulfilled requests / AED 900.00 estimated |
| Net financial savings | AED 720.00 estimated / costs AED 180.00 |
| Asset-life extension | N/A / retirement dates missing |
| Estimated carbon reduction | N/A / emission factors missing |
| Sources | Completed TRF-0007, TRF-0008; MWO-0012 |
| Owner review | Sustainability pending; Finance pending; Business administration pending |

**AI result:** AI-generated draft: Two confirmed fulfilled requests avoided an estimated AED 900 in purchases. After AED 180 attributable costs, estimated net savings are AED 720. Carbon is N/A.

**Confidence:** Unavailable - check carefully. Model/version unavailable in this example.

**Reason:** All claims use snapshot S06. Confidence unavailable; factual support is checked against the linked conventional totals, not a generated certainty score.

**Human decision:** Compare each written claim with snapshot S06 and its source records. Sustainability reviews environmental figures, Finance reviews money and Business administration reviews operations. Return unsupported claims with comments. The mixed report stays Draft until all owners review it.

**Low or unavailable confidence:** Confidence unavailable - check carefully. Unsupported claims or totals that disagree with S06 keep the narrative in Draft; no numeric cutoff is defined.

**AI unavailable:** AI narrative unavailable. No new AI draft is generated. Conventional totals and linked records remain available for the same owner review.

The report view uses the same S06 records as the dashboard. AI-written text is labelled Draft. Estimated savings and missing carbon or life-extension inputs remain labelled. The Sustainability officer can approve only the sustainability figures.

**Phase 3 references:** UC-13; FR-17.1 to FR-17.4; AI-09, AI-10, AI-12, AI-13; SU-01 to SU-09; BR-10, BR-18.

<!-- pagebreak -->
## 7.8 Campus Assistant

**Screen:** UI-12. **Role:** Requester in Computing. **Example state:** Draft proposal.

![Figure 7.9 Campus assistant UI-12](images/figure-7-9-ui-12.png)

<!-- pagebreak -->
### UI-12 Fields and decisions

A supporting record is a permitted system record used as evidence for the answer. A proposal is a draft action that the user must check. Desirable means this feature is optional in the project scope. It follows the same access checks and approval steps as the normal forms.

<!-- widths: 2600,6760 -->
| Field | Synthetic example |
|---|---|
| Your message | Find one Good HDMI monitor for A-315 by 12 Nov 2026 |
| Supporting record | LST-0024 / published monitor summary |
| Proposed category | Electronics / Monitors |
| Purpose | Second display for a teaching workstation |
| Specifications | 24-inch or larger, 1920 x 1080, HDMI |
| Quantity / condition | 1 / Good |
| Urgency | Normal (confirm or change) |
| Delivery location | Main Campus A / A-315 |
| Required by | 12 Nov 2026 |
| Next state on submission | Pending department approval (RQ-02) |

**AI result:** I found a permitted listing that may fit. I can prepare the request fields shown here. Please check the purpose, specifications and urgency before opening the request form.

**Confidence:** Unavailable - check carefully. Model/version unavailable in this example.

**Reason:** Listing LST-0024 supports the monitor details. The normal form validates missing information and current access. Unconfirmed policy values cannot be answered as facts.

**Human decision:** Confirm the exact fields or correct or cancel the proposal. Open the normal form and submit explicitly. The assistant cannot approve, reserve or transfer an asset.

**Low or unavailable confidence:** Confidence unavailable - check carefully. If supporting records do not answer the question, the assistant says it cannot confirm the answer and asks for clarification.

**AI unavailable:** Assistant unavailable. Your message is preserved. Open marketplace search, the request form or help to continue.

Desirable feature. All nine roles can use the assistant within their existing permissions. The server rechecks access and input on confirmation. Cancellation leaves the target record unchanged. The answer shows supporting records and unavailable model information honestly.

**Phase 3 references:** UC-12, UC-04; UI-12; AI-07.1 to AI-08.4; AI-11 to AI-13; BR-01, BR-03, BR-15.

<!-- pagebreak -->
