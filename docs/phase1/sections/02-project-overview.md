# 2. Project Overview

## 2.1 High-Level Description of the Proposed System

The system is a web-based internal marketplace and asset-life-cycle platform for a university campus. It operates in two layers:

- **Classic baseline layer.** Departments register assets with full metadata, publish surplus or underutilised items, and submit resource requests. Structured search and filtering, reservations, multi-stage approval workflows, transfer and custody tracking, inspection/maintenance/repair records, end-of-life actions (donation, recycling, disposal), role-based access control and conventional operational reports.
- **AI-enhanced layer.** An asset-classification service suggests categories, tags and standardised descriptions; a semantic matching engine ranks assets against requests using meaning, compatibility, condition, quantity, location, urgency and cost; a sustainable-action recommender proposes retain/transfer/repair/refurbish/donate/disassemble/recycle/dispose with an explanation and confidence; an LLM assistant provides natural-language search, request submission and guidance; and generative reporting turns operational data into monthly summaries and management bulletins.

Every AI output is a recommendation. Authorised human users remain accountable for approvals and high-impact actions (transfer, disposal, donation), and the system must be able to explain each recommendation and fall back to classic behaviour when an AI service is unavailable or low-confidence.

## 2.2 Background and Context

Traditional university asset-management systems record ownership, location, purchase information and disposal status. They do not support intelligent internal reuse, semantic matching between available assets and departmental requests, prediction of future demand, or measurement of the environmental and financial benefits of circular resource management. As a result, departments over-purchase, storage areas fill with idle equipment, and the institution cannot report on avoided purchases, reuse rates or carbon impact. Circular-economy practice and campus sustainability targets create a clear demand for a system that closes this gap.

The project is a lab-based running project for COSC 336 at Khalifa University. It simulates real-world engineering practice: planning, feasibility, requirements, architecture, design, implementation, testing and documentation, with all work tracked in a shared GitHub repository.

## 2.3 Business Goals and Objectives

<!-- widths: 700,2600,6060 -->
| # | Goal | Objective (what the system must achieve) |
|---|---|---|
| G1 | Reduce unnecessary purchases | Make existing surplus assets visible and easy to request so departments reuse before they buy. |
| G2 | Extend asset life | Track inspections, maintenance and repairs so assets are kept in service longer and retired only as a last option. |
| G3 | Improve matching quality | Use semantic matching and ranking so requests are met by functionally suitable assets even when terminology differs. |
| G4 | Ensure accountable workflows | Provide transparent, auditable approval, transfer and custody processes with role-based access. |
| G5 | Measure sustainability value | Calculate and report waste diversion, reuse rate, asset-life extension, financial savings and estimated carbon-emission reductions. |
| G6 | Integrate AI responsibly | Deliver explainable, confidence-scored recommendations with human oversight and fallback behaviour. |
| G7 | Learning objective | Apply and compare classic and AI-enhanced software engineering across the full SDLC. |

## 2.4 Project Constraints

<!-- widths: 2200,7160 -->
| Constraint | Description |
|---|---|
| Timeline | Eight phases across the Fall 2026 semester (Phase 1 week of 14 Sep 2026; final submission and demonstration week of 23 Nov 2026). The course sets the deadlines; this plan uses the earlier lab-slide dates pending instructor confirmation. |
| Budget | No monetary budget. Only free/open-source frameworks, free-tier cloud or LLM APIs, and university-provided lab resources may be used. |
| Team resources | Student team of three members working part-time alongside other courses; limited AI/ML experience; no dedicated designer, tester or DevOps engineer. |
| Data | No access to real university asset data. The prototype will use synthetic and anonymised sample data; sustainability figures (e.g., carbon factors) will use published estimates and must be reported with their uncertainty. |
| Process | Git and GitHub are mandatory; commit history is graded (10 % of each phase). Regular, meaningful, individually-authored commits are required. |
| Technology | Web application; must run on a grader's machine from the repository with documented setup. AI features depend on external LLM/embedding APIs with rate limits. |
| Policy and ethics | Must respect university procurement, ownership, privacy and safety policies; AI must not make final decisions on disposal, donation or transfer. |

