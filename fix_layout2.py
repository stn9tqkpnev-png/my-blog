import pathlib
p1 = pathlib.Path("src/layouts/BlogPost.astro")
s1 = p1.read_text(encoding="utf-8")
s1 = s1.replace("width: calc(100% - 2em);\n\t\t\t\t\t\tmax-width: 100%;\n\t\t\t\t\t\tmargin: 0 auto;", "width: 100%;\n\t\t\t\t\t\tmax-width: 100%;\n\t\t\t\t\t\tmargin: 0 auto;\n\t\t\t\t\t\tpadding: 0 1em;\n\t\t\t\t\t\tbox-sizing: border-box;")
p1.write_text(s1, encoding="utf-8")
p2 = pathlib.Path("src/styles/global.css")
s2 = p2.read_text(encoding="utf-8")
if "overflow-x: hidden;" not in s2:
    s2 = s2.replace("body {\n  margin: 0;\n  padding: 0;", "body {\n  margin: 0;\n  padding: 0;\n  overflow-x: hidden;")
p2.write_text(s2, encoding="utf-8")
print("レイアウトのはみ出し修正が完了しました！")
