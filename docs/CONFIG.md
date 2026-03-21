# 配置说明

## 环境变量

| 变量 | 说明 | 必需 |
|------|------|------|
| `OPENAI_API_KEY` | OpenAI API Key | OpenAI 提供商时 |
| `ANTHROPIC_API_KEY` | Anthropic API Key | Anthropic 提供商时 |
| `OLLAMA_BASE_URL` | Ollama 服务地址 | Ollama 提供商时 |
| `OPENAI_BASE_URL` | OpenAI 代理地址 | 使用代理时 |

## 构造函数参数

### provider

AI 服务提供商。

| 值 | 说明 | 默认模型 |
|-----|------|---------|
| `openai` | OpenAI GPT 系列 | gpt-4o-mini |
| `anthropic` | Anthropic Claude | claude-sonnet-4-20250514 |
| `ollama` | Ollama 本地模型 | llama3 |

### model

指定模型名称。

```python
translator = CommitTranslator(
    provider="openai",
    model="gpt-4"  # 使用 GPT-4
)
```

### base_url

API 代理地址。

```python
translator = CommitTranslator(
    provider="openai",
    base_url="https://api.openai.com/v1"  # 或代理地址
)
```

## LLM 参数

在 `translator.py` 中可调整：

```python
config = TranslateConfig(
    temperature=0.3,    # 创造性（越低越规范）
    max_tokens=300,     # 最大输出 tokens
)
```

### temperature 推荐值

| 场景 | 值 | 说明 |
|------|-----|------|
| 规范输出 | 0.1-0.3 | 越低越稳定 |
| 平衡 | 0.3-0.5 | 推荐 |
| 创意 | 0.5-0.7 | 可能不稳定 |
