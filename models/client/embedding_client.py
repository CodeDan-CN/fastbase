import logging
from typing import Literal, Optional, Dict

from langchain_ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEndpointEmbeddings,HuggingFaceEmbeddings

logger = logging.getLogger(__name__)

# 定义支持的嵌入模型类型
EmbeddingSource = Literal["ollama", "hf", "tei"]

class EmbeddingClientFactory:
    """
    嵌入模型客户端工厂类。
    在 FastAPI 启动阶段初始化不同嵌入模型的参数，
    根据传入 source 返回对应的嵌入实例。
    """

    _ollama_model: Optional[str] = None
    _hf_model: Optional[str] = None
    _tei_endpoint: Optional[str] = None
    _source: Optional[EmbeddingSource] = None

    @classmethod
    def init(cls, config: Dict[str, str]):
        """
        初始化三个嵌入模型的配置。
        应在 FastAPI 启动阶段调用。

        Args:
            config: 一个包含 ollama、hf、tei 模型配置的字典
        """
        cls._ollama_model = config.get("ollama_model")
        cls._hf_model = config.get("hf_model")
        cls._tei_endpoint = config.get("tei_endpoint")
        cls._source = config.get("source")

        logger.info("EmbeddingClientFactory initialized with: ")
        logger.info(f" - Ollama model: {cls._ollama_model}")
        logger.info(f" - HF model: {cls._hf_model}")
        logger.info(f" - TEI endpoint: {cls._tei_endpoint}")

    @classmethod
    def get_client(cls, source: EmbeddingSource=None):
        """
        获取指定 source 类型的嵌入模型客户端实例。

        Args:
            source: 模型来源类型，可为 "ollama", "hf", "tei"

        Returns:
            一个符合 LangChain Embeddings 接口的实例
        """
        if source is None:
            source = cls._source
        if source == "ollama":
            if not cls._ollama_model:
                raise ValueError("Ollama 模型未配置")
            logger.debug(f"Using OllamaEmbedding: {cls._ollama_model}")
            return OllamaEmbeddings(model=cls._ollama_model)

        elif source == "hf":
            if not cls._hf_model:
                raise ValueError("HuggingFace 模型未配置")
            logger.debug(f"Using HuggingFaceEmbedding: {cls._hf_model}")
            return HuggingFaceEmbeddings(model_name=cls._hf_model)

        elif source == "tei":
            if not cls._tei_endpoint:
                raise ValueError("TEI 接口地址未配置")
            logger.debug(f"Using TEI endpoint: {cls._tei_endpoint}")
            return HuggingFaceEndpointEmbeddings(model=cls._tei_endpoint)

        else:
            raise ValueError(f"不支持的嵌入来源类型: {source}")
