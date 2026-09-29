# Dawra Campus Phase 2 Feasibility Study

Dawra Campus is our student project brand at Khalifa University.

| Prepared by | Student ID |
| --- | --- |
| Sultan Almheiri | 100065654 |
| Zayed Alfadli | 100064657 |
| Ghaith Alhinaai | 100066185 |

29 September 2026   Phase 2 submission

## Recommendation

Proceed with the academic prototype using reusable software components, subject to the stated checks. The monitor scenario shows possible cash savings, but including development and support time prevents recovery within three years. It therefore does not yet justify a custom live KU rollout. Validate the current process and compare an existing product before an adoption decision.

## What this report establishes

This report presents the proposed scope, stakeholder needs, market research, technology choices, costs, benefits, ROI, payback and risks. It addresses the instructor’s additional notes and all six course feasibility areas. The report combines desk research, scenario calculations and two AI role-play interviews. The interviews explore stakeholder needs as a classroom exercise; they are not evidence from KU employees. Technical implementation and measured outcomes remain to be tested. [S01]

| Evidence status | Meaning in this report |
| --- | --- |
| Sourced | A cited official page or course document supports the statement. Vendor claims have not been independently tested. |
| Assumed or proposed | A planning input, target or design choice to validate. AF, AR and AS identifiers trace numerical assumptions. |
| Simulated interviews | Two AI role-play conversations on 29 September 2026, used to explore needs and refine proposed requirements. |
| Not yet measured | The actual KU workflow, demand, staff timings, AI results and live deployment performance. |

# Report guide

Dawra Campus is our proposed brand for a website that helps university staff find usable spare items, approve their transfer and maintain an asset record. The full project also includes maintenance, retirement, sustainability reports and AI support. The monitor example makes the analysis concrete without replacing that wider scope.

| Read this part | What it answers | Review lead |
| --- | --- | --- |
| Sections 1 to 5 | Who are we serving, what is in scope, and what do existing systems and university reports show? | Zayed |
| Sections 6 to 9 | What will we reuse and build, and how will we check the technology and AI? | Ghaith |
| Sections 10 to 13 | What costs repeat, what benefits could occur, and when could the investment be recovered? | Sultan |
| Sections 14 to 17 | How will we measure work, plan the schedule and manage risks? | Zayed and Sultan |
| Sections 18 to 20 | What is our recommendation, what assumptions need checking, and how did we use AI? | All members |

## Terms used in this report

| Term | Plain meaning |
| --- | --- |
| Nonrecurring cost | A one-time cost to prepare and start the system. |
| Recurring cost | A cost that continues while the system operates. |
| Baseline | What would happen using the current process without the new system. |
| Incremental benefit | An improvement caused by the new system beyond what already happens. |
| ROI | Net benefit divided by the included costs, shown as a percentage. |
| Payback | How long net benefits take to recover the initial investment. |
| Time value | An assumed value for hours used; it is not necessarily money paid. |

S identifiers point to references. AF, AR and AS identifiers mark our assumptions. Targets describe planned tests, while results require recorded measurements. All financial amounts are AED unless another currency is shown.

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

The proposed needs below combine the course scope, Phase 1 analysis and the simulated interviews in section 3. Actual KU policy and staff acceptance still need confirmation before a live service. [S01, S02]

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

## Public evidence for responsibilities

KU Procurement and Contracts describes purchasing responsibilities that include IT, laboratory equipment, maintenance and furniture. This supports involving Procurement in purchasing rules and comparable prices. The environmental sustainability policy assigns waste and recycling responsibilities to EHS. EHS is a consultation stakeholder alongside the sustainability role, rather than an additional system role. These public responsibilities do not establish staff approval of our proposal. [S35, S36]

# 3  Scenario and operational evidence

Proposed case: a staff member needs two working monitors with suitable connections. Another university unit has compatible spare monitors. This is an example, not an observed KU transaction. Quantity two is assumption AF06.

Concept illustration: request, find suitable spares, obtain release and receipt approval, record handover. The image represents a proposed workflow, not a working application.

| Stage | Proposed action and evidence |
| --- | --- |
| Request and search | Record purpose, connection, quantity and date. Check eligibility before offering a match. |
| Approval | Releasing and receiving staff approve. Apply additional policy approvals where required. |
| Handover | Confirm condition, quantity, new location and custody. Record who did what and when. |
| Measure | Count all staff’s active minutes, review, corrections and duplicate entry. Record waiting separately. |

The following two interviews use AI to act as hypothetical stakeholders, following the classroom role-play approach described by our instructor. We used the answers to refine the proposed workflow. No KU employee was interviewed, and the answers do not verify KU procedures or financial inputs.

# 3A  Simulated interview with an asset coordinator

