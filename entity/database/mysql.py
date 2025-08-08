from tortoise import fields
from tortoise.models import Model


from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.BigIntField(pk=True, description="自增主键")
    user_id = fields.CharField(max_length=36, null=True, description="唯一标识")
    name = fields.CharField(max_length=50, null=True, description="姓名")
    username = fields.CharField(max_length=20, unique=True, null=True, description="用户名")  # 加了唯一约束
    password = fields.CharField(max_length=50, null=True, description="用户密码")
    department = fields.CharField(max_length=50, null=True, description="所属部门")
    position = fields.CharField(max_length=50, null=True, description="所属岗位")
    role_id = fields.CharField(max_length=50, null=True, description="角色编号")
    rank = fields.IntField(null=True, description="排序")
    status = fields.IntField(default=1, description="状态（0：删除，1：启用）")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    create_by = fields.CharField(max_length=20, null=True, description="创建人")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    update_by = fields.CharField(max_length=20, null=True, description="更新人")
    expired_date = fields.DatetimeField(null=True, description="账号过期时间")
    last_login_time = fields.DatetimeField(null=True, description="最近登录时间")

    class Meta:
        table = "system_user"
        table_description = "系统用户表"


class Role(Model):
    id = fields.BigIntField(pk=True, description="自增主键")
    role_id = fields.CharField(max_length=32, unique=True, description="唯一标识")
    name = fields.CharField(max_length=50, description="角色名称")
    remark = fields.TextField(null=True, description="备注")
    status = fields.IntField(description="状态（0：删除，1：启用）")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    create_by = fields.CharField(max_length=20, null=True, description="创建人")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    update_by = fields.CharField(max_length=20, null=True, description="更新人")

    class Meta:
        table = "system_role"
        table_description = "角色表"
