from db.mongo import AdminSettings, Settings
from mfinder import LOGGER

async def get_search_settings(user_id):
    try:
        return await Settings.find_one({"user_id": user_id})
    except Exception as e:
        LOGGER.warning("Error getting search settings: %s", str(e))
        return None

async def change_search_settings(user_id, precise_mode=None, button_mode=None, link_mode=None, list_mode=None):
    try:
        settings = await Settings.find_one({"user_id": user_id})
        if settings:
            if precise_mode is not None:
                settings.precise_mode = precise_mode
            if button_mode is not None:
                settings.button_mode = button_mode
            if link_mode is not None:
                settings.link_mode = link_mode
            if list_mode is not None:
                settings.list_mode = list_mode
        else:
            settings = Settings(
                user_id=user_id,
                precise_mode=precise_mode,
                button_mode=button_mode,
                link_mode=link_mode,
                list_mode=list_mode
            )
        await settings.commit()
        return True
    except Exception as e:
        LOGGER.warning("Error changing search settings: %s", str(e))
        return False

async def get_admin_settings():
    try:
        admin_setting = await AdminSettings.find_one({"setting_name": "default"})
        if not admin_setting:
            admin_setting = AdminSettings(setting_name="default")
            await admin_setting.commit()
        return admin_setting
    except Exception as e:
        LOGGER.warning("Error getting admin settings: %s", str(e))
        return None

async def set_repair_mode(repair_mode):
    try:
        admin_setting = await get_admin_settings()
        admin_setting.repair_mode = repair_mode
        await admin_setting.commit()
    except Exception as e:
        LOGGER.warning("Error setting repair mode: %s", str(e))

async def set_auto_delete(dur):
    try:
        admin_setting = await get_admin_settings()
        admin_setting.auto_delete = dur
        await admin_setting.commit()
    except Exception as e:
        LOGGER.warning("Error setting auto delete: %s", str(e))

async def set_custom_caption(caption):
    try:
        admin_setting = await get_admin_settings()
        admin_setting.custom_caption = caption
        await admin_setting.commit()
    except Exception as e:
        LOGGER.warning("Error setting custom caption: %s", str(e))

async def set_force_sub(channel):
    try:
        admin_setting = await get_admin_settings()
        admin_setting.fsub_channel = channel
        await admin_setting.commit()
    except Exception as e:
        LOGGER.warning("Error setting Force Sub channel: %s", str(e))

async def set_channel_link(link):
    try:
        admin_setting = await get_admin_settings()
        admin_setting.channel_link = link
        await admin_setting.commit()
    except Exception as e:
        LOGGER.warning("Error setting channel link: %s", str(e))

async def get_channel():
    try:
        admin_setting = await get_admin_settings()
        return admin_setting.fsub_channel if admin_setting else False
    except Exception as e:
        LOGGER.warning("Error getting Force Sub channel: %s", str(e))
        return False

async def get_link():
    try:
        admin_setting = await get_admin_settings()
        return admin_setting.channel_link if admin_setting else False
    except Exception as e:
        LOGGER.warning("Error getting channel link: %s", str(e))
        return False

async def set_username(username):
    try:
        admin_setting = await get_admin_settings()
        admin_setting.caption_uname = username
        await admin_setting.commit()
    except Exception as e:
        LOGGER.warning("Error setting username: %s", str(e))
    
        
