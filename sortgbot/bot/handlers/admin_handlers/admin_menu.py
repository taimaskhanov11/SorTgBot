from pathlib import Path

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentTypes, ReplyKeyboardRemove
from loguru import logger

from sortgbot.bot import markups
from sortgbot.bot.filters.main_filter import MainFilter
from sortgbot.bot.states.create_summation import CreateSummation, UploadSummation
from sortgbot.bot.utils.main_helpers import temp
from sortgbot.config.config import config, TEMP_DIR
from sortgbot.db.models import User, SummationStorage
from sortgbot.loader import bot


class CreateMailing(StatesGroup):
    mailing = State()


class DeleteSummation(StatesGroup):
    delete = State()


async def admin_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Выберите функцию", reply_markup=markups.admin_menu)


async def no_admin_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Вы не администратор")


async def add_summation(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await state.update_data(is_admin=True)
    await call.message.answer("Выберите язык", reply_markup=markups.lang_choice)
    await CreateSummation.first()


@logger.catch
async def upload_summation_data(message: types.Message, state: FSMContext):
    # todo 28.03.2022 21:38 taima: text or photo
    data = await state.get_data()
    logger.trace(data)
    try:
        if message.text == "Завершить":
            await state.update_data(file_path="\n".join(map(str, temp.files_paths)))
            temp.files_paths = []
            await message.answer("Введите название кнопки", reply_markup=ReplyKeyboardRemove())
            await UploadSummation.next()

        else:
            if message.content_type in ["photo", "document"]:
                type = "photo" if message.photo else "document"
                # pprint(message.photo)
                text = message.caption
                # logger.info(message.document)
                file = message.photo[-1] if message.photo else message.document
                logger.info(file.as_json())
                file_path = TEMP_DIR / file.file_id
                await file.download(destination_file=file_path)
                temp.files_paths.append(file_path)
                if data.get("file_path"):
                    pass
                    # file_paths = data["file_path"] + f"\n{file_path}"
                    # await state.update_data(file_path=file_paths)
                else:
                    await state.update_data(type=type, text=text, file_path=str(file_path))
                await message.answer("Фото загружено", reply_markup=markups.summation_done_kbr)

            else:
                type = "text"
                text = message.text
                if temp.files_paths:
                    await state.update_data(file_path="\n".join(map(str, temp.files_paths)))
                    temp.files_paths = []

                await state.update_data(type=type, text=text)
                await message.answer("Введите название кнопки", reply_markup=ReplyKeyboardRemove())
                await UploadSummation.next()

    except Exception as e:
        logger.exception(e)
        logger.warning("Ошибка отправьте текст или фото")


@logger.catch
async def upload_summation_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    data = await state.get_data()
    logger.info(f"END DATA {data}")
    await SummationStorage.create(**data)
    await message.answer("Суммативка успешно добавлена")
    # await message.answer(str(await state.get_data()))
    await state.finish()


async def delete_summation(call: types.CallbackQuery):
    summations = await SummationStorage.all()
    answer = "Список суммативок\n"
    for summation in summations:
        answer += f"{summation}\n{'_' * 15}\n"
    answer += "\n\nВведите ID для удаления чтобы отменить введите /admin"
    await DeleteSummation.delete.set()
    await call.message.answer(answer)


async def delete_summation_done(message: types.Message, state: FSMContext):
    try:
        if message.text.isdigit():
            summation = await SummationStorage.get(pk=message.text)
            await summation.delete()
            await message.answer("Суммативка успешно удалена")
            await state.finish()
        else:
            await message.answer("Некорректный ввод, отмены введите /admin")
    except Exception as e:
        await message.answer("Некорректный ввод, отмены введите /admin")
        logger.critical(e)


async def users_list(call: types.CallbackQuery):
    users = "\n".join(map(str, await User.all()))
    await call.message.answer(users or "Пусто")


async def users_count(call: types.CallbackQuery):
    users = "\n".join(map(str, await User.all()))
    await call.message.answer(users or "Пусто")


async def create_mailing(call: types.CallbackQuery):
    await call.message.answer("Отправьте данные для рассылки всем пользователям")
    await CreateMailing.mailing.set()


async def create_mailing_done(message: types.Message, state: FSMContext):
    logger.trace(message)
    logger.trace(temp.send_data)
    if message.text == "Завершить":
        data = await state.get_data()
        _type = data.get("type")
        for file, caption in temp.send_data:
            if _type == "photo":
                for user in await User.all():
                    with open(file, "rb") as f:
                        try:
                            await message.bot.send_photo(user.user_id, f, caption=caption)
                        except Exception as e:
                            logger.critical(e)
                            await message.answer(f"Пользователь {user.user_id} заблокировал бота")

            else:
                for user in await User.all():
                    with open(file, "rb") as f:
                        try:
                            await message.bot.send_document(user.user_id, f, caption=caption)
                        except Exception as e:
                            logger.critical(e)
                            await message.answer(f"Пользователь {user.user_id} заблокировал бота")
        temp.send_data = []
        await message.answer("Рассылка успешно отправлена", reply_markup=ReplyKeyboardRemove())
        await state.finish()

    else:
        if message.content_type in ["photo", "document"]:
            type = "photo" if message.photo else "document"
            # pprint(message.photo)
            text = message.caption
            # logger.info(message.document)
            file = message.photo[-1] if message.photo else message.document
            logger.info(file.as_json())
            file_path: Path = TEMP_DIR / file.file_id
            await file.download(destination_file=file_path)
            temp.send_data.append((file_path, text))
            await state.update_data(type=type, text=text)
            await message.answer("Фото для отправки загружено", reply_markup=markups.summation_done_kbr)

        else:
            type = "text"
            text = message.text
            if temp.send_data:
                # await state.update_data(file_path="\n".join(map(str, temp.send_data)))
                temp.send_data = []
            await state.update_data(type=type, text=text)
            for user in await User.all():
                await bot.send_message(user.user_id, message.text)

            await message.answer("Рассылка успешно отправлена.", reply_markup=ReplyKeyboardRemove())
            await state.finish()


def register_admin_menu_handlers(dp: Dispatcher):
    dp.register_message_handler(admin_menu, MainFilter(), commands="admin", user_id=config.bot.admins, state="*")
    dp.register_message_handler(no_admin_menu, MainFilter(), commands="admin", state="*")

    dp.register_callback_query_handler(add_summation, MainFilter(), text="add_summation")

    dp.register_message_handler(
        upload_summation_data,
        MainFilter(),
        # content_types=[ContentTypes.PHOTO, ContentTypes.TEXT, ContentTypes.DOCUMENT],
        content_types=ContentTypes.ANY,
        state=UploadSummation.data,
    )

    dp.register_message_handler(upload_summation_title, MainFilter(), state=UploadSummation.title)

    dp.register_callback_query_handler(delete_summation, MainFilter(), text="delete_summation")
    dp.register_message_handler(delete_summation_done, MainFilter(), state=DeleteSummation)

    dp.register_callback_query_handler(users_list, MainFilter(), text="users_list")
    dp.register_callback_query_handler(users_count, MainFilter(), text="users_count")

    dp.register_callback_query_handler(create_mailing, MainFilter(), text="create_mailing")
    dp.register_message_handler(create_mailing_done, MainFilter(), content_types=ContentTypes.ANY, state=CreateMailing)
