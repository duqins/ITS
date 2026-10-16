## 4.16 AI Asset Classification

### 4.16.1 Description and Priority

AI helps the Asset custodian or Department representative complete an asset record by suggesting categories and other details. The user checks each suggestion before it becomes part of the record. This feature refines Phase 1 AI-01.

**Priority: Essential (Must, High).**

### 4.16.2 Stimulus/Response Sequences

1. The Asset custodian or Department representative enters asset details and asks for suggestions. The system checks the supplied information and requests AI assistance.
2. The system displays the suggested details, reasons and confidence information, with any missing or uncertain information clearly marked.
3. The user accepts, corrects or rejects the suggestions. The system applies only the confirmed details and records the user's decision.
4. If AI is unavailable or cannot read an attachment, the system explains the issue and allows manual entry.

### 4.16.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| AI-01.1 | When a user requests classification assistance, the system shall suggest a category, subcategory, standard description, tags, material where supported, and missing details using the supplied title, description, specifications and supported image or document content. |
| AI-01.2 | If an input format is unsupported or extracted information is uncertain, then the system shall identify the affected input and request manual review rather than treat it as confirmed information. |
| AI-01.3 | The system shall display suggested values separately from confirmed asset details and allow the Asset custodian or Department representative to accept, correct or reject them. |
| AI-01.4 | The system shall apply AI suggestions to the asset record only after the authorised user confirms them, while following the asset-record rules in section 4.4 and Table 5.2. |
| AI-01.5 | In a fixed test set of 20 labelled assets, the system shall suggest the correct category for at least 16 assets. Missing, invalid or failed AI responses shall count as incorrect results. |

## 4.17 Semantic Matching and Eligibility

### 4.17.1 Description and Priority

Semantic matching compares the meaning of a request with asset descriptions, so users can find suitable items even when different words are used. Before AI ranks any results, classic rules check whether each item is eligible. This feature refines Phase 1 AI-02 and AI-03.

**Priority: Essential (Must, High).**

### 4.17.2 Stimulus/Response Sequences

1. The Requester asks for matches using a request or search description. The system identifies published listings that the user may access.
2. The system checks the mandatory requirements, removes ineligible items and compares the meaning of the request with the remaining listings.
3. The system presents the eligible matches for ranking and review under section 4.18.
4. If no eligible item exists, the system explains that no suitable match was found and leaves the next action to the user.

### 4.17.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| AI-02.1 | When a user requests matches, the system shall compare the meaning of the request or search description with permitted published asset listings, including cases where different terms describe the same need. |
| AI-02.2 | For the fixed set of 20 requests with known suitable assets, the system shall return at least one reviewer-labelled useful asset among the first three results for at least 16 requests. |
| AI-02.3 | Using the same 20 requests, asset records and eligibility rules, AI matching shall succeed on at least two more requests than classic keyword search, with success measured by a useful asset appearing in the first three results. |
| AI-02.4 | If no eligible asset exists, then the system shall show a no-match message without presenting an ineligible item as suitable or automatically closing the request. The user may follow FR-07.8 to close it as No suitable item. |
| AI-03.1 | Before AI ranking, the system shall use classic rules to check access rights, availability, quantity, required condition, technical compatibility and the required date, as specified by BR-14. |
| AI-03.2 | When assessing matches, the system shall consider functional purpose, category, technical compatibility, available quantity, condition, location, urgency, required date, estimated transfer or repair cost, and sustainability benefit. |
| AI-03.3 | If information needed for a mandatory eligibility check is missing, then the system shall identify the missing information and withhold that item as an actionable recommendation until the check can be completed. Missing costs or sustainability figures shall be marked as unknown rather than assumed to be zero. |
| AI-03.4 | Across the 20-request matching test, the system shall show zero items that fail mandatory eligibility checks as actionable recommendations. |

The matching tests use the Phase 1 dataset of 500 synthetic assets, 10 departments and 50 requests. Two of us will label suitable assets independently and resolve differences before fixing the 20-request evaluation set. Classic search and AI matching shall use the same requests and asset snapshot. Failed AI responses count as unsuccessful requests. Cases with no suitable asset shall be tested separately and excluded from the 20-request usefulness calculation. These numbers are acceptance targets, not measured results.

## 4.18 Ranking, Explanations and Confidence

### 4.18.1 Description and Priority

