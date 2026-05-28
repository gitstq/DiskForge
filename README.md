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
  <strong>轻量级终端磁盘使用分析引擎</strong><br>
  <sub>Zero Dependencies • TUI Dashboard • Duplicate Detection • Multi-Format Reports</sub>
</p>

---

## 🎉 项目介绍

**DiskForge** 是一款轻量级、零依赖的终端磁盘使用分析工具，专为开发者、运维工程师和系统管理员设计。

### 🎯 解决的痛点

- 😫 磁盘空间不足，不知道哪些文件占用空间
- 😫 重复文件堆积，浪费存储资源
- 😫 需要快速了解目录结构和文件分布
- 😫 现有工具依赖复杂、安装麻烦

### ✨ 自研差异化亮点

| 特性 | DiskForge | 其他工具 |
|------|-----------|----------|
| **依赖** | ✅ 零依赖 | ❌ 需要安装多个包 |
| **TUI界面** | ✅ 内置交互式仪表盘 | ❌ 大多只有命令行输出 |
| **重复检测** | ✅ 支持智能哈希检测 | ❌ 需要额外工具 |
| **报告导出** | ✅ JSON/HTML/Markdown | ❌ 格式单一 |
| **跨平台** | ✅ 纯Python，全平台 | ❌ 部分仅支持Linux |

---

## ✨ 核心特性

### 📊 磁盘扫描引擎
- **快速扫描** - 高效递归扫描目录结构
- **实时进度** - 扫描过程中显示进度信息
- **智能过滤** - 支持最小文件大小、最大深度过滤
- **排除目录** - 自动排除 `.git`、`node_modules` 等目录

### 🔍 大文件检测器
- **Top N 识别** - 快速定位占用空间最大的文件
- **文件详情** - 显示文件大小、修改时间等信息
- **路径展示** - 完整文件路径，便于定位

### 🔄 重复文件检测器
- **双重校验** - 基于文件大小 + MD5哈希检测
- **浪费统计** - 计算重复文件浪费的空间
- **分组展示** - 按重复组分类显示

### 📁 文件类型分析器
- **扩展名统计** - 按文件扩展名统计空间占用
- **数量统计** - 显示每种类型的文件数量
- **可视化** - TUI界面中的进度条展示

### 💻 TUI 交互式仪表盘
- **实时界面** - 基于 curses 的终端用户界面
- **多视图切换** - 文件列表 / 扩展名统计 / 重复文件
- **键盘导航** - 支持上下键、翻页等操作

### 📦 多格式报告导出
- **JSON** - 结构化数据，便于程序处理
- **HTML** - 精美网页报告，支持分享
- **Markdown** - 文档格式，便于集成

---

## 🚀 快速开始

### 环境要求

- **Python**: 3.8 或更高版本
- **操作系统**: Linux / macOS / Windows
- **依赖**: 无需安装任何第三方包！

### 安装方式

#### 方式一：直接运行（推荐）

```bash
# 克隆仓库
git clone https://github.com/gitstq/DiskForge.git
cd DiskForge

# 直接运行
python diskforge.py /path/to/scan
```

#### 方式二：pip 安装

```bash
pip install diskforge

# 运行
diskforge /path/to/scan
```

### 基本使用

```bash
# 扫描目录并显示TUI仪表盘
python diskforge.py /home/user/projects

# 导出JSON报告
python diskforge.py /home/user/projects --json report.json

# 导出HTML报告
python diskforge.py /home/user/projects --html report.html

# 导出Markdown报告
python diskforge.py /home/user/projects --md report.md

# 查找重复文件
python diskforge.py /home/user/projects --find-dups

# 只扫描大于100MB的文件
python diskforge.py /home/user/projects --min-size 100MB

# 限制扫描深度
python diskforge.py /home/user/projects --max-depth 3

# 禁用TUI，仅显示文本摘要
python diskforge.py /home/user/projects --no-tui
```

---

## 📖 详细使用指南

