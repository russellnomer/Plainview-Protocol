# The Plainview Protocol: Truth, Kindness, & Security

## Overview
Version 8.4 - Hardened Patch. Established January 8, 2026. A production-ready Streamlit web application with bipartisan corruption tracking across all 50 states and 3,143 counties. Features Corruption Heatmap with Shadow Penalty scoring, Foreign Influence Tracker with Affidavit Gate (now with localStorage persistence), Revolving Door Tracker for lobbyist cooling-off violations, Ethics Complaint Trigger for OCC/Senate submissions, Agency Collaboration Portal with 72-hour correction window, and comprehensive FOIA/FARA tools. Pro-American, rule of law, domestic security focus.

## Version 8.4 Features (Hardened Patch)
- **UnitedStates.io Integration**: JSON API for reliable Congress legislator data with bioguide links
- **OG Meta Tags**: Viral SEO with og:title, og:description via metadata_handler.py
- **Grift Hunter Bill Search**: Mock AI fiscal risk analysis for bill numbers (HR 2617, S 1234)
- **Grift Alerts**: Flag bills/officials when fiscal impact is MINIMAL but power level is HIGH
- **Local Agenda Scanner**: Scan town/county agendas for grift keywords with user flagging
- **FORK_ME.md**: Updated decentralization guide with V8.4 features
- **Solid Ground Doctrine**: "We use the same data the Labyrinth uses, but we use it for the people"
- **Transparency Expanders**: All metrics/pages include sources and methodology citations

## Version 8.3 Features (Forensic Patch)
- **Routing Ghost Fix**: st.session_state exclusive navigation with catch-all redirect to Mission Control
- **Async Traffic Ledger**: Queue/Thread non-blocking database writes for high-performance logging
- **Affidavit Persistence**: LocalStorage-backed signature persistence (streamlit-local-storage)
- **FORK_ME.md**: Decentralized Sentinel Network mission for GitHub forking
- **All 62 NY Counties**: Complete county dataset including Chemung (FIPS 36015)

## Version 8.2 Features (Traffic Audit)
- **Traffic Ledger**: PostgreSQL-backed session tracking
- **Rate Limiting**: >10 FOIA/60s triggers nefarious activity flag
- **Protocol Pulse**: Founder dashboard with Plotly adoption charts
- **Forensic Error Tracking**: sentinel_logs table with incident IDs

## Version 8.1 Features (Forensic Error Tracking)
- **Error Logging**: Database-backed exception tracking with stack traces
- **Audit Logs Dashboard**: Admin-only (SUNLIGHT2026) error browser
- **Incident IDs**: SHA-256 based unique identifiers for errors

## Version 6.18 Features (Sovereign Affidavit Portal)
- **Affidavit of Integrity**: SHA-256 signature binding for Foreign Influence/FARA access
- **Revolving Door Tracker**: Lobbyist database with cooling-off violation detection
- **Ethics Complaint Trigger**: OCC/Senate Ethics formal complaint generator
- **Agency Collaboration Portal**: .gov/.mil email gate, 72-hour correction workflow
- **Legal Shield**: TERMS.md, PRIVACY.md, SAFE_HARBOR.md with footer modal

