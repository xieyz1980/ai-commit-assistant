"""
提交信息生成器
"""

import re
from typing import Dict, Optional

from .providers import BaseProvider


class CommitGenerator:
    """提交信息生成器"""
    
    # Conventional Commits 类型
    COMMIT_TYPES = {
        "feat": "新功能",
        "fix": "修复",
        "docs": "文档",
        "style": "代码格式",
        "refactor": "重构",
        "perf": "性能优化",
        "test": "测试",
        "chore": "构建/工具",
        "ci": "CI/CD",
        "build": "构建",
        "revert": "回滚"
    }
    
    # Emoji 映射
    EMOJI_MAP = {
        "feat": "✨",
        "fix": "🐛",
        "docs": "📝",
        "style": "💎",
        "refactor": "♻️",
        "perf": "🚀",
        "test": "✅",
        "chore": "🔧",
        "ci": "👷",
        "build": "📦",
        "revert": "⏪"
    }
    
    def __init__(self, provider: BaseProvider, config):
        self.provider = provider
        self.config = config
    
    def generate(self, diff: str, style: str = "conventional", language: str = "zh") -> str:
        """生成提交信息"""
        # 截断过长的 diff
        max_diff_length = 4000
        if len(diff) > max_diff_length:
            diff = diff[:max_diff_length] + "\n... (内容已截断)"
        
        # 构建提示词
        prompt = self._build_prompt(diff, style, language)
        
        # 调用 AI 生成
        response = self.provider.generate(prompt)
        
        # 清理和格式化
        commit_msg = self._clean_response(response, style)
        
        return commit_msg
    
    def _build_prompt(self, diff: str, style: str, language: str) -> str:
        """构建提示词"""
        lang_name = "中文" if language == "zh" else "English"
        
        type_descriptions = "\n".join([
            f"- {k}: {v}" for k, v in self.COMMIT_TYPES.items()
        ])
        
        if style == "conventional":
            format_example = "feat(auth): 添加用户登录验证功能"
        elif style == "emoji":
            format_example = "✨ feat(auth): 添加用户登录验证功能"
        else:
            format_example = "添加用户登录验证功能"
        
        prompt = f"""请根据以下代码变更生成一条专业的 Git 提交信息。

要求：
1. 使用 {lang_name}
2. 遵循 Conventional Commits 规范
3. 类型必须从以下选择：
{type_descriptions}

4. 格式：{format_example}
5. 标题不超过 50 个字符
6. 如有需要，可在正文详细说明变更内容
7. 只返回提交信息，不要其他内容

代码变更：
```diff
{diff}
```

提交信息："""
        
        return prompt
    
    def _clean_response(self, response: str, style: str) -> str:
        """清理 AI 响应"""
        # 去除多余空白
        response = response.strip()
        
        # 去除代码块标记
        response = re.sub(r'^```\w*\n?', '', response)
        response = re.sub(r'\n?```$', '', response)
        
        # 去除引号
        response = response.strip('"\'')
        
        # 如果是 emoji 风格，确保有 emoji
        if style == "emoji":
            # 检查是否已经有 emoji
            if not any(emoji in response[:20] for emoji in self.EMOJI_MAP.values()):
                # 尝试根据类型添加 emoji
                for type_name, emoji in self.EMOJI_MAP.items():
                    if response.startswith(type_name) or f"{type_name}:" in response[:30]:
                        response = f"{emoji} {response}"
                        break
        
        return response.strip()
