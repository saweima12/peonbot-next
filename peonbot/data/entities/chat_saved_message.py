from tortoise import fields
from tortoise.models import Model


class ChatSavedMessage(Model):
    chat_id = fields.CharField(max_length=40, index=True)
    message_id = fields.CharField(max_length=40, index=True)
    message_json = fields.JSONField()
    record_date = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "peon_saved_message"