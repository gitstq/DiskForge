<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Dependencies-Zero-orange.svg" alt="Dependencies">
  <img src="https://img.shields.io/badge/Platform-Cross--Platform-lightgrey.svg" alt="Platform">
</p>

<p align="center">
  <a href="README.md">简体中文</a> | 
  <a href="README_EN.md">English</a> | 
  <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">💾 DiskForge</h1>

<p align="center">
  <strong>輕量級終端機磁碟使用分析引擎</strong><br>
  <sub>零依賴 • TUI 儀表板 • 重複檔案偵測 • 多格式報告</sub>
</p>

---

## 🎉 專案介紹

**DiskForge** 是一款輕量級、零依賴的終端機磁碟使用分析工具，專為開發者、維運工程師和系統管理員設計。

### 🎯 解決的痛點

- 😫 磁碟空間不足，不知道哪些檔案佔用空間
- 😫 重複檔案堆積，浪費儲存資源
- 😫 需要快速了解目錄結構和檔案分佈
- 😫 現有工具依賴複雜、安裝麻煩

### ✨ 自研差異化亮點

| 特性 | DiskForge | 其他工具 |
|------|-----------|----------|
| **依賴** | ✅ 零依賴 | ❌ 需要安裝多個套件 |
| **TUI介面** | ✅ 內建互動式儀表板 | ❌ 大多只有命令列輸出 |
| **重複偵測** | ✅ 支援智慧雜湊偵測 | ❌ 需要額外工具 |
| **報告匯出** | ✅ JSON/HTML/Markdown | ❌ 格式單一 |
| **跨平台** | ✅ 純Python，全平台 | ❌ 部分僅支援Linux |

---

## ✨ 核心特性

### 📊 磁碟掃描引擎
- **快速掃描** - 高效遞迴掃描目錄結構
- **即時進度** - 掃描過程中顯示進度資訊
- **智慧過濾** - 支援最小檔案大小、最大深度過濾
- **排除目錄** - 自動排除 `.git`、`node_modules` 等目錄

### 🔍 大檔案偵測器
- **Top N 識別** - 快速定位佔用空間最大的檔案
- **檔案詳情** - 顯示檔案大小、修改時間等資訊
- **路徑展示** - 完整檔案路徑，便於定位

### 🔄 重複檔案偵測器
- **雙重校驗** - 基於檔案大小 + MD5雜湊偵測
- **浪費統計** - 計算重複檔案浪費的空間
- **分組展示** - 按重複組分類顯示

### 📁 檔案類型分析器
- **副檔名統計** - 按檔案副檔名統計空間佔用
- **數量統計** - 顯示每種類型的檔案數量
- **視覺化** - TUI介面中的進度條展示

### 💻 TUI 互動式儀表板
- **即時介面** - 基於 curses 的終端機使用者介面
- **多視圖切換** - 檔案列表 / 副檔名統計 / 重複檔案
- **鍵盤導航** - 支援上下鍵、翻頁等操作

### 📦 多格式報告匯出
- **JSON** - 結構化資料，便於程式處理
- **HTML** - 精美網頁報告，支援分享
- **Markdown** - 文件格式，便於整合

---

## 🚀 快速開始

### 環境要求

- **Python**: 3.8 或更高版本
- **作業系統**: Linux / macOS / Windows
- **依賴**: 無需安裝任何第三方套件！

### 安裝方式

#### 方式一：直接執行（推薦）

```bash
# 複製儲存庫
git clone https://github.com/gitstq/DiskForge.git
cd DiskForge

# 直接執行
python diskforge.py /path/to/scan
```

#### 方式二：pip 安裝

```bash
pip install diskforge

# 執行
diskforge /path/to/scan
```

### 基本使用

```bash
# 掃描目錄並顯示TUI儀表板
python diskforge.py /home/user/projects

# 匯出JSON報告
python diskforge.py /home/user/projects --json report.json

# 匯出HTML報告
python diskforge.py /home/user/projects --html report.html

# 匯出Markdown報告
python diskforge.py /home/user/projects --md report.md

# 尋找重複檔案
python diskforge.py /home/user/projects --find-dups

# 只掃描大於100MB的檔案
python diskforge.py /home/user/projects --min-size 100MB

# 限制掃描深度
python diskforge.py /home/user/projects --max-depth 3

# 停用TUI，僅顯示文字摘要
python diskforge.py /home/user/projects --no-tui
```

---

## 📖 詳細使用指南

### 命令列參數