The system puts eligible matches in a useful order and explains why each item was recommended. A compatibility score shows how well an item fits the request. Confidence describes the uncertainty of the AI output; it does not give approval or guarantee correctness. This feature refines Phase 1 AI-04 and AI-05.

**Priority: Essential (Must, High).**

### 4.18.2 Stimulus/Response Sequences

1. The system receives the eligible matches from section 4.17 and ranks them using the weights in Table 4.1.
2. The Requester opens a recommendation. The system shows its compatibility score, explanation, relevant asset details and confidence information.
3. The Requester chooses the top result or another eligible item. The system records the selection and, when the user overrides the recommended order, the reason.
4. If the user requests a reservation, the system starts the normal reservation workflow under section 4.8.

### 4.18.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| AI-04.1 | The system shall show each recommended match with a compatibility score from 0 to 100, an explanation of the main matching factors and references to the relevant asset and request details. |
| AI-04.2 | The system shall identify assumptions, missing information and unresolved non-mandatory concerns in the explanation. Mandatory constraints shall remain subject to BR-14. |
| AI-04.3 | The system shall display confidence separately from the compatibility score, explain the basis of the confidence information and mark it as unavailable when no supported measure exists. Neither value shall be presented as a guaranteed probability of correctness. |
| AI-05.1 | The system shall calculate the compatibility score (0 to 100) by adding the factor points in Table 4.1 and rank eligible matches from highest to lowest score. Ties and missing information shall be handled as stated under Table 4.1. |
| AI-05.2 | The system shall allow the user to choose another eligible item instead of the highest-ranked result and shall record the selected item and the user's reason for overriding the recommendation. |
| AI-05.3 | In a review of 20 sampled recommendations, the system shall show the matching reasons, relevant inputs and confidence information or its unavailability for every recommendation. |
| AI-05.4 | The system shall apply the confidence thresholds in Table 4.2 to every match and classification suggestion that has a confidence value. If no confidence value is available, the system shall show the result with a "Confidence unavailable – check carefully" label, as required by AI-04.3. |

### 4.18.4 Ranking Weights and Confidence Thresholds

We rank only matches that already passed the eligibility checks in section 4.17 (BR-14). The AI service gives the meaning-match similarity and the explanation; the system adds up the points below, so the same inputs always give the same score.

**Table 4.1 Ranking weights**

<!-- widths: 3000,1100,5260 -->
| Factor | Points | How the points are given |
|---|---|---|
| Functional purpose and meaning match | 30 | Similarity between the request and the listing text (0 to 1), multiplied by 30. |
| Technical compatibility | 20 | Share of the requested specifications that the item meets or exceeds, multiplied by 20. |
| Condition | 15 | Two or more levels above the minimum requested condition: 15; one level above: 10; equal to the minimum: 5. Levels: New, Good, Fair, Poor. |
| Location and transfer cost | 10 | Same building: 10; another building with no transfer cost: 6; transfer cost needed: 2. |
| Availability and required-by date | 10 | Available now: 10; available within 5 working days: 6; available later but before the required-by date: 2. |
| Sustainability benefit | 10 | Estimated remaining useful life of 3 years or more: 10; 1 to 3 years: 6; less than 1 year: 2. |
| Estimated repair cost | 5 | No repair needed: 5; repair estimate below 25% of the item's value: 3; 25% or more: 0. |
| **Total** | **100** | |

- **Ties:** if two matches have the same score, the one available earlier ranks first, then the one in the nearer building.
- **Missing information:** a factor with missing optional information gets 0 points and is shown as "unknown" in the explanation. Missing costs are not assumed to be zero (AI-03.3). If information needed for a mandatory check is missing, the item is not ranked at all.
- **Fairness:** no factor uses personal characteristics or department names (NFR-12).

**Table 4.2 Confidence thresholds**

<!-- widths: 2300,2100,4960 -->
| AI task | Confidence (0 to 1) | What the system does |
|---|---|---|
| Matching (4.17–4.18) | 0.75 or more | Shows the match normally. |
| Matching (4.17–4.18) | 0.50 to 0.74 | Shows the match with a "Check carefully" label. |
| Matching (4.17–4.18) | Below 0.50 | Insufficient confidence: the match is not shown as a recommendation, and the system offers classic search and filters (AI-13.1, NFR-07). |
| Classification (4.16) | 0.60 or more | Fills in the suggested value for the user to accept, correct or reject (AI-01.3). |
| Classification (4.16) | Below 0.60 | Insufficient confidence: the suggestion is listed as an option only, nothing is filled in, and the user enters the value manually. |

