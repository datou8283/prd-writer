---
name: write-prd
description: Draft or edit Product Requirements Documents. Covers document structure, user flows, flowchart generation, scope discipline, and the full competitor-analysis-to-tracking-spec workflow.
user-invocable: true
argument-hint: "[feature name]"
---

# Skill: Write PRD

Use this when drafting or editing a Product Requirements Document.

## Document structure (mandatory order)

1. **Feature Overview** — one paragraph: what it is, why it matters
2. **Background & Motivation** — business context, competitive landscape, user pain points
3. **Scope**
   - In Scope (v1): minimal viable feature set
   - Out of Scope (v2+): explicitly list deferred items with brief rationale
4. **User Stories** — table format only (see below)
5. **User Flows** — step-by-step flows for each primary user journey (see below)
6. **Functional Requirements** — detailed behavior specs, grouped by feature area
7. **API Specification** — see `.claude/skills/design-api/SKILL.md` for format and principles
8. **Error Handling** — error codes, user-facing messages, edge cases
9. **Non-Functional Requirements** — performance, security, rate limits, geo-restrictions
10. **Open Questions** — genuinely unresolved items only

## User Stories

Always a table, never prose:

| Role | Action | Outcome |
|------|--------|---------|
| Trader | Place a BBO order on the perpetual market | Order pegs to best bid/ask automatically |

## User Flows

Include one flow per primary user journey. Only cover journeys that involve meaningful decision points or multi-step state changes — skip trivial read-only flows.

Each flow must show:
- **Numbered steps** — one action or system event per step
- **Sub-details** — what the user sees or inputs at that step (bullet list under the step)
- **Decision points** — where the flow branches (e.g. validation pass/fail, oracle succeed/fail); show each branch outcome explicitly
- **System actions** — steps where the system acts without user input (e.g. "AMM rebalances") are included as their own step

Format each step as a two-column row: step number (highlighted) | step title + sub-details. Decision points use a distinct diamond/decision style with labelled branches.

Standard flows to include for any feature with a creation + consumption pattern:
1. **Creation flow** — how a user sets up or initialises the feature (e.g. create market, place order, enable setting)
2. **Core usage flow** — the primary action a user takes once the feature exists (e.g. trade on a market, redeem a position)

Add additional flows for non-obvious lifecycle events (e.g. resolution, expiry, error recovery) if they involve user-visible steps.

## Decision placement

Decisions go in the relevant body section, not in Open Questions. If a decision was made during discussion, weave it into Functional Requirements, API Spec, or Error Handling. Open Questions is strictly for items pending engineering or stakeholder input.

## Scope discipline

- v1 = minimum feature set that delivers value
- Known tradeoffs are acceptable if documented
- If it can be deferred without blocking core value, defer it
- Always state what's out of scope and why

## Writing style

- Technical but readable — an engineer implements from this doc alone
- Precise requirement language: must, should, may
- No ambiguity in specs — every field, status code, edge case covered
- Tables over prose for structured data
- Concise paragraphs, no filler

## Workflow

1. **Competitor analysis** — run `.claude/skills/crypto-exchange-competitor-analysis/SKILL.md` first, deliver report
2. Clarify scope — use analysis findings to confirm v1 vs deferred
3. Validate architecture — discuss key design decisions informed by competitor patterns
4. Draft PRD — full document in structure above, reference analysis in Background & Motivation
5. Iterate — targeted section edits, not full rewrites
6. Deliver as `.docx` file
7. **Tracking spec** — run `.claude/skills/write-posthog-events/SKILL.md` to define analytics events for the feature

## Flowchart diagrams

User flows must be delivered as **PNG image files** (not table-based layouts in the docx).

- Generate one PNG per flow using Python + Pillow (`from PIL import Image, ImageDraw, ImageFont`)
- Filename convention: `flow-<slug>.png`, e.g. `flow-create-conviction.png`, `flow-place-order.png`
- Save PNGs alongside the `.docx` in the same `/docs/` folder
- Embed the PNG images into the `.docx` at §5 (User Flows section)
- Use `SCALE = 3` for hi-dpi output; all coordinates go through `def S(x): return int(round(x * SCALE))`

### Node palette (Whimsical-style — pastel fills, no dark solid backgrounds)

