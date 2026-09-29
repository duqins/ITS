# Phase 2 Feasibility Study

Working brand and logo for team confirmation. Student project at Khalifa University.

| Prepared by | Student ID |
| --- | --- |
| Sultan Almheiri | 100065654 |
| Zayed Alfadli | 100064657 |
| Ghaith Alhinaai | 100066185 |

22 September 2026   Version 2.0   Evidence review and planning draft

## Recommendation

Proceed with the semester prototype subject to a workable time plan, permitted data, tested hosting and an AI evaluation. Evidence does not yet justify adopting the system as a live KU service. Confirm the current process and owner before claiming operational or financial improvement.

## What this report establishes

The proposed scope is defined, three existing systems have been researched, and a cost and benefit model is reproducible. This report covers the instructor’s scope, stakeholder, market, technical and financial checklist, plus all six course feasibility areas. [S01]

| Evidence status | Meaning in this report |
| --- | --- |
| Sourced | A cited official page or course document supports the statement. Vendor claims have not been independently tested. |
| Assumed or proposed | A planning input, target or design choice to validate. AF and AS identifiers trace numerical assumptions. |
| Still pending | Two interviews, a verified KU baseline, actual usage, staff timings, AI results and live deployment evidence. |

# 1  Objectives and project scope

Dawra Campus is a proposed staff-facing website to locate suitable surplus assets and manage their approved reuse. Three KU students would build the academic prototype. Facilities Management is a proposed functional owner, subject to confirmation. [S01–S03]

## Objectives and deliverables

- Make suitable items discoverable while preserving permissions, availability, technical compatibility and required approvals.
- Record custody, maintenance and end-of-life actions, with traceable cost and sustainability reports.
- Evaluate whether AI improves matching after counting review effort, errors and usage cost.
- Deliver the website, documented local setup, hosted deployment, tests and the required phase documents. [S01, S02]
| Area | In scope | Out of scope |
| --- | --- | --- |
| Campus work | Nine roles, inventory, requests, search, reservations, approvals, custody and audit | Live KU ERP, finance or procurement integration |
| Asset life cycle | Transfers, maintenance, repair and retirement records | Vehicle scheduling and barcode/RFID hardware |
| Reports | Cost records, conventional/AI reports and sustainability indicators | Purchasing and payment processing |
| AI support | Classification, matching/ranking, sustainable actions and assistant | Training new models from scratch or autonomous approvals |
| Delivery | Responsive website, hosted deployment, setup/restart instructions and documentation | Separate native iPhone/Android apps |

The monitor case is one small investigation within this wider scope. Required maintenance, retirement, sustainability and AI functions remain included. Deployment remains included. Implementation order does not authorise removing course requirements. [S01, S02]

# 2  Stakeholders and ownership

Functional ownership means accountability for the work process, requirements and acceptance. KU publicly places asset management under Facilities Management; this supports proposing that office, but does not prove ownership of the current software. [S03]

The expected needs below come from the course and Phase 1 analysis. They are hypotheses to confirm with stakeholders, not interview findings. [S01, S02]

| System role | Responsibility | Expected need |
| --- | --- | --- |
| Department representative | Approve release and receipt | Clear approval tasks and department controls |
| Asset custodian | Maintain item records and confirm handover | Accurate condition, quantity, location and history |
| Requester | Find items and submit requests | Suitable results and visible request status |
| Business administrator | Configure workflows and handle exceptions | Consistent records and approval routes |
| Procurement officer | Check reuse and procurement rules | Evidence that reuse is permitted and avoids a purchase |
| Finance officer | Check values, costs and thresholds | Traceable figures and authorised decisions |
| Maintenance staff | Inspect, repair and update condition | Work records, costs and safe condition |
| Sustainability officer | Review actions, factors and indicators | Sourced measures and explicit uncertainty |
| System administrator | Operate accounts, security and backups | Tested access and recovery; no automatic business approval |

## Client and development responsibilities

The instructors clarify course scope and evaluate the submission. Sultan, Zayed and Ghaith investigate, build and test the prototype. Student development access does not authorise releasing university property. Technical administration does not automatically grant business approval rights. Finance and Procurement must confirm applicable approval and record rules.

