# Dawra Campus Phase 2 technical feasibility, software reuse, data and ai

**Section review lead:** Ghaith Alhinaai  
**Student ID:** 100066185  
**Version:** 3.0, 22 September 2026

This section assesses the technical feasibility, software-component reuse, data requirements, AI evaluation and technical risks of Dawra Campus. Section and equation numbers follow the combined report supplied in the review package. The proposed technologies, effort estimates and evaluation targets remain subject to validation.

**Project:** Dawra Campus is our proposed brand for a KU staff website for approved asset reuse and life-cycle records. The academic prototype also includes maintenance, retirement, sustainability reporting, hosted deployment and AI support.

**Shared conclusion:** Continue the academic prototype subject to the stated conditions. The monitor case alone does not justify a custom live KU rollout once development and support time are counted. Two interviews, the current KU baseline and measured technical results remain pending.

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

A local MiniLM embedding model is an alternative, but needs its own memory and quality test. It does not provide all generative functions and is not assumed to fit the 0.5 GB hosting example. The zero-cash prototype plan needs permitted university API access or another validated option. No paid access is assumed to be free. [S02, S32]

### Hosting limitations to validate

Render's free web service can sleep after 15 minutes without incoming traffic and take about one minute to restart. Uploaded files stored on its local filesystem can also be lost during a restart or redeployment. These limits need explicit testing before confirming the hosting choice. [S12]

We will measure normal search response time and the first request after inactivity, reporting both results. Any change to the Phase 1 performance acceptance conditions must be agreed with the client rather than assumed.

We must also select and test persistent storage for uploaded photographs and documents. The validation must confirm that database records and uploaded files remain available after a restart or redeployment, with appropriate access controls and a documented recovery method. Hosting remains provisional until these checks pass.

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

All figures below are planned evaluation targets. No measured technical results are claimed.

The synthetic dataset contains a planned 500 assets, 10 departments and 50 requests. The matching evaluation will use a fixed subset of 20 requests for which suitable assets exist. Classification will use 20 labelled asset records; these are a different evaluation set from the 20 matching requests.

Two team members will independently label suitable matches and correct asset categories, resolve disagreements and freeze the evaluation sets before testing. Development examples will remain separate. Classic search and AI matching will use the same asset snapshot, requests and eligibility rules. [S02, S20]

## Metric definitions

Equation: E2  Hit@3 (%) = 100 × (Requests with at least one useful result in the first three positions) / (Eligible requests tested)

For the planned 20-request set, 16 successful requests gives Hit@3 = 80%. This measures request-level matching success, not the percentage of all returned items that are correct. A failed or invalid AI response counts as an unsuccessful request.

Equation: E3  Top-three miss rate (%) = 100 − Hit@3 (%)

A Hit@3 result of 80% therefore gives a miss rate of 20%. This is an evaluation error rate, not a neural-network training loss.

Equation: E4  Classification loss = (Incorrect category predictions) / (Labelled assets tested)

Missing or invalid predictions count as incorrect. For 20 labelled assets, four incorrect predictions give a classification loss of 0.20 and 16 correct predictions. No custom-model training is proposed. [S21]

## Planned acceptance checks

| Check | Planned cases | Target |
| --- | --- | --- |
| Useful matching | 20 eligible requests | At least 16 requests have a useful item in the first three results. |
| Additional AI value | The same 20 requests, tested with classic search and AI | AI succeeds on at least two more requests than classic search. For example, 14 classic successes would require at least 16 AI successes. |
| Classification | 20 labelled asset records | At least 16 correct categories; classification loss at most 0.20. |
| Eligibility | Every actionable recommendation returned during the matching tests | Zero recommendations violate mandatory eligibility or access rules. |
| Human approval | 14 base scenarios, defined below | All permitted actions follow the required approvals, and all unauthorised attempts are blocked. |
| AI fallback | Five failure scenarios, defined below | The relevant classic controls are available within 15 seconds of the attempted AI request, with user input preserved. |
| LLM assistant | Five request scenarios: confirmed, corrected, cancelled, unauthorised and incomplete | Proposed submissions require explicit confirmation; cancellation causes no submission; access and required-field checks remain enforced. |
| Explainability | 20 sampled recommendations | Every recommendation shows its reasons and confidence information, or explicitly states that confidence is unavailable. Required model information is recorded. |
| Generative reporting | Five generated summaries | Factual claims are traceable, numerical totals agree with conventional reports, and the relevant data owner reviews each summary before official use. |