Date: 29 September 2026. This classroom exercise uses AI role-play as a fictional procurement and asset coordinator, following the instructor permission reported by the team. No real KU employee participated. Answers explore a plausible workflow and do not establish current KU practice.

## How would you start a reuse request

Simulated answer: I would check what the department actually needs, then ask the custodian whether a suitable spare is available and can be released. An item appearing in a list does not tell me whether someone still needs it or whether its condition has changed.

Design implication: Show current availability and the responsible custodian, then require release approval before transfer.

## What information would you need about an item

Simulated answer: I need its asset ID, location, quantity, condition and technical details. I also need to know who checked the record and when. A photograph helps identify the item, but I would still ask for a condition check before accepting equipment.

Design implication: Record verification dates and inspection evidence, and flag missing information for review.

## Who should approve and record the transfer

Simulated answer: The releasing and receiving departments should confirm it, with any Finance or Procurement checks required by the actual policy. After handover, I would want a receipt confirmation and an updated custody record. Otherwise, the website and the main register could disagree.

Design implication: Preserve approval responsibilities and record handover, receipt and any required updates to existing records.

## What might create extra work for staff

Simulated answer: Entering the same details twice would be frustrating. We could also spend extra time checking old listings or correcting AI suggestions. I would compare the complete task, including those checks, rather than assuming a faster search means less work overall.

Design implication: Measure repeated entry, review and corrections across all staff involved, with waiting time reported separately.

## When would you accept a savings claim

Simulated answer: I would need evidence that reuse replaced a genuine purchase, a comparable price and the extra handling costs. I cannot confirm annual demand or savings through this exercise. The report's 40 purchases and 4, 8 or 12 avoided purchases remain assumptions.

Design implication: Keep financial assumptions labelled and count benefits only from documented additional reuse, after attributable costs.

# 3B  Simulated interview with a department requester

Date: 29 September 2026. AI plays a fictional department or laboratory requester in this classroom exercise, following the instructor permission reported by the team. No real KU employee participated. The scenario explores proposed user needs and does not demonstrate staff acceptance or measured performance.

## What would you need from the website

Simulated answer: I need two working monitors for existing computers before a planned lab activity. I would enter the connections, quantity, required date and location. I want to see useful details immediately, without repeated enquiries.

Design implication: Combine a plain language request with clear fields for specifications, quantity, condition, location and date.

## How would you choose between suggested items

Simulated answer: I would check the connections, condition and availability first. Finding an item called a display when I searched for a monitor would help. But I want the system to explain why it fits and flag anything that still needs checking.

Design implication: Use semantic search with mandatory eligibility checks and explanations that show missing information.

## What should happen after you select an item

Simulated answer: I would submit a request and expect a clear status, such as waiting for approval or ready for handover. Choosing an item should not promise it to me before the releasing unit agrees. If I cancel, I want to know the cancellation was recorded.

Design implication: Separate selection, reservation and approval, keep status clear, and prevent duplicate allocation.

## How should the assistant handle your request

Simulated answer: It could help draft my request, but I want to see the exact fields before anything is submitted. I should be able to correct or cancel them. If AI stops working, keep what I typed and let me finish through ordinary search and forms.

Design implication: Require confirmation, preserve access controls and entered information, and test classic fallback.

## What would make you comfortable using it

Simulated answer: A short demonstration, a simple guide and someone to contact would help. I would report unclear messages and repeated typing. If there is no suitable item, tell me clearly so I can discuss the next step with the responsible person.

Design implication: Provide user support and honest no-match messages, then record difficulties and repeat affected trial tasks.

# 3C  Operational requirements and adoption

The simulated interviews identify design needs rather than observed problems at KU. We link each proposed requirement to the role-play answer so the reason for it is clear. The course scope continues to control which features must be delivered. [S01, S02]

| Interview input | Proposed requirement | Acceptance evidence |
| --- | --- | --- |
| Coordinator needs verified availability | Show condition, quantity, custodian and last verification date; reserve approved quantities | Test an unavailable item and simultaneous requests without over-allocation |
| Coordinator needs accountable decisions | Separate release and receipt approval; record actor, time and decision | Pass authorised and unauthorised approval tests |
| Requester needs suitable items | Filter connection, condition, quantity and availability before ranking | Run matching and no-suitable-item cases |
| Requester needs a clear next step | Show status and the responsible role; retain normal search during AI failure | Complete the request and fallback tasks |
| Both roles need reliable records | Record handover and identify any required reconciliation with the existing register | Walk through one complete transfer and check the audit history |

## Proposed adoption and staff support

Begin with a supervised trial. Demonstrate requests, approvals, reservations and handover to requesters, custodians and department representatives, supported by a short task guide. Maintenance, Procurement and Sustainability representatives would review the steps that affect their responsibilities.

