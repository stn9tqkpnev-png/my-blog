import pathlib
p_dir = pathlib.Path("src/content/blog")
for p in p_dir.glob("*.mdx"):
    s = p.read_text(encoding="utf-8")
    s = s.replace("<SupportMessage />\n\n", "").replace("<SupportMessage />\n", "").replace("<SupportMessage />", "")
    s = s.replace("import SupportMessage from \"../../components/SupportMessage.astro\";\n", "")
    s = s.replace("import SupportMessage from \"../../components/SupportMessage.astro\";", "")
    target = "## あわせて読みたい"
    if target in s:
        s = s.replace(target, "<SupportMessage />\n\n" + target)
        if "import SupportMessage" not in s:
            if "import AffiliateCard" in s:
                s = s.replace("import AffiliateCard from \"../../components/AffiliateCard.astro\";", "import AffiliateCard from \"../../components/AffiliateCard.astro\";\nimport SupportMessage from \"../../components/SupportMessage.astro\";")
            elif "import RelatedArticle" in s:
                s = s.replace("import RelatedArticle from \"../../components/RelatedArticle.astro\";", "import RelatedArticle from \"../../components/RelatedArticle.astro\";\nimport SupportMessage from \"../../components/SupportMessage.astro\";")
    p.write_text(s, encoding="utf-8")
print("全記事で「あわせて読みたい」の直前に統一しました！")
