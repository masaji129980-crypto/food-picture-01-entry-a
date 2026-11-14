#!/usr/bin/env python3
"""Draw 'Sajian Nusantara' — an Indonesian feast spread, top-down on a banana
leaf — entirely in code with Pillow. Original illustration, no copied assets."""
import math
import random
from PIL import Image, ImageChops, ImageDraw, ImageFilter

random.seed(20261114)
W = H = 1024
img = Image.new("RGB", (W, H), (58, 34, 20))
d = ImageDraw.Draw(img)

# ---- wooden table background ---------------------------------------------
for y in range(0, H, 128):
    tone = random.randint(-8, 8)
    d.rectangle([0, y, W, y + 127], fill=(58 + tone, 34 + tone // 2, 20 + tone // 3))
    d.line([0, y, W, y], fill=(38, 22, 12), width=3)
for _ in range(2600):
    x, y = random.randint(0, W - 1), random.randint(0, H - 1)
    v = random.randint(-14, 14)
    d.point((x, y), fill=(58 + v, 34 + v // 2, 20 + v // 3))
# soft vignette
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-220, -220, W + 220, H + 220], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(180))
dark = Image.new("RGB", (W, H), (20, 10, 5))
img = Image.composite(img, dark, vig)
d = ImageDraw.Draw(img)

# ---- banana leaf (big, slightly rotated ellipse) --------------------------
leaf = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(leaf)
ld.ellipse([28, 60, 996, 964], fill=(34, 96, 38, 255))
# leaf shading: darker edges, lighter centre
for i, (c, a) in enumerate([((26, 78, 30), 90), ((46, 122, 48), 70), ((58, 140, 58), 50)]):
    ld.ellipse([28 + i * 26, 60 + i * 22, 996 - i * 26, 964 - i * 22], fill=c + (a,))
ld.ellipse([150, 150, 874, 874], fill=(52, 130, 52, 60))
# midrib
ld.line([512, 70, 512, 954], fill=(120, 165, 70, 255), width=10)
# veins
for k in range(1, 15):
    y = 70 + k * 60
    ld.line([512, y, 120, y + 70], fill=(90, 145, 60, 200), width=4)
    ld.line([512, y, 904, y + 70], fill=(90, 145, 60, 200), width=4)
leaf = leaf.filter(ImageFilter.GaussianBlur(1.2))
# clip the leaf (midrib + veins) to its ellipse so nothing sticks out
_leaf_mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(_leaf_mask).ellipse([28, 60, 996, 964], fill=255)
leaf.putalpha(ImageChops.multiply(leaf.split()[3], _leaf_mask))
img = Image.alpha_composite(img.convert("RGBA"), leaf)
d = ImageDraw.Draw(img)

def shadow(cx, cy, rx, ry, blur=14, alpha=110):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(0, 0, 0, alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    return sh

def speckle(cx, cy, rx, ry, n, colors, rmin=1, rmax=3):
    for _ in range(n):
        ang = random.uniform(0, 2 * math.pi)
        rr = math.sqrt(random.random())
        x = cx + rr * rx * math.cos(ang)
        y = cy + rr * ry * math.sin(ang)
        r = random.uniform(rmin, rmax)
        d.ellipse([x - r, y - r, x + r, y + r], fill=random.choice(colors))

# ---- rice mound (centre-left) --------------------------------------------
img = Image.alpha_composite(img, shadow(400, 560, 215, 165))
d = ImageDraw.Draw(img)
d.ellipse([190, 400, 610, 720], fill=(244, 238, 222))
d.ellipse([215, 420, 585, 660], fill=(252, 248, 236))
# rice grains: tiny arcs/dots
for _ in range(900):
    ang = random.uniform(0, 2 * math.pi)
    rr = math.sqrt(random.random())
    x = 400 + rr * 185 * math.cos(ang)
    y = 545 + rr * 135 * math.sin(ang) - 40 * (1 - rr)
    ln = random.uniform(4, 9)
    a = random.uniform(0, math.pi)
    col = random.choice([(255, 255, 250), (238, 230, 208), (226, 216, 188), (250, 244, 228)])
    d.line([x, y, x + ln * math.cos(a), y + ln * math.sin(a)], fill=col, width=2)
# fried shallots + herbs on rice
speckle(400, 520, 130, 80, 70, [(190, 120, 50), (160, 95, 35), (215, 150, 70)], 2, 4)
for _ in range(14):
    x = random.randint(300, 500); y = random.randint(460, 600)
    d.line([x, y, x + 12, y - 8], fill=(40, 110, 45), width=3)
    d.line([x + 6, y, x + 2, y - 12], fill=(55, 130, 55), width=3)

# ---- rendang (top-right, glossy dark brown chunks in sauce) --------------
img = Image.alpha_composite(img, shadow(760, 300, 165, 125))
d = ImageDraw.Draw(img)
d.ellipse([610, 185, 910, 415], fill=(88, 48, 22))          # sauce pool
d.ellipse([630, 200, 890, 395], fill=(104, 58, 26))
for _ in range(420):
    ang = random.uniform(0, 2 * math.pi); rr = math.sqrt(random.random())
    x = 760 + rr * 125 * math.cos(ang); y = 300 + rr * 95 * math.sin(ang)
    d.point((x, y), fill=random.choice([(120, 70, 32), (140, 84, 38), (70, 38, 16)]))
# beef chunks
chunks = [(700, 260, 62, 48, -20), (790, 240, 58, 46, 15), (740, 320, 66, 50, 5),
          (830, 320, 54, 44, -35), (690, 340, 50, 40, 25)]
for cx, cy, rx, ry, rot in chunks:
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(72, 38, 18))
    d.ellipse([cx - rx + 8, cy - ry + 6, cx + rx - 10, cy + ry - 12], fill=(96, 54, 24))
    d.ellipse([cx - rx + 16, cy - ry + 10, cx + rx - 22, cy + ry - 22], fill=(118, 68, 30))
    d.arc([cx - rx + 10, cy - ry + 8, cx + rx - 8, cy + ry - 6], 200, 340,
          fill=(210, 140, 70), width=5)  # glossy highlight
# coconut flakes / chilli flecks
speckle(760, 300, 130, 90, 60, [(235, 220, 190), (200, 60, 30), (255, 180, 60)], 1, 3)
# kaffir lime leaf garnish
d.polygon([(850, 210), (890, 225), (855, 250), (825, 230)], fill=(46, 120, 50))
d.line([825, 230, 890, 225], fill=(120, 170, 70), width=2)

# ---- sate skewers (bottom-right, diagonal) -------------------------------
img = Image.alpha_composite(img, shadow(720, 730, 230, 130))
d = ImageDraw.Draw(img)
# peanut sauce pool under skewers
d.ellipse([500, 640, 950, 870], fill=(176, 108, 44))
d.ellipse([520, 655, 930, 855], fill=(196, 128, 56))
speckle(725, 755, 200, 95, 200, [(220, 160, 80), (150, 88, 30), (230, 175, 95)], 1, 3)
for k in range(3):
    y0 = 690 + k * 55
    # bamboo skewer
    d.line([505, y0 + 8, 940, y0 - 28], fill=(214, 178, 120), width=6)
    # charred meat cubes along it
    for j in range(5):
        cx = 560 + j * 72 + random.randint(-4, 4)
        cy = y0 - j * 7 + random.randint(-4, 4)
        d.rounded_rectangle([cx - 26, cy - 24, cx + 26, cy + 24], radius=10,
                            fill=(122, 62, 26))
        d.rounded_rectangle([cx - 20, cy - 18, cx + 20, cy + 18], radius=8,
                            fill=(150, 80, 34))
        # char marks
        d.line([cx - 18, cy - 8, cx + 6, cy + 14], fill=(52, 24, 10), width=5)
        d.line([cx - 2, cy - 16, cx + 18, cy + 4], fill=(52, 24, 10), width=4)
        # glossy highlight
        d.arc([cx - 18, cy - 16, cx + 14, cy + 8], 200, 330, fill=(235, 160, 80), width=4)
    # peanut sauce drizzle over skewers
    for j in range(5):
        cx = 560 + j * 72
        cy = y0 - j * 7
        d.ellipse([cx - 12, cy + 16, cx + 14, cy + 30], fill=(222, 158, 74))

# ---- sambal bowl (top-left) ----------------------------------------------
img = Image.alpha_composite(img, shadow(250, 235, 95, 80))
d = ImageDraw.Draw(img)
d.ellipse([165, 165, 335, 305], fill=(245, 240, 225))       # bowl
d.ellipse([178, 178, 322, 292], fill=(196, 38, 22))         # sambal
d.ellipse([190, 188, 310, 280], fill=(220, 58, 30))
speckle(250, 235, 55, 40, 90, [(150, 20, 12), (255, 120, 50), (255, 200, 90), (120, 10, 8)], 1, 3)
d.arc([195, 190, 305, 270], 200, 340, fill=(255, 150, 90), width=5)  # gloss
d.line([250, 165, 250, 305], fill=(210, 205, 190), width=2)  # bowl rim shine

# ---- kerupuk crackers (left edge) ----------------------------------------
for cx, cy, rot in [(120, 480, 20), (105, 600, -15), (150, 700, 35)]:
    img = Image.alpha_composite(img, shadow(cx, cy, 70, 55, blur=10, alpha=90))
    d = ImageDraw.Draw(img)
    d.ellipse([cx - 62, cy - 48, cx + 62, cy + 48], fill=(250, 226, 170))
    d.ellipse([cx - 50, cy - 38, cx + 50, cy + 38], fill=(255, 238, 195))
    speckle(cx, cy, 45, 32, 40, [(230, 190, 120), (245, 215, 150)], 2, 4)
    d.arc([cx - 45, cy - 34, cx + 45, cy + 34], 30, 200, fill=(225, 185, 115), width=3)

# ---- cucumber + tomato garnish (bottom-left of rice) ----------------------
for cx, cy in [(300, 760), (360, 800), (255, 800)]:
    d.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(34, 120, 52))
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(190, 225, 160))
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(220, 240, 190))
    for a in range(0, 360, 45):
        x = cx + 18 * math.cos(math.radians(a)); y = cy + 18 * math.sin(math.radians(a))
        d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(240, 250, 220))