A designated support contact would record help requests, misunderstood statuses, repeated entry and failed tasks. Separate interface problems from unresolved policy questions. Revise the affected workflow and repeat the task before recommending wider use.

Operational feasibility remains conditional: the design is understandable in role-play, but only an authorised trial can establish staff acceptance and a lower total workload. Record all roles, corrections and duplicate entry when comparing the current and proposed process.

# 4  Market analysis and alternatives

Our target users are KU staff who request, manage, approve and maintain assets. The size of their unmet need is not yet known. Permitted records and later staff validation would establish request volumes, existing reuse and remaining gaps. The simulated interviews explore needs but cannot measure demand. We do not infer a market-size or savings statistic from the assignment.

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

## Local relevance

KU describes work on reducing, reusing and recycling waste, and Procurement identifies sustainability as a purchasing concern. This supports investigating reuse locally. It does not quantify unmet requests or prove demand for another application. Compare requests and suitable surplus for the same period, excluding demand already satisfied by existing reuse. [S35, S37]

# 5  Reuse evidence and the KU comparison

University reports show that organised reuse can avoid purchases. They establish a useful comparison, but they do not establish the amount KU could save or the net return from our software.

| University source | Reported result | How we use it |
| --- | --- | --- |
| Bristol 2025 annual report [S26] | Nearly 800 office-furniture items reused; estimated GBP 92,000 avoided purchase cost. | Supports the purchase-avoidance mechanism. Costs and item mix differ from our pilot. |
| Liverpool first-year report [S27] | GBP 300,442 reported savings in the first 12 months, including 1,732 furniture items reused. | Shows that staff, storage, transport and IT support matter alongside software. |

These figures are university-reported estimates. We do not convert them into a KU saving percentage, divide them into a monitor price, or treat them as net software profit. Our 10%, 20% and 30% cases in section 11 are separate assumptions.

## Current KU process and proposed change

| Step | Current KU baseline to verify | Proposed Dawra Campus action |
| --- | --- | --- |
| Find stock | Where staff search, who holds records and what is already visible | Search authorised spare-item records by condition, connection, quantity and availability |
| Approve reuse | Required release, receipt, finance and procurement checks | Show the same authorised checks and record each decision |
| Update records | Current asset system and any repeated entry requirements | Record custody and reconcile with required existing records |
| Measure value | Purchases still needed after current reuse, staff minutes and handling costs | Count only additional avoided purchases and the whole change in effort |

The current KU product name and its features have not been verified. The comparison therefore identifies the questions and proposed changes without assuming KU lacks these functions. The simulated interviews provide a proposed comparison process; permitted records and authorised staff confirmation would be needed to establish the actual baseline. No direct integration with live KU systems is assumed.

## Existing institutional framework

KU publishes a procurement portal and links the Abu Dhabi Procurement Standards. This establishes an existing procurement framework, but it does not identify the internal surplus-asset register, its search features or KU transfer-approval thresholds. Public procurement information cannot establish that a reuse marketplace is absent. Confirm the current system or form, responsible office and required record updates before claiming fewer steps. [S35, S38]

# 6  Technical feasibility

Selected candidate for validation: Django 5.2 LTS with server-rendered pages, PostgreSQL and a separate AI-service adapter. Use a currently patched release at implementation. [S33] Django supplies common web, authentication and permissions facilities; item/department access and approvals still require our own rules. PostgreSQL is a relational database candidate. These choices have not been tested by the team. [S09, S10]

| Option | Reason to consider it | Main trade-off |
| --- | --- | --- |
| Django pages and PostgreSQL | One application can cover forms, workflow and Python AI integration. | Team must confirm Python skills and implement a usable interface and item-level permissions. |
| Separate React interface and API | Useful if team familiarity and interface needs justify separate components. | More interface/API integration and deployment work. This is an architectural alternative, not a tested benchmark. |

## Hardware software and skills

| Resource | Proposed need | Feasibility check |
| --- | --- | --- |
| Development hardware | Existing student or KU lab computers, browser and internet | Run local database and application together; record actual machine limits. No new hardware purchase assumed. |
| Application resources | Web framework, relational database, source control, test tools and persistent uploads | Complete one request/approval transaction and restart without losing records. |
| AI access | Approved pretrained model/service, credentials and usage limits | Test classification, matching, cost and fallback. Candidate selected; access and suitability untested. |
| Skills | Web forms, SQL, permissions, APIs, tests and deployment | Each owner demonstrates a small task; plan time for any skill gap. |

## Technical decision gate

Before confirming the stack, complete a small test covering login, asset registration, an eligible search, separate approval, database persistence and AI failure. Measure resource use and confirm a working hosted route. A source-documented capability does not prove our implementation is feasible.

# 7  Reusing software components