These are our starting values. We will check them with the 20-request matching test (AI-02.2) and the 20-asset classification test (AI-01.5), and record any change with its reason.

## 4.19 Sustainable-Action Recommendation

### 4.19.1 Description and Priority

AI suggests ways to extend an asset's useful life or handle it responsibly when it leaves service. The recommendation supports the user's decision and follows the reuse-first order in BR-08. This feature refines Phase 1 AI-06.

**Priority: Desirable (Should, Medium).**

### 4.19.2 Stimulus/Response Sequences

1. An authorised user requests advice for an asset. The system gathers its permitted condition, demand, repair and cost information.
2. The system suggests an action and explains which information supports it and what remains uncertain.
3. The user accepts the suggestion as a proposal, changes it or rejects it. The system records the decision and keeps the normal approval requirements.
4. If the action concerns an item requiring special handling, the system identifies the checks required by BR-09.

### 4.19.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| AI-06.1 | When sustainable-action advice is requested, the system shall consider retaining or reusing, transferring, repairing, refurbishing, donating, disassembling, recycling, retiring or disposing of the asset, as relevant to its condition and use. |
| AI-06.2 | The system shall explain how condition, demand, repairability, cost, material, value and sustainability factors affected the recommendation, and identify any missing information. |
| AI-06.3 | The system shall follow the reuse-first order in BR-08 and explain why earlier options are unsuitable before recommending a later option. It shall not invent evidence to justify the recommendation. |
| AI-06.4 | When the user accepts a recommendation, the system shall treat it as a proposal and apply the relevant transfer, maintenance or end-of-life workflow. End-of-life actions shall require Sustainability officer review and Finance officer approval under BR-08. |
| AI-06.5 | Where BR-09 applies, the system shall identify the required EHS consultation and data-erasure evidence. An AI recommendation shall not replace either requirement. |
| AI-06.6 | If the available information is insufficient to support an action, then the system shall state the limitation and request manual review without changing the asset's state. |

## 4.20 Campus Assistant

### 4.20.1 Description and Priority

The campus assistant lets authorised users ask questions and draft requests in everyday language. It can help users search, understand record status and find relevant guidance. Users must review and confirm any proposed change, and the normal approval rules still apply. This feature refines Phase 1 AI-07 and AI-08.

**Priority: Desirable (Should, Medium).**

### 4.20.2 Stimulus/Response Sequences

1. The user asks a question or describes a resource need. The system checks the user's permissions before retrieving relevant information.
2. The assistant answers using permitted records or prepares a draft request with the proposed fields.
3. The user reviews the draft and corrects, confirms or cancels it.
4. After confirmation, the system checks permissions and required fields again. A valid submitted request enters Pending department approval (RQ-02).
5. If information is missing, the action is unauthorised or the user cancels, the system does not submit the request.

### 4.20.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| AI-07.1 | The system shall support natural-language resource search, asset-history and request-status questions, policy, service and sustainability guidance, and drafting resource requests. |
| AI-07.2 | The system shall limit information used and shown by the assistant to records and guidance the signed-in user is authorised to access. |
| AI-07.3 | When answering a factual question, the system shall provide references to the supporting records or approved guidance and identify any policy values that remain unconfirmed. |
| AI-07.4 | If the available sources do not support an answer, then the system shall state that it cannot confirm the answer rather than invent information. |
| AI-08.1 | Before submitting a request or changing a record through the assistant, the system shall show the exact proposed fields and changes and require explicit user confirmation. |
| AI-08.2 | After confirmation, the system shall recheck permissions and input validity and apply the same approval workflow as the classic interface. A submitted resource request shall enter RQ-02 under BR-03. |
| AI-08.3 | The system shall allow the user to correct or cancel the proposed action before submission. Cancellation shall leave the target record unchanged. |
| AI-08.4 | The assistant shall pass all five planned request-submission tests: confirmed, corrected, cancelled, unauthorised and incomplete requests. Valid submissions shall require confirmation; cancelled, unauthorised and incomplete requests shall not be submitted. |

## 4.21 Generative Reporting

### 4.21.1 Description and Priority

AI turns conventional report data into a readable draft summary. The conventional reports remain the source of the figures, and the responsible data owners review generated summaries before official use. This feature refines Phase 1 AI-09 and AI-10.

