from enum import Enum

class ErrorCode(Enum):
    SYSTEM_INIT_ERROR = (101,"项目启动初始化异常")

    USERNAME_OR_PASSWORD_UNDEFINED = (601,"用户账号或者密码为空，请检查填写内容")
    USER_NOT_FOUND = (602,"没有找到用户信息")
    TOKEN_PAYLOAD_INVALID = (603, "Token中包含的用户信息异常，请检查token生成流程")
    USER_STATUS_INVALID= (604,"当前用户账户状态处于未启用状态")
    USER_ACCOUNT_EXPIRED=(605,"用户账号已过期")
    USERNAME_DUPLICATE = (610, "用户名重复，请检查")
    FIELD_RANK_TOO_LONG = (611, "排序字段输入长度超出限制")
    FIELD_NAME_TOO_LONG = (612, "姓名字段输入长度超出限制")
    FIELD_USERNAME_TOO_LONG = (613, "用户名字段输入长度超出限制")
    DB_UNIQUE_CONFLICT = (620, "数据库唯一性冲突")
    USER_CREATE_FAILED = (630, "用户添加失败")
    # 更多错误码...

    def __init__(self, code, message):
        self.code = code
        self.message = message
