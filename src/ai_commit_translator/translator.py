"""AI Commit Translator — 核心翻译引擎"""
import os
import re
import logging
from typing import Optional, Literal
from dataclasses import dataclass

from .commit import CommitMessage, CommitType, detect_type

logger = logging.getLogger(__name__)


@dataclass
class TranslateConfig:
    """翻译配置"""
    provider: Literal["openai", "anthropic", "ollama"] = "openai"
    model: str = "gpt-4o-mini"
    temperature: float = 0.3
    max_tokens: int = 300
    base_url: Optional[str] = None
    api_key: Optional[str] = None


class CommitTranslator:
    """AI Commit Message 翻译器"""

    SYSTEM_PROMPT = """You are an expert at writing Git commit messages following the Conventional Commits specification.

Given a Chinese (or other language) description of a code change, generate a proper English commit message.

Rules:
1. Format: <type>(<scope>): <description>
2. <type> must be one of: feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert, hotfix
3. <scope> is optional but recommended (module/component name, lowercase)
4. <description> must be:
   - In English, lowercase
   - Max 72 characters
   - Start with imperative verb (add, fix, update, remove, improve, etc.)
   - No period at the end
5. If the change is breaking, add "!" before ":" and explain in body
6. Always infer the most appropriate type from the description

Output ONLY the commit message, nothing else. No markdown, no code blocks.
"""

    USER_PROMPT_TEMPLATE = """Generate a commit message for this change:

{input_text}

Requirements:
- Type: {commit_type}
- Output the commit message in Conventional Commits format
- Keep description under 72 characters
- Use imperative mood (add, fix, update, improve, remove, etc.)
"""

    def __init__(
        self,
        provider: Literal["openai", "anthropic", "ollama"] = "openai",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        self.config = TranslateConfig(
            provider=provider,
            model=model or self._default_model(provider),
            api_key=api_key or self._get_api_key(provider),
            base_url=base_url or self._get_base_url(provider),
        )
        self._client = None

    def _default_model(self, provider: str) -> str:
        models = {
            "openai": "gpt-4o-mini",
            "anthropic": "claude-sonnet-4-20250514",
            "ollama": "llama3",
        }
        return models.get(provider, "gpt-4o-mini")

    def _get_api_key(self, provider: str) -> Optional[str]:
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
        }
        var = env_vars.get(provider)
        return os.getenv(var) if var else None

    def _get_base_url(self, provider: str) -> Optional[str]:
        if provider == "ollama":
            return os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return os.getenv("OPENAI_BASE_URL")  # for proxies

    def _get_client(self):
        """懒加载 LLM 客户端"""
        if self._client:
            return self._client

        if self.config.provider == "openai":
            from openai import OpenAI
            kwargs = {"api_key": self.config.api_key}
            if self.config.base_url:
                kwargs["base_url"] = self.config.base_url
            self._client = OpenAI(**kwargs)

        elif self.config.provider == "anthropic":
            from anthropic import Anthropic
            self._client = Anthropic(api_key=self.config.api_key)

        elif self.config.provider == "ollama":
            try:
                import httpx
                self._client = httpx.Client(base_url=self.config.base_url or "http://localhost:11434", timeout=60.0)
            except ImportError:
                raise ImportError("请安装 httpx: pip install httpx")

        return self._client

    def _call_openai(self, messages: list) -> str:
        client = self._get_client()
        response = client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )
        return response.choices[0].message.content.strip()

    def _call_anthropic(self, messages: list) -> str:
        client = self._get_client()
        # 合并 messages
        system = next((m["content"] for m in messages if m["role"] == "system"), "")
        user = next((m["content"] for m in messages if m["role"] == "user"), "")

        response = client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            system=system,
            messages=[{"role": "user", "content": user}]
        )
        return response.content[0].text.strip()

    def _call_ollama(self, messages: list) -> str:
        client = self._get_client()
        # 合并 messages
        prompt = "\n".join(f"{m['role']}: {m['content']}" for m in messages)

        response = client.post("/api/chat", json={
            "model": self.config.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        })
        data = response.json()
        return data["message"]["content"].strip()

    def translate(
        self,
        text: str,
        commit_type: Optional[CommitType] = None,
        scope: Optional[str] = None,
        force_type: bool = False,
    ) -> str:
        """
        将中文需求翻译为英文 Commit Message

        Args:
            text: 中文（或任意语言）的需求描述
            commit_type: 强制指定类型（不自动推断）
            scope: 指定影响范围
            force_type: 是否强制使用指定类型

        Returns:
            规范的英文 commit message
        """
        if not text or not text.strip():
            raise ValueError("输入不能为空")

        # 自动推断类型
        if commit_type is None:
            commit_type = detect_type(text)

        # 构建 prompt
        type_str = commit_type.value if commit_type else "feat"
        user_prompt = self.USER_PROMPT_TEMPLATE.format(
            input_text=text.strip(),
            commit_type=type_str,
        )

        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]

        # 调用对应 provider
        try:
            if self.config.provider == "openai":
                result = self._call_openai(messages)
            elif self.config.provider == "anthropic":
                result = self._call_anthropic(messages)
            elif self.config.provider == "ollama":
                result = self._call_ollama(messages)
            else:
                raise ValueError(f"未知 provider: {self.config.provider}")

        except Exception as e:
            logger.error(f"LLM 调用失败: {e}")
            # 降级：使用规则引擎生成
            return self._fallback_translate(text, commit_type, scope)

        # 解析结果
        return self._parse_result(result, commit_type, scope)

    def _fallback_translate(self, text: str, commit_type: CommitType, scope: Optional[str]) -> str:
        """规则引擎降级方案"""
        # 简单翻译 + 格式化
        desc = text.lower().strip()
        desc = re.sub(r'[^\w\s-]', '', desc)
        desc = re.sub(r'\s+', ' ', desc)[:72]

        # 动词映射
        verb_map = {
            "feat": "add",
            "fix": "fix",
            "docs": "update",
            "style": "update",
            "refactor": "refactor",
            "perf": "improve",
            "test": "add",
            "chore": "update",
            "ci": "update",
            "build": "update",
            "revert": "revert",
            "hotfix": "fix",
        }

        verb = verb_map.get(commit_type.value, "update")
        if not desc.startswith(verb):
            desc = f"{verb} {desc}"

        scope_part = f"({scope})" if scope else ""
        return f"{commit_type.value}{scope_part}: {desc}"

    def _parse_result(self, result: str, commit_type: CommitType, scope: Optional[str]) -> str:
        """解析 LLM 返回结果"""
        # 清理 markdown 代码块
        result = re.sub(r'^```\w*\n?', '', result.strip())
        result = re.sub(r'\n?```$', '', result)

        # 如果有 scope，尝试合并
        if scope and "(" not in result:
            parts = result.split(":", 1)
            if len(parts) == 2:
                type_scope = parts[0].strip()
                desc = parts[1].strip()
                if "(" not in type_scope:
                    type_scope = f"{type_scope}({scope})"
                result = f"{type_scope}: {desc}"

        return result

    def batch_translate(self, texts: list[str]) -> list[str]:
        """批量翻译"""
        return [self.translate(t) for t in texts]

    def translate_with_options(self, text: str, **kwargs) -> str:
        """带额外选项的翻译"""
        return self.translate(text, **kwargs)
