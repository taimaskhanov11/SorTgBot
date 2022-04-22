from aiogram import types
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import BoundFilter
from loguru import logger

from sortgbot.bot.scenario.scenario import scenarios
from sortgbot.config.config import config
from sortgbot.db.models import User


class MainFilter(BoundFilter):
    @logger.catch
    async def check(self, message: types.Message):
        # logger.trace(message)
        ui = message.from_user.id
        is_admin = ui in config.bot.admins

        user, is_created = await User.get_or_create(
            user_id=ui, username=message.from_user.username, defaults={"is_admin": True} if is_admin else None
        )
        return {"user": user, "scenario": scenarios.get(user.language)}
