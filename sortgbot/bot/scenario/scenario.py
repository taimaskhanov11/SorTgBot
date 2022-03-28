from typing import Optional

from aiogram.types import ReplyKeyboardMarkup
from pydantic import BaseModel

from sortgbot.bot import markups
from sortgbot.bot.markups.main import get_subject_keyboard


class Combination(BaseModel):
    title: str
    keyboard: Optional[ReplyKeyboardMarkup]

    class Config:
        arbitrary_types_allowed = True


class Grade(BaseModel):
    pass


class Scenario(BaseModel):
    grade: Combination
    subject_: Combination
    quarter: Combination
    sorsoch: Combination
    subjects_list: list[list]

    @property
    def subject(self):
        if self.grade in (5, 6):
            subjects = self.subjects_list[0]
        elif self.grade in (7, 8):
            subjects = self.subjects_list[1]
        # 9, 10, 11
        else:
            subjects = self.subjects_list[2]

        return Combination(title=self.subject_.title, keyboard=get_subject_keyboard(subjects))


subjects_ru = [
    ["Математика", "Русский язык", "Русская литература", "Казахский язык", "История Казахстана",
     "Всемирная история", "Информатика", "Естествознание", "Английский язык"],

    ["Алгебра", "Геометрия", "Русский язык", "Русская литература", "Физика", "Химия",
     "Казахский язык", "История Казахстана", "Всемирная история", "Информатика", "География",
     "Биология", "Английский язык"],

    ["Алгебра", "Геометрия", "Русский язык", "Русская литература", "Физика", "Химия",
     "Казахский язык", "История Казахстана", "Всемирная история", "Основы права", "Информатика",
     "География", "Биология", "Английский язык"]
]
subjects_kz = [
    ["Математика", "Орыс тілі", "Қазақ әдебиеті", "Қазақ тілі", "Қазақстан тарихы",
     "Дүниежүзілік тарихы", "Информатика", "Жаратылыстану", "Ағылшын тілі"],

    ["Алгебра", "Геометрия", "Орыс тілі", "Қазақ әдебиеті", "Физика", "Химия", "Қазақ тілі",
     "Қазақстан тарихы", "Дүниежүзілік тарихы", "Информатика", "География", "Биология",
     "Ағылшын тілі"],

    ["Алгебра", "Геометрия", "Орыс тілі", "Қазақ әдебиеті", "Физика", "Химия", "Қазақ тілі",
     "Қазақстан тарихы", "Дүниежүзілік тарихы", "Құқық негіздер"]
]

scenarios = {
    "russian": Scenario(
        grade=Combination(title="🛑Какой класс?", keyboard=markups.numbers_button),
        subject_=Combination(title="🛑Какой предмет?"),
        subjects_list=subjects_ru,
        quarter=Combination(title="🛑Какая четверть?", keyboard=markups.ru_quarter_kbr),
        sorsoch=Combination(title="Выберите СОР или СОЧ", keyboard=markups.ru_sor_soch),
    ),
    "kazakh": Scenario(
        grade=Combination(title="🛑Қай сынып?", keyboard=markups.numbers_button),
        subject_=Combination(title="🛑Қай пән?"),
        subjects_list=subjects_kz,
        quarter=Combination(title="🛑Қай тоқсан?", keyboard=markups.kz_quarter_kbr),
        sorsoch=Combination(title="БЖБ немесе ТЖБ таңдаңыз", keyboard=markups.kz_sor_soch),
    ),
}
