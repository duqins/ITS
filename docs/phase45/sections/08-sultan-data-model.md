# 8. Data Model and ER Diagram

This section shows what the system stores and how the records link to each other. It covers the entity-relationship (ER) diagram, every relationship with its cardinality and the data dictionary. The data stores in the data-flow diagrams (section 2) use the same entity names.

## 8.1 Entity-Relationship Diagram

Figure 8.1 is the core ER diagram from the lab ("ER solution: core entities"). We kept its six entities and their keys. We added the three links that the lab slide mentions but does not draw: each recommendation belongs to one request, each transfer is for one asset, and each transfer records the user who gave the final approval. We also turned modelVersion into a link to the ModelVersion table, so every recommendation points to the exact model that made it.

![Figure 8.1 Core ER diagram (from the lab)](images/erd-core.png)

Figures 8.2 to 8.4 show the full design. We split it into three parts so it is easy to read. Grey dashed boxes belong to another part and only show where a link goes.

![Figure 8.2 Users, roles and access](images/erd-users.png)

![Figure 8.3 Assets, requests and matching](images/erd-assets-requests.png)

![Figure 8.4 Approvals, maintenance and end of life](images/erd-approvals-lifecycle.png)

A few design choices explain the diagrams:

- **One approval belongs to one record.** An approval is for a request, a listing, a transfer, a maintenance record or an end-of-life action. Only one of these five keys is filled in each approval.
- **One impact comes from one action.** Each sustainability impact comes from exactly one completed transfer, repair or end-of-life action.
- **Several roles per user.** A user can hold several roles in different departments through UserRole. This is how one person can be a requester in one department and a custodian in another (SRS section 2.3).
- **Who did what is in the audit log.** We keep the person behind each action in AuditLog, so the other tables do not need a "done by" key. Entries made by the system itself have no user, which is why AuditLog has 0..1 on the user side.
- **The final approver.** approverId in Transfer is the user who gave the final approval. Every stage before it is stored in Approval, following Table 5.2 of the SRS.

## 8.2 Relationships and Cardinalities

Table 8.1 lists all 34 relationships. "1 to 0..*" means one record on the left can link to many records on the right, and each record on the right links to exactly one on the left. "0..1" means the link is optional.

**Table 8.1 Relationships and cardinalities**

<!-- widths: 500,2000,1250,2000,3610 -->
| # | Entity | Cardinality | Entity | What it means |
|---|---|---|---|---|
| 1 | Department | 1 to 0..* | User | Each user belongs to one department. |
| 2 | Department | 1 to 0..* | Asset | Each asset is owned by one department. |
| 3 | Department | 1 to 0..* | UserRole | Each role is given for one department. |
| 4 | User | 1 to 0..* | UserRole | A user can hold several roles. |
| 5 | Role | 1 to 0..* | UserRole | A role can be given to many users. |
| 6 | User (requester) | 1 to 0..* | ResourceRequest | Each request has one requester. |
| 7 | User (custodian) | 1 to 0..* | Asset | Each asset has one custodian. |
| 8 | User (final approver) | 0..1 to 0..* | Transfer | A transfer has no final approver until it is approved, then exactly one. |
| 9 | User (approver) | 0..1 to 0..* | Approval | An approval gets its approver when someone decides it. |
| 10 | User | 1 to 0..* | Notification | Each notification goes to one user. |
| 11 | User | 0..1 to 0..* | AuditLog | Most entries come from a user. Entries made by the system have none. |
| 12 | Category | 1 to 0..* | Asset | Each asset is in one category. |
| 13 | Category | 1 to 0..* | ResourceRequest | Each request asks for one category. |
| 14 | Asset | 1 to 0..* | Listing | An asset can be listed more than once in its life. |
| 15 | Listing | 1 to 0..* | Reservation | A listing can have several holds for different quantities. |
| 16 | ResourceRequest | 1 to 0..* | Reservation | A request can hold items from one or more listings. |
| 17 | Reservation | 1 to 0..1 | Transfer | A confirmed hold can become one transfer. |
| 18 | Asset | 1 to 0..* | MatchRecommendation | An asset can be recommended for many requests. |
| 19 | ResourceRequest | 1 to 0..* | MatchRecommendation | A request gets a ranked list of matches. |
| 20 | ModelVersion | 1 to 0..* | MatchRecommendation | Each recommendation records the model that made it. |
| 21 | Asset | 1 to 0..* | Transfer | An asset can be transferred many times in its life. |
| 22 | ResourceRequest | 1 to 0..* | Transfer | A request can be fulfilled by one or more transfers. |
| 23 | ResourceRequest | 0..1 to 0..* | Approval | The department approval of a request (BR-03). |
| 24 | Listing | 0..1 to 0..* | Approval | The release approval of a listing (BR-04). |
| 25 | Transfer | 0..1 to 0..* | Approval | The release, receipt and policy approvals of a transfer (BR-05, BR-06). |
| 26 | MaintenanceRecord | 0..1 to 0..* | Approval | The cost approvals of a repair (BR-07). |
| 27 | EndOfLifeAction | 0..1 to 0..* | Approval | The sustainability and finance approvals (BR-08). |
| 28 | Asset | 1 to 0..* | Inspection | An asset can be inspected many times. |
| 29 | Asset | 1 to 0..* | MaintenanceRecord | An asset can have many repairs. |
| 30 | Inspection | 0..1 to 0..* | MaintenanceRecord | A repair can start from an inspection or be reported directly. |
| 31 | Asset | 1 to 0..* | EndOfLifeAction | An end-of-life action is for one asset. |
| 32 | Transfer | 0..1 to 0..1 | SustainabilityImpact | A completed transfer has one impact record. |
| 33 | MaintenanceRecord | 0..1 to 0..1 | SustainabilityImpact | A completed repair has one impact record. |
| 34 | EndOfLifeAction | 0..1 to 0..1 | SustainabilityImpact | A completed end-of-life action has one impact record. |

