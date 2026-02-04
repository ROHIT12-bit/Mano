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
    DEF_CAP = os.environ.get("DEF_CAP", "<b>{file_name}</b>\n\nPowered By @Botskingdoms")

    # Messages
    START_MSG = os.environ.get("START_MSG", "HEY!!, 『{mention}』\n\n➤ PURPOSE OF THE BOT:\nTHIS BOT MAKES RENAMING ANIME AND SERIES FILES EASY AND STRESS-FREE.\n\n➤ MAINTAINED BY : @Botskingdoms\n__________________________________")
    FORCE_SUB_MSG = os.environ.get("FORCE_SUB_MSG", "Join our channel to use me!")
    HELP_MSG = os.environ.get("HELP_MSG", "Send any file and choose option.\nUse /autorename to set format.")
    ABOUT_MSG = os.environ.get("ABOUT_MSG", "Fast Renamer Bot By @Botskingdoms.")

    # Sequence Messages
    S_SEQUENCE_MSG = os.environ.get("S_SEQUENCE_MSG", "Sequence started! Send files.")
    E_SEQUENCE_MSG = os.environ.get("E_SEQUENCE_MSG", "Sequence ended! Processing...")
    CANCEL_SEQUENCE_MSG = os.environ.get("CANCEL_SEQUENCE_MSG", "Sequence cancelled!")

    # Credits line
    CREDITS_LINE = os.environ.get("CREDITS_LINE", "Powered By @Botskingdoms")

    # Logs channel
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))

    # Webhook or for keeping it alive
    PORT = os.environ.get("PORT", "8080")
