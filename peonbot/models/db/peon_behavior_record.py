from tortoise import fields
from tortoise.models import Model
from peonbot.models.common import MemberLevel

class PeonBehaviorRecord(Model):

    chat_id = fields.CharField(max_length=40, index=True)
    user_id = fields.CharField(max_length=40, index=True)
    full_name = fields.TextField()
    msg_count = fields.IntField()
    member_level = fields.IntEnumField(enum_type=MemberLevel)
    update_time = fields.DatetimeField(auto_now=True)
    created_time = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "peon_behavior_record"
