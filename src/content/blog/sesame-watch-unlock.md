---
title: "スマートウォッチでSESAME 5を解錠・施錠する方法(Amazfit T-Rex 2・サーバー不要)"
description: "Amazfit T-Rex 2とミニアプリ「HTTP」、そしてGASを使って、サーバーなしでSESAME 5を腕時計から操作する方法を解説します。セキュリティ対策も解説。"
pubDate: "Oct 31 2026"
heroImage: "../../assets/hero-watch-lock-unlock.jpg"
---

腕時計のボタンをタップするだけで、自宅の SESAME 5 を解錠・施錠する方法を紹介します。使うのは、Amazfit T-Rex 2 と、Amazfit の時計で動くミニアプリ「HTTP」です。

「HTTP」アプリは、時計から HTTP リクエストを送れるミニアプリです。送り先と内容を一度設定しておけば、時計のボタンを押すだけで、そのリクエストを送ってくれます。

「HTTP」アプリが動く Amazfit の時計なら、T-Rex 2 以外でも同じ方法でできます。

HTTP リクエストを受け取る側には、本来はサーバーが必要です。この記事では、Google Apps Script(GAS)を使うことで、サーバーを用意せずに実現します。

**注意**: この記事の内容は、玄関の鍵を操作するものです。APIキーやシークレットキーなどの秘密情報は、記事や GitHub に絶対に載せないでください。

## 仕組み

- **時計の「HTTP」アプリ**: ボタンを押すと、リクエストを送る
- **GAS**: リクエストを受け取る中継役。SESAME の API に命令を送る
- **SESAME Web API**: クラウド経由で SESAME 5 を動かす

## この記事でやること

1. SESAME の準備をする
2. GAS にコードを入れる
3. GAS を Web アプリとして公開する
4. 時計に「HTTP」アプリを入れる
5. 解錠・施錠のボタンを作る
6. 時計で試す

## 準備するもの

- SESAME 5 と Wi-Fiモジュール2(SESAME 5 がインターネットにつながっている状態にしておく必要があります)
- SESAME アプリ(SESAME 5 を登録済みのもの)
- Amazfit T-Rex 2 と、Zepp アプリを入れたスマホ
- Google アカウント
- パソコン(なくても可能ですが、GAS の画面はパソコンのほうが操作しやすいです)

※ミニアプリ「HTTP」は、第三者(作者: galulex 氏)が開発した Amazfit 用のアプリです。アプリ内課金があります。利用は自己責任でお願いします。

## 手順1 SESAME の準備をする

GAS から SESAME を動かすために、次の3つの情報が必要です。

- **APIキー**: SESAME の Web API を使うための鍵
- **UUID**: 操作する SESAME を指定する ID
- **シークレットキー**: 命令に署名するための鍵

この手順は、CANDY HOUSE が公開している情報と、有志の方が公開している資料をもとにしています。画面の表示やメニュー名は、変更されている場合があります。

### A. APIキーを取得する

APIキーは、CANDY HOUSE の法人向けサービス「SESAME Biz」の、開発者向けのページで取得します。

1. スマホやパソコンのブラウザで、「biz.candyhouse.co」を開きます。
2. メールアドレスを入力して、ログインします。
3. ログインしたら、画面の左上にあるメニューを開きます。
4. メニューの中から、「開発者向け」を選びます。
5. 表示されたページで、APIキーをコピーします。
6. コピーしたAPIキーを、メモ帳などに控えます。

### B. シークレットキーと UUID を取得する

この2つは、SESAME アプリの「鍵のシェア」で表示される QR コードから取り出します。

