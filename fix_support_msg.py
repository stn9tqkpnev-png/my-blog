import pathlib
p_dir = pathlib.Path("src/content/blog")
for p in p_dir.glob("*.mdx"):
    s = p.read_text(encoding="utf-8")
    s = s.replace("<SupportMessage />\n\n", "").replace("<SupportMessage />\n", "").replace("<SupportMessage />", "")
    s = s.replace("import SupportMessage from \"../../components/SupportMessage.astro\";\n", "").replace("import SupportMessage from \"../../components/SupportMessage.astro\";", "")
    s = s.replace("import AffiliateCard from \"../../components/AffiliateCard.astro\";", "import AffiliateCard from \"../../components/AffiliateCard.astro\";\nimport SupportMessage from \"../../components/SupportMessage.astro\";")
    idx_read = s.rfind("## あわせて読みたい")
    idx_aff = s.rfind("<div style=\"margin: 40px 0; text-align: center;\">")
    idx_item = s.rfind("## あわせて使いたいアイテム")
    indices = [i for i in [idx_read, idx_aff, idx_item] if i != -1]
    if indices:
        insert_idx = min(indices)
        s = s[:insert_idx] + "<SupportMessage />\n\n" + s[insert_idx:]
    else:
        s = s.strip() + "\n\n<SupportMessage />\n"
    p.write_text(s, encoding="utf-8")
print("全記事のSupportMessageを、本文終了直後（末尾アフィリエイトの上）に移動しました！")
