#!/usr/bin/env python3
"""
AI Commit Assistant CLI
智能Git提交助手命令行工具
"""

import os
import sys
import argparse
import subprocess
from typing import Optional
from pathlib import Path

from .config import Config
from .generator import CommitGenerator
from .git_utils import GitUtils
from .providers import get_provider


def main():
    parser = argparse.ArgumentParser(
        description="AI Commit Assistant - 智能Git提交助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  ai-commit                    # 分析当前变更并生成提交信息
  ai-commit --model gpt-4      # 使用 GPT-4 模型
  ai-commit --style emoji      # 使用 emoji 风格
  ai-commit --raw              # 仅输出原始提交信息
  ai-commit config list        # 查看配置
  ai-commit hook install       # 安装 Git Hook
        """
    )
    
    parser.add_argument(
        "--model", "-m",
        help="指定AI模型 (如: gpt-4, claude-3-opus)"
    )
    parser.add_argument(
        "--style", "-s",
        choices=["conventional", "emoji", "simple"],
        default="conventional",
        help="提交信息风格 (默认: conventional)"
    )
    parser.add_argument(
        "--language", "-l",
        default="zh",
        help="提交信息语言 (默认: zh)"
    )
    parser.add_argument(
        "--raw", "-r",
        action="store_true",
        help="仅输出原始提交信息，不添加额外格式"
    )
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="预览生成的提交信息，不实际提交"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="显示详细信息"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # config 子命令
    config_parser = subparsers.add_parser("config", help="配置管理")
    config_parser.add_argument("action", choices=["list", "set", "get"])
    config_parser.add_argument("key", nargs="?")
    config_parser.add_argument("value", nargs="?")
    
    # hook 子命令
    hook_parser = subparsers.add_parser("hook", help="Git Hook 管理")
    hook_parser.add_argument("action", choices=["install", "uninstall", "status"])
    
    args = parser.parse_args()
    
    # 初始化配置
    config = Config()
    
    if args.command == "config":
        handle_config(args, config)
        return
    
    if args.command == "hook":
        handle_hook(args)
        return
    
    # 主功能：生成提交信息
    try:
        git_utils = GitUtils()
        
        # 检查是否在git仓库中
        if not git_utils.is_git_repo():
            print("❌ 错误：当前目录不是 Git 仓库", file=sys.stderr)
            sys.exit(1)
        
        # 获取变更内容
        diff = git_utils.get_staged_diff()
        if not diff:
            print("⚠️  警告：没有暂存的变更 (git add)", file=sys.stderr)
            sys.exit(1)
        
        if args.verbose:
            print(f"📊 检测到 {len(diff)} 个文件的变更")
        
        # 初始化AI提供商
        model = args.model or config.get("model", "gpt-3.5-turbo")
        provider = get_provider(model, config)
        
        # 生成提交信息
        generator = CommitGenerator(provider, config)
        commit_msg = generator.generate(
            diff=diff,
            style=args.style,
            language=args.language
        )
        
        if args.raw:
            print(commit_msg)
        else:
            print("\n📝 生成的提交信息：")
            print("=" * 50)
            print(commit_msg)
            print("=" * 50)
            
            if not args.dry_run:
                response = input("\n确认提交? [Y/n]: ").strip().lower()
                if response in ("", "y", "yes"):
                    # 执行提交
                    result = subprocess.run(
                        ["git", "commit", "-m", commit_msg],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0:
                        print("✅ 提交成功！")
                    else:
                        print(f"❌ 提交失败: {result.stderr}", file=sys.stderr)
                        sys.exit(1)
                else:
                    print("❌ 已取消")
    
    except KeyboardInterrupt:
        print("\n\n❌ 已取消", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


def handle_config(args, config):
    """处理配置命令"""
    if args.action == "list":
        print("📋 当前配置：")
        for key, value in config.list_all().items():
            if "key" in key.lower():
                value = "***" if value else "未设置"
            print(f"  {key}: {value}")
    
    elif args.action == "get":
        if not args.key:
            print("❌ 请指定配置项名称", file=sys.stderr)
            sys.exit(1)
        value = config.get(args.key)
        print(value if value else "未设置")
    
    elif args.action == "set":
        if not args.key or args.value is None:
            print("❌ 请指定配置项名称和值", file=sys.stderr)
            sys.exit(1)
        config.set(args.key, args.value)
        print(f"✅ 已设置 {args.key}")


def handle_hook(args):
    """处理 Git Hook 命令"""
    hook_path = Path(".git/hooks/prepare-commit-msg")
    
    if args.action == "install":
        if not Path(".git").exists():
            print("❌ 错误：当前目录不是 Git 仓库", file=sys.stderr)
            sys.exit(1)
        
        hook_content = '''#!/bin/bash
# AI Commit Assistant Hook
COMMIT_MSG_FILE=$1

if [ ! -s "$COMMIT_MSG_FILE" ] || [ "$(cat $COMMIT_MSG_FILE)" = "" ]; then
    ai-commit --raw > "$COMMIT_MSG_FILE" 2>/dev/null || true
fi
'''
        hook_path.write_text(hook_content)
        hook_path.chmod(0o755)
        print("✅ Git Hook 已安装")
        print("   提交时将自动使用 AI 生成提交信息")
    
    elif args.action == "uninstall":
        if hook_path.exists():
            hook_path.unlink()
            print("✅ Git Hook 已卸载")
        else:
            print("ℹ️  Git Hook 未安装")
    
    elif args.action == "status":
        if hook_path.exists():
            print("✅ Git Hook 已安装")
        else:
            print("❌ Git Hook 未安装")


if __name__ == "__main__":
    main()