1. スマホの SESAME アプリを開き、SESAME 5 を選びます。
2. 「鍵をシェア」を選びます。メニュー名は、アプリのバージョンによって多少異なります。
3. 鍵の種類は、「マネージャー」(または「オーナー」)を選びます。「ゲスト」の鍵では、取り出せません。
4. QR コードが表示されたら、スクリーンショットを撮ります。
5. ブラウザで、QR コード読み取りツール(`sesame-qr-reader.vercel.app`)を開きます。
6. 撮ったスクリーンショットを、ツールにアップロードします。
7. 読み取り結果に、「Secret Key」と「UUID」が表示されます。2つをコピーして、メモ帳などに控えます。
8. 控え終わったら、QR コードのスクリーンショットを削除します。「最近削除した項目」(ゴミ箱)からも、削除してください。

QR コードは、鍵そのものです。他人に見せたり、ネットに載せたりしないでください。この記事に QR コードの画像を載せていないのも、そのためです。

UUID は、SESAME アプリのデバイス情報の画面でも、確認できます。

### C. 3つの情報を確認する

3つとも、メモ帳などに控えたら、手順1は完了です。人に見せたり、ネットに載せたりしないでください。

## 手順2 GAS にコードを入れる

ブラウザで `script.google.com` を開き、Google アカウントでログインします。

1. 「新しいプロジェクト」をクリックします。
2. 左上の「無題のプロジェクト」をクリックして、「SESAME」など、わかりやすい名前に変えます。
3. エディタに最初から入っているコードを、すべて削除します。
4. 次のコードを貼り付けます。

