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
1. **Hook** — one opening line, energetic and user-focused (e.g., "More ways to track, trade, and level up!")
2. **Numbered list** — 3-8 items, numbered (not bullets)
3. No closing CTA needed — the list speaks for itself

Each line format: `{number}. {Bold topic} — {benefit in plain language} {emoji}`

Rules:
- Each line: **bold topic phrase** + em dash + user benefit in conversational tone + relevant emoji at the end
- Lead with the outcome the user cares about, not the feature name
- Most impactful feature first
- Bug fixes / minor improvements: last item, casual tone (e.g., "Plus some bug fixes and little improvements")
- Security updates: place prominently with clear framing
- Stay under 4000 characters (App Store limit)
- Emoji selection: pick one emoji per line that matches the vibe (not random)

Example:
```
More ways to track, trade, and level up!

1. VIP progress made clear — see exactly what you need to reach the next level 🎯
2. More control on the chart — add TP/SL and reverse positions right from the K-line 📈
3. Your trading stats, all in one place — check your performance in the Portfolio page 📊
4. Clearer order type descriptions — pick the right order with confidence 💡
5. Total value now includes staking — see your full portfolio at a glance 💰
6. Plus some bug fixes and little improvements 🛠️
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

**Tone**: casual, upbeat, user-first — like a friend showing you what's new. Short punchy phrases, not full sentences.

**Do**:
- Use em dashes to separate topic from benefit: "VIP progress made clear — see exactly what you need"
- Use active, direct language: "see", "check", "pick", "tap", "track"
- Use crypto terms users know: leverage, TP/SL, K-line, staking, APY, orderbook
- Sort features by impact — most exciting first
- End each line with a relevant emoji
- Keep it scannable — one glance should convey the update

**Don't**:
- Use passive voice: "A feature has been added..."
- Use internal jargon: endpoint, schema, websocket, API, migration
- List backend-only changes (unless they affect UX, e.g., faster order execution)
- Over-explain — the em dash format forces brevity
- Use generic emoji — each one should match the specific feature's vibe

**Edge cases**:
- Maintenance-only release (no new features): "We've been working behind the scenes to make Aster faster and more reliable. This update includes performance improvements and bug fixes."
- Hotfix release: lead with the fix if user-impacting, otherwise use the maintenance template
- Major release: consider a longer in-app announcement with screenshots or deep links

## Domain context

Product lines: Perpetual futures, Spot, Shield, Staking (veASTER), Prediction Markets, Wallet.
Users: crypto traders (beginner to professional), English-speaking.
