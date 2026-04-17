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

## 今後の改善候補

* URL を標準入力から受け取る
* PNG パスのクリップボードコピー
* 実行後に画像を自動で開く
* SVG 出力対応
* 有効期限付きログイン URL 向けの警告表示
