from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (10, 10, 10)          # #0A0A0A
WHITE = (240, 244, 243)    # #F0F4F3
TEAL = (0, 212, 170)       # #00D4AA
MUTED = (138, 155, 168)    # #8a9ba8

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# subtle teal corner accents
d.rectangle([0, 0, W, 6], fill=TEAL)
d.rectangle([0, H - 6, W, H], fill=(6, 10, 14))

bold = lambda s: ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", s)
reg = lambda s: ImageFont.truetype("C:/Windows/Fonts/arial.ttf", s)

PAD = 90

# small eyebrow
eyebrow = "AI AUTOMATION AGENCY"
d.text((PAD, 150), eyebrow, font=bold(28), fill=TEAL)

# wordmark: Core (white) + magna (teal)
wf = bold(132)
y_word = 200
x = PAD
d.text((x, y_word), "Core", font=wf, fill=WHITE)
x += d.textlength("Core", font=wf)
d.text((x, y_word), "magna", font=wf, fill=TEAL)

# tagline
tagline = "AI chatbots, voice agents & automation for"
tagline2 = "law firms, clinics, real estate & service businesses"
d.text((PAD, 380), tagline, font=reg(38), fill=WHITE)
d.text((PAD, 432), tagline2, font=reg(38), fill=MUTED)

# url
d.text((PAD, 520), "coremagna.com", font=bold(30), fill=TEAL)

img.save("images/og.jpg", "JPEG", quality=88)
print("saved images/og.jpg", img.size)
