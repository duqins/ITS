# Sultan's Phase 1 speaking guide

## Rehearse this way

1. Read **“Understand your story”** once. Explain the chair example aloud without looking at the page.
2. Practise only your slides: **1, 2, 3 and 7**. Use the short script as a starting point, then say the ideas naturally.
3. Run the presentation with the team and a timer. Your script takes about two minutes; leave the remaining 30 seconds for pauses, pointing to the slide and handoffs. Your total speaking allowance is **2 minutes 30 seconds**.

### Five-minute team timing

| Slide | Title | Speaker | Time |
|---|---|---|---|
| 1 | Campus Resource Exchange | Sultan | 15 seconds |
| 2 | The reuse problem | Sultan | 35 seconds |
| 3 | The proposed service | Sultan | 45 seconds |
| 4 | What Phase 1 established | Zayed | 55 seconds |
| 5 | Classic functions and AI support | Ghith | 55 seconds |
| 6 | Proposed success targets | Ghith | 40 seconds |
| 7 | Delivery plan | Sultan | 55 seconds |
| **Total** | | **Team** | **300 seconds / 5 minutes** |

Your part covers **Sections 1, 2 and 8** of the report: the problem, proposed service, scope and project plan. Let Zayed and Ghith explain their detailed analysis and requirement tables.

## Understand your story

### 1. The problem — why this project exists

The assignment describes departments buying equipment while similar usable items sit idle elsewhere. The gap is visibility and coordination: people cannot easily see available items, request them, approve a transfer, or track the outcome.

Remember three questions: **What exists? Who needs it? What should happen next?** They connect your introduction to the proposed features. This is the course scenario and an initial analysis; we have not yet verified the university's internal practices through stakeholder interviews.

### 2. The proposed service — how it helps

An asset is registered, published when available, found by another department, requested, approved and transferred. Its location, custodian and maintenance history remain recorded. Reports would show reuse activity and estimated benefits.

Classic rules handle permissions, stock quantities, reservations and approvals. AI helps interpret wording, suggest categories, rank suitable assets and draft summaries. A request for “seating” could find a listing called “office chairs.” The chairs must still meet quantity, condition and other constraints. AI recommends; authorised people decide.

### 3. Scope — what we promise to build

The intended scope includes the marketplace, requests, approvals, transfers, maintenance, AI services, sustainability reporting, and **hosting and deployment**. Hosting means the application will be accessible to intended users and reviewers through a documented HTTPS address.

Outside this semester's scope are live university finance/ERP integrations, purchases or payments, physical delivery systems or RFID hardware, training our own models from scratch, and native mobile apps.

“Should have” means planned after the initial Must-have baseline. Hosting, the assistant and sustainable-action recommendations are Should-have priorities **within scope**. A proposed course-scope deferral needs instructor agreement.

### 4. The plan — how three students make progress

We use short cycles: plan a small piece, do it, review it and adjust. Course phases still set the main milestones. This lets us test uncertain choices, such as AI access and hosting, early.

The sequence is **plan → feasibility → detailed requirements → design → implementation and deployment → testing and final demonstration**. Phase 2 checks the stack, hosting and AI service. Phase 6 includes an initial hosted deployment. The final phases check the deployed application, document its setup and demonstrate it. The course documents give conflicting dates, so the exact calendar still needs instructor confirmation.

You coordinate the project and lead planning and backend/integration work. Ghith leads AI, architecture and deployment; you support deployment configuration and integration. Zayed leads requirements, user experience and testing. Each member commits their own work. The Word report is generated from the shared Markdown sections.

## One example you can explain

**Hypothetical example — not a result we have achieved:** Department A has five unused office chairs. Department B requests seating for five people. A custodian records the chairs and their condition. Search finds the listing; AI can connect “seating” with “office chairs” and explain the suggestion. The relevant department representatives approve release and receipt. After transfer, the system records the new location and custodian. If this replaces a planned purchase, it can record an estimated avoided purchase using documented costs. It must not invent savings or carbon figures.

## Words you should know

| Term | Simple meaning |
|---|---|
| Asset | A physical item the university owns and tracks, such as a chair or monitor. |
| Circular | Keeping items useful through reuse, repair and transfer before recycling or disposal. |
| Classic vs AI | Classic code follows defined rules; AI adds suggestions based on meaning or patterns. Both use the same access and approval controls. |
| Scope | The agreed boundary of what the project includes and excludes. |
| Stakeholder vs user | A stakeholder affects or cares about the project; a user operates the application. Instructors are stakeholders who review our work without needing an application account. |
| Agile | Working in short cycles and adjusting after feedback. |
| Feasibility | Checking whether the proposal is practical with our time, money, technology and other constraints. |
| Requirement | A precise statement of what the system must do or satisfy. |
| NFR | A non-functional requirement: a quality or operating condition, such as search speed, security or deployment. |
| Deployment | Setting up the application and database on the chosen host so intended users can access it. |
| Synthetic data | Invented but realistic records used to develop and test the prototype. They are not real university records. |

