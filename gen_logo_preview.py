from PIL import Image, ImageDraw, ImageFont
import os

img = Image.new("RGB", (500, 120), color="white")
d = ImageDraw.Draw(img)

font_paths = ["/system/fonts/NotoSansCJK-Bold.ttc", "/system/fonts/DroidSansFallback.ttf"]
font_large = None
for fp in font_paths:
    if os.path.exists(fp):
        try:
            font_large = ImageFont.truetype(fp, 60)
            break
        except:
            pass
if not font_large:
    font_large = ImageFont.load_default()

def draw_text_with_shadow(draw, pos, text, fill, font):
    x, y = pos
    draw.text((x+3, y+3), text, font=font, fill=(0,0,0,50), stroke_width=3, stroke_fill="white")
    draw.text((x, y), text, font=font, fill=fill, stroke_width=3, stroke_fill="white")

current_x = 20
y = 20

# Work
draw_text_with_shadow(d, (current_x, y), "Work", "#2b569a", font_large)
current_x += d.textlength("Work", font=font_large) - 5

# bench
draw_text_with_shadow(d, (current_x, y), "bench", "#4a90e2", font_large)
current_x += d.textlength("bench", font=font_large)

# Note (Rotation)
note_img = Image.new("RGBA", (200, 100), (255, 255, 255, 0))
d_note = ImageDraw.Draw(note_img)
draw_text_with_shadow(d_note, (10, 10), "Note", "#ff9900", font_large)
note_img = note_img.rotate(-5, expand=1, resample=Image.BICUBIC)
img.paste(note_img, (int(current_x), y-20), note_img)

save_path = os.path.expanduser("~/storage/downloads/logo_preview.png")
if not os.path.exists(os.path.dirname(save_path)):
    save_path = os.path.expanduser("~/logo_preview.png")

img.save(save_path)
print(f"ロゴプレビューを保存しました: {save_path}")
