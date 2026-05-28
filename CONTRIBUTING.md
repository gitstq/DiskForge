# 🤝 Contributing to DiskForge

Thank you for your interest in contributing to DiskForge! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- **Bug Reports**: Submit issues for any bugs you find
- **Feature Requests**: Suggest new features or improvements
- **Code Contributions**: Submit pull requests with bug fixes or new features
- **Documentation**: Help improve or translate documentation
- **Testing**: Test on different platforms and report issues

## 🐛 Reporting Issues

When reporting issues, please include:

1. **Operating System**: Windows/macOS/Linux and version
2. **Python Version**: Output of `python --version`
3. **Steps to Reproduce**: Detailed steps to reproduce the issue
4. **Expected Behavior**: What you expected to happen
5. **Actual Behavior**: What actually happened
6. **Screenshots**: If applicable, especially for TUI issues

## 🔧 Development Setup

```bash
# Clone the repository
git clone https://github.com/gitstq/DiskForge.git
cd DiskForge

# No dependencies needed - just Python 3.8+
python diskforge.py --help
```

## 📝 Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and concise
- Write comments for complex logic

## 🔄 Pull Request Process

1. **Fork** the repository
2. **Create a branch** for your feature/fix
3. **Make your changes** with clear commit messages
4. **Test** your changes thoroughly
5. **Submit PR** with description of changes

### Commit Message Format

Use conventional commits:

- `feat: add new feature`
- `fix: resolve bug`
- `docs: update documentation`
- `refactor: improve code structure`
- `test: add tests`

## 🧪 Testing

Before submitting PR, test your changes:

```bash
# Basic functionality test
python diskforge.py /tmp --no-tui

# TUI test
python diskforge.py /tmp

# Export tests
python diskforge.py /tmp --json test.json --html test.html --md test.md

# Duplicate detection
python diskforge.py /tmp --find-dups --no-tui
```

## 📋 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Celebrate contributions

## ❓ Questions?

Feel free to open an issue for any questions or discussions!

---

Thank you for contributing to DiskForge! 💾✨
