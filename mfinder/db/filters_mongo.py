from db.mongo import Filters
from mfinder import LOGGER


async def add_filter(filters, message):
    try:
        existing = await Filters.find_one({"filters": {"$regex": f"^{filters}$", "$options": "i"}})
        if not existing:
            fltr = Filters(filters=filters, message=message)
            await fltr.commit()
            return True
    except Exception as e:
        LOGGER.warning("Add filter error: %s", str(e))
        return False


async def is_filter(filters):
    try:
        return await Filters.find_one({"filters": {"$regex": f"^{filters}$", "$options": "i"}})
    except Exception as e:
        LOGGER.warning("Check filter error: %s", str(e))
        return False


async def rem_filter(filters):
    try:
        fltr = await Filters.find_one({"filters": {"$regex": f"^{filters}$", "$options": "i"}})
        if fltr:
            await fltr.delete()
            return True
        return False
    except Exception as e:
        LOGGER.warning("Delete filter error: %s", str(e))
        return False


async def list_filters():
    try:
        all_filters = await Filters.find({}, projection={"filters": 1}).to_list(length=1000)
        return [f.filters for f in all_filters]
    except Exception as e:
        LOGGER.warning("List filters error: %s", str(e))
        return False
