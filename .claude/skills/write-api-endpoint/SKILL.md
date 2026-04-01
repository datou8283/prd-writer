---
name: write-api-endpoint
description: Implement or modify API endpoint code in TypeScript for the backend. Covers handler patterns, zod validation, service layer conventions, error handling, and the implementation checklist.
user-invocable: true
argument-hint: "[endpoint name]"
---

# Skill: Implement API Endpoint

Use this when writing or modifying API endpoint code in TypeScript. For API design principles and documentation format, see `.claude/skills/design-api/SKILL.md`.

## Handler pattern

```typescript
// Route: POST /api/v1/{domain}/{action}

export const handler = async (req: Request, res: Response) => {
  try {
    // 1. Validate input (zod schema)
    const input = PlaceOrderSchema.parse(req.body);

    // 2. Permission check (JWT handled by middleware, domain permissions here)

    // 3. Business logic (call service layer, never inline)
    const result = await tradingService.placeOrder(input);

    // 4. Return envelope
    return res.json({ code: 0, data: result, message: 'success' });
  } catch (err) {
    // Global error handler formats the envelope
    throw err;
  }
};
```

## Validation

- Zod for all request body validation
- Define schemas in `packages/shared/schemas/{domain}.ts`
- Reuse schemas across backend and mobile
- Coerce numeric strings to numbers where callers may send either

## Error handling

- Throw `AppError(code, message)` — global handler wraps in response envelope
- Error messages in three locales: EN, zh-Hans, zh-Hant
- Never expose internal error details (stack traces, DB errors) to client
- For Oracle/external failures: implement retry per `design-api.md` patterns

## Service layer

- Handlers call services, services call repositories — never skip layers
- Business logic lives in services, not handlers
- Side effects (notifications, analytics events) dispatched asynchronously from services
- Trading services must handle edge cases: zero balance, max leverage, liquidation boundary

## Checklist

- [ ] Zod schema for request body in `packages/shared/schemas/`
- [ ] Integration test: happy path + key error cases
- [ ] Error codes documented in `docs/error-codes.md`
- [ ] Rate limit configured if user-facing
- [ ] i18n error messages (EN, zh-Hans, zh-Hant)
- [ ] Idempotency key support for write operations
