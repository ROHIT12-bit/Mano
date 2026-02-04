import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", "0"))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    DB_URL = os.environ.get("DB_URL", "")
    DB_NAME = os.environ.get("DB_NAME", "renamer_bot")

    # Bot owner/admins
    ADMIN = [int(x) for x in os.environ.get("ADMIN", "").split() if x]

    # Channel for force subscribe
    FORCE_SUB = os.environ.get("FORCE_SUB", "")
    FORCE_SUB_PIC = os.environ.get("FORCE_SUB_PIC", "https://telegra.ph/file/a8a183d2cc03a6a9b6c00.jpg")

    # Start pic
    START_PIC = os.environ.get("START_PIC", "https://telegra.ph/file/a8a183d2cc03a6a9b6c00.jpg")

    # Workers for Pyrogram client
    WORKERS = int(os.environ.get("WORKERS", "20"))

    # Default caption
    DEF_CAP = os.environ.get("DEF_CAP", "<b>{file_name}</b>\n\nBy @Botskingdoms")

    # Messages
    START_MSG = os.environ.get("START_MSG", "Hello {mention}!\n\nI am a fast Telegram Auto Renamer Bot.\n\nSend me any file to rename it.\n\n<b>By @Botskingdoms</b>")
    FORCE_SUB_MSG = os.environ.get("FORCE_SUB_MSG", "<b>Please Join My Update Channel to use this Bot!</b>")
    HELP_MSG = os.environ.get("HELP_MSG", "<b>Help Menu</b>\n\n- Send me any file.\n- Choose rename option.\n- Set your custom format with /autorename.\n\n<b>By @Botskingdoms</b>")
    ABOUT_MSG = os.environ.get("ABOUT_MSG", "<b>About This Bot</b>\n\nA powerful Telegram bot to rename files and change metadata.\n\nDeveloper: @Botskingdoms")

    # Credits line
    CREDITS_LINE = os.environ.get("CREDITS_LINE", "By @Botskingdoms")

    # Logs channel
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))

    # Webhook or for keeping it alive
    PORT = os.environ.get("PORT", "8080")
