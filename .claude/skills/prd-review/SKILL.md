---
name: prd-review
description: >
  Multi-role PRD review — Product Lead, Engineering Lead, Design Lead, QA Lead.
  Runs four opinionated reviews tuned to crypto exchange domain conventions,
  produces a consolidated findings summary grouped by severity.
user-invocable: true
argument-hint: "[feature name or PRD path]"
---

# Skill: PRD Review

Use this to review a PRD from four role perspectives before human review. Works standalone (`/prd-review`) or automatically within `/feature-workflow`.

## Input resolution

1. If a file path is provided, read that `.docx` from `docs/`
2. If only a feature name is provided, find the most recent `*-prd.docx` in `docs/` by modification time
3. If no `.docx` found, use PRD content from the current conversation context

Read the **full PRD content** before starting any role review.

## Review protocol

Applies to all four roles:

- Be **opinionated and specific**. Reference actual section content, field names, endpoint paths — never give generic feedback.
- Cross-reference domain conventions from `CLAUDE.md` (error code domains, oracle retry patterns, BBO semantics, DEX model, i18n requirements).
- Cross-reference API conventions from `.claude/skills/design-api/SKILL.md` (envelope pattern, endpoint naming, idempotency, parameter flexibility).
- Each role outputs exactly: **2-3 key findings** + **1 praise**.
- Severity per finding:
  - `[RED]` must fix — blocks ship
  - `[YELLOW]` should fix — meaningful gap
  - `[GREEN]` nice to have — polish

---

## Role 1: Product Lead

- Is v1 scope right-sized? Too broad dilutes focus, too narrow misses competitive parity. Cross-check Section 3 (Scope) with Section 2 (Background).
- Are user stories in Section 4 comprehensive? Missing personas (market maker, liquidated trader, admin, new user)?
- Is competitive positioning clear in Section 2? Does it reference competitor analysis findings?
- Are success metrics / KPIs defined? If not, flag as must-fix — every PRD needs measurable outcomes.
- Section 10 (Open Questions): are items genuinely open or should they be resolved decisions?

---

## Role 2: Engineering Lead

- Is the API spec in Section 7 sound per `design-api.md`? Check: response envelope `{ code, data, message }`, 5-digit error codes in correct domain (10xxx auth, 20xxx trading, 30xxx staking, 40xxx wallet), kebab-case paths, idempotency keys on writes.
- Missing error codes or edge cases in Section 8? (zero balance, max leverage, liquidation boundary, oracle timeout, rate limit exhaustion)
- Is the data model implicit or explicit? If endpoints reference entities without defining schema, flag it.
- Performance/scalability: WebSocket fan-out, orderbook depth queries, pagination on list endpoints.
- Oracle/external service patterns: retry with backoff (3 attempts, 10s), hold-on-failure, never auto-cancel?
- i18n: user-facing strings flagged for EN, zh-Hans, zh-Hant?

---

## Role 3: Design Lead

- Are user flows in Section 5 complete? Check for missing states: loading, empty, error, timeout.
- Information hierarchy: is it logical for the primary user action? (e.g., order form prominence vs secondary info)
- Mobile vs web: are differences addressed? React Native constraints (no hover, bottom sheet vs modal, touch targets)?
- Flow diagrams: do they cover unhappy paths, not just the golden path?
- Accessibility: color contrast, keyboard navigation for web, screen reader considerations.

---

## Role 4: QA Lead

- Are acceptance criteria in Section 6 testable? Each requirement should map to a concrete test case.
- Edge cases enumerated: zero balance, max leverage (125x), liquidation boundary, minimum order size, empty orderbook, single-sided book (BBO fallback).
- Error scenarios from Section 8: all error codes tested? User-facing messages validated for all three locales?
- List 5-8 concrete integration test cases (happy path, boundary, concurrent, failure recovery).
- WebSocket/real-time: reconnection and stale-data scenarios covered?

---

## Output format

Present findings grouped by severity, not by role. Keep each finding to 1-2 sentences.

```
# PRD Review: {feature name}

## [RED] Must Fix
- **[Role]** Finding — specific description referencing PRD section

## [YELLOW] Should Fix
- **[Role]** Finding — specific description referencing PRD section

## [GREEN] Nice to Have
- **[Role]** Finding — specific description referencing PRD section

## What's Working Well
- **Product Lead**: {praise}
- **Engineering Lead**: {praise}
- **Design Lead**: {praise}
- **QA Lead**: {praise}

---
Summary: X must-fix, Y should-fix, Z nice-to-have.
Recommendation: proceed / address must-fix first / significant rework needed
```

Target: the entire output should be scannable in under 2 minutes.
