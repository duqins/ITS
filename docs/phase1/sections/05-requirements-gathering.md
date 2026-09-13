# 5. Requirements Gathering

## 5.1 Methodology

Requirements are gathered iteratively. The following techniques are used in Phase 1 and continued through Phases 2 and 3:

<!-- widths: 2000,2800,3000,1560 -->
| Technique | Purpose | Participants / sources | Timing |
|---|---|---|---|
| Document analysis | Extract mandated functionality, constraints and deliverables. | Project description (Fall 2026), Phase 1 lab slides, SRS template (IEEE-style) in the appendix. | Phase 1 (complete) |
| Client interview / Q&A | Clarify ambiguities (e.g., approval thresholds, sustainability factors, data availability). | Lab instructors during lab sessions. | Phases 1–3 |
| Stakeholder role-play interviews | Elicit needs for each of the nine roles. | Team members assigned as role owners; scripted interview guide. | Phase 2 |
| Survey | Gauge how staff/students would search for and request equipment, and trust AI recommendations. | Short online questionnaire to peers and faculty (10–20 responses). | Phases 2–3 |
| Process walkthrough / workshop | Model as-is and to-be workflows; identify states and approval stages. | Whole team; whiteboard session; output used for use-case and state diagrams. | Phase 1 (initial), Phase 3 |
| Benchmarking | Study existing asset-management and reuse platforms (e.g., university surplus portals, Warp It, open-source asset trackers) for feature ideas and terminology. | Public product documentation. | Phase 2 |
| Prototyping | Validate UI and AI explanation formats with mockups. | Team and instructors. | Phases 4–5 |

## 5.2 Summary of Gathered Requirements

The requirements gathered so far group into six areas:

- **Asset and inventory management:** full asset record with metadata, photos and documents; life-cycle status; department and custodian ownership.
- **Marketplace and requests:** publication of surplus; structured requests; search/filter; reservations; request tracking.
- **Workflow and governance:** approval stages for release, reservation, transfer, receipt, donation, recycling, disposal; custody and location changes; notifications; audit log; role-based permissions for nine roles.
- **Maintenance and life cycle:** defect reporting, inspection, repair, refurbishment, cost capture, condition update; complete event history.
- **AI services:** classification and tagging; semantic matching with compatibility score and human-readable explanation; prioritisation by suitability, urgency, cost and sustainability; sustainable-action recommendation; LLM assistant; generative reports; confidence information, user overrides, model-version tracking and fallback behaviour.
- **Sustainability and reporting:** waste diversion, avoided purchases, asset-life extension, reuse rate, financial savings, estimated carbon reductions; conventional and AI-generated reports and dashboards.

## 5.3 Prioritisation of Requirements

Requirements are prioritised with the MoSCoW method, aligned to the project description's three tiers: essential prototype functions (Must), desirable extensions (Should), and possible future enhancements (Could/Won't for this semester).

<!-- widths: 1800,2800,4760 -->
| Priority | Meaning | Requirement groups |
|---|---|---|
| Must have | Required for the Phase 6 prototype and final demonstration. | Authentication and RBAC; department and asset registration; publication; requests; search/filter; reservation; approval and transfer workflow; maintenance tracking; AI classification; AI matching with score and explanation; sustainability indicators; notifications; basic operational and AI-generated reports. |
| Should have | Expected in the final submission if time allows; adds significant value. | Sustainable-action recommendation with confidence; prioritisation model with transfer/repair cost and carbon estimate; LLM assistant for search and request submission; audit-log viewer; dashboard summaries; user overrides with justification. |
| Could have | Nice to have; implemented only after all Must/Should items are stable. | Demand prediction; assistant handling of policy guidance and asset-history questions; monthly management bulletins; image-based classification; accessibility refinements beyond baseline. |
| Won't have (this semester) | Explicitly excluded (see scope). | ERP/finance integration; payments; RFID/barcode hardware; custom model training; native mobile apps; production hosting. |
