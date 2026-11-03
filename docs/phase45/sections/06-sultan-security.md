# 6. Security

Our rule is default deny. A user can do only what one of their roles allows, inside their own department, assigned work or own requests (SRS section 2.3). The server checks this for every action, including actions proposed through the assistant (FR-02.2, NFR-03). A refused action is blocked, the user is told which role is needed, and the attempt goes to the audit log (FR-02.3).

## 6.1 Security Boundaries

**Table 6.1 Security boundaries**

<!-- widths: 2000,2100,3960,1300 -->
| Boundary | What crosses it | How we protect it | SRS |
|---|---|---|---|
| Browser and application | Pages, forms and uploads | HTTPS only. Every page except sign-in needs a signed-in user (FR-02.1). Five failed sign-ins block the account for 15 minutes (FR-02.4). A session ends after 30 minutes without activity. | 3.4, NFR-03 |
| Application and database | All business records | Only the application can reach the database. The connection details are kept in environment variables on the host, never in Git. Passwords are stored as salted hashes. | SI-01, NFR-03 |
| Application and file storage | Photos and documents | The storage bucket is private. A file opens through a short-lived link, given only after an access check. File type and size are checked before upload (FR-04.1). | SI-03 |
| Application and AI Provider | Approved text fields out, AI output in | The AI key stays on the server. Only the fields a task needs are sent, never passwords or personal data. Each response is checked for its required fields and saved as a suggestion, never written straight into a business record. | SI-02, NFR-04, BR-15 |
| Business and technical administration | Role changes | A business administrator authorises a role and a system administrator applies it. Neither can approve releases, transfers, spending or disposal through that role (BR-01). | UC-01 |

## 6.2 Access Matrix

Table 6.2 shows who may do what. It covers all nine roles in the SRS plus the AI services.

**Table 6.2 Access matrix**

<!-- widths: 2160,720,720,720,720,720,720,720,720,720,720 -->
| Action | Req | Dept rep | Cust | Bus admin | Proc | Fin | Maint | Sust | Sys admin | AI |
|---|---|---|---|---|---|---|---|---|---|---|
| Sign in and see own tasks (FR-02, FR-16) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | no |
| Register or edit an asset (FR-04) | — | ✓ | ✓ | — | — | — | — | — | — | suggest |
| Confirm another user's asset record | — | A | A | — | — | — | — | — | — | no |
| Prepare a listing (FR-06) | — | ✓ | ✓ | — | — | — | — | — | — | no |
| Release a listing (BR-04) | — | A | — | — | — | — | — | — | — | no |
| Search published listings (FR-08) | V | V | V | V | V | V | V | V | V | rank |
| Submit a resource request (FR-07) | ✓ | — | — | — | — | — | — | — | — | draft |
| Approve a resource request (BR-03) | — | A | — | — | — | — | — | — | — | no |
| Review matches and choose one (AI-05) | ✓ | — | — | — | — | — | — | — | — | rank |
| Request a hold and start a transfer (FR-09) | ✓ | — | — | — | — | — | — | — | — | no |
| Confirm a hold | — | A | A | — | — | — | — | — | — | no |
| Approve a transfer: release and receipt (BR-05) | — | A | — | — | — | — | — | — | — | no |
| Approve a transfer: policy stage (BR-06) | — | — | — | — | A | A | — | — | — | no |
| Record handover or receipt (FR-11, BR-13) | — | — | ✓ | — | — | — | — | — | — | no |
| Confirm an avoided purchase for the receiving department (BR-18) | — | A | — | — | — | — | — | — | — | no |
| Report a defect (FR-12) | — | ✓ | ✓ | — | — | — | ✓ | — | — | no |
| Inspect and record repair work (FR-13) | — | — | — | — | — | — | ✓ | — | — | no |
| Approve repair spending (BR-07) | — | A | — | — | — | A | — | — | — | no |
| Propose an end-of-life action (FR-14) | — | ✓ | ✓ | — | — | — | — | — | — | suggest |
| Review or write off an end-of-life action (BR-08) | — | — | — | — | — | A | — | A | — | no |
| Review an official report (BR-10) | — | — | — | A | V | A | — | A | — | draft |
| View an asset's history (UC-14) | — | V | V | V | — | — | V | — | — | no |
| Search and export the audit log (FR-18.3) | — | — | — | ✓ | — | — | — | — | — | no |
| Keep departments, categories and thresholds (FR-03) | — | — | — | ✓ | — | — | — | — | — | no |
| Authorise a role assignment (BR-01) | — | — | — | A | — | — | — | — | — | no |
| Create accounts and apply authorised roles | — | — | — | — | — | — | — | — | ✓ | no |
| Run backups and manage service keys (6.5) | — | — | — | — | — | — | — | — | ✓ | no |
| Ask the campus assistant (AI-07) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | answer |