We will reuse Django authentication, forms, administration and list views, and the PostgreSQL database. Their licences permit use subject to their conditions. We still implement our own asset workflow, department access, approvals, AI adapter and tests. Existing tools reduce foundation work; they do not supply KU policy. [S09, S10, S28, S29]

| Foundation work | Custom hours | Reuse hours | Hours avoided |
| --- | --- | --- | --- |
| Accounts and basic administration | 28 | 12 | 16 |
| Data forms and validation | 24 | 12 | 12 |
| Record lists and filters | 16 | 8 | 8 |
| Total | 68 | 32 | 36 |

AR01 engineering estimates compare the same behaviour. Reuse hours include configuration, adaptation and tests. All other work is held at 148 hours. These hour estimates are team assumptions, not figures published by Django.

Equation: E1  Project effort reduction = 100 × (216 − 180) / 216 = 16.7%

Derived from AR01–AR02: 148 + 68 = 216 custom-foundation hours; 148 + 32 = 180 hours with reuse. Capability evidence [S28] does not establish this percentage.

The one-time reduction is 36 base hours, or 41.4 hours with the same 15% reserve. At the assumed AED 30/hour time value, that is AED 1,242 of effort value avoided. It is not an annual cash saving. The existing 180-hour midpoint already includes reuse; do not subtract the 36 hours again.

## Provisional hosting and AI selection

Use Render plus Neon as the academic hosting candidate and test persistent uploads separately. Railway is the separately priced alternative. For matching, test hosted text-embedding-3-small; for category suggestions, the assistant, action explanations and report text, test gpt-4.1-mini-2025-04-14. Both require approved access, a budget and a data check. These are selected candidates, not completed integrations. [S11–S13, S30, S31]

Render free web services can sleep after 15 minutes without traffic and take about one minute to wake. Local files can be lost when the service restarts, redeploys or sleeps, so persistent uploads require a separate tested store. Check the hosted application after inactivity and restart, including records, images and permissions. Measure ordinary search latency and the first request after inactivity separately. Any change to Phase 1 performance criteria requires client agreement. Test a recovery method for both records and uploads. Hosting cold-start delay is separate from the 15-second AI fallback target inside an available application. [S12, S13]

A local MiniLM embedding model is an alternative, but needs its own memory and quality test. It does not provide all generative functions and is not assumed to fit the 0.5 GB hosting example. The zero-cash prototype plan needs permitted university API access or another validated option. No paid access is assumed to be free. [S02, S32]

# 8 Data and AI feasibility

| Data | Minimum information | Quality and access check |
| --- | --- | --- |
| Asset | ID, purpose/specification, condition, quantity, availability, location, custodian and verification date | Missing mandatory fields, duplicates and stale availability need correction. |
| Request and transfer | Need, constraints, dates, authorised requester, release/receipt approvals and handover | Preserve allowed roles and one authoritative reservation/status record. |
| Maintenance and end of life | Inspection, repair, costs, state, authorised action and supporting evidence | Do not infer safety or disposal permission from generated text. |
| Cost and sustainability | Comparable price, attributable costs, mass/factor where used, units and source date | Missing evidence produces N/A or a labelled estimate; no invented carbon savings. |

Start with synthetic data. Phase 1 proposes 500 assets, 10 departments and 50 requests, including 20 fixed eligible matching cases. These are test-design numbers, not KU inventory or demand. Add separate cases where no suitable asset exists. [S02]

## AI boundary and controls

- Classic code enforces access, availability, quantity and compatibility before ranking. AI suggests; authorised staff decide.
- Use pretrained models for classification, semantic matching, ranking, sustainable-action advice, assistant responses and summaries. The provisional hosted model choices in section 7 need access and performance checks. [S01, S02, S30, S31]
- Send only approved necessary fields to external services. Check retention, training use, location and permissions before real data. A default no-training setting does not mean zero retention or KU approval. [S34] Synthetic testing does not grant a live-data mandate.
- Keep normal search and forms available. Similarity scores are not automatically probabilities of correctness.
Data/AI feasibility remains conditional on suitable labelled records, service access, acceptable cost and repeatable evaluation. Document what cannot yet be measured. [S19]

# 9  Evaluation metrics and loss

Use the same asset snapshot and requests for ordinary and AI search. Two team members independently label suitable matches and correct asset categories, resolve disagreements and freeze both evaluation sets. Keep development examples separate. Ranked retrieval evaluation uses explicit relevance judgments. [S02, S20]

Equation: E2  Hit@3 (%) = 100 × (Σ h(q)) / (n)

Team operational definition informed by ranked evaluation [S20]. h(q)=1 if request q has a useful top-three result, otherwise 0; n is the eligible request count. A failed response counts as a miss.

Equation: E3  Top-three miss rate (%) = 100 − Hit@3 (%)

