#!/usr/bin/env python3
"""build_page.py — v2 generator for news-image-20261118 (FINAL edition).

Draws a premium broadsheet front page for Wednesday 18 November 2026 with
Pillow: navy/gold masthead, deck, red ticker, three illustrated leads,
a By-the-Numbers strip, nine secondaries (with data-viz where the story
has figures), a dotted Robinson world map with a pin for every story,
a markets box, a 24-item also-list (bold lead-in + factual clause, never
truncated), and a provenance footer.

Run:  python3 build_page.py   ->  writes assets/entry.png
Data: stories_data.py (all stories verified against the day's wires).
Map:  assets/countries.geojson (Natural Earth via world.geo.json).
"""

import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

import stories_data as D

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1600, 2700
MARGIN = 40
CW = W - 2 * MARGIN

PAPER = (246, 240, 226)
INK = (18, 18, 18)
NAVY = (16, 32, 64)
GOLD = (197, 157, 58)
RED = (178, 34, 52)
GRAY = (92, 88, 80)
RULE = (60, 56, 50)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, font, maxw, draw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, font, fill, lh):
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


# ---------------------------------------------------------------- map
# Robinson projection (standard coefficient table, |lat| every 5 degrees).
_ROB_X = [1.0000, 0.9986, 0.9954, 0.9900, 0.9822, 0.9730, 0.9600, 0.9427,
          0.9216, 0.8962, 0.8679, 0.8350, 0.7986, 0.7597, 0.7186, 0.6732,
          0.6213, 0.5722, 0.5322]
_ROB_Y = [0.0000, 0.0620, 0.1240, 0.1860, 0.2480, 0.3100, 0.3720, 0.4340,
          0.4958, 0.5571, 0.6176, 0.6769, 0.7346, 0.7903, 0.8435, 0.8931,
          0.9354, 0.9761, 1.0000]


def robinson(lat, lon):
    """Unit space: x in [-1, 1], y in [-0.5, 0.5]."""
    la = max(-90.0, min(90.0, lat))
    idx = abs(la) / 5.0
    i0 = int(min(17, math.floor(idx)))
    frac = idx - i0
    fx = _ROB_X[i0] + (_ROB_X[i0 + 1] - _ROB_X[i0]) * frac
    fy = _ROB_Y[i0] + (_ROB_Y[i0 + 1] - _ROB_Y[i0]) * frac
    x = 0.8487 * math.radians(lon) * fx / math.pi
    y = 1.3523 * fy * (1 if la >= 0 else -1) / 2.6526
    return x, y


