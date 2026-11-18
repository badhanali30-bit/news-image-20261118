#!/usr/bin/env python3
"""Draw the news-image-20261118 entry: a newspaper front page summing up
Wednesday 18 November 2026. All eight stories are real events verified
from live news reporting that day. Deterministic: fixed content, no
timestamps, no randomness — running it twice yields byte-identical
entry.png.

Usage: python3 draw.py   (writes entry.png next to this script)
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# --- palette ----------------------------------------------------------------
PAPER = (250, 246, 236)      # newsprint cream
INK = (22, 22, 22)
RED = (176, 32, 32)
NAVY = (24, 42, 76)
BLUE = (52, 110, 176)
SKY = (208, 226, 242)
GREY = (105, 105, 98)
RULE = (22, 22, 22)
CARD = (255, 255, 255)
CREAM = (240, 234, 219)
GOLD = (214, 138, 32)
GREEN = (46, 125, 50)

FONT_DIR = "/usr/share/fonts/truetype"
SERIF_B = f"{FONT_DIR}/noto/NotoSerif-Bold.ttf"
SANS_B = f"{FONT_DIR}/noto/NotoSans-Bold.ttf"
SANS_R = f"{FONT_DIR}/noto/NotoSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_width):
    """Greedy word wrap; returns lines that fit max_width."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, fnt, fill, leading):
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(d, x0, x1, y, width=2, fill=RULE):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# --- pictograms (flat vector style, drawn with PIL) -------------------------

