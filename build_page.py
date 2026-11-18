#!/usr/bin/env python3
"""Build the front-page image for make.fun's news-image-20261118 entry.

One 1024x1024 newspaper front page summing up the world news of Wednesday
18 November 2026, drawn entirely with Pillow primitives: real typeset text
and flat spot illustrations, no AI-generated text. Deterministic.

Edition note: this first edition was built mid-day (about 07:20 UTC) from
the day's reporting so far; the file can be re-rendered with the fuller
day before the deadline. Run: python3 build_page.py -> assets/entry.png.
main.py copies that file to /output/entry.png in the grader's sandbox.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (246, 240, 226)
CARD_BG = (255, 253, 246)
INK = (26, 25, 22)
RED = (178, 34, 40)
TEAL = (23, 107, 104)
NAVY = (24, 49, 83)
LINE = (196, 184, 158)
FAINT = (110, 100, 84)

FONT_DIR = "/usr/share/fonts/truetype/noto/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def serif(size, weight="Black"):
    return font(f"NotoSerif-{weight}.ttf", size)


def sans(size, weight="Regular"):
    return font(f"NotoSans-{weight}.ttf", size)


def wrap(d, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(d, xy, text, fnt, fill, width, leading):
    x, y = xy
    for ln in wrap(d, text, fnt, width):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- stories
# Every story below happened, or was first reported, on Wednesday
# 18 November 2026 (checked against the day's wire and broadcaster
# roundups available by about 07:20 UTC). Contested claims are
# attributed in the wording.

LEADS = [
    dict(n=1, region="MIDDLE EAST \u00b7 IRAN WAR", art="gulf2",
         headline="Bahrain downs six more Iranian drones; Kuwait also fires",
         summary="Second attack on US radar sites in three days; "
                 "the US confirms its Qeshm strike."),
    dict(n=2, region="EUROPE \u00b7 UKRAINE WAR", art="talks",
         headline="US scolds Kyiv on deep strikes as peace talks gather pace",
         summary="Zelensky confers with Kushner and Witkoff; envoys "
                 "seek one peace framework."),
    dict(n=3, region="MIDDLE EAST \u00b7 POLITICS", art="israel",
         headline="Israel's president asks Eisenkot to form a government",
         summary="The tap bypasses Netanyahu after the deadlocked "
                 "election; Knesset sworn in."),
]

CARDS = [
    dict(n=4, region="OCEANIA \u00b7 DISASTER", art="cyclone",
         headline="Cyclone Xavier, category 5, hits the Cook Islands",
         summary="Landfall in the northern Cooks; damage reports still coming in."),
    dict(n=5, region="ASIA \u00b7 DEFENCE", art="missile",
         headline="North Korea fires a ballistic missile into the sea",
         summary="Seoul says it came hours after US, Korean and Japanese drills."),
    dict(n=6, region="MIDDLE EAST \u00b7 GAZA", art="flood",
         headline="Floods deepen Gaza's misery as aid calls grow",
         summary="Four nations demand open crossings; one hot meal every two days."),
    dict(n=7, region="EUROPE \u00b7 DISASTER", art="quake",
         headline="Magnitude 5.3 earthquake strikes Romania",
         summary="The early-morning tremor was felt across the region."),
    dict(n=8, region="GLOBAL \u00b7 GAMING", art="gta",
         headline="The world counts down to GTA VI",
         summary="The decade's most awaited game unlocks first in New Zealand."),
    dict(n=9, region="AMERICAS \u00b7 POLITICS", art="venezuela",
         headline="US details $12bn from Venezuela's oil and minerals",
         summary="A 53-page report, a year after US forces captured Maduro."),
    dict(n=10, region="ASIA \u00b7 JUSTICE", art="court",
         headline="World Court to rule in Myanmar genocide case",
         summary="The Hague prepares its judgment in the Rohingya case."),
    dict(n=11, region="EUROPE \u00b7 FRANCE", art="protest",
         headline="Students blockade schools as French protests swell",
         summary="Unions join the cost-of-living movement; campuses shut."),
]

ALSO = [
    "Kerch Bridge shut a second day",
    "Kuwait reports drone interceptions",
    "UN: 372 Ukraine civilians killed in Oct",
    "Latvia backs Kulbergs government",
    "Malaysia eases rare-earth curbs",
    "Macron in Kuala Lumpur for plant deal",
    "Berlin charges Russian informant",
    "Guatemala prosecutor shot, wounded",
    "Cyber-attack freezes store freezers",
    "Canaries: 2,331 arrivals in a weekend",
    "Minister visits El Hierro on arrivals",
    "Alaska: Peltola wins, Dems at 56 seats",
    "France tests M51.3 submarine missile",
    "Iran executes man who fired on police",
    "Burnham reopens EU membership debate",
    "Merz warns Europe not to tire of Ukraine",
    "San Francisco extends data-centre freeze",
    "Leukaemia vaccine cuts death risk 41%",
    "German chess medal, first in 26 years",
    "Lula eyes fourth term vs Bolsonaro's son",
    "ESA chief calls for space laws",
    "M1.1 solar flare recorded on the Sun",
    "1,100 Gaza child amputees lack care",
    "Flydubai co-pilot was flagged a risk",
    "Climber survives 100m fall in the Alps",
    "US debates $50bn air-traffic funding",
]

TOTAL = len(LEADS) + len(CARDS) + len(ALSO)


# ------------------------------------------------------------ illustrations
# Lead art boxes are ~313x92, small-card art strips ~232x50. All labels
# are kept inside their box.

def _flag(d, x, y, w, h, kind):
    if kind == "us":
        for i in range(7):
            d.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                        fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
        d.rectangle([x, y, x + w * 0.45, y + h * 4 / 7], fill=(36, 44, 92))
    elif kind == "ua":
        d.rectangle([x, y, x + w, y + h / 2], fill=(40, 90, 170))
        d.rectangle([x, y + h / 2, x + w, y + h], fill=(245, 200, 40))
    elif kind == "eu":
        import math
        d.rectangle([x, y, x + w, y + h], fill=(30, 50, 140))
        for a in range(12):
            sx = x + w / 2 + (w * 0.30) * math.cos(a * math.pi / 6)
            sy = y + h / 2 + (h * 0.30) * math.sin(a * math.pi / 6)
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(250, 210, 60))
    elif kind == "il":
        d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
        d.rectangle([x, y + h * 0.16, x + w, y + h * 0.32], fill=(30, 60, 160))
        d.rectangle([x, y + h * 0.68, x + w, y + h * 0.84], fill=(30, 60, 160))
        cx, cy = x + w / 2, y + h / 2
        d.polygon([(cx, cy - 7), (cx + 6, cy + 4), (cx - 6, cy + 4)], outline=(30, 60, 160), width=2)
        d.polygon([(cx, cy + 7), (cx + 6, cy - 4), (cx - 6, cy - 4)], outline=(30, 60, 160), width=2)


def art_gulf2(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h * 0.62], fill=(224, 208, 168))
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(70, 118, 148))
    d.text((x + 42, y + 8), "BAHRAIN", font=sans(11, "Bold"), fill=INK)
    d.text((x + w - 14, y + 8), "QESHM \u00b7 IRAN", font=sans(11, "Bold"), fill=INK, anchor="ra")
    pts = [(x + w * 0.16, y + h * 0.34), (x + w * 0.42, y + h * 0.16), (x + w * 0.68, y + h * 0.32)]
    d.line(pts, fill=RED, width=3)
    for i in range(3):
        ex, ey = x + w * (0.22 + i * 0.13), y + h * (0.30 - (i % 2) * 0.08)
        d.polygon([(ex, ey), (ex - 11, ey - 4), (ex - 9, ey + 5)], fill=(66, 66, 70))
    dx, dy = pts[-1]
    d.polygon([(dx, dy), (dx - 15, dy - 5), (dx - 12, dy + 7)], fill=INK)
    sx, sy = x + w * 0.86, y + h * 0.30
    d.line([sx - 8, sy - 8, sx + 8, sy + 8], fill=RED, width=3)
    d.line([sx - 8, sy + 8, sx + 8, sy - 8], fill=RED, width=3)
    d.rectangle([x + w * 0.06, y + h * 0.70, x + w * 0.34, y + h * 0.92], fill=RED)
    d.text((x + w * 0.20, y + h * 0.81), "SIX DOWNED", font=sans(11, "Bold"),
           fill=(255, 255, 255), anchor="mm")
    tx, ty = x + w * 0.66, y + h * 0.80
    d.polygon([(tx, ty), (tx + 58, ty), (tx + 50, ty + 9), (tx + 8, ty + 9)], fill=(38, 38, 42))
    d.rectangle([tx + 12, ty - 7, tx + 44, ty], fill=(150, 60, 50))
    d.text((x + w * 0.97, y + h * 0.70), "KUWAIT", font=sans(9, "Bold"),
           fill=(255, 255, 255), anchor="ra")


def art_talks(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(38, 58, 92))
    fw, fh = w * 0.20, h * 0.52
    fy = y + h * 0.16
    for i, kind in enumerate(["us", "ua", "eu"]):
        fx = x + w * (0.06 + i * 0.26)
        d.rectangle([fx - 2, fy - 2, fx + fw + 2, fy + fh + 2], fill=(255, 255, 255))
        _flag(d, fx, fy, fw, fh, kind)
    labels = ["WASHINGTON", "KYIV", "EUROPE"]
    for i, t in enumerate(labels):
        d.text((x + w * (0.06 + i * 0.26) + fw / 2, fy + fh + 6), t,
               font=sans(9, "Bold"), fill=(255, 255, 255), anchor="ma")
    d.rectangle([x + w * 0.84, fy, x + w * 0.98, fy + fh], fill=(240, 238, 230))
    d.text((x + w * 0.91, fy + fh / 2), "ONE\nFRAME-\nWORK", font=sans(9, "Bold"),
           fill=INK, anchor="mm")


def art_israel(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 235, 239))
    for i in range(6):
        cx = x + w * (0.05 + i * 0.115)
        d.rectangle([cx, y + h * 0.30, cx + w * 0.07, y + h * 0.80], fill=(172, 174, 180))
        d.rectangle([cx - 3, y + h * 0.23, cx + w * 0.07 + 3, y + h * 0.30], fill=(142, 144, 150))
    d.rectangle([x, y + h * 0.80, x + w, y + h * 0.87], fill=(142, 144, 150))
    _flag(d, x + w * 0.80, y + h * 0.08, w * 0.16, h * 0.34, "il")
    d.text((x + w * 0.17, y + h * 0.06), "THE KNESSET", font=sans(10, "Bold"), fill=(90, 92, 98))
    d.rectangle([x + w * 0.72, y + h * 0.52, x + w * 0.99, y + h * 0.78], fill=NAVY)
    d.text((x + w * 0.855, y + h * 0.65), "EISENKOT'S TAP", font=sans(9.5, "Bold"),
           fill=(255, 255, 255), anchor="mm")


def art_cyclone(d, x, y, w, h):
    import math
    d.rectangle([x, y, x + w, y + h], fill=(88, 130, 160))
    cx, cy = x + w * 0.16, y + h * 0.52
    for r in (17, 12, 7):
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], 20, 300, fill=(240, 244, 246), width=3)
        d.arc([cx - r, cy - r * 0.8, cx + r, cy + r * 0.8], 200, 480, fill=(200, 216, 226), width=3)
    for px in (0.42, 0.52):
        bx = x + w * px
        d.line([bx, y + h * 0.92, bx + 3, y + h * 0.30], fill=(52, 84, 46), width=3)
        for a in (-0.5, 0.1, 0.7):
            ex = bx + 3 + 12 * math.cos(a - 0.6)
            ey = y + h * 0.30 + 7 * math.sin(a - 0.6)
            d.line([bx + 3, y + h * 0.30, ex, ey], fill=(52, 100, 52), width=2)
    d.rectangle([x + w * 0.62, y + h * 0.18, x + w * 0.97, y + h * 0.62], fill=RED)
    d.text((x + w * 0.795, y + h * 0.40), "CATEGORY 5", font=sans(11, "Bold"),
           fill=(255, 255, 255), anchor="mm")
    d.text((x + w * 0.62, y + h * 0.70), "COOK ISLANDS", font=sans(9, "Bold"), fill=(255, 255, 255))


def art_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 36, 54))
    for sx, sy in [(0.06, 0.2), (0.30, 0.12), (0.55, 0.18), (0.86, 0.12)]:
        d.ellipse([x + w * sx, y + h * sy, x + w * sx + 3, y + h * sy + 3], fill=(230, 232, 240))
    d.rectangle([x, y + h * 0.80, x + w, y + h], fill=(24, 60, 84))
    d.line([x + w * 0.06, y + h * 0.84, x + w * 0.34, y + h * 0.30, x + w * 0.58, y + h * 0.52],
           fill=(240, 160, 60), width=2)
    mx, my = x + w * 0.36, y + h * 0.28
    d.polygon([(mx, my), (mx + 15, my + 7), (mx + 3, my + 11), (mx - 4, my + 5)], fill=(210, 214, 220))
    d.polygon([(mx - 4, my + 5), (mx - 12, my + 11), (mx + 2, my + 10)], fill=(240, 120, 40))
    d.rectangle([x + w * 0.66, y + h * 0.16, x + w * 0.97, y + h * 0.52], fill=(150, 40, 40))
    d.text((x + w * 0.815, y + h * 0.34), "SEA OF JAPAN", font=sans(9.5, "Bold"),
           fill=(255, 255, 255), anchor="mm")


def art_flood(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(196, 208, 216))
    wy = y + h * 0.60
    d.rectangle([x, wy, x + w, y + h], fill=(90, 130, 150))
    for i, tx in enumerate([0.05, 0.24, 0.43]):
        px = x + w * tx
        d.polygon([(px, wy + 3), (px + w * 0.08, wy - h * 0.34), (px + w * 0.16, wy + 3)],
                  fill=(240, 238, 230), outline=FAINT)
    d.rectangle([x + w * 0.68, y + h * 0.14, x + w * 0.97, y + h * 0.56], fill=(178, 60, 40))
    d.text((x + w * 0.825, y + h * 0.35), "FLOODED", font=sans(11, "Bold"),
           fill=(255, 255, 255), anchor="mm")


def art_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 216, 192))
    gy = y + h * 0.66
    d.rectangle([x, gy, x + w, y + h], fill=(188, 168, 138))
    pts = [(x + w * 0.26, gy), (x + w * 0.33, gy + h * 0.14), (x + w * 0.30, gy + h * 0.22),
           (x + w * 0.40, y + h)]
    d.line(pts, fill=(70, 54, 40), width=3)
    bx0 = x + w * 0.05
    d.rectangle([bx0, gy - h * 0.44, bx0 + w * 0.15, gy], fill=(150, 148, 144), outline=INK)
    for r in range(2):
        for cidx in range(2):
            d.rectangle([bx0 + 6 + cidx * w * 0.065, gy - h * 0.36 + r * h * 0.17,
                         bx0 + 13 + cidx * w * 0.065, gy - h * 0.26 + r * h * 0.17], fill=(240, 230, 180))
    d.text((x + w * 0.97, y + h * 0.10), "5.3", font=serif(26, "Black"), fill=INK, anchor="ra")
    d.text((x + w * 0.97, y + h * 0.70), "ROMANIA \u00b7 06:17 UTC", font=sans(9, "Bold"), fill=INK, anchor="ra")


def art_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 20, 34))
    d.text((x + w * 0.11, y + h / 2), "VI", font=serif(30, "Black"), fill=(250, 190, 60), anchor="lm")
    cx, cy = x + w * 0.52, y + h * 0.50
    d.rounded_rectangle([cx - 34, cy - 14, cx + 34, cy + 15], 11, fill=(52, 48, 70), outline=(150, 144, 180), width=2)
    d.line([cx - 22, cy, cx - 10, cy], fill=(230, 230, 240), width=3)
    d.line([cx - 16, cy - 6, cx - 16, cy + 6], fill=(230, 230, 240), width=3)
    for dx, dy, col in [(16, -4, (240, 90, 90)), (24, 3, (90, 200, 120)), (16, 9, (90, 140, 240))]:
        d.ellipse([cx + dx - 4, cy + dy - 4, cx + dx + 4, cy + dy + 4], fill=col)
    d.text((x + w * 0.97, y + h * 0.28), "OUT", font=sans(10, "Bold"), fill=(250, 190, 60), anchor="ra")
    d.text((x + w * 0.97, y + h * 0.58), "19 NOV", font=sans(10, "Bold"), fill=(250, 190, 60), anchor="ra")


def art_venezuela(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 44, 40))
    for i, bh in enumerate([0.42, 0.60, 0.78]):
        bx = x + w * (0.05 + i * 0.13)
        d.rounded_rectangle([bx, y + h * 0.90 - h * bh, bx + w * 0.09, y + h * 0.90], 3,
                            fill=(196, 138, 30), outline=(120, 84, 20))
    d.text((x + w * 0.50, y + h * 0.16), "$12BN", font=sans(19, "Black"), fill=(250, 210, 90))
    d.text((x + w * 0.50, y + h * 0.58), "OIL + MINERALS", font=sans(9.5, "Bold"), fill=(240, 240, 235))


def art_court(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 234, 222))
    d.polygon([(x + w * 0.06, y + h * 0.10), (x + w * 0.50, y + h * 0.10), (x + w * 0.44, y + h * 0.22),
               (x + w * 0.12, y + h * 0.22)], fill=(150, 148, 140))
    for i in range(3):
        cx = x + w * (0.12 + i * 0.13)
        d.rectangle([cx, y + h * 0.28, cx + w * 0.06, y + h * 0.76], fill=(170, 168, 160))
    d.rectangle([x + w * 0.05, y + h * 0.76, x + w * 0.50, y + h * 0.86], fill=(150, 148, 140))
    sx = x + w * 0.74
    d.line([sx, y + h * 0.16, sx, y + h * 0.66], fill=INK, width=3)
    d.line([sx - 24, y + h * 0.22, sx + 24, y + h * 0.22], fill=INK, width=3)
    for dx in (-24, 24):
        d.line([sx + dx, y + h * 0.22, sx + dx - 8, y + h * 0.46], fill=INK, width=2)
        d.line([sx + dx, y + h * 0.22, sx + dx + 8, y + h * 0.46], fill=INK, width=2)
        d.arc([sx + dx - 10, y + h * 0.40, sx + dx + 10, y + h * 0.58], 0, 180, fill=INK, width=2)
    d.text((x + w * 0.97, y + h * 0.80), "THE HAGUE", font=sans(9, "Bold"), fill=INK, anchor="ra")


def art_protest(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(236, 228, 208))
    d.rectangle([x + w * 0.05, y + h * 0.10, x + w * 0.62, y + h * 0.56], fill=(255, 255, 255), outline=INK, width=2)
    d.text((x + w * 0.335, y + h * 0.33), "SCHOOLS SHUT", font=sans(12, "Black"), fill=RED, anchor="mm")
    d.rectangle([x + w * 0.68, y + h * 0.10, x + w * 0.97, y + h * 0.56], fill=NAVY)
    d.text((x + w * 0.825, y + h * 0.33), "UNIONS JOIN", font=sans(8.5, "Bold"),
           fill=(255, 255, 255), anchor="mm")
    for i in range(11):
        hx = x + w * (0.07 + i * 0.088)
        hy = y + h * (0.74 + (i % 3) * 0.07)
        d.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=(60, 60, 66))
        d.rectangle([hx - 6, hy + 5, hx + 6, hy + 12], fill=(60, 60, 66))


ART = {
    "gulf2": art_gulf2, "talks": art_talks, "israel": art_israel,
    "cyclone": art_cyclone, "missile": art_missile, "flood": art_flood,
    "quake": art_quake, "gta": art_gta, "venezuela": art_venezuela,
    "court": art_court, "protest": art_protest,
}

# ------------------------------------------------------------------- map
# Rough continent polygons in normalised map coords (x: lon -180..180,
# y: lat 80..-60). Deliberately simple silhouettes, newspaper-style.

LAND = [
    [(0.02, 0.20), (0.09, 0.09), (0.19, 0.06), (0.26, 0.11), (0.255, 0.21), (0.295, 0.27),
     (0.265, 0.35), (0.215, 0.33), (0.20, 0.41), (0.155, 0.37), (0.125, 0.29), (0.05, 0.29), (0.025, 0.25)],
    [(0.205, 0.44), (0.26, 0.435), (0.30, 0.52), (0.305, 0.65), (0.275, 0.79), (0.25, 0.80),
     (0.232, 0.63), (0.20, 0.53)],
    [(0.435, 0.11), (0.50, 0.065), (0.55, 0.115), (0.545, 0.20), (0.50, 0.245), (0.468, 0.20),
     (0.44, 0.225), (0.428, 0.165)],
    [(0.448, 0.305), (0.52, 0.27), (0.585, 0.30), (0.60, 0.41), (0.568, 0.56), (0.528, 0.685),
     (0.488, 0.66), (0.458, 0.50), (0.44, 0.385)],
    [(0.552, 0.085), (0.70, 0.05), (0.85, 0.075), (0.925, 0.16), (0.885, 0.26), (0.805, 0.295),
     (0.785, 0.40), (0.72, 0.375), (0.70, 0.30), (0.635, 0.335), (0.60, 0.26), (0.562, 0.20)],
    [(0.815, 0.575), (0.90, 0.555), (0.935, 0.635), (0.885, 0.725), (0.828, 0.685), (0.805, 0.615)],
]
ISLANDS = [(0.755, 0.455, 0.016), (0.79, 0.475, 0.013), (0.825, 0.46, 0.012), (0.715, 0.42, 0.010)]

# story number -> (lon, lat)
PINS = {
    1: (50, 26), 2: (31, 50), 3: (35, 32), 4: (-165, -17), 5: (127, 40),
    6: (34, 31), 7: (26, 46), 9: (-67, 10), 10: (95, 22), 11: (2, 49),
    15: (25, 57), 20: (-16, 28), 25: (102, 4), 30: (-150, 64), 36: (-122, 38),
}


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(233, 226, 205))
    for poly in LAND:
        pts = [(x + px * w, y + py * h) for px, py in poly]
        d.polygon(pts, fill=(206, 190, 150), outline=(150, 134, 96))
    for nx, ny, nr in ISLANDS:
        d.ellipse([x + (nx - nr) * w, y + (ny - nr) * h, x + (nx + nr) * w, y + (ny + nr) * h],
                  fill=(206, 190, 150), outline=(150, 134, 96))
    for n, (lon, lat) in PINS.items():
        px = x + (lon + 180) / 360 * w
        py = y + (80 - lat) / 140 * h
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED)
        d.text((px, py), str(n), font=sans(10, "Bold"), fill=(255, 255, 255), anchor="mm")


# ----------------------------------------------------------------- layout

def chip(d, x, y, n, r=11):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=RED)
    d.text((x + r, y + r), str(n), font=sans(13, "Bold"), fill=(255, 255, 255), anchor="mm")


def lead_card(d, x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=LINE)
    ART[s["art"]](d, x + 1, y + 1, w - 2, 92)
    chip(d, x + 8, y + 8, s["n"])
    ty = y + 102
    d.text((x + 12, ty), s["region"], font=sans(11, "Bold"), fill=RED)
    ty += 17
    ty = text_block(d, (x + 12, ty), s["headline"], serif(22, "Bold"), INK, w - 24, 26)
    ty += 3
    text_block(d, (x + 12, ty), s["summary"], sans(14), (52, 50, 44), w - 24, 18)


def small_card(d, x, y, w, h, s):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=LINE)
    ART[s["art"]](d, x + 1, y + 1, w - 2, 50)
    chip(d, x + 6, y + 6, s["n"], r=9)
    ty = y + 58
    d.text((x + 9, ty), s["region"], font=sans(10, "Bold"), fill=RED)
    ty += 14
    ty = text_block(d, (x + 9, ty), s["headline"], serif(15, "Bold"), INK, w - 18, 18)
    ty += 2
    text_block(d, (x + 9, ty), s["summary"], sans(11.5), (52, 50, 44), w - 18, 14.5)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 26

    # top strip
    d.text((M, 14), "THE WORLD'S NEWS IN ONE PICTURE", font=sans(13, "Bold"), fill=RED)
    d.text((W - M, 14), f"{TOTAL} STORIES \u00b7 6 CONTINENTS \u00b7 ALL FROM WEDNESDAY",
           font=sans(13, "Bold"), fill=INK, anchor="ra")
    d.line([M, 38, W - M, 38], fill=INK, width=2)

    # masthead
    d.text((W / 2, 46), "Wednesday 18 November 2026", font=serif(58, "Black"), fill=INK, anchor="ma")
    d.line([M, 124, W - M, 124], fill=INK, width=4)
    d.line([M, 130, W - M, 130], fill=INK, width=1)

    # leads
    lw = (W - 2 * M - 2 * 14) / 3
    for i, s in enumerate(LEADS):
        lead_card(d, M + i * (lw + 14), 142, lw, 232, s)

    # small cards, 2 rows of 4
    cw = (W - 2 * M - 3 * 12) / 4
    for i, s in enumerate(CARDS):
        cx = M + (i % 4) * (cw + 12)
        cy = 386 + (i // 4) * (164 + 10)
        small_card(d, cx, cy, cw, 164, s)

    # bottom: map + also list
    by = 742
    d.text((M, by), "WHERE IT HAPPENED", font=sans(13, "Bold"), fill=INK)
    draw_map(d, M, by + 22, 446, 196)
    d.text((M, by + 224), "Pins: stories 1\u201311, 15, 20, 25, 30 and 36 \u00b7 not to scale",
           font=sans(10), fill=FAINT)

    ax = M + 446 + 24
    d.text((ax, by), "ALSO ON WEDNESDAY 18 NOVEMBER", font=sans(13, "Bold"), fill=INK)
    col_w = (W - M - ax - 16) / 2
    half = (len(ALSO) + 1) // 2
    f = sans(11.5)
    lead = 214 / half
    for j, item in enumerate(ALSO):
        col = 0 if j < half else 1
        row = j if col == 0 else j - half
        ix = ax + col * (col_w + 16)
        iy = by + 24 + row * lead
        n = len(LEADS) + len(CARDS) + j + 1
        d.ellipse([ix, iy + 1, ix + 15, iy + 16], fill=TEAL if col == 0 else NAVY)
        d.text((ix + 7.5, iy + 8.5), str(n), font=sans(9, "Bold"), fill=(255, 255, 255), anchor="mm")
        t = item
        while d.textlength(t, font=f) > col_w - 22 and len(t) > 8:
            t = t[:-1]
        if t != item:
            t = t.rstrip(" ,;") + "\u2026"
        d.text((ix + 20, iy + 1), t, font=f, fill=(40, 38, 34))

    # footer
    d.line([M, 986, W - M, 986], fill=INK, width=2)
    d.text((M, 992), "Every story happened or was first reported on Wednesday 18 November 2026. "
                     "Contested claims are marked as claims.",
           font=sans(10.5), fill=(52, 50, 44))
    d.text((W - M, 992), "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 Al Jazeera \u00b7 UN \u00b7 WFP",
           font=sans(10.5), fill=(52, 50, 44), anchor="ra")
    return img


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    im = build()
    im.save(out, optimize=True)
    print("saved", out, im.size)