Derived complement of E2; an evaluation error rate, not neural-network training loss.

Equation: E4  Classification loss = (Wrong category predictions) / (Tested labelled assets)

Normalised zero-one loss [S21]. Missing or invalid predictions count as wrong. No custom-model training is proposed.

The 20 matching requests and 20 labelled assets are different evaluation sets. Hit@3 measures the share of requests with a useful top-three result, rather than the accuracy of every returned item. Keep failed AI responses in the matching denominator. Classic fallback success is recorded separately, never counted as an AI success.

# 9A  Planned acceptance checks

| Check | Cases | Target |
| --- | --- | --- |
| Useful matching | 20 eligible requests | At least 16 requests have a useful item in the first three results |
| Additional AI value | The same 20 requests with both search methods | At least two more successful requests than classic search |
| Classification | 20 labelled asset records | At least 16 correct categories; loss no more than 0.20 |
| Eligibility | Every actionable recommendation returned | Zero violations of mandatory eligibility or access rules |
| Human approval | 14 base scenarios | All authorised actions follow required approvals; all unauthorised attempts are blocked |
| AI fallback | Five failure scenarios | Classic controls available within 15 seconds of the attempted AI request, preserving user input |
| LLM assistant | Five request scenarios | Explicit confirmation before submission; cancellation causes no submission; access and required fields enforced |
| Explainability | 20 sampled recommendations | Reasons and confidence information, or an explicit statement that confidence is unavailable; record model information |
| Generative reporting | Five summaries | Facts traceable, totals match conventional reports, and relevant data owner reviews before official use |

These planned targets come from the Phase 1 success criteria [S02]. No technical results are claimed. For each trial, record the actual cases executed, prompts, model and version, errors, latency, usage cost and staff review time. Report unmet targets and limitations. A small synthetic trial cannot establish campus-wide savings or statistical significance. [S19, S20]

# 9B  Evaluation cases and boundaries

## Approval and failure cases

The 14 approval scenarios contain one authorised and one unauthorised case for each of seven actions: transfer, donation, recycling, disposal, repair spending, financial-value changes and user-role changes. If a scenario is executed through both the standard interface and a supported assistant route, record each execution separately.

The five AI failure cases are service unavailability, timeout, rate limit, malformed output and insufficient confidence. The five assistant cases are a confirmed request, a corrected request, cancellation, an unauthorised request and an incomplete request. These tests cover different behaviours and have separate results.

## Additional proposed Phase 2 coverage

| Proposed check | Cases | Expected behaviour |
| --- | --- | --- |
| No suitable asset | Five separate requests with no eligible asset | State that no suitable item is available; return zero ineligible actionable recommendations. Exclude these cases from the 20 eligible Hit@3 requests. |
| Sustainable action advice | Five assets with different conditions, demand and repair costs | Explain the action using available evidence, identify missing information and retain authorised human control. |

These additional case counts are proposed by the team. They extend coverage without replacing the Phase 1 targets. The sustainable-action checks cover the required AI advice, while the assistant and summary tests cover functions beyond matching and classification. [S01, S02]

## Fairness and recommendation acceptance

The course also requires fairness and recommendation acceptance to be evaluated [S01]. Compare Hit@3 and rejection reasons across synthetic departments and item categories, reporting each group’s case count so small samples are visible. Check equivalent requests with different department labels while retaining legitimate access rules. A gap prompts investigation of data, eligibility or ranking; this is not a claim of proven fairness. [S19]

Proposed acceptance measure: record how many AI suggestions a reviewer accepts out of all suggestions reviewed, together with reasons for rejection. Report the numerator and denominator; distinguish an accepted suggestion from a completed transfer. The team must agree coverage and acceptance thresholds before trials. No acceptance rate or fairness result has been measured.

## How to interpret a result

For example, 16 matching successes out of 20 eligible requests gives Hit@3 of 80% and a 20% miss rate. Four wrong categories out of 20 labelled assets gives classification loss of 0.20. These examples explain the equations; they are not observed results. A zero-error approval trial demonstrates only the cases tested and does not establish zero risk.

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

The financial case isolates monitors so that each saved purchase has a clear quantity and price. Other asset categories remain in project scope, but no unsupported benefit is credited to them. Start with a defined pilot and replace these inputs with permitted purchase records and actual observations before an adoption decision.

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

# 14  Benefits measurement and decision rules

The purchasing model is intentionally narrow. Measure other benefits separately before including them in ROI. The table explains the mechanism, the evidence and what is currently claimed.

