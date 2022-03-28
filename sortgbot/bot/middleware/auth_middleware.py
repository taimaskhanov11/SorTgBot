from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from loguru import logger

class AuthMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        logger.trace(message)
        user = users.get(message.from_user.id)
        logger.trace(user)
        data.update(user=user)
        # return {
        #     "user":user
        # }