#!/usr/bin/env python3
"""Render the Friday 20 November 2026 world-news front page.

The stories in news.json were researched from Reuters, AP, BBC and
The Hindu reporting of 20 November 2026 (morning editions in Asia and
overnight wires). This script draws them as a 1024x1024 newspaper front
page, entry.png. It runs fully offline and is deterministic: the same
news.json always yields the same PNG bytes.

Run it with: python3 render.py
"""
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024
INK = (24, 30, 38)
PAPER = (248, 244, 235)
NAVY = (13, 40, 68)
NAVY_SOFT = (203, 214, 226)
GOLD = (198, 158, 36)
GOLD_PALE = (233, 197, 94)
CARD = (255, 255, 255)
GREY = (86, 96, 108)
RULE = (212, 204, 188)
RED = (164, 27, 27)
TEAL = (14, 116, 108)
BLUE = (28, 76, 148)
GREEN = (45, 122, 48)
PLUM = (104, 60, 154)


def font(weight, size):
    name = "DejaVuSans-Bold.ttf" if weight == "bold" else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def fit_lines(draw, text, fnt, width):
    """Greedy word wrap of text to the given pixel width."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, x, y, lines, fnt, colour, step):
    """Draw lines top to bottom; return the y just below the last line."""
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=colour)
        y += step
    return y


def panel(draw, box, fill=CARD, edge=RULE):
    draw.rounded_rectangle(box, radius=10, fill=fill, outline=edge, width=2)


def cyclone_glyph(draw, x, y, w, h, colour):
    """A spiral storm: three arcs winding into the centre."""
    cx, cy = x + w // 2, y + h // 2
    for k, radius in enumerate((h // 2 - 4, h // 3, h // 5)):
        start = 20 + k * 120
        draw.arc([cx - radius, cy - radius, cx + radius, cy + radius],
                 start, start + 250, fill=colour, width=6)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=colour)


def clock_glyph(draw, x, y, w, h, colour):
    """A clock face: the decision that can wait."""
    cx, cy = x + w // 2, y + h // 2
    r = min(w, h) // 2 - 4
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour, width=6)
    draw.line([cx, cy, cx, cy - r + 12], fill=colour, width=6)
    draw.line([cx, cy, cx + r - 16, cy + 8], fill=colour, width=6)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=colour)


def scales_glyph(draw, x, y, w, h, colour):
    """Balanced scales: the court's judgment."""
    cx = x + w // 2
    top = y + 8
    draw.line([cx, top, cx, y + h - 14], fill=colour, width=6)
    draw.line([x + 8, top + 6, x + w - 8, top + 6], fill=colour, width=6)
    for side in (-1, 1):
        px = cx + side * (w // 2 - 12)
        draw.line([px, top + 6, px, top + 34], fill=colour, width=4)
        draw.arc([px - 22, top + 30, px + 22, top + 74], 0, 180,
                 fill=colour, width=5)
    draw.line([cx - 16, y + h - 14, cx + 16, y + h - 14], fill=colour, width=6)


def talks_glyph(draw, x, y, w, h, colour):
    """Two speech bubbles facing each other: negotiations."""
    draw.rounded_rectangle([x + 4, y + 10, x + w // 2 + 8, y + h // 2 + 6],
                           radius=12, outline=colour, width=5)
    draw.polygon([(x + 18, y + h // 2 + 6), (x + 34, y + h // 2 + 6),
                  (x + 20, y + h // 2 + 24)], fill=colour)
    draw.rounded_rectangle([x + w // 2 - 8, y + h // 2 - 2, x + w - 4,
                            y + h - 10], radius=12, outline=colour, width=5)
    draw.polygon([(x + w - 34, y + h - 10), (x + w - 18, y + h - 10),
                  (x + w - 20, y + h - 10 + 18)], fill=colour)


def tower_glyph(draw, x, y, w, h, colour):
    """A tall tower with lit windows and a burst at its crown."""
    tx, tw = x + w // 2 - 16, 32
    draw.rectangle([tx, y + 26, tx + tw, y + h - 6], outline=colour, width=5)
    for row in range(4):
        wy = y + 40 + row * 18
        draw.line([tx + 6, wy, tx + tw - 6, wy], fill=colour, width=4)
    cx, cy = x + w // 2, y + 16
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        draw.line([cx + int(10 * math.cos(rad)), cy + int(10 * math.sin(rad)),
                   cx + int(22 * math.cos(rad)), cy + int(22 * math.sin(rad))],
                  fill=colour, width=4)


GLYPHS = [clock_glyph, scales_glyph, talks_glyph, tower_glyph]
ACCENTS = [BLUE, TEAL, GREEN, PLUM]


def masthead(draw, data):
    draw.rectangle([0, 0, W, 140], fill=NAVY)
    draw.rectangle([0, 140, W, 146], fill=GOLD)
    draw.text((28, 20), data["title"], font=font("bold", 64), fill=(255, 255, 255))
    draw.text((30, 100), data["subtitle"], font=font("regular", 23), fill=NAVY_SOFT)
    draw.text((996, 22), data["weekday"], font=font("bold", 28),
              fill=GOLD_PALE, anchor="ra")
    draw.text((996, 56), data["dateline"], font=font("bold", 38),
              fill=(255, 255, 255), anchor="ra")


def hero(draw, data):
    story = data["hero"]
    panel(draw, [24, 158, 1000, 424])
    draw.rounded_rectangle([24, 158, 244, 424], radius=10, fill=RED)
    draw.rectangle([200, 158, 244, 424], fill=RED)
    cyclone_glyph(draw, 44, 208, 176, 140, (255, 255, 255))
    draw.text((268, 176), story["kicker"], font=font("bold", 21), fill=RED)
    y = text_block(draw, 268, 204,
                   fit_lines(draw, story["headline"], font("bold", 42), 700),
                   font("bold", 42), NAVY, 50)
    text_block(draw, 268, y + 12,
               fit_lines(draw, story["body"], font("regular", 25), 700),
               font("regular", 25), GREY, 33)


def story_grid(draw, data):
    for i, story in enumerate(data["stories"]):
        col, row = i % 2, i // 2
        x0 = 24 + col * 504
        y0 = 434 + row * 194
        panel(draw, [x0, y0, x0 + 472, y0 + 180])
        draw.rectangle([x0 + 10, y0, x0 + 462, y0 + 8], fill=ACCENTS[i])
        GLYPHS[i](draw, x0 + 14, y0 + 42, 84, 92, ACCENTS[i])
        tx = x0 + 110
        draw.text((tx, y0 + 24), story["kicker"], font=font("bold", 19),
                  fill=ACCENTS[i])
        y = text_block(draw, tx, y0 + 50,
                       fit_lines(draw, story["headline"], font("bold", 28), 346)[:2],
                       font("bold", 28), INK, 34)
        text_block(draw, tx, y + 6,
                   fit_lines(draw, story["body"], font("regular", 18), 346)[:2],
                   font("regular", 18), GREY, 24)


def briefs(draw, data):
    draw.text((28, 814), "ALSO TODAY", font=font("bold", 22), fill=NAVY)
    draw.line([170, 828, 996, 828], fill=RULE, width=2)
    for i, brief in enumerate(data["briefs"]):
        bx = 28 + i * 247
        draw.rectangle([bx, 856, bx + 14, 870], fill=NAVY)
        text_block(draw, bx + 24, 850,
                   fit_lines(draw, brief["headline"], font("bold", 20), 210)[:2],
                   font("bold", 20), INK, 25)
        text_block(draw, bx + 24, 904,
                   fit_lines(draw, brief["body"], font("regular", 17), 210)[:2],
                   font("regular", 17), GREY, 22)


def footer(draw, data):
    draw.rectangle([0, 954, W, 992], fill=RED)
    draw.text((512, 962), data["ticker"], font=font("bold", 22),
              fill=(255, 255, 255), anchor="ma")
    draw.text((512, 998), data["sources"], font=font("regular", 14),
              fill=GREY, anchor="ma")


def main():
    with open(os.path.join(HERE, "news.json"), encoding="utf-8") as fh:
        data = json.load(fh)
    image = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(image)
    masthead(draw, data)
    hero(draw, data)
    story_grid(draw, data)
    briefs(draw, data)
    footer(draw, data)
    out = os.path.join(HERE, "entry.png")
    image.save(out, format="PNG", optimize=True)
    print("wrote", out, image.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
