# 11. Component, Deployment and AI Design

This section explains how the components work together, where they run, and how AI results are checked and presented. It follows the architecture in section 3, the service rules in section 4, the human approval points in section 5 and the data model in section 8. These are design decisions and planned checks, not claims that the system has already been implemented or tested.

## 11.1 Component Diagram

The system uses one Django application with separate modules. The five AI service groups are parts of this application, not five separately deployed servers. Internal modules call each other through defined interfaces, while the AI adapter handles calls to the external AI Provider.

The business workflow component applies eligibility and approval rules. The AI components return suggestions to it. They cannot approve an action or directly change ownership, spending, financial values or user roles. Reporting calculates conventional figures first and uses AI only to draft a written summary. Notifications remain inside the application.

The ranking model uses the fixed SRS scoring rules. It does not need a separate trained model or an extra provider call. The matching engine supplies the meaning similarity, and the ranking component calculates the final score and builds the factor explanation.

<!-- pagebreak -->

![Figure 11.1 Component diagram. Dashed arrows show which component uses another component or service.](images/figure-11-1-components.png)

## 11.2 Deployment Diagram

The hosted design places the Django application on Render, the PostgreSQL database on Neon, and attachments in a private S3-compatible bucket. The browser connects to Django through HTTPS. Database traffic uses TLS, and file and AI service calls use HTTPS. Database, storage and AI credentials stay on the server.

The AI adapter uses gpt-4.1-mini-2025-04-14 and text-embedding-3-small, as specified in section 6.6. All five service groups use Pattern A: ask and wait. There is no separate AI worker or job queue in this prototype design. The complete AI request has one 15-second limit, including retries and response checks. If AI cannot finish, the relevant classic feature remains available and entered data is preserved.

The private file bucket holds files; Attachment records hold their metadata and storage keys. File access requires a permission check before a short-lived link is issued. Backups use a separate private bucket and follow the schedule, retention and restore checks in section 6.5. The classic application must also run from the repository without an AI key, as required by NFR-09.

<!-- pagebreak -->

![Figure 11.2 Deployment diagram. Dashed lines represent the backup copies required by section 6.5.](images/figure-11-2-deployment.png)

## 11.3 AI Recommendation Workflow

Figure 11.3 shows matching for an approved ResourceRequest.

1. The Requester asks for matches. Django checks sign-in, access and the request's approval status.
2. Classic rules identify permitted, published listings and check availability, quantity, condition, technical compatibility and the required date. An item with missing mandatory information is not ranked (BR-14).
3. The matching engine compares the request with eligible asset descriptions. The 15-second limit runs from the original AI request; later calls or retries do not restart it.
4. The application checks the returned data. A match with confidence below 0.50 is withheld as an AI recommendation. Confidence from 0.50 up to, but not including, 0.75 gets a "Check carefully" label. Confidence of 0.75 or more is displayed normally. Missing confidence is labelled "Confidence unavailable - check carefully". Thresholds use full precision before display rounding.
5. The ranking component calculates the SRS score and explanation for each usable match. Each stored MatchRecommendation links the asset, request and ModelVersion.
6. The Requester reviews the results and chooses an eligible item. Choosing a different recommended order requires an override reason. This records a choice; it does not reserve the item or approve a transfer.
7. A separate hold request rechecks current eligibility, verification and available quantity. The normal reservation and transfer approval stages then apply. Ownership changes only after confirmed receipt (BR-13).

If AI fails, returns an unusable response or has no usable suggestions, the system offers classic search and filters within the original limit. It does not invent an AI score for a classic result. If no eligible asset exists, it explains this and leaves the next step to the user; it does not automatically close the request.

<!-- pagebreak -->

![Figure 11.3 AI recommendation workflow for an approved resource request.](images/figure-11-3-ai-workflow.png)

## 11.4 Interface Contracts

An interface contract defines what a component receives, what it returns and what must be checked. These are internal application interfaces. They do not introduce five public APIs or new database tables.

