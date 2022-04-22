import asyncio

from tortoise import Tortoise

from sortgbot.db.db_main import init_tortoise




async def get_data():
    await init_tortoise()
    con = Tortoise.get_connection("default")
    await con.execute_script(
        "drop table summationstorage;"
    )
    print("Успешно удален")

if __name__ == "__main__":
    asyncio.run(get_data())
