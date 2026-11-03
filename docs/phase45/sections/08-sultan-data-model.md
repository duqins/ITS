# 8. Data Model and ER Diagram

This section shows what the system stores and how the records link to each other. It covers the entity-relationship (ER) diagram, every relationship with its cardinality and the data dictionary. The data stores in the data-flow diagrams (section 2) use the same entity names.

## 8.1 Entity-Relationship Diagram

Figure 8.1 is the core ER diagram from the lab ("ER solution: core entities"). We kept its six entities and their keys. We added the three links that the lab slide mentions but does not draw: each recommendation belongs to one request, each transfer is for one asset, and each transfer records the user who gave the final approval. We also turned modelVersion into a link to the ModelVersion table, which we added to the figure, so every recommendation points to the exact model that made it. Each line has a name, read from the first entity to the second, for example "Department owns Asset".

![Figure 8.1 Core ER diagram (from the lab)](images/erd-core.png)

Figures 8.2 to 8.5 show the full design with every entity, key and relationship and the main attributes. Table 8.2 lists every attribute. We split it into four parts so it is easy to read. Grey dashed boxes belong to another part and only show where a link goes.

![Figure 8.2 Users, roles and access](images/erd-users.png)

![Figure 8.3 Assets, requests and matching](images/erd-assets-requests.png)

![Figure 8.4 Approvals, maintenance and end of life](images/erd-approvals-lifecycle.png)

![Figure 8.5 AI suggestions, attachments and transfer details](images/erd-ai-attachments.png)

These design choices explain the diagrams:

- **One approval belongs to one record.** An approval is for a request, a listing, a transfer, a maintenance record or an end-of-life action. Only one of these five keys is filled in each approval. Attachment works the same way with its five owner keys. We use real foreign keys here, not a record type and an ID, so the database itself checks every link. Notification and AuditLog use recordType and recordId instead, because they can point to any table and no rule depends on them. The other stages in SRS Table 5.2 are kept on their own records: a role assignment in UserRole.status, the confirmation of a new asset in its state and verifiedOn, a hold in Reservation.status, and the owners' review of an official report in AuditLog, with AI report drafts also kept in AiSuggestion.
- **One impact comes from one action.** Each sustainability impact comes from exactly one completed transfer, repair or end-of-life action. It keeps the carbon saving as a low and a high value, because the factors we use give a range (section 12).
- **Several roles per user.** A user can hold several roles in different departments through UserRole. This is how one person can be a requester in one department and a custodian in another (SRS section 2.3).
- **Who did what.** Most actions are kept in AuditLog with the person who did them, so most tables do not need a "done by" key. We keep a direct key only where the SRS asks for it: the requester, the custodian, the final approver, the receiving custodian (FR-11.1) and the inspector (FR-12.1). Entries made by the system itself have no user, which is why AuditLog has 0..1 on the user side. AuditLog also keeps the role that was used (FR-18.1) and the reviewer who confirms an avoided purchase (BR-18, SU-03).
- **Versions.** Each request, listing, transfer, repair and end-of-life action keeps a version number. An approval stores the version it was given for and the approver's role, so a decision on an older version is refused (FR-10.6, FR-10.7).
- **The final approver.** approverId in Transfer is the user who gave the final approval. Every stage before it is stored in Approval, following Table 5.2 of the SRS.
- **Transfer details.** Transfer records the releasing and receiving departments, the receiving custodian, the new location, the planned date and the delivery arrangement (FR-11.1). It also keeps assetId and requestId, which its Reservation already links to. These are copies for fast lookup, and they must match the reservation. The lab diagram has them too.
- **AI suggestions.** Every AI output that is not a match is kept in AiSuggestion: category suggestions, sustainable-action advice, assistant answers and report drafts. Each row keeps its confidence, explanation, model version and the user's response (AI-12). assetId is filled only when the suggestion is about one asset.
- **Attachments.** Photos and documents for assets, transfers, inspections, repairs and end-of-life actions are kept in Attachment, with one owner for each file (FR-04.1, FR-11.1, FR-12.1). The file itself is in storage, and the table keeps its key (section 6.4). This is also how one asset keeps several photos. Attachment has its own key and is not a weak entity, because a file can belong to five kinds of record, not to one owner.
- **Location and asset age.** location is a composite attribute made of campus, building and room. assetAge is a derived attribute and is not stored. It is worked out from purchaseDate and today's date.

## 8.2 Relationships and Cardinalities

Table 8.1 lists all 45 relationships. "1 to 0..*" means one record on the left can link to many records on the right, and each record on the right links to exactly one on the left. "0..1" means the link is optional.

**Table 8.1 Relationships and cardinalities**