Every call carries a correlation ID for tracing, its task, permitted input references, and the time remaining before the shared deadline. A correlation ID identifies the AI call; requestId identifies a ResourceRequest. Django determines the user's role and access scope before preparing the input. Only approved fields needed for the task are sent to the provider.

Every result returns a status, task-specific output, source references, warnings and available confidence information. The application attaches the model identity from its configuration and provider response; the model cannot choose its own permissions or database references. Confidence is a number from 0 to 1 only when its basis is supported and recorded. Otherwise it is null and displayed as unavailable. It is never calculated by dividing the compatibility score by 100.

**Table 11.1 AI service contracts**

<!-- widths: 1800,3100,4460 -->
| Service | Input | Output and required checks |
|---|---|---|
| Classification service | Asset details, allowed categories and supported image or document content; assetId when a record already exists. | Suggested category, subcategory, description, tags, material, missing details, reasons and confidence information. Check category values and mark unsupported or uncertain input. Apply the 0.60 threshold from section 4. Save as AiSuggestion with task classification; only confirmed values enter the asset workflow. |
| Semantic matching engine | ResourceRequest reference, request text, eligible asset references and their permitted descriptions. | A meaning similarity from 0 to 1 for each candidate, supporting input references and available confidence information. Reject unknown asset references, invalid vectors or out-of-range results. Only candidates that passed eligibility may continue. |
| Ranking model | Eligible candidates, meaning similarities and the seven factor inputs in Table 11.2. | Ordered results with score, factor points, explanation and uncertainty labels. Check that the score equals the factor total and is between 0 and 100. Missing optional information earns 0 points and is labelled unknown. The result is stored as MatchRecommendation. |
| Sustainable-action engine | Permitted condition, demand, repairability, cost, material, value and sustainability information. | A proposed action, supporting facts, limitations and reasons for passing over earlier reuse-first options. Check BR-08 and identify BR-09 special handling. Save as AiSuggestion with task advice. Acceptance creates a proposal for the normal human workflow. |
| Assistant and report drafts | For the assistant: a question, permitted records and approved guidance. For reports: conventional figures, source references, reporting period, filters and units. | An answer or proposed request fields for the assistant; an AI-labelled draft for reporting. Check references and access. Report totals must match conventional totals. Save as AiSuggestion with task assistant or report. User confirmation is required before submitting a request; relevant data owners review official reports. |

The adapter checks required fields, types, ranges and source references before accepting a response. Asset text and uploaded content are treated as data, not permission to execute instructions. A valid response is still a suggestion, not an approval.

Unavailable service, rate limits, invalid output and timeouts return a clear status and the classic alternative from section 4. An unsupported answer is marked uncertain or withheld. For advice, assistant answers and reports, no new numerical confidence threshold is introduced. Late responses cannot overwrite confirmed user input. If a result cannot be saved with its required trace, it is not presented as a completed AI recommendation.

## 11.5 Recommendation Score and Explanation

The score follows the Phase 3 SRS ranking weights without changing them. Mandatory eligibility is checked first; a high score cannot make an ineligible item acceptable.

**Table 11.2 Compatibility score**

<!-- widths: 2400,800,6160 -->
| Factor | Maximum | Points awarded |
|---|---|---|
| Functional purpose and meaning | 30 | Meaning similarity from 0 to 1 multiplied by 30. |
| Technical compatibility | 20 | Share of requested specifications met or exceeded, multiplied by 20. Mandatory specifications must already pass eligibility. |
| Condition | 15 | At least two levels above the requested minimum: 15; one level above: 10; equal to the minimum: 5. Levels are New, Good, Fair and Poor. |
| Location and transfer cost | 10 | Same building: 10; another building with no transfer cost: 6; transfer cost needed: 2. |
| Availability and required date | 10 | Available now: 10; within five working days: 6; later but before the required date: 2. |
| Sustainability benefit | 10 | Estimated remaining useful life of at least three years: 10; at least one but less than three years: 6; less than one year: 2. |
| Estimated repair cost | 5 | No repair needed: 5; repair estimate below 25% of the asset value: 3; 25% or more: 0. |
| Total | 100 | Add the seven factor scores. |

