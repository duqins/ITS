# 4. Integration Testing

Integration testing checks that modules work together through their interfaces. In Dawra Campus one user action passes through several modules: the address goes to a page, the page checks the role (accounts), reads the form, calls a business rule in a model (assets, requests or transfers), saves to the database, writes the audit log (audit) and tells other users (notifications). An integration test does one action and then checks every module it reached.

We integrated feature by feature, in the order of Phase 6: sign-in and roles first (C1), then assets and listings (C2, C3), requests (C4), holds and transfers (C5), history and audit (C6), the dashboard (C7), notifications (C8) and reports (C9). The tests of each feature were added with it and were run again after every later feature, so a new feature could not quietly break an old one.

## 4.1 Test Oracle

Table 4.1 shows one or two test cases for each interface. Most go through the pages with the test browser. IT-07, IT-08, IT-10, IT-11 and IT-13 call the services directly, to test the interface between two services.

**Table 4.1 Test oracle for the integration tests**

<!-- widths: 820,1780,2300,2100,1660,700 -->
| ID | Modules and requirement | Input | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|---|
| IT-01 | Sign-in page and accounts (FR-02.4) | 5 wrong passwords for Mariam on the sign-in page, then the right one | The page says the account is locked, and it is locked | "locked" shown; account locked | Pass |
| IT-02 | Page, role check and audit (FR-02.2, FR-02.3) | Aisha, a requester, sends a listing release decision | Refused by the server (403), and the refusal is in the audit log | 403; audit entry "blocked: listing.publish" | Pass |
| IT-03 | Asset pages and asset rules (BR-02, FR-04.3) | Khalid registers an asset and confirms it himself; then Mariam confirms it | Khalid's confirmation is refused and it stays Draft; after Mariam it is In storage | Draft; then In storage | Pass |
| IT-04 | Listing pages, approvals and search (BR-04, FR-06.2, FR-06.3) | Khalid offers the oscilloscope for release; Mariam approves | Pending release approval; then Published | LS-02; then LS-03 | Pass |
| IT-05 | Request form, requests and approvals (FR-07.3, FR-07.5) | Aisha submits "Monitor for a TA desk" | Pending department approval is shown, and the request is on her list | Shown on both pages | Pass |
| IT-06 | Approval page and requests (BR-02, FR-10.4) | Omar makes a request with his requester role, then tries to approve it as representative | Refused, with a message that he cannot approve his own request; it stays pending | RQ-02; message about his own request | Pass |
| IT-07 | Holds and asset quantities (FR-09.5, BR-11) | Two holds on the last projector; the custodian confirms both | The second confirmation is refused; 0 free and 1 reserved | BusinessRuleError; (0, 1) | Pass |
| IT-08 | Transfers and policy approvals (BR-06) | The oscilloscope, worth AED 7,500 and in a procurement-controlled category, after release and receipt approval | Pending policy approval, with a Finance stage and a Procurement stage | TR-03; stages transfer_finance and transfer_procurement | Pass |
| IT-09 | Handover, receipt and transfers (FR-11.5) | 4 chairs are handed over; Fatima receives 3 and marks it OK; then she records a discrepancy | The first is refused and it stays Handed over; with the discrepancy it is Disputed | TR-05; then TR-07 | Pass |
| IT-10 | Assets and audit log (FR-18.1, FR-18.2, BR-17) | The oscilloscope's history; then an attempt to change and to delete an audit entry | Registered by Khalid and confirmed by Mariam are logged; change and delete are refused | Both entries found; ValueError twice | Pass |
| IT-11 | Requests and notifications (FR-16.2) | Omar rejects the chairs request; the projector request is approved | Aisha gets a "rejected" and an "approved" notification | Both found | Pass |
| IT-12 | Reports and CSV export (FR-17.2, FR-17.3) | The business administrator exports the transfers report as CSV | The file names the report and the department filter, lists the transfer and gives the total | "Transfers", "All departments", the transfer code, "Total records 1" | Pass |
| IT-13 | Holds, expiry and requests (BR-12, FR-09.4) | A confirmed hold on the projector whose hold period has ended; the expiry job runs | Hold Expired, the request Open again, and the unit free | RV-05; RQ-03; 1 free | Pass |

## 4.2 All Integration and Feature Tests

The test cases in Table 4.1 are examples. Table 4.2 counts all the automated tests of each feature. They were written in Phase 6 with the feature and are run again here, together with the new Phase 7 tests.

**Table 4.2 Automated tests of each feature**

<!-- widths: 3900,3500,980,980 -->
| Feature | Test file in src/tests | Tests | Use pages |
|---|---|---|---|
| C1 Sign-in and roles | test_c1_login_roles.py | 7 | 6 |
| C2 and C3 Assets, listings and search | test_c2_c3_assets.py | 7 | 7 |
| C4 Requests | test_c4_requests.py | 4 | 4 |
| C5 Holds and transfers | test_c5_transfers.py | 6 | 6 |
| C6 History and audit log | test_c6_history.py | 5 | 2 |
| C7 Sustainability dashboard | test_c7_sustainability.py | 4 | 3 |
| C8 Notifications | test_c8_notifications.py | 6 | 3 |
| C9 Reports | test_c9_reports.py | 5 | 5 |
| AI classification, matching and report summary | test_ai.py | 12 | 9 |
| AI search | test_ai_search.py | 7 | 6 |
| Photos, documents, verification, approval stages and role administration | test_document_gaps.py | 26 | 25 |
| Edge cases of holds, listings and transfers | test_edge_cases.py | 11 | 3 |
| Faults found in the first demo walkthrough | test_demo_checks.py | 12 | 6 |
| Faults found in the second walkthrough and by reviewers | test_walkthrough_fixes.py | 21 | 17 |
| Demo history and savings graph | test_history_and_graph.py | 8 | 4 |
| Numbers at the top of the home page | test_home_glance.py | 6 | 6 |
| Arabic and English | test_language.py | 7 | 6 |
| Settings and theme | test_settings.py | 5 | 4 |
| **Total, Phase 6 tests** | **18 files** | **159** | **122** |

"Use pages" counts the tests that open at least one page with the test browser. The others call the models and services directly. A test also counts as using pages when its class signs the users in before each test, as in `test_c5_transfers.py`; this is why IT-07 and IT-08 are counted there.
