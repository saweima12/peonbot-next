from tortoise import fields
from tortoise.models import Model


class PeonWatchUser(Model):
    chat_id = fields.CharField(max_length=40, index=True)
    user_id = fields.CharField(max_length=40, index=True)
    status = fields.CharField(max_length=8)
    attach_json = fields.JSONField()

    class Meta:
        table = "peon_watch_user"
