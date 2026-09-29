# Dawra Campus Phase 2 financial analysis, schedule and the consolidated risk register

**Section review lead:** Sultan Almheiri

**Student ID:** 100065654

**Version:** 3.0; source and price snapshot: 22 September 2026

**Repository revision:** 28 September 2026

This contribution covers Sultan's financial analysis, schedule and consolidated risks. Section and equation numbers follow the Version 3 team review package, so gaps in numbering are intentional. The supporting references are included below; shared inputs are in the [evidence and calculation model](../evidence-and-calculations.json). See the [team contribution workflow](../README.md) for review and integration steps. The analysis was prepared with AI assistance; personal and peer review remain to be recorded in the pull request.

**Project:** Dawra Campus is our proposed brand for a KU staff website for approved asset reuse and life-cycle records. The academic prototype also includes maintenance, retirement, sustainability reporting, hosted deployment and AI support.

**Shared conclusion:** Continue the academic prototype subject to the stated conditions. The monitor case alone does not justify a custom live KU rollout once development and support time are counted. Two interviews, the current KU baseline and measured technical results remain pending.

# 10  One time and recurring costs

Nonrecurring costs prepare the system once. Recurring costs keep it running. We separate cash paid from the value of student and staff hours, following life-cycle cost principles. [S24] The Phase 1 student cash target remains AED 0. The paid scenario below tests affordability; it is not an approved purchase. [S02]

| Cash cost | When it occurs | AED | Basis |
| --- | --- | --- | --- |
| Setup allowance | One time | 200.00 | AF09 |
| Setup reserve 15% | One time | 30.00 | AF10 |
| Initial cash investment | One time | 230.00 | 200 + 30 |
| Hosting usage example | Every year | 273.23 | S11, S14; AF02–05 |
| AI usage allowance | Every year | 440.70 | USD 10/month; AF07 |
| Files and backups | Every year | 220.35 | USD 5/month; AF08 |
| Annual reserve 15% | Every year | 140.14 | AF10 |
| Fixed recurring cash | Every year | 1,074.43 | Before per-monitor handling |
| Extra handling/materials | Each monitor reused | 25.00 | AF11; excludes wages |

The model spends the full reserve upfront and each year. Totals use unrounded inputs. AI and backup amounts are caps chosen for analysis, not supplier quotations. Eligible items need no major repair; otherwise reassess the case. Card fees, cloud tax and institutional overhead require actual quotes before purchase.

Equation: E5  Monthly hosting = max(5, 0.5×10 + 0.05×20 + 1×0.15 + 1×0.05) = USD 6.20

Railway rates and included Hobby minimum [S11]; assumed quantities AF02–05. This is not a Render/Neon price or a measured bill. Annual conversion: 6.20 × 12 × 3.6725 = AED 273.234 [S14].

Equation: E6  Model usage USD = (0.02Te + 0.40Ti + 1.60To) / 1,000,000

Sourced standard token rates [S30, S31]. Te is embedding input tokens; Ti and To are uncached generation input/output tokens. Include billable retries. Tool charges, tax and storage are separate. Actual tokens are unmeasured, so this formula does not validate the USD 10 cap.

# 11  Quantified benefits and assumptions

The financial case isolates monitors so that each saved purchase has a clear quantity and price. Other asset categories remain in project scope, but no unsupported benefit is credited to them. Start with a defined pilot and replace these inputs with interview and purchase records.

| Input | Base planning assumption | How to verify it |
| --- | --- | --- |
| Current annual purchases | 40 new monitors after existing reuse: 5 departments × 8 purchases each [AF12] | Check permitted purchase/request records; avoid counting demand already met by reuse |
| Extra purchases avoided | 8 of those 40, or 20%, each year [AF13] | Find suitable, available and authorised spares and record the purchases actually displaced |
| Price per monitor | AED 345 retail proxy including VAT [S15] | Obtain a like-for-like KU price; check specification, warranty, delivery and remaining useful life |
| Extra handling cash | AED 25 per reused monitor [AF11] | Record actual collection/material/inspection costs |
| Time horizon | Three years, same annual demand and net benefit [AF01, AF17] | Check recurring supply, useful life, adoption and timing |

We choose 10%, 20% and 30% as low, middle and higher test cases, not published success rates. The middle case is a hypothesis that one in five otherwise-new purchases can be replaced. Spare supply, suitability, permission and staff adoption can make the realised figure smaller or zero.

Equation: E7  Annual gross purchase avoidance B = N × P = 8 × 345 = AED 2,760

Project accounting definition: N is additional purchases avoided after the current process, P is the comparable price [S15; AF12–13]. No revenue is earned; the avoided expenditure remains available for other needs.

