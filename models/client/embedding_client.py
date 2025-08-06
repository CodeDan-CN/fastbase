from langchain.embeddings import HuggingFaceEmbeddings
from typing import Optional

from exception.custom_exception import CustomErrorThrowException


class EmbeddingClient:
    """
    简化版 EmbeddingClient，仅支持 HuggingFace 本地模型
    """
    _instance: Optional[HuggingFaceEmbeddings] = None

    @classmethod
    def init(cls, model_path: str, device: str = "cpu"):
        """
        初始化本地模型，只执行一次
        """
        if cls._instance is None:
            cls._instance = HuggingFaceEmbeddings(
                model_name=model_path,
                model_kwargs={"device": device}
            )

    @classmethod
    def get(cls) -> HuggingFaceEmbeddings:
        """
        获取模型实例
        """
        if cls._instance is None:
            raise CustomErrorThrowException(601,"EmbeddingClient not initialized. Call `init(...)` first.")
        return cls._instance
