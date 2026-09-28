# Dawra Campus Phase 2 context, scope, stakeholders, market and operational feasibility

**Section review lead:** Zayed Alfadli  
**Student ID:** 100064657  
**Version:** 3.0, 22 September 2026
**Repository revision:** 28 September 2026
This file contains the completed analysis text for your assigned areas. Section and equation numbers follow the [combined report](../Phase2_Feasibility_Study.md). Review the claims, sources and assumptions, make your own corrections, and commit the reviewed file through your own account. The initial text was prepared with AI assistance; no member review is claimed yet.

**Project:** Dawra Campus is our proposed brand for a KU staff website for approved asset reuse and life-cycle records. The academic prototype also includes maintenance, retirement, sustainability reporting, hosted deployment and AI support.

**Shared conclusion:** Continue the academic prototype subject to the stated conditions. The monitor case alone does not justify a custom live KU rollout once development and support time are counted. Two interviews, the current KU baseline and measured technical results remain pending.

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

## Public evidence for stakeholder responsibilities

KU's Procurement & Contracts Department describes its role in obtaining goods and services with appropriate value and controls. It covers IT, laboratory equipment, maintenance and furniture. This supports involving Procurement in checking purchasing rules and comparable replacement costs. KU's environmental policy assigns waste-management and recycling responsibilities to EHS. EHS is therefore a consultation stakeholder alongside the proposed sustainability role; this does not add a tenth system role. These published responsibilities support stakeholder selection but do not constitute staff acceptance of Dawra Campus.