```javascript
const API_KEY = "あなたのAPIキー";
const UUID = "あなたのUUID";
const SECRET_KEY = "あなたのシークレットキー";

function doGet(e) {
  const action = e && e.parameter ? e.parameter.action : null;
  if (action === "unlock") {
    return unlockDoor();
  } else if (action === "lock") {
    return lockDoor();
  } else {
    return ContentService.createTextOutput("Usage: add ?action=unlock or ?action=lock").setMimeType(ContentService.MimeType.TEXT);
  }
}

function unlockDoor() {
  const res = sendCommand(83, "GAS Unlock");
  return ContentService.createTextOutput("Unlock result: " + res.getResponseCode()).setMimeType(ContentService.MimeType.TEXT);
}

function lockDoor() {
  const res = sendCommand(82, "GAS Lock");
  return ContentService.createTextOutput("Lock result: " + res.getResponseCode()).setMimeType(ContentService.MimeType.TEXT);
}

function sendCommand(cmd, historyText) {
  const url = "https://app.candyhouse.co/api/sesame2/" + UUID + "/cmd";
  const historyName = Utilities.base64Encode(historyText);
  const data = { cmd: cmd, history: historyName, sign: getSign(SECRET_KEY) };
  const options = {
    method: "post",
    contentType: "application/json",
    headers: { "x-api-key": API_KEY },
    payload: JSON.stringify(data),
    muteHttpExceptions: true
  };
  return UrlFetchApp.fetch(url, options);
}

function getSign(secretKeyHex) {
  const sk = hexToBytes(secretKeyHex);
  const now = Math.floor(new Date().getTime() / 1000);
  const ts = [(now >>> 8) & 0xff, (now >>> 16) & 0xff, (now >>> 24) & 0xff];
  return bytesToHex(aesCmac(sk, ts));
}

function hexToBytes(hex) { const bytes = []; for (let i = 0; i < hex.length; i += 2) bytes.push(parseInt(hex.substr(i, 2), 16)); return bytes; }
function bytesToHex(bytes) { return bytes.map(function(b) { return ("0" + (b & 0xff).toString(16)).slice(-2); }).join(""); }
function xorBytes(a, b) { const out = new Array(a.length); for (let i = 0; i < a.length; i++) out[i] = a[i] ^ b[i]; return out; }
const SBOX = [0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76,0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0,0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15,0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75,0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84,0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf,0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8,0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2,0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73,0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb,0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79,0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08,0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a,0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e,0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf,0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16];
const RCON = [0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0x1b,0x36];
function rotWord(word) { return [word[1], word[2], word[3], word[0]]; }
function subWord(word) { return word.map(function(b) { return SBOX[b]; }); }
function keyExpansion(key) {
  const Nk = 4, Nb = 4, Nr = 10;
  const w = [];
  for (let i = 0; i < Nk; i++) w[i] = [key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3]];
  for (let i = Nk; i < Nb * (Nr + 1); i++) {
    let temp = w[i - 1].slice();
    if (i % Nk === 0) { temp = subWord(rotWord(temp)); temp[0] ^= RCON[i / Nk - 1]; }
    w[i] = w[i - Nk].map(function(b, idx) { return b ^ temp[idx]; });
  }
  return w;
}
function addRoundKey(state, w, round) { for (let c = 0; c < 4; c++) { const word = w[round * 4 + c]; for (let r = 0; r < 4; r++) state[c * 4 + r] ^= word[r]; } }
function subBytes(state) { for (let i = 0; i < 16; i++) state[i] = SBOX[state[i]]; }
function shiftRows(state) { const s = state.slice(); for (let r = 1; r < 4; r++) { for (let c = 0; c < 4; c++) { state[c * 4 + r] = s[(((c + r) % 4) * 4) + r]; } } }
function mulGF(a, b) { let p = 0; for (let i = 0; i < 8; i++) { if (b & 1) p ^= a; const hi = a & 0x80; a = (a << 1) & 0xff; if (hi) a ^= 0x1b; b >>= 1; } return p & 0xff; }
function mixColumns(state) { for (let c = 0; c < 4; c++) { const a0 = state[c * 4], a1 = state[c * 4 + 1], a2 = state[c * 4 + 2], a3 = state[c * 4 + 3]; state[c * 4] = mulGF(a0, 2) ^ mulGF(a1, 3) ^ a2 ^ a3; state[c * 4 + 1] = a0 ^ mulGF(a1, 2) ^ mulGF(a2, 3) ^ a3; state[c * 4 + 2] = a0 ^ a1 ^ mulGF(a2, 2) ^ mulGF(a3, 3); state[c * 4 + 3] = mulGF(a0, 3) ^ a1 ^ a2 ^ mulGF(a3, 2); } }
function aesEncryptBlock(input, key) {
  const state = input.slice();
  const w = keyExpansion(key);
  const Nr = 10;
  addRoundKey(state, w, 0);
  for (let round = 1; round < Nr; round++) { subBytes(state); shiftRows(state); mixColumns(state); addRoundKey(state, w, round); }
  subBytes(state); shiftRows(state); addRoundKey(state, w, Nr);
  return state;
}
function leftShift1(input) { const output = new Array(16); let overflow = 0; for (let i = 15; i >= 0; i--) { output[i] = ((input[i] << 1) | overflow) & 0xff; overflow = (input[i] & 0x80) ? 1 : 0; } return output; }
function generateSubkeys(key) { const zero = new Array(16).fill(0); const L = aesEncryptBlock(zero, key); let K1 = leftShift1(L); if (L[0] & 0x80) K1[15] ^= 0x87; let K2 = leftShift1(K1); if (K1[0] & 0x80) K2[15] ^= 0x87; return [K1, K2]; }
function padBlock(block) { const padded = block.slice(); padded.push(0x80); while (padded.length < 16) padded.push(0x00); return padded; }
function aesCmac(key, message) { const subkeys = generateSubkeys(key); const K1 = subkeys[0], K2 = subkeys[1]; const blockSize = 16; let n = Math.ceil(message.length / blockSize); let flag; if (n === 0) { n = 1; flag = false; } else { flag = (message.length % blockSize === 0); } const blocks = []; for (let i = 0; i < n - 1; i++) blocks.push(message.slice(i * blockSize, (i + 1) * blockSize)); const lastBlock = message.slice((n - 1) * blockSize); let mLast; if (flag) mLast = xorBytes(lastBlock, K1); else mLast = xorBytes(padBlock(lastBlock), K2); let X = new Array(16).fill(0); for (let i = 0; i < blocks.length; i++) X = aesEncryptBlock(xorBytes(X, blocks[i]), key); return aesEncryptBlock(xorBytes(mLast, X), key); }
```