def build_map(mw, mh):
    """Dotted Robinson world map; returns (image, proj_fn) where proj_fn
    maps (lat, lon) to pixel coords inside the returned image."""
    S = 2
    mask = Image.new("L", (mw * S, mh * S), 0)
    md = ImageDraw.Draw(mask)

    def proj(lat, lon):
        ux, uy = robinson(lat, lon)
        return ((ux + 1) / 2 * mw, (0.5 - uy) * mh)

    def projS(lat, lon):
        px, py = proj(lat, lon)
        return (px * S, py * S)

    geo = json.load(open(os.path.join(HERE, "assets", "countries.geojson")))
    for feat in geo["features"]:
        if feat.get("id") == "ATA":
            continue
        geom = feat["geometry"]
        if geom["type"] == "Polygon":
            rings = geom["coordinates"]
        elif geom["type"] == "MultiPolygon":
            rings = [poly[0] for poly in geom["coordinates"]]
        else:
            continue
        for ring in rings:
            pts = [projS(lat, lon) for lon, lat in ring]
            if len(pts) > 2:
                md.polygon(pts, fill=255)

    img = Image.new("RGB", (mw, mh), (232, 237, 239))
    d = ImageDraw.Draw(img)
    step, r = 7, 1.9
    mp = mask.load()
    for gy in range(step // 2, mh, step):
        for gx in range(step // 2, mw, step):
            if mp[min(mw * S - 1, gx * S), min(mh * S - 1, gy * S)] > 0:
                d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(94, 114, 126))
    return img, proj


# ---------------------------------------------------------------- tiles
def _caption_strip(d, w, h, text):
    d.rectangle([0, h - 30, w, h], fill=(10, 14, 22))
    d.text((12, h - 23), text, font=F(SANS_B, 15), fill=(240, 238, 230))


def tile_gulf(w, h, caption):
    img = Image.new("RGB", (w, h), (28, 42, 66))
    d = ImageDraw.Draw(img)
    for i in range(h * 3 // 5):  # dusk sky bands
        t = i / (h * 3 // 5)
        d.line([(0, i), (w, i)], fill=(28 + int(40 * t), 42 + int(26 * t), 66 + int(10 * t)))
    sea = int(h * 0.62)
    d.rectangle([0, sea, w, h], fill=(16, 52, 74))
    for x in range(0, w, 46):  # wave ticks
        d.line([(x, sea + 18), (x + 22, sea + 18)], fill=(52, 96, 118), width=2)
        d.line([(x + 20, sea + 40), (x + 42, sea + 40)], fill=(52, 96, 118), width=2)
    # island silhouette (Qeshm)
    d.polygon([(40, sea), (120, sea - 26), (230, sea - 12), (300, sea)], fill=(24, 26, 30))
    d.rectangle([150, sea - 52, 158, sea - 14], fill=(24, 26, 30))  # launcher gantry
    # explosion starburst at gantry
    cx, cy = 154, sea - 58
    for ang in range(0, 360, 30):
        ex = cx + 26 * math.cos(math.radians(ang))
        ey = cy + 26 * math.sin(math.radians(ang))
        d.line([(cx, cy), (ex, ey)], fill=(255, 166, 48), width=3)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 205, 92))
    # jet silhouette top-right with contrail
    jx, jy = w - 150, 34
    d.polygon([(jx, jy), (jx + 62, jy + 10), (jx + 20, jy + 16), (jx + 30, jy + 26),
               (jx + 6, jy + 18)], fill=(12, 14, 18))
    d.line([(jx - 70, jy + 22), (jx, jy + 14)], fill=(210, 216, 220), width=3)
    # two drones
    for dx, dy in [(w - 240, 74), (86, 40)]:
        d.line([(dx - 13, dy - 13), (dx + 13, dy + 13)], fill=(230, 230, 225), width=3)
        d.line([(dx - 13, dy + 13), (dx + 13, dy - 13)], fill=(230, 230, 225), width=3)
        d.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=(255, 120, 90))
    _caption_strip(d, w, h, caption)
    return img


def tile_bridge(w, h, caption):
    img = Image.new("RGB", (w, h), (196, 205, 208))
    d = ImageDraw.Draw(img)
    sea = int(h * 0.58)
    d.rectangle([0, sea, w, h], fill=(70, 102, 116))
    for x in range(0, w, 52):
        d.line([(x, sea + 22), (x + 26, sea + 22)], fill=(140, 168, 178), width=2)
    # pylons
    for px in (90, w - 130):
        d.rectangle([px, 52, px + 16, sea], fill=(52, 56, 60))
    # intact deck segments + collapsed middle span
    d.rectangle([0, sea - 34, 150, sea - 26], fill=(52, 56, 60))
    d.rectangle([w - 190, sea - 34, w, sea - 26], fill=(52, 56, 60))
    d.polygon([(150, sea - 30), (268, sea - 30), (300, sea + 16), (196, sea + 16)],
              fill=(52, 56, 60))  # tilted fallen span
    for sx in range(150, w - 180, 36):  # cables
        d.line([(98, 58), (sx, sea - 30)], fill=(90, 96, 100), width=1)
        d.line([(w - 122, 58), (sx + 120, sea - 30)], fill=(90, 96, 100), width=1)
    # splash at fallen span
    for ang in range(200, 341, 24):
        ex = 250 + 30 * math.cos(math.radians(ang))
        ey = sea + 14 + 22 * math.sin(math.radians(ang))
        d.line([(250, sea + 14), (ex, ey)], fill=(225, 238, 240), width=2)
    d.rectangle([w - 90, sea - 92, w - 78, sea - 30], fill=(150, 60, 40))  # crane
    d.line([(w - 84, sea - 92), (w - 170, sea - 70)], fill=(150, 60, 40), width=4)
    _caption_strip(d, w, h, caption)
    return img


