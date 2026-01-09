# Contributing to The Plainview Protocol

## Mission Statement

**Founded on January 8, 2026, by Russell Nomer as a tool for modern sovereignty.**

The Plainview Protocol is an open-source citizen oversight platform designed to bring transparency to government at all levels. We welcome contributions from anyone who shares our commitment to Truth, Kindness, and Security.

## Core Principles

1. **Bipartisan Scrutiny** - We apply equal scrutiny to Red and Blue jurisdictions. Transparency is a fiduciary duty, not a partisan choice.

2. **Data-Driven** - All claims must be backed by verifiable sources (government APIs, public records, official documents).

3. **Citizen Empowerment** - Features should help ordinary citizens hold officials accountable through legal means.

4. **Decentralization** - The Protocol is designed to be forked. Each fork is a new node in the transparency network.

## How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs or suggest features
- Include screenshots and steps to reproduce for bugs
- Tag issues appropriately (bug, enhancement, documentation)

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes following our code style
4. Test thoroughly
5. Submit a Pull Request with a clear description

### Accountability Tests (Most Needed)

New tests that verify the Protocol's integrity are the lifeblood of this project.

**The Golden Rule:**
> Tests must be readable by non-programmers.

A citizen should understand what a test does by reading its title.

**Naming Convention:**
```typescript
test('WHAT_IT_CHECKS in PLAIN_ENGLISH @category', async ({ page }) => {
  console.log('🔍 Running [Category] Audit: [Description]...');
  // test logic here
  console.log('✅ [Category] Audit: [Result]');
});
```

**Good Examples:**
- `Protocol loads successfully @smoke`
- `No API keys exposed in page source @security`
- `Foreign Influence data requires affidavit @access-control`

**Bad Examples:**
- `test1`, `should work`, `check stuff`

**Categories:**
| Tag | Purpose |
|-----|---------|
| `@smoke` | Critical path - must pass for basic functionality |
| `@security` | Security and privacy checks |
| `@accessibility` | WCAG compliance checks |
| `@data-integrity` | Verifies data accuracy |
| `@access-control` | Permission and gating checks |

**Running Tests:**
```bash
npx playwright test --project=chromium           # Full suite
npx playwright test --grep @smoke --project=chromium  # Smoke tests only
```

### Data Contributions
- Help us expand STATE_CORRUPTION_DATA to all 50 states
- Verify and cite all data sources
- Flag outdated information for review

### Documentation
- Improve README and user guides
- Translate documentation for broader reach
- Write tutorials for new users

## Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Comment complex logic
- Keep functions focused and modular

## Legal

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

## Contact

- **Founder:** Russell Nomer
- **Location:** Plainview, NY
- **Established:** January 8, 2026

*"Don't just watch us—become us."*
