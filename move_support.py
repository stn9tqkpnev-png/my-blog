import pathlib
p_layout = pathlib.Path("src/layouts/BlogPost.astro")
s = p_layout.read_text(encoding="utf-8")
s = s.replace("import SupportMessage from \"../components/SupportMessage.astro\";\n", "")
s = s.replace("<SupportMessage />\n\t\t\t<slot />", "<slot />")
s = s.replace("<slot />\n\t\t\t<SupportMessage />", "<slot />")
p_layout.write_text(s, encoding="utf-8")
p_dir = pathlib.Path("src/content/blog")
for p in p_dir.glob("*.mdx"):
    s = p.read_text(encoding="utf-8")
    if "SupportMessage" in s:
        continue
    s = s.replace("import AffiliateCard from \"../../components/AffiliateCard.astro\";", "import AffiliateCard from \"../../components/AffiliateCard.astro\";\nimport SupportMessage from \"../../components/SupportMessage.astro\";")
    target = "<div style=\"margin: 40px 0; text-align: center;\">"
    if target in s:
        s = s.replace(target, "<SupportMessage />\n\n" + target, 1)
    else:
        target2 = "## あわせて読みたい"
        if target2 in s:
            s = s.replace(target2, "<SupportMessage />\n\n" + target2, 1)
        else:
            s += "\n\n<SupportMessage />\n"
    p.write_text(s, encoding="utf-8")
print("各記事の末尾にSupportMessageを移動しました！")
