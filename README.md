# url2qr

URL を QR コードに変換する小さな CLI ツールです。

`uv run url2qr.py {url}` で実行すると、次を行います。

- ターミナル上に QR コードをレンダリング
- PNG ファイルとして保存
- 保存先の絶対パスを出力

Claude Code などのログイン URL を、別端末で素早く開きたいときに使う想定です。

## 動作要件

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)

## 依存関係

- `pyqrcode`
- `pypng`

`pyqrcode` で PNG を出力するために `pypng` が必要です。

## セットアップ

```bash
uv add pyqrcode pypng
````

単発で試すだけなら:

```bash
uv run --with pyqrcode --with pypng python url2qr.py "https://example.com"
```

## 使い方

### 基本

```bash
uv run url2qr.py "https://example.com"
```

実行すると:

* ターミナルに QR コードを表示
* `qrcodes/` 以下に PNG を保存
* 保存した PNG の `file://` URL を出力

### 出力先を指定

```bash
uv run url2qr.py "https://example.com" -o ./tmp/login.png
```

### ターミナル表示を無効化

```bash
uv run url2qr.py "https://example.com" --no-terminal
```

### PNG の解像度を変更

```bash
uv run url2qr.py "https://example.com" --scale 8
```

## 出力例

```text
<ターミナルにQRコードが表示される>

PNG: file:///absolute/path/to/qrcodes/qr_a1b2c3d4e5f6.png
```

## 想定ユースケース

* Claude Code のログイン URL を別端末で開く
* ローカル開発中の一時 URL をスマホで開く
* ブラウザに貼るのが面倒な長い URL を端末から直接共有する

## ファイル命名

`-o` を指定しない場合、URL の SHA-256 ハッシュ先頭 12 文字を使ってファイル名を生成します。

例:

```text
qrcodes/qr_a1b2c3d4e5f6.png
```

同じ URL なら同じファイル名になります。

## 注意点

* ターミナル表示は端末やフォントによって読み取りやすさが変わります
* 実運用では PNG 側を読む方が安定します
* ログイン URL にはトークンが含まれることがあるため、生成した PNG の扱いには注意してください

## ブラウザ版 (`index.html`)

別端末で取得した認証コードを QR 経由で元端末に戻すための往復リレー。CLI とは独立した単一の `index.html` で、Gist / GitHub Pages / ローカルで動作します。

```text
[スマホ] コードを貼付 → AES-GCM で暗号化 → QR を表示
[PC]    Web カメラで QR を読み取り → 復号 → クリップボードへコピー
```

### 特徴

- 単一ファイル、依存は CDN の `qrcode` / `jsQR` のみ
- シード値を共有すると AES-GCM (PBKDF2-SHA256, 100k iters) で暗号化
- シード未指定ならプレーンテキストで QR 化 (互換モード)
- シードは URL の `#seed=...` で両端末に同期可能
- カメラ権限は HTTPS 必須 (GitHub Pages なら自動的に満たされる)

### 使い方

1. `index.html` を GitHub Pages などで公開する (例: `https://<user>.github.io/url2qr/`)
2. 両端末で同じ URL を開き、シード入力欄に共通の値を入れる (もしくは URL に `#seed=xxx` を付けて共有)
3. スマホ側: 「エンコード」タブでコードを貼り付け → "QRに変換"
4. PC 側: 「デコード」タブ → "カメラを起動" → スマホの QR を向ける → 復号結果をコピー

### ローカル動作確認

```bash
python3 -m http.server 8000
# http://localhost:8000/ を開く (カメラは localhost なら HTTP でも可)
```

## 今後の改善候補

* URL を標準入力から受け取る
* PNG パスのクリップボードコピー
* 実行後に画像を自動で開く
* SVG 出力対応
* 有効期限付きログイン URL 向けの警告表示
* ブラウザ版: 画像ファイルからのデコード対応