These targets follow the Phase 1 success criteria. [S02]

The 14 approval scenarios consist of one authorised and one unauthorised case for each of seven actions: transfer, donation, recycling, disposal, repair spending, financial-value changes and user-role changes. Where a scenario is repeated through both a standard interface and a supported assistant route, each execution will be recorded separately.

The five fallback scenarios are service unavailability, timeout, rate limit, malformed output and insufficient confidence. Classic fallback success will be reported separately from AI matching success; a fallback response will not be counted as a successful AI result.

## Additional proposed Phase 2 coverage

The following case counts are proposals for team confirmation.

| Check | Proposed cases | Expected behaviour |
| --- | --- | --- |
| No suitable asset | Five separate requests for which no eligible asset exists | Explain that no suitable item is available and produce zero ineligible actionable recommendations. Report these cases separately from the 20 eligible requests used for Hit@3. |
| Sustainable-action advice | Five asset scenarios covering different conditions, demand and repair costs | Explain the proposed action using available evidence, identify missing information, and leave the final decision with the authorised human. |

The sustainable-action checks explicitly cover the AI advice described in Section 8 and the Phase 1 sustainable-action requirement. Assistant and reporting checks cover the other AI functions beyond matching and classification.

For each evaluation, record the actual number of cases executed, results, model/version, prompts, errors, latency, usage cost and staff review time. Report limitations and unmet targets. Small synthetic trials cannot establish campus-wide savings or statistical significance. [S19, S20]

# Technical risks

The shared risk register is in Sultan’s section. This section covers Ghaith's risks R2 and R3 and the technical aspects of R5, which Sultan owns. Scores are provisional ordinal priorities, not probabilities. Target scores require checked controls. [S17, S18]

## R2 AI recommends unsuitable items

Current score 3 × 4 = 12. Owner: Ghaith.

Mitigation: Filter eligibility before ranking. Freeze labels, check outputs and require staff review.

Trigger: Any ineligible actionable result or failure of the matching targets.

Contingency: Use classic search for task completion, investigate and retest AI. Keep the unmet requirement visible.

## R3 Restricted data or credentials exposed

Current score 3 × 5 = 15. Owner: Ghaith.

Mitigation: Synthetic data first, minimal fields, permission tests and protected secrets.

Trigger: Any unauthorised access, restricted prompt or exposed key.

Contingency: Stop the affected route, revoke keys and preserve relevant logs. Involve the authorised owner where applicable.

## R5 Hosting or AI limits interrupt work

Current score 3 × 3 = 9. Owner: Sultan.

Mitigation: Agree a spending cap. Measure usage and test storage, backup and fallback.

Trigger: Failed availability check or projected spend exceeds the approved cap.

Contingency: Recover or move to a tested option. A temporary local demo does not complete hosted deployment.



# Review and AI use

AI assisted the initial drafting, source research, calculations, document preparation and subsequent review. The student team remains responsible for understanding and checking the submitted claims, sources and calculations. The numerical examples are planning scenarios rather than measured KU results. Technical trials, stakeholder interviews and confirmation of the current KU process remain pending unless supported by separately recorded evidence.

# References used in this part

Source pages checked 22 September 2026. Source methods and capabilities do not establish our assumed workload, percentages or hours.

### S01 COSC336 course project description

