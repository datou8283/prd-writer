---
name: write-posthog-events
description: Define PostHog analytics event tracking specs for Aster Exchange web and mobile products. Use when the user asks to create, review, or update event tracking plans, analytics specs, or data instrumentation — typically after a PRD is written.
---

# PostHog Event Tracking Spec

Use this after a PRD is finalized to define the analytics events for the feature. The goal is to produce a complete tracking spec that engineers can implement directly and that product/data teams can use for analysis.

## Workflow

1. Read the PRD to identify all user-facing interactions and key system responses
2. Map each trackable interaction to an event
3. Define properties for each event
4. Assign trigger points
5. Note business goals where applicable
6. Output as a structured table

## Event naming convention

Format: `{product}_{object}_{action}`

- All lowercase, snake_case
- `{product}` — the product area: `perpetual`, `spot`, `shield`, `staking`, `prediction`, `wallet`, `account`
- `{object}` — the specific UI element or domain object: `order`, `position`, `market`, `orderbook`, `chart`, etc.
- `{action}` — what happened, past tense: `viewed`, `placed`, `canceled`, `clicked`, `switched`, `applied`, `shared`

Examples:
- `perpetual_order_placed`
- `spot_market_viewed`
- `shield_position_closed`
- `staking_epoch_claimed`
- `wallet_deposit_submitted`

## Action verbs (standardized)

Use these consistently — don't mix synonyms:

| Action | When to use |
|--------|-------------|
| `viewed` | User sees a page or detail screen |
| `clicked` | User taps a button or tab (no state change) |
| `placed` | User submits an order or transaction |
| `canceled` | User cancels an order or action |
| `switched` | User toggles between display options |
| `applied` | User applies a filter, sort, or setting |
| `shared` | User triggers a share action |
| `submitted` | User submits a form (deposit, withdrawal, etc.) |
| `confirmed` | User confirms a modal or action |

## Property types

| Type | Usage |
|------|-------|
| String | Free-form or known set of values (e.g., symbol) |
| Enum | Fixed set of values — list all possible values |
| Boolean | true / false |
| Num | Numeric value |
| JSON String | Structured data as serialized JSON |

## Output format

Each event spec should be a table with these columns:

| Column | Description |
|--------|-------------|
| Event name | snake_case event name |
| Trigger point | When exactly the event fires — be specific |
| Property | Property name (snake_case) |
| Type | String / Enum / Boolean / Num / JSON String |
| Property value | All possible values or format description |
| Business goal | Why we track this (optional, fill when non-obvious) |
| Status | Completed / Develop / Kick-off / empty |

For events with multiple properties, the first row carries the event name and trigger point; subsequent property rows leave those columns empty (same as the existing CSV convention).

## Property guidelines

- Property names are snake_case: `order_type`, `margin_mode`, `sort_by`
- `symbol` is always String type with values like `BTCUSDT`, `ETHUSDT`
- Boolean properties: always `true / false`, not `0 / 1`
- Enum properties: list ALL possible values explicitly
- When a property value is unclear or depends on implementation, write a description instead and flag for engineering input
- Events with no meaningful properties use `-` for Property, Type, and Property value

## Trigger point guidelines

- Write in English
- Be specific about the exact moment: "When user taps the place order button" not just "When placing order"
- Distinguish between user-initiated vs system-response triggers:
  - User action: "When user taps..." / "When user views..."
  - System response: "When WebSocket returns order result" / "When API returns success"

## What to track

For a typical feature, cover these interaction types:

1. **Page/screen views** — user lands on a key screen (`_viewed`)
2. **Core actions** — the main thing users do in this feature (`_placed`, `_submitted`, `_canceled`)
3. **Configuration choices** — settings, filters, toggles that reveal user preferences (`_switched`, `_applied`)
4. **Results/outcomes** — success/failure of key operations (especially async ones)
5. **Engagement signals** — sharing, clicking into details, exploring sub-features

Don't track every micro-interaction. Focus on events that answer:
- Are users using this feature?
- How are they using it? (which options, configurations)
- Is it working? (success/failure rates)

## Aster domain context

Key products and their prefixes:
- **Perpetual futures** → `perpetual_`
- **Spot trading** → `spot_`
- **Shield** (principal-protected) → `shield_`
- **veASTER staking** → `staking_`
- **Prediction markets** → `prediction_`
- **Wallet** (deposit/withdraw) → `wallet_`
- **Account** (login, settings) → `account_`

Common properties across trading events: `symbol`, `direction`, `leverage`, `margin_mode`, `order_type`