# 3  Scenario and operational evidence

Proposed case: a staff member needs two working monitors with suitable connections. Another university unit has compatible spare monitors. This is an example, not an observed KU transaction. Quantity two is assumption AF06.

Concept illustration: request, find suitable spares, obtain release and receipt approval, record handover. The image represents a proposed workflow, not a working application.

| Stage | Proposed action and evidence |
| --- | --- |
| Request and search | Record purpose, connection, quantity and date. Check eligibility before offering a match. |
| Approval | Releasing and receiving staff approve. Apply additional policy approvals where required. |
| Handover | Confirm condition, quantity, new location and custody. Record who did what and when. |
| Measure | Count all staff’s active minutes, review, corrections and duplicate entry. Record waiting separately. |

## Two interviews required

| Interview | Evidence to collect | Status |
| --- | --- | --- |
| Asset custodian or Facilities/IT equipment staff | Current system, ownership, availability checks, approval rules, record updates | Pending |
| Requester or department representative | Actual steps, need, delays, repeat entry, acceptable changes | Pending |

Record date, participant role, consent, questions, answers and resulting requirement changes. No completed interview records were available for this draft. If staff access is unavailable, seek instructor direction and identify any role-play as a simulation.

Operational question: does the proposal improve the complete task while fitting KU’s existing obligations? A faster search alone cannot establish lower overall workload.

# 4  Market analysis and alternatives

Our target users are KU staff who request, manage, approve and maintain assets. The size of their unmet need is not yet known. Interviews and permitted records should establish request volumes, existing reuse and remaining gaps. We do not infer a market-size or savings statistic from the assignment.

| Existing system | Documented capabilities | Implication for our proposal |
| --- | --- | --- |
| Rheaply | Internal reuse marketplace, asset information, approvals and impact reporting. AI can suggest listing details for review. [S04, S05] | A close reuse comparator. Reuse and AI already exist commercially. |
| Warp It | Surplus listing/search, claims and redeployment, approvals and impact reports. Homepage describes AI listing help. [S06] | Compare the full transfer process and staff effort, not the presence of a marketplace. |
| Snipe-IT | Inventory, custody, requests, history, permissions and API. [S07] | Consider configuration or extension before assuming custom development is the best operational choice. |

UC Berkeley documents using Rheaply for surplus furniture inventory and reservations. This supports relevance to universities, but does not establish KU demand or performance. [S08]

## Cost comparison boundaries

Snipe-IT advertises free self-hosted software and Basic Hosting at USD 39.99/month or USD 399.99/year. Rheaply requires a quotation on the reviewed pages. Warp It publishes UK pricing bands; these are not a KU offer. Compare equivalent service, support, setup and operating costs before selecting an option. [S04, S07, S23]

## What makes our study specific

Use the same monitor request to compare the verified KU process, our ordinary search and our AI-assisted search. Include compatibility, separate approvals, failed matches, staff checking and any required duplicate entry. Our contribution is the evidence and design decisions for this scenario; we do not claim that AI or reuse is unique.

Decision options: retain the current process, adopt/configure a suitable existing product, or build the academic prototype. Unknown product or KU features remain unverified rather than treated as absent.

# 5  Technical feasibility

Proposed starting option: a Django web application with PostgreSQL and a separate AI-service adapter. Django supplies common web, authentication and permissions facilities; item/department access and approvals still require our own rules. PostgreSQL is a relational database candidate. These choices have not been tested by the team. [S09, S10]

| Option | Reason to consider it | Main trade-off |
| --- | --- | --- |
| Django pages and PostgreSQL | One application can cover forms, workflow and Python AI integration. | Team must confirm Python skills and implement a usable interface and item-level permissions. |
| Separate React interface and API | Useful if team familiarity and interface needs justify separate components. | More interface/API integration and deployment work. This is an architectural alternative, not a tested benchmark. |

## Hardware software and skills

