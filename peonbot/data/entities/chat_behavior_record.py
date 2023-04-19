from tortoise import fields
from tortoise.models import Model

class ChatBehaviorRecord(Model):

    chat_id = fields.CharField(max_length=40, index=True)
    user_id = fields.CharField(max_length=40, index=True)
    full_name = fields.TextField()
    msg_count = fields.IntField()
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "peon_behavior_record"