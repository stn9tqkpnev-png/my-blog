from PIL import Image, ImageDraw, ImageFont
import os
img = Image.new("RGB", (600, 800), color="white")
d = ImageDraw.Draw(img)
font_paths = ["/system/fonts/NotoSansCJK-Bold.ttc", "/system/fonts/NotoSansCJK-Regular.ttc", "/system/fonts/DroidSansJapanese.ttf"]
font_large = None
for fp in font_paths:
    if os.path.exists(fp):
        try:
            font_large = ImageFont.truetype(fp, 36)
            font_small = ImageFont.truetype(fp, 18)
            break
        except:
            pass
if not font_large:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()
y_offset = 40
designs = ["1. アイコン + テキスト（現在案）", "2. シンプルテキスト（青）", "3. 枠線付き（バッジ風）", "4. 2色使い（Workbench=青, Note=黒）", "5. 下線付き（シンプル）"]
for i, text in enumerate(designs):
    d.text((40, y_offset), text, fill="gray", font=font_small)
    logo_y = y_offset + 40
    if i == 0:
        d.rectangle([40, logo_y+8, 55, logo_y+23], fill="#2b569a")
        d.text((65, logo_y), "Workbench Note", fill="black", font=font_large)
    elif i == 1:
        d.text((40, logo_y), "Workbench Note", fill="#2b569a", font=font_large)
    elif i == 2:
        d.rectangle([35, logo_y-5, 380, logo_y+45], outline="#2b569a", width=3)
        d.text((55, logo_y), "Workbench Note", fill="#2b569a", font=font_large)
    elif i == 3:
        d.text((40, logo_y), "Workbench ", fill="#2b569a", font=font_large)
        w = d.textlength("Workbench ", font=font_large)
        d.text((40 + w, logo_y), "Note", fill="black", font=font_large)
    elif i == 4:
        d.text((40, logo_y), "Workbench Note", fill="black", font=font_large)
        d.line([40, logo_y+50, 320, logo_y+50], fill="#2b569a", width=4)
    y_offset += 140
save_path = os.path.expanduser("~/storage/downloads/logo_designs.png")
if not os.path.exists(os.path.dirname(save_path)):
    save_path = os.path.expanduser("~/logo_designs.png")
    print("ダウンロードフォルダが見つからないため、ホームディレクトリに保存します。")
img.save(save_path)
print(f"画像を保存しました: {save_path}")
