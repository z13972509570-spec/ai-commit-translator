"""Commit Message 数据模型和类型定义"""
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class CommitType(str, Enum):
    """Conventional Commits 标准类型"""
    FEAT = "feat"           # 新功能
    FIX = "fix"             # 缺陷修复
    DOCS = "docs"           # 文档更新
    STYLE = "style"         # 代码格式
    REFACTOR = "refactor"   # 重构
    PERF = "perf"           # 性能优化
    TEST = "test"           # 测试
    CHORE = "chore"         # 构建/工具
    CI = "ci"               # CI/CD
    BUILD = "build"         # 构建系统
    REVERT = "revert"       # 回滚
    HOTFIX = "hotfix"       # 紧急修复


# 中文类型映射
TYPE_KEYWORDS = {
    "feat": ["新增", "添加", "增加", "新功能", "功能", "支持"],
    "fix": ["修复", "bug", "错误", "问题", "缺陷", "修复"],
    "docs": ["文档", "readme", "注释", "说明", "更新文档"],
    "style": ["样式", "格式", "风格", "美化", "排版"],
    "refactor": ["重构", "优化代码", "重写", "整理"],
    "perf": ["性能", "优化", "提速", "加快", "效率"],
    "test": ["测试", "用例", "test"],
    "chore": ["工具", "配置", "依赖", "更新", "chore"],
    "ci": ["ci", "cd", "pipeline", "github actions", "gitlab"],
    "build": ["构建", "编译", "build"],
    "hotfix": ["hotfix", "紧急修复", "临时修复"],
}


# 常用 scope 列表
COMMON_SCOPES = [
    "api", "ui", "auth", "db", "config", "docs", "test",
    "build", "deps", "ci", "core", "utils", "cli", "server",
    "client", "web", "mobile", "linux", "windows", "mac",
]


def detect_type(text: str) -> CommitType:
    """根据文本内容推断 commit 类型"""
    text_lower = text.lower()
    scores = {}

    for commit_type, keywords in TYPE_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[commit_type] = score

    if max(scores.values()) == 0:
        return CommitType.FEAT  # 默认

    return CommitType(max(scores, key=scores.get))


class CommitMessage(BaseModel):
    """Commit Message 结构化数据"""
    type: CommitType = Field(description="Commit 类型")
    scope: Optional[str] = Field(None, description="影响范围（模块名）")
    description: str = Field(description="简短描述（英文，小写）")
    body: Optional[str] = Field(None, description="详细说明（可选）")
    breaking: bool = Field(False, description="是否破坏性变更")
    footer: Optional[str] = Field(None, description="Footer 信息（如 BREAKING CHANGE）")

    def to_string(self) -> str:
        """转换为标准 commit string"""
        scope_part = f"({self.scope})" if self.scope else ""
        breaking_part = "!" if self.breaking else ""
        desc_part = self.description

        result = f"{self.type.value}{scope_part}{breaking_part}: {desc_part}"

        if self.body:
            result += f"\n\n{self.body}"

        if self.footer:
            result += f"\n\n{self.footer}"
        elif self.breaking:
            result += f"\n\nBREAKING CHANGE: introduces breaking changes"

        return result

    @property
    def conventional(self) -> str:
        """Alias for to_string()"""
        return self.to_string()
