---
name: feature-workflow
description: >
  End-to-end PRD workflow — competitor analysis, scope clarification,
  PRD drafting (with API spec + optional admin wireframes), .docx delivery,
  and PostHog tracking spec. Orchestrates existing skills with human checkpoints.
user-invocable: true
argument-hint: "[feature name]"
---

# Skill: Feature Workflow

End-to-end orchestrator for the PRD feature pipeline. Takes a feature name, runs through three phases with two human checkpoints, and delivers all documents.

## Slug rule

Convert the feature name to a slug used across all deliverables: lowercase, hyphen-separated, no special characters.
Example: "Offline Event Promotion" → `offline-event-promotion`

Use `{slug}` consistently in every filename below.

---

## Phase 1 — Competitor Analysis

Invoke `/crypto-exchange-competitor-analysis {feature name}`.

Deliver: `docs/{slug}-competitor-analysis.docx`

When complete, present findings as a concise summary:
- What each Tier 1 competitor offers (Binance, OKX, Hyperliquid)
- Notable patterns in UX, naming, and API design
- Recommended v1 scope based on competitive landscape
- Key design decisions the user should weigh

---

## ⏸ Checkpoint 1 — Scope & Architecture

**STOP. Do not proceed until the user responds.**

Ask the user three questions:

1. **v1 Scope** — Based on the competitor analysis, confirm which capabilities are in-scope for v1 and which are deferred to v2+.
2. **Architecture decisions** — Flag any architecture choices informed by competitor patterns (e.g., endpoint structure, order flow, oracle design) that need validation.
3. **Admin pages** — Does this feature require admin dashboard pages (management console, CRUD interfaces, monitoring)?

Capture all answers as context for Phase 2.

---

## Phase 2 — Draft PRD

Invoke `/write-prd {feature name}`, passing:
- Competitor analysis context from Phase 1
- Scope decisions and architecture validation from Checkpoint 1

The write-prd skill already uses `/design-api` conventions for Section 7 (API Specification) — do not invoke it separately.

### Conditional: Admin Wireframes

**If** the user confirmed admin pages at Checkpoint 1, **or** the PRD draft's Section 6 (Functional Requirements) contains admin dashboard / management console requirements:

→ Invoke `/admin-wireframe` to generate wireframe PNGs and embed them in the `.docx` via `doc.add_picture()`.

**Otherwise**, skip this step entirely.

### Deliverables

- `docs/{slug}-prd.docx` — the PRD document
- `docs/flow-*.png` — user flow diagrams (1+ files)
- `docs/wireframe-*.png` — admin wireframes (0+ files, conditional)
- `docs/generate-{slug}-prd.py` — the generator script

---

## Phase 2.5 — Multi-Role Review

After the PRD is drafted and the `.docx` is generated, automatically invoke `/prd-review {feature name}`.

This runs four role-based reviews (Product Lead, Engineering Lead, Design Lead, QA Lead) against the PRD content and produces a consolidated findings summary grouped by severity.

Present the consolidated review to the user as part of Checkpoint 2 below.

---

## ⏸ Checkpoint 2 — PRD Review

**STOP. Do not proceed until the user approves.**

Present two things:
1. The PRD structure: list each section heading with a one-line summary of what it covers.
2. The multi-role review findings from Phase 2.5.

Ask: "Review the PRD alongside the multi-role feedback above. Which findings do you want to address? Or approve to proceed to tracking spec."

If the user requests changes:
- Make targeted section edits (do not rewrite the entire document)
- Re-generate the `.docx`
- Present the updated structure again

Only proceed to Phase 3 when the user explicitly approves.

---

## Phase 3 — Tracking Spec & Delivery

Invoke `/write-posthog-events {feature name}`, reading from the finalized PRD.

Deliver: `docs/{slug}-posthog-events.docx`

Present a summary: number of events defined, categorized by trigger type (user action vs. system response).

---

## Optional: Git Commit

Ask the user: "Commit and push all deliverables to git?"

If yes, stage all generated files:
- `docs/{slug}-competitor-analysis.docx`
- `docs/{slug}-prd.docx`
- `docs/{slug}-posthog-events.docx`
- `docs/flow-*.png` (generated during this workflow)
- `docs/wireframe-*.png` (generated during this workflow)
- `docs/generate-{slug}-prd.py`

Commit message: `docs: add {slug} PRD, competitor analysis, and tracking spec`

Push to current branch.

---

## Deliverables Checklist

| Deliverable | File | Phase |
|---|---|---|
| Competitor analysis | `docs/{slug}-competitor-analysis.docx` | 1 |
| Flow diagrams | `docs/flow-*.png` (1+ files) | 2 |
| Admin wireframes | `docs/wireframe-*.png` (0+ files, conditional) | 2 |
| PRD | `docs/{slug}-prd.docx` | 2 |
| Generator script | `docs/generate-{slug}-prd.py` | 2 |
| PostHog tracking spec | `docs/{slug}-posthog-events.docx` | 3 |
