from db.mongo import BanList
from mfinder import LOGGER

async def ban_user(user_id):
    try:
        user = await BanList.find_one({"user_id": user_id})
        if not user:
            new_user = BanList(user_id=user_id)
            await new_user.commit()
            return True
        return False
    except Exception as e:
        LOGGER.warning("Error banning user: %s", str(e))
        return False

async def is_banned(user_id):
    try:
        user = await BanList.find_one({"user_id": user_id})
        return user is not None
    except Exception as e:
        LOGGER.warning("Error checking banned user: %s", str(e))
        return False

async def unban_user(user_id):
    try:
        user = await BanList.find_one({"user_id": user_id})
        if user:
            await user.delete()
            return True
        return False
    except Exception as e:
        LOGGER.warning("Error unbanning user: %s", str(e))
        return False
