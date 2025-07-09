from mfinder import LOGGER
from db.mongo import Broadcast


async def add_user(user_id, user_name):
    try:
        existing = await Broadcast.find_one({"user_id": user_id})
        if not existing:
            user = Broadcast(user_id=user_id, user_name=user_name)
            await user.commit()
    except Exception as e:
        LOGGER.warning("Add user error: %s", str(e))


async def is_user(user_id):
    try:
        user = await Broadcast.find_one({"user_id": user_id})
        if user:
            return user.user_id
        return False
    except Exception as e:
        LOGGER.warning("Check user error: %s", str(e))
        return False


async def query_msg():
    try:
        users = await Broadcast.find({}, projection={"user_id": 1}).to_list(length=100000)
        return [(user.user_id,) for user in users]
    except Exception as e:
        LOGGER.warning("Query users error: %s", str(e))
        return []


async def del_user(user_id):
    try:
        user = await Broadcast.find_one({"user_id": user_id})
        if user:
            await user.delete()
    except Exception as e:
        LOGGER.warning("Delete user error: %s", str(e))