Equation: E8  Gross purchase reduction = 100 × 8 / 40 = 20%

Derived from AF12–13. The denominator is this pilot’s assumed new-monitor purchases, not KU’s whole budget. The illustrated two-monitor request represents AED 690 gross avoidance if it genuinely prevents those purchases.

Do not count the same transfer as both avoided buying and resale revenue. Do not include disposal or carbon savings without a separate supported factor. Benefits occur only when reuse is suitable, approved and additional to the baseline.

# 12  Expected ROI and payback scenarios

Expected here means the result of our base planning case if its assumptions hold. It is not a statistical forecast. We first examine cash costs, then add time costs in section 13.

Equation: E9  Annual net cash benefit A = NP − (R + NV)

Derived cash model: R = AED 1,074.4266 recurring fixed cost, V = AED 25 per monitor. For N=8: 2,760 − 1,274.4266 = AED 1,485.57 annually. Initial cash I = AED 230 is separate.

Equation: E10  Year one ROI (%) = 100 × [B − (I + R + NV)] / (I + R + NV)

ROI method [S16] applied to the same year’s benefits and included costs. Base case: net AED 1,255.57 / total cost AED 1,504.43 = 83.46%. This excludes the time values added in section 13.

Equation: E11  Simple payback in years = Initial investment / Annual net benefit

Simple payback method [S25] when annual net benefit is positive and uniform. Base cash case: 230 / 1,485.5734 = 0.155 years, or 1.86 months after go-live. With zero/negative annual net benefit, no simple payback occurs.

| Annual extra reuse | Gross reduction | Annual net cash AED | Year one ROI | Cash payback months |
| --- | --- | --- | --- | --- |
| 0 | 0% | -1,074.43 | -100.00% | No payback |
| 4 | 10% | 205.57 | -1.74% | 13.43 |
| 8 | 20% | 1,485.57 | 83.46% | 1.86 |
| 12 | 30% | 2,765.57 | 158.04% | 1.00 |

The 1.86-month result spreads net benefits evenly across the year. Actual purchases are discrete, so it is not a promised recovery date. A safer annual view is below. Count the actual transaction dates during a trial. This simple model excludes discounting, inflation and residual value. [S25]

| Base case point | Cumulative net cash AED |
| --- | --- |
| Start before benefits | -230.00 |
| End of year 1 | 1,255.57 |
| End of year 2 | 2,741.15 |
| End of year 3 | 4,226.72 |

Five extra monitor purchases must be avoided to cover the first year’s included cash costs. Four cover the recurring annual cash cost. These are quantity thresholds, not payback durations. Base annual net cash equals 10.77% of the assumed AED 13,800 purchase baseline; first-year net saving is 9.10% after setup.

# 13  Investment including the value of time

A small cash investment can make cash ROI look high while development still takes substantial effort. We therefore add an explicit time-value scenario. AED 30/hour is a planning valuation for sensitivity analysis, not a KU wage, market salary or payment to students. [AF14–16]

| Resource investment | Calculation | AED |
| --- | --- | --- |
| Development and launch time once | 180 hours + 15% reserve = 207 hours × AED 30 | 6,210.00 |
| Initial cash including reserve | From section 10 | 230.00 |
| Initial investment including time | 6,210 + 230 | 6,440.00 |
| Annual recurring cash at 8 monitors | 1,074.4266 + 8 × 25 | 1,274.43 |
| Annual support time | 24 hours × AED 30 | 720.00 |
| Additional handling time | 8 monitors × 0.5 hour × AED 30 | 120.00 |
| Annual operating cost including time | 1,274.4266 + 720 + 120 | 2,114.43 |

The 0.5 hour is additional effort per monitor across all staff after baseline work, including checks and record updates. A two-monitor request therefore counts one additional hour in this scenario. Support covers maintenance, account administration and backups, excluding that separately counted handling. Initial launch/introduction effort is inside the development estimate.

Equation: E12  Annual net benefit including time = 2,760 − 2,114.4266 = AED 645.57

Same incremental accounting as E9; time assumptions AF14–16. Initial investment remains separate.

Equation: E13  Three year ROI (%) = 100 × [3B − (I + 3O)] / (I + 3O)

ROI method [S16]; I = 6,440 and O = 2,114.4266. Total benefits AED 8,280; total included cost AED 12,783.28; net AED −4,503.28; ROI −35.23%. No discounting. This is still a scenario, not an institutional total-cost quote.

