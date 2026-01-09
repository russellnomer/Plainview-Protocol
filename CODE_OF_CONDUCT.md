# The Sentinel's Code of Conduct

## The Plainview Protocol V6.17 — Gold Master Ethics Framework

**Established:** January 9, 2026  
**Author:** Russell Nomer, Plainview, NY  
**Standard:** Aligned with GAO 2024 Yellow Book (GAGAS) and modern digital forensic best practices

---

## The Sentinel Oath

> *"We don't just find corruption; we prove it. If the evidence isn't bulletproof, the vampires won't burn. Follow the Code. Protect the Integrity. Stay in the Light."*

---

## The 5 Pillars of Evidentiary Integrity

Every Sentinel operating within The Plainview Protocol must adhere to these five foundational principles. These standards ensure our findings are legally defensible, journalistically credible, and immune to dismissal as "partisan noise."

---

### PILLAR 1: OBJECTIVITY & INDEPENDENCE

**The Standard:** Auditors must maintain "Independence of Mind and Appearance."

**Requirements:**
- Any personal or financial conflict of interest with a target (PAC, Official, or Entity) must be disclosed immediately
- If a conflict exists, the auditor must recuse themselves from that investigation
- No Sentinel may audit an entity where they, their family members, or close associates have a financial interest
- Political party affiliation does not constitute a conflict, but active campaign involvement does

**Example Violations:**
- Auditing a PAC that employs your spouse
- Investigating an official you are actively campaigning against
- Accepting payment from any party related to an investigation

---

### PILLAR 2: DOCUMENTARY PRIMACY

**The Standard:** Verbal claims are hearsay. The Protocol only recognizes "Hard Evidence."

**Accepted Evidence Types:**
1. **PDFs of Official Records** — Government filings, court documents, FOIA responses
2. **FEC Filing Screenshots** — Direct captures from FEC.gov with visible URLs and timestamps
3. **60-Second Verified Video Reels** — Citizen Reel uploads with EXIF/GPS stripped and hash verification
4. **Notarized Affidavits** — Sworn statements under penalty of perjury
5. **Published Journalism** — Articles from verified news sources with named reporters

**Rejected Evidence:**
- Anonymous tips without corroboration
- Social media posts without official confirmation
- "I heard from someone who..."
- Screenshots without visible source URLs

---

### PILLAR 3: TECHNICAL INTEGRITY

**The Standard:** Digital evidence must be preserved using Hash-Verification (SHA-256) where possible.

**Requirements:**
- All uploaded files should include a SHA-256 hash for verification
- The hash proves the data was not modified between collection and upload
- Timestamps must be preserved in all evidence packages
- Chain of custody documentation is required for sensitive materials

**Hash Verification Process:**
```bash
# Generate SHA-256 hash of evidence file
sha256sum evidence_document.pdf

# Output example:
# a7b9c4d8e2f1a3b5c7d9e1f3a5b7c9d1e3f5a7b9c1d3e5f7a9b1c3d5e7f9a1b3  evidence_document.pdf
```

**Storage Requirements:**
- Original files must be preserved unmodified
- Working copies may be used for analysis
- Any redactions must be clearly marked and documented

---

### PILLAR 4: THE "VAMPIRE" RULE

**The Standard:** Use the Sunlight Flare to expose, not to harass.

**Requirements:**
- All data shared must be of "Overwhelming Public Interest"
- Personal information unrelated to official conduct must be redacted
- Home addresses, personal phone numbers, and family members are off-limits unless directly relevant
- The goal is transparency, not intimidation

**Public Interest Test:**
Before publishing, ask yourself:
1. Does this information relate to the official's public duties or use of public funds?
2. Would a reasonable citizen want to know this about their representative?
3. Is there a legitimate accountability purpose, or is this personal?

If the answer to any question is "No," do not publish.

**Prohibited Actions:**
- Sharing personal home addresses
- Contacting family members
- Publishing unrelated personal information
- Using evidence for personal vendettas

---

### PILLAR 5: ACCOUNTABILITY

**The Standard:** Every Sentinel is responsible for the accuracy of their uploads.

**Requirements:**
- Verify all claims before uploading to the Protocol
- Cite sources for every assertion
- Correct errors immediately and publicly
- Accept responsibility for mistakes

**Badge System:**
- **Verified Sentinel:** Completed Training Ground, 3+ accurate submissions
- **Senior Sentinel:** 10+ verified submissions, zero retractions
- **Sunlight Master:** 50+ verified submissions, documented impact

**Consequences for Violations:**
- **First Offense:** Private warning, required remedial training
- **Second Offense:** Public correction, badge downgrade
- **Bad Faith Conduct:** Badge stripped, moved to Shadow Watch list
- **Deliberate Falsification:** Permanent ban, potential legal referral

---

## The "Bad Faith" Standard

A Sentinel acts in "Bad Faith" when they:
1. Knowingly submit false or fabricated evidence
2. Deliberately misrepresent the content of official documents
3. Use the Protocol for personal harassment rather than public accountability
4. Refuse to correct documented errors
5. Coordinate with targets to undermine other investigations

---

## Recusal Protocol

When a conflict is identified:
1. Immediately stop work on the affected investigation
2. Notify Protocol leadership via the Recusal Form
3. Transfer all evidence to an unconflicted Sentinel
4. Do not access investigation materials after recusal
5. Document the conflict for transparency records

---

## Evidence Chain of Custody

For each piece of evidence:
1. **Collection Date:** When was this obtained?
2. **Collection Method:** FOIA, public record, court filing, etc.
3. **Original Source:** URL, agency, court docket number
4. **Collector:** Which Sentinel obtained this?
5. **Hash Verification:** SHA-256 of original file
6. **Storage Location:** Where is the original preserved?

---

## The Sunlight Promise

By operating under this Code, we ensure that:
- Our findings can withstand legal scrutiny
- Journalists can cite our work with confidence
- Courts will accept our evidence
- The public can trust our integrity
- The vampires have no shadows to hide in

---

## Reporting Violations

If you witness a Code violation:
1. Document the specific conduct
2. Preserve any evidence of the violation
3. Submit a report via the Internal Review Form
4. Do not publicly accuse without investigation

All reports are reviewed by the Protocol Ethics Committee.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| V6.17 | Jan 9, 2026 | Gold Master ethics framework established |
| V6.15 | Jan 8, 2026 | Sunlight Flare system integrated |
| V6.0 | Jan 2026 | Deep Dive Engine launched |

---

*"The Labyrinth has no place to hide when Sentinels follow the Code."*

**The Plainview Protocol** — Truth, Kindness, & Security

---

## Related Documents

- [TUTORIAL.md](TUTORIAL.md) — Sentinel Training Guide
- [README.md](README.md) — Project Overview
- [CONTRIBUTING.md](CONTRIBUTING.md) — How to Contribute

---

© 2026 Russell Nomer. The Plainview Protocol is free and open source.