Sources checked 28 September 2026: [KU Procurement & Contracts](https://www.ku.ac.ae/about/procurement-and-contracts-department); [KU EHS 7600, sections 5.1.1 and 6](https://www.ku.ac.ae/sustainability/assets/attachments/EHS_7600_Environmental_Sustainability_Policy.pdf).

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

## Evidence collection for the current process

Zayed will use the following question set for the two planned interviews. The proposed collection window is 28 September to 2 October 2026, ahead of the Requirements Document week. Access and attendance remain unconfirmed.

| Participant | Questions and evidence requested | Requirement affected |
| --- | --- | --- |
| Asset custodian or Facilities/IT staff | Where are spare items recorded? How is condition checked? Who may release an item? Request a permitted blank form or anonymised process example. | Availability, inspection, release authority and custody records |
| Requester or department representative | How is a need submitted? Where does staff time or repeated entry occur? Who confirms receipt? Ask the participant to walk through one actual or clearly labelled hypothetical request. | Search fields, request status, receipt and usability |

Record answers, date, role, consent and supporting evidence, then link each accepted finding to a requirement or an unresolved question. Seek clarification from Procurement, Finance or EHS where an interviewee cannot confirm a rule. If access is unavailable, retain the pending status and distinguish classroom role-play from KU evidence. No interview findings are asserted in this addition.

## Proposed adoption and staff support

We propose a supervised trial before considering wider adoption. Requesters, asset custodians and department representatives would receive a short demonstration and a task guide covering requests, approvals, reservations and handover. Maintenance, Procurement and Sustainability representatives would review the parts of the workflow that affect their responsibilities.

The trial would record where participants need help, misunderstand a status, repeat data entry or cannot complete a task. A designated support contact would collect these issues and distinguish interface problems from unresolved policy questions. The team would revise the workflow and repeat affected tasks before recommending wider use.


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

## Evidence of local relevance and demand

KU's sustainability initiatives describe EHS and Facilities Management work on reducing, reusing and recycling waste. Procurement also identifies sustainability as a purchasing concern. This supports investigating reuse at KU, but does not quantify unmet requests or establish demand for another application.

Validate demand by comparing permitted requests and suitable surplus for the same period, excluding needs already met through existing reuse. Until these records and staff findings are available, demand remains unquantified and the monitor quantities remain scenarios.

Sources checked 28 September 2026: [KU sustainability initiatives](https://www.ku.ac.ae/sustainability/initiative); [KU Procurement & Contracts](https://www.ku.ac.ae/about/procurement-and-contracts-department).

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

The current KU product name and its features have not been verified. The comparison therefore identifies the questions and proposed changes without assuming KU lacks these functions. Two stakeholder interviews and permitted records should settle this. No direct integration with live KU systems is assumed.

## What public KU evidence establishes

KU publishes a procurement portal and links the Abu Dhabi Procurement Standards. The linked framework describes procurement responsibilities, controls and authorisation arrangements. This establishes an existing institutional procurement framework, but does not identify the internal surplus-asset register, demonstrate its search features or reveal KU's transfer-approval thresholds.

For the comparison above, retain the current system and approval route as unverified. Zayed will record the confirmed system/form name, responsible office, release and receipt steps, and required record updates from the section 3 evidence exercise. Compare Dawra Campus against that documented baseline before claiming fewer steps or less duplicate entry. Public procurement information alone cannot establish that a reuse marketplace is absent.

Sources checked 28 September 2026: [KU procurement portal](https://www.ku.ac.ae/about/procurement-and-contracts-department); [linked Abu Dhabi Procurement Standards, introduction and core principles](https://www.ku.ac.ae/wp-content/uploads/2025/01/Abu-Dhabi-Procurement-Standards.pdf).

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

Use the two interviews to confirm the baseline and ownership. For a permitted pilot, log the item, original purchase need, accepted reuse, cost, staff minutes, failures and date. Keep the current process, classic search and AI search comparable. Record zero or negative outcomes as well as successful transfers.

# Legal and ethical feasibility

Confirm asset ownership, release/receipt authority, finance/procurement thresholds, safe handling, data permission, provider terms and software licences. Use synthetic data until access is authorised. Do not send sensitive fields to an AI provider by default. Keep human approvals and record-based explanations. These are required checks, not a claim of legal or KU policy approval. [S01, S19]

# Review and AI use

AI assisted the initial drafting, source research, calculations and artifact preparation. You remain responsible for understanding and checking the text you commit. The calculations are planning scenarios, not measured KU results. Do not replace pending interviews or tests with invented records. Add any other relevant tool use and record your corrections during review.


# References used in this part

Source pages checked 22 September 2026. Source methods and capabilities do not establish our assumed workload, percentages or hours.

### S01 COSC336 course project description

[COSC336 course project description](https://github.com/duqins/ITS/blob/main/docs/reference/Project-September2026.pdf)

Page 7: six feasibility areas; page 5: classic and AI comparison.

### S02 Group 4 Phase 1 scope and success criteria

[Group 4 Phase 1 scope and success criteria](https://github.com/duqins/ITS/blob/main/docs/phase1/sections/07-success-criteria.md)

Team-defined prototype targets, not achieved results. Scope: https://github.com/duqins/ITS/blob/main/docs/phase1/sections/02-project-overview.md . Effort and budget: https://github.com/duqins/ITS/blob/main/docs/phase1/sections/08-project-plan.md .

### S03 KU ISO certificates

[KU ISO certificates](https://www.ku.ac.ae/iso-certificates)

Lists asset management under Facilities Management; supports a proposed owner, not confirmed software ownership.

### S04 Rheaply internal reuse

[Rheaply internal reuse](https://rheaply.com/internal-reuse/)

Vendor-described marketplace, inventory, approvals and impact reporting.

### S05 Rheaply AI suggestions

[Rheaply AI suggestions](https://support.rheaply.com/en/articles/7967928-use-ai-powered-suggestions-to-create-and-backfill-listings)

AI-assisted listing details with human review.

### S06 Warp It product tour

[Warp It product tour](https://www.warp-it.co.uk/portal/warpit/tour)

Vendor-described reuse workflow and reports; homepage https://www.warp-it.co.uk/ describes AI photo-based listing.

### S07 Snipe-IT product and pricing

[Snipe-IT product and pricing](https://snipeitapp.com/product)

Inventory/custody, requests, history, permissions and API. Pricing: https://snipeitapp.com/pricing .

### S08 UC Berkeley Rheaply showroom

[UC Berkeley Rheaply showroom](https://property.berkeley.edu/surplus/campus/rheaply-online-showroom-inventory)

Institutional use elsewhere supports relevance, not KU demand or savings.

### S19 NIST AI RMF Playbook Measure

[NIST AI RMF Playbook Measure](https://airc.nist.gov/airmf-resources/playbook/measure/)

Context-specific metrics, limitations and corrective action; no prescribed sample sizes here.

### S23 Warp It UK pricing

[Warp It UK pricing](https://www.warp-it.co.uk/portal/warpit/pricing)

Published UK bands are not a KU quotation; confirm local eligibility and taxes before cost comparison.

### S24 GAO Cost Estimating and Assessment Guide

[GAO Cost Estimating and Assessment Guide](https://www.gao.gov/assets/d20195G.pdf)

GAO-20-195G (2020), printed pages 94–95: recurring/nonrecurring cost categories; page 123: double-counting checks. Our project amounts are assumptions.

### S26 University of Bristol Annual Report 2025

[University of Bristol Annual Report 2025](https://www.bristol.ac.uk/media-library/sites/finance/documents/UoB_ARFS2025_WEB.pdf)

Page 34 reports nearly 800 office-furniture items reused and estimated GBP 92,000 avoided purchase cost. This is university-reported gross avoidance, not KU savings or net system ROI.

### S27 University of Liverpool Warp It first-year results

[University of Liverpool Warp It first-year results](https://www.liverpool.ac.uk/about/sustainability/news/stories/title,1545664,en.php)

Published 24 February 2026: GBP 300,442 reported savings in the first 12 months, including 1,732 furniture items reused. Storage, collection, delivery and IT support also contributed. No complete net-cost method is disclosed.
