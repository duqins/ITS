<!-- GUIDANCE (Ghaith). AI features, written in the same format as Sultan's classic features in 4.3–4.16
(look at 04c-sultan-classic-features.md once it is merged, or at the example structure below).
Phase 3 brief p.8 asks for AI requirements for: classification, semantic matching, ranking,
sustainable-action recommendations, explanations, confidence information, user overrides and
model-version tracking. Start from your Phase 1 AI-01 to AI-13 and refine them into sub-requirements
(AI-02.1, AI-02.2 …). Keep the Phase 1 priorities: AI-06, AI-07 and AI-08 are Desirable (Should);
the others are Essential (Must). Section 1.2 explains the priority labels.

Each feature has three parts, exactly like the SRS template p.17–18:
### 4.x.1 Description and Priority      – what the feature does + "Priority: Essential (Must)"
### 4.x.2 Stimulus/Response Sequences   – numbered user action → system response pairs
### 4.x.3 Functional Requirements       – a table | ID | Requirement |

Write requirements with EARS (Chapter 3 slide 23) and state acceptable error, as slide 28 asks for AI
systems (for example "at least 16 of 20 labelled requests have a useful asset in the top three" from
your Phase 1 section 7). AI never approves anything: refer to BR-14 and BR-15 in section 5.5. -->

## 4.17 AI Asset Classification

TODO Ghaith: 4.17.1 description and priority, 4.17.2 stimulus/response, 4.17.3 requirements AI-01.x.

## 4.18 Semantic Matching and Eligibility

TODO Ghaith: AI-02.x and AI-03.x. Eligibility rules are classic code and run before ranking (BR-14).

## 4.19 Ranking, Explanations and Confidence

TODO Ghaith: AI-04.x and AI-05.x, including user override of the order and the reason recorded.

## 4.20 Sustainable-Action Recommendation

TODO Ghaith: AI-06.x. Priority: Desirable (Should). The final decision follows BR-08 and BR-09.

## 4.21 Campus Assistant

TODO Ghaith: AI-07.x and AI-08.x. Priority: Desirable (Should). Confirmation before any change.

## 4.22 Generative Reporting

TODO Ghaith: AI-09.x and AI-10.x. Generated figures must equal the conventional report totals in 4.16.

## 4.23 Model Tracking, Overrides and Fallback

TODO Ghaith: AI-11.x, AI-12.x, AI-13.x: human approval boundary, model/version records, user acceptance/correction/rejection log, fallback to classic search and forms.