<!-- widths: 450,1800,1550,1150,1800,2610 -->
| # | Entity | Relationship | Cardinality | Entity | What it means |
|---|---|---|---|---|---|
| 1 | Department | employs | 1 to 0..* | User | Each user belongs to one department. |
| 2 | Department | owns | 1 to 0..* | Asset | Each asset is owned by one department. |
| 3 | Department | scopes | 1 to 0..* | UserRole | Each role is given for one department. |
| 4 | User | holds | 1 to 0..* | UserRole | A user can hold several roles. |
| 5 | Role | used in | 1 to 0..* | UserRole | A role can be given to many users. |
| 6 | User | submits | 1 to 0..* | ResourceRequest | Each request has one requester. |
| 7 | User | is custodian of | 1 to 0..* | Asset | Each asset has one custodian. |
| 8 | User | gives final approval | 0..1 to 0..* | Transfer | A transfer has no final approver until it is approved, then exactly one. |
| 9 | User | decides | 0..1 to 0..* | Approval | An approval gets its approver when someone decides it. |
| 10 | User | receives | 1 to 0..* | Notification | Each notification goes to one user. |
| 11 | User | performs | 0..1 to 0..* | AuditLog | Most entries come from a user. Entries made by the system have none. |
| 12 | Category | classifies | 1 to 0..* | Asset | Each asset is in one category. |
| 13 | Category | classifies | 1 to 0..* | ResourceRequest | Each request asks for one category. |
| 14 | Asset | is offered in | 1 to 0..* | Listing | An asset can be listed more than once in its life. |
| 15 | Listing | is held by | 1 to 0..* | Reservation | A listing can have several holds for different quantities. |
| 16 | ResourceRequest | places | 1 to 0..* | Reservation | A request can hold items from one or more listings. |
| 17 | Reservation | becomes | 1 to 0..1 | Transfer | A confirmed hold can become one transfer. |
| 18 | Asset | is matched in | 1 to 0..* | MatchRecommendation | An asset can be recommended for many requests. |
| 19 | ResourceRequest | receives | 1 to 0..* | MatchRecommendation | A request gets a ranked list of matches. |
| 20 | ModelVersion | produces | 1 to 0..* | MatchRecommendation | Each recommendation records the model that made it. |
| 21 | Asset | is moved by | 1 to 0..* | Transfer | An asset can be transferred many times in its life. |
| 22 | ResourceRequest | is fulfilled by | 1 to 0..* | Transfer | A request can be fulfilled by one or more transfers. |
| 23 | ResourceRequest | needs | 0..1 to 0..* | Approval | The department approval of a request (BR-03). |
| 24 | Listing | needs | 0..1 to 0..* | Approval | The release approval of a listing (BR-04). |
| 25 | Transfer | needs | 0..1 to 0..* | Approval | The release, receipt and policy approvals of a transfer (BR-05, BR-06). |
| 26 | MaintenanceRecord | needs | 0..1 to 0..* | Approval | The cost approvals of a repair (BR-07). |
| 27 | EndOfLifeAction | needs | 0..1 to 0..* | Approval | The sustainability and finance approvals (BR-08). |
| 28 | Asset | checks | 1 to 0..* | Inspection | An asset can be inspected many times. |
| 29 | Asset | has | 1 to 0..* | MaintenanceRecord | An asset can have many repairs. |
| 30 | Inspection | leads to | 0..1 to 0..* | MaintenanceRecord | A repair can start from an inspection or be reported directly. |
| 31 | Asset | ends with | 1 to 0..* | EndOfLifeAction | Each end-of-life action is for one asset. |
| 32 | Transfer | creates | 0..1 to 0..1 | SustainabilityImpact | A completed transfer has one impact record. |
| 33 | MaintenanceRecord | creates | 0..1 to 0..1 | SustainabilityImpact | A completed repair has one impact record. |
| 34 | EndOfLifeAction | creates | 0..1 to 0..1 | SustainabilityImpact | A completed end-of-life action has one impact record. |
| 35 | Department | releases | 1 to 0..* | Transfer | Each transfer has one releasing department. |
| 36 | Department | receives | 1 to 0..* | Transfer | Each transfer has one receiving department. |
| 37 | User | receives as custodian | 1 to 0..* | Transfer | Each transfer names the custodian who will receive the asset. |
| 38 | User | inspects | 1 to 0..* | Inspection | Each inspection is done by one person. |
| 39 | ModelVersion | produces | 1 to 0..* | AiSuggestion | Each AI suggestion records the model that made it. |
| 40 | Asset | gets | 0..1 to 0..* | AiSuggestion | A suggestion can be about one asset, or about none. |
| 41 | Asset | has | 0..1 to 0..* | Attachment | Photos and documents of an asset. |
| 42 | Transfer | has | 0..1 to 0..* | Attachment | Handover and receipt documents. |
| 43 | Inspection | has | 0..1 to 0..* | Attachment | Inspection photos. |
| 44 | MaintenanceRecord | has | 0..1 to 0..* | Attachment | Repair evidence. |
| 45 | EndOfLifeAction | has | 0..1 to 0..* | Attachment | EHS and data-erasure evidence (BR-09). |