## Core Features
- **The National Lens**: Live national debt from Treasury API, state debt share, immigration burden with border state multipliers (1.6x)
- **The 2027 Fork**: Plotly chart anchored to live debt data, reform vs. status quo projections
- **Trade & Industry**: Tariff dividend calculator, sourcing finder
- **DOGE Scrutiny Hub**: DOGE metrics ($214B+ savings), Minnesota Feeding Our Future fraud case study
- **Corruption Heatmap**: 50-state Shadow Penalty scoring (FOIA speed, no-bid %, contractor donations), bipartisan tracking, Deep Dive triggers
- **State Deep Dive**: Detailed state-level analysis with no-bid contract tables, PAC black hole spending, Justice.gov/FBI Vault links (NY, FL, CA, TX, IL)
- **Local Watchdog**: All 62 NY counties with transparency scoring and Compare My County feature
- **The Activism Hub**: Tabbed interface (Veterans/Border/Education/Business), kindness rewriter, X share button
- **Accountability Tribunal**: Live Congress data, Shadow List, Scrutiny Tactics, Referendum Prototype (Vote to Audit)
- **FOIA Cannon**: Custom requests + Bipartisan Grift Hunter (Sanctuary Grift, Corporate Subsidy Grift, Universal)
- **Foreign Influence Tracker**: International conduits, 501(c)(4) dark money, FARA watchlist (requires affidavit)
- **FARA Violation Reporter**: Citizen reports to DOJ National Security Division (requires affidavit)
- **Shadow Watch**: Vampire Tax calculator, Sunlight Victory tracking
- **Lever Map**: Citizen's guide to pulling levers of power (Paper Trail, Whistleblower Hotlines, Financial Chokehold)
- **Course Correction**: State-by-state recall laws, impeachment procedures, grand jury petition guides
- **Sentinel Training Ground**: 4-step FOIA guide, Practice Cannon sandbox, Code of Conduct
- **Citizen Reel**: Video uploader with privacy scrubbing
- **The Ecosystem**: Russell's apps, books, and music
- **Support the Mission**: Buy Me a Coffee, PayPal, GitHub fork links

## Tech Stack
- Python 3.11
- Streamlit (web framework)
- streamlit-local-storage (affidavit persistence)
- Pandas (data handling)
- Plotly (interactive charts)
- Requests (API calls)
- lxml (XML/HTML parsing)
- psycopg2 (PostgreSQL)
- hashlib (SHA-256 signature binding)
- threading/queue (async logging)

## Project Structure
- `app.py` - Main Streamlit application with 30+ pages
- `affidavit_portal.py` - Sovereign Affidavit signing with localStorage persistence
- `forensic_patch.py` - V8.3 routing fixes and session state management
- `traffic_ledger.py` - Async Queue/Thread non-blocking database writes
- `forensic_logger.py` - Error and traffic logging with rate limiting
- `ethics_filing_logic.py` - OCC/Senate complaint generator
- `vampire_tax_calculator.py` - FARA penalty calculations
- `flare_animation_logic.py` - Sunlight Flare animations
- `sources.json` - Data source URLs (Treasury API, Senate feed, Wikipedia)
- `technical_audit.json` - Silicon & Soros Audit data
- `revolving_door_audit.json` - Lobbyist database with cooling-off tracking
- `leftist_target_list.json` - Updated PAC target list with AI regulation focus
- `foreign_influence_audit.json` - International conduits and 501(c)(4) tracking
- `grassroots_media.json` - Student press and indie creator contacts
- `county_portals.json` - 3,143 county portal data (all 62 NY counties with FIPS)
- `test_findings_v8.json` - Zero-Day Forensic Audit results
- `CODE_OF_CONDUCT.md` - Sentinel's 5 Pillars of Evidentiary Integrity
- `TERMS.md` - Terms of Service (AS-IS warranty)
- `PRIVACY.md` - Privacy Policy (AI disclosure)
- `SAFE_HARBOR.md` - Agency Collaboration Safe Harbor
- `TUTORIAL.md` - Sentinel onboarding guide
- `FORK_ME.md` - Decentralized Sentinel Network mission
- `.streamlit/config.toml` - Streamlit server configuration

## Running the App
```
streamlit run app.py --server.port 5000
```

## Playwright Testing Infrastructure
- **Test Suite**: 16 automated audits across 3 spec files
  - `tests/e2e/home.spec.ts` - Homepage critical path audits (4 tests)
  - `tests/e2e/contact.spec.ts` - Contact functionality audits (5 tests)
  - `tests/accountability/security.spec.ts` - Security & privacy audits (7 tests)
