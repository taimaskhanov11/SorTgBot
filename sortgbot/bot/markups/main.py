from itertools import chain

from aiogram.types import ReplyKeyboardMarkup

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
        ["1 тоқсан", "2 тоқсан", "3 тоқсан" "4 тоқсан"],
        [],
    ],
    resize_keyboard=True,
)


def get_subject_keyboard(subjects: list[list]) -> ReplyKeyboardMarkup:
    subjects_zip: list[tuple] = list(zip(*[iter(subjects)] * 4))

    remaining_subject = []
    for count in range(len(subjects) - len(list(chain.from_iterable(subjects_zip)))):
        remaining_subject.append(subjects.pop())
    subjects_zip.append(remaining_subject)
    return ReplyKeyboardMarkup(
        subjects_zip,
        resize_keyboard=True,
    )