[COSC336 course project description](https://github.com/duqins/ITS/blob/main/docs/reference/Project-September2026.pdf)

Page 7: six feasibility areas; page 5: classic and AI comparison.

### S02 Group 4 Phase 1 scope and success criteria

[Group 4 Phase 1 scope and success criteria](https://github.com/duqins/ITS/blob/main/docs/phase1/sections/07-success-criteria.md)

Team-defined prototype targets, not achieved results. Scope: https://github.com/duqins/ITS/blob/main/docs/phase1/sections/02-project-overview.md . Effort and budget: https://github.com/duqins/ITS/blob/main/docs/phase1/sections/08-project-plan.md .

### S09 Django overview and authentication

[Django overview and authentication](https://www.djangoproject.com/start/overview/)

Framework facilities; permissions: https://docs.djangoproject.com/en/stable/topics/auth/default/ . Department/item rules still need application code.

### S10 PostgreSQL overview

[PostgreSQL overview](https://www.postgresql.org/about/)

Relational database candidate. Proposed stack remains untested.

### S11 Railway pricing and billing

[Railway pricing and billing](https://docs.railway.com/pricing)

Rates and Hobby minimum. Billing: https://docs.railway.com/pricing/understanding-your-bill .

### S12 Render free services

Hosting limitations rechecked against the official Render documentation on 29 September 2026.

[Render free services](https://render.com/docs/free)

Idle sleep and nonpersistent local files. A lasting upload store is still required.

### S13 Neon official plan documentation source

[Neon official plan documentation source](https://github.com/neondatabase/website/blob/main/content/docs/introduction/plans.md)

Free allowances: 0.5 GB storage, 100 CU-hours and 5 GB public transfer per project/month.

### S17 NASA Software Engineering Handbook SWE-086

[NASA Software Engineering Handbook SWE-086](https://swehb.nasa.gov/spaces/SWEHBVD/pages/102695470/SWE-086%2B-%2BContinuous%2BRisk%2BManagement)

Risk assessment, owners, mitigation, triggers and continuing review. Our numeric rubric is a team adaptation.

### S18 NIST IR 8286Ar1

[NIST IR 8286Ar1](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=933223)

Printed pages 55–56 and 59: probability and monetary impact support quantitative risk exposure. Ordinal scores are not probabilities.

### S19 NIST AI RMF Playbook Measure

[NIST AI RMF Playbook Measure](https://airc.nist.gov/airmf-resources/playbook/measure/)

Context-specific metrics, limitations and corrective action; no prescribed sample sizes here.

### S20 Introduction to Information Retrieval ranked evaluation

[Introduction to Information Retrieval ranked evaluation](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html)

Ranked retrieval evaluation background. Our request-level Hit@3 is a stated operational definition.

### S21 scikit-learn zero one loss

[scikit-learn zero one loss](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.zero_one_loss.html)

Normalised zero-one loss is the fraction of misclassifications.

### S28 Django built-in application components

[Django built-in application components](https://www.djangoproject.com/start/)

Official forms, authentication and administration facilities. Supports reuse availability, not our estimated hours.

### S29 PostgreSQL and Django licence information

[PostgreSQL and Django licence information](https://www.postgresql.org/about/licence/)

PostgreSQL permits use without a licence fee subject to its notice conditions. Django BSD licence: https://docs.djangoproject.com/en/5.2/faq/general/#how-is-django-licensed . Hosting and maintenance still cost resources.

### S30 OpenAI GPT 4.1 mini model documentation

[OpenAI GPT 4.1 mini model documentation](https://developers.openai.com/api/docs/models/gpt-4.1-mini)

Provisional text-model candidate gpt-4.1-mini-2025-04-14. Standard uncached text rates: USD 0.40 per million input tokens, USD 1.60 per million output tokens. Access and suitability untested.

### S31 OpenAI text embedding 3 small documentation

[OpenAI text embedding 3 small documentation](https://developers.openai.com/api/docs/models/text-embedding-3-small)

Provisional hosted semantic-search candidate. USD 0.02 per million input tokens. Token volume remains unmeasured.

### S32 Sentence Transformers all MiniLM L6 v2 model card

[Sentence Transformers all MiniLM L6 v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)

Local English embedding alternative with Apache 2.0 licence. Requires separate loaded-memory, latency and quality tests; not assumed to fit 0.5 GB hosting.

### S33 Django supported release schedule

[Django supported release schedule](https://www.djangoproject.com/download/)

Django 5.2 LTS is the selected branch for a prototype trial. Official support table lists extended support through April 2028. Pin a current patched release at implementation.

### S34 OpenAI API data controls

[OpenAI API data controls](https://developers.openai.com/api/docs/guides/your-data)

Default no training use does not mean zero retention or KU approval. Review actual account retention, permitted fields and location before using real data.