- **Run Commands**:
  - Full suite: `npx playwright test --project=chromium`
  - Smoke tests: `npx playwright test --grep @smoke --project=chromium`
  - Security audits: `npx playwright test tests/accountability/ --project=chromium`
- **Output**: JSON results to `tests/test-results/results.json`

## Public Accountability Dashboard
- **Location**: `dashboard/` directory
- **Files**:
  - `dashboard/index.html` - Tailwind CSS Status Board with OPERATIONAL/FAILED indicators
  - `dashboard/dashboard.js` - Fetches results.json, renders Chart.js 30-day trend
  - `dashboard/history.json` - Rolling 30-day test history
- **Processing**: `scripts/process-history.js` - Updates history from test results
- **Serve**: `python scripts/serve-dashboard.py` (port 3000)

## Community Verification Framework
- **Docker Audit Capsule**:
  - `Dockerfile` - Playwright v1.40+ image with auto-test execution
  - `docker-compose.yml` - Audit service with volume mounts for results
  - Run: `docker compose up --build`
- **Citizen Documentation**:
  - `VERIFY.md` - Step-by-step guide for non-technical auditors
  - `CONTRIBUTING.md` - Accountability test guidelines
  - `.github/ISSUE_TEMPLATE/test_failure.yml` - Audit failure report form
- **Maintenance Scripts**:
  - `scripts/update-deps.sh` - Playwright browser update utility
  - `scripts/docker-entrypoint.sh` - Container startup script

## Database Tables (PostgreSQL)
- `sentinel_logs` - Error tracking with incident IDs
- `traffic_ledger` - Session and page view tracking
- `nefarious_activity` - Rate limit violations
- `sentinel_signups` - Affidavit signing adoption

## Data Sources
- **Treasury Debt**: https://api.fiscaldata.treasury.gov (live, cached 1 hour)
- **Senate Votes**: senate.gov XML feed
- **Congress Legislators**: UnitedStates.io live JSON API
- **FEC Data**: FEC.gov committee filings
- **FARA Database**: efile.fara.gov
- **Lobbying Data**: OpenSecrets.org, LDA filings

## Legal Framework
- **Code of Conduct**: 5 Pillars aligned with GAO 2024 Yellow Book (GAGAS)
- **Affidavit Gate**: 52 U.S.C. § 30121, 18 U.S.C. § 1001 basis
- **Ethics Complaints**: 18 U.S.C. § 207 cooling-off violations
- **FARA Reporting**: 22 U.S.C. § 611 et seq.
- **Safe Harbor**: 72-hour correction window for agencies

## Sidebar Controls
- State selector (all 50 states, default: New York)
- Focus selector (All, Border, Veterans, Education)
- System status indicator
- Affidavit status display
- Persistent "Support Russell" coffee button

## Key Data
- NY counties: 62 (all verified with FIPS codes)
- Border states: Texas, Arizona, California, New Mexico (1.6x multiplier)
- State populations for debt share calculations
- Base immigration cost: $150.7B (FAIR 2023-2024)
- Fallback debt value: $36.5T if API fails
- AI lobbying 2025: $50M total
- Revolving door rate: 53% of tech lobbyists are former government officials

## Design
- Patriotic color scheme (navy blue, red, white)
- Live data with caching (TTL 3600 seconds)
- Graceful fallbacks for all data sources
- System health monitoring
- Session-based SHA-256 signature binding with localStorage persistence
- Legal footer with Terms/Privacy/Safe Harbor links
- Async non-blocking traffic logging

## User Preferences
- Equal scrutiny for Red and Blue jurisdictions (bipartisan)
- Evidence-based claims only (Documentary Primacy)
- Free access (no paywalls)
- Open source (GitHub fork available via FORK_ME.md)

## Founder Access Keys
- Audit Logs: SUNLIGHT2026
- Protocol Pulse: SUNLIGHT2026
