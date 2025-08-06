import logging
from typing import Optional, Any, Dict, List

from langchain_milvus import Milvus
from exception.custom_exception import CustomErrorThrowException  # 自定义异常类（你原来已有）


class EmbeddingMilvusClient:
    """
    一个围绕 LangChain 的 Milvus 向量存储的轻量包装器。
    注意：Milvus 客户端不适合做单例，使用时建议每次调用创建新连接。
    """

    _host: str = "localhost"
    _port: int = 19530
    _index_params: Dict[str, Any] = {"index_type": "FLAT", "metric_type": "L2"}
    _db_name: str = "default"

    @classmethod
    def configure(cls, host: str, port: int, user: str = None, password: str = None, db_name: str = "default",
                  index_params: Optional[Dict[str, Any]] = None):
        """
        设置 Milvus 的基础连接配置，可在 FastAPI 启动时调用一次。

        Args:
            host: Milvus 地址
            port: Milvus 端口
            db_name: 数据库名称
            index_params: 创建向量索引所用的参数
        """
        cls._host = host
        cls._port = port
        cls._db_name = db_name
        cls.user = user,
        cls.password = password,
        if index_params:
            cls._index_params = index_params

        logging.info(f"Milvus client configured: host={host}, port={port}, db={db_name}")

    @classmethod
    def from_documents(cls,
                       embedding_function: Any,
                       documents: List[Any],
                       collection_name: str,
                       db_name: Optional[str] = None) -> Milvus:
        """
        将文档向量化后存入 Milvus 中，并返回向量库对象。

        Args:
            embedding_function: 用于生成向量的嵌入函数
            documents: 文档对象列表
            collection_name: Milvus 的 collection 名称
            db_name: 可选数据库名，默认使用类中配置

        Returns:
            Milvus 向量存储对象
        """
        try:
            db_name = db_name or cls._db_name
            logging.info(f"Creating Milvus collection: {collection_name} in db: {db_name}")
            client = Milvus(
                embedding_function=embedding_function,
                collection_name=collection_name,
                connection_args={
                    "host": cls._host,
                    "port": cls._port,
                    "db_name": db_name,
                    "user": cls.user,  # 新增字段
                    "password": cls.password  # 新增字段
                }
            )
            return client.from_documents(
                documents=documents,
                embedding=embedding_function,
                collection_name=collection_name,
                index_params=cls._index_params,
                connection_args={
                    "db_name": db_name
                }
            )
        except Exception as e:
            logging.exception("Failed to create Milvus collection from documents")
            raise CustomErrorThrowException(501, f"Milvus from_documents error: {str(e)}")

    @classmethod
    def similarity_search(cls,
                          query: str,
                          embedding_function: Any,
                          collection_name: str,
                          k: int = 4,
                          expr: Optional[str] = None,
                          timeout: Optional[float] = None,
                          db_name: Optional[str] = None) -> List[Any]:
        """
        基于 query 向量执行 Top-k 相似搜索。

        Args:
            query: 查询文本
            embedding_function: 嵌入函数
            collection_name: 要查询的 collection 名称
            k: 返回结果条数
            expr: 可选的过滤表达式
            timeout: 查询超时时间
            db_name: 可选数据库名，默认使用类中配置

        Returns:
            匹配的文档列表
        """
        try:
            db_name = db_name or cls._db_name
            client = Milvus(
                embedding_function=embedding_function,
                collection_name=collection_name,
                connection_args={
                    "host": cls._host,
                    "port": cls._port,
                    "user": cls.user,  # 新增字段
                    "password": cls.password,  # 新增字段
                    "db_name": db_name
                }
            )
            logging.debug(f"Executing similarity_search on {collection_name} with query: {query}")
            return client.similarity_search(query, k, expr, timeout)
        except Exception as e:
            logging.exception("Milvus similarity_search failed")
            raise CustomErrorThrowException(502, f"Milvus similarity_search error: {str(e)}")

    @classmethod
    def similarity_search_with_score(cls,
                                     query: str,
                                     embedding_function: Any,
                                     collection_name: str,
                                     k: int = 4,
                                     expr: Optional[str] = None,
                                     timeout: Optional[float] = None,
                                     db_name: Optional[str] = None) -> List[Any]:
        """
        与 similarity_search 类似，但返回的是 (文档, 相似度分数) 的元组列表。

        Returns:
            List of (doc, score) tuples
        """
        try:
            db_name = db_name or cls._db_name
            client = Milvus(
                embedding_function=embedding_function,
                collection_name=collection_name,
                connection_args={
                    "host": cls._host,
                    "port": cls._port,
                    "user": cls.user,  # 新增字段
                    "password": cls.password,  # 新增字段
                    "db_name": db_name
                }
            )
            logging.debug(f"Executing similarity_search_with_score on {collection_name}")
            return client.similarity_search_with_score(query, k, expr, timeout)
        except Exception as e:
            logging.exception("Milvus similarity_search_with_score failed")
            raise CustomErrorThrowException(503, f"Milvus similarity_search_with_score error: {str(e)}")

    @classmethod
    def delete_documents(cls,
                         collection_name: str,
                         ids: Optional[List[str]] = None,
                         expr: Optional[str] = None,
                         db_name: Optional[str] = None) -> bool:
        """
        删除指定 collection 中的数据（向量）。

        Args:
            collection_name: 要操作的 collection 名称
            ids: 可选，指定要删除的 document ID 列表
            expr: 可选，使用 Milvus 查询表达式删除数据
            db_name: 可选数据库名，默认使用初始化配置

        Returns:
            True 表示删除成功

        Raises:
            CustomErrorThrowException: 删除过程出错时抛出
        """
        try:
            db_name = db_name or cls._db_name
            logging.info(
                f"Deleting documents from collection: {collection_name}, db: {db_name}, ids: {ids}, expr: {expr}")
            client = Milvus(
                embedding_function=None,
                connection_args={
                    "host": cls._host,
                    "port": cls._port,
                    "user": cls.user,  # 新增字段
                    "password": cls.password,  # 新增字段
                    "db_name": db_name
                },
                collection_name=collection_name
            )
            client.delete(ids=ids, expr=expr)
            logging.info(f"Successfully deleted documents from collection: {collection_name}")
            return True
        except Exception as e:
            logging.exception("Milvus delete_documents failed")
            raise CustomErrorThrowException(504, f"Milvus delete_documents error: {str(e)}")
