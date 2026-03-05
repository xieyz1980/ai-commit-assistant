"""
AI 提供商模块
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseProvider(ABC):
    """AI 提供商基类"""
    
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """生成文本"""
        pass


class OpenAIProvider(BaseProvider):
    """OpenAI 提供商"""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.api_key = api_key
        self.model = model
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=self.api_key)
            except ImportError:
                raise ImportError("请安装 openai: pip install openai")
        return self._client
    
    def generate(self, prompt: str) -> str:
        try:
            client = self._get_client()
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的Git提交信息生成助手。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"错误: {e}"


class MockProvider(BaseProvider):
    """模拟提供商（用于测试）"""
    
    def generate(self, prompt: str) -> str:
        # 简单的模拟响应
        return """feat(core): 添加基础项目结构

- 创建核心模块和配置文件
- 实现Git工具类和配置管理
- 添加CLI命令行接口"""


def get_provider(model: str, config) -> BaseProvider:
    """获取 AI 提供商"""
    # 检测模型类型
    if "gpt" in model.lower():
        api_key = config.get("openai.api_key")
        if not api_key:
            raise ValueError("未设置 OpenAI API Key，请运行: ai-commit config set openai.api_key <your-key>")
        return OpenAIProvider(api_key, model)
    
    # 默认使用模拟提供商（无需API Key）
    return MockProvider()
