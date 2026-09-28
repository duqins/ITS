# Phase 2 contributions and review

Dawra Campus is our proposed KU asset reuse and life-cycle project. This folder collects the three members' contributions from the Version 3 review package. The analysis uses a **22 September 2026 source snapshot**; this contribution workflow was prepared on **28 September 2026**.

## Where we are now

- [Sultan's financial analysis, schedule and risks](sections/01-sultan-financial-schedule-risk.md) and the [shared calculation inputs](evidence-and-calculations.json) begin the member review process.
- Zayed and Ghaith must review and commit their own prepared Markdown files through their own GitHub accounts. Missing files mean their contributions are pending.
- The [published Word report and slides](progress/2026-09-22/README.md) are the earlier 18-page / 30-slide snapshot. The Version 3 team review package contains the newer 27-page report and 43-slide presentation; final publication must match the reviewed member sources.
- Two interviews, the current KU workflow and baseline, and measured prototype results remain pending. A successful check or merge does not make these complete.

## One contribution and one PR per person

| Member | Student ID | Contribution branch | Reviewer |
| --- | --- | --- | --- |
| Sultan Almheiri | 100065654 | `phase2/sultan-feasibility-review` | Zayed |
| Zayed Alfadli | 100064657 | `phase2/zayed-feasibility-review` | Ghaith |
| Ghaith Alhinaai | 100066185 | `phase2/ghaith-feasibility-review` | Sultan |

Each member commits their own work. A teammate reviews it from their own account. Never mark an approval or interview complete on someone else's behalf.

### Merge order

1. Review Sultan's PR into `phase2/progress-update`. It includes the shared check and this workflow. Merge it after a teammate approves and the check passes.
2. Zayed and Ghaith fetch that updated integration branch, then create their own branches and PRs using the steps below. They can work in parallel because they edit separate files.
3. Each member PR needs a teammate approval and passing checks. Resolve comments and use **Create a merge commit** to preserve the individual commits.
4. After all three contributions and the final report/slides agree, review the combined [Phase 2 PR #3](https://github.com/duqins/ITS/pull/3) into `main`. Merge only after its review and checks are complete.

Do not merge PR #3 early. Separate teammate PRs can only be opened after their branches contain changes. Their branches are proposed names, not a claim that they already exist.

## Zayed: make your contribution

After Sultan's PR is merged, run these commands inside your own clone:

```powershell
git fetch origin
git switch -c phase2/zayed-feasibility-review origin/phase2/progress-update
git config user.name
git config user.email
```

Check that the displayed identity is yours and that the email is verified on your GitHub account. If necessary, set your own identity locally with `git config user.name "YOUR NAME"` and `git config user.email "YOUR VERIFIED EMAIL"`.

Copy `sections/02-zayed-context-market-operational-legal.md` from the team review package to `docs/phase2/sections/02-zayed-context-market-operational-legal.md` in your clone. Read it, correct it and record what you checked. Its context, market, operational and legal claims are your review responsibility. Replace the package-only `../Phase2_Feasibility_Study.md` link with `../README.md` so it works on GitHub. Preserve the source dates, citations, assumption labels, pending evidence and AI disclosure.

```powershell
node scripts/check-phase2.js
git add docs/phase2/sections/02-zayed-context-market-operational-legal.md
git commit -m "docs(phase2): add Zayed context and market analysis"
git push -u origin phase2/zayed-feasibility-review
```

On GitHub, open **Pull requests → New pull request**. Set base to `phase2/progress-update` and compare to `phase2/zayed-feasibility-review`. Explain your actual review and remaining evidence. Ghaith reviews this PR.

## Ghaith: make your contribution

After Sultan's PR is merged, run these commands inside your own clone:

```powershell
git fetch origin
git switch -c phase2/ghaith-feasibility-review origin/phase2/progress-update
git config user.name
git config user.email
```

Use your own name and a verified GitHub email, correcting the local Git configuration if needed. Copy `sections/03-ghaith-technical-data-ai.md` from the team review package to `docs/phase2/sections/03-ghaith-technical-data-ai.md`. Review the architecture, deployment, data, AI functions, evaluation targets and fallback. Replace the package-only `../Phase2_Feasibility_Study.md` link with `../README.md`. Keep untested targets labelled as targets and retain the AI disclosure.

```powershell
node scripts/check-phase2.js
git add docs/phase2/sections/03-ghaith-technical-data-ai.md
git commit -m "docs(phase2): add Ghaith technical data and AI analysis"
git push -u origin phase2/ghaith-feasibility-review
```

Open a PR with base `phase2/progress-update` and compare `phase2/ghaith-feasibility-review`. Explain your actual review and any untested assumptions. Sultan reviews this PR.

## What the reviewer checks

- The author's ID and contribution are correct; the author can explain the material.
- Statistics and prices have sources and dates. Assumed quantities are clearly labelled.
- Equations, units and costs agree with the shared model. Cash savings and the value of time stay separate.
- Interviews, tests and approvals are not claimed without records.
- The AI-use paragraph remains accurate; comments and changes are resolved.

Use GitHub's **Files changed → Review changes → Approve** after actually reviewing. An unchecked box or a suggested reviewer is not an approval.

## Automatic checks and final publication

Run `npm run check:phase2` or `node scripts/check-phase2.js`. No dependency installation is needed. GitHub runs the same **Phase 2 document checks** on pushes and pull requests.

The check validates the available member files' IDs, local links, tables, citation identifiers, conflict markers and calculation-file JSON. It reports missing teammate files as pending while integration is in progress. For PRs into `main` and pushes to `main`, `--require-all` makes all three member files mandatory. Run `node scripts/check-phase2.js --require-all` locally before final integration. The check does not verify external sources, recalculate the finance model, prove interviews happened, approve the work or build the final Word/PPT files.

Before the final merge, all three member files must be present and peer-reviewed. Reconcile their numbers and recommendations, update the Word report and presentation to match, inspect their layout, and confirm the submission date with the instructor. Keep the academic-prototype recommendation separate from any claim that a live KU rollout has been approved.
