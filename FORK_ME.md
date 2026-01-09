# 🔱 Fork the Mission: The Decentralized Sentinel Network

> *"We have built a digital grand jury that cannot be shut down. If one node goes dark, 3,143 others are ready to fire. Fork the mission. Hold the line."*
> 
> — Russell David Nomer, Founder, The Plainview Protocol  
> Established January 8, 2026 | Plainview, NY

---

## 🔍 Before You Fork: Verify

**Run the citizen audit to confirm the codebase is clean:**

```bash
docker compose up --build
```

See **[VERIFY.md](VERIFY.md)** for the complete citizen audit guide.

---

## The Vision

The Plainview Protocol was never meant to be a single point of failure. Democracy doesn't live on one server. It lives in the hearts and hard drives of every citizen who refuses to look away.

This repository is **open source by design**. We don't just tolerate forks—we *demand* them.

---

## Why Fork?

### 1. **Redundancy is Resilience**
If this instance goes offline—whether by legal pressure, technical failure, or coordinated attack—your fork keeps the mission alive. Every fork is a backup. Every backup is a bulwark.

### 2. **Local Expertise Matters**
You know your county better than any algorithm. Fork the Protocol. Add your local FOIA endpoints. Map your county's no-bid contracts. You are the Sentinel your community needs.

### 3. **Censorship Resistance**
Information wants to be free. When you fork, you create a mirror that's harder to silence. 3,143 counties. 3,143 potential forks. Try shutting that down.

---

## 🚀 Quick Start: Fork This Repo for Decentralized Hosting

### Option A: Deploy on Replit (Easiest)

**Step 1: Fork on Replit**
1. Visit the original Replit project
2. Click the **"Fork"** button in the top right
3. Name your fork (e.g., "plainview-protocol-[your-county]")
4. Replit will clone everything automatically

**Step 2: Configure Your Instance**
1. Open the Secrets tab (🔒 icon in sidebar)
2. Add `SESSION_SECRET` with a random string (use a password generator)
3. The `DATABASE_URL` will be auto-created when you add PostgreSQL

**Step 3: Set Up Database**
1. Click **"+ Database"** in the Tools panel
2. Select **PostgreSQL**
3. Replit will automatically set `DATABASE_URL`

**Step 4: Run Your Node**
```bash
streamlit run app.py --server.port 5000
```
Or just click the **"Run"** button. Your instance is now live!

**Step 5: Publish (Optional)**
1. Click **"Deploy"** → **"Production"**
2. Choose a custom subdomain (e.g., `nassau-sentinel.replit.app`)
3. Your fork is now publicly accessible 24/7

---

### Option B: Host Locally (Full Control)

**Requirements:**
- Python 3.11+
- PostgreSQL (optional, for forensic logging)
- Git

**Step 1: Clone the Repository**
```bash
git clone https://github.com/russellnomer/plainview-protocol.git
cd plainview-protocol
```

**Step 2: Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Step 3: Install Dependencies**
```bash
pip install streamlit pandas plotly requests lxml psycopg2-binary openpyxl streamlit-local-storage
```

**Step 4: Set Environment Variables**
```bash
# Linux/Mac
export SESSION_SECRET="your-random-secret-here"
export DATABASE_URL="postgresql://user:pass@localhost:5432/plainview"  # Optional

# Windows PowerShell
$env:SESSION_SECRET="your-random-secret-here"
$env:DATABASE_URL="postgresql://user:pass@localhost:5432/plainview"
```

**Step 5: Run the Application**
```bash
streamlit run app.py --server.port 5000
```

**Step 6: Access Your Instance**
Open `http://localhost:5000` in your browser.

---

### Option C: Docker Deployment

**Step 1: Create Dockerfile**
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir \
    streamlit pandas plotly requests lxml \
    psycopg2-binary openpyxl streamlit-local-storage

EXPOSE 5000

