# 5. Other Nonfunctional Requirements

These requirements describe how well the system must work, including its speed, safety, security and ease of use. They retain the Phase 1 requirement IDs. The numerical values are acceptance targets, not results already achieved.

Unless a requirement states otherwise, testing shall use 500 synthetic assets across 10 departments, 50 requests and five concurrent users. We will record the hardware, operating system, browser, software versions and network conditions used so the tests can be repeated.

## 5.1 Performance Requirements

<!-- widths: 1100,6560,1700 -->
| ID | Requirement | Priority |
|---|---|---|
| NFR-02 | The system shall display classic search and filter results within 2 seconds for at least 95 of 100 measured searches under the stated test conditions. Time shall be measured from submitting the search until its results are displayed. AI processing time shall be measured separately. | Essential (Must) |
| NFR-11 | With 2,000 assets, 200 requests and five concurrent users, the system shall display classic search results within 3 seconds for at least 95 of 100 measured searches while preserving data integrity. This test shall be reported separately from NFR-02. | Desirable (Should) |

For each tested AI request, we will record the response time and whether the request succeeded, failed or timed out. The system shall provide the relevant classic alternative within the 15-second limit in NFR-07 and AI-13.2, including any retries.

Normal search performance and the first request after hosting inactivity shall be measured and reported separately, as agreed in Phase 2. Hosting startup time shall not be presented as AI processing time. The AI fallback test shall begin when the user submits an AI request through the running application. Any proposed change to the acceptance targets requires instructor agreement.

## 5.2 Safety Requirements

Incorrect records or recommendations could lead to unsafe equipment being transferred or an item being disposed of unnecessarily. The system shall apply the following safeguards:

- If an inspection record identifies an unresolved safety concern, then the system shall block handover until an authorised inspection records that the concern has been addressed for the proposed handling or use. Inspection evidence shall be kept with the asset's maintenance history under section 4.11.
- Before approving donation, recycling or disposal of an asset covered by BR-09, the system shall require the recorded EHS consultation and, for devices that store data, the required data-erasure record.
- When an end-of-life proposal selects a later option in the reuse-first order, the system shall require a recorded reason why the earlier options are unsuitable, as required by BR-08.
- The system shall keep the required human reviews and approvals in place even when an AI recommendation supports the action, following BR-15 and Table 5.2.
- In the agreed safety tests, the system shall block every attempt to bypass a required inspection, special-handling record, reuse-first justification or approval.

## 5.3 Security Requirements

<!-- widths: 1100,6560,1700 -->
| ID | Requirement | Priority |
|---|---|---|
| NFR-03 | The system shall check authentication, role and department permissions on the server for every protected action, including assistant actions. Locally managed passwords shall be stored only as salted hashes. Credentials shall remain outside version control, and browser traffic shall use HTTPS as specified in section 3.4. Every unauthorised action in the agreed role-and-permission test matrix shall be blocked. | Essential (Must) |
| NFR-04 | The system shall use synthetic records and test users for the prototype, following C-03 and DR-02. It shall block access to another department's restricted records in every agreed privacy test. AI input shall contain only the approved fields needed for the task. Credentials and unnecessary personal data shall be excluded from AI input content and ordinary logs. | Essential (Must) |
| NFR-05 | The system shall record an audit entry for every action listed in FR-18.1 that occurs in the acceptance tests, including controlled changes, approval decisions, role changes, refused actions and responses to AI outputs. Entries shall identify the actor, role, time, affected record, action, reason and relevant before-and-after values. The system shall reject every tested attempt to edit or delete an audit entry; corrections shall be new entries linked to the original, as required by BR-17. | Essential (Must) |

The role-and-permission test matrix shall cover all nine roles, allowed and refused actions, and access within and across departments. It shall also check that technical administration does not grant business approval rights and that users cannot approve their own work, as required by BR-01 and BR-02.

## 5.4 Software Quality Attributes

<!-- widths: 1000,1400,5360,1600 -->
| ID | Attribute | Requirement | Priority |
|---|---|---|---|
| NFR-01 | Usability | The system shall allow at least 4 of 5 representative test users to complete each of three tasks without help: register an asset, find a suitable listing and submit a request. Test users shall have the roles needed for their assigned tasks. Mean post-task satisfaction shall be at least 4 out of 5. | Essential (Must) |
| NFR-06 | Explainability | For all 20 sampled AI recommendations, the system shall show the main reasons, relevant inputs, supporting records and confidence information or its unavailability. It shall distinguish estimates and assumptions from recorded facts, following sections 4.18 and 4.22. | Essential (Must) |
| NFR-07 | Reliability and fallback | In all five planned AI failure tests, the system shall explain the failure and make the relevant classic alternative available within 15 seconds of the original request. The tests shall cover unavailable service, timeout, rate limit, malformed output and insufficient confidence. Every case shall preserve user input and allow the classic workflow to continue with its normal access and approval checks. | Essential (Must) |
| NFR-08 | Maintainability | The system shall separate asset management, workflows, reporting and AI integration into identifiable modules. Project documentation shall explain their responsibilities and interfaces and provide a repeatable command for testing critical business rules. | Essential (Must) |
| NFR-09 | Portability | The system shall run from a fresh repository copy using the documented prerequisites, setup commands, configuration examples and synthetic seed data. One teammate shall complete a fresh setup using those instructions and complete classic search and request workflows without a paid AI account or AI API key. | Essential (Must) |
| NFR-10 | Data integrity | The system shall validate quantities, record references and allowed state changes before saving them. Related stock changes shall succeed together or leave the records unchanged. The agreed tests shall produce zero negative quantities, duplicate allocations or invalid state changes. In 10 tests where two users simultaneously attempt to hold the same final unit, exactly one hold shall be confirmed each time. | Essential (Must) |
| NFR-12 | Fairness and ethics | The system shall exclude protected personal characteristics from matching factors and document any department-based policy priorities. In all 10 paired tests that change only personal names or department labels, eligibility and relative ranking shall remain unchanged when permissions, policy priority, asset needs and other relevant factors stay equal. | Essential (Must) |
| NFR-13 | Deployment | The system shall support deployment to the selected hosting environment through documented setup, configuration and restart steps, with a documented HTTPS address. One teammate shall complete a fresh deployment and pass the hosted registration, search, request, approval and AI-fallback checks. Restart testing shall confirm that records, uploaded files and access controls are preserved. | Desirable (Should) |

For each requirement, the test record shall identify the requirement ID, test conditions, expected result, actual result and supporting evidence. Unmet targets shall be reported clearly rather than described as completed.