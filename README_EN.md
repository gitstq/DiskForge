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
  <strong>Lightweight Terminal Disk Usage Analyzer Engine</strong><br>
  <sub>Zero Dependencies • TUI Dashboard • Duplicate Detection • Multi-Format Reports</sub>
</p>

---

## 🎉 Introduction

**DiskForge** is a lightweight, zero-dependency terminal disk usage analyzer designed for developers, DevOps engineers, and system administrators.

### 🎯 Problems We Solve

- 😫 Running out of disk space, don't know which files are taking up space
- 😫 Duplicate files piling up, wasting storage resources
- 😫 Need to quickly understand directory structure and file distribution
- 😫 Existing tools have complex dependencies and difficult installation

### ✨ Key Differentiators

| Feature | DiskForge | Other Tools |
|---------|-----------|-------------|
| **Dependencies** | ✅ Zero dependencies | ❌ Requires multiple packages |
| **TUI Interface** | ✅ Built-in interactive dashboard | ❌ Mostly command-line only |
| **Duplicate Detection** | ✅ Smart hash-based detection | ❌ Requires extra tools |
| **Report Export** | ✅ JSON/HTML/Markdown | ❌ Limited formats |
| **Cross-Platform** | ✅ Pure Python, all platforms | ❌ Some Linux only |

---

## ✨ Core Features

### 📊 Disk Scanning Engine
- **Fast Scanning** - Efficient recursive directory scanning
- **Real-time Progress** - Display progress during scanning
- **Smart Filtering** - Support for minimum file size, maximum depth
- **Directory Exclusion** - Auto-exclude `.git`, `node_modules`, etc.

### 🔍 Large File Detector
- **Top N Identification** - Quickly locate largest files
- **File Details** - Display size, modification time, etc.
- **Path Display** - Full file paths for easy location

### 🔄 Duplicate File Detector
- **Dual Verification** - Size + MD5 hash based detection
- **Wasted Space Stats** - Calculate space wasted by duplicates
- **Group Display** - Show files grouped by duplicates

### 📁 File Type Analyzer
- **Extension Statistics** - Space usage by file extension
- **Count Statistics** - Number of files per type
- **Visualization** - Progress bars in TUI interface

### 💻 TUI Interactive Dashboard
- **Real-time Interface** - Terminal UI based on curses
- **Multi-view Switching** - File list / Extension stats / Duplicates
- **Keyboard Navigation** - Arrow keys, page up/down support

### 📦 Multi-Format Report Export
- **JSON** - Structured data for programmatic processing
- **HTML** - Beautiful web reports for sharing
- **Markdown** - Document format for integration

---

## 🚀 Quick Start

### Requirements

- **Python**: 3.8 or higher
- **OS**: Linux / macOS / Windows
- **Dependencies**: No third-party packages required!

### Installation

#### Option 1: Direct Run (Recommended)

```bash
# Clone repository
git clone https://github.com/gitstq/DiskForge.git
cd DiskForge

# Run directly
python diskforge.py /path/to/scan
```

#### Option 2: pip Install

```bash
pip install diskforge

# Run
diskforge /path/to/scan
```

### Basic Usage

```bash
# Scan directory and show TUI dashboard
python diskforge.py /home/user/projects

# Export JSON report
python diskforge.py /home/user/projects --json report.json

# Export HTML report
python diskforge.py /home/user/projects --html report.html

# Export Markdown report
python diskforge.py /home/user/projects --md report.md

# Find duplicate files
python diskforge.py /home/user/projects --find-dups

# Only scan files larger than 100MB
python diskforge.py /home/user/projects --min-size 100MB

# Limit scan depth
python diskforge.py /home/user/projects --max-depth 3

# Disable TUI, show text summary only
python diskforge.py /home/user/projects --no-tui
```

---

## 📖 Detailed Usage Guide

