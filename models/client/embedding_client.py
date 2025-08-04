from typing import Optional, Any, Dict

from langchain_milvus import Milvus


class EmbeddingMilvusClient:
    """
    一个围绕LangChain的Milvus向量存储的单例包装器，
    由FastAPI的启动和关闭事件管理。
    """
    _client: Optional[Milvus] = None

    @classmethod
    def init(cls,
             embedding_function: Any,
             collection_name: str,
             connection_args: Dict[str, Any]) -> None:
        """
        使用给定的嵌入函数初始化Milvus向量存储，
        集合名称，以及Milvus连接参数。
        应在应用程序启动时调用一次。

        :param embedding_function: LangChain Embeddings 实例
        :param collection_name: Milvus集合的名称
        :param connection_args: 包含Milvus主机、端口等信息的字典。
        """
        if cls._client is None:
            cls._client = Milvus(
                embedding_function=embedding_function,
                connection_args=connection_args
            )
            print("EmbeddingMilvusClient initialized")
        else:
            print("EmbeddingMilvusClient already initialized")