| Resource | Proposed need | Feasibility check |
| --- | --- | --- |
| Development hardware | Existing student or KU lab computers, browser and internet | Run local database and application together; record actual machine limits. No new hardware purchase assumed. |
| Application resources | Web framework, relational database, source control, test tools and persistent uploads | Complete one request/approval transaction and restart without losing records. |
| AI access | Approved pretrained model/service, credentials and usage limits | Test classification, matching, cost and fallback. Provider remains undecided. |
| Skills | Web forms, SQL, permissions, APIs, tests and deployment | Each owner demonstrates a small task; plan time for any skill gap. |

## Technical decision gate

Before confirming the stack, complete a small test covering login, asset registration, an eligible search, separate approval, database persistence and AI failure. Measure resource use and confirm a working hosted route. A source-documented capability does not prove our implementation is feasible.

# 6  Data and AI feasibility

| Data | Minimum information | Quality and access check |
| --- | --- | --- |
| Asset | ID, purpose/specification, condition, quantity, availability, location, custodian and verification date | Missing mandatory fields, duplicates and stale availability need correction. |
| Request and transfer | Need, constraints, dates, authorised requester, release/receipt approvals and handover | Preserve allowed roles and one authoritative reservation/status record. |
| Maintenance and end of life | Inspection, repair, costs, state, authorised action and supporting evidence | Do not infer safety or disposal permission from generated text. |
| Cost and sustainability | Comparable price, attributable costs, mass/factor where used, units and source date | Missing evidence produces N/A or a labelled estimate; no invented carbon savings. |

Start with synthetic data. Phase 1 proposes 500 assets, 10 departments and 50 requests, including 20 fixed eligible matching cases. These are test-design numbers, not KU inventory or demand. Add separate cases where no suitable asset exists. [S02]

## AI boundary and controls

- Classic code enforces access, availability, quantity and compatibility before ranking. AI suggests; authorised staff decide.
- Use pretrained models for classification, semantic matching, ranking, sustainable-action advice, assistant responses and summaries. The model/provider and version remain to be selected. [S01, S02]
- Send only approved necessary fields to external services. Check retention, training use, location and permissions before real data. Synthetic testing does not grant a live-data mandate.
- Keep normal search and forms available. Similarity scores are not automatically probabilities of correctness.
Data/AI feasibility remains conditional on suitable labelled records, service access, acceptable cost and repeatable evaluation. Document what cannot yet be measured. [S19]

# 7  Evaluation metrics and loss

Use the same asset snapshot and requests for ordinary and AI search. Two team members independently label suitable items, resolve disagreements and freeze the evaluation set. Keep development examples separate. Ranked retrieval evaluation uses explicit relevance judgments. [S02, S20]

Equation: E1  Hit@3 (%) = 100 × (Σ h(q)) / (n)

Team operational definition informed by ranked evaluation [S20]. h(q)=1 if request q has a useful top-three result, otherwise 0; n is the eligible request count. A failed response counts as a miss.

Equation: E2  Top-three miss rate (%) = 100 − Hit@3 (%)

Derived complement of E1; an evaluation error rate, not neural-network training loss.

Equation: E3  Classification loss = (Wrong category predictions) / (Tested labelled assets)

Normalised zero-one loss [S21]. Missing or invalid predictions count as wrong. No custom-model training is proposed.

| Planned check | Target from Phase 1 | Interpretation |
| --- | --- | --- |
| Useful matching | At least 16 of 20 requests | 80% target Hit@3, not observed accuracy |
| Additional AI value | At least 2 more successes than ordinary search | Same cases and eligibility rules |
| Classification | At least 16 of 20 categories correct | Loss at most 4/20 = 0.20 |
| Eligibility and authority | 0 ineligible actionable suggestions; 0 approval bypasses in 14 planned tests | Zero observed errors would not establish zero risk |
| Fallback | 5 failure cases restore classic controls within 15 seconds | Outage, timeout, rate limit, malformed output and low confidence |

Targets are proposed acceptance criteria [S02]. Also report model/version, prompts, paired wins/losses, errors, latency, usage cost and staff review minutes. A 20-case synthetic trial cannot prove campus-wide savings or statistical significance. [S19, S20]

# 8  Financial costs and budget

