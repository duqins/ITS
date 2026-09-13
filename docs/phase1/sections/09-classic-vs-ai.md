# 9. Classic vs. AI-Enhanced Perspective (Initial Reflection)

The project description requires the team to compare the two perspectives explicitly. This initial position will be revisited in every later phase.

<!-- widths: 1500,2500,2700,2660 -->
| Aspect | Classic (rule-based) approach | AI-enhanced approach | Initial position |
|---|---|---|---|
| Search | Exact keyword/category filters; predictable, transparent. | Semantic search finds functionally similar items with different wording. | Provide both; classic filters remain the ground truth, AI adds recall. |
| Matching | Checks category, quantity, availability. | Ranks alternatives by specification, condition, urgency, location, cost, sustainability. | AI ranks; rules enforce hard constraints (availability, permissions). |
| Classification | User selects from fixed taxonomy. | Model suggests category/tags from free text and images. | AI suggests, user confirms; taxonomy stays controlled. |
| Life-cycle decisions | Policy thresholds (age, repair cost). | Recommendation with confidence and explanation. | AI advises; humans decide on disposal, donation, transfer. |
| Reporting | Fixed totals and tables. | Narrative summaries, anomalies, suggested actions. | Generative report built on top of classic figures so numbers stay verifiable. |
| Risks | Rigid; misses reuse when terminology differs. | Uncertain, opaque, possibly biased; depends on external services. | Explainability, confidence, override, model-version tracking and fallback are Must/Should requirements. |

Decisions that must remain under human control: approving transfers and custody changes; authorising donation, recycling and disposal; approving repair spend; changing financial values; changing user roles. AI must never execute these automatically.
