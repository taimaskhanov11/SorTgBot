from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loguru import logger

from sortgbot.bot import markups
from sortgbot.bot.filters.main_filter import MainFilter
from sortgbot.bot.scenario.scenario import scenarios, Scenario
from sortgbot.bot.states.create_summation import CreateSummation, UploadSummation
from sortgbot.bot.utils.main_helpers import channel_status_check
from sortgbot.db.models import User, SummationStorage


class ChoiceLang(StatesGroup):
    choice = State()


async def main_start(message: types.Message, state: FSMContext, user: User):
    # user.language = None
    # await user.save(update_fields=["language"])
    await state.finish()

    if not await channel_status_check(message.from_user.id):
        await message.answer("🇷🇺Для того, чтобы пользоваться ботом, нужно подписаться на каналы\n"
                             "🇰🇿Ботты пайдалану үшін арналарға жазылу керек\n"
                             "Каналы: https://t.me/schoolhack1 https://t.me/schoolprokz")
        return

    await message.answer("🇷🇺На каком языке продолжить?\n🇰🇿Қай тілде жалғастыру керек?",
                         reply_markup=markups.lang_choice)
    await CreateSummation.first()


async def choice_lang(message: types.Message, state: FSMContext, user: User):
    if message.text.startswith("🇰🇿"):
        user.language = "kazakh"
    elif message.text.startswith("🇷🇺"):
        user.language = "russian"
    await user.save()
    # await message.answer("Язык успешно выбрать, чтобы продолжить ведите /start", reply_markup=markups.start_button)
    # await state.finish()
    scenario = scenarios.get(user.language)
    await message.answer(scenario.grade.title, reply_markup=scenario.grade.keyboard)
    await CreateSummation.next()


async def grade(message: types.Message, state: FSMContext, scenario: Scenario):
    await state.update_data(grade=message.text)
    await message.answer(scenario.quarter.title, reply_markup=scenario.quarter.keyboard)
    await CreateSummation.next()


async def quarter(message: types.Message, state: FSMContext, scenario: Scenario):
    data = await state.get_data()
    await state.update_data(quarter=message.text)
    await message.answer(scenario.subject.title, reply_markup=scenario.get_subject_keyboard(int(data["grade"])))
    await CreateSummation.next()


async def subject(message: types.Message, state: FSMContext, scenario: Scenario):
    await state.update_data(subject=message.text)
    await message.answer(scenario.sorsoch.title, reply_markup=scenario.sorsoch.keyboard)
    await CreateSummation.next()


async def sorsoch(message: types.Message, state: FSMContext, scenario: Scenario):
    await state.update_data(sorsoch=message.text)
    data = await state.get_data()
    if data.get("is_admin"):
        await message.answer("Загрузка суммативки\n"
                             "Ведите текст или отправьте изображение")
        await UploadSummation.first()
    else:
        summations = await SummationStorage.filter(
            **data
        )
        logger.trace(data)
        logger.trace(summations)
        if summations:
            await message.answer("Выберите кнопку", reply_markup=markups.show_summation_keyboard(summations))
        else:
            await message.answer("Пусто")
        await state.finish()


async def show_summation(call: types.CallbackQuery):
    summation_pk = call.data[15:]
    summation = await SummationStorage.get(pk=summation_pk)
    # await call.message.delete()
    if summation.type == "text":
        await call.message.answer(f"[{summation.title}]\n{summation.text}")
    else:
        with open(summation.file_path, "rb") as f:
            await call.bot.send_photo(call.from_user.id, f, caption=summation.text)


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(main_start, MainFilter(), commands="start", state="*")

    dp.register_message_handler(choice_lang, MainFilter(), state=CreateSummation.choice_lang)
    dp.register_message_handler(grade, MainFilter(), state=CreateSummation.grade)
    dp.register_message_handler(subject, MainFilter(), state=CreateSummation.subject)
    dp.register_message_handler(quarter, MainFilter(), state=CreateSummation.quarter)
    dp.register_message_handler(sorsoch, MainFilter(), state=CreateSummation.sorsoch)

    dp.register_callback_query_handler(show_summation, text_startswith="show_summation_")
