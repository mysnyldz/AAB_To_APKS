# Bundle Tool Suite

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

使用bundletool将AAB（Android App Bundle）文件转换为APKs格式，并为Xiaomi GetApps等平台分发签署APK的跨平台GUI应用程序。

**语言:** [English](../README.md) | [Türkçe](README_TR.md) | [Deutsch](README_DE.md) | [Español](README_ES.md) | [Français](README_FR.md) | [日本語](README_JA.md) | [简体中文](README_ZH-CN.md) | [Русский](README_RU.md)

---

## 功能

### AAB转APKs
- 使用Google的bundletool将AAB文件转换为APKs格式
- 基于密钥库的签名支持
- 通过文本字段或TXT文件输入密码
- 实时输出日志

### APK签名和重命名
- 使用自定义密钥库签署APK文件
- 自动重命名为`com.xiaomi.getapps.signature.verification.apk`
- 兼容Xiaomi GetApps提交要求

### 通用
- 多语言界面（8种语言：EN, TR, DE, ES, FR, JA, ZH-CN, RU）
- 标签式界面
- 文件浏览器对话框
- 进度指示器
- 跨平台（Windows、macOS、Linux）
- 自动检测Android SDK
- 内置bundletool JAR支持

---

## 系统要求

### 系统
- **Python 3.10+**（从源代码运行）
- **Java Runtime Environment (JRE)**（bundletool需要）
- **PySide6**（Qt6 GUI框架）— 构建脚本自动安装，或手动安装：`pip install PySide6`

### 外部工具
- **bundletool** - Google官方AAB转换工具
  - 下载: https://github.com/google/bundletool/releases
  - 将`bundletool-all-x.x.x.jar`放在`tools/`文件夹中或添加到PATH
- **Android SDK build-tools** - APK签名所需
  - 随Android Studio提供
  - 在所有平台上自动检测

---

## 安装

### 选项A: 快速启动（推荐）

双击适合您平台的启动器（位于 `scripts/` 文件夹）：

- **Windows:** `scripts/start_windows.bat`
- **macOS:** `scripts/start_macos.command`
- **Linux:** `scripts/start_linux.sh`

启动器会自动：
1. 首次运行时创建虚拟环境（`.venv`）
2. 安装依赖（PySide6 约 100 MB）
3. 启动应用程序

### 选项B: 从源代码运行

```bash
git clone <repo-url>
cd AAB-To-APKs

python run.py
```

### 选项C: 独立可执行文件

#### Windows:
```bash
scripts/build_windows.bat
# 输出: dist/BundleToolSuite.exe
```

#### macOS / Linux:
```bash
chmod +x scripts/build_simple.sh
./scripts/build_simple.sh
# 输出: dist/BundleToolSuite
```

> **注意:** 构建可执行文件需要[PyInstaller](https://pyinstaller.org/):
> ```bash
> pip install pyinstaller
> ```

### 清理 / 全新安装

删除 `.venv`、`dist` 和 `build`（源代码保留）：

```bash
# Windows
scripts/clean_windows.bat

# macOS / Linux
chmod +x scripts/clean.sh
./scripts/clean.sh
```

这些文件夹已列入 `.gitignore`，不会推送到 GitHub。

---

## 使用方法

### AAB转APKs

1. 选择`.aab`文件
2. 设置输出`.apks`文件路径
3. 提供密钥库文件、密码、密钥别名和密钥密码
4. 点击**转换为APKs**

### APK签名

1. 选择源`.apk`文件
2. 设置输出目录
3. 提供密钥库文件、密码、密钥别名和密钥密码
4. 点击**签名并重命名APK**
5. 输出: `com.xiaomi.getapps.signature.verification.apk`

### 从TXT文件读取密码

两个标签页都支持从TXT文件读取密码。勾选**"从TXT读取"**选项并选择密码文件。

---

## 项目结构

```
AAB-To-APKs/
├── main_window.py           # 主 PySide6 GUI
├── theme.py                 # 设计令牌和 QSS
├── errors.py                # 错误分类与用户提示
├── run.py                   # 应用程序启动器
├── requirements.txt         # Python 依赖 (PySide6)
├── README.md                # 英文
├── .gitignore
├── i18n/                    # 翻译
│   ├── tr.json              # 土耳其语
│   └── en.json              # 英语
├── assets/                  # 图标和字体
│   ├── icon.png             # 应用图标
│   └── icons/               # SVG 图标
├── docs/                    # 文档
│   ├── BUILD.md             # 构建说明
│   ├── README_TR.md         # 土耳其语
│   ├── README_DE.md         # 德语
│   ├── README_ES.md         # 西班牙语
│   ├── README_FR.md         # 法语
│   ├── README_JA.md         # 日语
│   ├── README_ZH-CN.md      # 本文件（简体中文）
│   └── README_RU.md         # 俄语
├── scripts/                 # 构建与启动脚本
│   ├── build_simple.sh      # 构建（macOS/Linux）
│   ├── build_macos.sh       # macOS .app 构建
│   ├── build_windows.bat    # Windows .exe 构建
│   ├── start_windows.bat    # Windows 启动器
│   ├── start_macos.command  # macOS 启动器
│   ├── start_linux.sh       # Linux 启动器
│   ├── clean_windows.bat    # 删除 .venv / dist / build（Windows）
│   └── clean.sh             # 删除 .venv / dist / build（macOS/Linux）
├── tools/                   # 外部工具
│   └── bundletool-all-*.jar # 将 bundletool JAR 放在此处
└── examples/                # 示例 CLI 命令
    ├── BundleTool.txt
    └── APKsigner.txt
```

---

## 故障排除

### 未找到bundletool
- 确保bundletool在PATH中或放在`tools/`文件夹中
- 验证Java已安装: `java -version`
- 手动测试: `bundletool`或`java -jar tools/bundletool-all-x.x.x.jar`

### 未找到apksigner
- 安装Android Studio或Android SDK
- 确保已安装build-tools
- 应用程序在Windows、macOS和Linux上自动检测SDK路径

### 密钥库错误
- 验证密钥库文件格式（`.keystore`或`.jks`）
- 仔细检查密码和别名
- 确保密钥库文件未损坏

### AAB文件错误
- 确保AAB文件有效且未损坏
- 避免文件路径中使用特殊字符或空格

---

## 平台支持

| 平台    | 支持   |
|---------|--------|
| Windows | 完整   |
| macOS   | 完整   |
| Linux   | 完整   |

---

## 许可证

本项目为教育目的而开发。

## 贡献

欢迎错误报告和建议。请在GitHub上提交issue。