The base case does not recover the time-inclusive investment within three years. The 4- and 12-monitor cases also fail that horizon. At least 13 additional monitors a year, or 32.5% of the assumed baseline, would be needed for three-year recovery at these same costs. Extra demand may also raise costs, so this is a validation threshold rather than a promise.

Sensitivity to hourly value matters: at AED 15/hour, the base case still needs longer than three years; at AED 60/hour it has a negative annual net benefit. This is why the recommendation supports the academic prototype while requiring stronger evidence before KU adoption.

# 15  Schedule resources and legal constraints

Capacity scenario AS01: three members × eight hours per week × eight weeks = 192 person-hours. This uses the upper end of the Phase 1 weekly assumption. The remaining weeks, each member’s availability and the exact deadline still require confirmation. [S02]

| Work package | Lead | Initial hours AS02 |
| --- | --- | --- |
| Requirements and design | Zayed with all | 20–28 |
| Core inventory and approval workflows | Sultan | 36–48 |
| Maintenance, life cycle and reports | Sultan and Zayed | 24–32 |
| AI functions and evaluation | Ghaith | 30–44 |
| Deployment, uploads and security | Ghaith and Sultan | 16–24 |
| Tests, integration and documentation | All | 24–34 |
| Total before reserve | All | 150–210 |
| With 15% effort reserve | All | 172.5–241.5 |

At the midpoint, 180 hours plus 15% reserve is 207 hours: 15 more than the 192-hour scenario. The range therefore does not yet establish schedule feasibility. Review estimates with each owner, sequence dependencies before committing to implementation. Component reuse is already included. The midpoint needs five additional hours from each member across the period; the upper estimate needs more. Confirm availability rather than silently dropping required functions.

| Order | Dependency and exit check |
| --- | --- |
| First | Confirm workflow, evidence access and acceptance criteria. Complete the small stack/AI check. |
| Then | Build inventory and permissions before requests, approvals and custody. Add life-cycle records and AI against the stable baseline. |
| Before demonstration | Finish persistent uploads, hosted deployment, all required AI families, fallback, tests and documentation. Any scope change needs instructor agreement. |

## Legal ethical and university policy checks

Confirm asset ownership, release/receipt authority, finance/procurement thresholds, safe handling, data permission, provider terms and software licences. Use synthetic data until access is authorised. Do not send sensitive fields to an AI provider by default. Keep human approvals and record-based explanations. These are required checks, not a claim of legal or KU policy approval. [S01, S19]

# 16  Quantified risk assessment

Use a team-defined 5 × 5 likelihood–impact matrix for the remaining semester. NASA supports assessing, assigning, treating and reviewing software risks; our scores and cut-offs are planning judgments, not NASA-mandated values. [S17]

Equation: E15  Priority score = Likelihood rating × Impact rating

Team-adapted prioritisation method informed by [S17]. Each rating is 1–5. The product is neither a probability nor a money loss.

| Rating | Likelihood with current controls | Highest applicable impact |
| --- | --- | --- |
| 1 | Unlikely; relevant control demonstrated | Under 2 hours of rework, no required workflow affected |
| 2 | Possible with limited exposure | Up to 1 day of rework, minor feature affected |
| 3 | Plausible; important control untested | 2–3 days of delay or a repeated core trial |
| 4 | Expected without action; essential dependency missing | 4–7 days delay or unsupported feasibility conclusion |
| 5 | Almost certain without intervention | Over 7 days, missed mandatory deadline, confidential disclosure or unauthorised major action |

A working day here means one agreed project working day; calendar effects depend on availability. Bands: 1–4 low, 5–9 medium, 10–16 high, 17–25 critical. Review all impact-5 risks regardless of product score. Existing problems are also tracked as issues. Day boundaries and bands are team assumptions.

| Risk | L | I | Score | Owner | Target residual |
| --- | --- | --- | --- | --- | --- |
| R1 KU baseline and access unconfirmed | 4 | 4 | 16 | Zayed | 2 × 4 = 8 |
| R2 AI recommends unsuitable items | 3 | 4 | 12 | Ghaith | 2 × 4 = 8 |
| R3 Restricted data or credentials exposed | 3 | 5 | 15 | Ghaith | 1 × 5 = 5 |
| R4 Duplicate work removes the benefit | 3 | 4 | 12 | Zayed | 2 × 4 = 8 |
| R5 Hosting or AI limits interrupt work | 3 | 3 | 9 | Sultan | 2 × 2 = 4 |
| R6 Work exceeds available time | 3 | 5 | 15 | Sultan | 2 × 5 = 10 |

R1: owner/access evidence missing. R2/R3: AI and permission controls untested. R4: duplicate work unknown. R5: usage and recovery untested. R6: capacity unconfirmed. Current scores are provisional. Target residual scores are desired outcomes after checked controls, not achieved reductions.

