---
title: "スマートウォッチでSESAME 5を解錠・施錠する方法(Amazfit T-Rex 2・サーバー不要)"
description: "Amazfit T-Rex 2とミニアプリ「HTTP」、そしてGASを使って、サーバーなしでSESAME 5を腕時計から操作する方法を解説します。セキュリティ対策も解説。"
pubDate: "Oct 31 2026"
heroImage: "../../assets/hero-watch-lock-unlock.jpg"
---

# スマートウォッチでSESAME 5を解錠・施錠する方法

腕時計のボタンをタップするだけで、自宅の SESAME 5 を解錠・施錠する方法を紹介します。使うのは、Amazfit T-Rex 2 と、Amazfit の時計で動くミニアプリ「HTTP」です。

HTTP リクエストを受け取る側には、本来はサーバーが必要です。この記事では、Google Apps Script(GAS)を使うことで、サーバーを用意せずに実現します。

## 準備するもの

- SESAME 5 と Wi-Fiモジュール2
- SESAME アプリ(SESAME 5 を登録済みのもの)
- Amazfit T-Rex 2 と、Zepp アプリを入れたスマホ
- Google アカウント

## 手順1 SESAME の準備をする

GAS から SESAME を動かすために、APIキー、UUID、シークレットキーの3つの情報を取得します。
1. 「biz.candyhouse.co」にログインし、開発者向けページからAPIキーを取得します。
2. SESAMEアプリの「鍵をシェア」からQRコードを表示し、スクショを撮ります。
3. 「sesame-qr-reader.vercel.app」などのツールでQRコードを読み取り、Secret KeyとUUIDを取得します。

## 手順2 GAS にコードを入れる

ブラウザで `script.google.com` を開き、新しいプロジェクトを作成します。以下のコードを貼り付けてください。

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

## 手順3 GAS を Web アプリとして公開する

1. 画面右上の「デプロイ」から「新しいデプロイ」を選びます。
2. 種類の歯車アイコンから「ウェブアプリ」を選びます。
3. 「次のユーザーとして実行」は「自分」、「アクセスできるユーザー」は「全員」にします。
4. 「デプロイ」を押し、表示されたURLをコピーします。

## 手順4 時計に「HTTP」アプリを入れる

Zepp アプリから、T-Rex 2 のアプリストアで「HTTP」を検索し、インストールします。

## 手順5 解錠・施錠のボタンを作る

Zepp アプリで「HTTP」アプリの設定画面を開き、カスタムアクションを追加します。

- **名前**: 解錠
- **URL**: 手順3でコピーしたURLの末尾に `?action=unlock` を付ける
- **メソッド**: GET

施錠ボタンも同様に作成し、URLの末尾を `?action=lock` にします。

## セキュリティ上の注意

**WebアプリのURLは、玄関の鍵と同じです。** 他人に知られると、誰でも解錠できる可能性があります。
URLは絶対にSNSやブログに公開せず、厳重に管理してください。もし漏洩した可能性がある場合は、GASのデプロイを削除し、SESAMEのAPIキーを再発行してください。

## まとめ

時計のアプリから HTTP リクエストを送り、GAS で受け取ることで、サーバーなしで SESAME 5 を腕時計から操作できました。

<div style="text-align: center; margin: 40px 0;">
  <a href="https://www.amazon.co.jp/s?k=SESAME+5&tag=workbenchnote-22" target="_blank" rel="noopener" style="display: block; max-width: 400px; margin: 0 auto; text-decoration: none; border: 1px solid #ddd; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); background-color: #fff !important;">
    <div style="background-color: #f3f3f3 !important; padding: 15px; border-bottom: 1px solid #ddd;">
      <span style="font-size: 14px; color: #555 !important;">＼ 関連商品 ／</span>
    </div>
    <div style="padding: 20px;">
      <p style="color: #333 !important; font-weight: bold; margin: 0 0 15px 0; font-size: 16px;">SESAME 5 スマートロック</p>
      <div style="background-color: #ff9900 !important; color: #fff !important; padding: 12px 20px; border-radius: 8px; font-weight: bold; font-size: 16px; display: inline-block;">
        Amazonで詳細を見る ▶
      </div>
    </div>
  </a>
</div>
