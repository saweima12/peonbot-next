from tortoise import fields
from tortoise.models import Model


class PeonDeletedMessage(Model):

    chat_id = fields.CharField(max_length=40, index=True)
    content_type = fields.CharField(max_length=40, index=True)
    message_json = fields.JSONField()
    record_date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "peon_deleted_message"
