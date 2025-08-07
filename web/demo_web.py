from fastapi import APIRouter, Form

from core.demo_core import add_web_content_to_vector
from utils.base_response import BaseResponse

demo = APIRouter()

@demo.post("/add")
async def add_vector(url:str=Form(...,description="目标url")):
    """

    :param url:
    :return:
    """
    await add_web_content_to_vector(url)
    return BaseResponse(code=200,msg="success",data=None)
