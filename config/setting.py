import tomli
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # 项目根目录
CONFIG_PATH = BASE_DIR / "config" / "config.toml"

class Settings:
    def __init__(self, config_file=CONFIG_PATH):
        with open(config_file, "rb") as f:
            config_data = tomli.load(f)

        self.server = config_data.get("server", {})
        self.mysql = config_data.get("mysql", {})
        self.milvus = config_data.get("milvus", {})
        self.app = config_data.get("app", {})
        self.llm_default = config_data.get("llm-default", {})
        self.embedding_model = config_data.get("embedding-model", {})

# 全局唯一配置实例
settings = Settings()

