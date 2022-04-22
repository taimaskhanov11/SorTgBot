from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def ibtn(text, data):
    return InlineKeyboardButton(text=text, callback_data=data)


_admin_menu_buttons = [
    [ibtn("📋 Добавить суммативку", "add_summation")],
    [ibtn("🗑 Удалить суммативку", "delete_summation")],
    [ibtn("👥 Список пользователей", "users_list")],
    [ibtn("📈 Количество пользователей", "users_count")],
    [ibtn("📑 Сделать рассылку", "create_mailing"),],
]
admin_menu = InlineKeyboardMarkup(
    inline_keyboard=_admin_menu_buttons,
)
summation_done_kbr = ReplyKeyboardMarkup(
    [
        ["Завершить"],
        [],
    ],
    resize_keyboard=True,
)