The Phase 1 student cash budget is AED 0, using existing computers and free or university-provided resources. Paid services below are an optional planning scenario, not adopted spending. Free services still consume effort and may not satisfy all requirements. [S02]

| Hosting candidate | Known condition | Decision needed |
| --- | --- | --- |
| Render plus Neon | Render sleeps after 15 idle minutes and loses local files on restart. Neon Free lists 0.5 GB storage, 100 CU-hours and 5 GB public transfer per project/month. [S12, S13] | Test persistence and limits. Select a lasting upload store before recommending this route. |
| Railway Hobby | Minimum USD 5 includes usage. RAM 10/GB-month; CPU 20/vCPU-month; volume 0.15/GB-month; egress 0.05/GB. [S11] | Assumed combined use below gives USD 6.20/month. It requires budget permission and a usage test. |

Equation: E4  Monthly usage = (0.5 × 10) + (0.05 × 20) + 0.15 + 0.05 = USD 6.20

Rates [S11]; quantities AF02–05. Bill = max(USD 5, usage). Annual AED cost = 6.20 × 12 × 3.6725 = 273.23. Exchange rate [S14]; 12-month horizon AF01.

## Optional first year cash costs

| Item | Input | AED | Basis |
| --- | --- | --- | --- |
| Hosting usage example | 0.5 GB RAM; 0.05 vCPU; 1 GB volume/egress | 273.23 | S11, S14; AF02–05 |
| AI spending allowance | USD 10/month cap | 440.70 | AF07; S14 |
| Files and backup allowance | USD 5/month cap | 220.35 | AF08; S14 |
| Setup cash allowance | One-off, excludes labour | 200.00 | AF09 |
| Subtotal | Calculated | 1,134.28 | Derived |
| Reserve | 15%, assumed fully spent | 170.14 | AF10 |
| Fixed cost F | Illustrative | 1,304.43 | Derived |

Totals use unrounded inputs. The allowances are proposed caps, not provider quotations or proof of capacity. The reserve is not expected risk loss. Student labour, staff support, training, governance and cloud tax/fees are not included. Actual payable prices and VAT treatment need confirmation before a full financial decision.

# 9  Benefit estimate ROI and sensitivity

If the proposed system genuinely avoids two additional monitor purchases, the retail-price proxy gives AED 690 gross purchase avoidance: 2 × AED 345. This is before inspection, repair, transfer and system costs. [S15; AF06]

The source is a dated Sharaf DG marketplace listing for a 24-inch FHD HDMI monitor, seller ENGAGE, including VAT. It is not a KU quote or evidence that used monitors are equivalent. Confirm condition, remaining life, specification and the purchase that would otherwise happen. Reuse that already occurs adds no incremental benefit.

Equation: E5  B = N × P      C = F + N × V      Net benefit = B − C

Project accounting model adapted from [S16]. N=extra purchases avoided/year; P=comparable purchase price; V=extra handling cash/item; F=fixed first-year cash costs. Count each cost once.

Equation: E6  Cash ROI (%) = 100 × (B − C) / (C)

ROI method [S16], for C>0. This example covers included cash costs only; full KU economic ROI remains unestablished.

| Extra purchases N | Gross B AED | Included C AED | Net AED | Partial cash ROI |
| --- | --- | --- | --- | --- |
| 0 | 0.00 | 1,304.43 | -1,304.43 | -100.0% |
| 4 | 1,380.00 | 1,404.43 | -24.43 | -1.7% |
| 8 | 2,760.00 | 1,504.43 | 1,255.57 | 83.5% |

Sensitivity assumptions: P=345 [S15], V=25 [AF11], F=1,304.43 [AF01–10]. N=0, 4 or 8 [AF12] are deliberate cases, not a KU forecast. The full reserve is treated as spent. Taxes, fees and unpriced labour can change these results.

Equation: E7  Included-cost break-even = ceiling(F / (P − V)) = 5 extra purchases

Derived from E5 by setting net benefit to zero, for P>V. This threshold applies only to the stated partial cash model, not to full university adoption.

## Staff capacity remains a separate benefit