## 2.5 Scope of the Project

### In scope

- User management and authentication with role-based access for the nine defined roles (Section 3).
- Department management, asset registration and inventory with photographs and supporting documents.
- Circular resource marketplace: publication of surplus/underutilised/unwanted assets visible to authorised campus users.
- Departmental resource requests with category, purpose, specifications, quantity, preferred condition, urgency, location and required date.
- Structured search and filtering; reservations and request tracking.
- Approval workflows for release, reservation, transfer, receipt, donation, recycling and disposal.
- Transfer management (approval, collection/delivery, custody change, new location, confirmation, documents).
- Asset life-cycle history from acquisition to retirement; maintenance and repair module with costs and condition updates.
- Conventional operational reports; notifications; audit logging.
- AI: classification/tagging, semantic matching with compatibility score and explanation, prioritisation/ranking, sustainable-action recommendation, LLM assistant, generative reports.
- Sustainability indicators and dashboard summaries.
- Full documentation across all eight phases and a working prototype with demonstration.

### Out of scope

- Integration with the university's live ERP, finance or procurement systems (interfaces will be simulated).
- Financial transactions, purchasing or payment processing.
- Physical logistics (vehicle scheduling, barcode/RFID hardware), beyond recording collection/delivery arrangements.
- Training custom machine-learning models from scratch; the project uses pre-trained models and hosted LLM/embedding services.
- Mobile native applications (the web UI will be responsive instead).
- Production deployment, high-availability hosting and formal security certification.

## 2.6 Assumptions

- The lab instructors act as the client; their project description and slides are the authoritative statement of needs.
- Synthetic data of realistic size (hundreds of assets, tens of departments and requests) is sufficient to demonstrate all functionality.
- A free-tier hosted LLM and embedding API will remain available throughout the semester, and the team may fall back to a smaller open-source model if not.
- All team members have GitHub accounts, Git installed and access to the shared repository by 15 September 2026.
- Deadlines follow the Phase 1 lab slides (week of 14 Sep 2026 onward); the project description lists a tentative later schedule and the earlier slide dates are used for planning until the instructors confirm the schedule.

## 2.7 Key Terms

<!-- widths: 2400,6960 -->
| Term | Meaning in this project |
|---|---|
| Asset | Any physical item owned by the university that is tracked individually or in quantity: furniture, computers, lab equipment, books, office materials. |
| Surplus / underutilised asset | An asset its department no longer needs (surplus) or uses rarely (underutilised) and is willing to release to another department. |
| Listing | A published surplus asset visible on the campus marketplace. |
| Resource request | A department's structured description of something it needs (category, specifications, quantity, urgency, location, date). |
| Match | A pairing of a listing with a request, produced by the AI matching engine with a compatibility score and an explanation. |
| Custodian | The person responsible for an asset's physical condition and location at any given time. |
| Transfer | The approved movement of an asset from one department or custodian to another. |
| Life-cycle status | The current stage of an asset: registered, in use, published, reserved, in transfer, under maintenance, donated, recycled, disposed or retired. |
| Sustainable action | The recommended next step for an asset: retain, transfer, repair, refurbish, donate, disassemble, recycle or dispose. |
| Avoided purchase | A purchase that did not happen because a request was satisfied from an existing asset; its value is the estimated replacement cost. |
| Waste diversion | Items or kilograms kept out of disposal through reuse, repair, donation or recycling. |

## 2.8 Expected Benefits

<!-- widths: 2800,6560 -->
| Beneficiary | Benefit |
|---|---|
| Departments | Faster access to needed equipment without procurement lead time; reduced storage of idle items. |
| University finance | Avoided purchases and quantified savings; better visibility of asset value and utilisation. |
| Sustainability office | Measured waste diversion, reuse rate and carbon-emission reductions to support campus targets and reporting. |
| Asset custodians and maintenance staff | Single, auditable life-cycle record; structured inspection and repair workflow. |
| Administrators | Transparent approval trail; role-based control of high-impact actions. |
| Project team | Practical experience of the full SDLC, responsible AI integration and team-based Git workflows. |
