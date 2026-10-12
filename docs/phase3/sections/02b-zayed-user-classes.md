## 2.3 User Classes and Characteristics



Dawra Campus has nine staff roles. One person may hold several roles, with each assignment limited to named departments. The active role and department determine what that person can view and do; a second role does not remove the normal approval steps. Requesters, Asset custodians and Department representatives are the primary user classes because they carry out the everyday request and transfer process. The other classes provide policy review, specialist work or administration. The frequencies below are expected prototype use patterns, not measured KU usage.

<!-- widths: 1700,2500,1300,1300,1300,1260 -->
| User class | Main tasks in the system | Frequency of use | Technical expertise | Privilege level | Importance |
|---|---|---|---|---|---|
| Department representative | Review department needs; confirm asset records; approve listing release, requests, transfers and repair spending. | Daily or when a decision is needed | Basic browser and form skills; understands department responsibilities | Department records and assigned approval tasks | Primary |
| Asset custodian | Register and verify assets; prepare listings; confirm holds, handover and receipt; report defects and record completion evidence. | Daily | Basic browser skills and knowledge of asset condition and location | Operational records for assigned assets and departments | Primary |
| Requester | Search published listings; submit and track requests; review matches; request reservations and start transfers. | When a resource is needed | Basic browser and search skills | Own requests and linked records; authorised published listings | Primary |
| Business administrator | Maintain departments and categories; authorise role assignments; route exceptions; review operational reports and audit records. | Daily or weekly | Comfortable with administrative forms and business workflows | Business configuration and oversight within assigned departments | Secondary |
| Procurement officer | Review procurement-controlled transfers and relevant policy and reuse reports. | When policy approval or reporting is needed | Procurement-policy and record-review skills | Relevant records; transfer approval only when BR-06 applies | Secondary |
| Finance officer | Review threshold-controlled transfers and repair spending; approve end-of-life write-offs; review cost and savings reports. | When a financial decision is needed | Financial-review and reporting skills | Relevant financial records and assigned approval stages | Secondary |
| Maintenance staff | Inspect assigned assets; assess faults and repair costs; record approved work, parts, costs and resulting condition. | Daily or when work is assigned | Equipment inspection and maintenance skills; basic form skills | Assigned inspection and work-order records | Secondary |
| Sustainability officer | Review reuse-first end-of-life proposals, special-handling evidence and sustainability indicators. | When an action or report needs review | Sustainability and environmental-record skills | Relevant asset evidence; sustainability review and report review | Secondary |
| System administrator | Create and deactivate accounts; apply authorised role assignments; operate access, security and recovery settings. | During setup and as needed | Technical administration and security skills | Technical configuration; no automatic business approval rights | Secondary |


### 2.3.1 Permission Matrix



<!-- widths: 1800,940,940,940,940,940,940,940,980 -->
| Role | Assets | Listings | Requests | Reservations | Transfers | Maintenance | End-of-life | Users and roles |
|---|---|---|---|---|---|---|---|---|
| Department representative | C,V,E,A | C,V,E,A | V,A | V,E,A | V,A | C,V,A | C,V,E | - |
| Asset custodian | C,V,E,A | C,V,E | V | V,E,A | V,E | C,V,E | C,V,E | - |
| Requester | V | V | C,V,E | C,V,E | C,V | - | - | - |
| Business administrator | V | V | V | V | V | V | V | C,V,A |
| Procurement officer | V | V | V | V | V,A | - | V | - |
| Finance officer | V | V | V | V | V,A | V,A | V,A | - |
| Maintenance staff | V | V | - | - | - | C,V,E | V | - |
| Sustainability officer | V | V | V | - | V | V | V,A | - |
| System administrator | - | V | - | - | - | - | - | C,V,E |

C = create; V = view; E = edit permitted fields or record an operational confirmation; A = decide an assigned approval or confirmation stage; - = no access through that role alone.

**How to read the matrix.** Each permission is limited to the user's department, assigned work or linked request. Viewing a published listing gives access to its marketplace summary, not the owning department's private asset documents. Requesters can view the listed asset summary and their own linked transactions. All nine roles may search authorised published listings; the System administrator's V under Listings is this ordinary staff access, not permission to edit business records. A user who needs another function must also hold its required role.

**Approval limits.** A is permission to decide only the stage assigned in Table 5.2. Asset confirmation is by an Asset custodian or Department representative. Listing release and request approval are by the relevant Department representative. A reservation hold is confirmed by the releasing Asset custodian or Department representative. Transfers require both department representatives, followed by Finance and/or Procurement only when BR-06 applies. Repair spending requires the owning Department representative and Finance only when BR-07 applies. End-of-life review is by Sustainability, then Finance write-off approval. BR-02 blocks the creator or requester from deciding their own approval task even if they hold several roles; an eligible alternate is used under TBD-9.

**Editing limits.** E does not authorise changing an already approved decision or editing an audit entry. A Requester can edit a draft, revise a request with renewed approval where required, or cancel a permitted request or reservation. Custodians record verification, handover and receipt; Maintenance staff record assessment and work results. Department representatives may maintain their department's listings and cancel permitted reservation holds. End-of-life C and E allow the department or custodian to prepare a proposal and record completion evidence after approval. Approved quantity, value, recipient or action changes require a new decision under FR-10.7.

**Administration and reports.** Business administrator C,V,A under Users and roles covers requesting and authorising role assignments; System administrator C,V,E covers account maintenance and applying assignments already authorised under BR-01. Neither receives transfer, spending or disposal approval through technical or business administration alone. For reports, the Business administrator reviews operational figures, Finance reviews cost and savings figures, and Sustainability reviews sustainability figures (BR-10); Procurement can inspect relevant reports but is not a substitute for those data owners.

