---
name: admin-wireframe
description: >
  Generates admin dashboard wireframe PNGs using Pillow whenever there are admin
  dashboard UI requirements in a PRD or feature spec. Use this skill proactively
  whenever the user describes admin pages, management dashboards, CRUD interfaces,
  detail pages, or forms — even if they don't explicitly ask for wireframes. The
  skill produces high-fidelity lo-fi wireframes (SCALE=3, hi-dpi) that can be
  embedded directly into .docx PRDs or shared as standalone screenshots.
---

# Admin Wireframe Generator

This skill generates hi-fidelity lo-fi wireframe PNGs for admin dashboard pages
using Python Pillow. Run it any time admin UI requirements are described — the
wireframes make spec reviews faster and eliminate layout ambiguity for engineers.

## When to use

- PRD has a §6.x Admin Dashboard section describing page layouts
- User says "出圖", "wireframe", "畫個頁面", "generate wireframes", or describes admin pages
- A feature has: list pages, detail pages, create/edit forms, or modals

## Workflow

1. **Understand the screens** — read the PRD or requirements to identify all admin pages
2. **Write a screen generator script** — use `scripts/renderer.py` as the rendering engine
3. **Run it** — `python3 your_generator.py`
4. **Embed in PRD** — add `doc.add_picture(path, width=Inches(5.5))` after the relevant section

## Project conventions (from CLAUDE.md)

- Output directory: `/Users/dannychen/Documents/aster-docs/docs/`
- PRD generator scripts: `docs/generate-<feature>-wireframes.py`
- Output PNGs: `docs/wireframe-<screen-name>.png`
- Embed in PRD via `generate-<feature>-prd.py` using `doc.add_picture()`

---

## Screen types and layout patterns

### List page
```
[Page Title]        [Feature Description subtitle]    [+ Create] btn
[Tab: All | Active | Paused | Ended | Draft]
┌────────────────── table card ──────────────────┐
│ Name │ Status │ Budget (progress) │ ... │ Time  │
│ row… │ badge  │ ████░░  45%      │     │       │
└──────────────────────────────────────────────────┘
< 1 2 3 ... >
```

### Detail page
```
breadcrumb: Section > Item Name
[Page Title]                        [Action btn] [Danger btn]
[Stat] [Stat] [Stat] [Stat]   ← 4-card stat row
┌ QR ┐ ┌─── Budget / Config card ──────────────────┐
└────┘ └────────────────────────────────────────────┘
[Section heading]                         [Export] btn
┌────────── data table ──────────────────────────────┐
└────────────────────────────────────────────────────┘
< pagination >
```

### Create / Edit form page
```
breadcrumb: Section > Create New Item
[Page Title]
┌──────────── form card ─────────────────────────────┐
│ [Full-width field]                                  │
│ [Half field]         [Half field]                   │
│ [Half field]         [computed display]             │
│ [Half field]         [Half field]                   │
│ [Chip selector grid]                                │
│ [Create] btn                                        │
└─────────────────────────────────────────────────────┘
```

### Confirmation modal (over detail page)
```
[dimmed background page]
         ┌────────── modal ──────────┐
         │       ⚠️ icon              │
         │    "Pause Event?"         │
         │  body text line 1         │
         │  body text line 2         │
         ├────────────────────────────┤
         │  Cancel  │  Confirm       │
         └────────────────────────────┘
```

---

## Using scripts/renderer.py

Import the renderer at the top of your generator script:

```python
import sys
sys.path.insert(0, "/Users/dannychen/Documents/aster-docs/.claude/skills/admin-wireframe/scripts")
from renderer import (
    S, W_DEFAULT, hex_to_rgb, _tw,
    FONT_PAGE_TITLE, FONT_SECTION, FONT_TABLE_HEAD, FONT_TABLE_BODY,
    FONT_LABEL, FONT_BADGE, FONT_SMALL, FONT_STAT_NUM, FONT_STAT_LABEL,
    FONT_BUTTON, FONT_BREADCRUMB, FONT_INPUT,
    BG_COLOR, CARD_BG, CARD_BORDER, TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, DIVIDER,
    BADGE_ACTIVE, BADGE_PAUSED, BADGE_ENDED, BADGE_DRAFT,
    BTN_PRIMARY, BTN_WARNING, BTN_DANGER, BTN_OUTLINE, BTN_SUBTLE,
    draw_card, draw_badge, draw_button, draw_progress_bar, draw_tabs,
    draw_pagination, draw_input_field, draw_chip, draw_qr_placeholder, draw_table,
)
from PIL import Image, ImageDraw
```

### Canvas setup

