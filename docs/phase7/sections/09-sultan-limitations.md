# 9. What Was Not Tested and Limitations

## 9.1 Summary of the Results

All 191 automated tests pass. The AI classification evaluation reached 20 of 20 on our set (target 16), all 10 sustainability cases agree with the hand calculation, and the acceptance test met NFR-01. The rest of this section says what these results do not cover.

## 9.2 Features Not Built, So Not Tested

These features are in our SRS but were not built in Phase 6, so they have no test cases:

- maintenance and repair tracking, with inspections and work orders (FR-12, FR-13), and so the repair success rate (SU-09) and asset-life extension (SU-06);
- end-of-life review: donation, recycling, disassembly and disposal (FR-14);
- sustainable-action advice from the AI (AI-06);
- the campus assistant (AI-07, AI-08).

## 9.3 Targets We Set but Did Not Test

Our SRS and our Phase 1 success criteria set targets for some checks that we did not carry out. We list them so that no result in this document is read as covering them.

**Table 9.1 Targets that were not tested**

<!-- widths: 3000,1700,4660 -->
| Target | Requirement | What we have instead |
|---|---|---|
| At least 16 of 20 labelled requests have a useful match in the top three, and 2 more than classic search | AI-02.2, AI-02.3 | Not run. The match score and its rules are tested with a stand-in (UT-11 to UT-13, AT-04), but not whether the matches are useful. |
| No ineligible item among the matches of the 20 requests | AI-03.4 | Not run as a set. The rule that a hold needs the right category, condition and date is tested in `test_walkthrough_fixes`. |
| 20 sampled recommendations show reasons and confidence | AI-05.3 | Not run as a review. AT-04 checks that each match has a reason and a stored confidence. |
| Every claim is traceable in 5 generated summaries | AI-10.3 | Not run with the real AI. The figures check is tested (UT-14, AT-07). |
| 14 approval tests, one allowed and one refused path for 7 kinds of action | AI-11.3 | Only transfers (ST-02, IT-06, IT-08) and role changes (`test_document_gaps`) exist. Donation, recycling, disposal and repair spending are not built. |
| 95 of 100 classic searches within 2 seconds with 500 assets and 5 users at once | NFR-02 | Not measured. |
| 95 of 100 classic searches within 3 seconds with 2,000 assets, 200 requests and 5 users at once | NFR-11 | Not measured. |
| 95 of 100 AI matching requests within 5 seconds | NFR-16 | Not measured. The classification run in section 6.2 took at most 2.6 seconds per item, for one user. |
| The classic way within 15 seconds when the AI is slow | NFR-07 | The logic is tested with a stand-in that fails at once (Table 6.2). A real slow connection was not measured. |
| 10 pairs where only names or departments change keep the same ranking | NFR-12 | Not run. AT-09 checks that 5 names of people, the label "Department:" and one building name are not sent to the AI search. |
| In 10 two-user attempts to hold the last unit at the same moment, exactly one succeeds | NFR-10, FR-09.5 | Tested one after the other (IT-07), not at the same moment. |
| 5 of 10 scripted purchase needs end in a confirmed avoided purchase | SU-03, SU-04 | Not run as 10 scripts. SV-02 and SV-05 check the avoided purchases that exist. |
| At least 5 of a fixed cohort of 10 assets return to use, a reuse rate of at least 50% | SU-05 (Phase 1 target) | Not run. The reuse rate is calculated correctly (SV-08), but in the demo period it is 16.7%, or 25.0% after one more transfer. |
| Keyboard-only use and WCAG 2.2 AA contrast on the registration, request and approval screens | NFR-15 | Not tested. |
| A teammate sets up the system from a fresh copy using only the README | NFR-09 | Not recorded in Phase 7. The automated tests need no AI key. |
| A fresh deployment by a teammate, and 95% of hourly availability checks in the last two weeks | NFR-13, NFR-14 | The system is deployed and was used for the Phase 6 demonstration, but the deployment steps and the availability checks were not recorded as tests. |
| Every Must-have requirement is mapped to at least one test | Phase 1 success criteria | Not done in full. The tables in this document name the requirements each test checks, but some Must-have requirements, such as the features in 9.2, have no test. |

## 9.4 Limitations of the Test Data

- **Synthetic and small.** All tests use our made-up demo data: 8 departments, 12 users and, with the history, 22 assets, 15 requests and 11 transfers. Our Phase 1 plan asked for 500 assets in 10 departments and 50 requests. Only Engineering and Computing exchange items, and only monitors have a cited price, so all money figures come from monitors. The transfer costs of items without a price are left out of the net savings (section 7.1).
- **We wrote both the code and the tests.** The expected results come from our own requirements and design, so a mistake in those documents would be in the test too. The acceptance test is the only test by people outside the team.
- **The AI is a stand-in in the automated tests.** Those tests check our code, not the AI. The real AI was only used for the 20 classification items, once, with one model and one prompt version, on items we wrote and labelled ourselves after the system was built.
- **The test browser does not run JavaScript or show the page.** The automated tests read the pages the server sends. The confirm dialogs, the busy state of buttons, the layout on a phone and the dark theme were only checked in a real browser during Phase 6, and those checks are not part of this test set.
- **One database.** The automated tests run on SQLite. The live site uses PostgreSQL, where the demo data was loaded several times without errors, but the test set was not run there.
- **Coverage.** 91% of the statements and 76% of the branches ran (section 3.3). The rest has no test, and coverage does not show that a result is right.

Because of these limits, the results in this document show that the prototype works as designed on our demo data. They do not show how accurate the AI is in general, how fast the system is with many users, or how much the campus would really save.