d.ellipse([430, 780, 500, 845], fill=(214, 48, 32))          # tomato wedge
d.ellipse([440, 788, 492, 838], fill=(235, 90, 60))
d.polygon([(465, 790), (480, 815), (450, 815)], fill=(255, 180, 150))

# ---- lime wedge + herbs (top centre) -------------------------------------
d.pieslice([470, 120, 560, 205], 180, 360, fill=(46, 140, 60))
d.pieslice([478, 128, 552, 197], 180, 360, fill=(190, 225, 120))
for a in range(200, 341, 28):
    x = 515 + 28 * math.cos(math.radians(a)); y = 162 + 28 * math.sin(math.radians(a))
    d.line([515, 162, x, y], fill=(240, 245, 200), width=2)
for _ in range(10):
    x = random.randint(560, 640); y = random.randint(150, 220)
    d.line([x, y, x + 14, y - 10], fill=(40, 110, 45), width=3)

# ---- steam wisps above rendang & rice (soft white, blurred) --------------
steam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(steam)
for bx, by, hgt in [(760, 190, 90), (400, 400, 80), (720, 640, 70)]:
    for i, off in enumerate([-14, 0, 14]):
        sd.line([(bx + off, by), (bx + off + 10, by - hgt // 2),
                 (bx + off - 8, by - hgt)], fill=(255, 255, 255, 70), width=9)
steam = steam.filter(ImageFilter.GaussianBlur(6))
img = Image.alpha_composite(img.convert("RGBA"), steam)

# ---- final warm grade + gentle sharpen ------------------------------------
img = img.convert("RGB")
img.save("/home/hatch/workspace/makefun/entry-food01-a/entry.png", optimize=True)
print("saved")
