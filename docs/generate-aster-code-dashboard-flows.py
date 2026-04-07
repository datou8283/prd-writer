#!/usr/bin/env python3
"""Generate user flow PNGs for the Aster Code Dashboard PRD."""

from PIL import Image, ImageDraw, ImageFont

SCALE = 3

def S(x):
    return int(round(x * SCALE))

# --- Palette (Whimsical-style pastels) ---
PAL_START    = {"fill": "#EDE9FF", "border": "#9B8EC4", "text": "#5C3D9E"}
PAL_STEP     = {"fill": "#F4F4F6", "border": "#C4C4CC", "text": "#333344"}
PAL_SYSTEM   = {"fill": "#EAF4FF", "border": "#7AB0DC", "text": "#1A5C8A"}
PAL_DECISION = {"fill": "#FEF3CD", "border": "#F0B429", "text": "#7A5200"}
PAL_SUCCESS  = {"fill": "#E6F9EE", "border": "#6CC08B", "text": "#1B5E35"}
PAL_ERROR    = {"fill": "#FFE8E8", "border": "#E07070", "text": "#8B1A1A"}

ARROW_COLOR = "#AAAAAA"
YES_COLOR   = "#2E7D32"
NO_COLOR    = "#C62828"

AH = S(2.5)

# Fonts
try:
    FONT_TITLE = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", S(6))
    FONT_BODY  = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", S(5))
    FONT_SMALL = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", S(3.5))
    FONT_LABEL = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", S(3.5))
except Exception:
    FONT_TITLE = ImageFont.load_default()
    FONT_BODY  = ImageFont.load_default()
    FONT_SMALL = ImageFont.load_default()
    FONT_LABEL = ImageFont.load_default()

# ---------- helpers ----------

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _tw(text, font):
    bbox = _scratch.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

_scratch_img = Image.new("RGB", (1, 1))
_scratch = ImageDraw.Draw(_scratch_img)


def node_size(n):
    pad_x = S(16)
    pad_y_top = S(7)
    pad_y_bottom = S(7)
    line_gap = S(6)

    if n["type"] == "decision":
        tw, th = _tw(n["title"], FONT_BODY)
        w = int(tw * 1.7) + pad_x
        h = max(S(40), int(th * 3.2))
        return w, h

    tw_title, th_title = _tw(n["title"], FONT_BODY)
    max_w = tw_title

    sub_h = 0
    if "sub" in n:
        for s in n["sub"]:
            tw_s, th_s = _tw(s, FONT_SMALL)
            max_w = max(max_w, tw_s)
            sub_h += th_s + line_gap

    w = max_w + pad_x * 2
    h = pad_y_top + th_title + S(4) + sub_h + pad_y_bottom

    if n["type"] == "start" or (n["type"] == "success" and "sub" not in n):
        h = max(h, S(22))
        w = max(w, tw_title + pad_x * 3)
    else:
        h = max(h, S(28))

    return w, h


def arrowhead(draw, x, y, direction, color):
    c = hex_to_rgb(color)
    if direction == "down":
        pts = [(x, y), (x - AH, y - AH * 2), (x + AH, y - AH * 2)]
    elif direction == "right":
        pts = [(x, y), (x - AH * 2, y - AH), (x - AH * 2, y + AH)]
    elif direction == "left":
        pts = [(x, y), (x + AH * 2, y - AH), (x + AH * 2, y + AH)]
    elif direction == "up":
        pts = [(x, y), (x - AH, y + AH * 2), (x + AH, y + AH * 2)]
    draw.polygon(pts, fill=c)

def arrow_down(draw, x, y1, y2, color=ARROW_COLOR):
    draw.line([(x, y1), (x, y2 - AH * 2)], fill=hex_to_rgb(color), width=2)
    arrowhead(draw, x, y2, "down", color)


