from tortoise import fields
from tortoise.models import Model


class PeonUserWhitelist(Model):

    user_id = fields.CharField(max_length=40, index=True)
    status = fields.CharField(max_length=8)
    created_date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "peon_user_whitelist"
