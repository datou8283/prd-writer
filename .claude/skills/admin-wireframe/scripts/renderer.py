"""
Admin Wireframe Renderer
Bundled Pillow rendering engine for Aster admin dashboard wireframes.

Usage:
    import sys
    sys.path.insert(0, "/Users/dannychen/Documents/aster-docs/.claude/skills/admin-wireframe/scripts")
    from renderer import *
"""

from PIL import Image, ImageDraw, ImageFont

# ─────────────────────────────────────────────
# Scale & sizing
# ─────────────────────────────────────────────
SCALE = 3
W_DEFAULT = 400  # logical px — multiply by SCALE for actual pixels


def S(x):
    """Convert logical pixels to hi-dpi pixels."""
    return int(round(x * SCALE))


# ─────────────────────────────────────────────
# Color palette
# ─────────────────────────────────────────────
BG_COLOR       = "#F5F5F7"
CARD_BG        = "#FFFFFF"
CARD_BORDER    = "#E0E0E4"
TEXT_PRIMARY   = "#1A1A2E"
TEXT_SECONDARY = "#6B6B80"
TEXT_MUTED     = "#9B9BAE"
DIVIDER        = "#ECECF0"

# Status badge palettes  (bg, text, border)
BADGE_ACTIVE = {"bg": "#E6F9EE", "text": "#1B5E35", "border": "#6CC08B"}
BADGE_PAUSED = {"bg": "#FEF3CD", "text": "#7A5200", "border": "#F0B429"}
BADGE_ENDED  = {"bg": "#FFE8E8", "text": "#8B1A1A", "border": "#E07070"}
BADGE_DRAFT  = {"bg": "#F0F0F4", "text": "#6B6B80", "border": "#C4C4CC"}

# Button palettes  (bg, text, optional border)
BTN_PRIMARY = {"bg": "#5C3D9E", "text": "#FFFFFF"}
BTN_WARNING = {"bg": "#F0B429", "text": "#7A5200"}
BTN_DANGER  = {"bg": "#E07070", "text": "#FFFFFF"}
BTN_OUTLINE = {"bg": "#FFFFFF", "text": "#5C3D9E", "border": "#5C3D9E"}
BTN_SUBTLE  = {"bg": "#F4F4F6", "text": "#333344", "border": "#C4C4CC"}

# Progress bar
PROGRESS_BG   = "#ECECF0"
PROGRESS_FILL = "#5C3D9E"

# Tab colors
TAB_ACTIVE_BG     = "#5C3D9E"
TAB_ACTIVE_TEXT   = "#FFFFFF"
TAB_INACTIVE_BG   = "#F0F0F4"
TAB_INACTIVE_TEXT = "#6B6B80"

# Chip colors
CHIP_SELECTED_BG     = "#EDE9FF"
CHIP_SELECTED_TEXT   = "#5C3D9E"
CHIP_SELECTED_BORDER = "#9B8EC4"
CHIP_UNSELECTED_BG     = "#F4F4F6"
CHIP_UNSELECTED_TEXT   = "#6B6B80"
CHIP_UNSELECTED_BORDER = "#C4C4CC"


# ─────────────────────────────────────────────
# Fonts  (Helvetica, macOS system path)
# ─────────────────────────────────────────────
_FONT_PATH = "/System/Library/Fonts/Helvetica.ttc"

try:
    FONT_PAGE_TITLE = ImageFont.truetype(_FONT_PATH, S(8))
    FONT_SECTION    = ImageFont.truetype(_FONT_PATH, S(5.5))
    FONT_TABLE_HEAD = ImageFont.truetype(_FONT_PATH, S(4))
    FONT_TABLE_BODY = ImageFont.truetype(_FONT_PATH, S(4))
    FONT_LABEL      = ImageFont.truetype(_FONT_PATH, S(3.8))
    FONT_BADGE      = ImageFont.truetype(_FONT_PATH, S(3.5))
    FONT_SMALL      = ImageFont.truetype(_FONT_PATH, S(3.2))
    FONT_STAT_NUM   = ImageFont.truetype(_FONT_PATH, S(7))
    FONT_STAT_LABEL = ImageFont.truetype(_FONT_PATH, S(3.8))
    FONT_BUTTON     = ImageFont.truetype(_FONT_PATH, S(4))
    FONT_BREADCRUMB = ImageFont.truetype(_FONT_PATH, S(4))
    FONT_INPUT      = ImageFont.truetype(_FONT_PATH, S(4))
