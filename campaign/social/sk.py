# -*- coding: utf-8 -*-
"""Rendering toolkit for the Smart Biogas social media kit.

Brand palette + typography copied from campaign/biogas/style.css so the
images, videos and website read as one system.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT.parent / "biogas" / "assets"
IMG_DIR = ROOT / "images"

# ---------------------------------------------------------------- palette ---
GREEN = (15, 61, 46)       # --green
TEAL = (14, 159, 110)      # --teal
TEAL2 = (11, 122, 86)      # --teal2
AMBER = (245, 158, 11)     # --amber
AMBER2 = (217, 119, 6)     # --amber2
BG = (248, 250, 249)       # --bg
DARK = (11, 28, 22)        # --dark
MUTED = (107, 114, 128)    # --muted
LINE = (229, 231, 235)     # --line
WHITE = (255, 255, 255)
INK = (17, 24, 39)
GRAY = (75, 85, 99)
MINT = (236, 253, 245)
MINT2 = (167, 243, 208)
LIME = (110, 231, 183)
CREAM = (255, 251, 235)
RUST = (146, 64, 14)

F_BLACK = r"C:\Windows\Fonts\seguibl.ttf"
F_BOLD = r"C:\Windows\Fonts\segoeuib.ttf"
F_SEMI = r"C:\Windows\Fonts\segoeuisl.ttf"
F_REG = r"C:\Windows\Fonts\segoeui.ttf"
F_MONO = r"C:\Windows\Fonts\consolab.ttf"

BRAND = "SMART BIOGAS"
SUBBRAND = "SUT · ENERGY ENGINEERING"
TAGLINE = "WASTE HAS ENERGY."

WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)


def F(path, size):
    return ImageFont.truetype(path, size)


# ------------------------------------------------------------- primitives ---
def vgrad(size, c1, c2):
    w, h = size
    strip = Image.new("RGB", (1, h))
    px = strip.load()
    for y in range(h):
        t = y / max(1, h - 1)
        px[0, y] = (int(c1[0] + (c2[0] - c1[0]) * t),
                    int(c1[1] + (c2[1] - c1[1]) * t),
                    int(c1[2] + (c2[2] - c1[2]) * t))
    return strip.resize((w, h), Image.BILINEAR)


def dgrad(size, c1, c2):
    """Diagonal gradient (top-left -> bottom-right)."""
    w, h = size
    base = vgrad((1, h), c1, c2).resize((w, h), Image.BILINEAR)
    # blend horizontally for a diagonal feel
    side = vgrad((w, 1), c1, c2).resize((w, h), Image.BILINEAR)
    return Image.blend(base, side, 0.45)


def cover(img, size, focus=0.45):
    iw, ih = img.size
    w, h = size
    sc = max(w / iw, h / ih)
    nw, nh = max(w, int(iw * sc + 0.5)), max(h, int(ih * sc + 0.5))
    img = img.resize((nw, nh), Image.LANCZOS)
    left = (nw - w) // 2
    top = int((nh - h) * focus)
    return img.crop((left, top, left + w, top + h))


def paste_round(base, img, box, radius=28, focus=0.45):
    x, y, w, h = box
    img = cover(img, (w, h), focus).convert("RGB")
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    base.paste(img, (x, y), mask)


def scrim(base, box, color=(0, 0, 0), top=0, bottom=200):
    x, y, w, h = box
    strip = Image.new("L", (1, h))
    px = strip.load()
    for i in range(h):
        t = i / max(1, h - 1)
        px[0, i] = int(top + (bottom - top) * t)
    grad = strip.resize((w, h), Image.BILINEAR)
    base.paste(Image.new("RGB", (w, h), color), (x, y), grad)


def wrap(draw, text, font, max_w):
    out = []
    for block in text.split("\n"):
        words, cur = block.split(), ""
        for w in words:
            t = (cur + " " + w).strip()
            if draw.textlength(t, font=font) <= max_w or not cur:
                cur = t
            else:
                out.append(cur)
                cur = w
        out.append(cur)
    return out


def line_h(font, gap=0.14):
    return int(font.size * 1.22 + font.size * gap)


def tracked(draw, xy, text, font, fill, track=2, anchor_left=True):
    """Letter-spaced text (PIL has no tracking). Returns advance width."""
    x, y = xy
    total = 0
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + track
        total = x - xy[0]
    return total


def fit(draw, text, path, max_w, start, minimum=26, max_lines=None, bold_scale=1):
    size = start
    while size > minimum:
        f = F(path, int(size * bold_scale))
        lines = wrap(draw, text, f, max_w)
        if max_lines is None or len(lines) <= max_lines:
            return f, lines
        size -= 2
    f = F(path, minimum)
    return f, wrap(draw, text, f, max_w)


def para(draw, x, y, text, font, fill, max_w, gap=0.16, align="l"):
    lh = line_h(font, gap)
    for i, ln in enumerate(wrap(draw, text, font, max_w)):
        w = draw.textlength(ln, font=font)
        if align == "c":
            draw.text((x + (max_w - w) / 2, y + i * lh), ln, font=font, fill=fill)
        elif align == "r":
            draw.text((x + max_w - w, y + i * lh), ln, font=font, fill=fill)
        else:
            draw.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(wrap(draw, text, font, max_w)) * lh


def pill(draw, x, y, text, font, fg=WHITE, bg=TEAL, padx=26, pady=14, border=None, r=None):
    tw = int(draw.textlength(text, font=font))
    w = tw + 2 * padx
    h = font.size + 2 * pady
    if r is None:
        r = h // 2
    draw.rounded_rectangle((x, y, x + w, y + h), radius=r, fill=bg,
                           outline=border, width=3 if border else 0)
    draw.text((x + padx, y + pady - int(font.size * 0.08)), text, font=font, fill=fg)
    return w, h


def card(canvas, box, fill=WHITE, outline=None, r=24, width=3):
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)
    return d


def chip_flow(draw, x, y, max_w, items, font, fg=INK, bg=WHITE, border=LINE, arrow=TEAL):
    """Wrapping row of chips joined by arrows. Returns bottom y."""
    lh = font.size + 34
    cx, cy = x, y
    ah = draw.textlength("→", font=font)
    for i, it in enumerate(items):
        tw = int(draw.textlength(it, font=font))
        cw = tw + 44
        need = cw + (34 if cx > x else 0)
        if cx > x and cx - x + need > max_w:
            cx, cy = x, cy + lh + 12
        draw.rounded_rectangle((cx, cy, cx + cw, cy + lh), radius=lh // 2,
                               fill=bg, outline=border, width=3)
        draw.text((cx + 22, cy + (lh - font.size) / 2 - 4), it, font=font, fill=fg)
        cx += cw
        if i < len(items) - 1:
            draw.text((cx + 11, cy + (lh - font.size) / 2 - 4), "→", font=font, fill=arrow)
            cx += 22 + int(ah)
    return cy + lh


def numbered_tile(canvas, box, n, head, body, dark=False, accent=AMBER):
    d = card(canvas, box, fill=(17, 37, 30) if dark else WHITE,
             outline=None if dark else LINE, r=22)
    x, y, w, h = box
    pad = 28
    bx = x + pad
    by = y + pad
    d.ellipse((bx, by, bx + 62, by + 62), fill=accent)
    f_n = F(F_BLACK, 34)
    d.text((bx + 31 - d.textlength(str(n), font=f_n) / 2, by + 12), str(n), font=f_n, fill=INK)
    f_h = F(F_BOLD, 34)
    hl = wrap(d, head, f_h, w - 2 * pad)
    for i, ln in enumerate(hl[:2]):
        d.text((bx, by + 78 + i * int(f_h.size * 1.2)), ln, font=f_h,
               fill=WHITE if dark else GREEN)
    f_b = F(F_REG, 25)
    yy = by + 78 + len(hl[:2]) * int(f_b.size * 1.5)
    for ln in wrap(d, body, f_b, w - 2 * pad):
        d.text((bx, yy), ln, font=f_b, fill=MINT2 if dark else GRAY)
        yy += int(f_b.size * 1.34)
    if yy > y + h:
        warn("tile overflow: %s (%d > %d)" % (head[:24], yy, y + h))
    return d


def spec_table(draw, x, y, w, rows, dark=True, rh=54, key_w=None):
    f_k = F(F_BOLD, 25)
    f_v = F(F_REG, 25)
    key_w = key_w or int(w * 0.34)
    yy = y
    for i, (k, v) in enumerate(rows):
        if i % 2 == 0:
            draw.rectangle((x, yy - 8, x + w, yy + rh - 8),
                           fill=(17, 37, 30) if dark else MINT)
        draw.text((x + 6, yy + 4), k, font=f_k, fill=LIME if dark else TEAL2)
        vl = wrap(draw, v, f_v, w - key_w - 12)
        for j, ln in enumerate(vl):
            draw.text((x + key_w, yy + 4 + j * 30), ln, font=f_v,
                      fill=MINT if dark else INK)
        yy += max(rh, len(vl) * 30 + 12)
        if i < len(rows) - 1:
            draw.line((x, yy - 6, x + w, yy - 6), fill=(31, 58, 46) if dark else LINE, width=2)
    return yy