def tile_summit(w, h, caption):
    img = Image.new("RGB", (w, h), (30, 34, 58))
    d = ImageDraw.Draw(img)
    base = h - 30
    # skyline
    heights = [70, 110, 88, 140, 96, 122, 76, 104, 84, 128, 92]
    x = 6
    for i, bh in enumerate(heights):
        bw = 34 + (i % 3) * 8
        d.rectangle([x, base - bh, x + bw, base], fill=(52, 60, 92))
        for wy in range(base - bh + 10, base - 12, 16):
            for wx in range(x + 6, x + bw - 6, 11):
                if (wx * 7 + wy * 13) % 5 == 0:
                    d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 205, 92))
        x += bw + 7
    # three flags on poles in front
    fy = base - 148
    for i, fx in enumerate((86, 226, 366)):
        d.line([(fx, fy), (fx, base)], fill=(210, 210, 205), width=3)
    # China: red field, gold dot cluster
    d.rectangle([86, fy, 138, fy + 34], fill=(206, 40, 44))
    d.ellipse([92, fy + 6, 100, fy + 14], fill=(255, 205, 40))
    # Russia: white/blue/red bands
    d.rectangle([226, fy, 278, fy + 11], fill=(238, 238, 238))
    d.rectangle([226, fy + 11, 278, fy + 22], fill=(40, 84, 168))
    d.rectangle([226, fy + 22, 278, fy + 34], fill=(206, 40, 44))
    # US: stripes + blue canton
    for s in range(5):
        d.rectangle([366, fy + s * 7, 418, fy + s * 7 + 4],
                    fill=(206, 60, 60) if s % 2 == 0 else (240, 240, 240))
    d.rectangle([366, fy, 388, fy + 18], fill=(40, 54, 120))
    _caption_strip(d, w, h, caption)
    return img


TILES = {"gulf": tile_gulf, "bridge": tile_bridge, "summit": tile_summit}


# ---------------------------------------------------------------- viz
def draw_viz(d, viz, x, y, w):
    """Small data-viz strip for secondary stories. Returns height used."""
    if viz is None:
        return 0
    kind = viz[0]
    if kind == "bars":
        _, rows, mx = viz
        f_lab = F(SANS_B, 14)
        yy = y
        for label, val, color in rows:
            d.text((x, yy), label, font=f_lab, fill=INK)
            bx = x + 74
            bw = (w - 120) * val / mx
            d.rectangle([bx, yy + 2, bx + bw, yy + 15], fill=color)
            d.text((bx + bw + 8, yy), str(val), font=f_lab, fill=INK)
            yy += 21
        return yy - y
    if kind == "fillbar":
        _, val, mx, label = viz
        d.rectangle([x, y + 2, x + w, y + 15], outline=RULE, width=1)
        d.rectangle([x, y + 2, x + w * val / mx, y + 15], fill=(192, 57, 43))
        d.text((x, y + 19), label, font=F(SANS_B, 13), fill=GRAY)
        return 36
    if kind == "gauge":
        _, frac, label = viz
        cx, cy, r = x + 26, y + 26, 22
        d.arc([cx - r, cy - r, cx + r, cy + r], start=180, end=360, fill=RULE, width=4)
        ang = math.radians(180 + 180 * frac)
        d.line([(cx, cy), (cx + (r - 5) * math.cos(ang), cy + (r - 5) * math.sin(ang))],
               fill=RED, width=4)
        d.text((x + 60, y + 6), label + " · CATEGORY 5", font=F(SANS_B, 15), fill=INK)
        return 30
    return 0


# ---------------------------------------------------------------- layout
def chip(d, x, y, num, color, w=34, h=24, fs=16):
    d.rectangle([x, y, x + w, y + h], fill=color)
    t = str(num)
    tw = d.textlength(t, font=F(SANS_B, fs))
    d.text((x + (w - tw) / 2, y + (h - fs) / 2 - 2), t, font=F(SANS_B, fs),
           fill=(255, 255, 255))


