import pathlib
p = pathlib.Path("src/content/blog/amazfit-trex2-bumper.mdx")
s = p.read_text(encoding="utf-8")

target = "<div style=\"margin: 40px 0; text-align: center;\">\n<AffiliateCard url=\"https://www.amazon.co.jp/dp/B0HFQQ51B6?tag=workbenchnote-22\" image=\"/images/amazon-item.webp\" title=\"T-Rex 2用 バンパーカバー\" />"

addition = """## あわせて使いたいアイテム

<div style="margin: 40px 0; text-align: center; display: flex; gap: 20px; flex-wrap: wrap; justify-content: center;">
  <div style="flex: 1; min-width: 250px;">
    <AffiliateCard url="https://www.amazon.co.jp/dp/B0B2RCFXX6/ref=cm_sw_r_as_gl_apa_gl_i_F17BJG3CT3Y9S1K0QVNJ?linkCode=ml1&tag=workbenchnote-22&linkId=a9d36f09f38ed7cd1e2ececddeee31fb" image="/images/trex2-film-perfect.avif" title="T-Rex 2用 保護フィルム（画面いっぱいタイプ）" />
  </div>
  <div style="flex: 1; min-width: 250px;">
    <AffiliateCard url="https://ja.aliexpress.com/item/1005009240238149.html?srcSns=sns_Copy&businessType=ProductDetail&spreadType=socialShare&aff_fcid=55946cc6a36d4617b6cc46c180d5858c-1793620945521-09722-_c3BSiN6n&tt=CPS_NORMAL&aff_fsk=_c3BSiN6n&aff_platform=shareComponent-detail&sk=_c3BSiN6n&aff_trace_key=55946cc6a36d4617b6cc46c180d5858c-1793620945521-09722-_c3BSiN6n&terminal_id=041fee096f2a4a3999a8d93fe4a4d28f&afSmartRedirect=y" image="/images/aliexpress-trex2-band.webp" title="Amazfit T-Rex 2用 交換用シリコンバンド" buttonText="AliExpressで詳細を見る ▶" />
  </div>
</div>



"""

if target in s and "あわせて使いたいアイテム" not in s:
    s = s.replace(target, addition + target)
    p.write_text(s, encoding="utf-8")
    print("バンパーカバー記事にバンドとフィルムのアフィリエイトを追加しました！")
else:
    print("対象の文字列が見つからないか、すでに追加されています。")
