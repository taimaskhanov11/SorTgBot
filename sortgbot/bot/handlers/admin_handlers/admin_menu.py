from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from sortgbot.bot import markups
from sortgbot.bot.filters.main_filter import MainFilter
from sortgbot.bot.states.create_summation import CreateSummation, UploadSummation
from sortgbot.config.config import config
from sortgbot.db.models import User
from sortgbot.loader import bot


class CreateMailing(StatesGroup):
    mailing = State()


async def admin_menu(message: types.Message):
    await message.answer("Выберите функцию", reply_markup=markups.admin_menu)


async def add_summation(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await state.update_data(is_admin=True)
    await call.message.answer("Выберите язык", reply_markup=markups.lang_choice)
    await CreateSummation.first()


@logger.catch
async def upload_summation_data(message: types.Message, state: FSMContext):
    # todo 28.03.2022 21:38 taima: text or photo
    await state.update_data(some_data=message.text)
    await message.answer("Введите название кнопки")
    await UploadSummation.next()


async def upload_summation_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    logger.info(data)
    await state.update_data(title=message.text)
    await message.answer(str(await state.get_data()))
    await state.finish()


async def delete_summation(call: types.CallbackQuery):
    pass


async def users_list(call: types.CallbackQuery):
    users = "\n".join(map(str, await User.all()))
    await call.message.answer(users or "Пусто")


async def create_mailing(call: types.CallbackQuery):
    await call.message.answer("Отправьте данные для рассылки всем пользователям")
    await CreateMailing.mailing.set()


async def create_mailing_done(message: types.Message, state: FSMContext):
    await state.finish()
    for user in await User.all():
        await bot.send_message(user.user_id, message.text)
    await message.answer("Рассылка успешно отправлена")


def register_admin_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_menu, MainFilter(), commands="admin", user_id=config.bot.admins, state="*")

    dp.register_callback_query_handler(add_summation, MainFilter(), text="add_summation")
    dp.register_message_handler(upload_summation_data, MainFilter(), state=UploadSummation.data)
    dp.register_message_handler(upload_summation_title, MainFilter(), state=UploadSummation.title)

    dp.register_callback_query_handler(delete_summation, MainFilter(), text="delete_summation")
    dp.register_callback_query_handler(users_list, MainFilter(), text="users_list")

    dp.register_callback_query_handler(create_mailing, MainFilter(), text="create_mailing")
    dp.register_message_handler(create_mailing_done, MainFilter(), state=CreateMailing)