| Potential benefit | Mechanism and measurement | Current treatment |
| --- | --- | --- |
| Purchase avoidance | A verified spare item fulfils a need that would otherwise require a new purchase. Record quantity, approval and comparable purchase price. | Quantified by the monitor scenarios only |
| Lower workload | Search and status visibility may reduce follow-up, but review, correction and duplicate entry add work. Compare the same complete request across all roles. | No saving percentage claimed until timed evidence exists |
| Software reuse | Framework components replace custom foundation work. Record integration, adaptation and test hours. | 36 base hours avoided in an explicit one-time estimate; already reflected in costs |
| Disposal and sustainability | Reuse may postpone waste and reduce impact. Record material, mass, useful life and a cited factor. | No cash or carbon benefit counted yet |
| Better records | Custody and decision history may reduce missing information. Count missing fields, unmatched records and correction tasks. | A proposed quality indicator, not a cash saving |

Equation: E14  Released hours = (Baseline active minutes − Proposed active minutes) / 60

Team measurement definition for the same period and workload. Include all roles, failed cases, AI checking, correction, duplicate entry, setup, training and ongoing administration. Record waiting time separately.

Count additional benefits and additional costs against the current process. A faster search does not prove a faster whole task. Released staff hours create capacity; they reduce cash only if a paid expense actually disappears. Never count the same hours as both capacity value and avoided wages. [S24]

## Evidence needed before replacing assumptions

Use the simulated interviews to refine questions and requirements. Confirm the actual baseline and ownership with authorised staff and permitted records before a live pilot. For a permitted pilot, log the item, original purchase need, accepted reuse, cost, staff minutes, failures and date. Keep the current process, classic search and AI search comparable. Record zero or negative outcomes as well as successful transfers.

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

Owner: Zayed. Mitigation: Use the two simulated interviews to refine requirements. Confirm the actual workflow, owner and permitted records before a live pilot.

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

# 18  Feasibility recommendation

Recommendation: continue the supervised academic prototype with reusable components and the selected technology candidates. A custom KU rollout is not justified by the monitor case alone: the base scenario has a three-year time-inclusive ROI of −35.23%. Compare configuration of an existing product and gather evidence for wider asset benefits before an institutional investment decision.

| Area | Current conclusion | Condition for proceeding |
| --- | --- | --- |
| Technical | Plausible design, untested implementation | Demonstrate the small stack, persistence and hosted workflow. |
| Economic | Cash case positive at 8 extra monitors; time-inclusive case fails three-year recovery | Validate demand and all costs; compare an existing system and wider asset benefits. |
| Legal and ethical | Relevant checks identified | Confirm permitted data, approval authority, provider terms and licences. |
| Operational | Workflow examined through two simulated interviews; actual KU baseline unverified | Confirm the real process and measure complete tasks in an authorised trial. |
| Schedule | Capacity could be exceeded | Agree availability and a work plan that includes every required function. |
| Data and AI | Test design exists, results pending | Obtain suitable permitted/labelled data and meet evaluation and control checks. |

TELOS covers Technical, Economic, Legal, Operational and Schedule; the course separately requires data and AI. This framework structures our feasibility assessment. [S01, S22]

## Team contributions and next validation

| Owner | Contribution and follow-up |
| --- | --- |
| Sultan | Financial and schedule analysis, benefit scenarios and consolidated risks. Next: validate costs, effort and capacity against records. |
| Zayed | Scope, stakeholders, market comparison, public KU evidence and operational/legal analysis. Next: validate the proposed workflow and ownership. |
| Ghaith | Technical design, reusable components, data, AI evaluation and technical risks. Next: run the planned checks and record results. |

Our joint recommendation is to continue the academic prototype subject to the conditions above. Reassess it if costs, capacity or controls fail their checks. The eight-week capacity calculation is a planning scenario; align implementation tasks with the confirmed course dates and each member’s availability.

# 19  Financial assumptions

Assumptions are planning choices made for this feasibility assessment. They are not external statistics, KU measurements or approved commitments. Check them before relying on the calculations.

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

# 20  Assumptions and AI use

| ID | Input | Status or purpose |
| --- | --- | --- |
| AR01 | 68 custom hours vs 32 integration hours for three components | Team engineering estimate; includes adaptation and tests |
| AR02 | 36 base hours avoided; 41.4 with 15% reserve | Already reflected in 180/207 hours, never subtracted twice |
| AS01 | Eight weeks, three members, eight hours/week | 192 hours of capacity, subject to availability/deadline confirmation |
| AS02 | 150–210 estimated hours; 15% effort reserve | 172.5–241.5 hours; 207-hour midpoint exceeds AS01 by 15 |

## Plain language summary of the result

In our base scenario, Dawra Campus prevents 8 extra monitor purchases a year. This is a 20% reduction in the assumed 40-purchase pilot baseline. After recurring cash costs, it leaves AED 1,485.57 a year. However, including the assumed value of development and support time produces a three-year loss of AED 4,503.28. This is useful evidence for a cautious decision; it is not a claim that KU has saved money.

