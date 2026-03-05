#!/bin/bash
# 基础使用示例

# 1. 配置 API Key
ai-commit config set openai.api_key sk-your-openai-key

# 2. 修改代码并暂存
echo "# New feature" >> README.md
git add README.md

# 3. 生成提交信息
ai-commit

# 4. 使用不同模型
ai-commit --model gpt-4

# 5. 使用 emoji 风格
ai-commit --style emoji

# 6. 预览模式（不实际提交）
ai-commit --dry-run