Equation: E16  Expected cash loss = Event probability × Cash impact

Quantitative method [S18] for a defined scenario and period. We do not calculate it because defensible probabilities and loss amounts are unavailable. A score of 12 is not 12%, AED 12 or expected loss.

# 17  Mitigation and contingency plan

Mitigation reduces a risk before it occurs. Contingency defines the response when its trigger occurs. The owner coordinates the action and gathers evidence before changing the score. [S17]

## R1  KU baseline and access unconfirmed

Owner: Zayed. Mitigation: Arrange two interviews and a permitted sample. Record the current workflow.

Trigger: No verified baseline by the agreed evidence cut-off. Contingency: Use labelled synthetic cases and state that KU benefit remains unverified. Seek instructor direction.

## R2  AI recommends unsuitable items

Owner: Ghaith. Mitigation: Filter eligibility before ranking. Freeze labels, check outputs and require staff review.

Trigger: Any ineligible actionable result or failure of the matching targets. Contingency: Use classic search for task completion, investigate and retest AI. Keep the unmet requirement visible.

## R3  Restricted data or credentials exposed

Owner: Ghaith. Mitigation: Synthetic data first, minimal fields, permission tests and protected secrets.

Trigger: Any unauthorised access, restricted prompt or exposed key. Contingency: Stop the affected route, revoke keys and preserve relevant logs. Involve the authorised owner where applicable.

## R4  Duplicate work removes the benefit

Owner: Zayed. Mitigation: Measure the whole request, including review, handover and reconciliation.

Trigger: No lower total handling effort or staff reject the workflow. Contingency: Redesign around the verified process or reconsider an existing product. Retain required approvals.

## R5  Hosting or AI limits interrupt work

Owner: Sultan. Mitigation: Agree a spending cap. Measure usage and test storage, backup and fallback.

Trigger: Failed availability check or projected spend exceeds the approved cap. Contingency: Recover or move to a tested option. A temporary local demo does not complete hosted deployment.

## R6  Work exceeds available time

Owner: Sultan. Mitigation: Estimate dependencies with each owner. Integrate early and review weekly.

Trigger: Remaining effort exceeds confirmed capacity or a dependent task slips. Contingency: Reassign work and seek instructor agreement for any required-scope change. Record deadline risk.

Review at each team meeting and after a failure or major change. Record date, evidence, current/target score and who accepts remaining risk. R3 remains subject to explicit review even at its target score; R6 remains high after its proposed controls. Do not calculate a percentage reduction from ordinal scores.

# 19  Financial and schedule assumptions

Assumptions are planning choices made for this draft. They are not external statistics, KU measurements or approved commitments. Check them before relying on the calculations.

| ID | Input | Status or purpose |
| --- | --- | --- |
| AF01 | Three-year decision horizon; steady annual activity | Simple, undiscounted comparison; no terminal value or price growth |
| AF02–05 | 0.5 GB RAM; 0.05 vCPU; 1 GB volume; 1 GB monthly egress | App/database usage example only; test actual usage |
| AF06 | Two monitors in the illustrated request | A scenario, not a completed KU transaction |
| AF07–08 | USD 10/month AI; USD 5/month files and backups | Unapproved spending caps, not provider quotations |
| AF09 | AED 200 initial setup cash | Materials/configuration allowance excluding labour |
| AF10 | 15% cash reserve spent upfront and each year | Conservative planning convention; separate from risk expected loss |
| AF11 | AED 25 additional cash per reused monitor | Local handling/materials; major repairs excluded from eligible stock |
| AF12 | 40 annual new-monitor purchases after current reuse | Five proposed departments × eight purchases; all inputs unverified |
| AF13 | 4, 8 or 12 extra purchases avoided yearly | 10%, 20%, 30% of AF12; scenarios, not externally proven rates |
| AF14 | 207 hours of development at AED 30/hour | 180 base hours plus 15% effort reserve; time-value assumption, no salary paid |
| AF15 | 24 support hours/year at AED 30/hour | Two hours/month; excludes transfer handling counted separately |
| AF16 | 0.5 additional staff hour per reused monitor | Across all roles after baseline effort; applies per monitor, not per request |
| AF17 | Benefits recur uniformly after go-live | Simplifies payback; discrete transactions can recover costs later |
| AS01 | Three members × eight hours per week × eight weeks = 192 hours | Capacity scenario based on the upper end of Phase 1 availability; confirm remaining weeks and each member's capacity |
| AS02 | Work packages total 150–210 hours before a 15% reserve | 172.5–241.5 hours with reserve; midpoint 207 hours exceeds AS01 by 15 hours |

