#!/usr/bin/env python3
"""build_page.py — v3 generator for news-image-20261118 (FINAL edition).

Competition gate: the image must be at most 1024x1024 px and 1 MiB, so this
edition is typeset for exactly 1024x1024 — the same canvas every winner
uses. Premium broadsheet front page for Wednesday 18 November 2026:
navy/gold masthead, deck, red ticker, three illustrated leads, a
Day-in-Numbers line, nine secondaries with mini data-viz, a dotted
Robinson world map with a pin for every story, a markets box, a 21-item
also-list (bold lead-in + factual clause, never truncated) and a
provenance footer.

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
W = H = 1024
MARGIN = 24
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
    """Dotted Robinson world map; returns (image, proj_fn)."""
    S = 3
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
    step, r = 4.4, 1.25
    mp = mask.load()
    gy = step / 2
    while gy < mh:
        gx = step / 2
        while gx < mw:
            if mp[min(mw * S - 1, int(gx * S)), min(mh * S - 1, int(gy * S))] > 0:
                d.ellipse([gx - r, gy - r, gx + r, gy + r], fill=(94, 114, 126))
            gx += step
        gy += step
    return img, proj


# ---------------------------------------------------------------- tiles
def _caption_strip(d, w, h, text):
    d.rectangle([0, h - 20, w, h], fill=(10, 14, 22))
    d.text((8, h - 15), text, font=F(SANS_B, 10), fill=(240, 238, 230))


def tile_gulf(w, h, caption):
    img = Image.new("RGB", (w, h), (28, 42, 66))
    d = ImageDraw.Draw(img)
    skyh = int(h * 0.6)
    for i in range(skyh):
        t = i / max(1, skyh)
        d.line([(0, i), (w, i)], fill=(28 + int(40 * t), 42 + int(26 * t), 66 + int(10 * t)))
    sea = skyh
    d.rectangle([0, sea, w, h], fill=(16, 52, 74))
    for x in range(0, w, 30):
        d.line([(x, sea + 10), (x + 14, sea + 10)], fill=(52, 96, 118), width=1)
        d.line([(x + 13, sea + 24), (x + 27, sea + 24)], fill=(52, 96, 118), width=1)
    d.polygon([(26, sea), (78, sea - 15), (150, sea - 7), (196, sea)], fill=(24, 26, 30))
    d.rectangle([98, sea - 30, 103, sea - 8], fill=(24, 26, 30))
    cx, cy = 100, sea - 34
    for ang in range(0, 360, 30):
        ex = cx + 15 * math.cos(math.radians(ang))
        ey = cy + 15 * math.sin(math.radians(ang))
        d.line([(cx, cy), (ex, ey)], fill=(255, 166, 48), width=2)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 205, 92))
    jx, jy = w - 96, 16
    d.polygon([(jx, jy), (jx + 40, jy + 6), (jx + 13, jy + 10), (jx + 19, jy + 17),
               (jx + 4, jy + 11)], fill=(12, 14, 18))
    d.line([(jx - 44, jy + 14), (jx, jy + 9)], fill=(210, 216, 220), width=2)
    for dx, dy in [(w - 150, 42), (54, 22)]:
        d.line([(dx - 8, dy - 8), (dx + 8, dy + 8)], fill=(230, 230, 225), width=2)
        d.line([(dx - 8, dy + 8), (dx + 8, dy - 8)], fill=(230, 230, 225), width=2)
        d.ellipse([dx - 2.5, dy - 2.5, dx + 2.5, dy + 2.5], fill=(255, 120, 90))
    _caption_strip(d, w, h, caption)
    return img


def tile_bridge(w, h, caption):
    img = Image.new("RGB", (w, h), (196, 205, 208))
    d = ImageDraw.Draw(img)
    sea = int(h * 0.58)
    d.rectangle([0, sea, w, h], fill=(70, 102, 116))
    for x in range(0, w, 34):
        d.line([(x, sea + 13), (x + 17, sea + 13)], fill=(140, 168, 178), width=1)
    for px in (58, w - 84):
        d.rectangle([px, 30, px + 10, sea], fill=(52, 56, 60))
    d.rectangle([0, sea - 20, 96, sea - 15], fill=(52, 56, 60))
    d.rectangle([w - 122, sea - 20, w, sea - 15], fill=(52, 56, 60))
    d.polygon([(96, sea - 18), (172, sea - 18), (192, sea + 9), (125, sea + 9)],
              fill=(52, 56, 60))
    for sx in range(96, w - 116, 24):
        d.line([(63, 34), (sx, sea - 18)], fill=(90, 96, 100), width=1)
        d.line([(w - 79, 34), (sx + 76, sea - 18)], fill=(90, 96, 100), width=1)
    for ang in range(200, 341, 28):
        ex = 160 + 19 * math.cos(math.radians(ang))
        ey = sea + 8 + 13 * math.sin(math.radians(ang))
        d.line([(160, sea + 8), (ex, ey)], fill=(225, 238, 240), width=1)
    d.rectangle([w - 58, sea - 54, w - 50, sea - 18], fill=(150, 60, 40))
    d.line([(w - 54, sea - 54), (w - 108, sea - 41)], fill=(150, 60, 40), width=3)
    _caption_strip(d, w, h, caption)
    return img


def tile_summit(w, h, caption):
    img = Image.new("RGB", (w, h), (30, 34, 58))
    d = ImageDraw.Draw(img)
    base = h - 20
    heights = [42, 66, 52, 84, 58, 74, 46, 62, 50, 78, 56]
    x = 4
    for i, bh in enumerate(heights):
        bw = 22 + (i % 3) * 5
        d.rectangle([x, base - bh, x + bw, base], fill=(52, 60, 92))
        for wy in range(base - bh + 6, base - 7, 10):
            for wx in range(x + 4, x + bw - 4, 7):
                if (wx * 7 + wy * 13) % 5 == 0:
                    d.rectangle([wx, wy, wx + 2.5, wy + 3.5], fill=(255, 205, 92))
        x += bw + 5
    fy = base - 88
    fw = int(w * 0.115)
    for i, fx in enumerate((int(w * 0.17), int(w * 0.455), int(w * 0.74))):
        d.line([(fx, fy), (fx, base)], fill=(210, 210, 205), width=2)
        if i == 0:
            d.rectangle([fx, fy, fx + fw, fy + int(fw * 0.65)], fill=(206, 40, 44))
            d.ellipse([fx + 4, fy + 4, fx + 9, fy + 9], fill=(255, 205, 40))
        elif i == 1:
            fh = int(fw * 0.65)
            d.rectangle([fx, fy, fx + fw, fy + fh // 3], fill=(238, 238, 238))
            d.rectangle([fx, fy + fh // 3, fx + fw, fy + 2 * fh // 3], fill=(40, 84, 168))
            d.rectangle([fx, fy + 2 * fh // 3, fx + fw, fy + fh], fill=(206, 40, 44))
        else:
            fh = int(fw * 0.65)
            for sidx in range(5):
                d.rectangle([fx, fy + sidx * fh // 5, fx + fw, fy + (sidx + 1) * fh // 5],
                            fill=(206, 60, 60) if sidx % 2 == 0 else (240, 240, 240))
            d.rectangle([fx, fy, fx + fw * 0.42, fy + fh * 0.55], fill=(40, 54, 120))
    _caption_strip(d, w, h, caption)
    return img


TILES = {"gulf": tile_gulf, "bridge": tile_bridge, "summit": tile_summit}


# ---------------------------------------------------------------- viz
def draw_viz(d, viz, x, y, w):
    if viz is None:
        return 0
    kind = viz[0]
    if kind == "bars":
        _, rows, mx = viz
        f_lab = F(SANS_B, 9)
        yy = y
        for label, val, color in rows:
            d.text((x, yy), label, font=f_lab, fill=INK)
            bx = x + 30
            bw = (w - 52) * val / mx
            d.rectangle([bx, yy + 1, bx + bw, yy + 8], fill=color)
            d.text((bx + bw + 5, yy), str(val), font=f_lab, fill=INK)
            yy += 11
        return yy - y
    if kind == "fillbar":
        _, val, mx, label = viz
        tw = w - 72
        d.rectangle([x, y + 1, x + tw, y + 8], outline=RULE, width=1)
        d.rectangle([x, y + 1, x + tw * val / mx, y + 8], fill=(192, 57, 43))
        d.text((x + tw + 6, y), label, font=F(SANS_B, 9), fill=INK)
        return 11
    if kind == "gauge":
        _, frac, label = viz
        cx, cy, r = x + 12, y + 12, 11
        d.arc([cx - r, cy - r, cx + r, cy + r], start=180, end=360, fill=RULE, width=3)
        ang = math.radians(180 + 180 * frac)
        d.line([(cx, cy), (cx + (r - 3) * math.cos(ang), cy + (r - 3) * math.sin(ang))],
               fill=RED, width=3)
        d.text((x + 30, y + 2), label + " · CATEGORY 5", font=F(SANS_B, 10), fill=INK)
        return 14
    return 0


# ---------------------------------------------------------------- layout
def chip(d, x, y, num, color, w=26, h=18, fs=11):
    d.rectangle([x, y, x + w, y + h], fill=color)
    t = str(num)
    f = F(SANS_B, fs)
    d.text((x + (w - d.textlength(t, font=f)) / 2, y + (h - fs) / 2 - 1.5), t,
           font=f, fill=(255, 255, 255))


def story_head(d, x, y, num, region, topic, big=False):
    name, color = D.REGIONS[region]
    if big:
        chip(d, x, y, num, color, 26, 18, 11)
        d.text((x + 34, y + 2), f"{name} · {topic}", font=F(SANS_B, 11), fill=color)
        return y + 24
    chip(d, x, y, num, color, 22, 15, 10)
    d.text((x + 28, y + 1), f"{name} · {topic}", font=F(SANS_B, 10), fill=color)
    return y + 19


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 10, H - 10], outline=RULE, width=2)

    # ---- masthead
    d.rectangle([MARGIN, 24, W - MARGIN, 100], fill=NAVY)
    f_furn = F(SANS_B, 11)
    d.text((MARGIN + 14, 33), "THE DAY IN WORLD NEWS", font=f_furn, fill=GOLD)
    right = "33 STORIES · 6 CONTINENTS · ONE PAGE"
    d.text((W - MARGIN - 14 - d.textlength(right, font=f_furn), 33), right,
           font=f_furn, fill=GOLD)
    f_date = F(SERIF_B, 37)
    date = "Wednesday 18 November 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 50), date, font=f_date,
           fill=(250, 248, 242))

    # ---- deck + ticker
    f_deck = F(SERIF_I, 12)
    d.text(((W - d.textlength(D.DECK, font=f_deck)) / 2, 107), D.DECK,
           font=f_deck, fill=(50, 46, 40))
    d.rectangle([MARGIN, 126, W - MARGIN, 148], fill=RED)
    f_tick = F(SANS_B, 12)
    d.text(((W - d.textlength(D.TICKER, font=f_tick)) / 2, 131), D.TICKER,
           font=f_tick, fill=(255, 250, 244))

    # ---- leads
    colw, gap = 317, 12
    xs = [MARGIN + i * (colw + gap) for i in range(3)]
    ly = 158
    for i, (region, topic, head, summ, lat, lon, tile, cap) in enumerate(D.LEADS):
        x = xs[i]
        img.paste(TILES[tile](colw, 106, cap), (x, ly))
        y = story_head(d, x, ly + 112, i + 1, region, topic, big=True)
        y = draw_lines(d, wrap(head, F(SERIF_B, 17), colw, d)[:3], x, y,
                       F(SERIF_B, 17), INK, 20)
        y += 2
        draw_lines(d, wrap(summ, F(SERIF, 10), colw, d)[:5], x, y,
                   F(SERIF, 10), (40, 38, 34), 13.5)

    # ---- day in numbers (one line)
    ny = 414
    d.line([(MARGIN, ny), (W - MARGIN, ny)], fill=RULE, width=2)
    f_lab, f_fig = F(SANS_B, 11), F(SERIF_B, 13)
    parts = ["THE DAY IN NUMBERS —  ", "66 of 120", " Kahana votes  ·  ",
             "$130bn", " Nvidia guide  ·  ", "315 km/h", " Xavier gusts  ·  ",
             "11,000+", " Ebola cases"]
    widths = [d.textlength(p, font=f_lab if j % 2 == 0 and j == 0 else f_fig if j % 2 == 1 else f_lab)
              for j, p in enumerate(parts)]
    total = sum(widths)
    x = (W - total) / 2
    for j, p in enumerate(parts):
        fnt = f_fig if j % 2 == 1 else f_lab
        d.text((x, ny + 7), p, font=fnt, fill=NAVY if j % 2 == 1 or j == 0 else GRAY)
        x += widths[j]
    d.line([(MARGIN, ny + 28), (W - MARGIN, ny + 28)], fill=RULE, width=1)

    # ---- secondaries
    sy = 452
    rowh = 70
    for i, (region, topic, head, summ, lat, lon, viz) in enumerate(D.SECONDARIES):
        cx = xs[i % 3]
        cy = sy + (i // 3) * rowh
        y = story_head(d, cx, cy, i + 4, region, topic)
        y = draw_lines(d, wrap(head, F(SERIF_B, 13), colw, d)[:2], cx, y,
                       F(SERIF_B, 13), INK, 16)
        y += 1
        maxl = 1 if viz else 2
        y = draw_lines(d, wrap(summ, F(SERIF, 10), colw, d)[:maxl], cx, y,
                       F(SERIF, 10), (40, 38, 34), 12.5)
        if viz:
            draw_viz(d, viz, cx, y + 2, colw)

    # ---- map + markets
    by = 672
    d.text((MARGIN, by), "THE WORLD IN ONE MAP", font=F(SANS_B, 10), fill=NAVY)
    d.text((492, by), "MARKETS — WEDNESDAY CLOSE", font=F(SANS_B, 10), fill=NAVY)
    mapw, maph = 452, 132
    map_img, proj = build_map(mapw, maph)
    img.paste(map_img, (MARGIN, by + 16))
    d = ImageDraw.Draw(img)
    for (region, lead, clause, lat, lon) in D.ALSO:
        px, py = proj(lat, lon)
        px, py = px + MARGIN, py + by + 16
        _, color = D.REGIONS[region]
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=color, outline=(255, 255, 255))
    featured = [(s[0], s[4], s[5]) for s in D.LEADS] + \
               [(s[0], s[4], s[5]) for s in D.SECONDARIES]
    for i, (region, lat, lon) in enumerate(featured):
        px, py = proj(lat, lon)
        px, py = px + MARGIN, py + by + 16
        _, color = D.REGIONS[region]
        r = 8
        d.ellipse([px - r, py - r, px + r, py + r], fill=color, outline=(255, 255, 255), width=1)
        t = str(i + 1)
        f_p = F(SANS_B, 9)
        d.text((px - d.textlength(t, font=f_p) / 2, py - 5.5), t, font=f_p,
               fill=(255, 255, 255))
    lx, ly2 = MARGIN, by + 16 + maph + 6
    for i, key in enumerate(["NA", "SA", "EU", "AF", "AS", "OC"]):
        name, color = D.REGIONS[key]
        cx = lx + (i % 3) * 152
        cy = ly2 + (i // 3) * 14
        d.ellipse([cx, cy + 2, cx + 8, cy + 10], fill=color)
        d.text((cx + 12, cy), name.title(), font=F(SANS, 9), fill=INK)
    mx = 492
    mcolw = (W - MARGIN - mx) // 2
    for i, (name, level, chg, down) in enumerate(D.MARKETS):
        cx = mx + (i % 2) * mcolw
        cy = by + 20 + (i // 2) * 21
        d.text((cx, cy), name, font=F(SANS_B, 10), fill=INK)
        d.text((cx + 92, cy), level, font=F(SERIF, 10), fill=(40, 38, 34))
        d.text((cx + 168, cy), chg, font=F(SANS_B, 10),
               fill=RED if down else (30, 130, 76))
    d.text((mx, by + 20 + 5 * 21 + 4),
           "AROUND THE WORLD — EURO STOXX 50 -2.15% · HANG SENG -0.90% · ASX 200 -2.38% · BOVESPA +0.31%",
           font=F(SANS, 9), fill=GRAY)

    # ---- also list
    ay = 866
    d.line([(MARGIN, ay), (W - MARGIN, ay)], fill=RULE, width=2)
    d.text((MARGIN, ay + 6), "ALSO ON WEDNESDAY — 21 MORE STORIES",
           font=F(SANS_B, 11), fill=NAVY)
    iy = ay + 26
    f_lead, f_cl = F(SERIF_B, 10), F(SERIF, 10)
    for i, (region, lead, clause, lat, lon) in enumerate(D.ALSO):
        cx = xs[i % 3]
        cy = iy + (i // 3) * 14.5
        _, color = D.REGIONS[region]
        d.text((cx, cy), f"{i + 13}.", font=F(SANS_B, 9), fill=color)
        tx = cx + 24
        d.text((tx, cy), lead, font=f_lead, fill=INK)
        d.text((tx + d.textlength(lead, font=f_lead), cy), " — " + clause,
               font=f_cl, fill=(40, 38, 34))

    # ---- footer
    fy = 994
    d.line([(MARGIN, fy), (W - MARGIN, fy)], fill=RULE, width=1)
    foot = ("Every story happened or was first reported on Wednesday 18 November 2026. "
            "Disputed claims are attributed. Sources: Reuters · AP · AFP · BBC · "
            "Al Jazeera · UN · WHO · Der Spiegel · Le Monde. Original drawings.")
    f_f = F(SERIF_I, 9)
    d.text(((W - d.textlength(foot, font=f_f)) / 2, fy + 6), foot, font=f_f, fill=GRAY)

    out = os.path.join(HERE, "assets", "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes", img.size)


if __name__ == "__main__":
    main()
