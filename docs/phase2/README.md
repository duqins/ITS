# Dawra Campus Phase 2 feasibility study

The final submission combines the three reviewed member contributions with the instructor's latest feedback. The report revision is **29 September 2026**. The financial source baseline remains **22 September 2026**, with later KU research and technical clarifications dated in the references.

## Final files

- [Final Word report for Blackboard](final/Dawra_Campus_Phase2_Feasibility_Study.docx)
- [Final PowerPoint presentation](final/Dawra_Campus_Phase2_Presentation.pptx)
- [Read the final report on GitHub](final/Dawra_Campus_Phase2_Feasibility_Study.md)
- [Submission contents and evidence status](final/README.md)
- [Shared evidence and calculation inputs](evidence-and-calculations.json)

The [22 September materials](progress/2026-09-22/README.md) are an archived progress snapshot. Use the final files above for submission and presentation.

## Individual contributions

| Member | Student ID | Reviewed contribution | Merged PR |
| --- | --- | --- | --- |
| Sultan Almheiri | 100065654 | [Financial analysis, schedule and consolidated risks](sections/01-sultan-financial-schedule-risk.md) | [#4](https://github.com/duqins/ITS/pull/4) |
| Zayed Alfadli | 100064657 | [Scope, stakeholders, market and operational/legal analysis](sections/02-zayed-context-market-operational-legal.md) | [#5](https://github.com/duqins/ITS/pull/5) |
| Ghaith Alhinaai | 100066185 | [Technical design, data, AI and evaluation](sections/03-ghaith-technical-data-ai.md) | [#6](https://github.com/duqins/ITS/pull/6) |

Each member's original commits and reviewed source file remain in the history. The final report consolidates those contributions and adds the later classroom role-play exercise. Member snapshots may retain earlier evidence-status wording; the final report records the current submission status.

## Evidence and recommendation

Two [AI stakeholder role-play interviews](final/Simulated_Stakeholder_Interviews.md) are included under the classroom approach the instructor allowed. They explore proposed requirements and are explicitly simulated. No real KU employee participated, and they do not validate actual KU demand, approval rules or savings.

The base monitor scenario assumes eight additional avoided purchases a year. It gives AED 1,485.57 annual net cash benefit, but the value of development and support time makes three-year ROI negative at -35.23%. The recommendation is to continue the academic prototype subject to the stated conditions. A live KU rollout still needs evidence and an institutional decision.

Hosted deployment, maintenance, retirement, sustainability reporting and all required AI functions remain in scope. Actual KU workflow, staff timings, provider usage and technical results remain to be measured.

## Review and checks

All three member PRs are merged into the integration history. Final publication goes through a pull request to `main`, with one actual teammate approval and passing **Phase 2 document checks**. Use a merge commit to retain individual contribution history.

Run `node scripts/check-phase2.js --require-all` before merging. The check validates member IDs, local links, tables, citation identifiers, conflict markers and calculation-file JSON. It does not establish source accuracy, real interviews, test results or document layout. The final Word pages and presentation slides are reviewed separately.

The Phase 2 deadline in the current course brief is the lab week beginning **4 October 2026**, subject to the instructor's confirmed lab arrangements. Publishing on GitHub does not submit the Blackboard assignment.
