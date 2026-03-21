# 使用指南

## 快速开始

### 安装

```bash
pip install -e .
```

### CLI 使用

```bash
# 交互式翻译
ai-commit translate "新增用户登录功能"

# 指定 scope
ai-commit translate "修复支付bug" --scope payment

# 指定类型
ai-commit translate "更新README" --type docs

# 管道输入
echo "新增用户注册功能" | ai-commit translate

# 直接复制到剪贴板
ai-commit translate "新增功能" --copy
```

### Python API 使用

```python
from ai_commit_translator import CommitTranslator, CommitType

# 初始化
translator = CommitTranslator(provider="openai")

# 翻译
result = translator.translate("修复了登录页面的样式问题")
print(result)  # "fix(ui): resolve login page styling issue"
```

## 环境配置

### OpenAI

```bash
export OPENAI_API_KEY=sk-...
```

### Anthropic

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

### Ollama (本地)

```bash
export OLLAMA_BASE_URL=http://localhost:11434
ai-commit translate "新增功能" --provider ollama --model llama3
```

## Git Hooks 集成

```bash
# 安装 hook
ai-commit install-hook

# 卸载 hook
ai-commit uninstall-hook
```

## 最佳实践

### 1. 使用 Scope 精确描述

```python
# 好的
translator.translate("用户登录失败", scope="auth")
# -> "fix(auth): resolve user login failure"

# 不好的
translator.translate("用户登录失败")
# -> "fix: fix user login failure"
```

### 2. 批量翻译

```python
commits = [
    "新增用户注册",
    "修复支付bug",
    "更新接口文档",
    "优化数据库查询"
]

for commit in translator.batch_translate(commits):
    print(commit)
```

### 3. CI/CD 集成

```yaml
# GitHub Actions
- name: Generate Commit Message
  run: |
    ai-commit translate "${{ github.event.commits[0].message }}" --copy
```

## 常见问题

### Q: 如何处理多行 commit？
A: 使用 body 参数：

```python
msg = CommitMessage(
    type=CommitType.FEAT,
    description="add dark mode support",
    body="支持跟随系统主题自动切换\n可通过设置手动切换"
)
print(msg.to_string())
```

### Q: 如何生成 breaking change？
A: 设置 breaking=True：

```python
msg = CommitMessage(
    type=CommitType.FEAT,
    description="change api response format",
    breaking=True
)
```
