---
name: design-api
description: Design API endpoints for Aster Exchange following the standard envelope pattern, error code domains, and naming conventions. Use when designing APIs in a PRD or reviewing endpoint specifications.
user-invocable: true
argument-hint: "[endpoint or feature name]"
---

# Skill: Design Aster API

Use this when designing API endpoints (in a PRD) or implementing them (in code). This skill covers design principles and documentation format. For TypeScript implementation patterns, see `.claude/skills/write-api-endpoint.md`.

## Response envelope

Every endpoint returns:
```json
{
  "code": 0,
  "data": { ... },
  "message": "success"
}
```
- `code: 0` = success
- `code: non-zero` = domain-specific error (5-digit numeric)

## Error code domains

- 10xxx — authentication & authorization
- 20xxx — trading (orders, positions, liquidation)
- 30xxx — staking (veASTER, epochs, validators)
- 40xxx — wallet (deposits, withdrawals, transfers)

## Endpoint naming

- Pattern: `{METHOD} /api/v1/{domain}/{action}`
- Examples: `POST /api/v1/trading/place-order`, `GET /api/v1/staking/my-positions`
- Use kebab-case for paths
- RESTful where natural, but don't force it — action-based paths are fine for complex operations

## API spec format (for PRDs)

For each endpoint, document:

**Method + path + description + auth requirement**, then:

Request body fields as a table:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| symbol | string | Yes | Trading pair, e.g., "BTC-USDT" |
| side | enum | Yes | "BUY" or "SELL" |

Response body fields as a table (same columns).

HTTP status codes and domain error codes.

Example request/response JSON.

## Design principles

- **Flexibility over hardcoded values** — parameters that could change (pairs, fees, leverage, thresholds) must be configurable, never hardcoded
- **Delegate to callers** — let partners/frontends control UX decisions; backend provides the building blocks
- **Follow Binance Futures conventions** where applicable (e.g., BBO uses `pegPrice` enum modeled after `priceMatch`)
- **Idempotency** — all write operations should support client-generated request IDs for safe retries
- **i18n error messages** — always provide EN, zh-Hans, zh-Hant

## Oracle / external service patterns

- Retry with exponential backoff: 3 attempts, 10-second intervals
- Failure = retries exhausted, not a single failed call
- On full failure: hold state (e.g., Locked), escalate via alerts — never auto-cancel
- HMAC authentication for external partner callbacks

## Domain-specific rules

- **BBO**: single `pegPrice` enum parameter on standard orders endpoint, not a separate endpoint. Fallback when one side of book is empty: use other side ± tick size
- **Chase Order**: targets maker positions — Buy → Best Bid, Sell → Best Ask (not reversed)
- **DEX model**: one wallet address = one uid = one user. Subscription control is two-dimensional (user-level + device-level)
- **Prediction markets**: binary YES/NO shares in USDT, `≥` and `<` operators only