Equation: E8  Released hours = (Baseline active minutes − Proposed active minutes) / 60

Team measurement definition for the same period and workload. Proposed minutes include all roles, failed cases, checking, correction, duplicate entry, setup, training and extra administration. Waiting is separate. No measured inputs are yet available.

A release of staff hours does not automatically reduce spending. Do not add both staff-time value and the same avoided wage cost to benefits. Obtain the two interviews and a workflow trial before reporting a realised saving.

# 10  Schedule resources and legal constraints

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

At the midpoint, 180 hours plus 15% reserve is 207 hours: 15 more than the 192-hour scenario. The range therefore does not yet establish schedule feasibility. Review estimates with each owner, reuse proven components and sequence dependencies before committing to implementation.

| Order | Dependency and exit check |
| --- | --- |
| First | Confirm workflow, evidence access and acceptance criteria. Complete the small stack/AI check. |
| Then | Build inventory and permissions before requests, approvals and custody. Add life-cycle records and AI against the stable baseline. |
| Before demonstration | Finish persistent uploads, hosted deployment, all required AI families, fallback, tests and documentation. Any scope change needs instructor agreement. |

## Legal ethical and university policy checks

Confirm asset ownership, release/receipt authority, finance/procurement thresholds, safe handling, data permission, provider terms and software licences. Use synthetic data until access is authorised. Do not send sensitive fields to an AI provider by default. Keep human approvals and record-based explanations. These are required checks, not a claim of legal or KU policy approval. [S01, S19]

# 11  Quantified risk assessment

Use a team-defined 5 × 5 likelihood–impact matrix for the remaining semester. NASA supports assessing, assigning, treating and reviewing software risks; our scores and cut-offs are planning judgments, not NASA-mandated values. [S17]

Equation: E9  Priority score = Likelihood rating × Impact rating

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

Equation: E10  Expected cash loss = Event probability × Cash impact

Quantitative method [S18] for a defined scenario and period. We do not calculate it because defensible probabilities and loss amounts are unavailable. A score of 12 is not 12%, AED 12 or expected loss.

# 12  Mitigation and contingency plan

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

# 13  Feasibility recommendation and next steps

Recommendation: proceed with a supervised semester prototype, with conditions. A real KU rollout is not yet justified. Continue the investigation and resolve the conditions below before claiming that the complete service is feasible.

| Area | Current conclusion | Condition for proceeding |
| --- | --- | --- |
| Technical | Plausible design, untested implementation | Demonstrate the small stack, persistence and hosted workflow. |
| Economic | Illustrative cost/benefit model only | Validate incremental demand, full costs and comparable institutional prices. |
| Legal and ethical | Relevant checks identified | Confirm permitted data, approval authority, provider terms and licences. |
| Operational | Workflow proposed, KU baseline unknown | Complete two interviews and count full-task effort. |
| Schedule | Capacity could be exceeded | Agree availability and a work plan that includes every required function. |
| Data and AI | Test design exists, results pending | Obtain suitable permitted/labelled data and meet evaluation and control checks. |

TELOS covers Technical, Economic, Legal, Operational and Schedule; the course separately requires data and AI. This framework structures our feasibility assessment. [S01, S22]

## Who finishes what

| Owner | Next deliverable |
| --- | --- |
| Sultan | Hosting test inputs, full cost/benefit calculation, agreed workload and consolidated risk register. |
| Zayed | Three-system comparison, two interviews, KU owner/workflow evidence, operational/legal findings and integration. |
| Ghaith | Stack/AI investigation, labelled trial, technical controls and recommendation draft with the team. |

The team should agree the final recommendation from the evidence. If costs, capacity or controls fail the conditions, revise the plan and explain the changed decision. Confirm the submission day next week before replacing relative milestones with dates.

# 14  Assumptions quality and AI use

Assumptions are planning choices made for this draft. They are not external statistics, KU measurements or approved commitments. Check them before relying on the calculations.