### Command Line Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `path` | Path to scan (required) | `/home/user` |
| `--json FILE` | Export JSON report | `--json report.json` |
| `--html FILE` | Export HTML report | `--html report.html` |
| `--markdown FILE` | Export Markdown report | `--md report.md` |
| `--min-size SIZE` | Minimum file size | `--min-size 100MB` |
| `--max-depth N` | Maximum scan depth | `--max-depth 3` |
| `--find-dups` | Find duplicate files | `--find-dups` |
| `--no-tui` | Disable TUI interface | `--no-tui` |
| `--version` | Show version | `--version` |

### TUI Keyboard Shortcuts

| Key | Function |
|-----|----------|
| `F` | Switch to file list view |
| `E` | Switch to extension stats view |
| `D` | Switch to duplicates view |
| `↑` / `↓` | Move selection up/down |
| `PageUp` / `PageDown` | Page navigation |
| `Q` | Quit |

### Usage Scenarios

#### Scenario 1: Free Up Disk Space

```bash
# Scan entire user directory, find large files
python diskforge.py ~ --no-tui

# Sample output:
# Top 10 Largest Files:
#   1.     2.50 GB  node_modules.tar.gz
#   2.     1.80 GB  backup_2024.zip
#   ...
```

#### Scenario 2: Project Directory Analysis

```bash
# Analyze file type distribution in project
python diskforge.py ~/myproject --html project_analysis.html

# Generated HTML report includes:
# - Overall statistics
# - Top 20 largest files
# - Space distribution charts by extension
```

#### Scenario 3: Find Duplicate Files

```bash
# Find duplicate files in directory
python diskforge.py ~/Downloads --find-dups --no-tui

# Sample output:
# Found 15 duplicate groups
# Group 1 (Wasted: 500 MB):
#   - /Downloads/file1.pdf
#   - /Downloads/backup/file1.pdf
```

---

## 💡 Design Philosophy & Roadmap

### Design Principles

1. **Zero Dependencies First** - Use only Python standard library for maximum compatibility
2. **Terminal Friendly** - TUI interface suitable for server environments
3. **Rich Reports** - Multiple export formats for different needs
4. **Performance First** - Efficient scanning algorithm for large directories

### Technology Choices

- **Language**: Python 3.8+ - Wide compatibility, no compilation needed
- **TUI**: curses - Standard library, cross-platform support
- **Hash**: MD5 - Balance between speed and accuracy

### Future Roadmap

- [ ] Support remote directory scanning (SSH)
- [ ] Add file deletion functionality
- [ ] Support configuration files
- [ ] Add more hash algorithm options
- [ ] Support CSV export format
- [ ] Add real-time monitoring mode

---

## 📦 Packaging & Deployment

### Use as Script

```bash
# Run Python script directly
python diskforge.py /path/to/scan
```

### Package as Executable

```bash
# Package with PyInstaller
pip install pyinstaller
pyinstaller --onefile diskforge.py

# Generated executable in dist/ directory
./dist/diskforge /path/to/scan
```

### System Installation

```bash
# Install to system
pip install .

# Then use directly
diskforge /path/to/scan
```

---

## 🤝 Contributing

We welcome all forms of contribution!

### Ways to Contribute

1. **Report Issues** - Submit bug reports in Issues
2. **Feature Requests** - Propose new features
3. **Code Contributions** - Submit Pull Requests
4. **Documentation** - Improve docs or translations

### Development Guide

```bash
# Clone repository
git clone https://github.com/gitstq/DiskForge.git
cd DiskForge

# Run tests
python diskforge.py /tmp --no-tui

# Before submitting code, ensure:
# 1. Code style follows PEP 8
# 2. Add necessary comments
# 3. Tests pass
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## 📄 License

This project is licensed under the **MIT License**.

This means you can:
- ✅ Commercial use
- ✅ Modify code
- ✅ Distribute code
- ✅ Private use

The only requirement is to retain the copyright notice and license notice.

---

<p align="center">
  Made with ❤️ by DiskForge Team<br>
  <sub>If this project helps you, please give it a ⭐ Star!</sub>
</p>
