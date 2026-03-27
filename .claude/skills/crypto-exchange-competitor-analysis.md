---
name: crypto-exchange-competitor-analysis
description: Research how competing crypto exchanges implement a feature before writing a PRD. Produces a standalone competitor analysis report covering Binance, OKX, Hyperliquid, and relevant Tier 2 exchanges.
user-invocable: true
argument-hint: "[feature name]"
---

# Skill: Crypto Exchange Competitor Analysis

Use this when researching how competing exchanges implement a feature before writing a PRD. The output is a standalone competitor analysis report that feeds into the PRD's Background & Motivation and Functional Requirements.

## Competitor set

### Tier 1 — always analyze
- **Binance** (CEX) — market leader, de facto standard for order types and API conventions
- **OKX** (CEX) — strong derivatives, aggressive feature shipping
- **Hyperliquid** (DEX) — on-chain perps, closest DEX competitor to Aster

### Tier 2 — analyze when relevant
- **EdgeX** (DEX) — decentralized derivatives, relevant for perps and margin features
- **Lighter** (DEX) — on-chain order book, relevant for matching engine and order type design
- **Bybit** (CEX) — large derivatives volume, relevant for copy trading and campaign mechanics
- **dYdX** (DEX) — v4 appchain model, relevant for L1 and governance features
- **Polymarket** (prediction) — relevant only for prediction market features

Select 3-5 competitors per analysis based on feature relevance. Not every competitor is relevant to every feature.

## Research dimensions

For each competitor that offers the feature (or a comparable one), investigate:

1. **Feature availability** — does it exist? Since when? Which platforms (web, mobile, API)?
2. **User flow** — how many steps from entry point to completion? Key screens and decision points
3. **Naming & positioning** — what do they call it? How do they describe it to users?
4. **Parameters & configuration** — what can the user control? What's fixed? What are the defaults?
5. **API design** — endpoint structure, request/response shape, parameter naming conventions
6. **Edge cases & limitations** — what's restricted? What happens on failure? Known complaints?
7. **Fee structure** — any fee differences for this feature vs standard?

Not every dimension applies to every feature. Skip what's irrelevant.

## Research method

1. **Product docs & help center** — official documentation is the primary source (e.g., Binance Futures FAQ, OKX Learn, Hyperliquid docs)
2. **API documentation** — for API design patterns, parameter naming, endpoint structure
3. **App / web walkthrough** — if accessible, observe actual UX flow
4. **Community & social** — Twitter/X, Discord, Reddit for user sentiment and known issues
5. **Changelogs & announcements** — when was the feature launched or last updated?

Always cite sources. If something is inferred rather than verified, mark it clearly.

## Report structure

### 1. Executive summary
2-3 sentences: what was analyzed, key takeaway, primary recommendation for Aster.

### 2. Feature comparison matrix

| Dimension | Binance | OKX | Hyperliquid | [Others] |
|-----------|---------|-----|-------------|----------|
| Available? | ✅ | ✅ | ❌ | ... |
| Platform | Web, App, API | Web, App, API | Web, API | ... |
| User flow steps | 3 | 4 | N/A | ... |
| Key parameters | ... | ... | ... | ... |
| Fee impact | ... | ... | ... | ... |

Keep the matrix scannable. Details go in per-competitor sections below.

### 3. Per-competitor deep dive
One section per analyzed competitor. Include:
- How the feature works (user perspective)
- Notable UX decisions (good or bad)
- API design choices worth noting
- Screenshots or flow descriptions where helpful

### 4. Gap analysis
What do competitors offer that Aster doesn't? What does Aster offer that competitors don't? Where is the market converging?

### 5. Recommendations for Aster
Concrete, actionable input for the PRD:
- Which competitor's approach to follow (and why)
- Which to deliberately diverge from (and why)
- Suggested v1 scope based on competitive landscape
- Naming recommendations (align with industry conventions vs differentiate)

## Delivery

- Format: `.docx` file
- Filename: `{feature-name}-competitor-analysis.docx`
- This report is a separate deliverable from the PRD
- Reference it in the PRD's Background & Motivation section

## Relationship to PRD workflow

```
competitor analysis → PRD
```

1. Run this skill first to produce the analysis report
2. Use findings to inform PRD scope, naming, API design, and feature decisions
3. In the PRD, cite the analysis: "Per competitor analysis, Binance uses X approach..."
4. Decisions influenced by competitor research should be explicit, not assumed
