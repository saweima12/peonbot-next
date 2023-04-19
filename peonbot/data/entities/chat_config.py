from tortoise import fields
from tortoise.models import Model

class ChatConfig(Model):
    chat_id = fields.CharField(max_length=40, index=True)
    status = fields.CharField(max_length=8, index=True)
    chat_name = fields.TextField()
    config_json = fields.JSONField()
    permission_json = fields.JSONField(default={})
    attach_json = fields.JSONField(default={})

    class Meta:
        table = "peon_chat_config"