5. 画面上部のディスクのアイコンで、保存します。

## 手順3 GAS を Web アプリとして公開する

1. 画面右上の「デプロイ」から「新しいデプロイ」を選びます。
2. 種類の歯車アイコンから「ウェブアプリ」を選びます。
3. 「次のユーザーとして実行」は「自分」にします。
4. 「アクセスできるユーザー」は「全員」にします。時計のアプリは、Google にログインしていないためです。
5. 「デプロイ」を押し、初めての場合に出る権限の承認画面で、許可します。
6. 表示された「ウェブアプリ」の URL をコピーして、メモ帳などに控えます。手順5で使います。

※コードを書き換えたときは、「デプロイを管理」から新しいバージョンに更新しないと、公開中のものに反映されません。

## 手順4 時計に「HTTP」アプリを入れる

1. スマホで Zepp アプリを開きます。
2. T-Rex 2 のアプリストアを開きます。
3. アプリストアで「ユーティリティ」のカテゴリを開き、「HTTP」を検索します。作者が「galulex」のものです。
4. インストールします。

## 手順5 解錠・施錠のボタンを作る

「HTTP」アプリの設定は、Zepp アプリから行います。時計のボタンひとつにつき、リクエストをひとつ設定します。解錠用と施錠用の、2つを作ります。

1. Zepp アプリで、「HTTP」アプリの設定画面を開きます。
2. カスタムアクションを追加します。
3. 次の表のとおりに入力します。

**TITLE**
`UNLOCK` （施錠用を作る場合は `LOCK`）

**METHOD**
`GET`

**URL**
手順3でコピーしたURLの**一番最後**に、以下の文字を追加して入力します。
（解錠用）`?action=unlock`
（施錠用）`?action=lock`

※入力例: `https://script.google.com/macros/s/xxxx/exec?action=unlock`

**HEADERS**
空欄のまま

**BODY**
空欄のまま

アプリの説明では、1画面に1〜4個のボタンを並べられます。無料版で作れるアクションの数には、上限があります。上限を超える場合は、有料の Pro が必要です。

## 手順6 時計で試す

まず、動きを目で確認しやすい「施錠」から試します。
1. 時計で「HTTP」アプリを開き、施錠のボタンをタップします。
2. SESAME が動いたかを、目で見て確認します。SESAME アプリで、状態を見ても構いません。
3. 問題なければ、解錠も試します。

## うまく動かないとき

- Web アプリの URL が、正しくコピーできているか確認します。
- コードを書き換えた場合は、「デプロイを管理」で新しいバージョンに更新したか確認します。
- SESAME 5 が、Wi-Fiモジュール2を通じてインターネットにつながっているか確認します。
- 画面に結果が「成功」と出ても、実際に鍵が動いたとは限りません。SESAME アプリで状態を確認してください。

## セキュリティ上の注意

**Web アプリの URL は、玄関の鍵と同じです。** 他人に知られると、誰でも解錠できる可能性があります。

- URLは、推測されにくい長いランダム文字列にします。（※GASのURL自体が長いランダム文字列になっています）
- 秘密情報は、記事や GitHub に実際の値を載せません。
- 漏れたかもしれないときは、デプロイを削除して作り直します。SESAME の APIキーも、必要に応じて再発行します。
- **万が一に備え、URLは絶対にSNSやブログに公開せず、厳重に管理してください。**

## まとめ

時計のアプリから HTTP リクエストを送り、GAS で受け取ることで、サーバーなしで SESAME 5 を腕時計から操作できました。使う前に、漏えいしたときの対応手順を決めておくことをおすすめします。

