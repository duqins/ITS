# 1. Context Diagram

Figure 1.1 shows Dawra Campus as one process, numbered 0, and everyone who sends data to it or gets data from it. The diagram shows the boundary of the system only. It has no data stores and no steps inside the system.

We grouped the nine roles from SRS section 2.3 into six external entities, by what they do with the system. The AI Provider is the outside service that runs our AI models (SRS section 2.4 and SI-02). It only receives the approved text fields it needs and sends back AI output. It never changes our records. Notifications stay inside the application (FR-16), so there is no email service on the diagram.

![Figure 1.1 Context diagram of Dawra Campus](images/dfd-context.png)

Each flow on the context diagram groups several smaller flows. Section 2 shows where each part goes.

**Table 1.1 External entities**

<!-- widths: 1750,2350,2630,2630 -->
| External entity | Roles from the SRS | Sends to the system | Gets from the system |
|---|---|---|---|
| Requester | Requester | Resource requests, match choices and assistant questions (UC-04 to UC-07, UC-12) | Ranked matches, request status and assistant answers |
| Asset Custodian | Asset custodian | Asset details, handover records, and defect and end-of-life reports (UC-02, UC-03, UC-09 to UC-11) | Suggested categories, transfer tasks and asset history (UC-14) |
| Maintenance Staff | Maintenance staff | Inspection and repair records (UC-10) | Work orders |
| Approvers | Department representative, finance officer, procurement officer | Approval decisions (UC-08, Table 5.2 of the SRS) | Approval tasks, and finance and reuse reports |
| Sustainability Officer | Sustainability officer | End-of-life reviews (UC-11) | Review tasks and the impact report (UC-13) |
| Administrators | Business administrator, system administrator | Account details, role assignments, settings and report requests (UC-01, UC-13) | Account status, and operational and audit reports |
| AI Provider | None (outside service) | AI output: suggestions, vectors, rankings with reasons and draft text | Approved text fields only (SI-02, NFR-04) |
