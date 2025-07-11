import asyncio
from pyrogram.errors import FloodWait
from pyrogram import enums
from mfinder import LOGGER
from mfinder.db.broadcast_mongo import query_msg, del_user


async def users_info(bot):
    users = 0
    blocked = 0
    identity = await query_msg()

    for user in identity:
        user_id = user.user_id  # user is a Document object

        name = False
        try:
            name = await bot.send_chat_action(user_id, enums.ChatAction.TYPING)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            pass

        if name:
            users += 1
        else:
            await del_user(user_id)
            LOGGER.info("Deleted user id %s from broadcast list", user_id)
            blocked += 1

    return users, blocked