except Exception:
    # Fallback for non-macOS environments
    _default = ImageFont.load_default()
    FONT_PAGE_TITLE = FONT_SECTION = FONT_TABLE_HEAD = FONT_TABLE_BODY = _default
    FONT_LABEL = FONT_BADGE = FONT_SMALL = FONT_STAT_NUM = FONT_STAT_LABEL = _default
    FONT_BUTTON = FONT_BREADCRUMB = FONT_INPUT = _default


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
_scratch_img = Image.new("RGB", (1, 1))
_scratch = ImageDraw.Draw(_scratch_img)


def hex_to_rgb(h):
    """'#RRGGBB' → (R, G, B)."""
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def _tw(text, font):
    """Measure (width, height) of text string."""
    bbox = _scratch.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


# ─────────────────────────────────────────────
# UI Components
# ─────────────────────────────────────────────

def draw_card(draw, x, y, w, h, radius=None):
    """White rounded card with subtle border."""
    if radius is None:
        radius = S(4)
    draw.rounded_rectangle(
        [x, y, x + w, y + h],
        radius=radius,
        fill=hex_to_rgb(CARD_BG),
        outline=hex_to_rgb(CARD_BORDER),
        width=2,
    )


def draw_badge(draw, x, y, text, badge_style):
    """Status badge pill.  Returns (width, height)."""
    tw, th = _tw(text, FONT_BADGE)
    pad_x, pad_y = S(5), S(2)
    w = tw + pad_x * 2
    h = th + pad_y * 2
    r = h // 2
    draw.rounded_rectangle(
        [x, y, x + w, y + h],
        radius=r,
        fill=hex_to_rgb(badge_style["bg"]),
        outline=hex_to_rgb(badge_style["border"]),
        width=1,
    )
    draw.text((x + pad_x, y + pad_y), text, fill=hex_to_rgb(badge_style["text"]), font=FONT_BADGE)
    return w, h


def draw_button(draw, x, y, text, btn_style, font=None):
    """Rounded button.  Returns (width, height)."""
    if font is None:
        font = FONT_BUTTON
    tw, th = _tw(text, font)
    pad_x, pad_y = S(8), S(3.5)
    w = tw + pad_x * 2
    h = th + pad_y * 2
    r = S(3)
    outline_color = btn_style.get("border", btn_style["bg"])
    draw.rounded_rectangle(
        [x, y, x + w, y + h],
        radius=r,
        fill=hex_to_rgb(btn_style["bg"]),
        outline=hex_to_rgb(outline_color),
        width=2,
    )
    draw.text((x + pad_x, y + pad_y), text, fill=hex_to_rgb(btn_style["text"]), font=font)
    return w, h


def draw_progress_bar(draw, x, y, w, pct, h=None):
    """Horizontal progress bar (pct = 0.0–1.0).  Returns bar height."""
    if h is None:
        h = S(4)
    r = h // 2
    draw.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=hex_to_rgb(PROGRESS_BG))
    fill_w = max(int(w * pct), h)
    if pct > 0:
        draw.rounded_rectangle([x, y, x + fill_w, y + h], radius=r, fill=hex_to_rgb(PROGRESS_FILL))
    return h


