# 3. Stakeholder Analysis

## 3.1 Identification of Stakeholders

The stakeholders were identified from the project description, the Phase 1 slides, and a walkthrough of the asset process from registration to transfer, maintenance, and disposal. They include people who use the system, approve decisions, operate the software, define the project requirements, or benefit from its results.


| Group | Stakeholders | Interest in the system |
|---|---|---|
| Operational users | Department representatives, asset custodians, requesters, maintenance staff | Register, find, request, transfer, inspect, and maintain assets. |
| Decision makers | Administrators, procurement officers, finance officers | Control approvals, costs, ownership changes, and policy compliance. |
| Sustainability | Sustainability officers | Encourage reuse and repair and measure environmental benefits. |
| Technical operations | System administrators | Keep the system secure, available, and correctly configured. |
| Client | Lab instructors | Clarify requirements and evaluate the project deliverables. |
| Development team | Student project team | Design, build, test, document, and demonstrate the system. |
| Institutional beneficiaries | University management and departments | Reduce unnecessary purchases and improve asset use and reporting. |

## 3.2 Stakeholder Roles and Responsibilities

Permissions are assigned according to each person's role. Technical access does not give someone business approval authority; for example, a system administrator cannot approve an asset transfer simply because they manage the software.


| Stakeholder | Main responsibilities | Main system permissions |
|---|---|---|
| Department representative | Confirm department needs and approve releasing or receiving assets. | Manage department requests and listings; approve release and receipt. |
| Asset custodian | Keep asset details, condition, location, and custody accurate. | Register and update assets; request maintenance; confirm handover. |
| Requester | Search for resources and submit and track requests. | Search listings; create requests; reserve items; review recommendations. |
| Administrator | Manage business workflows, categories, departments, and exceptions. | Review records; route approvals; manage workflow settings; run reports. |
| Procurement officer | Check policy, ownership, and whether reuse can avoid a purchase. | Review and approve policy-controlled transfers and end-of-life actions. |
| Finance officer | Validate values, costs, savings, and financial thresholds. | Review financial data and approve actions above agreed limits. |
| Maintenance staff | Inspect assets and record repair work, cost, and outcome. | Manage assigned maintenance records and update asset condition. |
| Sustainability officer | Review reuse, repair, donation, recycling, and disposal options. | Review recommendations; manage sustainability factors; validate indicators. |
| System administrator | Manage accounts, roles, configuration, backup, and security. | Perform technical administration without automatic business approval rights. |
| Lab instructors | Clarify scope and review the project's work. | Use reviewer access and make course acceptance decisions. |
| Student project team | Gather requirements and build, test, and document the prototype. | Use development and test access with synthetic data. |

## 3.3 Stakeholder Needs and Expectations


| Stakeholder | Main need | Expected system support |
|---|---|---|
| Department representative | Control department requests and assets. | Clear approval tasks and confirmed ownership, custody, and location changes. |
| Asset custodian | Maintain an accurate asset record. | Simple updates, evidence uploads, reminders, and full life-cycle history. |
| Requester | Find suitable resources quickly. | Useful search, explainable matches, easy requests, and visible status. |
| Administrator | Apply one consistent process. | Configurable workflows, exception handling, notifications, and audit records. |
| Procurement officer | Confirm reuse and policy compliance. | Internal availability, policy checks, and documented approvals. |
| Finance officer | Trust financial and savings figures. | Controlled values, calculation evidence, and financial reports. |
| Maintenance staff | Receive complete work information. | Work queues, asset history, repair forms, costs, and status updates. |
| Sustainability officer | Extend asset life and measure benefits. | Reuse-first recommendations and transparent sustainability calculations. |
| System administrator | Operate a secure and maintainable service. | Access controls, monitoring, backup, audit logs, and AI fallback. |
| Lab instructors | See that the project meets the assignment. | Traceable requirements, a working prototype, tests, and honest limitations. |
| Student project team | Work within a realistic semester scope. | Clear priorities, open questions, test data, and acceptance criteria. |

## 3.4 Stakeholder-to-Feature Mapping

AI features only provide recommendations. People remain responsible for approving transfers, repair spending, donation, recycling, disposal, financial values, and user roles. Approval thresholds that depend on university policy will be confirmed with the client in later phases.


| Feature | Primary users | Main data needed | Approval owner |
|---|---|---|---|
| Asset registration and classification | Asset custodian, department representative | Asset details, owner, location, condition, value, photos, documents, AI tags | Custodian or department representative confirms the record and AI suggestions. |
| Asset publication | Custodian, department representative | Availability, quantity, condition, restrictions, owner | Releasing department representative. |
| Resource requests | Requester, department representative | Purpose, specifications, quantity, urgency, location, required date | Department representative where the request commits the department. |
| Search and filtering | Requester, procurement officer | Category, condition, location, quantity, availability, status | No approval required. |
| AI matching | Requester, department representative | Asset and request data, compatibility score, explanation, confidence | User chooses a match; AI does not approve it. |
| Reservation | Requester, custodian | Asset availability, quantity, requester, expiry | Releasing custodian or department representative. |
| Transfer and receipt | Department representatives, custodians, administrator | Approvals, custody, location, collection, condition, confirmation | Releasing and receiving departments; finance/procurement when required. |
| Maintenance and repair | Custodian, maintenance staff, finance | Defect, inspection, work, cost, outcome, condition | Department representative; finance above an agreed threshold. |
| Sustainable-action recommendation | Sustainability officer, custodian, administrator | Condition, demand, cost, material, value, sustainability factors | Authorised human roles; AI only recommends. |
| LLM assistant | All authorised users | User role, permitted records, question or intended action | User confirms changes; normal approval workflow still applies. |
| Reports and dashboards | Administrators, finance, procurement, sustainability | Assets, requests, transfers, maintenance, savings, sustainability indicators | Relevant data owner reviews official reports. |
| User and access management | Administrator, system administrator | Identity, department, role, account status, audit history | Business administrator authorises the role; system administrator applies it. |
