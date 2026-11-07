from PIL import Image, ImageDraw, ImageFont
import os

font_paths = [
    "/system/fonts/Roboto-Bold.ttf",
    "/system/fonts/Roboto-Regular.ttf",
    "/system/fonts/NotoSansCJK-Bold.ttc",
    "/system/fonts/NotoSansCJK-Regular.ttc",
    "/system/fonts/DroidSansFallback.ttf",
    "/system/fonts/DroidSans.ttf"
]
font_path = None
for p in font_paths:
    if os.path.exists(p):
        font_path = p
        break

img = Image.new("RGBA", (800, 160), (255, 255, 255, 0))
d = ImageDraw.Draw(img)
if font_path:
    font = ImageFont.truetype(font_path, 95)
    font_w = ImageFont.truetype(font_path, 120)
else:
    font = ImageFont.load_default()
    font_w = ImageFont.load_default()

x, y = 20, 15
d.text((x+8, y+8), "W", font=font_w, fill=(0,0,0,255))
d.text((x, y), "W", font=font_w, fill="#ff9900", stroke_width=5, stroke_fill="#ffffff")
x += d.textlength("W", font=font_w) - 5

d.text((x+8, y+8), "orkbench", font=font, fill=(0,0,0,255))
d.text((x, y), "orkbench", font=font, fill="#000000", stroke_width=5, stroke_fill="#007bff")
x += d.textlength("orkbench", font=font) + 15

note_img = Image.new("RGBA", (300, 150), (255,255,255,0))
nd = ImageDraw.Draw(note_img)
nd.text((8, 8), "Note", font=font, fill="#ff9900")
nd.text((0, 0), "Note", font=font, fill="#000000", stroke_width=5, stroke_fill="#007bff")
note_img = note_img.rotate(-8, expand=1, resample=Image.BICUBIC)
img.alpha_composite(note_img, (int(x), int(y-10)))

os.makedirs("public/images", exist_ok=True)
img.save("public/images/logo.png")
print("ロゴ画像を生成しました！")
