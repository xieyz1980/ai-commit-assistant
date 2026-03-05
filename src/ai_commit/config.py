"""
配置管理模块
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """配置管理类"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "ai-commit"
        self.config_file = self.config_dir / "config.yml"
        self._config = {}
        self._load()
    
    def _load(self):
        """加载配置"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self._config = yaml.safe_load(f) or {}
            except Exception:
                self._config = {}
        
        # 加载项目级配置
        project_config = Path(".ai-commit.yml")
        if project_config.exists():
            try:
                with open(project_config, 'r', encoding='utf-8') as f:
                    project_settings = yaml.safe_load(f) or {}
                    self._config.update(project_settings)
            except Exception:
                pass
    
    def save(self):
        """保存配置"""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self._config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value if value is not None else default
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split('.')
        config = self._config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
        self.save()
    
    def list_all(self) -> Dict[str, Any]:
        """列出所有配置"""
        return self._config.copy()