def icon_summit(d, x, y, s):
    """Three flags on poles above a round table: the trilateral summit."""
    w, h = s, int(s * 0.66)
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # three flag poles with flags (red, gold, green)
    for i, col in enumerate((RED, GOLD, GREEN)):
        px = x + 28 + i * (w // 3)
        d.line([(px, y + 14), (px, y + h - 52)], fill=INK, width=3)
        d.polygon([(px, y + 14), (px + 62, y + 26), (px, y + 38)], fill=col)
    # round table
    d.ellipse([x + w // 2 - 78, y + h - 48, x + w // 2 + 78, y + h - 16],
              fill=NAVY)


def icon_drone(d, x, y, s):
    """A quadcopter drone above a target crosshair."""
    # sky
    d.rectangle([x, y, x + s, y + s], fill=SKY)
    # drone body, centred and larger
    cx, cy = x + s // 2, y + 20
    d.ellipse([cx - 13, cy - 8, cx + 13, cy + 8], fill=INK)
    # arms and rotors
    for dx in (-24, 24):
        d.line([(cx, cy), (cx + dx, cy - 8)], fill=INK, width=3)
        d.ellipse([cx + dx - 10, cy - 14, cx + dx + 10, cy - 10],
                  fill=GREY)
    # camera dot under the body
    d.ellipse([cx - 4, cy + 8, cx + 4, cy + 14], fill=RED)
    # target crosshair below
    tx, ty = x + s // 2, y + s - 14
    d.ellipse([tx - 9, ty - 9, tx + 9, ty + 9], outline=RED, width=3)
    d.line([(tx - 13, ty), (tx - 5, ty)], fill=RED, width=2)
    d.line([(tx + 5, ty), (tx + 13, ty)], fill=RED, width=2)
    d.line([(tx, ty - 13), (tx, ty - 5)], fill=RED, width=2)
    d.line([(tx, ty + 5), (tx, ty + 13)], fill=RED, width=2)


def icon_city(d, x, y, s):
    """City skyline with a red starburst: the Gaza operation."""
    d.rectangle([x, y, x + s, y + s], fill=SKY)
    base = y + s - 8
    # buildings, all inside the s-wide box
    for bx, bw, bh in ((2, 12, 24), (16, 10, 36), (28, 13, 20), (43, 11, 30)):
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=NAVY)
    # starburst over the middle building, kept small and clear of text
    cx, cy = x + s // 2, y + 12
    for dx, dy in ((-9, -8), (0, -11), (9, -8), (-11, 1), (11, 1),
                   (-8, 9), (8, 9)):
        d.line([(cx, cy), (cx + dx, cy + dy)], fill=RED, width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)


def icon_cyclone(d, x, y, s):
    """Spiral storm over waves."""
    d.rectangle([x, y, x + s, y + s], fill=SKY)
    cx, cy = x + s // 2, y + s // 2 - 4
    # spiral arms, kept inside the box
    for r1, a0, a1 in ((10, 0, 200), (17, 40, 260), (24, 80, 300)):
        d.arc([cx - r1, cy - r1, cx + r1, cy + r1], a0, a1, fill=NAVY,
              width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    # waves
    for wy in (y + s - 14, y + s - 6):
        d.line([(x + 6, wy), (x + s - 6, wy)], fill=BLUE, width=3)


def icon_plane(d, x, y, s):
    """Jet flying level with a red downward arrow: the crash."""
    d.rectangle([x, y, x + s, y + s], fill=SKY)
    # jet silhouette, nose to the right, level flight
    cx, cy = x + s // 2, y + 20
    d.polygon([(x + 6, cy), (x + s - 10, cy - 7), (x + s - 4, cy),
               (x + s - 10, cy + 7), (x + 20, cy + 6)], fill=NAVY)
    # tail fin and wing
    d.polygon([(x + 12, cy), (x + 20, cy - 12), (x + 26, cy - 2)],
              fill=NAVY)
    d.polygon([(x + 24, cy + 2), (x + 36, cy + 14), (x + 28, cy + 4)],
              fill=NAVY)
    # red downward arrow below the jet
    ax = x + s // 2
    d.line([(ax, y + 34), (ax, y + s - 8)], fill=RED, width=4)
    d.polygon([(ax - 7, y + s - 14), (ax + 7, y + s - 14), (ax, y + s - 4)],
              fill=RED)


def icon_trade(d, x, y, s):
    """Two flags with a double-headed trade arrow between them."""
    d.rectangle([x, y, x + s, y + s], fill=SKY)
    # left flag (saffron) and right flag (blue)
    for fx, col in ((x + 6, GOLD), (x + s - 28, BLUE)):
        d.line([(fx + 6, y + 6), (fx + 6, y + 28)], fill=INK, width=2)
        d.rectangle([fx + 6, y + 6, fx + 22, y + 18], fill=col)
    # double arrow across the middle
    ay = y + s // 2 + 2
    d.line([(x + 8, ay), (x + s - 8, ay)], fill=NAVY, width=4)
    d.polygon([(x + s - 8, ay - 6), (x + s - 1, ay), (x + s - 8, ay + 6)],
              fill=NAVY)
    d.polygon([(x + 8, ay - 6), (x + 1, ay), (x + 8, ay + 6)], fill=NAVY)
    # small coin at bottom right, clear of the arrow
    d.ellipse([x + s - 20, y + s - 18, x + s - 4, y + s - 2],
              fill=GOLD, outline=INK, width=2)
    d.text((x + s - 16, y + s - 17), "$", font=font(SANS_B, 12),
           fill=INK)


def icon_virus(d, x, y, s):
    """Spiked virus circle: measles."""
    d.rectangle([x, y, x + s, y + s], fill=SKY)
    cx, cy, r = x + s // 2, y + s // 2, 16
    for ang in range(0, 360, 30):
        import math
        a = math.radians(ang)
        x1 = cx + int((r + 2) * math.cos(a))
        y1 = cy + int((r + 2) * math.sin(a))
        x2 = cx + int((r + 10) * math.cos(a))
        y2 = cy + int((r + 10) * math.sin(a))
        d.line([(x1, y1), (x2, y2)], fill=RED, width=3)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=RED)
    d.ellipse([cx - 8, cy - 9, cx - 1, cy - 2], fill=(255, 120, 120))
    d.ellipse([cx + 3, cy + 4, cx + 9, cy + 10], fill=(255, 120, 120))


def icon_quake(d, x, y, s):
    """Cracked ground under a leaning building."""
    d.rectangle([x, y, x + s, y + s], fill=SKY)
    gy = y + s - 18
    # leaning building with windows, kept inside the box
    d.polygon([(x + 18, gy), (x + 25, y + 12), (x + 43, y + 16),
               (x + 38, gy)], fill=NAVY)
    for wy in (y + 24, y + 34):
        d.rectangle([x + 26, wy, x + 31, wy + 4], fill=(255, 255, 255))
        d.rectangle([x + 34, wy + 1, x + 39, wy + 5], fill=(255, 255, 255))
    # ground crack zigzag
    pts = [(x + 4, gy + 6), (x + 18, gy - 2), (x + 30, gy + 8),
           (x + 44, gy - 2), (x + s - 4, gy + 6)]
    d.line(pts, fill=RED, width=3)
    # shaking lines
    for sx in (x + 8, x + s - 12):
        d.line([(sx, y + 10), (sx, y + 22)], fill=GREY, width=2)


ICONS = {
    "summit": icon_summit,
    "drone": icon_drone,
    "city": icon_city,
    "cyclone": icon_cyclone,
    "plane": icon_plane,
    "trade": icon_trade,
    "virus": icon_virus,
    "quake": icon_quake,
}

# --- stories (all verified events of Wednesday 18 November 2026) -----------
LEAD = (
    "LEAD STORY  •  SHENZHEN SUMMIT",
    "Trump, Xi and Putin meet in Shenzhen",
    "A first-ever trilateral summit: Trump arrives in China and shakes "
    "hands with Putin, their first meeting in over a year.",
    "summit",
)

STORIES = [
    ("IRAN WAR", "Iran strikes US bases in the Gulf",
     "Drones hit Patriot systems at Ali Al Salem in Kuwait; Gulf "
     "states intercept missiles and drones.",
     "drone"),
    ("GAZA", "Israel begins Gaza operation",
     "A \u201cconcentrated operation\u201d starts in three areas of "
     "central Gaza.",
     "city"),
    ("CYCLONE", "Cyclone Akvan strengthens",
     "Odisha moves people from unsafe houses to shelters as the "
     "severe storm builds.",
     "cyclone"),
    ("SIBERIA", "Plane crash kills 19 in Siberia",
     "A Russian military transport plane goes down; all 19 people "
     "on board are killed.",
     "plane"),
    ("TRADE", "India\u2013US deal nearly finalised",
     "Signing waits on a new US tariff framework; Modi returns to "
     "New Delhi after ASEAN in Manila.",
     "trade"),
    ("HEALTH", "US loses measles-free status",
     "5,400+ cases this year \u2014 the worst in over three decades.",
     "virus"),
    ("EARTHQUAKE", "Magnitude 6.0 quake hits PNG",
     "A magnitude 6.0 earthquake strikes Papua New Guinea.",
     "quake"),
]

NUMBERS = [("19", "killed in the\nSiberia crash"),
           ("5,400+", "US measles\ncases in 2026"),
           ("350 MW", "Nepal power\nimport today"),
           ("6.0", "PNG quake\nmagnitude")]


# --- page -------------------------------------------------------------------
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 44
    CW = W - 2 * MX

    # outer double frame
    d.rectangle([16, 16, W - 17, H - 17], outline=RULE, width=3)
    d.rectangle([22, 22, W - 23, H - 23], outline=RULE, width=1)

    # masthead
    f_mast = font(SERIF_B, 74)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 32), title, font=f_mast, fill=INK)
    f_tag = font(SANS_B, 17)
    tag = "ONE DAY  •  ONE PAGE  •  THE WORLD IN BRIEF"
    tw = d.textlength(tag, font=f_tag)
    d.text(((W - tw) / 2, 118), tag, font=f_tag, fill=GREY)
    rule(d, MX, W - MX, 148, width=3)

    # date band
    d.rectangle([MX, 160, W - MX, 208], fill=NAVY)
    f_date = font(SANS_B, 36)
    date = "WEDNESDAY 18 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, 169), date, font=f_date, fill=(255, 255, 255))

    # ---- lead story ------------------------------------------------------
    ly0, ly1 = 222, 462
    d.rectangle([MX, ly0, W - MX, ly1], fill=CARD, outline=RULE, width=2)
    f_kick = font(SANS_B, 19)
    d.text((MX + 22, ly0 + 14), LEAD[0], font=f_kick, fill=RED)
    f_lead = font(SANS_B, 36)
    lines = wrap(d, LEAD[1], f_lead, 556)
    y = draw_lines(d, MX + 22, ly0 + 46, lines, f_lead, INK, 44)
    f_sum = font(SANS_R, 23)
    lines = wrap(d, LEAD[2], f_sum, 556)
    draw_lines(d, MX + 22, y + 12, lines, f_sum, INK, 29)
    px, py, ps = W - MX - 22 - 300, ly0 + 16, 300
    ICONS[LEAD[3]](d, px, py, ps)
    d.rectangle([px, py, px + ps, py + int(ps * 0.66)], outline=RULE,
                width=2)

    # ---- story grid: 2 columns x 4 rows ----------------------------------
    gx, gy = MX, 474
    cell_w, cell_h = (CW - 16) // 2, 114
    f_k = font(SANS_B, 15)
    f_h = font(SANS_B, 21)
    f_s = font(SANS_R, 17)

    cells = list(STORIES) + [None]  # last cell = numbers box
    for idx, story in enumerate(cells):
        col, row = idx % 2, idx // 2
        x0 = gx + col * (cell_w + 16)
        y0 = gy + row * (cell_h + 8)
        d.rectangle([x0, y0, x0 + cell_w, y0 + cell_h], fill=CARD,
                    outline=RULE, width=1)
        if story is None:
            d.text((x0 + 16, y0 + 10), "THE DAY IN NUMBERS", font=f_k,
                   fill=RED)
            nx = x0 + 16
            f_n = font(SANS_B, 24)
            f_nl = font(SANS_R, 14)
            for num, lab in NUMBERS:
                d.text((nx, y0 + 34), num, font=f_n, fill=NAVY)
                ly = y0 + 64
                for lab_line in lab.split("\n"):
                    d.text((nx, ly), lab_line, font=f_nl, fill=GREY)
                    ly += 17
                nx += 108
            continue
        kicker, headline, summary, icon = story
        d.text((x0 + 78, y0 + 8), kicker, font=f_k, fill=RED)
        lines = wrap(d, headline, f_h, cell_w - 94)
        draw_lines(d, x0 + 78, y0 + 26, lines[:2], f_h, INK, 24)
        lines = wrap(d, summary, f_s, cell_w - 32)
        draw_lines(d, x0 + 16, y0 + 74, lines[:2], f_s, INK, 19)
        ICONS[icon](d, x0 + 10, y0 + 8, 58)

    # footer
    f_f = font(SANS_R, 15)
    foot = "All stories verified from live news reporting on 18 November 2026"
    tw = d.textlength(foot, font=f_f)
    d.text(((W - tw) / 2, 984), foot, font=f_f, fill=GREY)

    img.save(OUT, optimize=True)
    print(f"wrote {OUT} ({os.path.getsize(OUT)} bytes)")


if __name__ == "__main__":
    main()
