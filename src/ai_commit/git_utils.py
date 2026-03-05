"""
Git 工具模块
"""

import subprocess
from pathlib import Path
from typing import List, Optional, Tuple


class GitUtils:
    """Git 工具类"""
    
    def is_git_repo(self) -> bool:
        """检查当前目录是否是 Git 仓库"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def get_staged_diff(self) -> str:
        """获取暂存区的变更内容"""
        result = subprocess.run(
            ["git", "diff", "--cached", "--no-color"],
            capture_output=True,
            text=True
        )
        return result.stdout
    
    def get_staged_files(self) -> List[str]:
        """获取暂存的文件列表"""
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True
        )
        return [f for f in result.stdout.strip().split('\n') if f]
    
    def get_repo_name(self) -> Optional[str]:
        """获取仓库名称"""
        try:
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                url = result.stdout.strip()
                # 解析仓库名
                if '/' in url:
                    name = url.rstrip('.git').split('/')[-1]
                    return name
        except Exception:
            pass
        return None
    
    def get_current_branch(self) -> Optional[str]:
        """获取当前分支"""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except Exception:
            pass
        return None
    
    def get_recent_commits(self, n: int = 5) -> List[Tuple[str, str]]:
        """获取最近的提交记录"""
        result = subprocess.run(
            ["git", "log", "--oneline", "-n", str(n)],
            capture_output=True,
            text=True
        )
        commits = []
        for line in result.stdout.strip().split('\n'):
            if ' ' in line:
                hash_, msg = line.split(' ', 1)
                commits.append((hash_, msg))
        return commits
