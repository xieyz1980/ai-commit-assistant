# 🤖 AI Commit Assistant

<p align="center">
  <a href="https://github.com/xieyz1980/ai-commit-assistant/stargazers"><img src="https://img.shields.io/github/stars/xieyz1980/ai-commit-assistant?style=social" alt="GitHub stars"></a>
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/AI-OpenAI%20%7C%20Claude%20%7C%20Gemini-orange.svg" alt="AI Providers">
</p>

<p align="center">
  <b>让 AI 帮你写 Git 提交信息</b><br>
  智能分析代码变更，生成专业、规范的 commit message
</p>

---

## ✨ 特性

- 🎯 **智能分析** - 自动分析代码变更，理解修改意图
- 📝 **规范提交** - 遵循 Conventional Commits 规范
- 🚀 **多模型支持** - 支持 OpenAI、Claude、Gemini、Azure 等
- ⚡ **极速响应** - 本地缓存，重复提交秒级响应
- 🔧 **Git 集成** - 支持 Git Hook，自动拦截空提交信息
- 🎨 **自定义模板** - 支持自定义提交信息模板
- 🌍 **多语言支持** - 支持中英文等多语言提交信息

---

## 📦 安装

### 使用 pip 安装（推荐）

```bash
pip install ai-commit-assistant
```

### 使用 Homebrew 安装

```bash
brew tap xieyz1980/ai-commit
brew install ai-commit-assistant
```

### 从源码安装

```bash
git clone https://github.com/xieyz1980/ai-commit-assistant.git
cd ai-commit-assistant
pip install -e .
```

---

## 🚀 快速开始

### 1. 配置 API Key

```bash
# OpenAI
ai-commit config set openai.api_key sk-your-key

# Claude
ai-commit config set anthropic.api_key sk-ant-your-key

# Gemini
ai-commit config set gemini.api_key your-key
```

### 2. 使用

```bash
# 分析当前变更并生成提交信息
ai-commit

# 或者使用 git 别名
git ai-commit
```

---

## 📖 使用示例

### 基础使用

```bash
# 修改代码后
$ git add .

# 生成提交信息
$ ai-commit
📝 feat(auth): 添加用户登录验证功能

- 实现 JWT token 生成和验证
- 添加登录/登出接口
- 集成密码加密存储

# 确认提交
$ git commit -m "$(ai-commit --raw)"
```

### 使用不同模型

```bash
# 使用 Claude
ai-commit --model claude-3-opus-20240229

# 使用 GPT-4
ai-commit --model gpt-4-turbo-preview

# 使用 Gemini
ai-commit --model gemini-pro
```

### 自定义模板

```bash
# 设置自定义模板
ai-commit config set template "
{type}: {message}

{body}

{changes}
"

# 使用emoji风格
ai-commit --style emoji
```

---

## ⚙️ 配置

### 全局配置

```bash
# 查看当前配置
ai-commit config list

# 设置默认模型
ai-commit config set model gpt-4-turbo-preview

# 设置语言
ai-commit config set language zh

# 启用本地缓存
ai-commit config set cache.enabled true
```

### 项目级配置

在项目根目录创建 `.ai-commit.yml`：

```yaml
model: gpt-4-turbo-preview
language: zh
style: conventional
max_length: 100
templates:
  conventional: "{type}: {message}"
  emoji: "{emoji} {type}: {message}"
exclude:
  - "*.lock"
  - "node_modules/"
  - ".env"
```

---

## 🔧 Git Hook 集成

### 自动拦截空提交

```bash
# 安装 Git Hook
ai-commit hook install

# 现在 git commit 会自动调用 AI 生成提交信息
git commit
# AI 将分析变更并提示提交信息
```

### 手动配置 Hook

在 `.git/hooks/prepare-commit-msg` 添加：

```bash
#!/bin/bash
COMMIT_MSG_FILE=$1

# 如果提交信息为空，使用 AI 生成
if [ ! -s "$COMMIT_MSG_FILE" ]; then
    ai-commit --raw > "$COMMIT_MSG_FILE"
fi
```

---

## 🎨 提交风格

### Conventional Commits（默认）

```
feat(auth): add JWT authentication
fix(api): resolve null pointer exception
docs(readme): update installation guide
refactor(core): simplify error handling
test(auth): add unit tests for login
```

### Emoji 风格

```
✨ feat(auth): add JWT authentication
🐛 fix(api): resolve null pointer exception
📝 docs(readme): update installation guide
♻️ refactor(core): simplify error handling
✅ test(auth): add unit tests for login
```

### 自定义风格

```bash
ai-commit --style custom --template "[{type}] {message}"
```

---

## 🔌 支持的 AI 提供商

| 提供商 | 模型 | 配置方式 |
|--------|------|----------|
| OpenAI | gpt-4, gpt-3.5-turbo | `openai.api_key` |
| Anthropic | claude-3-opus, claude-3-sonnet | `anthropic.api_key` |
| Google | gemini-pro, gemini-ultra | `gemini.api_key` |
| Azure | azure-gpt-4 | `azure.api_key`, `azure.endpoint` |
| OpenRouter | 多种模型 | `openrouter.api_key` |
| 本地模型 | Ollama, LM Studio | `local.endpoint` |

---

## 🛠️ 开发

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/xieyz1980/ai-commit-assistant.git
cd ai-commit-assistant

# 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements-dev.txt
pip install -e .

# 运行测试
pytest tests/

# 代码格式化
black src/
isort src/
```

### 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📈 路线图

- [x] 基础提交信息生成
- [x] 多模型支持
- [x] Git Hook 集成
- [x] 本地缓存
- [ ] VSCode 扩展
- [ ] JetBrains 插件
- [ ] 提交信息评分系统
- [ ] 团队规范检查
- [ ] CI/CD 集成

---

## 📝 许可证

[MIT](LICENSE) © xieyz1980

---

## 🙏 致谢

感谢所有贡献者和使用者！如果觉得这个项目有帮助，请给个 ⭐️ 支持一下！

<p align="center">
  <a href="https://github.com/xieyz1980/ai-commit-assistant/stargazers">
    <img src="https://img.shields.io/github/stars/xieyz1980/ai-commit-assistant?style=social" alt="GitHub stars">
  </a>
</p>
