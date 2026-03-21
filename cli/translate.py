#!/usr/bin/env python3
"""
CLI 入口 — ai-commit translate
"""
import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from src.ai_commit_translator import CommitTranslator
from src.ai_commit_translator.commit import CommitType

console = Console()


@click.command()
@click.argument("text", required=False)
@click.option(
    "--type", "-t",
    "commit_type",
    type=click.Choice([ct.value for ct in CommitType], case_sensitive=False),
    default=None,
    help="强制指定 commit 类型"
)
@click.option(
    "--scope", "-s",
    default=None,
    help="指定影响范围 (scope)"
)
@click.option(
    "--provider", "-p",
    type=click.Choice(["openai", "anthropic", "ollama"], case_sensitive=False),
    default="openai",
    help="选择 AI 服务商"
)
@click.option(
    "--model", "-m",
    default=None,
    help="指定模型"
)
@click.option(
    "--no-color",
    is_flag=True,
    help="禁用彩色输出"
)
@click.option(
    "--copy",
    "-c",
    is_flag=True,
    help="直接复制到剪贴板"
)
def translate(text, commit_type, scope, provider, model, no_color, copy):
    """📝 将中文需求翻译为规范的英文 Commit Message"""

    # 如果没有传参，尝试读取剪贴板或 stdin
    if not text:
        try:
            import pyperclip
            text = pyperclip.paste().strip()
            if not text:
                console.print("[yellow]⚠️  未提供输入，请传入文本或复制到剪贴板[/]")
                console.print("[dim]用法: ai-commit translate \"新增用户登录功能\"[/]")
                sys.exit(1)
            else:
                console.print(f"[dim]从剪贴板读取: {text[:50]}...[/]")
        except ImportError:
            console.print("[yellow]⚠️  请传入文本参数或安装 pyperclip[/]")
            console.print("[dim]用法: ai-commit translate \"新增用户登录功能\"[/]")
            sys.exit(1)

    # 解析类型
    ctype = CommitType(commit_type) if commit_type else None

    # 创建翻译器
    translator = CommitTranslator(
        provider=provider,
        model=model,
    )

    # 执行翻译
    try:
        result = translator.translate(text, commit_type=ctype, scope=scope)
    except Exception as e:
        console.print(f"[red]❌ 翻译失败: {e}[/]")
        sys.exit(1)

    # 输出结果
    if no_color:
        console.print(result)
    else:
        syntax = Syntax(result, "bash", theme="monokai", word_wrap=True)
        panel = Panel(
            syntax,
            title="📝 Commit Message",
            border_style="green",
            padding=(1, 2)
        )
        console.print(panel)

    # 复制到剪贴板
    if copy:
        try:
            import pyperclip
            pyperclip.copy(result)
            console.print("[green]✅ 已复制到剪贴板[/]")
        except ImportError:
            pass


if __name__ == "__main__":
    translate()