<div style="text-align: center; margin: 40px 0;">
  <a href="https://www.amazon.co.jp/s?k=SESAME+5&tag=workbenchnote-22" target="_blank" rel="noopener" style="display: block; max-width: 400px; margin: 0 auto; text-decoration: none; border: 1px solid #ddd; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); background-color: #fff !important;">
    <div style="background-color: #f3f3f3 !important; padding: 15px; border-bottom: 1px solid #ddd;">
      <span style="font-size: 14px; color: #555 !important;">＼ 関連商品 ／</span>
    </div>
    <div style="padding: 20px;">
      <img src="/images/sesame5.avif" alt="SESAME 5" style="max-width: 80%; height: auto; margin-bottom: 15px; border-radius: 8px;">
      <p style="color: #333 !important; font-weight: bold; margin: 0 0 15px 0; font-size: 16px;">SESAME 5 スマートロック</p>
      <div style="background-color: #ff9900 !important; color: #fff !important; padding: 12px 20px; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">
        Amazonで詳細を見る ▶
      </div>
    </div>
  </a>
</div>

<div style="margin: 40px 0; text-align: center;">
<div style="max-width: 400px; margin: 0 auto 20px auto; border: 1px solid #ddd; border-radius: 12px; overflow: hidden; background: #fff;"><a href="https://www.amazon.co.jp/dp/B0HFQQ51B6?tag=workbenchnote-22" target="_blank" rel="noopener" style="text-decoration: none; display: block; padding: 15px;"><img src="/images/amazon-item.webp" style="max-width: 80%; height: auto; border-radius: 8px; margin-bottom: 10px;" alt="T-Rex 2用 バンパーカバー"><p style="color: #333; font-weight: bold; margin: 0 0 10px 0;">T-Rex 2用 バンパーカバー</p><div style="background-color: #ff9900; color: #fff; padding: 10px 20px; border-radius: 8px; font-weight: bold; display: inline-block;">Amazonで詳細を見る ▶</div></a></div>
<div style="max-width: 400px; margin: 0 auto 20px auto; border: 1px solid #ddd; border-radius: 12px; overflow: hidden; background: #fff;"><a href="https://link.amazon/B0eCn4zla" target="_blank" rel="noopener" style="text-decoration: none; display: block; padding: 15px;"><img src="/images/amazon-trex3.avif" style="max-width: 80%; height: auto; border-radius: 8px; margin-bottom: 10px;" alt="Amazfit T-Rex 3"><p style="color: #333; font-weight: bold; margin: 0 0 10px 0;">Amazfit T-Rex 3 スマートウォッチ</p><div style="background-color: #ff9900; color: #fff; padding: 10px 20px; border-radius: 8px; font-weight: bold; display: inline-block;">Amazonで詳細を見る ▶</div></a></div>
<div style="max-width: 400px; margin: 0 auto; border: 1px solid #ddd; border-radius: 12px; overflow: hidden; background: #fff;"><a href="https://www.amazon.co.jp/s?k=SESAME+5&tag=workbenchnote-22" target="_blank" rel="noopener" style="text-decoration: none; display: block; padding: 15px;"><img src="/images/sesame5.avif" style="max-width: 80%; height: auto; border-radius: 8px; margin-bottom: 10px;" alt="SESAME 5"><p style="color: #333; font-weight: bold; margin: 0 0 10px 0;">SESAME 5 スマートロック</p><div style="background-color: #ff9900; color: #fff; padding: 10px 20px; border-radius: 8px; font-weight: bold; display: inline-block;">Amazonで詳細を見る ▶</div></a></div>
</div>

---

## あわせて読みたい

<div style="margin: 40px 0; text-align: center;">
  <a href="/blog/amazfit-trex2-bumper/" style="display: block; max-width: 400px; margin: 0 auto; text-decoration: none; border: 1px solid #ddd; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); background-color: #fff;">
    <img src="/images/amazfit-trex2-bumper-card.jpg" alt="T-Rex 2 バンパーカバー" style="width: 100%; height: 200px; object-fit: cover;">
    <div style="padding: 15px;">
      <p style="color: #333; font-weight: bold; margin: 0; font-size: 16px;">Amazfit T-Rex 2にAmazonのバンパーカバーを装着レビュー</p>
    </div>
  </a>
</div>