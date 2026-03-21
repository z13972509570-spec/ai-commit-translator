# 📝 AI Commit Translator

> 输入中文需求描述，自动生成规范的英文 Git commit message（基于 Conventional Commits 标准）

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Conventional Commits](https://img.shields.io/badge/Commit-Conventional%20Commits-Feature-FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)

## ✨ 特性

- 🎯 **中文 → 英文 Commit**：输入中文需求，自动生成规范的英文 commit message
- 📋 **Conventional Commits**：严格遵循 `<type>(<scope>): <description>` 格式
- 🔄 **支持多种类型**：`feat` / `fix` / `docs` / `style` / `refactor` / `test` / `chore`
- 🎨 **多语言支持**：中文、英文、日文、韩文需求均可处理
- ⚡ **本地 LLM 支持**：支持 Ollama 本地模型，无需 API Key
- 🔧 **Git Hooks 集成**：可作为 `commit-msg` hook 使用
- 📦 **CLI + Python API**：命令行工具和 Python 库两种使用方式

## 🚀 快速开始

### 安装

```bash
pip install ai-commit-translator
```

### CLI 使用

```bash
# 交互式模式
ai-commit translate

# 直接输入
ai-commit translate "修复了登录页面的样式问题"

# 管道输入
echo "新增用户注册功能" | ai-commit translate

# 指定类型
ai-commit translate "更新了 README 文档" --type docs
```

### Python API

```python
from ai_commit_translator import CommitTranslator

translator = CommitTranslator()
message = translator.translate("修复了登录页面的样式问题")
print(message)  # "fix(ui): resolve login page styling issue"
```

## 📋 支持的 Commit 类型

| 类型 | 英文 | 中文说明 |
|------|------|---------|
| feat | Feature | 新功能 |
| fix | Bug Fix | 缺陷修复 |
| docs | Documentation | 文档更新 |
| style | Styling | 代码格式（不影响功能） |
| refactor | Refactoring | 重构（不修复bug不加功能） |
| perf | Performance | 性能优化 |
| test | Tests | 测试相关 |
| chore | Chores | 构建/工具/依赖 |
| ci | CI/CD | CI/CD 配置 |
| build | Build | 构建系统变更 |
| revert | Revert | 回滚提交 |

## ⚙️ 配置

### API Key 配置

```bash
# OpenAI
export OPENAI_API_KEY=sk-...

# Anthropic Claude
export ANTHROPIC_API_KEY=sk-ant-...

# 本地 Ollama
export OLLAMA_BASE_URL=http://localhost:11434
ai-commit translate "需求" --provider ollama --model llama3
```

### Git Hooks 集成

```bash
# 安装 commit-msg hook
ai-commit install-hook

# 卸载
ai-commit uninstall-hook
```

## 🔧 工作原理

```
[中文需求]
    │
    ▼
┌─────────────────┐
│  AI LLM 模型     │  ← 语义理解 + 类型推断
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Conventional   │  ← 自动选择 type/scope
│    Commits      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  英文 Commit     │
│  Message        │
└─────────────────┘
```

## 📦 License

MIT © 2026
