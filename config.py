import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    DB_URL = os.environ.get("DB_URL", "")
    DB_NAME = os.environ.get("DB_NAME", "Botskingdoms_Renamer")

    # Bot owner/admins
    admins = [int(x) for x in os.environ.get("ADMIN", "").split() if x]
    Botskingdoms = admins

    # Channel for force subscribe
    FORCE_SUB = os.environ.get("FORCE_SUB", "")
    FORCE_SUB_PIC = os.environ.get("FORCE_SUB_PIC", "https://telegra.ph/file/a8a183d2cc03a6a9b6c00.jpg")

    # Start pic
    START_PIC = os.environ.get("START_PIC", "https://telegra.ph/file/a8a183d2cc03a6a9b6c00.jpg")

    # Workers for Pyrogram client
    WORKERS = int(os.environ.get("WORKERS", "20"))

    # Default caption
    DEF_CAP = os.environ.get("DEF_CAP", "<b>{file_name}</b>\n\n[ᴘᴏᴡᴇʀᴇᴅ ʙʏ ʙᴏᴛsᴋɪɴɢᴅᴏᴍs](ʜᴛᴛᴘs://ᴛ.ᴍᴇ/ʙᴏᴛsᴋɪɴɢᴅᴏᴍs)")

    # Messages
    START_MSG = os.environ.get("START_MSG", "ʜᴇʟʟᴏ {mention}!\n\nɪ ᴀᴍ ғᴀsᴛ ʀᴇɴᴀᴍᴇʀ ʙᴏᴛ.\n\nsᴇɴᴅ ғɪʟᴇ ᴛᴏ sᴛᴀʀᴛ.\n\n[ᴘᴏᴡᴇʀᴇᴅ ʙʏ ʙᴏᴛsᴋɪɴɢᴅᴏᴍs](ʜᴛᴛᴘs://ᴛ.ᴍᴇ/ʙᴏᴛsᴋɪɴɢᴅᴏᴍs)")
    FORCE_SUB_MSG = os.environ.get("FORCE_SUB_MSG", "ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴜsᴇ ᴍᴇ!")
    HELP_MSG = os.environ.get("HELP_MSG", "sᴇɴᴅ ғɪʟᴇ ᴀɴᴅ ᴄʜᴏᴏsᴇ ᴏᴘᴛɪᴏɴ.\nᴜsᴇ /autorename ᴛᴏ sᴇᴛ ғᴏʀᴍᴀᴛ.")
    ABOUT_MSG = os.environ.get("ABOUT_MSG", "ғᴀsᴛ ʀᴇɴᴀᴍᴇʀ ʙᴏᴛ ʙʏ ʙᴏᴛsᴋɪɴɢᴅᴏᴍs.")

    # Sequence Messages
    S_SEQUENCE_MSG = os.environ.get("S_SEQUENCE_MSG", "sᴇǫᴜᴇɴᴄᴇ sᴛᴀʀᴛᴇᴅ! sᴇɴᴅ ғɪʟᴇs.")
    E_SEQUENCE_MSG = os.environ.get("E_SEQUENCE_MSG", "sᴇǫᴜᴇɴᴄᴇ ᴇɴᴅᴇᴅ! ᴘʀᴏᴄᴇssɪɴɢ...")
    CANCEL_SEQUENCE_MSG = os.environ.get("CANCEL_SEQUENCE_MSG", "sᴇǫᴜᴇɴᴄᴇ ᴄᴀɴᴄᴇʟʟᴇᴅ!")

    # Credits line
    CREDITS_LINE = os.environ.get("CREDITS_LINE", "[ᴘᴏᴡᴇʀᴇᴅ ʙʏ ʙᴏᴛsᴋɪɴɢᴅᴏᴍs](ʜᴛᴛᴘs://ᴛ.ᴍᴇ/ʙᴏᴛsᴋɪɴɢᴅᴏᴍs)")

    # Logs channel
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))

    # Webhook or for keeping it alive
    PORT = os.environ.get("PORT", "8080")