| ID | Input | Status or purpose |
| --- | --- | --- |
| AF01 | One year, 12 months | Comparison horizon, not semester duration |
| AF02–05 | 0.5 GB RAM; 0.05 vCPU; 1 GB volume; 1 GB/month egress | Combined app/database planning use, replace after testing |
| AF06 | Two monitors | Illustrative request, not measured KU demand |
| AF07–09 | USD 10/month AI; USD 5/month files/backups; AED 200 setup | Proposed cash caps/allowance, not quotes or approved spending |
| AF10 | 15% reserve, fully spent in the model | Planning convention, not expected loss |
| AF11 | AED 25 handling per monitor | Unmeasured extra cash materials/handling, excludes staff time |
| AF12 | 0, 4 or 8 extra purchases avoided/year | Sensitivity cases, not a forecast |
| AS01 | 8 weeks; 3 members; 8 hours/member/week | Capacity scenario, member availability/deadline unconfirmed |
| AS02 | Task effort ranges and 15% effort reserve | Initial team planning estimates from scope, need owner review |

## Document consistency and review

Use one scenario, scope, role definition and calculation set in the report and deck. Keep sources and dates beside claims. Label sourced facts, assumptions, targets and results. Sultan checks arithmetic and layout; Zayed checks stakeholder evidence and integration; Ghaith checks technical and AI claims. All three review the recommendation. Review the final rendered pages and slides before submission.

## AI use statement

Claude and OpenAI Codex assisted with drafting and revising project text, reviewing consistency against the supplied course documents, and preparing the documents and slides. Codex also assisted with finding official sources, constructing the explicitly labelled calculation examples, and preparing this expanded revision. The workflow illustration and provisional logo were generated using an AI image tool. AI assistance is not stakeholder evidence: interviews, KU procedures and realised benefits require separate records. Proposed figures and targets are labelled until validated. The named student team remains responsible for checking the submission and explaining its contents; members should add any other tools or uses relevant to their contributions.

# References 1

External pages checked 22 September 2026. Click a source title to open its original page. Source IDs beside claims and equations match this list. Course and team criteria are distinguished from external evidence.

