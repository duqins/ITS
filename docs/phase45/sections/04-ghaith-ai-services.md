# 4. AI Services

The application uses five AI service groups. Each group supports an existing workflow, and every workflow has a classic alternative. AI outputs remain suggestions or drafts; they do not approve actions or directly change business records (BR-15).

The services use the AI adapter and models specified in section 6.6. Classification, sustainable-action advice, assistant answers and report drafts use gpt-4.1-mini-2025-04-14. Semantic matching uses text-embedding-3-small. Django calculates compatibility scores using the fixed weights in SRS Table 4.1.

## 4.1 Calling Pattern Decision

The Phase 4 lab defines three calling patterns:

- **A (ask and wait):** the user requests a result and the application waits for a response within a set time limit.
- **B (compute ahead):** reusable results are prepared before a user needs them.
- **C (queue and notify):** work runs in the background and the user is notified when it finishes.

**Choice.** We use pattern A for the initial prototype. Users request classification, matches, advice, assistant answers and report drafts while completing a task. This approach fits the agreed 15-second limit and keeps the design within one Django application.

**Alternatives and trade-off.** Pattern B could reduce repeated matching work, but it would require a maintained set of prepared results and rules for refreshing them when assets or models change. Pattern C would suit scheduled advice or long report jobs, but would require background jobs and progress tracking. We accept that users may wait briefly for an AI result, with a classic alternative available when the time limit is reached.

Pattern A describes how the application returns a result. It does not mean that every step makes a separate provider call: eligibility checks and the weighted score calculation run in Django.

## 4.2 AI Service Behaviour

**Table 4.1 AI services, calling patterns and fallback**

<!-- widths: 1700,2200,1000,2100,2360 -->
| AI service | Pattern and reason | Time limit | If down | If unsure |
|---|---|---|---|---|
| Classification service (AI-01) | A. The user is completing an asset form and needs suggestions to review. | 15 seconds. | Keep entered details and allow manual category selection and data entry. | Below 0.60: show the suggestion as an option only, without filling the field. At 0.60 or above: show the suggested value for acceptance, correction or rejection. |
| Semantic matching engine (AI-02, AI-03) | A. The user needs matches for the current request, using listings that pass the current eligibility checks. | Shares one 15-second deadline with ranking and explanations. Target: results within 5 seconds for 95 of 100 requests (NFR-16). | Show classic keyword search and filters, without presenting the results as AI recommendations. | The current embedding model returns no confidence, so matches show "Confidence unavailable - check carefully" and the score and its factors guide the requester. When a model version returns a confidence, below 0.50 withholds the AI recommendation, 0.50 to below 0.75 shows "Check carefully", and 0.75 or above shows normally. |
| Ranking model and explanations (AI-04, AI-05) | A. The user needs an ordered list and reasons before choosing an item. Django applies the SRS weights. | Uses the time remaining in the matching request's 15-second deadline. | Show eligible results in classic order, without AI scores. | Apply the same matching confidence thresholds. Keep the compatibility score separate from confidence, and show missing information. |
| Sustainable-action engine (recommendation engine, AI-06) | A. The user requests advice while reviewing maintenance or an end-of-life action. | 15 seconds. | Continue with manual assessment and the reuse-first and special-handling rules in BR-08 and BR-09. | No inspection or cost record cited, or the advice does not follow the reuse-first order in BR-08: mark the advice uncertain and list the missing evidence. In every case the advice stays a proposal for human review and does not change the asset's state. |
| LLM assistant and report drafts (AI-07 to AI-10) | A. The user asks a question, prepares a request or asks for a written report summary. | 15 seconds per user request. | Keep normal screens, request forms and conventional reports available. | No permitted record supports a claim, or a report total differs from the conventional total: say what cannot be confirmed and add no facts. Proposed changes need user confirmation, and official report summaries need the relevant data owner's review. |

## 4.3 Confidence and Output Checks

The classification and matching thresholds above come from SRS Table 4.2. The system compares the full confidence value before rounding it for display.

Confidence uses a value from 0 to 1 when a supported measure is available. text-embedding-3-small returns vectors only, so with the current models matching has no supported confidence and every match is labelled unavailable. For classification, the confidence is the probability that gpt-4.1-mini gives the chosen category, read from the token probabilities the API returns, and it is stored with that basis. Compatibility uses a separate score from 0 to 100. Neither value is an approval or a guaranteed probability that the result is correct (AI-04.3).

If confidence is unavailable, the system shows "Confidence unavailable - check carefully". It does not invent a value or treat missing confidence as zero (AI-05.4, AI-12.2).

The SRS sets no confidence thresholds for sustainable-action advice, assistant answers or report drafts. Instead, advice is checked against the inspection and cost records it cites, and assistant answers and reports against the permitted records and conventional totals they cite. These outputs remain subject to source checks and human review. Missing evidence and uncertainty must be identified. Unsupported answers or unusable drafts lead to the relevant classic alternative.

Before using an AI response, the adapter checks that:

- Required fields are present and have the expected types.
- Any supplied confidence value is within 0 to 1.
- Referenced records are valid and within the user's access rights.
- Suggested matches pass the mandatory eligibility checks in BR-14.
- Ranking reasons agree with the calculated factor points.
- Report figures agree with the conventional source totals.

A malformed response is treated as an AI failure. A well-formed response still requires the normal user review and approval controls.

## 4.4 Time Limit and Failure Handling

The 15-second limit starts with the original user request. All model calls, checks and retries needed for that result share the same deadline. A retry does not receive a new 15-second allowance.

If the service fails, is rate-limited or does not return usable output before the deadline, the application shows a clear message, preserves entered data and makes the relevant classic alternative available (AI-13, NFR-07). A late response must not overwrite the user's manual entries or apply an action.

Matching and ranking are one user request, so their time allowances are not added together.

The application records the model used and the user's response through ModelVersion, MatchRecommendation or AiSuggestion, as appropriate. Section 11 defines the interface details and monitoring records. Failed calls and fallback outcomes are also recorded without storing credentials or unnecessary personal data.