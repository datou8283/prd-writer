# PRD Writer

Cryptocurrency trading platform — perpetual futures, spot, Shield, staking, prediction markets.
TypeScript monorepo: Node backend, React Native mobile (iOS + Android), Next.js admin dashboard.

## Commands

- `npm run dev` — start dev server
- `npm run test` — run Jest tests
- `npm run lint` — ESLint + Prettier
- `npm run build` — production build
- `npm run typecheck` — tsc --noEmit

## Architecture

- `/packages/api` — Node.js backend services
- `/packages/mobile` — React Native app (iOS + Android)
- `/packages/admin` — Next.js admin dashboard
- `/packages/shared` — shared types, utils, constants, zod schemas
- `/docs` — PRDs, API specs, architecture decisions

## Conventions

- All API responses: `{ code: number, data: T, message: string }` envelope
- Error codes: 5-digit numeric (10xxx auth, 20xxx trading, 30xxx staking, 40xxx wallet)
- i18n: always provide EN, zh-Hans, zh-Hant — no hardcoded user-facing strings
- Never hardcode trading pairs, fee rates, leverage tiers, or thresholds — always parameterized
- Order types follow Binance Futures naming conventions where applicable
- Validation: zod schemas in `packages/shared/schemas/`, reused across backend and mobile
- Oracle integrations: retry with backoff (3 attempts, 10s intervals); failure = retries exhausted, not single fail

## Domain terms

- **Perpetual** — perpetual futures contract (use full word in code, not "perp")
- **Shield** — principal-protected product
- **veASTER** — vote-escrowed ASTER token for staking governance
- **BBO** — Best Bid/Offer order modifier; single `pegPrice` enum (modeled after Binance Futures `priceMatch`), not a separate endpoint
- **Chase Order** — maker-targeting order: Buy → Best Bid, Sell → Best Ask (not reversed)
- **Epoch** — staking reward period for veASTER
- **DEX model** — one wallet address = one uid = one user (no separate account layer)

## Skills

- `.claude/skills/crypto-exchange-competitor-analysis.md` — competitor research workflow, run before writing PRDs
- `.claude/skills/write-prd.md` — PRD document structure, format, writing style, scope discipline
- `.claude/skills/design-api.md` — API design principles, envelope pattern, error codes, field tables (shared by PRD and code)
- `.claude/skills/write-api-endpoint.md` — TypeScript endpoint implementation patterns
- `.claude/skills/write-posthog-events.md` — PostHog analytics event tracking spec, run after PRD is finalized

Feature workflow: competitor analysis → clarify scope → validate architecture → draft PRD → deliver `.docx` → write tracking spec.

## Testing

- New API endpoints: integration tests (happy path + key error cases)
- Trading logic: unit tests with edge cases (zero balance, max leverage, liquidation boundary)
- Mobile components: snapshot tests for UI, unit tests for hooks

## Git

- Branch: `feat/JIRA-123-short-description` or `fix/JIRA-456-short-description`
- Commits: conventional commits (feat:, fix:, chore:, docs:)
- Run lint + typecheck before committing