# Review and AI use

AI assisted drafting, source research, calculations and artifact preparation. Sultan remains responsible for understanding and checking this contribution. Automated structural checks and an AI-assisted arithmetic audit do not establish personal or teammate approval. The calculations are planning scenarios, not measured KU results; interviews and tests remain pending. Any corrections, additional tool use and actual reviews should be recorded in the pull request.


# References used in this part

Source pages checked 22 September 2026. Source methods and capabilities do not establish our assumed workload, percentages or hours.

### S01 COSC336 course project description

[COSC336 course project description](https://github.com/duqins/ITS/blob/main/docs/reference/Project-September2026.pdf)

Page 7: six feasibility areas; page 5: classic and AI comparison.

### S02 Group 4 Phase 1 scope and success criteria

[Group 4 Phase 1 scope and success criteria](https://github.com/duqins/ITS/blob/main/docs/phase1/sections/07-success-criteria.md)

Team-defined prototype targets, not achieved results. Scope: https://github.com/duqins/ITS/blob/main/docs/phase1/sections/02-project-overview.md . Effort and budget: https://github.com/duqins/ITS/blob/main/docs/phase1/sections/08-project-plan.md .

### S11 Railway pricing and billing

[Railway pricing and billing](https://docs.railway.com/pricing)

Rates and Hobby minimum. Billing: https://docs.railway.com/pricing/understanding-your-bill .

### S14 CBUAE reference exchange rates

[CBUAE reference exchange rates](https://centralbank.ae/umbraco/Surface/Exchange/GetExchangeRateAllCurrency)

Table updated 21 September 2026: USD 1 = AED 3.6725. Reference rate, not card fees.

### S15 Sharaf DG Samsung S3 S33GF monitor listing

[Sharaf DG Samsung S3 S33GF monitor listing](https://uae.sharafdg.com/product/samsung-s3-s33gf-essential-fhd-monitor-24inch-ls24f330eamxue/)

22 September 2026 listing: AED 345 incl. VAT, ENGAGE seller, 24-inch FHD with HDMI. Retail proxy, not KU quote. Delivery excluded.

### S16 NHS Measurement for Improvement and Return on Investment

[NHS Measurement for Improvement and Return on Investment](https://www.england.nhs.uk/improvement-hub/wp-content/uploads/sites/44/2017/11/2010-Measurement-for-Improvement-and-ROI.pdf)

Printed page 26: ROI = net benefits / costs x 100. Project inputs are separate assumptions.

### S17 NASA Software Engineering Handbook SWE-086

[NASA Software Engineering Handbook SWE-086](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695470/SWE-086%2B-%2BContinuous%2BRisk%2BManagement)

Risk assessment, owners, mitigation, triggers and continuing review. Our numeric rubric is a team adaptation.

### S18 NIST IR 8286Ar1

[NIST IR 8286Ar1](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=933223)

Printed pages 55–56 and 59: probability and monetary impact support quantitative risk exposure. Ordinal scores are not probabilities.

### S19 NIST AI RMF Playbook Measure

[NIST AI RMF Playbook Measure](https://airc.nist.gov/airmf-resources/playbook/measure/)

Context-specific metrics, limitations and corrective action; no prescribed sample sizes here.

### S24 GAO Cost Estimating and Assessment Guide

[GAO Cost Estimating and Assessment Guide](https://www.gao.gov/assets/d20195G.pdf)

GAO-20-195G (2020), printed pages 94–95: recurring/nonrecurring cost categories; page 123: double-counting checks. Our project amounts are assumptions.

### S25 NIST investment analysis guide

[NIST investment analysis guide](https://nvlpubs.nist.gov/nistpubs/ams/NIST.AMS.200-11.pdf)

Appendix A1.3, printed page 25 equation 7: simple payback from initial investment and uniform annual net inflow. Page 26 discusses limitations. Our inputs are scenarios.

### S30 OpenAI GPT 4.1 mini model documentation

[OpenAI GPT 4.1 mini model documentation](https://developers.openai.com/api/docs/models/gpt-4.1-mini)

Provisional text-model candidate gpt-4.1-mini-2025-04-14. Standard uncached text rates: USD 0.40 per million input tokens, USD 1.60 per million output tokens. Access and suitability untested.

### S31 OpenAI text embedding 3 small documentation

[OpenAI text embedding 3 small documentation](https://developers.openai.com/api/docs/models/text-embedding-3-small)

Provisional hosted semantic-search candidate. USD 0.02 per million input tokens. Token volume remains unmeasured.