def draw_tabs(draw, x, y, tabs, active_idx=0):
    """Horizontal filter tabs.  Returns tab height."""
    cur_x = x
    tab_h = S(0)
    for i, tab_text in enumerate(tabs):
        tw, th = _tw(tab_text, FONT_LABEL)
        pad_x, pad_y = S(6), S(3)
        w = tw + pad_x * 2
        h = th + pad_y * 2
        tab_h = h
        r = S(3)
        is_active = (i == active_idx)
        bg = TAB_ACTIVE_BG if is_active else TAB_INACTIVE_BG
        fg = TAB_ACTIVE_TEXT if is_active else TAB_INACTIVE_TEXT
        draw.rounded_rectangle([cur_x, y, cur_x + w, y + h], radius=r, fill=hex_to_rgb(bg))
        draw.text((cur_x + pad_x, y + pad_y), tab_text, fill=hex_to_rgb(fg), font=FONT_LABEL)
        cur_x += w + S(3)
    return tab_h


def draw_pagination(draw, x, y):
    """Simple pagination: < 1 2 3 ... 10 >"""
    pages = ["<", "1", "2", "3", "...", "10", ">"]
    cur_x = x
    for p in pages:
        tw, th = _tw(p, FONT_LABEL)
        sz = max(th + S(4), tw + S(6))
        is_active = (p == "1")
        r = S(2)
        bg = TAB_ACTIVE_BG if is_active else TAB_INACTIVE_BG
        fg = TAB_ACTIVE_TEXT if is_active else TAB_INACTIVE_TEXT
        draw.rounded_rectangle([cur_x, y, cur_x + sz, y + sz], radius=r, fill=hex_to_rgb(bg))
        draw.text(
            (cur_x + (sz - tw) // 2, y + (sz - th) // 2),
            p, fill=hex_to_rgb(fg), font=FONT_LABEL,
        )
        cur_x += sz + S(2)


def draw_input_field(draw, x, y, w, label, placeholder="", suffix=""):
    """Labelled form input field.  Returns total height (label + field)."""
    draw.text((x, y), label, fill=hex_to_rgb(TEXT_PRIMARY), font=FONT_LABEL)
    lw, lh = _tw(label, FONT_LABEL)
    field_y = y + lh + S(3)
    field_h = S(14)
    r = S(3)
    draw.rounded_rectangle(
        [x, field_y, x + w, field_y + field_h],
        radius=r,
        fill=hex_to_rgb("#FFFFFF"),
        outline=hex_to_rgb(CARD_BORDER),
        width=2,
    )
    text_y = field_y + (field_h - _tw(placeholder or "M", FONT_INPUT)[1]) // 2
    if placeholder:
        draw.text((x + S(4), text_y), placeholder, fill=hex_to_rgb(TEXT_MUTED), font=FONT_INPUT)
    if suffix:
        sw, _ = _tw(suffix, FONT_SMALL)
        draw.text((x + w - sw - S(4), text_y + S(1)), suffix, fill=hex_to_rgb(TEXT_SECONDARY), font=FONT_SMALL)
    return lh + S(3) + field_h


def draw_chip(draw, x, y, text, selected=False):
    """Multi-select chip.  Returns (width, height)."""
    tw, th = _tw(text, FONT_LABEL)
    pad_x, pad_y = S(5), S(2.5)
    w = tw + pad_x * 2
    h = th + pad_y * 2
    r = S(3)
    if selected:
        draw.rounded_rectangle(
            [x, y, x + w, y + h], radius=r,
            fill=hex_to_rgb(CHIP_SELECTED_BG),
            outline=hex_to_rgb(CHIP_SELECTED_BORDER), width=2,
        )
        draw.text((x + pad_x, y + pad_y), text, fill=hex_to_rgb(CHIP_SELECTED_TEXT), font=FONT_LABEL)
    else:
        draw.rounded_rectangle(
            [x, y, x + w, y + h], radius=r,
            fill=hex_to_rgb(CHIP_UNSELECTED_BG),
            outline=hex_to_rgb(CHIP_UNSELECTED_BORDER), width=1,
        )
        draw.text((x + pad_x, y + pad_y), text, fill=hex_to_rgb(CHIP_UNSELECTED_TEXT), font=FONT_LABEL)
    return w, h


def draw_qr_placeholder(draw, x, y, size):
    """Deterministic fake QR code with corner finder patterns."""
    import random
    draw.rectangle([x, y, x + size, y + size], fill=hex_to_rgb("#FFFFFF"), outline=hex_to_rgb("#333344"), width=2)
    finder_size = size // 5
    corners = [
        (x + S(2), y + S(2)),
        (x + size - finder_size - S(2), y + S(2)),
        (x + S(2), y + size - finder_size - S(2)),
    ]
    for fx, fy in corners:
        draw.rectangle([fx, fy, fx + finder_size, fy + finder_size], fill=hex_to_rgb("#333344"))
        inner = S(2)
        draw.rectangle([fx + inner, fy + inner, fx + finder_size - inner, fy + finder_size - inner], fill=hex_to_rgb("#FFFFFF"))
        inner2 = S(4)
        draw.rectangle([fx + inner2, fy + inner2, fx + finder_size - inner2, fy + finder_size - inner2], fill=hex_to_rgb("#333344"))
    dot_size = size // 20
    rng = random.Random(42)
    for _ in range(60):
        dx = rng.randint(x + finder_size + S(4), x + size - S(6))
        dy = rng.randint(y + finder_size + S(4), y + size - S(6))
        draw.rectangle([dx, dy, dx + dot_size, dy + dot_size], fill=hex_to_rgb("#333344"))


def draw_table(draw, x, y, headers, rows, col_widths, row_height=None):
    """Data table with headers and rows.

    Cell values can be:
      - str                          → plain text
      - ("badge", text, badge_style) → status badge
      - ("progress", pct, label)     → progress bar + text label

    Returns bottom_y (use this to stack elements below the table).
    """
    if row_height is None:
        row_height = S(16)
    header_height = S(14)
    total_w = sum(col_widths)

    # Header row
    draw.rounded_rectangle([x, y, x + total_w, y + header_height], radius=S(2), fill=hex_to_rgb("#F8F8FA"))
    cx = x
    for i, h in enumerate(headers):
        tw, th = _tw(h, FONT_TABLE_HEAD)
        draw.text((cx + S(5), y + (header_height - th) // 2), h, fill=hex_to_rgb(TEXT_SECONDARY), font=FONT_TABLE_HEAD)
        cx += col_widths[i]

    cur_y = y + header_height

    for ri, row in enumerate(rows):
        # Alternating stripe
        if ri % 2 == 1:
            draw.rectangle([x, cur_y, x + total_w, cur_y + row_height], fill=hex_to_rgb("#FBFBFD"))
        # Row divider
        draw.line([(x, cur_y), (x + total_w, cur_y)], fill=hex_to_rgb(DIVIDER), width=1)

        cx = x
        for ci, cell in enumerate(row):
            mid_y = cur_y + row_height // 2

            if isinstance(cell, tuple) and cell[0] == "badge":
                _, text, style = cell
                draw_badge(draw, cx + S(5), mid_y - S(5), text, style)

            elif isinstance(cell, tuple) and cell[0] == "progress":
                _, pct, label = cell
                bar_w = col_widths[ci] - S(14)
                draw_progress_bar(draw, cx + S(5), mid_y - S(5), bar_w, pct)
                draw.text((cx + S(5), mid_y + S(1)), label, fill=hex_to_rgb(TEXT_SECONDARY), font=FONT_SMALL)

            else:
                tw, th = _tw(str(cell), FONT_TABLE_BODY)
                draw.text((cx + S(5), mid_y - th // 2), str(cell), fill=hex_to_rgb(TEXT_PRIMARY), font=FONT_TABLE_BODY)

            cx += col_widths[ci]

        cur_y += row_height

    # Bottom border
    draw.line([(x, cur_y), (x + total_w, cur_y)], fill=hex_to_rgb(DIVIDER), width=1)
    return cur_y


def make_modal_overlay(img):
    """Apply semi-transparent dark overlay for modal dialogs.

    Call this after drawing the background page, then draw the modal on top.
    Returns (new_img, new_draw) ready to use.
    """
    W, H = img.size
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.rectangle([0, 0, W, H], fill=(30, 30, 50, 160))
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")
    draw = ImageDraw.Draw(img)
    return img, draw
