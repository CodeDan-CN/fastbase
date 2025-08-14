from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

from models.client.embedding_client import EmbeddingClientFactory
from models.client.llm_client import LLMClient
from utils.milvus_client import EmbeddingMilvusClient


async def add_web_content_to_vector(url:str):
    """
    :param url:
    :return:
    """
    # loader = WebBaseLoader(web_path="https://baike.baidu.com/item/XIAOMI%20SU7%20Ultra/64669588")
    loader = WebBaseLoader(web_path=url)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)
    embedding_function = EmbeddingClientFactory.get_client()
    EmbeddingMilvusClient.from_documents(embedding_function=embedding_function,documents=all_splits,collection_name="test01")
    return True

async def chat_model(user_input:str,name:str):

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system","你是一个智能助手，你的名字是{name}"),
            ("human","我的问题是{user_input}")
        ]
    )
    chat = LLMClient.get()
    chain = prompt_template | chat
    response = chain.invoke({
        "name":name,
        "user_input":user_input,
    })
    # 非流式
    return response.content


async def get_document_by_title(query:str,title:str):
    embedding_function = EmbeddingClientFactory.get_client()
    document = EmbeddingMilvusClient.similarity_search(query=query,embedding_function=embedding_function,collection_name="test01",expr=f"title == '{title}'")
    return document


async def get_document_by_title_with_score(query:str,title:str):
    embedding_function = EmbeddingClientFactory.get_client()
    document = EmbeddingMilvusClient.similarity_search_with_score(query=query,embedding_function=embedding_function,collection_name="test01",expr=f"title == '{title}'")
    return document

async def delete_document_by_title(title:str):
    embedding_function = EmbeddingClientFactory.get_client()
    EmbeddingMilvusClient.delete_documents(embedding_function=embedding_function,collection_name="test01",expr=f"title == '{title}'",db_name="fastbase")
    return True