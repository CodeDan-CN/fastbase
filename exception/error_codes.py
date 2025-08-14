from enum import Enum

class ErrorCode(Enum):
    SYSTEM_INIT_ERROR = (101,"项目启动初始化异常")
    LLM_INIT_NAMESPACE_ERROR = (102,"Namespace not initialized")
    LLM_INIT_LOADER_ERROR = (103, "暂不支持此类别模型加载方式")

    USERNAME_OR_PASSWORD_UNDEFINED = (601,"用户账号或者密码为空，请检查填写内容")
    USER_NOT_FOUND = (602,"没有找到用户信息")
    TOKEN_PAYLOAD_INVALID = (603, "token状态已过期")
    USER_STATUS_INVALID= (604,"当前用户账户状态处于未启用状态")
    USER_ACCOUNT_EXPIRED=(605,"用户账号已过期")
    USERNAME_DUPLICATE = (610, "用户名重复，请检查")
    FIELD_RANK_TOO_LONG = (611, "排序字段输入长度超出限制")
    FIELD_NAME_TOO_LONG = (612, "姓名字段输入长度超出限制")
    FIELD_USERNAME_TOO_LONG = (613, "用户名字段输入长度超出限制")
    DB_UNIQUE_CONFLICT = (614, "数据库唯一性冲突")
    USER_CREATE_FAILED = (615, "用户添加失败")

    MILVUS_COLLECTION_CREATE_ERROR = (701,"Failed to create Milvus collection from documents")
    MILVUS_SEARCH_SIMILARITY_FAILED = (702,"Milvus similarity_search error")
    MILVUS_SEARCH_WITH_SCOPE_FAILED = (703,"Milvus similarity_search_with_score error")
    MILVUS_DELETE_DOCUMENT_FAILED = (704,"Milvus delete_documents error")
    # 更多错误码...

    def __init__(self, code, message):
        self.code = code
        self.message = message
