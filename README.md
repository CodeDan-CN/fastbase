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

##### core包
编写业务的核心逻辑包，存放web包中接口处理的核心逻辑以及负责与数据持久操作交互（数据持久操作后续会详细说明）。
```python
async def delete_user_by_id(user_id: int) -> bool:
    """
    删除用户
    :param user_id: 用户 ID
    :return: 是否删除成功
    """
    user = await User.get_or_none(id=user_id)
    if user:
        await user.delete()
        logger.info(f"用户删除成功: ID={user_id}")
        return True
    logger.warning(f"删除失败，用户不存在: ID={user_id}")
    return False
```
其中User是数据持久层创建的与数据库表对应的实体

##### entity（database）包
此包是数据持久操作定义的实体类，本框架使用`tortoise-orm`orm框架，在使用上和MyBatis很像，特别方便。下述是对应的数据库表和其实体类代码
```sql
CREATE TABLE `user` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(50) NOT NULL UNIQUE,
    `email` VARCHAR(100) NOT NULL UNIQUE,
    `is_active` BOOLEAN NOT NULL DEFAULT TRUE,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```
那他对应的数据实体代码为：
```python
from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)  # 主键，自增
    username = fields.CharField(max_length=50, unique=True)  # 用户名，唯一
    email = fields.CharField(max_length=100, unique=True)  # 邮箱，唯一
    is_active = fields.BooleanField(default=True)  # 是否激活
    created_at = fields.DatetimeField(auto_now_add=True)  # 创建时间
    updated_at = fields.DatetimeField(auto_now=True)  # 更新时间****
```
tortoise-orm不需要去定义具体的数据持久化类，他的快捷curd操作均在from tortoise.models import Model中，所以我们可以通过直接操作实体类去调用curd方法。
 
**类方法（Model 级别的）**

| 方法                                                  | 说明                                   |
| --------------------------------------------------- | ------------------------------------ |
| `create(**kwargs)`                                  | 创建并保存对象（等同于 `save()`）                |
| `get(**kwargs)`                                     | 获取一个匹配记录（找不到或多条时抛异常）                 |
| `get_or_none(**kwargs)`                             | 获取一个匹配记录，找不到时返回 `None`               |
| `get_or_create(defaults: dict = None, **kwargs)`    | 获取或创建（若不存在）                          |
| `update_or_create(defaults: dict = None, **kwargs)` | 更新或创建（若不存在）                          |
| `filter(**kwargs)`                                  | 返回一个 QuerySet（可用于链式查询）               |
| `all()`                                             | 获取所有记录                               |
| `first()`                                           | 获取第一条记录                              |
| `last()`                                            | 获取最后一条记录                             |
| `exists()`                                          | 判断是否存在符合条件的记录（返回布尔）                  |
| `count()`                                           | 计数                                   |
| `delete()`                                          | 删除符合条件的记录（⚠️ 是 QuerySet 上的方法，不是实例方法） |


**实例方法（对象级别）**

| 方法                             | 说明                               |
| ------------------------------ | -------------------------------- |
| `save()`                       | 保存当前对象（新建或更新）                    |
| `delete()`                     | 删除当前对象                           |
| `fetch_related(*fields)`       | 预加载关联字段（ManyToMany / ForeignKey） |
| `update_from_dict(data: dict)` | 快速从字典更新字段（不会自动保存）                |
| `pk`                           | 主键值的快捷访问（等价于 `self.id`）          |

**高级用法**
```.filter()
await User.filter(username="alice")   # 相当于: WHERE username = 'alice'
```

| Python 写法                          | SQL 等价               | 说明       |
| ---------------------------------- | -------------------- | -------- |
| `.filter(field=value)`             | `field = value`      | 等于       |
| `.filter(field__not=value)`        | `field != value`     | 不等于      |
| `.filter(field__in=[...])`         | `field IN (...)`     | in 查询    |
| `.filter(field__not_in=[...])`     | `field NOT IN (...)` | not in   |
| `.filter(field__contains="abc")`   | `LIKE '%abc%'`       | 模糊包含     |
| `.filter(field__icontains="abc")`  | `ILIKE '%abc%'`      | 忽略大小写包含  |
| `.filter(field__startswith="abc")` | `LIKE 'abc%'`        | 以...开头   |
| `.filter(field__endswith="abc")`   | `LIKE '%abc'`        | 以...结尾   |
| `.filter(field__isnull=True)`      | `IS NULL`            | 是否为 NULL |
| `.filter(field__gte=5)`            | `>= 5`               | 大于等于     |
| `.filter(field__lte=10)`           | `<= 10`              | 小于等于     |
| `.filter(Q(...))`                  | `(表达式)`              | 支持复杂组合条件 |

##### mapping包
存放业务对应的复杂SQL，由于orm不可能满足所有复杂的SQL，所以可以通过自定义SQL的方式进行查询和操作
```python
# 在mapping层
USER_Online_SQL="SELECT id, username FROM user WHERE is_active=TRUE"

# 在core层
users = await User.raw(USER_Online_SQL)

for user in users:
    print(user.id, user.username)     # ✅ 正常
    print(user.email)                 # ⚠️ 报错或是 None
```

### 快速启动
1、安装conda
2、下载requirement.txt中的依赖
3、点击运行app.py即可