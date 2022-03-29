from aiogram import Dispatcher

from sortgbot.bot.filters.main_filter import MainFilter
from sortgbot.bot.handlers.common_menu import main_start


def register_end_case_handlers(dp: Dispatcher):
    dp.register_message_handler(main_start, MainFilter(), state="*")
