#!/usr/bin/env python3
"""Mini-poster (4x6, 300dpi = 1200x1800) for the violin lessons QR handout.
Tone matches the main poster: cream + deep-navy serif + gold accents.
NO black ink: all "dark" tones are deep navy; landmark photos are rendered as
a navy<->cream duotone so they print on a color-only printer and read as one set.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
import segno

HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "assets")
URL = "https://taehyungalexkim.github.io/alice-violin/?ref=poster"

# ---- palette ----
NAVY   = (33, 56, 78)
NAVY2  = (47, 74, 99)
GOLD   = (176, 138, 74)
GOLDS  = (201, 169, 106)
CREAM  = (246, 241, 231)
CARD   = (252, 250, 245)
INK    = (74, 70, 62)
W, H   = 1200, 1800
M      = 92

# ---- fonts ----
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
GEO   = "/System/Library/Fonts/Supplemental/Georgia.ttf"
GEOI_CANDIDATES = ["/System/Library/Fonts/Supplemental/Georgia Italic.ttf"]
def f_didot(sz, idx=0): return ImageFont.truetype(DIDOT, sz, index=idx)   # 0 reg,1 ital,2 bold
def f_geo(sz):          return ImageFont.truetype(GEO, sz)
def f_geo_i(sz):
    for p in GEOI_CANDIDATES:
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return f_didot(sz, 1)

# ---- helpers ----
def vgradient(w, h, top, bot):
    base = Image.new("RGB", (w, h), top)
    px = base.load()
    for y in range(h):
        t = y / (h - 1)
        c = tuple(int(top[i] + (bot[i]-top[i])*t) for i in range(3))
        for x in range(w):
            px[x, y] = c
    return base

def crop_aspect(im, w, h, ox=0.5, oy=0.5):
    im = ImageOps.exif_transpose(im)   # honour camera orientation (Korea jpeg was flipped)
    im = im.convert("RGB")
    iw, ih = im.size
    tar = w / h; ar = iw / ih
    if ar > tar:
        nw = int(ih * tar); x = int((iw - nw) * ox); im = im.crop((x, 0, x+nw, ih))
    else:
        nh = int(iw / tar); y = int((ih - nh) * oy); im = im.crop((0, y, iw, y+nh))
    return im.resize((w, h), Image.LANCZOS)

def duotone(im, dark, light):
    g = ImageOps.autocontrast(im.convert("L"), cutoff=1)
    chans = []
    for i in range(3):
        lut = [int(dark[i] + (light[i]-dark[i]) * v/255) for v in range(256)]
        chans.append(g.point(lut))
    return Image.merge("RGB", chans)

def tracked(draw, cx, cy, text, font, fill, tracking):
    ws = [draw.textlength(ch, font=font) for ch in text]
    total = sum(ws) + tracking*(len(text)-1)
    x = cx - total/2
    for ch, w in zip(text, ws):
        draw.text((x, cy), ch, font=font, fill=fill, anchor="lm")
        x += w + tracking

def rrect(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

# ---- canvas ----
img = vgradient(W, H, (250, 246, 238), (243, 237, 224))
d = ImageDraw.Draw(img)
cx = W // 2

# faint German accent (like original "Spaß mit musik")
tracked(d, cx, 92, "Spaß mit Musik", f_geo_i(30), (199, 184, 150), 2)

# ---- title ----
tracked(d, cx, 196, "VIOLIN",  f_didot(132, 2), NAVY, 8)
tracked(d, cx, 322, "LESSONS", f_didot(132, 2), NAVY, 8)

# divider with diamond
dy = 405
d.line([(cx-150, dy), (cx-22, dy)], fill=GOLD, width=2)
d.line([(cx+22, dy), (cx+150, dy)], fill=GOLD, width=2)
d.polygon([(cx, dy-9), (cx+11, dy), (cx, dy+9), (cx-11, dy)], fill=GOLD)

tracked(d, cx, 452, "PRIVATE 1:1 INSTRUCTION", f_geo(33), GOLD, 8)

# ---- triptych ----
panels = [
    ("vancouver.webp", "VANCOUVER", 0.5, 0.5),
    ("freiburg.jpg",   "FREIBURG",  0.5, 0.5),
    ("korea.webp",     "KOREA",     0.5, 0.5),
]
pw = (W - 2*M - 2*30) // 3
ph = 250
ty = 506
capf = f_geo(27)
for i, (fn, cap, ox, oy) in enumerate(panels):
    x0 = M + i*(pw + 30)
    src = Image.open(os.path.join(A, fn))
    duo = duotone(crop_aspect(src, pw, ph, ox, oy), NAVY, (247, 243, 233))
    img.paste(duo, (x0, ty))
    d.rectangle([x0, ty, x0+pw-1, ty+ph-1], outline=GOLDS, width=2)
    d.line([(x0+pw*0.18, ty+ph+20), (x0+pw*0.82, ty+ph+20)], fill=GOLD, width=1)
    tracked(d, x0+pw/2, ty+ph+44, cap, capf, NAVY, 5)

# ---- teacher ----
by = ty + ph + 110            # ~866
tracked(d, cx, by, "Ja Young (Alice) Jeon", f_didot(54, 0), NAVY, 2)
d.text((cx, by+50), "Bachelor & Master of Music (Germany)", font=f_geo_i(31), fill=INK, anchor="mm")
d.text((cx, by+95), "Beginners to Advanced  ·  RCM Exam Prep  ·  Vancouver, BC",
       font=f_geo(27), fill=INK, anchor="mm")

# ---- QR card ----
qr_png = os.path.join(HERE, "_qr_navy.png")
segno.make(URL, error="h").save(qr_png, scale=9, border=4, dark="#21384e", light="#fcfaf5")
qr = Image.open(qr_png).convert("RGB")
QSZ = qr.size[0]                       # 57 modules * 9 = 513
pad_top, cap_h = 46, 150
cardw = QSZ + 2*64
cardh = pad_top + QSZ + cap_h
card_x = cx - cardw//2
card_y = by + 150                      # ~1016
rrect(d, [card_x, card_y, card_x+cardw, card_y+cardh], 26, fill=CARD, outline=GOLDS, width=2)
img.paste(qr, (cx - QSZ//2, card_y + pad_top))
qcap_y = card_y + pad_top + QSZ + 18
tracked(d, cx, qcap_y+16, "SCAN THE QR CODE", f_geo(31), GOLD, 6)
d.text((cx, qcap_y+62), "to see lessons, philosophy & contact",
       font=f_geo_i(28), fill=INK, anchor="mm")

# ---- footer ----
fy = card_y + cardh + 58
d.line([(M+40, fy), (W-M-40, fy)], fill=GOLDS, width=1)
tracked(d, cx, fy+34, "JA YOUNG (ALICE) JEON   ·   VANCOUVER, BC",
        f_geo(25), NAVY, 4)

out = os.path.join(HERE, "violin-mini-poster.png")
img.save(out, dpi=(300, 300))
os.remove(qr_png)
print("saved:", out, img.size)
