# 5. Human Approval Points

AI can suggest, explain and prepare drafts. It cannot approve transfers, spending, end-of-life actions, financial values or user-role changes. A high compatibility score or confidence value never replaces a required human decision (AI-11, BR-15).

**Design choice.** Classic and AI-assisted actions use the same approval workflow. A separate workflow for AI actions would duplicate the role checks, approval stages and audit rules. We use one workflow so that both routes apply the same controls. AI can reduce preparation work, but it does not remove the time needed for human review.

Reviewing an AI suggestion is different from approving a business action. For example, accepting a category suggestion helps complete an asset draft; the asset still needs the confirmation required by SRS Table 5.2.

## 5.1 Human Review of AI Outputs

**Table 5.1 AI review points**

<!-- widths: 1800,1900,3400,2260 -->
| Decision | Person responsible | What the person sees | What is recorded |
|---|---|---|---|
| Accept, correct or reject asset suggestions | Asset custodian or Department representative | Entered details, suggested values, supporting information, confidence or its unavailability, and any missing information. | The response and any correction in AiSuggestion, with an audit entry. Final asset confirmation remains a separate step (AI-01, AI-12). |
| Choose a recommended asset or another eligible option | Requester | Eligible listings, compatibility scores, matching reasons, confidence, condition, quantity, costs and unresolved concerns. | The choice in MatchRecommendation and the reason for an override. Choosing an item does not automatically reserve it (AI-05.2, BR-15). |
| Review sustainable-action advice | Asset custodian, Department representative or Sustainability officer, within their permitted role | Condition, demand, repair options, costs, reuse-first reasoning, missing evidence and any special-handling requirements. | Acceptance, correction or rejection in AiSuggestion. An accepted suggestion remains a proposal for the approval stages below (AI-06, BR-08, BR-09). |
| Confirm an assistant's proposed action | The signed-in user, provided their role allows the action | The exact proposed fields or changes, supporting records, validation errors and the next approval stage. | The user's response in AiSuggestion. A valid confirmed action enters the normal workflow; cancellation leaves the target record unchanged (AI-08, BR-15). |
| Review an AI-generated report for official use | Finance officer for financial figures; Sustainability officer for sustainability figures; Business administrator for operational figures | The draft, reporting period, filters, source totals, supporting records, estimates and missing information. | The review outcome, reviewer and date. The report remains Draft until the relevant data owners review it. The same ownership applies to conventional reports (AI-10, FR-17.4, BR-10). |

Each AI output remains linked to its ModelVersion record. The original output and the user's response are kept separately so a correction does not hide what the AI originally suggested (AI-12, section 8).

## 5.2 Business Approvals and Operational Confirmations

The following points follow SRS Table 5.2 and the access matrix in section 6.2. Every formal approval requires the correct role and department. The creator or requester cannot approve their own record, even if they hold several roles (BR-02).

**Table 5.2 Business approval and confirmation points**

<!-- widths: 1600,2500,3000,2260 -->
| Workflow | Person responsible | Information reviewed | Recorded result |
|---|---|---|---|
| Role assignment | Business administrator authorises; System administrator applies the authorised assignment. | User, requested role, department scope and recorded authorisation. | The authorisation, applied role and audit entries. Technical access does not grant business approval rights (BR-01). |
| Asset confirmation | An eligible Asset custodian or Department representative who did not create the record. | Asset details, condition, quantity, value, evidence and any accepted AI suggestions. | Confirmation and the move from Draft to In service or In storage. A rejected record stays in Draft (FR-04.3, BR-02). |
| Listing release | Owning Department representative. | Ownership, available quantity, condition, restrictions and the asset's verification information. | Release decision and publication as LS-03, or return to Draft (BR-04). |
| Resource request | Requester's Department representative. | Purpose, specifications, quantity, urgency, location and required date. | Department approval opens the request as RQ-03. An assistant confirmation alone cannot open it (BR-03). |
| Reservation hold | Releasing Asset custodian or Department representative. | Approved request, published listing, quantity, current availability, verification date and hold expiry. | Confirmation as RV-02 or decline as RV-03. The hold is not transfer approval (BR-11, BR-12, BR-16). |
| Transfer approval | Releasing Department representative, then receiving Department representative, followed by Finance and/or Procurement when BR-06 applies. | Asset, quantity, both departments, value, costs, category restrictions, delivery arrangements and supporting evidence. | Each approval stage is recorded separately. The transfer reaches TR-04 only when all required stages pass (BR-05, BR-06). |
| Handover and receipt | Releasing Asset custodian confirms handover; receiving Asset custodian confirms receipt. | Approved transfer, actual quantity, condition and handover evidence. | Handover gives TR-05. Matching receipt gives TR-06 and updates ownership, custody and location. A discrepancy gives TR-07 and keeps ownership unchanged (BR-13, FR-11.3 to FR-11.5). |
| Repair spending | Owning Department representative, plus Finance officer when the estimate reaches the spending threshold. | Inspection findings, planned work, estimate and any difference from previously approved spending. | Cost approval is recorded before the work starts. If actual cost exceeds the approved amount, the difference needs approval before completion (BR-07, FR-13.5). |
| End-of-life action | Sustainability officer reviews first; Finance officer then approves the write-off. | Reuse and repair alternatives, reason for the proposed action, value, recipient or destination, and required EHS and data-erasure evidence. | Approval gives EL-04. Completion evidence is recorded separately before EL-05 and the final asset state (BR-08, BR-09). |

EHS consultation is supporting evidence under BR-09. It does not create an additional system role or replace the Sustainability officer's review.

Transfer and repair thresholds remain the policy values identified by TBD-1 and TBD-2. This design does not introduce new financial limits.

## 5.3 Financial Values and Avoided-Purchase Claims

Financial values are entered or confirmed by users who have permission to edit the relevant record. For example, asset values belong to the asset-record workflow and repair costs belong to the maintenance workflow. AI cannot change these values on its own. Finance approval and official financial-report review remain subject to BR-06, BR-07 and BR-10.

An avoided purchase requires a fulfilled request and a human confirmation that a new purchase would otherwise have been needed. The system records the reviewer, quantity and replacement-cost estimate with its source (BR-18, SU-03). An AI recommendation or a completed transfer alone is not enough to count an avoided purchase.

**Role to confirm.** BR-18 identifies an authorised reviewer but does not name a specific role. The team must confirm that permission before implementation. Until it is assigned, the system must not accept an avoided-purchase confirmation or count the claim.

## 5.4 Enforcement and Audit Records

The application applies these controls on the server:

1. Check the user's identity, role, department and access to the record.
2. For an approval task, check that the user is not the creator or requester and that the task applies to the current record version.
3. Show the evidence needed for the decision. If required evidence is missing, explain what must be completed before approval.
4. Record the decision and any allowed state change together with the audit entry. Display the resulting in-application notification after the change is saved.
5. Require a reason for rejection, requests for changes and cancellation. Release held quantities where the rejected or cancelled workflow requires it (BR-20).
6. If approved quantity, value, recipient or action changes, withdraw the affected approval and create a new task (FR-10.7).
7. Apply the same controls when AI is unavailable or when the user follows a classic alternative.

Each formal decision records the approver, role, date and time, reason and record version (FR-10.6). AuditLog also records the action, affected record and relevant before-and-after values. AI corrections, rejections and overrides include the user's reason (AI-12.3).

Audit entries can only be added. Corrections use a new entry linked to the original, as described in section 6.3 (BR-17). Passwords, service keys and unnecessary personal data are excluded from these records.