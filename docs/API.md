# API 文档

## CommitTranslator

主翻译器类。

### 构造函数

```python
CommitTranslator(
    provider: Literal["openai", "anthropic", "ollama"] = "openai",
    model: Optional[str] = None,       # 自动选择默认模型
    api_key: Optional[str] = None,     # 从环境变量读取
    base_url: Optional[str] = None,    # API 代理地址
)
```

**默认模型**:
- OpenAI: `gpt-4o-mini`
- Anthropic: `claude-sonnet-4-20250514`
- Ollama: `llama3`

### 方法

#### `translate()`

翻译中文需求为英文 commit。

```python
def translate(
    self,
    text: str,                              # 中文需求
    commit_type: Optional[CommitType] = None, # 强制类型
    scope: Optional[str] = None,             # 影响范围
    force_type: bool = False,                 # 强制使用指定类型
) -> str
```

**示例**:

```python
translator = CommitTranslator(provider="openai")

# 自动推断类型
result = translator.translate("新增用户登录功能")
# -> "feat(auth): add user registration feature"

# 强制指定类型
result = translator.translate("更新文档说明", commit_type=CommitType.DOCS)
# -> "docs: update documentation"

# 指定 scope
result = translator.translate("修复支付bug", scope="payment")
# -> "fix(payment): resolve payment failure bug"
```

#### `batch_translate()`

批量翻译。

```python
def batch_translate(self, texts: list[str]) -> list[str]
```

**示例**:

```python
texts = [
    "新增用户注册功能",
    "修复登录bug",
    "更新README"
]
results = translator.batch_translate(texts)
```

#### `_fallback_translate()`

规则引擎降级方案。

当 LLM 调用失败时，自动使用规则引擎生成 commit message。

## CommitMessage

结构化 commit 数据模型。

### 字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `type` | CommitType | commit 类型 |
| `scope` | Optional[str] | 影响范围 |
| `description` | str | 简短描述（英文）|
| `body` | Optional[str] | 详细说明 |
| `breaking` | bool | 是否破坏性变更 |
| `footer` | Optional[str] | footer 信息 |

### 方法

#### `to_string()`

转换为标准 commit string。

```python
msg = CommitMessage(
    type=CommitType.FEAT,
    scope="auth",
    description="add user login feature"
)
print(msg.to_string())
# -> "feat(auth): add user login feature"
```

## CommitType

Commit 类型枚举。

```python
from src.ai_commit_translator.commit import CommitType

CommitType.FEAT       # 新功能
CommitType.FIX        # 缺陷修复
CommitType.DOCS       # 文档更新
CommitType.STYLE      # 代码格式
CommitType.REFACTOR   # 重构
CommitType.PERF       # 性能优化
CommitType.TEST       # 测试
CommitType.CHORE      # 杂项
CommitType.CI         # CI/CD
CommitType.BUILD      # 构建
CommitType.REVERT     # 回滚
CommitType.HOTFIX     # 紧急修复
```

## 便捷函数

```python
from ai_commit_translator import CommitTranslator

translator = CommitTranslator()
```
