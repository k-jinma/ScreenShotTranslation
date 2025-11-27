# Screenshot Translator - 実行ファイル化ガイド

このドキュメントでは、Screenshot Translatorアプリケーションを実行ファイル（.exe）として配布する方法を説明します。

## 目次
1. [事前準備](#事前準備)
2. [ビルド方法](#ビルド方法)
3. [配布方法](#配布方法)
4. [トラブルシューティング](#トラブルシューティング)

---

## 事前準備

### 1. PyInstallerのインストール

```bash
pip install pyinstaller
```

### 2. UPXのインストール（オプション - ファイルサイズ削減用）

UPXは実行ファイルを圧縮するツールです。

1. [UPX公式サイト](https://upx.github.io/)からダウンロード
2. ダウンロードしたファイルを解凍
3. `upx.exe`をシステムのPATHに追加、または`ScreenshotTranslator.spec`で`upx=False`に設定

### 3. アイコンファイルの準備（オプション）

アプリケーションにカスタムアイコンを設定したい場合：

1. `.ico`形式のアイコンファイルを用意
2. プロジェクトルートに配置
3. `ScreenshotTranslator.spec`の`icon=None`を`icon='your_icon.ico'`に変更

---

## ビルド方法

### オプション A: 単一実行ファイル（推奨）

**メリット:**
- 配布が簡単（1つの.exeファイルのみ）
- ユーザーが扱いやすい

**デメリット:**
- ファイルサイズが大きい（500MB〜1GB以上）
- 起動時に一時フォルダに展開するため、初回起動が遅い

**ビルドコマンド:**
```bash
pyinstaller ScreenshotTranslator.spec
```

生成されたファイル: `dist/ScreenshotTranslator.exe`

### オプション B: フォルダ形式

**メリット:**
- 起動が速い
- ファイルサイズが小さい
- デバッグが容易

**デメリット:**
- 複数のファイルを配布する必要がある

**ビルドコマンド:**

1. `ScreenshotTranslator.spec`を編集し、`EXE`セクションを以下のように変更:

```python
exe = EXE(
    pyz,
    a.scripts,
    [],  # a.binaries を削除
    exclude_binaries=True,  # 追加
    name='ScreenshotTranslator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ScreenshotTranslator',
)
```

2. ビルド:
```bash
pyinstaller ScreenshotTranslator.spec
```

生成されたフォルダ: `dist/ScreenshotTranslator/`

---

## 配布方法

### 必要なファイル

#### 単一実行ファイルの場合:
1. `dist/ScreenshotTranslator.exe`
2. `.env`ファイル（Google Gemini APIキーを含む）
3. `README.md`（使用方法の説明）

#### フォルダ形式の場合:
1. `dist/ScreenshotTranslator/`フォルダ全体
2. `.env`ファイル
3. `README.md`

### .envファイルの扱い

**重要:** APIキーを含む`.env`ファイルは、セキュリティ上の理由から実行ファイルに埋め込むべきではありません。

**推奨される配布方法:**

1. **テンプレートファイルを提供:**
   `.env.template`ファイルを作成:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

2. **ユーザーに設定を依頼:**
   README.mdに以下の手順を記載:
   - `.env.template`を`.env`にリネーム
   - `your_api_key_here`を実際のAPIキーに置き換え

3. **または、初回起動時にAPIキーを入力させる:**
   プログラムを修正して、APIキーが設定されていない場合に入力ダイアログを表示

### EasyOCRモデルファイルの扱い

EasyOCRは初回実行時にモデルファイルをダウンロードします（約100MB）。

**オプション1: ユーザーに初回ダウンロードさせる（推奨）**
- 初回起動時にインターネット接続が必要
- README.mdにその旨を記載

**オプション2: モデルファイルを同梱**
1. モデルファイルの場所を確認:
   ```
   C:\Users\<ユーザー名>\.EasyOCR\model\
   ```

2. `ScreenshotTranslator.spec`の`datas`セクションに追加:
   ```python
   datas=[
       ('.env', '.'),
       ('C:\\Users\\ユーザー名\\.EasyOCR\\model', '.EasyOCR/model'),
   ],
   ```

3. 配布パッケージのサイズが大幅に増加（+100MB程度）

---

## トラブルシューティング

### 問題1: 実行ファイルが起動しない

**原因:** 依存関係の欠落

**解決策:**
1. `ScreenshotTranslator.spec`の`hiddenimports`に不足しているモジュールを追加
2. コマンドプロンプトから実行してエラーメッセージを確認:
   ```bash
   dist\ScreenshotTranslator.exe
   ```

### 問題2: OCRが動作しない

**原因:** EasyOCRのモデルファイルが見つからない

**解決策:**
- インターネット接続を確認
- または、モデルファイルを同梱（上記参照）

### 問題3: 翻訳が動作しない

**原因:** `.env`ファイルが見つからない、またはAPIキーが無効

**解決策:**
- `.env`ファイルが実行ファイルと同じディレクトリにあることを確認
- APIキーが正しいことを確認

### 問題4: ファイルサイズが大きすぎる

**原因:** PyTorch、EasyOCRなどの大きな依存関係

**解決策:**
1. UPXで圧縮（既に有効化済み）
2. 不要な依存関係を除外:
   ```python
   excludes=['matplotlib', 'pandas', 'jupyter'],
   ```
3. フォルダ形式で配布

### 問題5: ウイルス対策ソフトに検出される

**原因:** PyInstallerで作成された実行ファイルは誤検出されることがある

**解決策:**
1. コード署名証明書を取得して署名
2. ウイルス対策ソフトのホワイトリストに追加
3. ソースコードも一緒に配布して信頼性を示す

---

## ビルドの最適化

### ファイルサイズを削減する方法

1. **不要なモジュールを除外:**
   ```python
   excludes=[
       'matplotlib',
       'pandas',
       'jupyter',
       'IPython',
       'notebook',
   ],
   ```

2. **PyTorchのCPU版のみを使用:**
   ```bash
   pip uninstall torch torchvision
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   ```

3. **UPXで圧縮:**
   - 既に`ScreenshotTranslator.spec`で有効化済み

### 起動速度を改善する方法

1. **フォルダ形式で配布**（上記参照）

2. **Lazy Importを使用:**
   `main.py`を修正して、必要な時だけモジュールをインポート

---

## 配布パッケージの作成

### ZIP形式で配布

```bash
# PowerShellで実行
Compress-Archive -Path dist\ScreenshotTranslator.exe, .env.template, README.md -DestinationPath ScreenshotTranslator_v1.0.zip
```

### インストーラーの作成（高度）

[Inno Setup](https://jrsoftware.org/isinfo.php)などのツールを使用してWindowsインストーラーを作成できます。

---

## チェックリスト

配布前に以下を確認してください:

- [ ] 実行ファイルが正常に起動する
- [ ] OCR機能が動作する
- [ ] 翻訳機能が動作する（APIキー設定後）
- [ ] スクリーンショット機能が動作する
- [ ] `.env.template`ファイルを用意
- [ ] README.mdに使用方法を記載
- [ ] ライセンス情報を記載（必要に応じて）
- [ ] 依存ライブラリのライセンスを確認

---

## 参考情報

- [PyInstaller公式ドキュメント](https://pyinstaller.org/en/stable/)
- [EasyOCR GitHub](https://github.com/JaidedAI/EasyOCR)
- [UPX公式サイト](https://upx.github.io/)
