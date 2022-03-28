from aiogram.dispatcher.filters.state import StatesGroup, State


class UploadSummation(StatesGroup):
    data = State()
    title = State()


class CreateSummation(StatesGroup):
    choice_lang = State()
    grade = State()
    quarter = State()
    subject = State()
    sorsoch = State()
