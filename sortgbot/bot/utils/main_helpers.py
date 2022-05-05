import asyncio

from loguru import logger

from sortgbot.loader import bot


class temp:
    files_paths = []
    send_data: list[tuple] = []


async def part_sending(message, answer):
    logger.trace(f"Message sign count {len(answer)}")

    if len(answer) > 4096:
        for x in range(0, len(answer), 4096):
            y = x + 4096
            await message.bot.send_message(message.chat.id, answer[x: y])
            await asyncio.sleep(0.1)
    else:
        await message.answer(answer)


async def channel_status_check(user_id):
    chats = ["@schoolhack1", "@schoolprokz", "@tjbbjb10", "@MEKTEP_KZ"]
    results = []
    for chat in chats:
        try:
            status = await bot.get_chat_member(
                chat_id=chat,
                user_id=user_id,
            )
            # logger.trace(status)
            if status["status"] != "left":
                results.append(True)
            else:
                results.append(False)
        except Exception as e:
            logger.critical(e)
            results.append(True)
    return all(results)
