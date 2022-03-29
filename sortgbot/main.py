import asyncio
import logging

from aiogram import Bot
from aiogram.types import BotCommand
from loguru import logger

from sortgbot.bot.filters.main_filter import MainFilter
from sortgbot.bot.handlers.admin_handlers.admin_menu import register_admin_menu_handlers
from sortgbot.bot.handlers.common_menu import register_common_handlers
from sortgbot.bot.handlers.end_case import register_end_case_handlers
from sortgbot.bot.middleware.auth_middleware import AuthMiddleware
from sortgbot.config.log_settings import init_logging
from sortgbot.db.db_main import init_tortoise
from sortgbot.loader import bot, dp


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Главное меню"),
        BotCommand(command="/admin", description="Админ панель"),
    ]
    await bot.set_my_commands(commands)


async def main():
    # Настройка логирования
    init_logging(old_logger=True, level=logging.DEBUG, steaming=False)
    logger.info(f"Starting bot {(await bot.get_me()).username}")

    # Установка команд бота
    await set_commands(bot)

    # Инициализация базы данных
    await init_tortoise()
    # Меню админа
    # register_admin_commands_handlers(dp)

    # Регистрация хэндлеров
    register_admin_menu_handlers(dp)
    register_common_handlers(dp)
    register_end_case_handlers(dp)
    # Регистрация middleware
    # dp.middleware.setup(FatherMiddleware())
    # dp.middleware.setup(AuthMiddleware())
    # todo 19.03.2022 17:42 taima:
    # dp.middleware.setup(ThrottlingMiddleware(limit=0.5))

    # Регистрация фильтров
    # dp.filters_factory.bind(MainFilter,
    #                         event_handlers=[dp.message_handlers, dp.callback_query_handlers], )
    # print(dp.message_handlers)
    # asyncio.create_task(message_delete_worker())

    # Запуск поллинга
    # await dp.skip_updates()  # пропуск накопившихся апдейтов (необязательно)
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
