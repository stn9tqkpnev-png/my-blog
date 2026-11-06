import pathlib
p=pathlib.Path("src/content/blog")
repls={
  "amazfit-trex2-bumper.mdx": [
    ("![装着イメージ1]", "![T-Rex 2にバンパーカバーを装着した手元の様子1]"),
    ("![装着イメージ2]", "![T-Rex 2にバンパーカバーを装着した手元の様子2]"),
    ("![バンパーカバー装着時の様子]", "![T-Rex 2用バンパーカバーを装着した正面の様子]"),
    ("![側面の様子1]", "![バンパーカバーを装着したT-Rex 2の側面1]"),
    ("![側面の様子2]", "![バンパーカバーを装着したT-Rex 2の側面2]")
  ],
  "sesame5-3years-review.mdx": [
    ("![ドアセンサー]", "![SESAMEのドアセンサーを取り付けた様子]"),
    ("![Echo Dot]", "![SESAMEと連携しているEcho Dot]"),
    ("![Fire TV Cube]", "![SESAMEと連携しているFire TV Cube]"),
    ("![SESAME Wi-Fiモジュール2]", "![SESAME Wi-Fiモジュール2の外観]"),
    ("![電池ボックス（EVE電池）]", "![SESAME 5の電池ボックスとEVE電池]"),
    ("![ドアポストの内側]", "![スペアキーを吊るしたドアポストの内側]"),
    ("![吊るされたスペアキー]", "![ドアポストの内側に吊るしたスペアキー]")
  ],
  "trex2-band-review.mdx": [
    ("![これまでに試してきたバンドの数々]", "![T-Rex 2用にこれまで試してきたシリコンバンドの数々]"),
    ("![金属の留め具の塗装剥がれ]", "![T-Rex 2用バンドの金属留め具の塗装剥がれ]"),
    ("![プラスチック製の止め具]", "![純正バンドから取り外したプラスチック製の止め具]"),
    ("![専用工具の写真]", "![T-Rex 2のバンド交換用Y字ネジと専用工具]")
  ],
  "trex2-protective-film.mdx": [
    ("![2つのフィルムを重ねた比較画像]", "![少し小さいタイプと画面いっぱいタイプの保護フィルムを重ねた比較]"),
    ("![付属品一式]", "![保護フィルムに付属していたクリーニングキット一式]")
  ]
}
for f, tuples in repls.items():
  fp = p / f
  if fp.exists():
    txt = fp.read_text(encoding="utf-8")
    for old, new in tuples:
      txt = txt.replace(old, new)
    fp.write_text(txt, encoding="utf-8")
print("Alt属性の修正が完了しました！")
