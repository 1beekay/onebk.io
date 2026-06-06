from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
img = Image.new("RGB", (W, H), (14, 19, 32))
d = ImageDraw.Draw(img)

# soft radial glows: violet top right, blue bottom left
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
for r in range(500, 0, -4):
    a = int(40 * (1 - r / 500))
    gd.ellipse([1020 - r, 60 - r, 1020 + r, 60 + r], fill=a)
violet = Image.new("RGB", (W, H), (124, 58, 237))
img = Image.composite(violet, img, glow)

glow2 = Image.new("L", (W, H), 0)
gd2 = ImageDraw.Draw(glow2)
for r in range(520, 0, -4):
    a = int(36 * (1 - r / 520))
    gd2.ellipse([120 - r, 600 - r, 120 + r, 600 + r], fill=a)
blue = Image.new("RGB", (W, H), (37, 99, 235))
img = Image.composite(blue, img, glow2)

d = ImageDraw.Draw(img)

# gradient top bar
for x in range(W):
    t = x / W
    c = (
        int(37 + (124 - 37) * t),
        int(99 + (58 - 99) * t),
        int(235 + (237 - 235) * t),
    )
    d.line([(x, 0), (x, 12)], fill=c)

def font(size, bold=True):
    paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/HelveticaNeue.ttc",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size, index=1 if bold else 0)
        except Exception:
            continue
    return ImageFont.load_default()

name_f = font(76, bold=True)
tag_f = font(36, bold=True)
sub_f = font(27, bold=False)
url_f = font(28, bold=True)

d.text((90, 200), "Robert Ball-Konieczny", font=name_f, fill=(245, 247, 250))

# gradient tagline rendered via mask
tag = "I build the platforms engineering organizations run on."
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
md.text((90, 320), tag, font=tag_f, fill=255)
grad = Image.new("RGB", (W, H))
gdr = ImageDraw.Draw(grad)
for x in range(W):
    t = x / W
    c = (
        int(138 + (196 - 138) * t),
        int(180 + (181 - 180) * t),
        int(255 + (253 - 255) * t),
    )
    gdr.line([(x, 0), (x, H)], fill=c)
img = Image.composite(grad, img, mask)
d = ImageDraw.Draw(img)

d.text((90, 400), "Multicloud SaaS   ·   Reliability   ·   AI first engineering", font=sub_f, fill=(151, 163, 182))
d.text((90, 520), "onebk.io", font=url_f, fill=(122, 156, 220))

img.save("og.png", optimize=True)
print("og.png written", img.size)
