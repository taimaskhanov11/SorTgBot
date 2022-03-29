from loguru import logger

from sortgbot.loader import bot


class temp:
    files_paths = []


async def channel_status_check(user_id):
    chats = ["@schoolhack1", "@schoolprokz"]
    results = []
    for chat in chats:
        try:
            status = await bot.get_chat_member(
                chat_id=chat,
                user_id=user_id,
            )
            logger.trace(status)
            if status["status"] != "left":
                results.append(True)
            else:
                results.append(False)
        except Exception as e:
            logger.critical(e)
            results.append(True)
    return all(results)
