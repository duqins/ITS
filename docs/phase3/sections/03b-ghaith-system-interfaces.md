## 3.2 Hardware Interfaces

<!-- GUIDANCE (Ghaith). SRS template p.17. Barcode and RFID hardware are out of scope (Phase 2 section 1),
so this is short: ordinary laptops and phones, photo upload from a phone camera through the browser. -->

TODO Ghaith: two or three sentences.

## 3.3 Software Interfaces

<!-- Describe each connection to other software: name and version (or candidate), the data going in and
out, and its purpose. Give each an ID (SI-01 …). Must include: the database; the AI service adapter
(what fields are sent – only approved, necessary fields – and what comes back: suggestion, score,
explanation, confidence, model identifier and version); file storage; the export used to reconcile
with the existing KU asset register (no live integration – out of scope). -->

<!-- widths: 900,2000,4400,2060 -->
| ID | Interface | Data exchanged | Purpose |
|---|---|---|---|

TODO Ghaith: fill the rows, then one paragraph on what happens when the AI service is unavailable (link to AI-13 and BR-15).

## 3.4 Communications Interfaces

TODO Ghaith: HTTPS for all browser traffic, HTTPS/JSON to the AI provider with a timeout (the 15-second fallback target from Phase 1 NFR-07), in-application notifications (email is optional, not required for the prototype), no credentials or unnecessary personal data in AI requests or logs.
