## 2.5 Design and Implementation Constraints

<!-- widths: 900,8460 -->
| ID | Constraint |
|---|---|
| C-01 | We will use the tools picked in Phase 2 (Django 5.2 LTS, PostgreSQL and a separate AI adapter), unless testing in Phase 4 shows they won't work. If we change, we will write down why. |
| C-02 | Our budget is AED 0, so we only use free tiers, university services or open-source tools unless the instructors approve a cost. |
| C-03 | We only store made-up or anonymised data, never real KU records or staff details. |
| C-04 | There is no live connection to KU's ERP, finance, procurement or login systems. |
| C-05 | AI features use existing (pretrained) models through the AI adapter; we don't train our own. |
| C-06 | Only the fields an AI task needs are sent to an AI service, never passwords or unnecessary personal data. |
| C-07 | The classic system has to install and run from the repository without a paid account or an AI key (NFR-09). |
| C-08 | All work goes through our GitHub repository, with each member committing their own work and teammates reviewing pull requests. |
| C-09 | The system is a website in English that works on laptops and phones. No phone apps and no Arabic version in this release. |
| C-10 | The course sets the schedule: design in Phases 4–5 (week of 26 October), first build in Phase 6 (week of 16 November) and the final demo in Phase 8. |

## 2.6 User Documentation

<!-- widths: 900,4300,4160 -->
| ID | Document | Who it's for |
|---|---|---|
| D-01 | Setup guide (README) | Graders and developers |
| D-02 | One-page guides for requesters, custodians, department representatives and approvers | Staff using the system |
| D-03 | Help text next to forms and status labels | All users |
| D-04 | Admin guide for roles, departments, categories, approval settings and AI settings | Administrators |
| D-05 | A "How AI suggestions work" page explaining scores, confidence and how to override them | All users |
| D-06 | A short note on how each sustainability number is calculated (section 6.1) | Sustainability and finance staff |

## 2.7 Assumptions and Dependencies

**Assumptions**

- A-01: The lab instructors are our client and will confirm the requirements and the TBD values in Appendix C.
- A-02: Made-up data of the size planned in Phase 1 (500 assets, 10 departments, 50 requests, 20 labelled matching cases) is enough to show and test every feature.
- A-03: The nine roles from Phase 1 cover everyone involved, and one person can have more than one role.
- A-04: One asset record can be a batch of identical items with a quantity, for example 20 identical chairs.
- A-05: The current KU process in Phases 1 and 2 is our best reconstruction; we haven't checked it with KU staff.

**Dependencies**

- DEP-01: The AI features need access to the AI services we picked, at an acceptable cost (Phase 2, section 7). Without it we use the local model or the classic features.
- DEP-02: Putting the site online depends on the free hosting tier from Phase 2, plus separate storage for uploaded files.
- DEP-03: Carbon estimates need published emission factors for each category (TBD-6).
- DEP-04: Approval limits and special-handling rules need KU's real values (TBD-1, TBD-2, TBD-8).
