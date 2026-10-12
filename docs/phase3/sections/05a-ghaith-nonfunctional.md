# 5. Other Nonfunctional Requirements

<!-- GUIDANCE (Ghaith). SRS template p.18–19. Refine your Phase 1 NFR-01 to NFR-12 into the template's
headings. Keep the IDs and make every requirement measurable (Chapter 3 slide 11: "95% of searches
return within 2 seconds", not "fast"). Keep the test conditions from Phase 1: 500 synthetic assets,
10 departments, 50 requests, five concurrent users. -->

## 5.1 Performance Requirements

TODO Ghaith: NFR-02 (search time), NFR-11 (larger dataset), AI response time and the 15-second fallback (NFR-07), cold start on the hosting candidate measured separately (Phase 2 section 7).

## 5.2 Safety Requirements

TODO Ghaith: harm that could come from wrong records or AI advice: unsafe equipment transferred without inspection, hazardous items (electronics, lab equipment) needing EHS consultation (BR-09), disposal of an item that should have been reused. Link to BR-08 and BR-09.

## 5.3 Security Requirements

TODO Ghaith: NFR-03 (authentication, server-side authorisation, hashed passwords, secrets out of Git), NFR-04 (privacy, synthetic data, minimal data to AI), NFR-05 (audit cannot be edited), role-and-permission test matrix.

## 5.4 Software Quality Attributes

TODO Ghaith: NFR-01 usability, NFR-06 explainability, NFR-07 reliability/fallback, NFR-08 maintainability, NFR-09 portability, NFR-10 data integrity, NFR-12 fairness. A table | ID | Attribute | Requirement | Priority | works well.
