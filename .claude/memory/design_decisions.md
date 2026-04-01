---
name: Design decisions log
description: Accumulated architectural and API design decisions across features. Reference before proposing new patterns to maintain consistency.
type: project
---

# Design Decisions

Ongoing log of design decisions made across features. Check here before proposing new patterns.

## API & Architecture

- **Response envelope**: all endpoints return `{ code: 0, data, message: "success" }`. Non-zero code = error.
- **Error codes**: 5-digit, domain-scoped (10xxx auth, 20xxx trading, 30xxx staking, 40xxx wallet).
- **Endpoint naming**: `{METHOD} /api/v1/{domain}/{action}`, kebab-case. Action-based paths preferred over forced RESTful.
- **Idempotency**: all write operations support client-generated request IDs.
- **i18n**: always EN, zh-Hans, zh-Hant. No hardcoded user-facing strings.
- **Parameterization**: never hardcode trading pairs, fee rates, leverage tiers, or thresholds.

## Trading Domain

- **BBO (Best Bid/Offer)**: single `pegPrice` enum on standard orders endpoint (Binance Futures `priceMatch` convention), NOT a separate endpoint. Fallback when one side empty: other side +/- tick size.
- **Chase Order**: maker-targeting — Buy -> Best Bid, Sell -> Best Ask (not reversed).
- **Order types**: follow Binance Futures naming conventions where applicable.

## DEX Model

- One wallet address = one uid = one user (no separate account layer).
- Subscription control is two-dimensional: user-level + device-level.

## Products

- **Prediction Markets**: binary YES/NO shares in USDT, `>=` and `<` operators only.
- **Shield**: principal-protected product (always use full name).
- **veASTER**: vote-escrowed ASTER token for staking governance.

## Oracle & External Services

- Retry with exponential backoff: 3 attempts, 10s intervals.
- Failure = retries exhausted, not a single failed call.
- On full failure: hold state (e.g., Locked), escalate via alerts — never auto-cancel.
- HMAC authentication for external partner callbacks.

## PostHog Event Naming

- Format: `{product}_{object}_{action}` (snake_case).
- Products: perpetual, spot, shield, staking, prediction, wallet, account.
- Standardized verbs: viewed, clicked, placed, canceled, switched, applied, shared, submitted, confirmed.
- Property naming: use specific names (e.g., `notification_type` not `type`) to avoid ambiguity.
- Bind flows: split into started -> completed/failed for funnel analysis.