| 參數 | 說明 | 範例 |
|------|------|------|
| `path` | 要掃描的路徑（必需） | `/home/user` |
| `--json FILE` | 匯出JSON報告 | `--json report.json` |
| `--html FILE` | 匯出HTML報告 | `--html report.html` |
| `--markdown FILE` | 匯出Markdown報告 | `--md report.md` |
| `--min-size SIZE` | 最小檔案大小 | `--min-size 100MB` |
| `--max-depth N` | 最大掃描深度 | `--max-depth 3` |
| `--find-dups` | 尋找重複檔案 | `--find-dups` |
| `--no-tui` | 停用TUI介面 | `--no-tui` |
| `--version` | 顯示版本號 | `--version` |

### TUI 快捷鍵

| 按鍵 | 功能 |
|------|------|
| `F` | 切換到檔案列表視圖 |
| `E` | 切換到副檔名統計視圖 |
| `D` | 切換到重複檔案視圖 |
| `↑` / `↓` | 上下移動選擇 |
| `PageUp` / `PageDown` | 翻頁 |
| `Q` | 離開 |

### 使用場景範例

#### 場景一：清理磁碟空間

```bash
# 掃描整個使用者目錄，找出大檔案
python diskforge.py ~ --no-tui

# 輸出範例：
# Top 10 Largest Files:
#   1.     2.50 GB  node_modules.tar.gz
#   2.     1.80 GB  backup_2024.zip
#   ...
```

#### 場景二：專案目錄分析

```bash
# 分析專案目錄的檔案類型分佈
python diskforge.py ~/myproject --html project_analysis.html

# 生成的HTML報告包含：
# - 總體統計資訊
# - Top 20 大檔案
# - 按副檔名的空間分佈圖表
```

#### 場景三：尋找重複檔案

```bash
# 尋找目錄中的重複檔案
python diskforge.py ~/Downloads --find-dups --no-tui

# 輸出範例：
# Found 15 duplicate groups
# Group 1 (Wasted: 500 MB):
#   - /Downloads/file1.pdf
#   - /Downloads/backup/file1.pdf
```

---

## 💡 設計思路與迭代規劃

### 設計理念

1. **零依賴優先** - 僅使用Python標準庫，確保最大相容性
2. **終端機友善** - TUI介面適合伺服器環境使用
3. **報告豐富** - 多格式匯出滿足不同需求
4. **效能優先** - 高效掃描演算法，支援大目錄

### 技術選型

- **語言**: Python 3.8+ - 廣泛相容，無需編譯
- **TUI**: curses - 標準庫，跨平台支援
- **雜湊**: MD5 - 平衡速度與準確性

### 後續迭代計劃

- [ ] 支援遠端目錄掃描（SSH）
- [ ] 新增檔案刪除功能
- [ ] 支援設定檔
- [ ] 新增更多雜湊演算法選項
- [ ] 支援匯出CSV格式
- [ ] 新增即時監控模式

---

## 📦 打包與部署指南

### 作為腳本使用

```bash
# 直接執行Python腳本
python diskforge.py /path/to/scan
```

### 打包為可執行檔

```bash
# 使用PyInstaller打包
pip install pyinstaller
pyinstaller --onefile diskforge.py

# 生成的可執行檔在 dist/ 目錄
./dist/diskforge /path/to/scan
```

### 系統安裝

```bash
# 安裝到系統
pip install .

# 之後可直接使用
diskforge /path/to/scan
```

---

## 🤝 貢獻指南

我們歡迎所有形式的貢獻！

### 貢獻方式

1. **報告問題** - 在 Issues 中提交 Bug 報告
2. **功能建議** - 提出新功能想法
3. **程式碼貢獻** - 提交 Pull Request
4. **文件改進** - 完善文件或翻譯

### 開發指南

```bash
# 複製儲存庫
git clone https://github.com/gitstq/DiskForge.git
cd DiskForge

# 執行測試
python diskforge.py /tmp --no-tui

# 提交程式碼前請確保：
# 1. 程式碼風格符合 PEP 8
# 2. 新增必要的註解
# 3. 測試通過
```

詳細貢獻指南請查看 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 開源授權說明

本專案採用 **MIT License** 開源授權。

這表示您可以：
- ✅ 商業使用
- ✅ 修改程式碼
- ✅ 分發程式碼
- ✅ 私人使用

唯一要求是保留版權聲明和授權聲明。

---

<p align="center">
  Made with ❤️ by DiskForge Team<br>
  <sub>如果這個專案對您有幫助，請給一個 ⭐ Star 支持一下！</sub>
</p>
