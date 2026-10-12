## 4.2 Record States

The project description asks for the states of assets, requests, transfers and maintenance. These tables list every state, what it means and what can come next. A record is always in exactly one state. If someone tries a change that isn't in the "Next states" column, the system blocks it and logs the attempt (FR-05.2). The state names are the labels users see on screen, and we will turn these tables into UML state diagrams in Phase 5.

### 4.2.1 Asset Life-Cycle States

How many units are available, reserved or allocated is tracked separately from the state (FR-05.3). That way a batch of chairs can be in service while some of them are listed for reuse.

<!-- widths: 800,1800,4060,2700 -->
| ID | State | Meaning | Next states |
|---|---|---|---|
| AS-01 | Draft | Record being entered; not yet confirmed | AS-02, AS-03 (on confirmation) |
| AS-02 | In service | In use by the owning department | AS-03, AS-04, AS-05, AS-06 |
| AS-03 | In storage | Not in use; may be listed for reuse | AS-02, AS-04, AS-05, AS-06 |
| AS-04 | Under maintenance | An approved work order is open | AS-02, AS-03, AS-06 (not repairable) |
| AS-05 | In transfer | Handed over by the releasing custodian, awaiting receipt | AS-02 or AS-03 under the new owner (receipt confirmed); previous state (transfer cancelled or dispute resolved) |
| AS-06 | Retired | Out of service; an end-of-life action is proposed or under review | AS-02, AS-03 (action rejected), AS-07, AS-08, AS-09, AS-10 |
| AS-07 | Donated | Given to an approved recipient | None (final) |
| AS-08 | Recycled | Sent to an approved recycler | None (final) |
| AS-09 | Disassembled | Taken apart; usable parts registered as new assets | None (final) |
| AS-10 | Disposed | Disposed of as the last option | None (final) |

### 4.2.2 Listing States

<!-- widths: 800,2200,4060,2300 -->
| ID | State | Meaning | Next states |
|---|---|---|---|
| LS-01 | Draft | Listing being prepared by the custodian or department representative | LS-02, deleted |
| LS-02 | Pending release approval | Waiting for the releasing department representative (BR-04) | LS-03, LS-01 (changes requested), LS-05 |
| LS-03 | Published | Visible to authorised staff; quantity can be reserved | LS-04, LS-05, LS-06 |
| LS-04 | Fully reserved | All offered quantity is held by reservations | LS-03 (a reservation ends), LS-06 |
| LS-05 | Withdrawn | Removed by the owning department (not allowed during an approved transfer, BR-19) | LS-01 |
| LS-06 | Closed | All offered quantity has been transferred | None (final) |

### 4.2.3 Request States

<!-- widths: 800,2300,4060,2200 -->
| ID | State | Meaning | Next states |
|---|---|---|---|
| RQ-01 | Draft | Being written by the requester or drafted by the assistant | RQ-02, deleted |
| RQ-02 | Pending department approval | Waiting for the requester's department representative (BR-03) | RQ-03, RQ-01 (changes requested), RQ-08 |
| RQ-03 | Open | Approved; the requester searches and reviews matches | RQ-04, RQ-07, RQ-09, RQ-10, RQ-02 (changed after approval) |
| RQ-04 | Reservation requested | A listing has been selected and a reservation requested | RQ-05, RQ-03 (reservation declined or expired), RQ-09 |
| RQ-05 | In transfer | A transfer for the request is being approved or carried out | RQ-06, RQ-03 (transfer rejected or cancelled) |
| RQ-06 | Fulfilled | The requested quantity has been received | None (final) |
| RQ-07 | No suitable item | Closed because no eligible asset exists; the requester may follow the normal purchasing process outside the system | None (final) |
| RQ-08 | Rejected | Refused by the department representative, with a reason | None (final) |
| RQ-09 | Cancelled | Withdrawn by the requester | None (final) |
| RQ-10 | Expired | The required-by date passed before fulfilment | None (final) |

### 4.2.4 Reservation States

