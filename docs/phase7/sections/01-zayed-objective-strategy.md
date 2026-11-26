# 1. Test Objective

This document gives the test cases for Dawra Campus, the system we built in Phase 6. It follows the three steps of the Phase 7 lab slides: the test objective, the test strategies and the test oracle. Every test case in the oracle has an input, an expected result, an actual result and a pass or fail.

Our objective is to show that the system does what our Phase 3 requirements say, for both the classic functions and the AI functions, and to find faults before the final submission. In detail, the tests check that:

- each function and class gives the right output for each kind of input (unit testing);
- the modules work together through the pages: the role check, the form, the business rule, the database, the audit log and the notification (integration testing);
- a whole workflow runs from the first page to the last across several users (system testing);
- the AI classification gives the right category on a fixed labelled set, and the sustainability numbers equal the numbers we work out by hand;
- test users can do the main tasks of the system (user-acceptance testing).

**What is tested.** The nine core features of the Phase 6 lab slides (C1 to C9), AI classification, AI matching, the AI report summary, and AI search. The version tested is the main branch of our GitHub repository after Phase 6.

**What is not tested.** Maintenance and repair tracking, the end-of-life review, sustainable-action advice and the campus assistant are in our requirements but are not built yet, so they have no test cases. Section 9 lists them.

**Where the expected results come from.** Each expected result comes from a document we wrote before the test: a requirement in the SRS (FR, AI, SU or NFR), a business rule (BR-01 to BR-20), a state diagram or a formula in the design document, or a target in our Phase 1 success criteria. The test case names the ID it checks.

**Test environment.** The tests run on a laptop copy of the system with Python 3.13 and Django 5.2. Each run creates a new test database and fills it with our synthetic demo data, so every run starts from the same state. The automated tests replace the AI service with a stand-in that returns fixed answers, so they need no key and give the same result every time. Only the AI classification evaluation in section 6.2 calls the real AI service. The whole automated set is run with one command, `python manage.py test`, from the `src` folder of the repository.

# 2. Test Strategy

We use the four kinds of testing from the lab slides, in the same order: unit, integration, system and acceptance. The project description also asks for an AI classification evaluation and a sustainability-calculation validation, so each of these has its own section.

**Table 2.1 Test strategy for each kind of testing**

<!-- widths: 1500,2500,3260,1200,900 -->
| Kind of testing | What it checks | How we do it | Carried out by | Section |
|---|---|---|---|---|
| Unit | One function or class on its own | Static analysis: every change is read by a teammate in a pull request before it is merged. Dynamic analysis: black-box tests with equivalence classes and boundary values, and white-box measurement of statement and branch coverage | Developers | 3 |
| Integration | Groups of modules and the interfaces between them | Automated tests that go through the real pages with a test browser, so the address, the role check, the form, the model, the database, the audit log and the notifications are used together | Developers | 4 |
| System | The entire system against the requirements | Whole workflows from start to finish across several signed-in users, and a check of every main page for every role | Developers | 5 |
| AI classification evaluation | Whether the AI suggests the right category | The real AI service on a fixed set of 20 labelled assets, against the target written in requirement AI-01.5 | Developers | 6 |
| Sustainability-calculation validation | Whether the dashboard numbers are right | Ten cases worked out by hand from the formulas of the design document and compared with the system | Developers | 7 |
| Acceptance | Whether the system is ready for its users | Test users do the three tasks of requirement NFR-01 on a task sheet: register an asset, find a suitable listing and submit a request | Test users | 8 |

**Black-box testing.** For each function we list the equivalence classes of its input. All values in one class should behave the same way, so one value from each class is enough. We add the values at the edges of the classes, because faults are often there. For example, the classification threshold is tested at 0.599, 0.600 and 0.667.

**White-box testing.** We measure how much of the code the tests run, by statement and by branch, with the coverage tool for Python. Section 3.3 gives the numbers and the parts that are not covered.

**Regression testing.** The automated tests are run as one set. When a fault is fixed, a test for it is added, and the whole set is run again, so a fix cannot quietly break something else. In Phase 6 the tests in `test_demo_checks.py` and `test_walkthrough_fixes.py` were added this way, after faults we found when we walked through the demo. Phase 6 ended with 159 tests. Phase 7 added 32 more (sections 3, 5, 6 and 7), and all 191 were run together for this document.

**Pass criteria.** An automated test passes when every check in it holds. For the AI evaluation, the sustainability validation and the acceptance test, the pass criterion is the target we wrote in Phase 1 or Phase 3, before any result existed.

**Test case numbers.** UT is a unit test, IT an integration test, ST a system test, AT an AI test, SV a sustainability validation case and UA a user-acceptance case.

**Table 2.2 Number of automated tests by kind**

<!-- widths: 2600,1500,5260 -->
| Kind | Tests | Where they are in the repository |
|---|---|---|
| Unit (section 3) | 14 | src/tests/test_units.py |
| Integration and feature tests from Phase 6 (sections 4 and 6) | 159 | 18 files, listed in Table 4.2 |
| System (section 5) | 5 | src/tests/test_system_workflows.py |
| AI failure conditions (section 6) | 3 | src/tests/test_ai_failures.py |
| Sustainability validation (section 7) | 10 | src/tests/test_sustainability_validation.py |
| **Total** | **191** | |
