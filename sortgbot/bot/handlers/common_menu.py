from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from sortgbot.bot import markups
from sortgbot.bot.filters.main_filter import MainFilter
from sortgbot.bot.scenario.scenario import scenarios, Scenario
from sortgbot.bot.states.create_summation import CreateSummation, UploadSummation
from sortgbot.bot.utils.main_helpers import channel_status_check
from sortgbot.db.models import User


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
    await state.update_data(quarter=message.text)
    await message.answer(scenario.subject.title, reply_markup=scenario.subject.keyboard)
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
                             "Ведите текст или отправьте сообщение")
        await UploadSummation.first()
    else:
        await message.answer(str(data))
        await state.finish()


def register_common_handlers(dp: Dispatcher):
    dp.register_message_handler(main_start, MainFilter(), commands="start", state="*")

    dp.register_message_handler(choice_lang, MainFilter(), state=CreateSummation.choice_lang)
    dp.register_message_handler(grade, MainFilter(), state=CreateSummation.grade)
    dp.register_message_handler(subject, MainFilter(), state=CreateSummation.subject)
    dp.register_message_handler(quarter, MainFilter(), state=CreateSummation.quarter)
    dp.register_message_handler(sorsoch, MainFilter(), state=CreateSummation.sorsoch)
