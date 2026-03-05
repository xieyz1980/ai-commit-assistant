from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-commit-assistant",
    version="0.1.0",
    author="xieyz1980",
    author_email="45018045@qq.com",
    description="智能Git提交助手 - AI Commit Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xieyz1980/ai-commit-assistant",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
    ],
    extras_require={
        "openai": ["openai>=1.0.0"],
        "anthropic": ["anthropic>=0.18.0"],
        "google": ["google-generativeai>=0.3.0"],
        "all": [
            "openai>=1.0.0",
            "anthropic>=0.18.0",
            "google-generativeai>=0.3.0",
        ],
        "dev": [
            "pytest>=7.0",
            "black>=23.0",
            "isort>=5.0",
            "flake8>=6.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-commit=ai_commit.cli:main",
        ],
    },
    keywords="git, commit, ai, llm, openai, claude, automation, developer-tools",
    project_urls={
        "Bug Reports": "https://github.com/xieyz1980/ai-commit-assistant/issues",
        "Source": "https://github.com/xieyz1980/ai-commit-assistant",
    },
)
