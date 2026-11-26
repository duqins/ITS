# 8. User-Acceptance Testing

The lab slides say acceptance testing is done by the client or the users, to decide whether the system is ready for them. Our acceptance criterion is requirement NFR-01 from Phase 3: at least 4 of 5 representative test users complete each of three tasks without help (register an asset, find a suitable listing and submit a request), and the mean post-task satisfaction is at least 4 out of 5.

## 8.1 How the Test Was Run

We used one task sheet for every test user. Each person did the three tasks below on one laptop with the demo data, in windows where Khalid (asset custodian) and Aisha (requester) were already signed in, so nobody typed a password. We told each person that the data is made up, that we were testing the app and not them, and that they could stop at any time. We did not help unless a person was stuck for about two minutes, and any help was recorded. After each task the person rated how easy it was from 1 (very hard) to 5 (very easy), and at the end they rated their overall satisfaction from 1 to 5. We wrote P1, P2 and so on instead of names.

The test was run on 26 Nov 2026 with five classmates who are not in our group (P1 to P5). Each of them agreed to take part before starting. For task 2, all five used the normal search.

## 8.2 Test Oracle

**Table 8.1 Test oracle for the acceptance test**

<!-- widths: 820,1650,2600,2100,1490,700 -->
| ID | Task (requirement) | Input given to the test user | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|---|
| UA-01 | Register an asset, as Khalid (NFR-01, FR-04.1) | "Your department has a spare office chair that nobody uses. Add it to the system so it can be reused." A mesh chair with armrests, good condition, Engineering Building room E2-114, bought in September 2023, worth about 450 dirhams | The asset is saved and shown as a Draft. At least 4 of 5 users do it without help | 5 of 5 finished without help. Ease: 5, 5, 5, 5, 5 (mean 5.0) | Pass |
| UA-02 | Find a suitable listing, as Aisha (NFR-01, FR-08.1) | "Your lab needs something to show slides in a small seminar room. Find an item on the system that you could use, and open its page." | The user opens the page of a published projector, with the normal search or Search with AI. At least 4 of 5 users do it without help | 5 of 5 finished without help. Ease: 5, 5, 5, 5, 5 (mean 5.0); all used the normal search | Pass |
| UA-03 | Submit a request, as Aisha (NFR-01, FR-07.1) | "Your tutorial room needs two monitors within the next three weeks. Ask for them through the system." | The request is sent and shows Pending department approval. At least 4 of 5 users do it without help | 5 of 5 finished without help. Ease: 5, 5, 5, 5, 5 (mean 5.0) | Pass |
| UA-04 | Satisfaction (NFR-01) | "Overall, from 1 to 5, how satisfied are you with the app?" | Mean of at least 4 out of 5 | 5, 5, 5, 5, 5 (mean 5.0) | Pass |

## 8.3 Result

Requirement NFR-01 is met. Each of the three tasks was finished without help by 5 of the 5 test users, where the target is at least 4 of 5, and the mean satisfaction was 5.0, where the target is at least 4. The mean of the ease rating after each task was also 5.0, so the target is met whichever of the two ratings is used. Nobody needed help, so the test did not show a step that people found hard.

Every rating was 5, so the ratings cannot tell the tasks apart. Nobody tried Search with AI in task 2, so this test says nothing about how easy the AI search is to use.

This test gives feedback on the prototype from a small group of five students. It does not show that the whole campus would accept the system, because the test users were not the real asset custodians and requesters of the university.
