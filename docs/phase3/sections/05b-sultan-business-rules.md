## 5.5 Business Rules

Business rules are the policies the system has to follow, like who can approve what. They aren't features on their own, but the requirements in section 4 make sure they're followed. Where a rule needs a number from KU, such as a money limit, we use a proposed value until the instructors confirm it (Appendix C).

### 5.5.1 Rules

<!-- widths: 900,8460 -->
| ID | Rule |
|---|---|
| BR-01 | Technical administration does not give business approval rights. A Business administrator authorises role assignments and a System administrator applies them; neither approves releases, transfers, spending or disposal unless the user also holds the business role for that department. |
| BR-02 | Nobody approves their own work. The requester or creator of a record cannot decide an approval task for that record. Where a department has only one representative, an alternate approver is named by the Business administrator (TBD-9). |
| BR-03 | A request becomes Open only after the requester's department representative approves it, because receiving an asset makes the department its owner and custodian. |
| BR-04 | A listing becomes visible to other departments only after the owning department's representative approves its release. |
| BR-05 | Every transfer needs two approvals: release by the releasing department's representative and receipt by the receiving department's representative. |
| BR-06 | A transfer also needs Finance officer approval when the asset's value is at or above the policy threshold (TBD-1), and Procurement officer approval when its category is procurement-controlled. |
| BR-07 | Maintenance and repair spending needs the owning department representative's approval, and Finance officer approval when the estimate is at or above the spending threshold (TBD-2). |
| BR-08 | End-of-life actions follow the reuse-first order: reuse or transfer, repair or refurbish, donate, disassemble for parts, recycle, and only then dispose. Choosing a later option requires a recorded reason why the earlier options are unsuitable. Every action needs Sustainability officer review and Finance officer write-off approval. |
| BR-09 | Assets in special-handling categories (for example electronics with batteries, laboratory equipment with contamination risk, and devices that store data) need a recorded EHS consultation, and data-storing devices need a data-erasure record, before donation, recycling or disposal (TBD-8). |
| BR-10 | A report or generated summary becomes official only after its data owner reviews it: the Finance officer for cost and savings figures, the Sustainability officer for sustainability figures and the Business administrator for operational figures. |
| BR-11 | Available, reserved and allocated quantities may never add up to more than the asset's total quantity, and the same unit may never be reserved or allocated twice. |
| BR-12 | A confirmed reservation is held for the hold period (TBD-3, proposed 5 working days). It expires unless a transfer has been approved by then. |
| BR-13 | Ownership, custody and location change only when the receiving custodian confirms receipt. Until then, the releasing department remains responsible for the asset. |
| BR-14 | Mandatory constraints (access rights, availability, quantity, required condition, technical compatibility and required date) are checked by classic rules before any AI ranking. An asset that fails a mandatory constraint is never shown as an actionable recommendation. |
| BR-15 | AI outputs are recommendations only. Selecting a match is not a reservation, a reservation is not an approval, and an action proposed by the assistant takes effect only after the user confirms it and every normal approval is given. When AI is unavailable, the classic functions are used. |
| BR-16 | An asset whose availability and condition were last verified more than the verification period ago (TBD-4, proposed 90 days) cannot have a reservation confirmed until the custodian verifies it again. |
| BR-17 | Audit entries are never changed or deleted. A mistake is corrected by a new entry that refers to the original. |
| BR-18 | A purchase counts as avoided only when an approved request is fulfilled with an existing asset and an authorised reviewer records that a new purchase would otherwise have been needed. Requests closed as No suitable item never count. |
| BR-19 | A listing cannot be withdrawn while an approved transfer for it is in progress. |
| BR-20 | Every rejection, request for changes and cancellation records a reason, and cancelling or rejecting a record releases any quantity it held. |

### 5.5.2 Approval Stages

Table 5.2 lists every approval in the system, in order. The approver must have the right role for that department, and BR-01 and BR-02 always apply. The states of an approval are in section 4.2.8.

**Table 5.2 Approval stages**

<!-- widths: 1700,2600,2600,2460 -->
| Workflow | Stages in order and approver | Result when all approve | Result of a rejection |
|---|---|---|---|
| Role assignment | 1. Authorise: Business administrator. 2. Apply: System administrator | Role active | Request closed with reason |
| Asset record | 1. Confirm: Asset custodian or department representative | AS-02 or AS-03 | Stays in Draft (AS-01) |
| Listing release | 1. Release: owning department representative | Published (LS-03) | Back to Draft (LS-01) |
| Resource request | 1. Department approval: requester's department representative | Open (RQ-03) | Rejected (RQ-08) |
| Reservation | 1. Confirm hold: releasing custodian or department representative | Confirmed (RV-02) | Declined (RV-03) |
| Transfer | 1. Release: releasing department representative. 2. Receipt: receiving department representative. 3. Policy, only under BR-06: Finance officer and/or Procurement officer. Then handover and receipt confirmations by the two custodians | Approved (TR-04), then Completed (TR-06) | Rejected (TR-08); held quantity released |
| Maintenance spending | 1. Department: owning department representative. 2. Finance, only at or above TBD-2: Finance officer | Approved (MW-04) | Rejected (MW-08) |
| End-of-life action | 1. Sustainability review: Sustainability officer, including the recorded EHS consultation under BR-09. 2. Write-off: Finance officer | Approved (EL-04), then Completed (EL-05) | Rejected (EL-06); asset returns to its previous state |
| Official report | 1. Review: the data owner under BR-10 | Marked Reviewed | Stays Draft with comments |