**Priority: Essential (Must, High).**

### 4.21.2 Stimulus/Response Sequences

1. An authorised user selects the reporting period, departments and report information. The system produces the conventional figures under section 4.15.
2. The user requests a written summary. The system generates a draft using those figures and permitted supporting records.
3. The user checks the summary and follows its references to the source information.
4. The relevant data owner reviews the summary. The system records the review or keeps the summary in Draft with comments.

### 4.21.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| AI-09.1 | The system shall generate draft summaries covering resource exchange, high-demand categories, maintenance trends, recommended actions, avoided purchases, financial savings, waste diversion and estimated carbon reductions where supporting data is available. |
| AI-09.2 | The system shall take reported figures from the corresponding conventional reports, using the same record snapshot, filters, units and rounding. Generated totals shall equal the conventional report totals. |
| AI-09.3 | The system shall label generated summaries as AI-generated drafts and distinguish recorded outcomes from estimates, assumptions and proposed actions. |
| AI-10.1 | The system shall link factual claims to supporting records or report totals and identify missing information rather than invent figures or conclusions. |
| AI-10.2 | Before a summary becomes official, the system shall require review by the relevant data owners under BR-10: the Finance officer for financial figures, the Sustainability officer for sustainability figures and the Business administrator for operational figures. |
| AI-10.3 | In five generated test summaries, every factual claim shall be traceable to its supporting information and every reported total shall match the corresponding conventional report. Unsupported claims or mismatched figures shall fail the relevant test. |

## 4.22 Model Tracking, Overrides and Fallback

### 4.22.1 Description and Priority

The system records how AI outputs were produced and how users responded to them. People retain control over approvals and record changes. If AI fails or is unavailable, users can continue through the classic features. This feature refines Phase 1 AI-11, AI-12 and AI-13.

**Priority: Essential (Must, High).**

### 4.22.2 Stimulus/Response Sequences

1. The system receives an AI output and records its source, time and available model information.
2. The user accepts, corrects, rejects or overrides the output. The system records the response and applies the normal validation and approval rules.
3. If an AI service fails, the system shows a clear message, preserves the user's input and makes the relevant classic alternative available.
4. The user continues with classic search, forms, approvals or reports.

### 4.22.3 Functional Requirements

<!-- widths: 1100,8260 -->
| ID | Requirement |
|---|---|
| AI-11.1 | The system shall treat AI outputs as recommendations and preserve human control over transfers, donation, recycling, disposal, repair spending, financial values and user roles, following the permissions and approval stages in sections 4.1 and 5.5. |
| AI-11.2 | The system shall not treat selecting a match as a reservation, a reservation as transfer approval, or confirmation of an assistant action as approval by another role. A transfer shall reach Approved (TR-04) only after the approvals required by BR-05 and BR-06. |
| AI-11.3 | In the 14 planned approval tests, covering one authorised and one unauthorised path for each of the seven actions in AI-11.1, the system shall allow zero bypasses of required confirmation, permissions or approvals. |
| AI-12.1 | For each AI output, the system shall record the task, input record references, output, generation time, model or deployment identifier, available model version, and any score or confidence information used. |
| AI-12.2 | If model-version or confidence information is unavailable, then the system shall mark it as unavailable rather than create a value. |
| AI-12.3 | When a user accepts, corrects, rejects or overrides an AI output, the system shall record the user, time, original output, response and any corrected values. Corrections, rejections and overrides shall include a reason and follow the audit rules in FR-18 and BR-17. |
| AI-13.1 | If AI is unavailable, rate-limited, returns invalid output or falls below the confidence threshold for its task in Table 4.2, then the system shall explain the issue and offer the relevant classic search, filters, form or report. |
| AI-13.2 | If an AI request fails or remains unanswered, then the system shall display a failure or timeout message and make the classic alternative available within 15 seconds of the original request, including any retries. It shall preserve entered data and allow the classic workflow to continue. |
| AI-13.3 | The system shall pass all five planned fallback tests: unavailable service, timeout, rate limit, malformed output and insufficient confidence. Each test shall preserve user input and provide the relevant classic alternative within 15 seconds. |
| AI-13.4 | When AI credentials are absent or AI services are disabled, the system shall allow the classic features to start and operate without a paid AI account or AI API key, as required by NFR-09. |