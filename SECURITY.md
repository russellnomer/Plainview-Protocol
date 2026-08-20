# Security Policy — The Plainview Protocol

## Classification

**Public** GitHub repository. Anyone can fork the code. Only the instance at `plainviewprotocol.com` is founder-supported.

Owner: Russell Nomer / Russell Nomer Consulting.

This policy is **high-level**. It does not include exploit steps, default credentials, or attack recipes.

## Reporting

If you find a security flaw, hidden tracking, or code that violates the project’s transparency principles:

1. **Do not** open a public GitHub issue that includes a working exploit.
2. Email **help@russellnomerconsulting.com** (and/or use the in-app “Support Russell” path).
3. We will assess the report, fix verified issues, and credit reporters who want credit.

Third-party forks are not covered. Run official code or audit the diff yourself ([VERIFY.md](VERIFY.md)).

## Data handled

Public features are designed around **public records and user-initiated tools** (FOIA drafts, heatmaps, affidavits stored in the browser). Depending on deployment configuration, an instance **may** also keep operational telemetry (session/error logs) in PostgreSQL. Operators must disclose that in their own privacy notice. See [PRIVACY.md](PRIVACY.md).

Do not submit secrets, classified material, or other people’s private data into forms or uploads.

## Authentication

Most citizen features do not require an account. Administrative or founder views, if enabled on a deployment, must be gated with credentials **that are not committed to the repository**. Agency collaboration uses an email-domain gate (`.gov` / `.mil`) plus a documented correction window — that is an access policy, not a cryptographic guarantee.

## Secrets

This tree has no `SECRETS_MANIFEST.txt`. Typical deployment names (values never in git):

- `DATABASE_URL` (optional ledger)
- Streamlit / host session configuration

Rotate anything that ever appeared in a public commit, gist, or screenshot.

## Attack surface (high level)

- Public web app (`plainviewprotocol.com`)
- Optional database
- Outbound fetches of public government data
- User-supplied URLs, bill numbers, county names, uploads (treat as untrusted)
- Static file serving (share cards)
- Docker image supply chain if you run `docker compose`

## Principles (defensive)

- Prefer public, cited data sources; keep methodology visible
- Do not collect more personal data than a feature requires
- Rate-limit expensive generators (FOIA / export) so the app cannot be used as an anonymous mail cannon
- Keep administrative functions off the default navigation and behind a secret the operator sets per instance
- Hash or bind affidavits in the browser; do not turn a civic signature into a reusable credential
- Pin dependencies (`pyproject.toml` / `uv.lock`) and scan the Docker base image

## Supported versions

Only the latest founder-hosted build at `plainviewprotocol.com` is officially supported.

## Contact

help@russellnomerconsulting.com

*“Truth, Kindness, Security.”*
