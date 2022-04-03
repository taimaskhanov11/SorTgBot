from tortoise import models, fields


class User(models.Model):
    user_id = fields.BigIntField()
    username = fields.CharField(max_length=30, null=True)
    language = fields.CharField(max_length=15, null=True)
    is_admin = fields.BooleanField(default=False)

    def __str__(self):
        return f"@{self.username}:{self.user_id}"


# class SummationSearch(BaseModel):
#     pass
#
#
# class AbstractData(models.Model):
#     title = fields.CharField(max_length=255)
#
#     class Meta:
#         abstract = True


class SummationStorage(models.Model):
    grade = fields.CharField(max_length=255)
    subject = fields.CharField(max_length=255)
    quarter = fields.CharField(max_length=255)
    sorsoch = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255)

    # photo or text
    type = fields.CharField(max_length=255)
    text = fields.TextField(null=True)
    file_path = fields.TextField(null=True)

    def __str__(self):
        return (
            f"Класс:{self.grade}\n"
            f"Предмет:{self.subject}\n"
            f"Четверть:{self.quarter}\n"
            f"Сор или соч:{self.sorsoch}\n"
            f"Название кнопки:{self.title}\n"
            f"Тип:{self.type}\n"
            f"Текст:{self.text}\n"
            # f"Путь файла:{self.file_path}\n"
            f"ID:{self.pk}"
        )
