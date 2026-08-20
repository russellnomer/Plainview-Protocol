# The Plainview Protocol

**Activism as Code for the Sovereign Citizen**

> “We do not believe in virtue signals. We believe in evidence, facts, transparency, and action.”
> — **Russell Nomer**, Founder (Plainview, NY)

The Plainview Protocol is a public, forkable Streamlit platform that scores official transparency, maps FOIA and no-bid risk, and gives citizens tools (FOIA templates, ethics-complaint drafts, affidavit-gated foreign-influence views) **regardless of party**. It is evidence first, not a PAC site.

Live site: [plainviewprotocol.com](https://plainviewprotocol.com)

Owner: **Russell Nomer / Russell Nomer Consulting**. Established January 8, 2026.

## Verify this project

You do not need to trust a screenshot. Run the code.

| Document | Purpose |
| --- | --- |
| [VERIFY.md](VERIFY.md) | Step-by-step citizen audit |
| [FORK_ME.md](FORK_ME.md) | Decentralized hosting / Sentinel network |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Add accountability tests |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Five pillars of evidentiary integrity |
| [TUTORIAL.md](TUTORIAL.md) | Sentinel onboarding |

```bash
docker compose up --build
# or locally:
streamlit run app.py --server.port 5000
```

## Who it is for

- Citizens who want FOIA / ethics / county-portal tooling without a party loyalty test
- Journalists and student press who need sourced heatmaps and bill-level “grift” flags
- Agencies using the collaboration portal (`.gov` / `.mil` email, 72-hour correction window — see [SAFE_HARBOR.md](SAFE_HARBOR.md))

## What it does

- Accountability Tribunal and 50-state Corruption Heatmap (Shadow Penalty: FOIA speed, no-bid %, contractor donations)
- Local Watchdog for NY counties (all 62) plus a 3,143-county portal dataset
- FOIA Cannon, CCW Truth templates, ethics complaint generator, revolving-door tracker
- Foreign Influence / FARA views behind an **Affidavit of Integrity** (SHA-256, localStorage persistence)
- Viral battle cards (static PNGs + Open Graph) for shareable evidence cards
- National debt / Treasury-fed charts, DOGE scrutiny hub, Vampire Tax calculator
- Optional PostgreSQL traffic ledger and founder “Protocol Pulse” (when a database is configured)

Legal: [TERMS.md](TERMS.md), [PRIVACY.md](PRIVACY.md), [SAFE_HARBOR.md](SAFE_HARBOR.md).

## Stack

| Layer | Choice |
| --- | --- |
| App | Python 3.11, Streamlit, Plotly, Pandas |
| Persistence | streamlit-local-storage (affidavits); optional PostgreSQL (`psycopg2`) for traffic/error logs |
| APIs | Treasury, UnitedStates.io / Congress, public FOIA/FARA sources |
| Packaging | Docker / docker-compose; Playwright (+ axe-core) for a11y tests |
| Hosting | Replit Autoscale (`streamlit run app.py --server.port 5000`) |

## How to run

```bash
# Python 3.11
pip install -e .   # pyproject.toml
streamlit run app.py --server.port 5000
```

Optional: `DATABASE_URL` if you enable the traffic ledger. Do not commit admin credentials.

## Repo layout

```
app.py                      # Streamlit UI (Mission Control + pages)
affidavit_portal.py
ethics_filing_logic.py / vampire_tax_calculator.py / forensic_logger.py
traffic_ledger.py
county_portals.json / sources.json / revolving_door_audit.json / …
static/                     # battle cards and public assets
dashboard/ tests/ scripts/
Dockerfile  docker-compose.yml
```

## Replit

- Workspace: [https://replit.com/@RussellNomer/Plainview-Protocol](https://replit.com/@RussellNomer/Plainview-Protocol)
- GitHub: [https://github.com/russellnomer/Plainview-Protocol](https://github.com/russellnomer/Plainview-Protocol)

Forks are welcome; only the founder-vetted host at `plainviewprotocol.com` is the supported official instance.

Questions / security: help@russellnomerconsulting.com
