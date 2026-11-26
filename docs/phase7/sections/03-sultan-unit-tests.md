# 3. Unit Testing

Unit testing checks one function or class on its own. The lab slides split it into static analysis, where the code is not run, and dynamic analysis, where it is run with chosen inputs.

## 3.1 Static Analysis

**Code inspection.** All code reached the main branch through a pull request on GitHub, and the repository only allows a merge after another member approves it. In Phase 6 this was 12 pull requests (#26 to #37). The reviewer reads the changed lines before approving, and a fault found this way is fixed on the same branch before the merge. For example, the review of pull request #30 found that one commit with style fixes was missing, and it was added before the pull request was merged.

**Hand execution.** The expected result of every test case in this document was worked out by hand from the requirements and the design document, not copied from the output of the program. For the sustainability cases in section 7 the working is written next to each test as a comment, so it can be checked line by line. We also traced some functions by hand before running them. For example, `add_working_days` for Friday 20 Nov plus 1 working day: the loop moves to Saturday (weekend, not counted), then Sunday (not counted), then Monday 23 Nov (counted, 1 of 1), and stops. Monday 23 Nov is the expected result of UT-10.

**Automatic checks.** Django runs its system check before every test run. It checks the models, the addresses and the settings, and reported no issues in the final run.

## 3.2 Black-Box Unit Tests

For each unit we listed the equivalence classes of its input: groups of values that the requirement treats the same way. We tested one value from each class and the values on the boundary between two classes. These tests call the function or class directly, with no page, and are in `src/tests/test_units.py`.

**Table 3.1 Test oracle for the unit tests**

<!-- widths: 820,2000,2150,2050,1640,700 -->
| ID | Unit and requirement | Input | Expected result | Actual result | Pass/Fail |
|---|---|---|---|---|---|
| UT-01 | `User.sign_in` (FR-02.4) | The right password; then 1 to 4 wrong passwords; then a 5th wrong one; then the right password again | Signed in; not locked after 1 to 4; locked after the 5th; the right password is refused while locked | Signed in; not locked after 1 to 4; locked after the 5th; refused while locked | Pass |
| UT-02 | `Role.allows` (FR-02.2, BR-01) | Requester: submit request, view report. System administrator: apply role, authorise role. An action that does not exist | Allowed, refused, allowed, refused, refused | Allowed, refused, allowed, refused, refused | Pass |
| UT-03 | `Asset.reserve` (BR-11, FR-09.2) | Ergonomic chairs, 6 free. Reserve 4, then 2, then 1 more | 2 free and 4 reserved; then 0 free and 6 reserved (boundary); then refused with nothing changed | (2, 4); then (0, 6); then BusinessRuleError and (0, 6) kept | Pass |
| UT-04 | Database rule on the asset table (BR-11, FR-05.3) | Set the reserved quantity to the total quantity plus 1, directly in the database | The database refuses the change | IntegrityError; reserved quantity still 0 | Pass |
| UT-05 | `change_state` (FR-05.2 refusal, asset state diagram) | Asset In storage. Move to Donated; move to In storage; move to In service | First two refused; the third is allowed, keeps the previous state and adds one audit entry | Refused, refused; In service, previous state In storage, audit entries plus 1 | Pass |
| UT-06 | `Asset.missing_for_confirmation` (FR-04.2) | Every field filled; category empty; category, room and value empty | No missing fields; "Category"; 3 missing fields | [ ]; ["Category"]; 3 fields | Pass |
| UT-07 | `ClassificationService.can_prefill` (AI-05.4, threshold 0.60) | Confidence none, 0.333, 0.599, 0.600, 0.667, 1.000 | Not filled in for the first three; filled in from 0.600 (boundary) | No, no, no, yes, yes, yes | Pass |
| UT-08 | `confidence_label` (AI-05.4, thresholds 0.50 and 0.75) | None, 0.49, 0.50, 0.74, 0.75, 0.90 | Unavailable; withheld; check carefully at 0.50 and 0.74; shown as a number from 0.75 | Unavailable; Withheld; check carefully twice; "Confidence 0.75", "Confidence 0.90" | Pass |
| UT-09 | `Transfer.needs_finance` (BR-06, AED 5,000) | AED 4,999.99 x 1; AED 5,000 x 1; AED 2,700 x 2; no value x 3 | No; yes (boundary); yes, because the total is 5,400; no | No, yes, yes, no | Pass |
| UT-10 | `add_working_days` (BR-12, 5 working days) | Mon 23 Nov + 0; Mon 23 Nov + 4; Fri 20 Nov + 1; Mon 23 Nov + 5 | Mon 23 Nov; Fri 27 Nov; Mon 23 Nov, skipping the weekend; Mon 30 Nov | Mon 23, Fri 27, Mon 23, Mon 30 Nov | Pass |
| UT-11 | Match score, meaning factor (AI-05.1) | AI similarity 0.0, 0.5 and 1.0 | 0, 15 and 30 points of 30 | 0, 15, 30 | Pass |
| UT-12 | Match score, condition factor (AI-05.1) | Item in fair condition. Minimum asked: fair, poor, not working | 5, 10 and 15 points: more points when the item is above the minimum | 5, 10, 15 | Pass |
| UT-13 | Match score total (AI-05.1) | Similarity 0.0, 0.37 and 1.0 | Total equals the sum of the factor points, the maximum points add up to 100, and the total is from 0 to 100 | Equal every time; maximum 100; within 0 to 100 | Pass |
| UT-14 | Figures check of the AI report summary (AI-10.1, AI-09.2) | Text using only the report figures; "AED 9,999"; "22 items"; "twenty items"; "in 2025" | Nothing flagged for the first; each of the other four numbers is flagged | [ ]; ["9,999"]; ["22"]; ["twenty"]; ["2025"] | Pass |

The other tests that call code directly, without a page, came from Phase 6. Examples are the audit entry that cannot be changed or deleted (`test_c6_history`) and the check for numbers in the AI summary (`test_ai`). Section 4 counts them with the integration tests of their feature, and Appendix A lists every test.

## 3.3 White-Box Testing: Coverage

We measured statement and branch coverage with coverage.py 7.17.5 while the whole automated set ran (191 tests). Statement coverage counts the lines that ran at least once. Branch coverage counts, for each `if` or loop, whether both the true and the false way were taken. We measured the code of the ten apps of the system. Migration files (Django writes them), the settings package and the tests themselves are left out.

**Table 3.2 Coverage of the application code (26 Nov 2026)**

<!-- widths: 3360,2000,2000,2000 -->
| Measure | Covered | Total | Coverage |
|---|---|---|---|
| Statements | 3,696 | 4,059 | 91% |
| Branches | 694 | 918 | 76% |
| Statements and branches together | | | 88% |

The parts with the lowest coverage, and why:

- `ai/management/commands/evaluate_classification.py` (0%). It calls the real AI service, so it is run by hand for the evaluation in section 6.2 and not by the automated tests.
- `transfers/management/commands/expire_overdue.py` (0%). This is only the command that the server runs on a schedule. The function it calls is tested in `test_edge_cases` (overdue holds expire and free the units).
- `resource_requests/views.py` (66%). Editing a saved request draft, submitting a saved draft later, and closing a request as No suitable item are not tested through the pages.
- `notifications/views.py` (74%), `audit/admin.py` (75%), `resource_requests/models.py` (78%) and `transfers/views.py` (79%). Some refusal branches, such as opening a notification that does not exist, are not tested.

Coverage shows which lines the tests ran. It does not show that the results were right; the checks inside each test do that. We did not measure loop or path coverage. One loop was tested on purpose: in UT-10 the loop in `add_working_days` runs zero times (Monday plus 0) and several times (3, 4 and 7 times for the other three inputs). The full coverage report is saved in `docs/phase7/results/coverage_report.txt`.
