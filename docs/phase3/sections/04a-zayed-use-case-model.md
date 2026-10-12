# 4. System Features

Section 4.1 shows the use-case model, section 4.2 defines the states that records move through, and sections 4.3 to 4.23 specify the requirements feature by feature.

## 4.1 Use-Case Model

<!-- GUIDANCE (Zayed). Phase 3 brief p.8: "Create use-case diagrams and detailed use-case descriptions."
Follow the Chapter 3 slides: slide 19 (diagram notation), slide 21 (include/extend), slide 22
(step-by-step method) and slide 18 (the description format). Your KU Eats layout template is a good model. -->

### 4.1.1 Actors

TODO Zayed: table of actors. Primary actors = the nine roles from section 2.3. Secondary actor = «system» AI service (external language and embedding models). Say which actors are generalisations, e.g. every role inherits "Staff user" (sign in, view notifications, use the assistant).

<!-- widths: 2200,1500,5660 -->
| Actor | Type | Goal in the system |
|---|---|---|

### 4.1.2 Use-Case Diagram

<!-- Draw ONE UML use-case diagram (draw.io, PlantUML or Visual Paradigm), export it as PNG to
docs/phase3/images/use-case-diagram.png, then replace the TODO below with this line:
![Figure 1. Dawra Campus use-case diagram](images/use-case-diagram.png)
Rules from the slides: actors outside the system boundary, use cases named verb + noun, solid lines for
associations, «include» for steps that always run, «extend» only for conditional steps, external
system on the right. Suggested include/extend:
UC-02 Register asset «include» Suggest classification (AI service);
UC-04 Submit resource request «include» Check eligibility; UC-06 Review ranked matches «extend» UC-04;
UC-08 Approve workflow step «include» Send notification;
UC-11 Decide end-of-life action «extend» Review sustainable-action recommendation.
Keep the use-case IDs and names below so section 6.5 (traceability) stays correct. If you must rename
or add one, tell Sultan. -->

TODO Zayed: insert the diagram image and one sentence explaining the boundary and the AI service actor.

### 4.1.3 Use-Case Descriptions

<!-- Write one description per use case in the slide 18 format. Copy this block for each:

#### UC-04 Submit resource request

**Actors:** Requester (initiator), Department representative
**Related requirements:** FR-07.1 to FR-07.6, BR-03
**Precondition:** …
**Main success scenario:**
1. Requester …
2. System …
**Alternative and exception flows:**
3a. …
**Postcondition:** …

Number alternatives after the step they branch from (3a, 4a), as on slide 18. Use the state names
from section 4.2 (for example "request becomes Pending department approval") and the business rule
IDs from section 5.5. The related requirement IDs are listed in the table below so you don't have to
search for them. -->

<!-- widths: 900,2700,2700,3060 -->
| ID | Use case | Main actors | Related requirements |
|---|---|---|---|
| UC-01 | Manage accounts and roles | Business administrator, System administrator | 4.3 (FR-01, FR-02), BR-01, BR-02 |
| UC-02 | Register asset | Asset custodian, Department representative, AI service | 4.5 (FR-04, FR-05), 4.17 (AI-01) |
| UC-03 | Publish asset listing | Department representative, Asset custodian | 4.6 (FR-06), BR-04 |
| UC-04 | Submit resource request | Requester, Department representative | 4.7 (FR-07), BR-03 |
| UC-05 | Search and filter assets | Requester, all staff users | 4.8 (FR-08) |
| UC-06 | Review ranked matches | Requester, AI service | 4.18–4.19 (AI-02 to AI-05) |
| UC-07 | Reserve asset | Requester, Asset custodian | 4.9 (FR-09), BR-11, BR-12 |
| UC-08 | Approve workflow step | Department representative, Finance officer, Procurement officer, Sustainability officer | 4.10 (FR-10), BR-04 to BR-10 |
| UC-09 | Confirm handover and receipt | Asset custodian, Department representative | 4.11 (FR-11), BR-13 |
| UC-10 | Manage maintenance work | Asset custodian, Maintenance staff, Department representative | 4.12 (FR-12, FR-13), BR-07 |
| UC-11 | Decide end-of-life action | Sustainability officer, Finance officer, Department representative, AI service | 4.13 (FR-14), 4.20 (AI-06), BR-08, BR-09 |
| UC-12 | Ask the campus assistant | All staff users, AI service | 4.21 (AI-07, AI-08) |
| UC-13 | Generate and review report | Business administrator, Finance, Procurement and Sustainability officers, AI service | 4.16 (FR-17), 4.22 (AI-09, AI-10), 6.1 |
| UC-14 | View asset history and audit log | Asset custodian, Business administrator | 4.14 (FR-15, FR-18) |

TODO Zayed: write the fourteen descriptions below this line in the format above (the comment shows the exact format).
