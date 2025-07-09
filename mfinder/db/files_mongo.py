from mfinder.utils.helpers import unpack_new_file_id
from mfinder import LOGGER
from db.mongo import Media


async def save_file(media):
    file_id, file_ref = unpack_new_file_id(media.file_id)

    try:
        existing = await Media.find_one({"file_id": file_id})
        if existing:
            LOGGER.warning("%s is already saved", media.file_name)
            return False

        existing_name = await Media.find_one({"file_name": media.file_name})
        if existing_name:
            LOGGER.warning("%s is already saved", media.file_name)
            return False

        file = Media(
            file_name=media.file_name,
            file_id=file_id,
            file_ref=file_ref,
            file_size=media.file_size,
            file_type=media.file_type,
            mime_type=media.mime_type,
            caption=media.caption or None
        )
        await file.commit()
        LOGGER.info("%s is saved", media.file_name)
        return True
    except Exception as e:
        LOGGER.warning("Save error: %s", str(e))
        return False


async def get_filter_results(query, page=1, per_page=10):
    try:
        search = query.split()
        filters = []

        for word in search:
            filters.append({
                "$or": [
                    {"file_name": {"$regex": word, "$options": "i"}},
                    {"caption": {"$regex": word, "$options": "i"}}
                ]
            })

        mongo_query = {"$and": filters} if filters else {}
        skip = (page - 1) * per_page

        cursor = Media.collection.find(mongo_query).sort("file_name", 1)
        total_count = await Media.collection.count_documents(mongo_query)
        results = await cursor.skip(skip).limit(per_page).to_list(length=per_page)

        return results, total_count
    except Exception as e:
        LOGGER.warning("Filter error: %s", str(e))
        return [], 0


async def get_file_details(file_id):
    try:
        return await Media.find({"file_id": file_id}).to_list(length=10)
    except Exception as e:
        LOGGER.warning("Detail error: %s", str(e))
        return []


async def delete_file(media):
    file_id, _ = unpack_new_file_id(media.file_id)
    try:
        doc = await Media.find_one({"file_id": file_id})
        if doc:
            await doc.delete()
            return True
        return "Not Found"
    except Exception as e:
        LOGGER.warning("Delete error: %s", str(e))
        return False


async def count_files():
    try:
        return await Media.collection.count_documents({})
    except Exception as e:
        LOGGER.warning("Count error: %s", str(e))
        return 0
