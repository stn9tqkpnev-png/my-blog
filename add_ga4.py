import pathlib
p = pathlib.Path("src/components/BaseHead.astro")
s = p.read_text(encoding="utf-8")
ga4_tag = """
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-70RQKLN2LT"></script>
<script is:inline>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-70RQKLN2LT');
</script>
"""
if "G-70RQKLN2LT" not in s:
    s = s.replace("</head>", "")
    s = s + "\n" + ga4_tag
    p.write_text(s, encoding="utf-8")
    print("GA4タグを追加しました！")
else:
    print("GA4タグはすでに追加されています。")
