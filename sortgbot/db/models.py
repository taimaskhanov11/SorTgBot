from tortoise import models, fields

from sortgbot.bot.scenario.scenario import Scenario


class User(models.Model):
    user_id = fields.BigIntField()
    username = fields.CharField(max_length=30, null=True)
    language = fields.CharField(max_length=15, null=True)
    is_admin = fields.BooleanField(default=False)

    def __str__(self):
        return f"@{self.username}:{self.user_id}"
