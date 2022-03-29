from itertools import chain

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger


def ibtn(text, data):
    return InlineKeyboardButton(text=text, callback_data=data)


lang_choice = ReplyKeyboardMarkup(
    [
        ["🇷🇺Русский, орыс", "🇰🇿Казахский, қазақ"],
        [],
    ],
    resize_keyboard=True,
)

start_button = ReplyKeyboardMarkup(
    [
        ["/start"],
        [],
    ],
    resize_keyboard=True,
)

numbers_button = ReplyKeyboardMarkup(
    [
        ["5", "6", "7", "8"],
        ["9", "10", "11"],
        [],
    ],
    resize_keyboard=True,
)
kz_sor_soch = ReplyKeyboardMarkup(
    [
        ["БЖБ", "ТЖБ"],
        [],
    ],
    resize_keyboard=True,
)
ru_sor_soch = ReplyKeyboardMarkup(
    [
        ["СОР", "СОЧ"],
        [],
    ],
    resize_keyboard=True,
)

ru_quarter_kbr = ReplyKeyboardMarkup(
    [
        ["1 четверть", "2 четверть", "3 четверть", "4 четверть"],
        [],
    ],
    resize_keyboard=True,
)
kz_quarter_kbr = ReplyKeyboardMarkup(
    [
        ["1 тоқсан", "2 тоқсан", "3 тоқсан", "4 тоқсан"],
        [],
    ],
    resize_keyboard=True,
)

i_subscribe_kbr = ReplyKeyboardMarkup(
    [
        ["Я подписался"],
        [],
    ],
    resize_keyboard=True,
)


def get_subject_keyboard(subjects: list[list]) -> ReplyKeyboardMarkup:
    logger.info(subjects)
    print(subjects)
    subjects_zip: list[tuple] = list(zip(*[iter(subjects)] * 4))
    logger.info(subjects_zip)

    remaining_subject = []
    k = 0
    for count in range(len(subjects) - len(list(chain.from_iterable(subjects_zip)))):
        k -= 1
        remaining_subject.append(subjects[k])

    logger.info(remaining_subject)
    subjects_zip.append(remaining_subject)
    logger.info(subjects_zip)
    return ReplyKeyboardMarkup(
        subjects_zip,
        resize_keyboard=True,
    )


def show_summation_keyboard(summations):
    summation_admin_menu_buttons = [
        [ibtn(summation.title, f"show_summation_{summation.pk}") for summation in summations]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=summation_admin_menu_buttons,
    )