```python
DOCS = "/Users/dannychen/Documents/aster-docs/docs"
W, H = S(400), S(340)  # adjust height per screen
img = Image.new("RGB", (W, H), hex_to_rgb(BG_COLOR))
draw = ImageDraw.Draw(img)
pad = S(12)
img.save(f"{DOCS}/wireframe-my-screen.png")
```

Standard widths: `S(400)` for most pages. Heights: `S(280–320)` list, `S(340–420)` detail, `S(320–380)` form.

### Component reference

| Function | Returns | Notes |
|----------|---------|-------|
| `draw_card(draw, x, y, w, h)` | — | White rounded card with border |
| `draw_badge(draw, x, y, text, style)` | `(w, h)` | style = BADGE_ACTIVE/PAUSED/ENDED/DRAFT |
| `draw_button(draw, x, y, text, style)` | `(w, h)` | style = BTN_PRIMARY/WARNING/DANGER/OUTLINE/SUBTLE |
| `draw_progress_bar(draw, x, y, w, pct)` | `h` | pct = 0.0–1.0 |
| `draw_tabs(draw, x, y, tabs, active_idx)` | `tab_h` | active tab is purple-filled |
| `draw_pagination(draw, x, y)` | — | `< 1 2 3 ... 10 >` |
| `draw_input_field(draw, x, y, w, label, placeholder, suffix)` | `total_h` | returns height for stacking |
| `draw_chip(draw, x, y, text, selected)` | `(w, h)` | multi-select chip |
| `draw_qr_placeholder(draw, x, y, size)` | — | deterministic fake QR pattern |
| `draw_table(draw, x, y, headers, rows, col_widths)` | `bottom_y` | cell can be str, ("badge", text, style), ("progress", pct, label) |

### Right-aligning buttons

```python
btn_w, btn_h = draw_button(draw, 0, 0, "Label", BTN_PRIMARY)  # measure first
draw_button(draw, W - pad - btn_w, title_y, "Label", BTN_PRIMARY)
```

### Confirmation modal overlay (RGBA composite)

```python
overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ov_draw = ImageDraw.Draw(overlay)
ov_draw.rectangle([0, 0, W, H], fill=(30, 30, 50, 160))
img = img.convert("RGBA")
img = Image.alpha_composite(img, overlay)
img = img.convert("RGB")
draw = ImageDraw.Draw(img)  # redraw on composited image
# then draw modal card, icon, text, buttons
```

---

## Color palette reference

| Name | Hex | Use |
|------|-----|-----|
| BG_COLOR | #F5F5F7 | Page background |
| CARD_BG | #FFFFFF | Card/panel fill |
| CARD_BORDER | #E0E0E4 | Card outline |
| TEXT_PRIMARY | #1A1A2E | Headings, body |
| TEXT_SECONDARY | #6B6B80 | Labels, secondary text |
| TEXT_MUTED | #9B9BAE | Placeholder, hints |
| PROGRESS_FILL | #5C3D9E | Primary purple |
| BADGE_ACTIVE | green family | Active status |
| BADGE_PAUSED | yellow family | Paused status |
| BADGE_ENDED | red family | Ended status |
| BADGE_DRAFT | grey family | Draft status |
| BTN_PRIMARY | #5C3D9E bg / #FFF text | Primary CTA |
| BTN_WARNING | #F0B429 bg | Pause actions |
| BTN_DANGER | #E07070 bg | Destructive actions |
| BTN_OUTLINE | #FFF bg / #5C3D9E border | Secondary CTA |

---

## Full example: minimal list page

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, "/Users/dannychen/Documents/aster-docs/.claude/skills/admin-wireframe/scripts")
from renderer import *
from PIL import Image, ImageDraw

DOCS = "/Users/dannychen/Documents/aster-docs/docs"
W, H = S(400), S(280)
img = Image.new("RGB", (W, H), hex_to_rgb(BG_COLOR))
draw = ImageDraw.Draw(img)
pad = S(12)

draw.text((pad, S(8)), "My Feature Management", fill=hex_to_rgb(TEXT_PRIMARY), font=FONT_PAGE_TITLE)
draw_button(draw, W - pad - S(80), S(8), "+ Create", BTN_PRIMARY)
tab_h = draw_tabs(draw, pad, S(28), ["All", "Active", "Draft"], active_idx=0)

card_y = S(44)
draw_card(draw, pad, card_y, W - pad * 2, H - card_y - S(8))

headers = ["Name", "Status", "Created"]
col_widths = [S(140), S(50), S(180)]
rows = [
    ["My Item", ("badge", "Active", BADGE_ACTIVE), "2026-03-28"],
]
draw_table(draw, pad + S(5), card_y + S(6), headers, rows, col_widths)

img.save(f"{DOCS}/wireframe-my-feature-list.png")
print("Done")
```
