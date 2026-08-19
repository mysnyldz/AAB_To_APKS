# Bundle Tool Suite

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](../LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

bundletoolを使用してAAB（Android App Bundle）ファイルをAPKs形式に変換し、Xiaomi GetAppsなどのプラットフォーム配信用にAPKに署名するクロスプラットフォームGUIアプリケーション。

**言語:** [English](../README.md) | [Türkçe](README_TR.md) | [Deutsch](README_DE.md) | [Español](README_ES.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [简体中文](README_ZH-CN.md) | [Русский](README_RU.md)

---

## 機能

### AABからAPKsへの変換
- Googleのbundletoolを使用してAABファイルをAPKs形式に変換
- キーストアベースの署名サポート
- テキストフィールドまたはTXTファイルからのパスワード入力
- リアルタイム出力ログ

### APK署名と名前変更
- カスタムキーストアでAPKファイルに署名
- `com.xiaomi.getapps.signature.verification.apk`に自動名前変更
- Xiaomi GetApps提出要件と互換

### 全般
- 多言語UI（8言語: EN, TR, DE, ES, FR, JA, ZH-CN, RU）
- タブインターフェース
- ファイルブラウザダイアログ
- プログレスインジケーター
- クロスプラットフォーム（Windows、macOS、Linux）
- 自動Android SDK検出
- bundletool JAR同梱サポート

---

## 要件

### システム
- **Python 3.10+**（ソースから実行する場合）
- **Java Runtime Environment (JRE)**（bundletoolが必要）
- **PySide6**（Qt6 GUIフレームワーク）— ビルドスクリプトが自動インストール、または手動: `pip install PySide6`

### 外部ツール
- **bundletool** - Google公式のAAB変換ツール
  - ダウンロード: https://github.com/google/bundletool/releases
  - `bundletool-all-x.x.x.jar`を`tools/`フォルダに配置またはPATHに追加
- **Android SDK build-tools** - APK署名に必要
  - Android Studioに同梱
  - すべてのプラットフォームで自動検出

---

## インストール

### オプションA: クイックスタート（推奨）

`scripts/`フォルダ内の、お使いのプラットフォーム用ランチャーをダブルクリック:

- **Windows:** `scripts/start_windows.bat`
- **macOS:** `scripts/start_macos.command`
- **Linux:** `scripts/start_linux.sh`

ランチャーは自動的に:
1. 初回起動時に仮想環境（`.venv`）を作成
2. 依存関係をインストール（PySide6 約100 MB）
3. アプリケーションを起動

### オプションB: ソースから実行

```bash
git clone <repo-url>
cd AAB-To-APKs

python run.py
```

### オプションC: スタンドアロン実行ファイル

#### Windows:
```bash
scripts/build_windows.bat
# 出力: dist/BundleToolSuite.exe
```

#### macOS / Linux:
```bash
chmod +x scripts/build_simple.sh
./scripts/build_simple.sh
# 出力: dist/BundleToolSuite
```

> **注意:** 実行ファイルの作成には[PyInstaller](https://pyinstaller.org/)が必要です:
> ```bash
> pip install pyinstaller
> ```

### クリーン / 再インストール

`.venv`、`dist`、`build`を削除します（ソースコードは残します）:

```bash
# Windows
scripts/clean_windows.bat

# macOS / Linux
chmod +x scripts/clean.sh
./scripts/clean.sh
```

これらのフォルダは`.gitignore`に含まれているため、GitHubにはプッシュされません。

---

## 使い方

### AABからAPKs

1. `.aab`ファイルを選択
2. 出力`.apks`ファイルパスを設定
3. キーストアファイル、パスワード、キーエイリアス、キーパスワードを入力
4. **APKsに変換**をクリック

### APK署名

1. ソース`.apk`ファイルを選択
2. 出力ディレクトリを設定
3. キーストアファイル、パスワード、キーエイリアス、キーパスワードを入力
4. **APKに署名して名前変更**をクリック
5. 出力: `com.xiaomi.getapps.signature.verification.apk`

### TXTファイルからパスワード

両方のタブでTXTファイルからのパスワード読み取りをサポートしています。**「TXTから読み取り」**オプションをチェックして、パスワードファイルを選択してください。

---

## プロジェクト構造

```
AAB-To-APKs/
├── main_window.py           # メインPySide6 GUI
├── theme.py                 # デザイントークンとQSS
├── errors.py                # エラー分類とユーザー向けメッセージ
├── run.py                   # アプリケーションランチャー
├── requirements.txt         # Python依存関係 (PySide6)
├── README.md                # 英語
├── .gitignore
├── i18n/                    # 翻訳
│   ├── tr.json              # トルコ語
│   └── en.json              # 英語
├── assets/                  # アイコンとフォント
│   ├── icon.png             # アプリケーションアイコン
│   └── icons/               # SVGアイコン
├── docs/                    # ドキュメント
│   ├── BUILD.md             # ビルド手順
│   ├── README_TR.md         # トルコ語
│   ├── README_DE.md         # ドイツ語
│   ├── README_ES.md         # スペイン語
│   ├── README_FR.md         # フランス語
│   ├── README_JA.md         # このファイル（日本語）
│   ├── README_ZH-CN.md      # 中国語（簡体字）
│   └── README_RU.md         # ロシア語
├── scripts/                 # ビルド＆ランチャースクリプト
│   ├── build_simple.sh      # ビルド（macOS/Linux）
│   ├── build_macos.sh       # macOS .appビルド
│   ├── build_windows.bat    # Windows .exeビルド
│   ├── start_windows.bat    # Windowsランチャー
│   ├── start_macos.command  # macOSランチャー
│   ├── start_linux.sh       # Linuxランチャー
│   ├── clean_windows.bat    # .venv / dist / buildを削除（Windows）
│   └── clean.sh             # .venv / dist / buildを削除（macOS/Linux）
├── tools/                   # 外部ツール
│   └── bundletool-all-*.jar # bundletool JARをここに配置
└── examples/                # CLIコマンド例
    ├── BundleTool.txt
    └── APKsigner.txt
```

---

## トラブルシューティング

### bundletoolが見つからない
- bundletoolがPATHまたは`tools/`フォルダにあることを確認
- Javaがインストールされていることを確認: `java -version`
- 手動テスト: `bundletool`または`java -jar tools/bundletool-all-x.x.x.jar`

### apksignerが見つからない
- Android StudioまたはAndroid SDKをインストール
- build-toolsがインストールされていることを確認
- アプリはWindows、macOS、LinuxでSDKパスを自動検出します

### キーストアエラー
- キーストアファイル形式を確認（`.keystore`または`.jks`）
- パスワードとエイリアスを再確認
- キーストアファイルが破損していないことを確認

### AABファイルエラー
- AABファイルが有効で破損していないことを確認
- ファイルパスに特殊文字やスペースを使用しない

---

## プラットフォームサポート

| プラットフォーム | サポート   |
|------------------|------------|
| Windows          | フル       |
| macOS            | フル       |
| Linux            | フル       |

---

## ライセンス

このプロジェクトは [MITライセンス](../LICENSE) の下でライセンスされています。

## 貢献

バグ報告や提案は歓迎します。GitHubでissueを開いてください。