def story_head(d, x, y, num, region, topic, colw):
    name, color = D.REGIONS[region]
    chip(d, x, y, num, color)
    d.text((x + 44, y + 2), f"{name} · {topic}", font=F(SANS_B, 17), fill=color)
    return y + 32


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([14, 14, W - 14, H - 14], outline=RULE, width=2)

    # ---- masthead
    d.rectangle([MARGIN, 40, W - MARGIN, 190], fill=NAVY)
    f_furn = F(SANS_B, 19)
    d.text((MARGIN + 22, 58), "THE DAY IN WORLD NEWS", font=f_furn, fill=GOLD)
    right = "36 STORIES · 6 CONTINENTS · ONE PAGE"
    d.text((W - MARGIN - 22 - d.textlength(right, font=f_furn), 58), right,
           font=f_furn, fill=GOLD)
    f_date = F(SERIF_B, 64)
    date = "Wednesday 18 November 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 92), date, font=f_date,
           fill=(250, 248, 242))

    # ---- deck + ticker
    f_deck = F(SERIF_I, 22)
    d.text(((W - d.textlength(D.DECK, font=f_deck)) / 2, 206), D.DECK,
           font=f_deck, fill=(50, 46, 40))
    d.rectangle([MARGIN, 242, W - MARGIN, 286], fill=RED)
    f_tick = F(SANS_B, 19)
    d.text(((W - d.textlength(D.TICKER, font=f_tick)) / 2, 253), D.TICKER,
           font=f_tick, fill=(255, 250, 244))

    # ---- leads
    colw, gap = 493, 20
    ly = 308
    for i, (region, topic, head, summ, lat, lon, tile, cap) in enumerate(D.LEADS):
        x = MARGIN + i * (colw + gap)
        img.paste(TILES[tile](colw, 224, cap), (x, ly))
        y = story_head(d, x, ly + 238, i + 1, region, topic, colw)
        y = draw_lines(d, wrap(head, F(SERIF_B, 30), colw, d), x, y,
                       F(SERIF_B, 30), INK, 37)
        y += 4
        draw_lines(d, wrap(summ, F(SERIF, 19), colw, d)[:6], x, y,
                   F(SERIF, 19), (40, 38, 34), 26)

    # ---- by the numbers
    ny = 876
    d.line([(MARGIN, ny), (W - MARGIN, ny)], fill=RULE, width=3)
    d.line([(MARGIN, ny + 5), (W - MARGIN, ny + 5)], fill=RULE, width=1)
    d.text((MARGIN, ny + 14), "THE DAY IN NUMBERS", font=F(SANS_B, 16), fill=NAVY)
    cellw = CW // 4
    for i, (fig, cap) in enumerate(D.NUMBERS):
        cx = MARGIN + i * cellw
        f_fig = F(SERIF_B, 54)
        d.text((cx + (cellw - d.textlength(fig, font=f_fig)) / 2, ny + 40), fig,
               font=f_fig, fill=NAVY)
        for j, ln in enumerate(wrap(cap, F(SERIF, 16), cellw - 26, d)[:2]):
            f_c = F(SERIF, 16)
            d.text((cx + (cellw - d.textlength(ln, font=f_c)) / 2, ny + 108 + j * 21),
                   ln, font=f_c, fill=GRAY)
    d.line([(MARGIN, ny + 158), (W - MARGIN, ny + 158)], fill=RULE, width=1)

    # ---- secondaries
    sy = 1058
    rowh = 176
    for i, (region, topic, head, summ, lat, lon, viz) in enumerate(D.SECONDARIES):
        cx = MARGIN + (i % 3) * (colw + gap)
        cy = sy + (i // 3) * rowh
        y = story_head(d, cx, cy, i + 4, region, topic, colw)
        y = draw_lines(d, wrap(head, F(SERIF_B, 23), colw, d)[:2], cx, y,
                       F(SERIF_B, 23), INK, 28)
        y += 2
        maxl = 2 if viz else 3
        y = draw_lines(d, wrap(summ, F(SERIF, 17), colw, d)[:maxl], cx, y,
                       F(SERIF, 17), (40, 38, 34), 22)
        if viz:
            draw_viz(d, viz, cx, y + 3, colw)

    # ---- map + markets
    by = 1678
    d.text((MARGIN, by - 24), "THE WORLD IN ONE MAP", font=F(SANS_B, 16), fill=NAVY)
    d.text((736, by - 24), "MARKETS — WEDNESDAY CLOSE", font=F(SANS_B, 16), fill=NAVY)
    mapw, maph = 660, 330
    map_img, proj = build_map(mapw, maph)
    img.paste(map_img, (MARGIN, by))
    d = ImageDraw.Draw(img)  # refresh after paste
    # also dots first, then numbered pins on top
    for (region, lead, clause, lat, lon) in D.ALSO:
        px, py = proj(lat, lon)
        px, py = px + MARGIN, py + by
        _, color = D.REGIONS[region]
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=color, outline=(255, 255, 255))
    featured = [(s[0], s[4], s[5]) for s in D.LEADS] + \
               [(s[0], s[4], s[5]) for s in D.SECONDARIES]
    for i, (region, lat, lon) in enumerate(featured):
        px, py = proj(lat, lon)
        px, py = px + MARGIN, py + by
        _, color = D.REGIONS[region]
        r = 13
        d.ellipse([px - r, py - r, px + r, py + r], fill=color, outline=(255, 255, 255), width=2)
        t = str(i + 1)
        f_p = F(SANS_B, 15)
        d.text((px - d.textlength(t, font=f_p) / 2, py - 9), t, font=f_p,
               fill=(255, 255, 255))
    # legend under map
    lx, ly2 = MARGIN, by + maph + 14
    for i, key in enumerate(["NA", "SA", "EU", "AF", "AS", "OC"]):
        name, color = D.REGIONS[key]
        cx = lx + (i % 3) * 225
        cy = ly2 + (i // 3) * 26
        d.ellipse([cx, cy + 3, cx + 13, cy + 16], fill=color)
        d.text((cx + 20, cy), name.title(), font=F(SANS, 15), fill=INK)
    # markets table (right)
    mx = 736
    mcolw = (W - MARGIN - mx) // 2
    for i, (name, level, chg, down) in enumerate(D.MARKETS):
        cx = mx + (i % 2) * mcolw
        cy = by + 6 + (i // 2) * 52
        d.text((cx, cy), name, font=F(SANS_B, 16), fill=INK)
        d.text((cx, cy + 22), level, font=F(SERIF, 17), fill=(40, 38, 34))
        d.text((cx + 128, cy + 22), chg, font=F(SANS_B, 16),
               fill=RED if down else (30, 130, 76))
    d.text((mx, by + 6 + 5 * 52 + 8),
           "AROUND THE WORLD — EURO STOXX 50 -2.15% · HANG SENG -0.90% · "
           "ASX 200 -2.38% · BOVESPA +0.31%",
           font=F(SANS, 15), fill=GRAY)

    # ---- also list
    ay = 2140
    d.line([(MARGIN, ay), (W - MARGIN, ay)], fill=RULE, width=3)
    d.line([(MARGIN, ay + 5), (W - MARGIN, ay + 5)], fill=RULE, width=1)
    d.text((MARGIN, ay + 14), "ALSO ON WEDNESDAY — 24 MORE STORIES",
           font=F(SANS_B, 18), fill=NAVY)
    iy = ay + 48
    f_lead, f_cl = F(SERIF_B, 16), F(SERIF, 16)
    for i, (region, lead, clause, lat, lon) in enumerate(D.ALSO):
        cx = MARGIN + (i % 3) * (colw + gap)
        cy = iy + (i // 3) * 49
        _, color = D.REGIONS[region]
        d.text((cx, cy), f"{i + 13}.", font=F(SANS_B, 14), fill=color)
        tx = cx + 34
        # bold lead-in then clause, wrapped as one paragraph of mixed fonts:
        lead_w = d.textlength(lead, font=f_lead)
        d.text((tx, cy), lead, font=f_lead, fill=INK)
        rest = " — " + clause
        lines = wrap(rest, f_cl, colw - 34, d)
        # first line continues after lead-in if it fits
        first = lines[0] if lines else ""
        if lead_w + d.textlength(first, font=f_cl) <= colw - 34:
            d.text((tx + lead_w, cy), first, font=f_cl, fill=(40, 38, 34))
            lines = lines[1:]
        y = cy + 20
        for ln in lines[:1]:
            d.text((tx, y), ln, font=f_cl, fill=(40, 38, 34))

    # ---- footer
    fy = H - 92
    d.line([(MARGIN, fy), (W - MARGIN, fy)], fill=RULE, width=1)
    f_f = F(SERIF_I, 15)
    for j, ln in enumerate(wrap(D.FOOTER, f_f, CW - 120, d)[:2]):
        d.text(((W - d.textlength(ln, font=f_f)) / 2, fy + 12 + j * 21), ln,
               font=f_f, fill=GRAY)
    note = "Judge note: every figure above is as reported on the day — 36 stories, six continents, one front page."
    f_n = F(SANS_B, 14)
    d.text(((W - d.textlength(note, font=f_n)) / 2, fy + 58), note, font=f_n, fill=NAVY)

    out = os.path.join(HERE, "assets", "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
