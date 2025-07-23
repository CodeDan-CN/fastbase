# FastBase脚手架：帮助你快速搭建基于FastAPI的Web应用
### 整体介绍
此脚手架可以帮你快速的构建功能完善的web应用，因为他自带“结构规整的web代码编写层级规范”、“全局异常捕获和自定义异常”、“日志打印及持久化”、“无感知ORM框架嵌入”、“配置统一管理”、“支持多种数据库接入”以及“可访问的swagger接口文档”，接下来我们就一个一个来看看这些功能在此脚手架中是如何体现的

```TEXT
fastbase
    |
    cofig
    |
    core
    |
    entity
    |
    exception
    |
    mapping
    |
    models
    |
    utils
    |
    web
    app.py
```
###  结构规整的web代码编写层级规范
一个闭环的web响应流程会涉及到上述目录下的web、core、mapping、entity（schema）包 
##### web包：存放的定义网络接口代码
通过集成pydantic和fastapi的特性，实现网络接口json格式数据与实体类的映射，方便进行参数的接收。当然也支持form表单、url路径中参数的提取。

**1、url参数的提取**
```python
# 定义fastapi的路由，并确定取名为当前接口层对应业务名称，一个相关业务py文件内只需要定义一次即可
user = APIRouter() 
@user.get("/info/{user_id}")
async def get_user(user_id: int):
    user = await get_user_by_id(user_id)
    if not user:
        raise CustomErrorThrowException(status_code=404, detail="User not found")
    return BaseResponse(code=200, msg="success", data=user)
```

**2、form表单的参数提取**
```python
# 定义fastapi的路由，并确定取名为当前接口层对应业务名称，一个相关业务py文件内只需要定义一次即可
user = APIRouter() 
@user.post("/info")
async def get_user_from_form(
    user_id: int = Form(...),
    file: UploadFile = File(...)
):
    """
    根据表单提交的用户ID查询用户信息，并处理上传的文件。

    参数:
    - user_id (int): 从表单中接收的用户ID，字段名为 'user_id'。
    - file (UploadFile): 从 multipart/form-data 中上传的文件，字段名为 'file'。

    返回:
    - BaseResponse: 自定义的统一响应格式，包含状态码、消息和用户数据。
    """
    user = await get_user_by_id(user_id)
    if not user:
        raise CustomErrorThrowException(status_code=404, detail="User not found")

    # 你可以在这里处理 file，比如保存、读取内容等
    file_content = await file.read()
    # 这里只是演示打印文件名和大小
    print(f"Uploaded file: {file.filename}, size: {len(file_content)} bytes")

    return BaseResponse(code=200, msg="success", data=user)
```

**3、json格式参数提取**
```python
# 定义fastapi的路由，并确定取名为当前接口层对应业务名称，一个相关业务py文件内只需要定义一次即可
@user.post("/add")
async def create_user(user: UserCreate):
    """
    创建用户接口
    
    参数:
    - user: UserCreate 类型，通过请求体（JSON）传入的用户信息，包含 username 和 email。

    返回:
    - BaseResponse: 包含状态码、提示信息和创建成功的用户对象。
    """
    user_obj = await create_user_info(user.username, user.email)
    return BaseResponse(code=200, msg="success", data=user_obj)
```
上述参数接收方式可以覆盖大多数应用场景，极大程度支持了restful风格
而在json格式参数提取中，我们通过定义实体类去接收了json参数，这就引出了实体类在我们这个脚手架中如何去定义

##### entity（schema）包
schema包下专门定义用于接口层参数接收和参数返回的数据实体，我们就拿上一步中的json参数映射的UserCreate实体类来演示
```python
# 这是简单使用
class UserCreate(BaseModel):
    username: str
    email: str = 'CODEDAN@163.COM'

# 这是复杂使用，其中...是代表必填的意思，这样写的好处是可以被swagger监听到
class UserCreate(BaseModel):
    username: str = Field(..., title="用户名", description="新用户的用户名", min_length=3, max_length=30)
    email: str = Field(title="邮箱", description="新用户的邮箱地址", example="user@example.com",default="test@example.com")
```
如果想要在swagger文档中定义出好看的接口参数，推荐使用复杂写法



