---
name: write-release-note
description: >
  Generate app release notes for App Store / Google Play and in-app announcements.
  User-benefit focused, Coinbase-inspired tone. Accepts version number, feature list,
  or PRD as input.
user-invocable: true
argument-hint: "[version number or feature list]"
---

# Skill: Write Release Note

Generate release notes in two formats: App Store / Google Play listing, and in-app announcement.

## Input resolution

Accept any of these inputs and combine as needed:

1. **Version number** (e.g., `v2.5.0`) — extract commits from `git log` for that version/tag, cross-reference with PRDs in `docs/`
2. **Feature list** — user describes or lists what shipped in this release
3. **PRD path** — read the PRD and extract user-visible functionality

If multiple inputs are available, combine them. Prioritize user-facing features over internal changes.

## Output: two versions

Always produce both versions in a single response.

---

### Version 1: App Store / Google Play

Structure:
1. **Hook** — one opening line, user-focused excitement (e.g., "Your trading experience just leveled up!")
2. **Bullets** — 3-6 bullet points, one line each
3. **CTA** — one closing line (e.g., "Update now and explore what's new!")

Rules:
- Each bullet focuses on **user benefit**, not technical implementation
- Lead with the outcome: "Place orders that automatically chase the best price" not "Added Chase Order functionality"
- Most impactful feature first
- Bug fixes: one line at the end — "Bug fixes and performance improvements" unless a major fix deserves its own bullet
- Security updates: place prominently with "Enhanced security" framing
- Stay under 4000 characters (App Store limit)

Example:
```
Your trading experience just leveled up!

- Place orders that automatically chase the best price — new Chase Orders keep you at the top of the book
- Protect your principal with Shield — earn yield without downside risk
- Track your staking rewards in real-time with the new veASTER dashboard
- Bug fixes and performance improvements

Update now and explore what's new!
```

---

### Version 2: In-App Announcement

Structure:
1. **Title** — short, includes version number and headline features (e.g., "v2.5.0: Chase Orders & Shield")
2. **Feature sections** — one section per major feature, each with:
   - Section heading (feature name)
   - 1-2 sentences: what it is + why it matters to the user
3. **Optional CTA** — suggest button text for each feature (e.g., "Try Chase Orders →")

Example:
```
# v2.5.0: Chase Orders & Shield

## Chase Orders
Never miss the best price. Chase Orders automatically follow the best bid or ask, keeping your orders competitive without manual adjustments.

## Shield
Earn yield with zero downside. Shield products protect your principal while giving you exposure to market upside.

## Staking Dashboard
See exactly what your veASTER is earning. The new real-time dashboard shows rewards by epoch, projected APY, and governance power.
```

---

## Writing guidelines

**Tone**: conversational, confident, user-first — like explaining a new feature to a friend who trades crypto.

**Do**:
- Use active voice: "You can now..." / "Place orders that..."
- Use crypto terms users know: leverage, liquidation, staking, APY, orderbook
- Sort features by impact — most exciting first
- Keep sentences short and punchy

**Don't**:
- Use passive voice: "A feature has been added..."
- Use internal jargon: endpoint, schema, websocket, API, migration
- List backend-only changes (unless they affect UX, e.g., faster order execution)
- Over-explain — one sentence per feature is usually enough for App Store version

**Edge cases**:
- Maintenance-only release (no new features): "We've been working behind the scenes to make Aster faster and more reliable. This update includes performance improvements and bug fixes."
- Hotfix release: lead with the fix if user-impacting, otherwise use the maintenance template
- Major release: consider a longer in-app announcement with screenshots or deep links

## Domain context

Product lines: Perpetual futures, Spot, Shield, Staking (veASTER), Prediction Markets, Wallet.
Users: crypto traders (beginner to professional), English-speaking.
