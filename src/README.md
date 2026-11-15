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
| `maintenance.staff` | Maintenance staff |
| `system.admin` | System administrator (also opens `/admin/`) |

All demo data is synthetic.

## AI features

The AI features use the Claude API. Put the key in `src\.env` as `ANTHROPIC_API_KEY=...` (never commit it). Without a key the app still runs: the AI panels say the AI is unavailable and the classic path is offered.

## Rules that come from the design

- Every status change goes through `audit/lifecycle.py`, which allows only the moves of the state diagrams (section 10.2) and writes an audit entry.
- Permissions are checked on the server for every page (`accounts/permissions.py`), using the access matrix of section 6.
- `available + reserved + allocated` can never be more than an asset's quantity (a database constraint), so the last item cannot go to two people.
- The thresholds still marked TBD in the SRS are in `dawra/settings.py` under `DAWRA`. TBD-1 (Finance approval) uses AED 5,000 as our prototype value.