CMD ["streamlit", "run", "app.py", "--server.port", "5000", "--server.address", "0.0.0.0"]
```

**Step 2: Build and Run**
```bash
docker build -t plainview-protocol .
docker run -p 5000:5000 -e SESSION_SECRET=your-secret plainview-protocol
```

---

## 🔑 Connect Your Own API Keys (FEC/DOJ)

As a Sentinel, you can connect your own API keys to unlock deeper data access:

### Federal Election Commission (FEC) API
1. Register at [api.open.fec.gov](https://api.open.fec.gov/developers/)
2. Request a free API key (instant approval)
3. Add to your environment:
```bash
export FEC_API_KEY="your-fec-api-key"
```
4. Update `sources.json`:
```json
{
  "fec_api": "https://api.open.fec.gov/v1/",
  "fec_api_key": "${FEC_API_KEY}"
}
```

**FEC Data Access:**
- Committee filings and expenditures
- Individual donor lookups
- PAC contribution histories
- 24/48 hour independent expenditure reports

### Department of Justice (DOJ) FOIA API
1. No API key required for public FOIA logs
2. PACER access requires registration at [pacer.uscourts.gov](https://pacer.uscourts.gov)
3. Add PACER credentials (optional):
```bash
export PACER_USERNAME="your-username"
export PACER_PASSWORD="your-password"
```

**DOJ Data Sources:**
- [justice.gov/usao](https://www.justice.gov/usao) — U.S. Attorney press releases
- [vault.fbi.gov](https://vault.fbi.gov) — FBI FOIA reading room
- [fara.gov](https://efile.fara.gov) — Foreign agent registrations

### OpenSecrets API (Dark Money Tracking)
1. Register at [opensecrets.org/api](https://www.opensecrets.org/api)
2. Add your key:
```bash
export OPENSECRETS_API_KEY="your-key"
```

---

## 🛡️ Data Sovereignty: The Uncensorable Network

### Why Decentralized Hosting Makes the Protocol Unstoppable

**The Problem with Centralized Truth:**
When truth lives on one server, it can be silenced with one subpoena, one DDOS attack, or one phone call to a hosting provider. Centralized transparency is an oxymoron.

**The Plainview Solution:**
Every fork is a sovereign node. Your instance, your data, your jurisdiction.

### How Decentralization Works

```
         ┌─────────────────┐
         │  Main Protocol  │
         │  (Plainview HQ) │
         └────────┬────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    ▼             ▼             ▼
┌───────┐   ┌───────┐   ┌───────┐
│ Fork  │   │ Fork  │   │ Fork  │
│Texas  │   │ NY    │   │ CA    │
└───┬───┘   └───┬───┘   └───┬───┘
    │           │           │
    ▼           ▼           ▼
