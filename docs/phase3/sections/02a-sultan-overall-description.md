# 2. Overall Description

## 2.1 Product Perspective

Dawra Campus is a new system. It doesn't replace KU's current asset register; it runs next to it. When an item is transferred or disposed of in Dawra Campus, staff can export the record and update the official register themselves. There is no direct connection to KU's systems in this version (Phase 2, section 5).

The table shows who and what sits outside the system and how they connect to it. We will draw the full context diagram in Phase 4.

<!-- widths: 2600,6760 -->
| Outside the system | How it connects |
|---|---|
| Staff in the nine roles | Use the website in a browser (section 2.3) |
| AI service provider | Gets only the fields it needs for a task and sends back suggestions, scores, explanations and draft text through one AI adapter (sections 3.3 and 4.16–4.22) |
| KU's current asset register | Not connected. Staff update it using the transfer and end-of-life records we export (FR-11.7) |
| Finance, Procurement and EHS offices | Take part through the Finance officer, Procurement officer and Sustainability officer roles, and set the policy values in Appendix C |
| Hosting and database provider | Runs the website, database and file storage (section 2.4) |

Inside, the system is split into these parts, covered one by one in sections 4.2 to 4.22: accounts and access; departments and settings; asset records; listings, requests, search and reservations; approvals; transfers; inspections and maintenance; end-of-life actions; history, audit and notifications; reports and sustainability; and the AI services.

## 2.2 Product Functions

**Classic features**

- Create user accounts and give each person roles for their department.
- Register assets with their details, photos and documents.
- List unused items once the owning department approves.
- Submit, track, change and cancel requests, and search the listed items.
- Reserve items for a limited time without the same item going to two people.
- Send every approval to the right person, with a reason for any rejection.
- Record transfers from approval to handover and receipt, updating the owner and location.
- Record inspections, repairs and their costs.
- Propose, approve and record donation, recycling, retirement and disposal.
- Show each asset's full history, keep a log that can't be edited, send notifications and produce reports.

**AI features**

- Suggest a category, tags and a description when an asset is registered.
- Match requests to suitable items by meaning, after the normal rules remove items that don't qualify, with a score and an explanation.
- Suggest what to do with an old item and explain why.
- Answer questions and help draft requests through a chat assistant, always asking before changing anything.
- Write report summaries using the numbers from the normal reports.
- Record which AI model produced each result and whether the user accepted it, and fall back to the normal features if AI isn't available.

**Sustainability**

- Calculate waste diverted, avoided purchases, reuse rate, repair success, extra asset life, money saved and estimated carbon saved.