<!-- widths: 800,2200,4060,2300 -->
| ID | State | Meaning | Next states |
|---|---|---|---|
| RV-01 | Requested | The requester asked to hold a quantity | RV-02, RV-03, RV-06 |
| RV-02 | Confirmed | The releasing custodian or representative holds the quantity until the hold period ends (BR-12) | RV-04, RV-05, RV-06 |
| RV-03 | Declined | The releasing side refused, with a reason | None (final) |
| RV-04 | Converted to transfer | A transfer record was created from the reservation | None (final) |
| RV-05 | Expired | The hold period ended without a transfer | None (final) |
| RV-06 | Cancelled | The requester or the releasing side cancelled it | None (final) |

### 4.2.5 Transfer States

<!-- widths: 800,2300,4060,2200 -->
| ID | State | Meaning | Next states |
|---|---|---|---|
| TR-01 | Pending release approval | Waiting for the releasing department representative (BR-05) | TR-02, TR-08, TR-09 |
| TR-02 | Pending receipt approval | Waiting for the receiving department representative (BR-05) | TR-03, TR-04, TR-08, TR-09 |
| TR-03 | Pending policy approval | Waiting for the Finance and/or Procurement officer, only when BR-06 applies | TR-04, TR-08, TR-09 |
| TR-04 | Approved | All approvals given; collection or delivery is being arranged | TR-05, TR-09 |
| TR-05 | Handed over | The releasing custodian confirmed handover, quantity and condition | TR-06, TR-07 |
| TR-06 | Completed | The receiving custodian confirmed receipt; ownership, custody and location updated (BR-13) | None (final) |
| TR-07 | Disputed | The receiving custodian recorded a quantity or condition difference | TR-06 (resolved and received), TR-09 (returned) |
| TR-08 | Rejected | An approver refused the transfer, with a reason | None (final) |
| TR-09 | Cancelled | Cancelled before completion; the held quantity returns to the listing | None (final) |

### 4.2.6 Maintenance Work Order States

<!-- widths: 800,2300,4060,2200 -->
| ID | State | Meaning | Next states |
|---|---|---|---|
| MW-01 | Reported | A defect or inspection request was reported | MW-02, MW-09 |
| MW-02 | Under assessment | Maintenance staff inspect the asset and estimate the cost | MW-03, MW-07, MW-09 |
| MW-03 | Awaiting cost approval | Waiting for approval of the estimate (BR-07) | MW-04, MW-08 |
| MW-04 | Approved | Spending approved; work can start | MW-05, MW-09 |
| MW-05 | In progress | Repair or refurbishment under way | MW-06, MW-07, MW-03 (cost exceeds the approved amount) |
| MW-06 | Completed | Work, actual cost, outcome and new condition recorded; the asset returns to service or storage | None (final) |
| MW-07 | Not repairable | Repair is impossible or uneconomic; an end-of-life review starts (EL-01) | None (final) |
| MW-08 | Rejected | Spending was not approved, with a reason | None (final) |
| MW-09 | Cancelled | The work order was withdrawn | None (final) |

### 4.2.7 End-of-Life Action States

<!-- widths: 800,2300,4060,2200 -->
| ID | State | Meaning | Next states |
|---|---|---|---|
| EL-01 | Proposed | Action (retain, donate, disassemble, recycle or dispose), reason and evidence entered; an AI recommendation may be attached | EL-02 |
| EL-02 | Under sustainability review | The Sustainability officer checks the action against the reuse-first order (BR-08) and any EHS rules (BR-09) | EL-03, EL-06, EL-01 (changes requested) |
| EL-03 | Awaiting finance approval | The Finance officer approves the write-off | EL-04, EL-06 |
| EL-04 | Approved | The action may be carried out | EL-05 |
| EL-05 | Completed | Date, recipient or destination, quantity and evidence recorded; the asset enters its final state | None (final) |
| EL-06 | Rejected | The asset returns to its previous state | None (final) |

### 4.2.8 Approval Task States

<!-- widths: 800,2200,4060,2300 -->
| ID | State | Meaning | Next states |
|---|---|---|---|
| AT-01 | Pending | Assigned to the users who hold the required role | AT-02, AT-03, AT-04, AT-05 |
| AT-02 | Approved | Decision recorded with user, role and time | None (final) |
| AT-03 | Rejected | Decision recorded with a mandatory reason | None (final) |
| AT-04 | Changes requested | Returned to the submitter with a reason | None (final; a new task is created on resubmission) |
| AT-05 | Withdrawn | The parent record was cancelled before a decision | None (final) |