For the embedding-based implementation, the proposed meaning measure is cosine similarity clipped to the 0-to-1 range. This conversion is recorded with the scoring configuration. It measures text similarity, not confidence. Invalid or zero-length vectors are rejected rather than assigned an invented similarity. Personal and department names are excluded from the text used for matching.

A missing optional input gives that factor 0 points and an "unknown" explanation. Missing costs are not treated as zero cost. If a required ratio cannot be calculated, such as repair cost against an unknown or zero asset value, the factor is marked unknown. Missing mandatory information prevents ranking. Equal scores are ordered by earlier availability, then the nearer building. Personal characteristics and department names do not contribute to the score.

For example, a synthetic eligible asset with meaning similarity 0.80, all requested specifications met, condition one level above the minimum, the same building, immediate availability, four years of remaining life and no repair needed receives 24 + 20 + 10 + 10 + 10 + 10 + 5 = 89 points. This is a worked example, not a measured test result.

The explanation lists the factor points, the asset and request information used, and any missing information. The ranking component builds it directly from the calculation, so the wording cannot contradict the score. Confidence is shown separately with its basis or an unavailable label. Neither score nor confidence grants approval or guarantees that an item is suitable.

## 11.6 Model-Monitoring Records

Monitoring uses the entities already defined in section 8. It records both the original AI result and the user's response, so corrections remain traceable.

**Table 11.3 AI records and monitoring information**

<!-- widths: 2200,7160 -->
| Record | Information retained |
|---|---|
| ModelVersion | modelVersionId, task, modelName, version and activeFrom. The configured model identifier is retained even when a more detailed version is unavailable. A model change creates a new record rather than changing the identity of an earlier result. |
| MatchRecommendation | matchId, assetId, requestId, modelVersionId, score, confidence, explanation, userResponse and overrideReason. The model reference identifies the embedding model used for meaning matching. The explanation includes the factor breakdown and missing-input labels. |
| AiSuggestion | suggestionId, modelVersionId, optional assetId, task, original suggestion, confidence, explanation, userResponse, correctedValue and createdAt. Tasks remain classification, advice, assistant and report. |
| AuditLog | The user, action, time, related record, before and after values, and reason. Generation and response entries retain permitted input references and the original result. Corrections, rejections and overrides include a reason. Entries are appended, never edited or deleted. |
| Protected application log | Correlation ID, task, start and finish times, duration, model reference, outcome, retry count and fallback reason. Failures are recorded even when no recommendation row was created. API keys, passwords and unnecessary personal or uploaded content are excluded. |

For reproducibility, each generation audit entry also keeps the permitted input snapshot, scoring or prompt configuration version, confidence basis and model reference in its structured afterValue. These are trace details within the existing audit field, not additional business tables. The scored inputs must be retained because a later asset update could otherwise hide how an earlier score was produced.

Unavailable confidence is stored as null, not zero. An unavailable model version is explicitly marked unavailable while the ModelVersion link remains valid. User responses and corrected values are stored separately from the original suggestion. The logging and backup access controls follow section 6, and retention follows the agreed policy once TBD-7 is resolved.

The team will review response times, failure and fallback rates, correction and override reasons, and results on the fixed SRS datasets. User acceptance alone does not prove that an AI result was correct. Planned checks include at least 16 correct classifications out of 20 assets; useful top-three matches for at least 16 of 20 requests and two more requests than classic search; zero actionable ineligible matches; all five fallback cases within 15 seconds; and five report summaries with traceable claims and correct totals. Changes to models, prompts, weights or thresholds must be recorded with a reason and checked again against the same evaluation data before being enabled.