**Key.** Req = Requester, Dept rep = Department representative, Cust = Asset custodian, Bus admin = Business administrator, Proc = Procurement officer, Fin = Finance officer, Maint = Maintenance staff, Sust = Sustainability officer, Sys admin = System administrator. ✓ = can do it within their own scope. A = decides an assigned approval stage, never for their own record (BR-02). V = view only. — = refused. The finance and procurement policy stages apply only when BR-06 or BR-07 needs them. For the AI: suggest, rank, draft and answer mean it produces a suggestion that a person accepts, corrects or rejects (BR-15). "no" means the AI never does it.

## 6.3 Audit Log

The audit log records every creation, change, state change, approval decision, role change, refused action and response to an AI output (FR-18.1). It also records failed sign-ins and every backup and restore.

**Table 6.3 What each audit entry records**

<!-- widths: 2200,7160 -->
| Field | What it holds |
|---|---|
| Who | userId and the role used. Entries made by the system itself have no user. |
| What | The action, the record type and the record ID, for example "approve, Transfer, 214". |
| When | The date and time, to the second. |
| Why | The reason, which is required for every rejection, request for changes and cancellation (BR-20). |
| Before and after | The values of the changed fields before and after the action. |

Entries can only be added. The application's database account can insert into AuditLog but cannot update or delete it, so a mistake is fixed with a new entry that points to the original (BR-17, FR-18.2). A business administrator can search the log and export it as CSV (FR-18.3). Custodians and department representatives see the history of their own assets (UC-14). Entries are kept for the retention period (TBD-7).

## 6.4 Data Storage

**Table 6.4 Where data is stored**

<!-- widths: 2400,3300,3660 -->
| Data | Where | Notes |
|---|---|---|
| Business records (all entities in section 8) | PostgreSQL database on Neon (SRS section 2.4) | Only made-up test data in the prototype (C-03, DR-02). |
| Photos and documents | A private S3-compatible storage bucket | The Attachment table keeps the file key, type and size, not the file itself (SI-03). |
| AI requests and results | AiSuggestion and MatchRecommendation tables (D4) | Each row keeps the model version and the user's response (AI-12). |
| Passwords, database and AI keys | Environment variables on the Render host | Never in Git. The .env file is ignored. |
| Backups | A separate private backup bucket | See section 6.5. |

## 6.5 Backup and Restore

- **Database.** An automatic backup runs every night at 02:00 UAE time and goes to the backup bucket. We keep the last 7 daily copies and the last 4 weekly copies. We also take a manual backup before each release and before the demo.
- **Uploads.** The uploads bucket keeps old versions of each file, and a full copy goes to the backup bucket every week.
- **Targets.** We lose at most one day of data, and a full restore takes no more than one hour.
- **Restore test.** Once a month and before the demo, the system administrator restores the latest backup into a new, empty database and storage folder. The test passes when the record counts in Asset, ResourceRequest, Transfer, Approval and AuditLog match the source, 10 random attachments open, a requester, a custodian and a business administrator can each sign in and open one record, and the newest audit entry matches the source. The result and the time taken are written to the audit log (DR-03, NFR-13).

## 6.6 Integration Points

**Table 6.5 Integration points**

<!-- widths: 500,2300,2200,3060,1300 -->
| # | Integration point | Data | Protection | SRS |
|---|---|---|---|---|
| 1 | Browser and Django application | Pages, forms and uploads | HTTPS, sign-in, server-side permission checks | UI-01 to UI-14, 3.4 |
| 2 | Application and PostgreSQL on Neon | All records | Private connection details in environment variables | SI-01 |
| 3 | Application and file storage | Photos and documents | Private bucket and short-lived links | SI-03 |
| 4 | AI adapter and AI Provider (gpt-4.1-mini-2025-04-14 and text-embedding-3-small) | Approved text fields out, AI output in | HTTPS with JSON, key on the server, 15-second limit, then the classic alternative | SI-02, AI-13 |
| 5 | Exports | CSV and printable transfer, audit and report exports | Access check before every export | SI-04 |
| 6 | Email | Notifications | Not in the prototype; notifications stay in the application | FR-16.6 |
