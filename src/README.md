# Dawra Campus app (Phase 6)

The Django application of our design. Each app matches a part of the component diagram in the Phase 4 and 5 design (section 11):

| App | What it does |
|---|---|
| `accounts` | Sign-in, the nine roles, role switching and the server-side permission checks |
| `core` | Page layout and the home page |
| `assets` | Asset registration, listings and search |
| `resource_requests` | Resource requests |
| `transfers` | Approvals, holds (reservations) and transfers |
| `audit` | The state rules of section 10.2 and the audit history |
| `notifications` | In-app notifications |
| `sustainability` | Sustainability indicators (section 12) |
| `reports` | Request and transfer report with CSV export |
| `ai` | The AI adapter and the AI services |

## Run it on your laptop (PowerShell)

From the repository folder (`ITS`), one line at a time:

```
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r src\requirements.txt
cd src
copy .env.example .env
```

Open `src\.env` and set `DEBUG=True`. Then:

```
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Open http://127.0.0.1:8000 and sign in. The demo users all use the password `dawra-demo-2026` (local only; set `DEMO_PASSWORD` before seeding anywhere else):

| Username | Role and department |
|---|---|
| `eng.rep` | Department representative, Engineering |
| `eng.custodian` | Asset custodian, Engineering |
| `comp.requester` | Requester, Computing |
| `comp.rep` | Department representative and Requester, Computing (switch role at the top) |
| `comp.custodian` | Asset custodian, Computing |
| `finance.officer` | Finance officer |
| `procurement.officer` | Procurement officer |
| `sustainability.officer` | Sustainability officer |
| `business.admin` | Business administrator |
| `business.admin2` | Business administrator (a second one, so a role request has an independent authoriser) |
| `maintenance.staff` | Maintenance staff |
| `system.admin` | System administrator |

All demo data is synthetic. Besides the records of the demo script, `seed_demo` adds nine transfers that finished over the last five months (so the dashboard and its savings graph have a history), more published items, and two approvals waiting longer than 3 working days (overdue). The history goes through the real workflow and only its dates are moved back. Money only comes from monitors, the one category with a cited replacement price. `python manage.py seed_demo --without-history` creates only the demo script records and the section 12 worked example; the tests use it.

## AI features

The AI features use the Claude API. Put the key in `src\.env` as `ANTHROPIC_API_KEY=...` (never commit it). Without a key the app still runs: the AI panels say the AI is unavailable and the classic path is offered.

## Rules that come from the design

- Every status change goes through `audit/lifecycle.py`, which allows only the moves of the state diagrams (section 10.2) and writes an audit entry.
- Permissions are checked on the server for every page (`accounts/permissions.py`), using the access matrix of section 6.
- `available + reserved + allocated` can never be more than an asset's quantity (a database constraint), so the last item cannot go to two people.
- Roles are given only on the Administration page (UI-14): a Business administrator requests the role, a second Business administrator authorises it and the System administrator applies it (BR-01, BR-02). The Django administration site (`/admin/`) shows roles but cannot change them. The two administrators reach it from Administration for what they maintain: staff accounts (System administrator), and departments and categories (Business administrator). No demo user is a superuser.
- Photos and PDF documents of assets (FR-04.1) are stored in the database, because Render's disk is emptied on every deploy. Pillow checks that a photo is a real JPG or PNG, refuses pictures over 16 megapixels (memory on the free plan) and keeps a 1568-pixel copy and a small copy for lists. The AI classification reads the first two photos.
- An asset can be saved as a draft early, but a second person can confirm it only when its mandatory fields are filled (FR-04.2). A possible duplicate needs an extra tick (FR-04.5). Items checked more than 90 days ago show "Verification needed" until the custodian verifies them again (FR-06.4, BR-16). Custodians and representatives see how many on their home page, which opens the list of those assets (UI-02). The demo data has one: the Computing standing desks, last checked 120 days ago.
- The thresholds still marked TBD in the SRS are in `dawra/settings.py` under `DAWRA`. TBD-1 (Finance approval) uses AED 5,000 as our prototype value.
