import pathlib
p = pathlib.Path("src/layouts/BlogPost.astro")
s = p.read_text(encoding="utf-8")
s = s.replace("<Image width={1020} height={510} src={heroImage} alt=\"\" />", "<Image src={heroImage} alt=\"\" />")
s = s.replace(".hero-image img {\n\t\t\t\t\t\t\t\tdisplay: block;\n\t\t\t\t\t\t\t\tmargin: 0 auto;\n\t\t\t\t\t\t\t\tborder-radius: 12px;\n\t\t\t\t\t\t\t\tbox-shadow: var(--box-shadow);\n\t\t\t\t\t\t\t}", ".hero-image img {\n\t\t\t\t\t\t\t\twidth: 100%;\n\t\t\t\t\t\t\t\theight: auto;\n\t\t\t\t\t\t\t\tdisplay: block;\n\t\t\t\t\t\t\t\tmargin: 0 auto;\n\t\t\t\t\t\t\t\tborder-radius: 12px;\n\t\t\t\t\t\t\t\tbox-shadow: var(--box-shadow);\n\t\t\t\t\t\t\t}")
p.write_text(s, encoding="utf-8")
print("ヒーロー画像のレスポンシブ化修正が完了しました！")