### 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `path` | 要扫描的路径（必需） | `/home/user` |
| `--json FILE` | 导出JSON报告 | `--json report.json` |
| `--html FILE` | 导出HTML报告 | `--html report.html` |
| `--markdown FILE` | 导出Markdown报告 | `--md report.md` |
| `--min-size SIZE` | 最小文件大小 | `--min-size 100MB` |
| `--max-depth N` | 最大扫描深度 | `--max-depth 3` |
| `--find-dups` | 查找重复文件 | `--find-dups` |
| `--no-tui` | 禁用TUI界面 | `--no-tui` |
| `--version` | 显示版本号 | `--version` |

### TUI 快捷键

| 按键 | 功能 |
|------|------|
| `F` | 切换到文件列表视图 |
| `E` | 切换到扩展名统计视图 |
| `D` | 切换到重复文件视图 |
| `↑` / `↓` | 上下移动选择 |
| `PageUp` / `PageDown` | 翻页 |
| `Q` | 退出 |

### 使用场景示例

#### 场景一：清理磁盘空间

```bash
# 扫描整个用户目录，找出大文件
python diskforge.py ~ --no-tui

# 输出示例：
# Top 10 Largest Files:
#   1.     2.50 GB  node_modules.tar.gz
#   2.     1.80 GB  backup_2024.zip
#   ...
```

#### 场景二：项目目录分析

```bash
# 分析项目目录的文件类型分布
python diskforge.py ~/myproject --html project_analysis.html

# 生成的HTML报告包含：
# - 总体统计信息
# - Top 20 大文件
# - 按扩展名的空间分布图表
```

#### 场景三：查找重复文件

```bash
# 查找目录中的重复文件
python diskforge.py ~/Downloads --find-dups --no-tui

# 输出示例：
# Found 15 duplicate groups
# Group 1 (Wasted: 500 MB):
#   - /Downloads/file1.pdf
#   - /Downloads/backup/file1.pdf
```

---

## 💡 设计思路与迭代规划

### 设计理念

1. **零依赖优先** - 仅使用Python标准库，确保最大兼容性
2. **终端友好** - TUI界面适合服务器环境使用
3. **报告丰富** - 多格式导出满足不同需求
4. **性能优先** - 高效扫描算法，支持大目录

### 技术选型

- **语言**: Python 3.8+ - 广泛兼容，无需编译
- **TUI**: curses - 标准库，跨平台支持
- **哈希**: MD5 - 平衡速度与准确性

### 后续迭代计划

- [ ] 支持远程目录扫描（SSH）
- [ ] 添加文件删除功能
- [ ] 支持配置文件
- [ ] 添加更多哈希算法选项
- [ ] 支持导出CSV格式
- [ ] 添加实时监控模式

---

## 📦 打包与部署指南

### 作为脚本使用

```bash
# 直接运行Python脚本
python diskforge.py /path/to/scan
```

### 打包为可执行文件

```bash
# 使用PyInstaller打包
pip install pyinstaller
pyinstaller --onefile diskforge.py

# 生成的可执行文件在 dist/ 目录
./dist/diskforge /path/to/scan
```

### 系统安装

```bash
# 安装到系统
pip install .

# 之后可直接使用
diskforge /path/to/scan
```

---

## 🤝 贡献指南

我们欢迎所有形式的贡献！

### 贡献方式

1. **报告问题** - 在 Issues 中提交 Bug 报告
2. **功能建议** - 提出新功能想法
3. **代码贡献** - 提交 Pull Request
4. **文档改进** - 完善文档或翻译

### 开发指南

```bash
# 克隆仓库
git clone https://github.com/gitstq/DiskForge.git
cd DiskForge

# 运行测试
python diskforge.py /tmp --no-tui

# 提交代码前请确保：
# 1. 代码风格符合 PEP 8
# 2. 添加必要的注释
# 3. 测试通过
```

详细贡献指南请查看 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 开源协议说明

本项目采用 **MIT License** 开源协议。

这意味着您可以：
- ✅ 商业使用
- ✅ 修改代码
- ✅ 分发代码
- ✅ 私人使用

唯一要求是保留版权声明和许可声明。

---

<p align="center">
  Made with ❤️ by DiskForge Team<br>
  <sub>如果这个项目对您有帮助，请给一个 ⭐ Star 支持一下！</sub>
</p>
