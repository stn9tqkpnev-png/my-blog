import pathlib
p = pathlib.Path("src/layouts/BlogPost.astro")
s = p.read_text(encoding="utf-8")
s = s.replace("max-width: 100%;\n\t\t\t\t\t\tmargin: 0;", "max-width: 100%;\n\t\t\t\t\t\tmargin: 0 auto;")
p.write_text(s, encoding="utf-8")
print("レイアウトの中央揃え修正が完了しました！")
