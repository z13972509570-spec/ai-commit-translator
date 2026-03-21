"""单元测试"""
import pytest
from src.ai_commit_translator.commit import (
    CommitMessage, CommitType, detect_type
)


class TestCommitType:
    def test_detect_feat(self):
        assert detect_type("新增用户登录功能") == CommitType.FEAT
        assert detect_type("添加支付模块") == CommitType.FEAT

    def test_detect_fix(self):
        assert detect_type("修复登录bug") == CommitType.FIX
        assert detect_type("修复了按钮点击无效的问题") == CommitType.FIX

    def test_detect_docs(self):
        assert detect_type("更新README文档") == CommitType.DOCS
        assert detect_type("添加接口说明") == CommitType.DOCS

    def test_detect_refactor(self):
        assert detect_type("重构用户模块代码") == CommitType.REFACTOR

    def test_default_feat(self):
        assert detect_type("随便写点什么") == CommitType.FEAT


class TestCommitMessage:
    def test_to_string_basic(self):
        msg = CommitMessage(
            type=CommitType.FEAT,
            scope="auth",
            description="add user login feature"
        )
        assert msg.to_string() == "feat(auth): add user login feature"

    def test_to_string_no_scope(self):
        msg = CommitMessage(
            type=CommitType.FIX,
            description="fix null pointer exception"
        )
        assert msg.to_string() == "fix: fix null pointer exception"

    def test_to_string_breaking(self):
        msg = CommitMessage(
            type=CommitType.FEAT,
            description="change api response format",
            breaking=True
        )
        result = msg.to_string()
        assert "!" in result
        assert "BREAKING CHANGE" in result

    def test_body_optional(self):
        msg = CommitMessage(
            type=CommitType.FEAT,
            description="add dark mode support",
            body="支持跟随系统主题自动切换"
        )
        result = msg.to_string()
        assert "支持跟随系统主题" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