## 8.3 Data Dictionary

Table 8.2 describes each entity. Every entity has its own ID as the primary key, and its foreign keys are shown in the ER diagrams. IDs and quantities are whole numbers, money is in AED with two decimals, and dates are stored with the time. The Source column gives the Phase 3 IDs each entity comes from.

**Table 8.2 Data dictionary**

<!-- widths: 1850,2400,3410,1700 -->
| Entity | What it stores | Main attributes | Source |
|---|---|---|---|
| Department | A university department or unit. | name, code | FR-03.1 |
| User | A staff account. | name, email, accountStatus (active, inactive or blocked) | FR-01, FR-02 |
| Role | One of the nine roles in SRS section 2.3. | name | FR-01, SRS 2.3 |
| UserRole | A role given to a user for one department. | status (requested, authorised, active or removed) | FR-01, BR-01 |
| Category | A type of item, such as office chair or monitor. | name, subcategory, unit, procurementControlled, specialHandling, emissionFactorLow and emissionFactorHigh (kg CO2e per unit), factorSource, factorVersion | FR-03.2, FR-03.4, SU-07 |
| Asset | One registered item or batch of the same item. | name, description, condition (New, Good, Fair, Poor or Not working), status (AS-01 to AS-10), quantity, availableQty, reservedQty, allocatedQty, specifications, location (campus, building and room), value, purchaseDate, verifiedOn, plannedRetirementDate, revisedRetirementDate, version; serialNumber and storesData for IT assets; material and dimensions for furniture; assetAge (worked out, not stored) | FR-04.1, FR-05, SU-06, BR-09 |
| Listing | An offer of an asset for reuse by other departments. | quantity, availableFrom, restrictions, releaseReason, version, status (LS-01 to LS-06) | FR-06.1 |
| ResourceRequest | A department's need for an item. | purpose, specifications, quantity, minCondition, urgency, deliveryLocation, requiredBy, version, status (RQ-01 to RQ-10) | FR-07.1, FR-07.9 |
| Reservation | A short hold on a listing for one request. | quantity, expiresAt, status (RV-01 to RV-06) | FR-09.1, BR-12 |
| MatchRecommendation | One ranked match between a request and an asset. | score (0 to 100), confidence (0 to 1), explanation, userResponse (accepted, rejected or overridden), overrideReason, createdAt | AI-04, AI-05, AI-12 |
| AiSuggestion | Any other AI output and the user's answer to it. | task (classification, advice, assistant or report), suggestion, confidence (0 to 1), explanation, userResponse, correctedValue, createdAt | AI-01, AI-06, AI-07, AI-09, AI-12 |
| ModelVersion | The AI model used for a task. | task, modelName, version, activeFrom | AI-12.1 |
| Transfer | The move of an asset from one department to another. | quantity, toLocation, plannedDate, deliveryArrangement (collection or delivery), transferCostAED, vanTrips, distanceKm, version, status (TR-01 to TR-09), handedOverAt, receivedAt, disputeNote | FR-11.1, BR-13 |
| Approval | One approval stage for one record. | stage (a request, listing, transfer, repair or end-of-life stage of SRS Table 5.2), decision, reason, approverRole, recordVersion, decidedAt, status (AT-01 to AT-05) | FR-10, BR-02 |
| Inspection | A check of an asset's condition and safety. | inspectedOn, conditionFound, safeToUse, findings, followUp | FR-12.1 |
| MaintenanceRecord | A repair work order. | defect, estimatedCost, actualCost, parts, labourHours, outcome, conditionAfter, version, status (MW-01 to MW-09) | FR-13.4 |
| EndOfLifeAction | A decision to retain, donate, disassemble, recycle or dispose of an asset. | action, quantity, destination, reason, ehsConsulted, dataErased, version, status (EL-01 to EL-06) | FR-14.1, FR-14.5, BR-08 |
| SustainabilityImpact | The benefit of one completed transfer, repair or end-of-life action. | wasteDivertedKg, avoidedPurchaseAED, replacementCostAED, replacementCostSource, co2eLowKg, co2eHighKg, factorVersion, dataStatus (measured, estimated or synthetic) | SU-01 to SU-09 |
| Attachment | One photo or document for one record. | fileName, fileType (JPG, PNG or PDF), sizeKB, storageKey, uploadedAt | FR-04.1, FR-11.1, FR-12.1 |
| Notification | A message to one user about one record. | recordType, recordId, message, sentAt, readAt | FR-16 |
| AuditLog | Who did what and when. Entries are never changed or deleted (BR-17). | role, action, recordType, recordId, beforeValue, afterValue, reason, createdAt | FR-18.1, NFR-05 |
