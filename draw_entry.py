#!/usr/bin/env python3
"""Draw the news-image-20261123 entry: one newspaper-style front page that sums
up the world news of Monday 23 November 2026.

Lead story: a Russian strike levelled an apartment block in Dymer, north of
Kyiv; rescuers pulled a 7-year-old boy out alive while the death toll climbed
past 15. Side stories: a Russian corvette sunk at Benghazi, the COP31 talks
collapsing in Antalya, and two supertankers ablaze near the Strait of Hormuz.

Run:  python3 draw_entry.py   ->  writes entry.png beside this file.
The image is 1024 x 1024, flat shapes and bold text, legible at a glance.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
MARGIN = 32

PAPER = (246, 243, 236)
INK = (18, 18, 18)
RED = (176, 32, 32)
GREY_TEXT = (70, 70, 70)

BOLD_PATHS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
REGULAR_PATHS = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def pick(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    raise SystemExit("no usable font found in " + ", ".join(paths))


BOLD = pick(BOLD_PATHS)
REGULAR = pick(REGULAR_PATHS)


def bold(size):
    return ImageFont.truetype(BOLD, size)


def regular(size):
    return ImageFont.truetype(REGULAR, size)


def fit(draw, text, max_w, size, path=BOLD):
    """Largest font at or below size whose text fits max_w."""
    while size > 10:
        f = ImageFont.truetype(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 2
    return ImageFont.truetype(path, size)


def centered(draw, cx, y, text, f, fill):
    w = draw.textlength(text, font=f)
    draw.text((cx - w / 2, y), text, font=f, fill=fill)


def slab(d, cx, cy, w, h, ang, fill, outline=(38, 38, 42)):
    """A rotated concrete slab (a parallelogram of rubble)."""
    a = math.radians(ang)
    pts = []
    for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2)):
        pts.append((cx + dx * math.cos(a) - dy * math.sin(a),
                    cy + dx * math.sin(a) + dy * math.cos(a)))
    d.polygon(pts, fill=fill, outline=outline, width=3)


def rescuer(d, x, y, s, vest=(255, 124, 30)):
    """A simple rescue worker: white helmet, hi-vis vest, dark limbs.
    (x, y) is the ground point between the feet; s is the figure height."""
    skin = (232, 190, 150)
    dark = (30, 32, 38)
    head_r = 0.10 * s
    head_cy = y - s + head_r
    # legs
    d.line([x - 0.16 * s, y, x - 0.05 * s, y - 0.38 * s], fill=dark, width=max(4, int(0.07 * s)))
    d.line([x + 0.16 * s, y, x + 0.05 * s, y - 0.38 * s], fill=dark, width=max(4, int(0.07 * s)))
    # torso (vest)
    d.polygon([(x - 0.17 * s, y - 0.36 * s), (x + 0.17 * s, y - 0.36 * s),
               (x + 0.13 * s, y - 0.72 * s), (x - 0.13 * s, y - 0.72 * s)], fill=vest)
    # arms
    d.line([x - 0.14 * s, y - 0.68 * s, x - 0.30 * s, y - 0.42 * s], fill=dark, width=max(4, int(0.06 * s)))
    d.line([x + 0.14 * s, y - 0.68 * s, x + 0.30 * s, y - 0.42 * s], fill=dark, width=max(4, int(0.06 * s)))
    # head + helmet
    d.ellipse([x - head_r, head_cy - head_r, x + head_r, head_cy + head_r], fill=skin)
    d.pieslice([x - head_r - 2, head_cy - head_r - 2, x + head_r + 2, head_cy + head_r + 2],
               start=180, end=360, fill=(245, 245, 245), outline=dark)
    # headlamp
    lamp_r = max(2.5, 0.035 * s)
    d.ellipse([x - lamp_r, head_cy - head_r - lamp_r, x + lamp_r, head_cy - head_r + lamp_r],
              fill=(255, 244, 170), outline=dark)


def flame(d, cx, base_y, h, w):
    """A jagged flame silhouette in three layered colours."""
    for hh, ww, col in ((h, w, (216, 66, 30)), (h * 0.66, w * 0.64, (243, 138, 38)),
                        (h * 0.38, w * 0.36, (252, 208, 84))):
        pts = [(cx - ww / 2, base_y), (cx - ww * 0.16, base_y - hh * 0.52),
               (cx, base_y - hh), (cx + ww * 0.20, base_y - hh * 0.48),
               (cx + ww / 2, base_y)]
        d.polygon(pts, fill=col)
        d.ellipse([cx - ww / 2, base_y - hh * 0.22, cx + ww / 2, base_y + hh * 0.08], fill=col)


def chair(d, x, y, s, col=(96, 110, 128)):
    """An empty chair seen from the front: back, seat, two legs."""
    d.rectangle([x, y, x + s, y + s * 0.55], fill=col, outline=INK, width=2)
    d.rectangle([x - s * 0.08, y + s * 0.55, x + s * 1.08, y + s * 0.72], fill=col, outline=INK, width=2)
    d.line([x + 2, y + s * 0.72, x + 2, y + s * 1.15], fill=INK, width=3)
    d.line([x + s - 2, y + s * 0.72, x + s - 2, y + s * 1.15], fill=INK, width=3)


def draw_lead_scene(img):
    """The Dymer rescue: night, a levelled apartment block, rescuers at work."""
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = MARGIN, 262, W - MARGIN, 672
    # night sky
    d.rectangle([x0, y0, x1, y1], fill=(36, 46, 64))
    # standing wall fragment, left: a five-storey corner with a broken top
    wall = [(58, 672), (58, 340), (104, 316), (150, 344), (196, 330), (222, 372), (222, 672)]
    d.polygon(wall, fill=(118, 124, 132), outline=(16, 18, 24), width=3)
    for r in range(5):
        for c in range(2):
            wx = 76 + c * 62
            wy = 356 + r * 58
            lit = (r, c) == (1, 1)
            d.rectangle([wx, wy, wx + 34, wy + 36], fill=(244, 200, 92) if lit else (26, 31, 42),
                        outline=(16, 18, 24), width=2)
    # broken wall fragment, right
    d.polygon([(856, 672), (856, 452), (902, 420), (946, 452), (966, 430), (966, 672)],
              fill=(104, 110, 118), outline=(16, 18, 24), width=3)
    d.rectangle([884, 486, 916, 520], fill=(26, 31, 42), outline=(16, 18, 24), width=2)
    # fallen slabs across the middle
    slab(d, 420, 486, 300, 34, -14, (150, 155, 162))
    slab(d, 478, 552, 340, 36, 9, (138, 143, 150))
    slab(d, 540, 612, 380, 38, -5, (160, 164, 170))
    slab(d, 742, 520, 210, 30, 22, (144, 149, 156))
    # exposed rebar sticking out of the slabs
    for rx, ry, dx, dy in ((300, 462, -26, -30), (560, 462, 14, -34), (668, 540, 30, -22),
                           (392, 588, -30, -18)):
        d.line([rx, ry, rx + dx, ry + dy], fill=(20, 20, 24), width=4)
    # rubble mound along the bottom
    d.polygon([(268, 672), (420, 566), (618, 528), (806, 596), (918, 672)],
              fill=(100, 104, 112), outline=(16, 18, 24), width=3)
    slab(d, 470, 620, 90, 22, 12, (128, 132, 138))
    slab(d, 660, 606, 80, 20, -16, (122, 126, 132))
    slab(d, 372, 646, 64, 18, -8, (134, 138, 144))

    # glow behind the rescued boy, then headlamp beams (translucent overlays)
    fx, fy = 596, 600
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, a in ((120, 26), (88, 40), (56, 58)):
        gd.ellipse([fx - r, fy - r, fx + r, fy + r], fill=(255, 236, 170, a))
    for bx, by, tx, ty in ((430, 512, 520, 640), (700, 528, 636, 648)):
        gd.polygon([(bx, by), (tx - 34, ty), (tx + 34, ty)], fill=(255, 240, 180, 62))
    # dust hanging over the rubble
    for cx, cy, rw, rh in ((360, 520, 120, 26), (700, 486, 140, 30), (540, 452, 100, 22)):
        gd.ellipse([cx - rw, cy - rh, cx + rw, cy + rh], fill=(200, 204, 210, 46))
    img.alpha_composite(glow)
    d = ImageDraw.Draw(img)

    # rescuers: one standing left, one kneeling centre with the boy, one digging right
    rescuer(d, 430, 636, 96)
    rescuer(d, 706, 640, 92, vest=(255, 176, 32))
    # shovel in the right rescuer's hands
    d.line([736, 600, 770, 646], fill=(90, 62, 34), width=6)
    d.polygon([(770, 646), (786, 640), (782, 660)], fill=(70, 74, 80))
    # kneeling rescuer at centre, drawn lower and wider
    rescuer(d, 548, 652, 84)
    # the boy, wrapped in a blue blanket, carried in front of the centre rescuer
    d.rounded_rectangle([576, 590, 646, 618], radius=12, fill=(64, 104, 196), outline=(16, 18, 24), width=3)
    d.ellipse([640, 588, 664, 612], fill=(232, 190, 150), outline=(16, 18, 24), width=2)
    # ground shadow strip
    d.rectangle([x0, 656, x1, y1], fill=(24, 30, 42))
    # scene frame
    d.rectangle([x0, y0, x1, y1], outline=INK, width=4)


def draw_panel_ship(d, x0, y0, x1, y1):
    """A Russian corvette sinking at Benghazi, a sea drone closing in."""
    d.rectangle([x0, y0, x1, y1], fill=(196, 212, 224))
    sea_y = y0 + int((y1 - y0) * 0.52)
    d.rectangle([x0, sea_y, x1, y1], fill=(43, 94, 138))
    cx = (x0 + x1) / 2
    # smoke from the stern
    for sx, sy, r in ((cx + 74, y0 + 26, 17), (cx + 92, y0 + 12, 13), (cx + 58, y0 + 40, 12)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(105, 108, 112))
    # hull, bow up to the left, stern settling to the right
    hull = [(x0 + 36, sea_y + 6), (x0 + 236, sea_y - 14), (x0 + 262, sea_y + 8),
            (x0 + 232, sea_y + 34), (x0 + 66, sea_y + 36)]
    d.polygon(hull, fill=(96, 104, 112), outline=INK, width=3)
    # superstructure and mast
    d.rectangle([cx - 28, sea_y - 44, cx + 18, sea_y - 8], fill=(110, 118, 126), outline=INK, width=3)
    d.line([cx - 6, sea_y - 44, cx - 6, sea_y - 70], fill=INK, width=4)
    d.line([cx - 22, sea_y - 64, cx + 10, sea_y - 64], fill=INK, width=4)
    # splashes where the stern goes under
    for sx in (x0 + 226, x0 + 244, x0 + 210):
        d.arc([sx - 12, sea_y + 16, sx + 12, sea_y + 40], start=180, end=330, fill=(240, 246, 250), width=3)
    # the sea drone: a small dark craft with a wake, lower left
    dx, dy = x0 + 52, y1 - 34
    d.polygon([(dx, dy), (dx + 52, dy - 4), (dx + 62, dy + 6), (dx + 8, dy + 9)], fill=(22, 26, 32))
    d.rectangle([dx + 20, dy - 10, dx + 36, dy - 2], fill=(22, 26, 32))
    d.line([dx - 26, dy + 12, dx + 4, dy + 8], fill=(240, 246, 250), width=3)
    d.line([dx - 18, dy + 20, dx + 10, dy + 12], fill=(240, 246, 250), width=3)
    # waves
    for wx, wy in ((x0 + 120, y1 - 22), (x0 + 190, y1 - 14), (x0 + 96, sea_y + 52)):
        d.arc([wx - 16, wy - 8, wx + 16, wy + 8], start=200, end=340, fill=(240, 246, 250), width=3)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=3)


def draw_panel_talks(d, x0, y0, x1, y1):
    """COP31: a torn agreement over a table of empty chairs."""
    d.rectangle([x0, y0, x1, y1], fill=(233, 227, 212))
    cx = (x0 + x1) / 2
    # the torn agreement: two halves of one sheet, pulled apart
    jag_l = [(cx - 96, y0 + 16), (cx - 8, y0 + 16), (cx - 22, y0 + 40), (cx - 4, y0 + 62),
             (cx - 24, y0 + 84), (cx - 96, y0 + 84)]
    jag_r = [(cx + 22, y0 + 22), (cx + 104, y0 + 22), (cx + 104, y0 + 90), (cx + 16, y0 + 90),
             (cx + 32, y0 + 66), (cx + 14, y0 + 44)]
    d.polygon(jag_l, fill=(252, 252, 250), outline=INK, width=3)
    d.polygon(jag_r, fill=(252, 252, 250), outline=INK, width=3)
    for gx in (cx - 84, cx + 34):
        for gy in (y0 + 30, y0 + 48, y0 + 66):
            d.line([gx, gy, gx + 52, gy], fill=(150, 150, 146), width=3)
    # a red cross over the gap: no deal
    d.line([cx - 4, y0 + 34, cx + 26, y0 + 72], fill=RED, width=6)
    d.line([cx + 26, y0 + 34, cx - 4, y0 + 72], fill=RED, width=6)
    # conference table
    d.rectangle([x0 + 34, y1 - 62, x1 - 34, y1 - 40], fill=(122, 84, 52), outline=INK, width=3)
    d.line([x0 + 52, y1 - 40, x0 + 52, y1 - 14], fill=INK, width=4)
    d.line([x1 - 52, y1 - 40, x1 - 52, y1 - 14], fill=INK, width=4)
    # nameplates on the table
    for nx in (x0 + 78, cx - 14, x1 - 106):
        d.rectangle([nx, y1 - 76, nx + 30, y1 - 62], fill=(252, 252, 250), outline=INK, width=2)
    # empty chairs behind the table
    for chx in (x0 + 52, cx - 62, cx + 44):
        chair(d, chx, y1 - 118, 30)
    # one chair tipped over in front: the talks have collapsed
    slab(d, x1 - 66, y1 - 30, 44, 12, 38, (96, 110, 128))
    slab(d, x1 - 84, y1 - 18, 34, 10, -24, (96, 110, 128))
    d.rectangle([x0, y0, x1, y1], outline=INK, width=3)


def draw_panel_tankers(d, x0, y0, x1, y1):
    """Two supertankers ablaze near the Strait of Hormuz at dusk."""
    d.rectangle([x0, y0, x1, y1], fill=(248, 168, 92))
    d.rectangle([x0, y0 + int((y1 - y0) * 0.38), x1, y1], fill=(240, 122, 66))
    sea_y = y0 + int((y1 - y0) * 0.58)
    d.rectangle([x0, sea_y, x1, y1], fill=(30, 54, 86))

    def tanker(tx, ty, s, flip=False):
        hull = [(tx, ty), (tx + 128 * s, ty), (tx + 118 * s, ty + 20 * s), (tx + 12 * s, ty + 20 * s)]
        d.polygon(hull, fill=(22, 24, 28), outline=INK, width=2)
        d.rectangle([tx + 14 * s, ty - 14 * s, tx + 58 * s, ty], fill=(22, 24, 28))
        d.rectangle([tx + 92 * s, ty - 24 * s, tx + 112 * s, ty], fill=(22, 24, 28))
        flame(d, tx + 36 * s, ty - 12 * s, 52 * s, 30 * s)
        for sx, sy, r in ((tx + 40 * s, ty - 66 * s, 13 * s), (tx + 56 * s, ty - 80 * s, 10 * s)):
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(62, 58, 58))

    tanker(x0 + 14, sea_y + 16, 1.0)
    tanker(x0 + 168, sea_y + 30, 0.82)
    # the rocky shores of the strait closing in at both corners
    d.polygon([(x0, y1), (x0, y1 - 44), (x0 + 44, y1)], fill=(16, 18, 22))
    d.polygon([(x1, y1), (x1, y1 - 52), (x1 - 50, y1)], fill=(16, 18, 22))
    # firelight on the water
    for wx, wy in ((x0 + 60, y1 - 18), (x0 + 210, y1 - 12)):
        d.line([wx - 18, wy, wx + 18, wy], fill=(250, 170, 80), width=3)
    d.rectangle([x0, y0, x1, y1], outline=INK, width=3)


def main():
    img = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(img)

    # page frame
    d.rectangle([12, 12, W - 12, H - 12], outline=INK, width=4)

    # kicker and date banner
    centered(d, W / 2, 24, "THE DAY'S WORLD NEWS", bold(22), GREY_TEXT)
    d.rectangle([MARGIN, 52, W - MARGIN, 120], fill=INK)
    date_font = fit(d, "MONDAY 23 NOVEMBER 2026", W - 2 * MARGIN - 40, 54)
    centered(d, W / 2, 66, "MONDAY 23 NOVEMBER 2026", date_font, (255, 255, 255))
    d.rectangle([MARGIN, 128, W - MARGIN, 134], fill=RED)

    # lead headline
    centered(d, W / 2, 146, "BOY PULLED ALIVE FROM", bold(56), INK)
    centered(d, W / 2, 208, "THE RUBBLE IN DYMER", bold(56), INK)

    # lead scene
    draw_lead_scene(img)
    d = ImageDraw.Draw(img)
    centered(d, W / 2, 680,
             "Rescuers dig through the night in Dymer, north of Kyiv - the death toll climbs past 15",
             fit(d, "Rescuers dig through the night in Dymer, north of Kyiv - the death toll climbs past 15",
                 W - 2 * MARGIN - 30, 24, REGULAR), GREY_TEXT)
    d.line([MARGIN, 714, W - MARGIN, 714], fill=INK, width=3)

    # three side panels
    panels = [
        (draw_panel_ship, ("RUSSIAN CORVETTE", "SUNK AT BENGHAZI")),
        (draw_panel_talks, ("COP31 TALKS COLLAPSE", "IN ANTALYA")),
        (draw_panel_tankers, ("TANKERS ABLAZE", "NEAR HORMUZ")),
    ]
    pw, gap, py0, py1 = 304, 24, 726, 898
    for i, (fn, label) in enumerate(panels):
        px0 = MARGIN + i * (pw + gap)
        fn(d, px0, py0, px0 + pw, py1)
        d = ImageDraw.Draw(img)
        centered(d, px0 + pw / 2, 906, label[0], bold(26), INK)
        centered(d, px0 + pw / 2, 938, label[1], bold(26), INK)

    # footer
    d.line([MARGIN, 976, W - MARGIN, 976], fill=INK, width=2)
    centered(d, W / 2, 984, "MONDAY 23 NOVEMBER 2026 - WORLD NEWS IN ONE IMAGE", bold(19), GREY_TEXT)

    img.convert("RGB").save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT}: {W}x{H}, {size} bytes")


if __name__ == "__main__":
    main()
