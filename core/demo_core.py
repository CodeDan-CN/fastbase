from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models.client.embedding_client import EmbeddingClientFactory
from utils.milvus_client import EmbeddingMilvusClient


async def add_web_content_to_vector(url:str):
    """
    :param url:
    :return:
    """
    loader = WebBaseLoader(web_path="https://baike.baidu.com/item/XIAOMI%20SU7%20Ultra/64669588")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)
    embedding_function = EmbeddingClientFactory.get_client()
    EmbeddingMilvusClient.from_documents(embedding_function=embedding_function,documents=all_splits,collection_name="test")
    return True
