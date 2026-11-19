#!/usr/bin/env python3
"""Draw a 1024x1024 front page summing up world news, Thu 19 Nov 2026.
Stdlib + Pillow only at build time; main.py (the entry program) is stdlib only.
Drawn shapes/icons only -- no photos, no copied artwork."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def text_block(draw, x, y, text, fnt, color, max_w, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    lh = leading or int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=color)
        y += lh
    return y

img = Image.new("RGB", (W, H), (250, 248, 242))
d = ImageDraw.Draw(img)

NAVY = (11, 31, 58)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
INK = (20, 20, 20)
GREY = (70, 70, 70)
LIGHT = (232, 236, 242)
BLUE = (30, 90, 160)

# --- Masthead ---
d.rectangle([0, 0, W, 128], fill=NAVY)
d.rectangle([0, 128, W, 134], fill=GOLD)
d.text((32, 18), "THE WORLD IN ONE PAGE", font=font(BOLD, 52), fill=(255, 255, 255))
d.text((32, 82), "Thursday 19 November 2026", font=font(BOLD, 30), fill=GOLD)
d.text((700, 84), "WORLD NEWS", font=font(BOLD, 28), fill=(255, 255, 255))

# --- Lead story ---
d.rectangle([24, 152, 1000, 400], outline=(180, 180, 180), width=2)
d.rectangle([24, 152, 150, 186], fill=RED)
d.text((36, 158), "LEAD", font=font(BOLD, 22), fill=(255, 255, 255))
y = text_block(d, 40, 194, "Trump, Xi and Putin meet in Shenzhen", font(BOLD, 44), INK, 940)
text_block(d, 40, y + 8,
           "China's Xi Jinping hugged President Trump on the tarmac as leaders "
           "gathered for a regional summit in Shenzhen. A trilateral meeting "
           "with President Putin is expected on Thursday.",
           font(REG, 23), GREY, 940)

# --- Middle row: three stories ---
cols = [
    ("US-IRAN CLASH", RED, "US and Iran exchange fire in the Gulf",
     "US struck a missile site on Qeshm Island after Iran hit a US radar base "
     "in Bahrain. Iran then hit a US base in Kuwait. Oil prices fell."),
    ("WASHINGTON", NAVY, "Jeffries nominated as first Black Speaker",
     "House Democrats nominated Hakeem Jeffries. He would take the gavel "
     "on 3 January."),
    ("BUSINESS", (0, 110, 60), "Anthropic raises $81.3bn in biggest IPO ever",
     "The Claude-maker is poised for a debut valued at more than $1.4tn -- "
     "the biggest IPO of all time."),
]
for i, (tag, col, head, body) in enumerate(cols):
    x0 = 24 + i * 326
    x1 = x0 + 302
    d.rectangle([x0, 416, x1, 678], outline=(180, 180, 180), width=2)
    d.rectangle([x0, 416, x1, 448], fill=col)
    d.text((x0 + 12, 422), tag, font=font(BOLD, 20), fill=(255, 255, 255))
    y = text_block(d, x0 + 14, 458, head, font(BOLD, 25), INK, 274)
    text_block(d, x0 + 14, y + 6, body, font(REG, 19), GREY, 274)

# --- Second row: two stories ---
row2 = [
    ("SPACE", NAVY, "Voyager 1 reaches one light-day from Earth",
     "NASA's Voyager 1 sets a record distance milestone, 50 years after launch."),
    ("GAMING", (120, 40, 140), "GTA VI begins global rollout",
     "Gamers enter Vice City as GTA VI launches worldwide after a 13-year wait."),
]
for i, (tag, col, head, body) in enumerate(row2):
    x0 = 24 + i * 490
    x1 = x0 + 466
    d.rectangle([x0, 694, x1, 878], outline=(180, 180, 180), width=2)
    d.rectangle([x0, 694, x1, 726], fill=col)
    d.text((x0 + 12, 700), tag, font=font(BOLD, 20), fill=(255, 255, 255))
    y = text_block(d, x0 + 14, 736, head, font(BOLD, 29), INK, 438)
    text_block(d, x0 + 14, y + 6, body, font(REG, 20), GREY, 438)

# --- Bottom briefs ---
d.rectangle([24, 894, 1000, 978], fill=LIGHT)
d.text((40, 904), "IN BRIEF", font=font(BOLD, 22), fill=RED)
d.text((40, 930), "Van Gogh painting sells for a record $190.4m after a row over its Nazi history.",
       font=font(REG, 20), fill=INK)
d.text((40, 954), "Crimean Bridge attacked again, a Russian official says.",
       font=font(REG, 20), fill=INK)

# --- Footer ---
d.text((32, 992), "19 November 2026  •  The world in one page", font=font(REG, 20), fill=GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, optimize=True)
print(out, img.size, os.path.getsize(out), "bytes")