## Document consistency and review

The report uses one scope, role definition and financial model across the team contributions. Sources and dates accompany factual claims, while assumptions and targets remain distinct from results. Sultan leads financial and risk analysis, Zayed leads stakeholder and market analysis, and Ghaith leads technical and AI analysis. A changed input must be reflected in the calculations, risk discussion and recommendation together.

## AI use statement

Claude and OpenAI Codex assisted with drafting, revising, source research, calculation examples and document preparation. AI also acted as the two hypothetical stakeholders in section 3, using the classroom role-play approach. Their answers are simulated and do not represent statements by KU employees or independent validation of the financial assumptions. An AI image tool generated the project logo and workflow illustration. Student contributions were reviewed through the team’s GitHub workflow. The named students remain responsible for checking the sources, calculations and submission, and for explaining their work. Proposed targets remain distinct from measured results.

# References 1

The financial/source baseline is dated 22 September 2026. KU sources S35 to S38 were added in the 28 September review; hosting and evaluation coverage were revised on 29 September. Prices are dated examples, not live quotations. Source IDs beside claims and equations match this list.

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

# References 2

The financial/source baseline is dated 22 September 2026. KU sources S35 to S38 were added in the 28 September review; hosting and evaluation coverage were revised on 29 September. Prices are dated examples, not live quotations. Source IDs beside claims and equations match this list.

