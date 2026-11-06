import pathlib
p = pathlib.Path("src/content/blog/sesame-watch-unlock.mdx")
s = p.read_text(encoding="utf-8")

# 末尾のアフィリエイトブロックを一旦削除
import re
s = re.sub(r"<div style=\"margin: 40px 0; text-align: center;\">\n<AffiliateCard url=\"https://www.amazon.co.jp/dp/B0HFQQ51B6.*?</div>\n", "", s, flags=re.DOTALL)
s = re.sub(r"---\n\n<div style=\"margin: 40px 0; text-align: center;\">\n<AffiliateCard url=\"https://www.amazon.co.jp/dp/B09GVSC3CK.*?</div>\n", "", s, flags=re.DOTALL)

# 準備するもの の直後にSESAME 5とT-Rex 3のリンクを挿入
prereq_end = "※ミニアプリ「HTTP」は、第三者(作者: galulex 氏)が開発した Amazfit 用のアプリです。アプリ内課金があります。利用は自己責任でお願いします。"
new_prereq = prereq_end + "\n\n<div style=\"margin: 20px 0; text-align: center; display: flex; gap: 20px; flex-wrap: wrap; justify-content: center;\">\n  <div style=\"flex: 1; min-width: 250px;\">\n    <AffiliateCard url=\"https://www.amazon.co.jp/s?k=SESAME+5&tag=workbenchnote-22\" image=\"/images/sesame5.avif\" title=\"SESAME 5 スマートロック\" />\n  </div>\n  <div style=\"flex: 1; min-width: 250px;\">\n    <AffiliateCard url=\"https://link.amazon/B0eCn4zla\" image=\"/images/amazon-trex3.avif\" title=\"Amazfit T-Rex 3 スマートウォッチ\" />\n  </div>\n</div>\n"
s = s.replace(prereq_end, new_prereq)

# 手順1 SESAMEの準備の直後にドアセンサーとHub3のリンクを挿入
step1_end = "この手順は、CANDY HOUSE が公開している情報と、有志の方が公開している資料をもとにしています。画面の表示やメニュー名は、変更されている場合があります。"
new_step1 = step1_end + "\n\n<div style=\"margin: 20px 0; text-align: center; display: flex; gap: 20px; flex-wrap: wrap; justify-content: center;\">\n  <div style=\"flex: 1; min-width: 250px;\">\n    <AffiliateCard url=\"https://www.amazon.co.jp/dp/B0D59WGSQB/ref=cm_sw_r_as_gl_apa_gl_i_YSKBAFJ4KCXP0BHC7H7E?linkCode=ml1&tag=workbenchnote-22&linkId=013588cc67cd49f82a8b3870e15d0887\" image=\"/images/sesame-hub3.avif\" title=\"SESAME Hub3 (スマートリモコン)\" />\n  </div>\n  <div style=\"flex: 1; min-width: 250px;\">\n    <AffiliateCard url=\"https://www.amazon.co.jp/dp/B0BFDRWHJB/ref=cm_sw_r_as_gl_apa_gl_i_F0TCNP1SNANGNX9XWFBM?linkCode=ml1&tag=workbenchnote-22&linkId=ec4cccd82c000888061b84cf8f56e542\" image=\"/images/sesame-door-sensor.avif\" title=\"エジソンスマート ドアセンサー\" />\n  </div>\n</div>\n"
s = s.replace(step1_end, new_step1)

# まとめの直前にバンパーと電池のリンクを配置
summary_end = "時計のアプリから HTTP リクエストを送り、GAS で受け取ることで、サーバーなしで SESAME 5 を腕時計から操作できました。使う前に、漏えいしたときの対応手順を決めておくことをおすすめします。"
new_summary = summary_end + "\n\n<div style=\"margin: 40px 0; text-align: center; display: flex; gap: 20px; flex-wrap: wrap; justify-content: center;\">\n  <div style=\"flex: 1; min-width: 250px;\">\n    <AffiliateCard url=\"https://www.amazon.co.jp/dp/B09GVSC3CK/ref=cm_sw_r_as_gl_apa_gl_i_1AE38G9WRHAY3DX7F1B4?linkCode=ml1&tag=workbenchnote-22&linkId=b6ba8ac30d9fcd0f5672189495749dd1\" image=\"/images/sesame-mid-card.avif\" title=\"SESAME用 交換電池（CR123A）\" />\n  </div>\n  <div style=\"flex: 1; min-width: 250px;\">\n    <AffiliateCard url=\"https://www.amazon.co.jp/dp/B0HFQQ51B6?tag=workbenchnote-22\" image=\"/images/amazon-item.webp\" title=\"T-Rex 2用 バンパーカバー\" />\n  </div>\n</div>\n"
s = s.replace(summary_end, new_summary)

p.write_text(s, encoding="utf-8")
print("記事のアフィリエイト配置を最適化しました！")