| Node type | Use when | Fill | Border | Text |
|-----------|----------|------|--------|------|
| `PAL_START` pill | First/last node | `#EDE9FF` | `#9B8EC4` | `#5C3D9E` |
| `PAL_STEP` rounded-rect | User action / regular step | `#F4F4F6` | `#C4C4CC` | `#333344` |
| `PAL_SYSTEM` rounded-rect | System acts without user input | `#EAF4FF` | `#7AB0DC` | `#1A5C8A` |
| `PAL_DECISION` diamond | Branch point | `#FEF3CD` | `#F0B429` | `#7A5200` |
| `PAL_SUCCESS` rounded-rect | Terminal success state | `#E6F9EE` | `#6CC08B` | `#1B5E35` |
| `PAL_ERROR` rounded-rect | Error / rejection box | `#FFE8E8` | `#E07070` | `#8B1A1A` |

Branch labels: Yes/Pass in `#2E7D32`, No/Fail in `#C62828`.

### Node sizing (critical — adaptive widths)

**Never use a fixed width for all nodes.** Each node's width must be computed from its text content:

```python
def node_size(n):
    pad_x = S(16)  # padding each side
    # Measure title (FONT_BODY) and all sub-items (FONT_SMALL)
    max_text_w = max(text_width(title), text_width(sub1), text_width(sub2), ...)
    w = max_text_w + pad_x * 2
    # Decision diamonds need ~1.7× text width (text sits inside rotated shape)
    if diamond: w = int(text_width * 1.7) + pad_x
    return max(w, S(60))  # minimum width
```

Boxes are always **centered on CX** regardless of individual width. This gives a clean, content-hugging look — short labels get narrow boxes, long sub-items get wider boxes.

### Line thickness (critical — keep thin and delicate)

All lines must be **thin** — use absolute pixel widths, never scaled values:

- Arrow lines: `width = 2` (absolute pixels, NOT `S(2)` which would be 6px at SCALE=3)
- Node borders / outlines: `width = 2` (absolute pixels, NOT `S(1)`)
- Loop-back / retry lines: `width = 2` (absolute pixels)

This produces clean, Whimsical-style diagrams. Thick lines make the diagram look chunky and unprofessional.

### Arrow style

- Main flow: solid gray (`#AAAAAA`) vertical arrows, `width = 2`
- Error branch to error box: solid, coloured with `PAL_ERROR` border colour, `width = 2`
- Loop-back path: solid, coloured with `PAL_ERROR` border colour, `width = 2`

### Arrowhead convention

```python
AH = S(2.5)  # half-size — keep proportional to thin lines (NOT S(4))

def arrowhead(draw, x, y, direction, color):
    if   direction == "down":  pts = [(x,y),(x-AH,y-AH*2),(x+AH,y-AH*2)]
    elif direction == "right": pts = [(x,y),(x-AH*2,y-AH),(x-AH*2,y+AH)]  # tip at x, base left
    elif direction == "left":  pts = [(x,y),(x+AH*2,y-AH),(x+AH*2,y+AH)]  # tip at x, base right
    elif direction == "up":    pts = [(x,y),(x-AH,y+AH*2),(x+AH,y+AH*2)]
    draw.polygon(pts, fill=color)
```

Use `"right"` for the loop-back arrowhead (entering from the left side of a node).
Line terminates at `arrowhead_base = loop_x_target - AH*2` so the line never enters the node.

### Error-loop routing (critical — must follow exactly)

The loop-back path from the error box to the retry target must **never cross or overlap any node**.
Route as four segments:

```
① DOWN   error-box bottom-centre → y_route_bottom  (= E_TOP + EH + S(14), guaranteed below error box)
② LEFT   y_route_bottom          → pipe_x          (= target_left - S(24), left of main flow)
③ UP     pipe_x                  → loop_y_target    (mid-height of target node)
④ RIGHT  pipe_x                  → loop_x_target - AH*2  (stop at arrowhead base, outside node)
```

Then draw arrowhead with `direction="right"`, tip at `loop_x_target` (left edge of target node).
This means the arrowhead points **rightward into the node** and the dashed line never enters the box.

## Release notes (when requested separately)

Short punchy opening, emoji-accented bullets, benefit-focused, approachable non-technical tone. Target: end users, not engineers.