## How your part connects to the team

| Your contribution | What it leads to |
|---|---|
| Problem and goals | Zayed identifies whose needs and current processes matter. |
| Scope and constraints | Ghith turns the intended behavior into testable requirements. |
| Schedule, ownership and risks | All three members know what to deliver, who owns it and what could delay it. |

Zayed owns Sections 3–5. Ghith owns Sections 6, 7 and 9. You own Sections 1, 2 and 8.

## Six likely questions

**1. Why do we need this instead of an inventory spreadsheet?**

An inventory tells us what items exist. Our proposal connects that record to requests, reservations, approvals, transfers, maintenance and reporting. The course scenario asks for that complete process, plus AI assistance.

**2. Why use AI, and can it approve a transfer?**

AI can find relevant items when wording differs and explain suggested matches. It cannot approve transfers or disposal. Defined rules enforce eligibility and access; authorised humans approve. Classic search and workflows remain available if AI fails.

**3. What have you actually completed in Phase 1?**

We have completed the initial plan and requirements document and organised the team's contributions in GitHub. It contains stakeholder/process analysis, 52 initial requirements, proposed success criteria and a project plan. The application, stakeholder interviews and performance results are future work.

**4. Is deployment included, even though it is marked Should have?**

Yes. It is in the intended scope and planned after the initial baseline. Phase 2 chooses hosting; the plan includes a hosted draft, a final HTTPS URL and documented deployment steps. The priority sets implementation order, not permission to silently omit it.

**5. Why Agile when the course already has fixed phases?**

The phases tell us what to submit and when. Short cycles tell us how to work between those deadlines. We can test AI access early, review what we learn and adjust the next tasks while still meeting the course milestones.

**6. How will you know the system is successful?**

We have proposed tests, not measured results. Examples include checking that at least 16 of 20 eligible requests have a useful asset in the top three AI matches, and that at least 95 of 100 classic searches finish within two seconds on the defined dataset. We will also test approvals, hosted workflows and fallback. User tests will assign tasks appropriate to each participant's role. Simulated savings will be labelled as simulated.

## Short practice script for your four slides

The words below take about two minutes. Use pauses and the slide visuals to reach your combined 2:30 allowance. Do not rush to fill every second with words.

### Slide 1 — Campus Resource Exchange

> We are Group 4. Our project proposes a campus resource exchange system that helps departments reuse existing equipment and track its life cycle.

### Slide 2 — The reuse problem

> The assignment describes departments buying equipment while similar usable items sit idle elsewhere. We want to answer three questions: what exists, who needs it, and what should happen next? Imagine one department has five unused office chairs and another needs seating. This is a hypothetical example. The opportunity is to make those chairs visible and move them through an accountable process.

### Slide 3 — The proposed service

> Our proposed service lets departments register assets, publish available items, request them and obtain approval for transfers. Classic rules manage availability, permissions and approvals. AI helps classify items, understand different search wording, rank suitable matches and explain suggestions. Authorised people make the final decisions, and classic workflows remain available if AI fails. Hosting and deployment are included in our scope. Live university finance integration and payment processing are outside it. Zayed will now explain the analysis that established these needs.

### Slide 7 — Delivery plan

> Those requirements and targets lead to our delivery plan. Next comes feasibility: checking technology, AI access and hosting. We then refine requirements, design, implement, deploy and test. We work in short cycles within the course phases. Zayed leads requirements and user experience; Ghith leads AI, architecture and deployment; I coordinate planning and backend integration. Phase 1 gives us our starting point. Implementation and measured results come later.

## Report sources

- [Section 1 — Introduction](https://github.com/duqins/ITS/blob/main/docs/phase1/sections/01-introduction.md)
- [Section 2 — Project overview and scope](https://github.com/duqins/ITS/blob/main/docs/phase1/sections/02-project-overview.md)
- [Section 5 — Requirements gathering and priorities](https://github.com/duqins/ITS/blob/main/docs/phase1/sections/05-requirements-gathering.md)
- [Section 6 — Initial requirements](https://github.com/duqins/ITS/blob/main/docs/phase1/sections/06-requirements-specification.md)
- [Section 7 — Proposed success criteria](https://github.com/duqins/ITS/blob/main/docs/phase1/sections/07-success-criteria.md)
- [Section 8 — Project plan and team responsibilities](https://github.com/duqins/ITS/blob/main/docs/phase1/sections/08-project-plan.md)

*These explanations follow the corrected Phase 1 report. Numerical targets describe planned evaluation, not achieved performance.*
