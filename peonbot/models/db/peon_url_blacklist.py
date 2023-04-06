from tortoise import fields
from tortoise.models import Model

class PeonUrlBlackList(Model):

    chat_id = fields.CharField(max_length=40, index=True)
    pattern_list = fields.JSONField()

    class Meta:
        table = "peon_url_blacklist"