def draw_node(draw, cx, y, n, w, h):
    R = S(6)
    pal = n["pal"]

    if n["type"] == "start" or (n["type"] == "success" and "sub" not in n):
        r = h // 2
        draw.rounded_rectangle([cx - w // 2, y, cx + w // 2, y + h], radius=r,
                               fill=hex_to_rgb(pal["fill"]), outline=hex_to_rgb(pal["border"]), width=2)
        tw, th = _tw(n["title"], FONT_BODY)
        draw.text((cx - tw // 2, y + h // 2 - th // 2), n["title"],
                  fill=hex_to_rgb(pal["text"]), font=FONT_BODY)

    elif n["type"] == "decision":
        cy = y + h // 2
        draw.polygon(
            [(cx, y), (cx + w // 2, cy), (cx, y + h), (cx - w // 2, cy)],
            fill=hex_to_rgb(pal["fill"]), outline=hex_to_rgb(pal["border"]), width=S(1),
        )
        tw, th = _tw(n["title"], FONT_BODY)
        draw.text((cx - tw // 2, cy - th // 2), n["title"],
                  fill=hex_to_rgb(pal["text"]), font=FONT_BODY)

    else:
        draw.rounded_rectangle([cx - w // 2, y, cx + w // 2, y + h], radius=R,
                               fill=hex_to_rgb(pal["fill"]), outline=hex_to_rgb(pal["border"]), width=2)
        ty = y + S(7)
        tw, th = _tw(n["title"], FONT_BODY)
        draw.text((cx - tw // 2, ty), n["title"],
                  fill=hex_to_rgb(pal["text"]), font=FONT_BODY)
        ty += th + S(4)
        if "sub" in n:
            for s in n["sub"]:
                tw_s, th_s = _tw(s, FONT_SMALL)
                draw.text((cx - tw_s // 2, ty), s,
                          fill=hex_to_rgb(pal["text"]), font=FONT_SMALL)
                ty += th_s + S(6)

    return y + h


# ---------- generic flow renderer ----------

def render_flow(title, nodes, side_branch=None, output_path=""):
    GAP = S(22)

    sizes = [node_size(n) for n in nodes]
    widths  = [s[0] for s in sizes]
    heights = [s[1] for s in sizes]

    sb_w, sb_h = (0, 0)
    if side_branch:
        sb_w, sb_h = node_size(side_branch["node"])

    max_main_w = max(widths)
    CX = max(max_main_w // 2 + S(30), S(120))

    total_h = S(28)
    for h in heights:
        total_h += h + GAP
    total_h += S(40)

    right_extra = max_main_w // 2 + S(30)
    if side_branch:
        dec_idx = side_branch["from_idx"]
        dec_w = widths[dec_idx]
        right_extra = max(right_extra, dec_w // 2 + S(24) + sb_w + S(30))
    IMG_W = CX + right_extra
    IMG_H = total_h

    img = Image.new("RGB", (IMG_W, IMG_H), "white")
    draw = ImageDraw.Draw(img)

    tw, _ = _tw(title, FONT_TITLE)
    draw.text((IMG_W // 2 - tw // 2, S(6)), title,
              fill=hex_to_rgb("#333344"), font=FONT_TITLE)

    y = S(28)
    y_tops = []
    y_bots = []

    for i, n in enumerate(nodes):
        w, h = widths[i], heights[i]
        y_tops.append(y)
        bot = draw_node(draw, CX, y, n, w, h)
        y_bots.append(bot)

        if i > 0:
            prev_bot = y_bots[i - 1]
            prev_n = nodes[i - 1]
            if prev_n["type"] == "decision" and side_branch and side_branch["from_idx"] == i - 1:
                col = side_branch["main_label_color"]
                draw.line([(CX, prev_bot), (CX, y - AH * 2)],
                          fill=hex_to_rgb(col), width=2)
                arrowhead(draw, CX, y, "down", col)
                lbl = side_branch["main_label"]
                lbl_w, lbl_h = _tw(lbl, FONT_LABEL)
                lbl_y = prev_bot + (y - prev_bot) // 2 - lbl_h // 2
                draw.text((CX + S(6), lbl_y), lbl,
                          fill=hex_to_rgb(col), font=FONT_LABEL)
            else:
                arrow_down(draw, CX, prev_bot, y)

        y = bot + GAP

    # --- Side branch ---
    if side_branch:
        dec_idx = side_branch["from_idx"]
        dec_cy = y_tops[dec_idx] + heights[dec_idx] // 2
        dec_right = CX + widths[dec_idx] // 2

        sb_cx = dec_right + S(24) + sb_w // 2
        sb_y = dec_cy - sb_h // 2

        lbl_col = side_branch["label_color"]

        draw.line([(dec_right, dec_cy), (sb_cx - sb_w // 2 - AH * 2, dec_cy)],
                  fill=hex_to_rgb(lbl_col), width=2)
        arrowhead(draw, sb_cx - sb_w // 2, dec_cy, "right", lbl_col)

        lbl = side_branch["label"]
        lbl_tw, _ = _tw(lbl, FONT_LABEL)
        draw.text((dec_right + S(4), dec_cy - S(10)), lbl,
                  fill=hex_to_rgb(lbl_col), font=FONT_LABEL)

        draw_node(draw, sb_cx, sb_y, side_branch["node"], sb_w, sb_h)

        if side_branch.get("retry_to_idx") is not None:
            target_idx = side_branch["retry_to_idx"]
            target_cy = y_tops[target_idx] + heights[target_idx] // 2
            target_left = CX - widths[target_idx] // 2

            pipe_x = target_left - S(24)
            y_route_bottom = sb_y + sb_h + S(14)

            err_col = PAL_ERROR["border"]
            draw.line([(sb_cx, sb_y + sb_h), (sb_cx, y_route_bottom)],
                      fill=hex_to_rgb(err_col), width=2)
            draw.line([(sb_cx, y_route_bottom), (pipe_x, y_route_bottom)],
                      fill=hex_to_rgb(err_col), width=2)
            draw.line([(pipe_x, y_route_bottom), (pipe_x, target_cy)],
                      fill=hex_to_rgb(err_col), width=2)
            draw.line([(pipe_x, target_cy), (target_left - AH * 2, target_cy)],
                      fill=hex_to_rgb(err_col), width=2)
            arrowhead(draw, target_left, target_cy, "right", err_col)

            rl_w, _ = _tw("retry", FONT_LABEL)
            draw.text((pipe_x - rl_w - S(3), target_cy - S(6)), "retry",
                      fill=hex_to_rgb(PAL_ERROR["text"]), font=FONT_LABEL)

    img.save(output_path)
    print(f"Saved {output_path}")


# ============================================================
# Flow 1: Browse Aster Code Dashboard
# ============================================================
def generate_flow_dashboard_view():
    nodes = [
        {"type": "start", "title": "Aster Code Dashboard URL", "pal": PAL_START},
        {"type": "system", "title": "Show loading skeleton", "sub": [
            "* KPI cards: shimmer placeholders",
            "* Charts: gray skeleton boxes",
            "* Table: row placeholders",
        ], "pal": PAL_SYSTEM},
        {"type": "system", "title": "Fetch dashboard data", "sub": [
            "* GET /api/v1/aster-code/overview (KPIs)",
            "* GET /api/v1/aster-code/series (default charts)",
            "* GET /api/v1/aster-code/stats (table page 1)",
        ], "pal": PAL_SYSTEM},
        {"type": "decision", "title": "Data available?", "pal": PAL_DECISION},
        {"type": "step", "title": "View KPI summary cards", "sub": [
            "* Total Aster Code Fees",
            "* Total Aster Code Volume",
            "* Total Aster Code Users",
        ], "pal": PAL_STEP},
        {"type": "step", "title": "Browse time-series & analysis charts", "sub": [
            "* Volume, fees, users by code",
            "* Proportion charts, pie chart, rankings",
        ], "pal": PAL_STEP},
        {"type": "step", "title": "Scroll to Aster Code Stats table", "sub": [
            "* Sortable columns: Code, Volume, Fees, Trades, Users",
            "* Paginated (10 per page)",
        ], "pal": PAL_STEP},
        {"type": "decision", "title": "Copy address?", "pal": PAL_DECISION},
        {"type": "success", "title": "Address copied to clipboard", "pal": PAL_SUCCESS},
    ]

    side = {
        "from_idx": 3,
        "node": {"type": "error", "title": "Show empty state", "sub": [
            "* 'No data yet. Check back after",
            "  the first data sync.'",
            "* KPI cards show $0 / 0",
        ], "pal": PAL_ERROR},
        "label": "No data",
        "label_color": NO_COLOR,
        "main_label": "Yes",
        "main_label_color": YES_COLOR,
        "retry_to_idx": None,
    }

    render_flow(
        "Flow 1 — Browse Aster Code Dashboard",
        nodes, side,
        "/Users/dannychen/Documents/aster-docs/docs/flow-aster-code-dashboard-view.png",
    )


# ============================================================
# Flow 2: Filter & Interact with Charts
# ============================================================
def generate_flow_dashboard_filter():
    nodes = [
        {"type": "start", "title": "Aster Code Dashboard", "pal": PAL_START},
        {"type": "step", "title": "Select time range", "sub": [
            "* Options: W (week), M (month), Q (quarter)",
            "* Default: M (monthly)",
        ], "pal": PAL_STEP},
        {"type": "system", "title": "Fetch data for selected range", "sub": [
            "* API call with interval parameter",
            "* Loading skeleton shown during fetch",
        ], "pal": PAL_SYSTEM},
        {"type": "decision", "title": "API success?", "pal": PAL_DECISION},
        {"type": "system", "title": "Render updated charts", "sub": [
            "* Re-render all time-series charts",
            "* Animate data transition",
        ], "pal": PAL_SYSTEM},
        {"type": "step", "title": "Toggle chart type", "sub": [
            "* Line / Bar / Area chart options",
            "* Charts re-render in place",
        ], "pal": PAL_STEP},
        {"type": "step", "title": "Toggle pie chart dimension", "sub": [
            "* Switch between: Fees, Volume, Trades, Users",
            "* Pie chart updates instantly",
        ], "pal": PAL_STEP},
        {"type": "step", "title": "Toggle code legend filters", "sub": [
            "* Click code name to show/hide in chart",
            "* 'Deselect all' to clear all codes",
        ], "pal": PAL_STEP},
        {"type": "success", "title": "Dashboard reflects user selections", "pal": PAL_SUCCESS},
    ]

    side = {
        "from_idx": 3,
        "node": {"type": "error", "title": "Show error state", "sub": [
            "* Display inline error message",
            "* Show retry button",
        ], "pal": PAL_ERROR},
        "label": "No",
        "label_color": NO_COLOR,
        "main_label": "Yes",
        "main_label_color": YES_COLOR,
        "retry_to_idx": 2,
    }

    render_flow(
        "Flow 2 — Filter & Interact with Charts",
        nodes, side,
        "/Users/dannychen/Documents/aster-docs/docs/flow-aster-code-dashboard-filter.png",
    )


if __name__ == "__main__":
    generate_flow_dashboard_view()
    generate_flow_dashboard_filter()
