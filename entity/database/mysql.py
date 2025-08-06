from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk=True)  # 主键，自增
    username = fields.CharField(max_length=50, unique=True)  # 用户名，唯一
    email = fields.CharField(max_length=100, unique=True)  # 邮箱，唯一
    is_active = fields.BooleanField(default=True)  # 是否激活
    created_at = fields.DatetimeField(auto_now_add=True)  # 创建时间
    updated_at = fields.DatetimeField(auto_now=True)  # 更新时间

    def __str__(self):
        return self.username