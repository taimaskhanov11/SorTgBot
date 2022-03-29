import asyncio

from loguru import logger
from tortoise import Tortoise

from sortgbot.config.config import config
from sortgbot.db.models import User


async def init_tortoise():
    db = config.db
    logger.debug(f"Инициализация BD {db.host}")
    data = {
        "db_url": f"postgres://{db.username}:{db.password}@{db.host}:{db.port}/{db.db_name}",
        "modules": {"models": ["sortgbot.db.models"]},
    }
    try:
        await Tortoise.init(**data)
    except Exception as e:
        logger.critical(e)
        await Tortoise.init(_create_db=True, **data, )
    await Tortoise.generate_schemas()

async def get_data():
    await init_tortoise()
    print((await User.first()))

if __name__ == '__main__':
    asyncio.run(get_data())