[S01  COSC336 course project description](https://github.com/duqins/ITS/blob/main/docs/reference/Project-September2026.pdf)

Page 7: six feasibility areas; page 5: classic and AI comparison.

[S02  Group 4 Phase 1 scope and success criteria](https://github.com/duqins/ITS/blob/main/docs/phase1/sections/07-success-criteria.md)

Team-defined prototype targets, not achieved results. Scope: https://github.com/duqins/ITS/blob/main/docs/phase1/sections/02-project-overview.md . Effort and budget: https://github.com/duqins/ITS/blob/main/docs/phase1/sections/08-project-plan.md .

[Additional source page](https://github.com/duqins/ITS/blob/main/docs/phase1/sections/02-project-overview.md)

[Additional source page](https://github.com/duqins/ITS/blob/main/docs/phase1/sections/08-project-plan.md)

[S03  KU ISO certificates](https://www.ku.ac.ae/iso-certificates)

Lists asset management under Facilities Management; supports a proposed owner, not confirmed software ownership.

[S04  Rheaply internal reuse](https://rheaply.com/internal-reuse/)

Vendor-described marketplace, inventory, approvals and impact reporting.

[S05  Rheaply AI suggestions](https://support.rheaply.com/en/articles/7967928-use-ai-powered-suggestions-to-create-and-backfill-listings)

AI-assisted listing details with human review.

[S06  Warp It product tour](https://www.warp-it.co.uk/portal/warpit/tour)

Vendor-described reuse workflow and reports; homepage https://www.warp-it.co.uk/ describes AI photo-based listing.

[Additional source page](https://www.warp-it.co.uk/)

[S07  Snipe-IT product and pricing](https://snipeitapp.com/product)

Inventory/custody, requests, history, permissions and API. Pricing: https://snipeitapp.com/pricing .

[Additional source page](https://snipeitapp.com/pricing)

[S08  UC Berkeley Rheaply showroom](https://property.berkeley.edu/surplus/campus/rheaply-online-showroom-inventory)

Institutional use elsewhere supports relevance, not KU demand or savings.

# References 2

External pages checked 22 September 2026. Click a source title to open its original page. Source IDs beside claims and equations match this list. Course and team criteria are distinguished from external evidence.

[S09  Django overview and authentication](https://www.djangoproject.com/start/overview/)

Framework facilities; permissions: https://docs.djangoproject.com/en/stable/topics/auth/default/ . Department/item rules still need application code.

[Additional source page](https://docs.djangoproject.com/en/stable/topics/auth/default/)

[S10  PostgreSQL overview](https://www.postgresql.org/about/)

Relational database candidate. Proposed stack remains untested.

[S11  Railway pricing and billing](https://docs.railway.com/pricing)

Rates and Hobby minimum. Billing: https://docs.railway.com/pricing/understanding-your-bill .

[Additional source page](https://docs.railway.com/pricing/understanding-your-bill)

[S12  Render free services](https://render.com/docs/free)

Idle sleep and nonpersistent local files. A lasting upload store is still required.

[S13  Neon official plan documentation source](https://github.com/neondatabase/website/blob/main/content/docs/introduction/plans.md)

Free allowances: 0.5 GB storage, 100 CU-hours and 5 GB public transfer per project/month.

[S14  CBUAE reference exchange rates](https://centralbank.ae/umbraco/Surface/Exchange/GetExchangeRateAllCurrency)

Table updated 21 September 2026: USD 1 = AED 3.6725. Reference rate, not card fees.

[S15  Sharaf DG Samsung S3 S33GF monitor listing](https://uae.sharafdg.com/product/samsung-s3-s33gf-essential-fhd-monitor-24inch-ls24f330eamxue/)

22 September 2026 listing: AED 345 incl. VAT, ENGAGE seller, 24-inch FHD with HDMI. Retail proxy, not KU quote. Delivery excluded.

[S16  NHS Measurement for Improvement and Return on Investment](https://www.england.nhs.uk/improvement-hub/wp-content/uploads/sites/44/2017/11/2010-Measurement-for-Improvement-and-ROI.pdf)

Printed page 26: ROI = net benefits / costs x 100. Project inputs are separate assumptions.

# References 3

External pages checked 22 September 2026. Click a source title to open its original page. Source IDs beside claims and equations match this list. Course and team criteria are distinguished from external evidence.

[S17  NASA Software Engineering Handbook SWE-086](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695470/SWE-086%2B-%2BContinuous%2BRisk%2BManagement)

Risk assessment, owners, mitigation, triggers and continuing review. Our numeric rubric is a team adaptation.

[S18  NIST IR 8286Ar1](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=933223)

Printed pages 55–56 and 59: probability and monetary impact support quantitative risk exposure. Ordinal scores are not probabilities.

[S19  NIST AI RMF Playbook Measure](https://airc.nist.gov/airmf-resources/playbook/measure/)

Context-specific metrics, limitations and corrective action; no prescribed sample sizes here.

[S20  Introduction to Information Retrieval ranked evaluation](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html)

Ranked retrieval evaluation background. Our request-level Hit@3 is a stated operational definition.

[S21  scikit-learn zero one loss](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.zero_one_loss.html)

Normalised zero-one loss is the fraction of misclassifications.

[S22  Act on Heat TELOS workflow](https://actionheat.eu/workflow-step-8)

Technical, economic, legal, operational and scheduling framework; data/AI added separately by course.

[S23  Warp It UK pricing](https://www.warp-it.co.uk/portal/warpit/pricing)

Published UK bands are not a KU quotation; confirm local eligibility and taxes before cost comparison.

## Source and calculation rules

Provider pages support advertised capabilities and rates, not measured performance. The monitor price is a dated retail proxy. AF/AS assumptions come from the planning model. Equations E1–E3 and E8–E10 identify their method or operational definition; E4–E7 identify sourced inputs and derived arithmetic. No external statistic is used as evidence of an achieved KU benefit.

## Visual attribution

Dawra Campus logo: provisional AI-generated concept. Monitor-transfer illustration: AI-generated explanation of the proposed scenario. Neither image is an official KU mark, a photograph of KU activity or a screenshot of an implemented application. Creation prompts are retained with the project assets.
