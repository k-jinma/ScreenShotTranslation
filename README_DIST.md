# Screenshot Translator

スクリーンショットを撮影し、画像内のテキストを自動的に日本語に翻訳するWindowsアプリケーションです。

## 機能

- 📸 **スクリーンショット撮影**: ホットキー（Ctrl+Shift+S）で画面をキャプチャ
- 🔍 **OCR（文字認識）**: EasyOCRを使用して画像内のテキストを抽出
- 🌐 **AI翻訳**: Google Gemini APIを使用して高品質な日本語翻訳
- 💾 **自動保存**: 翻訳されたテキストを画像と共に保存
- 📋 **クリップボード連携**: 翻訳結果を自動的にクリップボードにコピー

## システム要件

- Windows 10/11
- インターネット接続（初回起動時とAPI翻訳時に必要）
- 空きディスク容量: 約2GB（モデルファイル含む）

## セットアップ

### 1. ファイルの配置

ダウンロードしたファイルを任意のフォルダに展開してください。

### 2. Google Gemini APIキーの取得

1. [Google AI Studio](https://makersuite.google.com/app/apikey)にアクセス
2. Googleアカウントでログイン
3. 「Create API Key」をクリックしてAPIキーを取得

### 3. APIキーの設定

1. `.env.template`ファイルを`.env`にリネーム
2. `.env`ファイルをテキストエディタで開く
3. `your_api_key_here`を取得したAPIキーに置き換える

```
GEMINI_API_KEY=your_actual_api_key_here
```

4. ファイルを保存

## 使い方

### 起動

`ScreenshotTranslator.exe`をダブルクリックして起動します。

**初回起動時の注意:**
- EasyOCRのモデルファイル（約100MB）が自動的にダウンロードされます
- インターネット接続が必要です
- ダウンロードには数分かかる場合があります

### スクリーンショットの撮影と翻訳

1. アプリケーションが起動すると、小さなウィンドウが表示されます
2. **Ctrl+Shift+S**を押すか、「Capture Screenshot」ボタンをクリック
3. マウスをドラッグして翻訳したい範囲を選択
4. 自動的にOCRと翻訳が実行されます
5. 翻訳結果がウィンドウに表示され、クリップボードにコピーされます

### 保存されるファイル

キャプチャした画像は`captured_images`フォルダに保存されます:
- `screenshot_YYYYMMDD_HHMMSS.png`: 元の画像
- `screenshot_YYYYMMDD_HHMMSS.txt`: 翻訳されたテキスト

## トラブルシューティング

### アプリケーションが起動しない

- ウイルス対策ソフトがブロックしている可能性があります
- ホワイトリストに追加してください

### 翻訳が動作しない

1. `.env`ファイルが実行ファイルと同じフォルダにあることを確認
2. APIキーが正しく設定されていることを確認
3. インターネット接続を確認

### OCRが動作しない

1. 初回起動時にモデルファイルのダウンロードが完了しているか確認
2. インターネット接続を確認
3. アプリケーションを再起動

### エラーメッセージが表示される

エラーメッセージの内容をメモして、開発者に報告してください。

## ライセンス

このソフトウェアは個人利用・商用利用ともに自由に使用できます。

### 使用しているライブラリ

- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - Apache License 2.0
- [Google Generative AI](https://ai.google.dev/) - Google利用規約に準拠
- [Pillow](https://python-pillow.org/) - HPND License
- [Deep Translator](https://github.com/nidhaloff/deep-translator) - Apache License 2.0

## お問い合わせ

バグ報告や機能要望は、GitHubのIssuesページまでお願いします。

---

**注意事項:**
- Google Gemini APIには使用制限があります。詳細は[公式ドキュメント](https://ai.google.dev/pricing)を参照してください
- OCRの精度は画像の品質に依存します
- 翻訳の品質はAIモデルに依存します
