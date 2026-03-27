#!/usr/bin/env python3
"""Generate user flow PNGs for the homepage navigation PRD.
Style matches the prediction-market flows (flow-create-conviction.png, flow-place-order.png).
"""

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

AH = S(2.5)  # arrowhead half-size (keep proportional to thin lines)

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
    """Return text width using a scratch draw context."""
    bbox = _scratch.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]

_scratch_img = Image.new("RGB", (1, 1))
_scratch = ImageDraw.Draw(_scratch_img)


def node_size(n):
    """Return (width, height) adapted to the node's text content."""
    pad_x = S(16)  # padding each side
    pad_y_top = S(7)
    pad_y_bottom = S(7)
    line_gap = S(6)

    if n["type"] == "decision":
        tw, th = _tw(n["title"], FONT_BODY)
        # diamond text sits inside the diamond; need ~1.7× text width
        w = int(tw * 1.7) + pad_x
        h = max(S(40), int(th * 3.2))
        return w, h

    # Measure title
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
        w = max(w, tw_title + pad_x * 3)  # pills need a bit more x room
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
    """Draw a single node centered at cx, top at y. Returns bottom y."""
    R = S(6)
    pal = n["pal"]

    if n["type"] == "start" or (n["type"] == "success" and "sub" not in n):
        # Pill shape
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
        # Rounded rect
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
    """
    Render a vertical flow with optional one side branch.

    side_branch = {
        "from_idx": int,        # decision node index
        "node": dict,           # the side-branch node
        "label": str,           # branch label (e.g., "No", "WebView")
        "label_color": str,     # color for label and arrow
        "main_label": str,      # label for the main (down) branch
        "main_label_color": str,
        "retry_to_idx": int | None,  # if set, draw loop-back from side node to this main node
    }
    """
    GAP = S(22)

    # Compute sizes
    sizes = [node_size(n) for n in nodes]
    widths  = [s[0] for s in sizes]
    heights = [s[1] for s in sizes]

    # Side branch sizes
    sb_w, sb_h = (0, 0)
    if side_branch:
        sb_w, sb_h = node_size(side_branch["node"])

    max_main_w = max(widths)
    CX = max(max_main_w // 2 + S(30), S(120))  # left margin

    # Total height
    total_h = S(28)  # top (title)
    for h in heights:
        total_h += h + GAP
    total_h += S(40)  # bottom margin

    # Image width: main flow + gap + side branch
    right_extra = max_main_w // 2 + S(30)  # at minimum, fit all main nodes
    if side_branch:
        dec_idx = side_branch["from_idx"]
        dec_w = widths[dec_idx]
        right_extra = max(right_extra, dec_w // 2 + S(24) + sb_w + S(30))
    IMG_W = CX + right_extra
    IMG_H = total_h

    img = Image.new("RGB", (IMG_W, IMG_H), "white")
    draw = ImageDraw.Draw(img)

    # Title
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

        # Arrow from previous
        if i > 0:
            prev_bot = y_bots[i - 1]
            prev_n = nodes[i - 1]
            if prev_n["type"] == "decision" and side_branch and side_branch["from_idx"] == i - 1:
                # Main branch (down) from decision
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

        # Horizontal arrow
        draw.line([(dec_right, dec_cy), (sb_cx - sb_w // 2 - AH * 2, dec_cy)],
                  fill=hex_to_rgb(lbl_col), width=2)
        arrowhead(draw, sb_cx - sb_w // 2, dec_cy, "right", lbl_col)

        # Label
        lbl = side_branch["label"]
        lbl_tw, _ = _tw(lbl, FONT_LABEL)
        draw.text((dec_right + S(4), dec_cy - S(10)), lbl,
                  fill=hex_to_rgb(lbl_col), font=FONT_LABEL)

        # Draw side node
        draw_node(draw, sb_cx, sb_y, side_branch["node"], sb_w, sb_h)

        # Retry loop-back
        if side_branch.get("retry_to_idx") is not None:
            target_idx = side_branch["retry_to_idx"]
            target_cy = y_tops[target_idx] + heights[target_idx] // 2
            target_left = CX - widths[target_idx] // 2

            pipe_x = target_left - S(24)
            y_route_bottom = sb_y + sb_h + S(14)

            err_col = PAL_ERROR["border"]
            # Down from side node
            draw.line([(sb_cx, sb_y + sb_h), (sb_cx, y_route_bottom)],
                      fill=hex_to_rgb(err_col), width=2)
            # Left
            draw.line([(sb_cx, y_route_bottom), (pipe_x, y_route_bottom)],
                      fill=hex_to_rgb(err_col), width=2)
            # Up
            draw.line([(pipe_x, y_route_bottom), (pipe_x, target_cy)],
                      fill=hex_to_rgb(err_col), width=2)
            # Right to target
            draw.line([(pipe_x, target_cy), (target_left - AH * 2, target_cy)],
                      fill=hex_to_rgb(err_col), width=2)
            arrowhead(draw, target_left, target_cy, "right", err_col)

            # "retry" label
            rl_w, _ = _tw("retry", FONT_LABEL)
            draw.text((pipe_x - rl_w - S(3), target_cy - S(6)), "retry",
                      fill=hex_to_rgb(PAL_ERROR["text"]), font=FONT_LABEL)

    img.save(output_path)
    print(f"Saved {output_path}")


# ============================================================
# Flow 1: Menu Navigation to Feature
# ============================================================
def generate_flow_menu_navigation():
    nodes = [
        {"type": "start", "title": "App Homepage", "pal": PAL_START},
        {"type": "step", "title": "Tap hamburger icon (top-left)", "sub": ["• Hamburger menu icon on homepage header"], "pal": PAL_STEP},
        {"type": "system", "title": "Push full-screen navigation page", "sub": ["• Page slides in from right", "• Shows wallet address + settings gear", "• Feature grid organized by category"], "pal": PAL_SYSTEM},
        {"type": "step", "title": "Browse feature categories", "sub": ["• Manage Assets: Deposit, Withdraw", "• Trade: Perpetual, Spot, Shield", "• Earn & Rewards: Earn, Staking, Points, etc.", "• Explore: Explorer, Referral, Leaderboard"], "pal": PAL_STEP},
        {"type": "step", "title": "Tap a feature icon", "sub": ["• User selects desired feature from grid"], "pal": PAL_STEP},
        {"type": "decision", "title": "Route type?", "pal": PAL_DECISION},
        {"type": "success", "title": "Navigate to native screen", "sub": ["• Deep link to in-app screen", "• e.g., Perpetual trading page"], "pal": PAL_SUCCESS},
    ]

    side = {
        "from_idx": 5,
        "node": {"type": "system", "title": "Open WebView", "sub": ["• Load web URL in-app", "• Auth token auto-injected", "• Top bar: back button + title"], "pal": PAL_SYSTEM},
        "label": "WebView",
        "label_color": NO_COLOR,
        "main_label": "Native",
        "main_label_color": YES_COLOR,
        "retry_to_idx": None,
    }

    render_flow(
        "Flow 1 — Menu Navigation to Feature",
        nodes, side,
        "/Users/dannychen/Documents/aster-docs/docs/flow-menu-navigation.png",
    )


# ============================================================
# Flow 2: Customize Shortcuts
# ============================================================
def generate_flow_customize_shortcuts():
    nodes = [
        {"type": "start", "title": "Navigation Page", "pal": PAL_START},
        {"type": "step", "title": "Tap edit button (pencil icon)", "sub": ["• Located in Shortcuts section header"], "pal": PAL_STEP},
        {"type": "system", "title": "Enter edit mode", "sub": ["• Icons show drag handles", "• Delete (×) buttons appear", "• \"Reset to default\" option shown"], "pal": PAL_SYSTEM},
        {"type": "step", "title": "Drag icons to reorder", "sub": ["• Long-press to pick up icon", "• Drag to new position", "• Other icons shift to accommodate"], "pal": PAL_STEP},
        {"type": "step", "title": "Tap \"Done\" to save", "sub": ["• Confirm new arrangement"], "pal": PAL_STEP},
        {"type": "system", "title": "Save to device storage", "sub": ["• Write to AsyncStorage / MMKV", "• Persists across app restarts"], "pal": PAL_SYSTEM},
        {"type": "success", "title": "Exit edit mode", "sub": ["• New order applied immediately", "• Toast: \"Shortcuts updated\""], "pal": PAL_SUCCESS},
    ]

    side = None

    render_flow(
        "Flow 2 — Customize Shortcuts",
        nodes, side,
        "/Users/dannychen/Documents/aster-docs/docs/flow-customize-shortcuts.png",
    )


# ============================================================
# Flow 3: Settings Access
# ============================================================
def generate_flow_settings_access():
    nodes = [
        {"type": "start", "title": "App Homepage", "pal": PAL_START},
        {"type": "step", "title": "Tap hamburger icon", "sub": ["• Top-left of homepage header"], "pal": PAL_STEP},
        {"type": "system", "title": "Push navigation page", "sub": ["• Full-screen feature navigation", "• Settings gear icon at top-right"], "pal": PAL_SYSTEM},
        {"type": "step", "title": "Tap settings gear icon", "sub": ["• Located in navigation page header"], "pal": PAL_STEP},
        {"type": "system", "title": "Push settings sub-page", "sub": ["• Relocated from old hamburger menu"], "pal": PAL_SYSTEM},
        {"type": "step", "title": "Browse settings items", "sub": ["• Security", "• Language", "• Help", "• Privacy Policy", "• Terms & Conditions", "• About"], "pal": PAL_STEP},
        {"type": "step", "title": "Tap a setting item", "sub": ["• Navigate to detail screen"], "pal": PAL_STEP},
        {"type": "success", "title": "Setting detail page", "pal": PAL_SUCCESS},
    ]

    render_flow(
        "Flow 3 — Settings Access",
        nodes, None,
        "/Users/dannychen/Documents/aster-docs/docs/flow-settings-access.png",
    )


if __name__ == "__main__":
    generate_flow_menu_navigation()
    generate_flow_customize_shortcuts()
    generate_flow_settings_access()
