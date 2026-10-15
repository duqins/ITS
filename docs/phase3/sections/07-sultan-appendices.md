# Appendix A: Glossary

<!-- widths: 2600,6760 -->
| Term | Meaning |
|---|---|
| Asset | Anything the university owns that we track, or a batch of identical items with a quantity |
| Listing | An item a department has offered to other departments |
| Request | What a department needs, written as a form |
| Reservation | Holding some units of a listing for a limited time; not an approval |
| Transfer | Moving an item from one department to another, after approval |
| Custodian | The person responsible for an item's condition and location |
| Department representative | The person who approves listings, requests, receipts and spending for a department |
| Approval task | One decision waiting for someone with the right role (section 4.1.8) |
| Work order | A repair or maintenance job, from report to completion |
| End-of-life action | What happens to an item that leaves service: keep, donate, take apart, recycle or dispose |
| Compatibility score | How well an item fits a request, from 0 to 100; not a probability and not an approval |
| Confidence | How sure the AI is about its answer, shown separately from the score |
| Eligibility check | The normal rules that remove items that can't be used before the AI ranks the rest (BR-14) |
| Avoided purchase | Something the department didn't have to buy because it got an existing item (BR-18) |
| Waste diverted | Items kept out of the bin through reuse, repair, donation, taking apart or recycling |
| kg CO2e | Kilograms of carbon dioxide equivalent, the unit for carbon estimates |
| EARS | The "When / While / If … then / Where" way of writing requirements from the Chapter 3 slides |
| EHS | Environment, Health and Safety, the KU office we check with for special items |
| TBD | Something we still need the instructors to confirm (Appendix C) |

# Appendix B: Analysis Models

For this phase, our analysis models are the use-case diagram and descriptions in section 7 and the state tables in section 4.1. The other diagrams come later, as the project description sets out: context and data-flow diagrams in Phase 4, and the UML class, sequence, activity and state diagrams, the ER diagram and the AI workflow diagram in Phase 5. They will use the same IDs as this document.

# Appendix C: To Be Determined List

<!-- widths: 900,4560,2100,1800 -->
| ID | Open question | Our proposal | Used in |
|---|---|---|---|
| TBD-1 | Item value at which a transfer also needs Finance approval | KU Finance to set | BR-06, FR-11.2 |
| TBD-2 | Repair cost at which Finance approval is also needed | KU Finance to set | BR-07, FR-13.2 |
| TBD-3 | How long a reservation is held | 5 working days | BR-12, FR-09.3 |
| TBD-4 | How old an item's last check can be before it must be checked again | 90 days | BR-16, FR-06.4 |
| TBD-5 | When an approval counts as overdue | 3 working days | FR-10.5 |
| TBD-6 | Where the carbon factors for each category come from | A published factor set, to agree | SU-07, DEP-03 |
| TBD-7 | How long records and audit entries are kept | Same as KU's record policy | FR-18.4, DR-03 |
| TBD-8 | Which categories need special handling, and the EHS steps | To confirm with EHS | BR-09, FR-14.4 |
| TBD-9 | Who approves when a department has only one representative | Named by the Business administrator | BR-02 |
| TBD-10 | Which KU office would own the system | Facilities Management (from Phase 2) | 2.1 |

# Appendix D: Team Contributions and AI Use

<!-- widths: 2200,4300,2860 -->
| Member | Sections | Branch |
|---|---|---|
| Sultan Almheiri (100065654) | 1; 2.1–2.2; 2.5–2.7; 4.1–4.15; 5.5; 6; Appendices A–D; document build | phase3/sultan-requirements |
| Zayed Alfadli (100064657) | 2.3; 3.1; 7 | phase3/zayed |
| Ghaith Alhinaai (100066185) | 2.4; 3.2–3.4; 4.16–4.22; 5.1–5.4 | phase3/ghaith |

**AI use.**  We used Claude (Anthropic) as a writing and checking assistant. All requirements, design decisions and analysis are our own and build on our Phase 1 and Phase 2 work. Claude helped us organise our sections, refine the wording of drafts we had written, and keep requirement IDs and cross-references consistent. It also generated the Word document and slides from our files, so the content of both comes from our work and Claude only handled the formatting. To verify the result, we checked it against the project description and the Chapter 3 slides, ran a check that every ID we refer to exists, and read the final document page by page. Each of us reviewed, edited and approved our own sections, and a teammate reviewed every change in a GitHub pull request before it was merged.
