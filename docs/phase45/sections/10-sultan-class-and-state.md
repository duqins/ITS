# 10. Class and State Diagrams

## 10.1 Class Diagram

The class diagram turns the entities in section 8 into classes with attributes, operations and associations. Every association has the same multiplicities as the ER diagram (Table 8.1). Keys are not shown as attributes, because each foreign key becomes an association. Like the ER diagram, it is split into four figures so it stays readable.

We use the notation from the lab slides:

- **Visibility and types.** "-" marks a private attribute and "+" a public operation, each with its type, for example "- status: AssetStatus" and "+ reserve(qty: int): void".
- **Aggregation (hollow diamond).** A department groups its assets, but an asset can move to another department, so it does not depend on the department.
- **Composition (filled diamond).** A user's role assignments, a request's specification and an asset's attachments cannot exist without their owner. RequestSpecification is kept inside the ResourceRequest table, so it is not a separate entity in section 8. Attachments of transfers, inspections, repairs and end-of-life actions work the same way (Table 8.1, rows 41 to 45).
- **Generalization (hollow triangle).** ITAsset and FurnitureAsset are kinds of Asset with extra attributes. ITAsset knows whether the device stores data, which decides if a data-erasure record is needed (BR-09).
- **Derived attribute.** /assetAge is worked out from purchaseDate and is not stored.

Condition is an enumeration with the values New, Good, Fair, Poor and Not working (FR-04.1). AssetStatus, ListingStatus, RequestStatus, ReservationStatus, TransferStatus, WorkOrderStatus, EndOfLifeStatus and ApprovalStatus hold the state codes from SRS section 4.1. Sections 10.2 to 10.5 show four of them.

![Figure 10.1 Class diagram: people and access](images/class-people.png)

![Figure 10.2 Class diagram: assets and listings](images/class-assets.png)

![Figure 10.3 Class diagram: requests, matching and transfers](images/class-requests.png)

![Figure 10.4 Class diagram: approvals and life cycle](images/class-lifecycle.png)

**Table 10.1 Main operations and the requirements they carry out**

<!-- widths: 3200,3600,2560 -->
| Operation | What it does | SRS |
|---|---|---|
| Asset.confirm(by) | Confirms a new asset record by a second user. | Table 5.2, BR-02 |
| Listing.publish() | Makes a listing visible after its release is approved. | FR-06, BR-04 |
| ResourceRequest.approve(by) | Opens a request after department approval. | FR-07, BR-03 |
| MatchRecommendation.override(reason) | Records that the requester chose another item, and why. | AI-05.2 |
| Reservation.confirm(by) | Holds the quantity without allocating it twice. | FR-09, BR-11, BR-12 |
| Transfer.confirmReceipt() | Moves ownership, custody and location to the receiver. | FR-11, BR-13 |
| Approval.approve(by), reject(by, reason) | Records one decision by an eligible user. | FR-10, BR-02, BR-20 |
| MaintenanceRecord.complete(after) | Closes a repair with its cost and the new condition. | FR-13.4, BR-07 |
| AiSuggestion.correct(value) | Keeps the AI output and the user's correction. | AI-12.3, BR-15 |
| SustainabilityImpact.calculate() | Works out the impact of one completed action (section 12). | SU-01 to SU-09 |
| AuditLog.record(actor, action) | Adds an entry that can never be changed. | FR-18.1, BR-17 |

## 10.2 Asset State Diagram

Figure 10.5 shows the asset life cycle from SRS section 4.1.1. Active is a composite state that holds AS-02 In service and AS-03 In storage, so a repair, a transfer or an end-of-life proposal can start from either of them. When a repair is completed, a transfer is received or cancelled, or an end-of-life action is rejected, the asset goes back to In service or In storage. AS-07 to AS-10 are final states.

![Figure 10.5 Asset state diagram](images/state-asset.png)

## 10.3 Resource Request State Diagram

Figure 10.6 follows SRS section 4.1.3. RQ-03 Open and RQ-04 Reservation requested sit inside the composite state "Active request", because the requester can cancel from both. A change to an approved request sends it back for department approval (BR-03).

![Figure 10.6 Resource request state diagram](images/state-request.png)

## 10.4 Transfer State Diagram

Figure 10.7 follows SRS section 4.1.5. TR-01 to TR-03 sit inside the composite state "Waiting for approvals", because the transfer can be rejected or cancelled at any of these stages (BR-05, BR-06). TR-03 is used only when BR-06 applies. Ownership changes only when receipt is confirmed (BR-13).

![Figure 10.7 Transfer state diagram](images/state-transfer.png)

## 10.5 Approval State Diagram

Figure 10.8 follows SRS section 4.1.8. Every approval stage in Table 5.2 of the SRS uses this life cycle. A request for changes ends the task, and resubmitting the record creates a new task (SRS section 4.1.8). Every state change in sections 10.2 to 10.5 also writes an audit entry (FR-18.1).

![Figure 10.8 Approval state diagram](images/state-approval.png)
