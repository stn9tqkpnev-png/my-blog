import pathlib, re
p_dir = pathlib.Path("src/content/blog")
targets = {
    "amazfit-trex2-bumper.mdx": "## まとめ：最初から付けておけばよかった",
    "sesame-watch-unlock.mdx": "## 手順1 SESAME の準備をする",
    "sesame5-3years-review.mdx": "## 総合評価：コスパ最強。次もSESAMEを選びます",
    "trex2-band-review.mdx": "## 【T-Rex 2】バンド交換の落とし穴",
    "trex2-protective-film.mdx": "## 2つのサイズを重ねて比較してみた",
    "trex2-review.mdx": "## 総合評価：コスパ最強。それでもT-Rex 3に買い替えたい理由"
}
for p in p_dir.glob("*.mdx"):
    s = p.read_text(encoding="utf-8")
    s = re.sub(r"<SupportMessage />\s*", "", s)
    s = re.sub(r"import SupportMessage.*?\n", "", s)
    p.write_text(s, encoding="utf-8")
for filename, heading in targets.items():
    p = p_dir / filename
    if not p.exists(): continue
    s = p.read_text(encoding="utf-8")
    if "import SupportMessage" not in s:
        if "import AffiliateCard" in s:
            s = s.replace("import AffiliateCard from \"../../components/AffiliateCard.astro\";", "import AffiliateCard from \"../../components/AffiliateCard.astro\";\nimport SupportMessage from \"../../components/SupportMessage.astro\";")
        elif "import RelatedArticle" in s:
            s = s.replace("import RelatedArticle from \"../../components/RelatedArticle.astro\";", "import RelatedArticle from \"../../components/RelatedArticle.astro\";\nimport SupportMessage from \"../../components/SupportMessage.astro\";")
        else:
            s = s.replace("---\n\n", "---\nimport SupportMessage from \"../../components/SupportMessage.astro\";\n\n", 1)
    if heading in s:
        s = s.replace(heading, "<SupportMessage />\n\n" + heading, 1)
    else:
        s = s.rstrip() + "\n\n<SupportMessage />\n"
    p.write_text(s, encoding="utf-8")
print("記事ごとに最適な位置へSupportMessageを移動しました！")
