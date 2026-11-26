# 5. System Testing

System testing checks the whole system against its requirements. Each system test is one complete workflow from the first page to the last, done by several demo users who each sign in with their own role, the same way people would use it. Every step goes through the real pages; no step is made to happen by calling the code behind a page. The AI is a stand-in (ST-03) or switched off (ST-04), so the tests need no key and no internet. The tests are in `src/tests/test_system_workflows.py`.

The demo users are the same as in Phase 6: Khalid (asset custodian, Engineering), Mariam (department representative, Engineering), Aisha (requester, Computing), Omar (department representative, Computing), Fatima (asset custodian, Computing) and Salem (sustainability officer).

## 5.1 Test Oracle

**Table 5.1 Test oracle for the system tests**

<!-- widths: 820,1500,2550,2250,1540,700 -->
| ID | Workflow (requirements) | Steps and input | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|---|
| ST-01 | From registration to search (FR-04.1, FR-04.3, BR-02, BR-04, FR-06.2, FR-06.3, FR-08.4, FR-16.1) | 1. Khalid registers "BenQ 24-inch monitor" with all fields.<br>2. Khalid tries to confirm it himself.<br>3. Mariam confirms it.<br>4. Aisha searches "BenQ".<br>5. Khalid offers 2 units for release.<br>6. Mariam approves the release.<br>7. Aisha searches again | 1. Draft, Engineering, custodian Khalid, logged.<br>2. Refused with BR-02 and logged.<br>3. In storage, verified by Mariam.<br>4. Not found.<br>5. Pending release approval, a task for Mariam, and she is told.<br>6. Published; Khalid is told.<br>7. Found | Every step as expected: AS-01, refused and logged, AS-03, not found, LS-02 with task AT-01, LS-03, found | Pass |
| ST-02 | From request to a completed transfer (FR-07.3, BR-03, FR-09.1, FR-09.3, FR-11.1 to FR-11.4, BR-05, BR-13, FR-15.1, FR-16.2) | 1. Aisha requests 2 monitors.<br>2. Omar approves.<br>3. Aisha asks for a hold on 2 Dell monitors.<br>4. Khalid confirms the hold.<br>5. Aisha starts the transfer (10 km, 1 van trip, AED 40).<br>6. Mariam approves the release.<br>7. Omar approves the receipt.<br>8. Khalid hands over.<br>9. Fatima confirms receipt of 2 | 1. Pending department approval; Omar is told.<br>2. Open; Aisha is told.<br>3. Reservation requested; nothing held yet.<br>4. Hold confirmed: 0 free, 2 reserved.<br>5. Pending release approval; the request is In transfer; 2 allocated.<br>6. Pending receipt approval.<br>7. Approved (AED 690 is below AED 5,000, so no Finance stage).<br>8. Handed over, still owned by Engineering.<br>9. Completed and the request Fulfilled; owner Computing, custodian Fatima; one sustainability record; the history shows every step; Aisha is told | Every step as expected: RQ-02, RQ-03, RV-01 with 2 free, RV-02 with (0, 2), TR-01 and RQ-05 with 2 allocated, TR-02, TR-04, TR-05 Engineering, TR-06 and RQ-06, Computing, Fatima, 1 record | Pass |
| ST-03 | AI-assisted path with a person deciding each time (AI-01.4, AI-05.1, BR-15, AI-10.2, BR-10) | 1. Khalid registers a monitor without a category and presses Classify.<br>2. Khalid accepts the suggestion.<br>3. Aisha asks for AI matches for the projector request and chooses the top one.<br>4. Salem drafts the report summary and tries to publish it with "AED 9,999" added.<br>5. Salem publishes it without that number | 1. A suggestion with confidence 1.00 is saved; the asset is not changed.<br>2. Category Monitor, condition good.<br>3. Score equals the factor total; the request is only Reservation requested and nothing is held.<br>4. Refused, naming 9,999.<br>5. Published and shown on the dashboard | Every step as expected: 3 AI calls, asset unchanged, then Monitor; RQ-04 and RV-01 with 1 free and 0 reserved; refused; accepted and shown | Pass |
| ST-04 | Everything still works without the AI (AI-13.4, FR-08.6, NFR-07) | No API key.<br>1. Khalid registers a projector and presses Classify.<br>2. He chooses the category by hand; Mariam confirms; the item is released.<br>3. Aisha opens AI matches and AI search.<br>4. Aisha asks for a hold from the item's own page | 1. The page says to choose the category yourself; no AI record.<br>2. Published and found by the normal search.<br>3. Classic order with no scores; AI search says it is not available and points to the normal way.<br>4. Reservation requested | Every step as expected: no AI record, LS-03, found, classic order, messages shown, RQ-04 and RV-01 | Pass |
| ST-05 | Each role reaches only its own pages (FR-02.2, FR-02.3, FR-18.1) | Each of the 12 demo users signs in and opens the 10 main pages: 120 page visits | The pages of Table 5.2 open (200): 69 visits. Every other page is refused (403): 51 visits. Each refusal is written to the audit log | 69 opened, 51 refused, 51 refusals in the audit log | Pass |

## 5.2 Expected Access for Each Role

Table 5.2 is the expected result of ST-05. We worked it out by hand from the permission matrix in SRS section 2.3.1 and the access matrix in Table 6.2 of our design. Home is open to every signed-in user. Adding up the table gives 69 pages that open and 51 that are refused, and ST-05 checks both numbers.

**Table 5.2 Main pages each demo user can open**

<!-- widths: 2900,900,5560 -->
| Demo user and role | Pages | Which pages |
|---|---|---|
| Latifa and Khalfan, Business administrators | 8 | Home, Assets, Search, Transfers, Dashboard, Reports, Audit log, Administration |
| Omar and Mariam, Department representatives | 8 | Home, Assets, Search, Requests, Approvals, Transfers, Dashboard, Reports |
| Hamad, Finance officer, and Noura, Procurement officer | 7 | Home, Assets, Search, Approvals, Transfers, Dashboard, Reports |
| Salem, Sustainability officer | 5 | Home, Assets, Search, Dashboard, Reports |
| Fatima and Khalid, Asset custodians | 4 | Home, Assets, Search, Transfers |
| Aisha, Requester | 4 | Home, Search, Requests, Transfers |
| Yousef, Maintenance staff | 3 | Home, Assets, Search |
| Reem, System administrator | 3 | Home, Search, Administration |