[S08  UC Berkeley Rheaply showroom](https://property.berkeley.edu/surplus/campus/rheaply-online-showroom-inventory)

Institutional use elsewhere supports relevance, not KU demand or savings.

[S09  Django overview and authentication](https://www.djangoproject.com/start/overview/)

Framework facilities; permissions: https://docs.djangoproject.com/en/stable/topics/auth/default/ . Department/item rules still need application code.

[Additional source page](https://docs.djangoproject.com/en/stable/topics/auth/default/)

[S10  PostgreSQL overview](https://www.postgresql.org/about/)

Relational database candidate. Proposed stack remains untested.

[S11  Railway pricing and billing](https://docs.railway.com/pricing)

Rates and Hobby minimum. Billing: https://docs.railway.com/pricing/understanding-your-bill .

[Additional source page](https://docs.railway.com/pricing/understanding-your-bill)

[S12  Render free services](https://render.com/docs/free)

Idle sleep and nonpersistent local files. A lasting upload store is still required. Hosting limitations rechecked against the official Render documentation on 29 September 2026.

[S13  Neon official plan documentation source](https://github.com/neondatabase/website/blob/main/content/docs/introduction/plans.md)

Free allowances: 0.5 GB storage, 100 CU-hours and 5 GB public transfer per project/month.

[S14  CBUAE reference exchange rates](https://centralbank.ae/umbraco/Surface/Exchange/GetExchangeRateAllCurrency)

Table updated 21 September 2026: USD 1 = AED 3.6725. Reference rate, not card fees.

# References 3

The financial/source baseline is dated 22 September 2026. KU sources S35 to S38 were added in the 28 September review; hosting and evaluation coverage were revised on 29 September. Prices are dated examples, not live quotations. Source IDs beside claims and equations match this list.

[S15  Sharaf DG Samsung S3 S33GF monitor listing](https://uae.sharafdg.com/product/samsung-s3-s33gf-essential-fhd-monitor-24inch-ls24f330eamxue/)

22 September 2026 listing: AED 345 incl. VAT, ENGAGE seller, 24-inch FHD with HDMI. Retail proxy, not KU quote. Delivery excluded.

[S16  NHS Measurement for Improvement and Return on Investment](https://www.england.nhs.uk/improvement-hub/wp-content/uploads/sites/44/2017/11/2010-Measurement-for-Improvement-and-ROI.pdf)

Printed page 26: ROI = net benefits / costs x 100. Project inputs are separate assumptions.

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

# References 4

The financial/source baseline is dated 22 September 2026. KU sources S35 to S38 were added in the 28 September review; hosting and evaluation coverage were revised on 29 September. Prices are dated examples, not live quotations. Source IDs beside claims and equations match this list.

[S22  Act on Heat TELOS workflow](https://actionheat.eu/workflow-step-8)

Technical, economic, legal, operational and scheduling framework; data/AI added separately by course.

[S23  Warp It UK pricing](https://www.warp-it.co.uk/portal/warpit/pricing)

Published UK bands are not a KU quotation; confirm local eligibility and taxes before cost comparison.

[S24  GAO Cost Estimating and Assessment Guide](https://www.gao.gov/assets/d20195G.pdf)

GAO-20-195G (2020), printed pages 94–95: recurring/nonrecurring cost categories; page 123: double-counting checks. Our project amounts are assumptions.

[S25  NIST investment analysis guide](https://nvlpubs.nist.gov/nistpubs/ams/NIST.AMS.200-11.pdf)

Appendix A1.3, printed page 25 equation 7: simple payback from initial investment and uniform annual net inflow. Page 26 discusses limitations. Our inputs are scenarios.

[S26  University of Bristol Annual Report 2025](https://www.bristol.ac.uk/media-library/sites/finance/documents/UoB_ARFS2025_WEB.pdf)

Page 34 reports nearly 800 office-furniture items reused and estimated GBP 92,000 avoided purchase cost. This is university-reported gross avoidance, not KU savings or net system ROI.

[S27  University of Liverpool Warp It first-year results](https://www.liverpool.ac.uk/about/sustainability/news/stories/title,1545664,en.php)

Published 24 February 2026: GBP 300,442 reported savings in the first 12 months, including 1,732 furniture items reused. Storage, collection, delivery and IT support also contributed. No complete net-cost method is disclosed.

[S28  Django built-in application components](https://www.djangoproject.com/start/)

Official forms, authentication and administration facilities. Supports reuse availability, not our estimated hours.

# References 5

The financial/source baseline is dated 22 September 2026. KU sources S35 to S38 were added in the 28 September review; hosting and evaluation coverage were revised on 29 September. Prices are dated examples, not live quotations. Source IDs beside claims and equations match this list.

[S29  PostgreSQL and Django licence information](https://www.postgresql.org/about/licence/)

PostgreSQL permits use without a licence fee subject to its notice conditions. Django BSD licence: https://docs.djangoproject.com/en/5.2/faq/general/#how-is-django-licensed . Hosting and maintenance still cost resources.

[Additional source page](https://docs.djangoproject.com/en/5.2/faq/general/#how-is-django-licensed)

[S30  OpenAI GPT 4.1 mini model documentation](https://developers.openai.com/api/docs/models/gpt-4.1-mini)

Provisional text-model candidate gpt-4.1-mini-2025-04-14. Standard uncached text rates: USD 0.40 per million input tokens, USD 1.60 per million output tokens. Access and suitability untested.

[S31  OpenAI text embedding 3 small documentation](https://developers.openai.com/api/docs/models/text-embedding-3-small)

Provisional hosted semantic-search candidate. USD 0.02 per million input tokens. Token volume remains unmeasured.

[S32  Sentence Transformers all MiniLM L6 v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

Local English embedding alternative with Apache 2.0 licence. Requires separate loaded-memory, latency and quality tests; not assumed to fit 0.5 GB hosting.

[S33  Django supported release schedule](https://www.djangoproject.com/download/)

Django 5.2 LTS is the selected branch for a prototype trial. Official support table lists extended support through April 2028. Pin a current patched release at implementation.

[S34  OpenAI API data controls](https://developers.openai.com/api/docs/guides/your-data)

Default no training use does not mean zero retention or KU approval. Review actual account retention, permitted fields and location before using real data.

[S35  KU Procurement and Contracts Department](https://www.ku.ac.ae/about/procurement-and-contracts-department)

Public purchasing responsibilities, scope and procurement links. Added from the 28 September team review.

# References 6

The financial/source baseline is dated 22 September 2026. KU sources S35 to S38 were added in the 28 September review; hosting and evaluation coverage were revised on 29 September. Prices are dated examples, not live quotations. Source IDs beside claims and equations match this list.

[S36  KU Environmental Sustainability Policy EHS 7600](https://www.ku.ac.ae/sustainability/assets/attachments/EHS_7600_Environmental_Sustainability_Policy.pdf)

Sections 5.1.1 and 6 support EHS consultation on waste and recycling. Public policy is not evidence of acceptance of Dawra Campus.

[S37  KU sustainability initiatives](https://www.ku.ac.ae/sustainability/initiative)

Public reduction, reuse and recycling activity supports local relevance, not a measured demand or saving for our system.

[S38  Abu Dhabi Procurement Standards linked by KU](https://www.ku.ac.ae/wp-content/uploads/2025/01/Abu-Dhabi-Procurement-Standards.pdf)

Institutional procurement framework linked from S35. No inference is made about the name or functions of the internal KU asset system.

## Source and calculation rules

Provider pages support advertised capabilities and rates. University reports describe their own results, not KU performance. The monitor price is a retail proxy. AF, AR and AS assumptions are team planning choices. Each equation identifies its source method or team definition. No external report establishes our assumed percentages, staff timings or development hours.

## Visual attribution

Dawra Campus logo: AI-generated student project concept. Monitor-transfer illustration: AI-generated explanation of the proposed scenario. Neither image is an official KU mark, a photograph of KU activity or a screenshot of an implemented application. Creation prompts are retained with the project assets.