## 8.3 Data Dictionary

Table 8.2 describes each entity. Every entity has its own ID as the primary key, and its foreign keys are shown in the ER diagrams. IDs and quantities are whole numbers, money is in AED with two decimals, and dates are stored with the time.

**Table 8.2 Data dictionary**

<!-- widths: 2100,3100,4160 -->
| Entity | What it stores | Main attributes |
|---|---|---|
| Department | A university department or unit. | name, code |
| User | A staff account. | name, email, accountStatus (active, inactive or blocked) |
| Role | One of the nine roles in SRS section 2.3. | name |
| UserRole | A role given to a user for one department. | status (requested, authorised, active or removed) |
| Category | A type of item, such as office chair or monitor. | name, subcategory, unit, procurementControlled, specialHandling, emissionFactor (kg CO2e per unit), factorSource |
| Asset | One registered item or batch of the same item. | name, description, condition (New, Good, Fair, Poor or Not working), status (AS-01 to AS-10), quantity, availableQty, reservedQty, location (building and room), value, purchaseDate, verifiedOn |
| Listing | An offer of an asset for reuse by other departments. | quantity, availableFrom, restrictions, releaseReason, status (LS-01 to LS-06) |
| ResourceRequest | A department's need for an item. | purpose, specifications, quantity, minCondition, urgency, deliveryLocation, requiredBy, status (RQ-01 to RQ-10) |
| Reservation | A short hold on a listing for one request. | quantity, expiresAt, status (RV-01 to RV-06) |
| MatchRecommendation | One ranked match between a request and an asset. | score (0 to 100), confidence (0 to 1), explanation, userResponse (accepted, rejected or overridden), overrideReason |
| ModelVersion | The AI model used for a task. | task (classification, matching, advice, assistant or reports), modelName, version, activeFrom |
| Transfer | The move of an asset from one department to another. | quantity, status (TR-01 to TR-09), handedOverAt, receivedAt, disputeNote |
| Approval | One approval stage for one record. | stage (Table 5.2 of the SRS), decision, reason, decidedAt, status (AT-01 to AT-05) |
| Inspection | A check of an asset's condition and safety. | inspectedOn, conditionFound, safeToUse, notes |
| MaintenanceRecord | A repair work order. | defect, estimatedCost, actualCost, outcome, status (MW-01 to MW-09) |
| EndOfLifeAction | A decision to retain, donate, disassemble, recycle or dispose of an asset. | action, quantity, destination, reason, ehsConsulted, dataErased, status (EL-01 to EL-06) |
| SustainabilityImpact | The benefit of one completed transfer, repair or end-of-life action. | wasteDivertedKg, avoidedPurchaseAED, co2eSavedKg, factorVersion, dataStatus (measured, estimated or synthetic) |
| Notification | A message to one user about one record. | recordType, recordId, message, sentAt, readAt |
| AuditLog | Who did what and when. Entries are never changed or deleted (BR-17). | action, recordType, recordId, beforeValue, afterValue, reason, createdAt |

