from typing import Annotated

from fastapi import APIRouter, Form, Depends

from core.demo_core import add_web_content_to_vector, chat_model, get_document_by_title, \
    get_document_by_title_with_score, delete_document_by_title
from utils.base_response import BaseResponse

demo = APIRouter()


@demo.post("/embedding")
async def add_vector(url: str = Form(..., description="目标url")):
    """

    :param url:
    :return:
    """
    await add_web_content_to_vector(url)
    return BaseResponse(code=200, msg="success", data=None)


@demo.post("/chat")
async def add_vector(user_input: str = Form(..., description="用户问题"),
                     name:str = Form(...,description="ai智能名称")):
    """

    :param url:
    :return:
    """
    response = await chat_model(user_input,name)
    return BaseResponse(code=200, msg="success", data=response)

@demo.post("/get")
async def get_document(query: str = Form(..., description="用户问题"),
                       title:str = Form(...,description="标题")):
    document = await get_document_by_title(query,title)
    return BaseResponse(code=200, msg="success", data=document)

@demo.post("/get/score")
async def get_document(query: str = Form(..., description="用户问题"),
                       title:str = Form(...,description="标题")):
    document = await get_document_by_title_with_score(query,title)
    return BaseResponse(code=200, msg="success", data=document)

@demo.post("/delete")
async def delete_document(title:str = Form(...,description="标题")):
    document = await delete_document_by_title(title)
    return BaseResponse(code=200, msg="success", data=None)