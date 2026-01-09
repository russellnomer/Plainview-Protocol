# How to Audit This Project

> **"You do not need to trust us. Run the code. Verify the truth."**

This guide enables any citizen—regardless of technical background—to independently verify the integrity of The Plainview Protocol. No special skills required.

---

## Why Verification Matters

The Plainview Protocol makes claims about transparency, security, and accountability. Words are cheap. This document hands you the tools to verify those claims yourself.

We use the same data the Labyrinth uses, but we use it for the people. Fork the code. Spread the light.

---

## Prerequisites

You need one thing: **Docker Desktop**

Docker is a free tool that runs code in an isolated environment. It ensures you're running the exact same tests we run—no modifications possible.

### Step 1: Install Docker

| Operating System | Installation Link |
|-----------------|-------------------|
| Windows | [Download Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) |
| Mac | [Download Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/) |
| Linux | [Docker Engine Install Guide](https://docs.docker.com/engine/install/) |

After installation:
1. Open Docker Desktop
2. Wait for the whale icon to appear in your system tray
3. Verify by opening Terminal/Command Prompt and typing: `docker --version`

---

## Step 2: Download This Repository

### Option A: Download ZIP (Easiest)
1. Click the green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract to a folder you'll remember

### Option B: Clone with Git
```bash
git clone https://github.com/YOUR_USERNAME/plainview-protocol.git
cd plainview-protocol
```

---

## Step 3: Run the Audit

Open Terminal (Mac/Linux) or Command Prompt (Windows) and navigate to the project folder:

```bash
cd path/to/plainview-protocol
```

Then run the audit capsule:

```bash
docker compose up --build
```

**What happens next:**
1. Docker downloads the official Playwright testing environment
2. The audit suite runs automatically (16 tests across 3 categories)
3. Results display in real-time in your terminal

---

## Step 4: Interpret the Results

### The Green Light (PASS)
```
✓ Protocol loads successfully
✓ No sensitive data exposed
✓ All security headers present
```
**Meaning:** The system is operating as intended. Integrity verified.

### The Red Light (FAIL)
```
✗ Security header missing
✗ Unexpected data exposure detected
```
**Meaning:** Something requires attention. Report it immediately.

---

## Understanding the Output

| Symbol | Meaning |
|--------|---------|
| ✓ | Audit passed - integrity verified |
| ✗ | Audit failed - investigate immediately |
| ○ | Audit skipped - not applicable to this run |

### Success Rate

At the end of the audit, you'll see:
```
16 passed (45.2s)
```

This means 16 out of 16 audits passed. **100% is the standard. Anything less requires investigation.**

---

## What Gets Tested

| Category | What It Checks |
|----------|---------------|
| **Homepage Audits** | Protocol loads, navigation works, live data displays |
| **Security Audits** | HTTPS enforcement, data exposure prevention, header security |
| **Contact Audits** | Form validation, email protection, submission handling |

---

## View Detailed Results

After running the audit, check these files:

| File | Contents |
|------|----------|
| `tests/test-results/results.json` | Raw audit data (machine-readable) |
| `dashboard/index.html` | Visual status board (open in browser) |
| `dashboard/history.json` | 30-day trend data |

---

## Report Issues

If you discover a failing audit:

1. **Do not panic** - Document what you see
2. **Screenshot the terminal output**
3. **Open an issue** on GitHub using the "Audit Failure Report" template
4. **Include your environment**: OS, Docker version, timestamp

---

## Frequently Asked Questions

### Is this actually running on my computer?
Yes. Docker creates an isolated environment, but the code runs locally. No data leaves your machine.

### Can I modify the tests?
Yes. Fork the repo and add your own accountability tests. See `CONTRIBUTING.md` for guidelines.

### How often should I run this?
Run it whenever you want verification. We run it automatically on every code change.

### What if Docker doesn't work?
1. Ensure Docker Desktop is running (whale icon visible)
2. Try: `docker system prune -a` then retry
3. Open an issue—we'll help

---

## The Sentinel's Oath

By running this audit, you join the Sentinel Network. You are not just a user—you are a guardian of transparency.

> "The barrier to entry for truth must be zero."

---

## Quick Reference

```bash
# Full audit
docker compose up --build

# View results
open dashboard/index.html

# Clean up
docker compose down
```

---

*The Plainview Protocol - Established January 8, 2026*  
*"Truth, Kindness, & Security"*
