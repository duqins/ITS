# 3. Architecture

## 3.1 Decision Record

**ADR-01: Use one Django application with separate modules.**

The system must support accounts, asset records, requests, approvals, transfers, maintenance and reports. It must also support AI assistance while allowing the classic workflows to continue when AI is unavailable (NFR-07, NFR-09).

We compared two architecture styles from the Phase 4 lab.

**Table 3.1 Architecture options**

<!-- widths: 1800,3780,3780 -->
| Option | Benefits | Trade-offs |
|---|---|---|
| Modular monolith | One application contains separate business modules. It supports the agreed Django and PostgreSQL setup and keeps local installation, testing and deployment manageable for our team. | The modules are deployed together. We must keep their responsibilities clear, and we cannot scale one module separately from the application. |
| Service-oriented architecture | A separate AI service could be deployed and scaled independently from the main application. | It adds another service to host, secure, monitor and test. Calls between our own services would also need error handling and version management. |

**Decision.** We choose a modular monolith because it fits the size of our team, the semester schedule and the technologies selected in Phase 2. Django 5.2 LTS will provide the web pages and application modules. PostgreSQL on Neon will store records, and a private file bucket will store photographs and documents.

The Django application will run on Render. Its AI adapter will call the external models specified in section 6.6: gpt-4.1-mini-2025-04-14 and text-embedding-3-small. The adapter is the part that prepares AI requests, checks responses and handles failures.

**What we give up.** Our internal AI and reporting modules will not have independent deployments. A change to either module requires deploying the application. Clear module boundaries will make it easier to separate a service later if a measured need arises.

**Validation.** This is a design choice, not a claim that deployment has been tested. During implementation, we will test a complete request-and-approval workflow, an AI failure, and a restart that preserves records and uploaded files.

## 3.2 Architecture View

Figure 3.1 shows the main parts of the system and their connections. The boxes inside the Django boundary are modules within one application. Arrows show calls and returned data, rather than the order of workflow steps.

<!-- pagebreak -->

![Figure 3.1 Dawra Campus architecture and AI service connections](images/figure-3-1-architecture.png)

The security rules apply to every protected action and record lookup. The dashed connection shows reporting supplying source figures for an AI draft and receiving draft text for review.

**Table 3.2 Architecture responsibilities**

<!-- widths: 1800,5460,2100 -->
| Part | Responsibility | SRS links |
|---|---|---|
| Presentation | Provides the Django pages and forms for all nine roles. Shows records, suggestions, errors and confirmation controls. | UI-01 to UI-14, NFR-01 |
| Application | Manages accounts, assets, requests, reservations, approvals, transfers, maintenance and end-of-life workflows. Applies classic eligibility checks and allowed state changes. | FR-01 to FR-14, BR-14 |
| AI and analytics | Provides classification, semantic matching, ranking and explanations, sustainable-action advice, and assistant answers and report drafts. Keeps compatibility scores separate from confidence. | AI-01 to AI-13 |
| Data | Stores business records in PostgreSQL and files in the private bucket. Uses the entities in section 8, including MatchRecommendation, AiSuggestion and ModelVersion. | SI-01, SI-03, AI-12 |
| Integration | Connects the application to the database, AI provider, file storage and exports. Sends approved AI inputs, checks returned data and enforces the AI time limit. | SI-01 to SI-04, AI-13 |
| Notifications | Records and displays in-application tasks and status updates for users who may access the related records. | FR-16 |
| Security | Checks sign-in, roles and department access. Protects service credentials and records actions in the audit log. | FR-02, FR-18, NFR-03, BR-17 |
| Reporting | Calculates conventional report totals and sustainability indicators. Uses those figures as the source for AI report drafts and requires the relevant owner's review for official reports. | FR-17, AI-09, AI-10, SU-01 to SU-09, BR-10 |

**How the application uses the AI services**

1. **Classification service.** Asset registration sends approved asset details through the AI adapter. Category and tag suggestions return for the Asset custodian or Department representative to accept, correct or reject (AI-01).
2. **Semantic matching engine.** The application checks the request and asset eligibility before requesting meaning-based matches. Only permitted, eligible listings can become actionable recommendations (AI-02, AI-03, BR-14).
3. **Ranking model and explanations.** Django calculates the compatibility score from the fixed weights in SRS Table 4.1. AI supplies meaning-match information and can help explain the result. The score is 0 to 100; confidence is separate and, when available, ranges from 0 to 1 (AI-04, AI-05).
4. **Sustainable-action engine.** Maintenance and end-of-life workflows can request advice based on the asset's condition, costs and reuse options. The result remains a proposal subject to the usual reviews and approvals (AI-06, BR-07 to BR-09).
5. **Assistant and report drafts.** The assistant uses records the user may access. Report drafts use conventional report figures. Proposed changes require user confirmation, and normal approvals still apply (AI-07 to AI-10, BR-10, BR-15).

**Behaviour when AI is unavailable**

Classic registration, keyword search, filters, requests, reservations, approvals, transfers, maintenance and conventional reports remain available. Manual category selection replaces classification assistance, and normal forms replace assistant actions.

The AI adapter and any calls it makes share the 15-second deadline measured from the original user request. If AI fails or does not return usable output within that time, the application explains the issue, preserves the user's input and offers the relevant classic alternative (AI-13, NFR-07). Hosting startup time is measured separately.

Low-confidence matching and classification outputs follow SRS Table 4.2. Unavailable confidence is labelled as unavailable rather than invented. AI suggestions are stored for review and never directly approve a transfer, change a user's role or authorise spending.