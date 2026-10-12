## 3.2 Hardware Interfaces

The system shall work through a browser on ordinary laptops, desktop computers and phones. Users shall be able to upload asset photographs taken with a phone camera, subject to the file limits in FR-04.1. The prototype shall not require dedicated hardware; barcode and RFID scanners are outside its scope.

## 3.3 Software Interfaces

The following interfaces connect Dawra Campus to other software and storage services. The proposed technologies are listed in section 2.4. Their exact versions and settings will be recorded in the setup guide after testing.

<!-- widths: 900,2000,4400,2060 -->
| ID | Interface | Data exchanged | Purpose |
|---|---|---|---|
| SI-01 | PostgreSQL database through Django | The application reads and writes accounts, departments, assets, requests, reservations, approvals, transfers, maintenance records, AI output records and audit entries. The database returns the requested records or the result of an update. | Store and retrieve project records while preserving the access rules and data integrity requirements. |
| SI-02 | AI adapter and the models listed in section 2.4 | The adapter sends only approved fields needed for the task, such as asset descriptions, categories, specifications, condition, quantity and request details. It processes model responses and returns suggestions, matching scores where relevant, explanations, confidence information or its unavailability, and the model identifier and version. | Keep AI connections separate from the main application and check responses before presenting them to users. |
| SI-03 | Persistent file storage; provider to be confirmed | The application sends uploaded photographs and supporting documents, together with their record references. Storage returns a file reference and allows authorised retrieval. Uploads must meet the file type, size and quantity limits in FR-04.1. | Keep supporting evidence available after restarts and redeployments while restricting access to authorised users. |
| SI-04 | Export and printable views | Transfer exports contain the asset ID, quantity, ownership and custody details, locations, approvals and handover and receipt confirmations. Audit exports contain the selected audit entries. Report exports contain the selected filters, records and totals. | Support manual checking against the existing KU asset register under FR-11.7 and audit export under FR-18.3. CSV and printable report export remains Desirable under FR-17.3. |

The system shall apply the user's access permissions before retrieving data for AI processing, displaying files or producing exports. Exported records support manual reconciliation; the prototype shall not connect directly to KU's asset register, finance, procurement or identity systems, as stated in C-04.

If the AI service is unavailable, times out or returns an invalid response, the system shall show a clear message and provide the relevant classic search, form or report. It shall preserve the user's input and keep all normal permission and approval checks in place, as required by AI-13, NFR-07 and BR-15.

## 3.4 Communications Interfaces

- The system shall use HTTPS for browser communication to protect data while it is being sent.
- The AI adapter shall communicate with external AI services through HTTPS using JSON, a structured format for exchanging data. It shall check that each response contains the fields required for its task before using it.
- If an AI request fails or remains unanswered, the system shall display a failure or timeout message and make the relevant classic alternative available within 15 seconds of the original request. Any retries shall remain within that time limit. User input shall be preserved, as required by NFR-07.
- The system shall keep AI service credentials on the server and use them only to authenticate service calls. It shall exclude user passwords, service credentials and unnecessary personal data from AI input content and ordinary logs.
- The system shall provide notifications inside the application and show them only to users who may access the related record, as required by FR-16. Email delivery is a Future enhancement under FR-16.6 and is not required for the prototype.