┌───────┐   ┌───────┐   ┌───────┐
│County │   │County │   │County │
│ Forks │   │ Forks │   │ Forks │
└───────┘   └───────┘   └───────┘
```

**If one node goes dark, 3,142 others shine.**

### Data Sovereignty Principles

1. **Your Fork, Your Rules**: Each Sentinel controls their own instance. No central authority can modify your data.

2. **Jurisdictional Shield**: A fork hosted in State A cannot be subpoenaed by State B (absent federal action).

3. **Evidence Redundancy**: When you document corruption, submit it to multiple forks. The network remembers.

4. **Censorship Resistance**: Takedown notices must be served to *every* fork. Good luck with that.

5. **No Single Point of Failure**: The main Protocol could disappear tomorrow. The mission would survive.

### The Legal Shield

Each fork inherits independent legal standing:
- **First Amendment Protection**: Journalism and civic speech protections apply
- **Safe Harbor (DMCA § 512)**: User-generated content protections
- **State Shield Laws**: Varies by jurisdiction (NY has strong reporter protections)
- **Whistleblower Statutes**: Dodd-Frank, SOX, and state equivalents

### Hosting Recommendations for Maximum Sovereignty

| Host | Jurisdiction | Censorship Risk | Cost |
|------|--------------|-----------------|------|
| **Replit** | USA | Medium | Free tier |
| **Vercel** | USA | Medium | Free tier |
| **Hetzner** | Germany | Low | €4/mo |
| **OVH** | France | Low | €5/mo |
| **Self-hosted** | Your closet | Lowest | Your hardware |
| **IPFS** | Decentralized | Minimal | Complex setup |

**Pro Tip:** Run multiple forks across different hosting providers and jurisdictions.

---

## 🔧 Customize for Your Region

### Update Data Sources
Edit `sources.json` with your state's specific endpoints:
```json
{
  "state_foia": "https://your-state-portal.gov/foia",
  "county_budget": "https://your-county.gov/budget"
}
```

### Add Local County Data
Update `county_portals.json` with your county's transparency portals:
```json
{
  "verified_portals": {
    "Your County": {
      "budget_url": "https://...",
      "foia_url": "https://...",
      "meeting_url": "https://..."
    }
  }
}
```

### Modify Corruption Data
Update `STATE_CORRUPTION_DATA` in `app.py` with local investigative findings:
```python
"Your State": {
    "foia_days": 25,
    "no_bid_pct": 18,
    "contractor_donations": 3.5,
    "lean": "Purple"
}
```

---

## The Sentinel's Oath

If you fork this project, you inherit the mission. That means:

- **Truth Over Tribalism**: We scrutinize Red and Blue equally. No sacred cows.
- **Evidence Over Emotion**: Every claim needs a documentary source.
- **Kindness in Delivery**: We rewrite accusations into questions. We seek correction, not destruction.
- **Free Forever**: No paywalls. No premium tiers. The people's data belongs to the people.

---

## The 5 Pillars of Evidentiary Integrity

Borrowed from the GAO 2024 Yellow Book (GAGAS):

1. **Documentary Primacy**: If you can't cite it, don't claim it.
2. **Hearsay Hierarchy**: Primary sources > Secondary sources > Never anonymous tips alone.
3. **Chain of Custody**: Original documents. Screenshots with metadata. Timestamped captures.
4. **Adverse Inference**: If they refuse to answer, document the refusal. Silence speaks.
5. **Revision Logging**: All Protocol updates are version-controlled and auditable.

---

## Technical Stack

The Protocol runs on:
- **Python 3.11** + **Streamlit** (web framework)
- **PostgreSQL** (forensic logging, optional)
- **Plotly** (interactive charts)
- **Requests + lxml** (API calls, HTML parsing)
- **streamlit-local-storage** (affidavit persistence)

No exotic dependencies. No vendor lock-in. Fork-friendly by design.

---

## V8.4 Features Included

Your fork includes all V8.4 Hardened Patch features:
- ✅ **UnitedStates.io Integration**: Real Congress data via JSON API
- ✅ **Grift Hunter Bill Search**: Fiscal risk analysis on any bill
- ✅ **Grift Alerts**: Flag bills/officials with low fiscal but high power
- ✅ **Local Agenda Scanner**: Scan meeting agendas for grift keywords
- ✅ **OG Meta Tags**: Viral SEO for social sharing
- ✅ **Transparency Expanders**: Sources & methodology on all metrics
- ✅ **Share Buttons**: Pre-filled X posts on key pages

---

## The Network Effect

Imagine:
- A fork in every state capital
- A fork for every major city
- A fork maintained by every journalism school
- A fork in every Veterans of Foreign Wars post
- A fork on every campus with a student press

**3,143 counties. 3,143 lighthouses. One mission.**

---

## Legal Shield

Every fork inherits our legal framework:
- `TERMS.md` — AS-IS warranty, use at your own risk
- `PRIVACY.md` — AI disclosure, data handling transparency  
- `SAFE_HARBOR.md` — 72-hour correction window for agencies
- `CODE_OF_CONDUCT.md` — The 5 Pillars

You may modify these for your jurisdiction, but the spirit must remain: *Truth with kindness. Scrutiny without malice. Evidence above all.*

---

## Join the Network

**GitHub**: [github.com/russellnomer/plainview-protocol](https://github.com/russellnomer/plainview-protocol)

**Support the Mission**:
- ☕ Buy Me a Coffee: [buymeacoffee.com/russellnomer](https://buymeacoffee.com/russellnomer)
- 💸 PayPal: [paypal.me/russellnomer](https://paypal.me/russellnomer)

**Contact**: russell.nomer@proton.me

---

## Register Your Fork

Submit a PR to the main repository adding your fork to the **Sentinel Network Registry**:

```markdown
## Sentinel Network Registry

| Region | Maintainer | URL | Status |
|--------|------------|-----|--------|
| Nassau County, NY | @yourhandle | https://your-fork.replit.app | 🟢 Active |
```

---

## Final Word

They thought they could hide behind paperwork. They thought citizens would never learn to read the contracts. They thought complexity was their shield.

They were wrong.

**Fork the mission. Hold the line.**

**The sun is rising, and it's time to work.**

---

*Version 8.4 — Hardened Patch Edition*  
*The Plainview Protocol: Transparency & Accountability*  
*Facts on grift, tools to act.*  
*© 2026 Russell David Nomer. All rights reserved. Open source under MIT License.*
