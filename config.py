import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.environ.get("API_ID", "20366634"))
    API_HASH = os.environ.get("API_HASH", "72095ec36984aa9ceb0dbaa9cec31559")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "8306570313:AAFU7TYT_4KOl4-XLy9OX_92gewFSeJeeeQ")
    DB_URL = os.environ.get("DB_URL", "mongodb+srv://rohitreddyathuru:R6Co7MOjTYQOAqcq@cluster0.xrwjpl9.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    DB_NAME = os.environ.get("DB_NAME", "Botskingdoms_Renamer")

    # Bot owner/admins
    admins = [int(x) for x in os.environ.get("ADMIN", "8476571786").split() if x]
    Botskingdoms = admins

    # Channel for force subscribe
    FORCE_SUB = os.environ.get("FORCE_SUB", "-1003790363380")
    FORCE_SUB_PIC = os.environ.get("FORCE_SUB_PIC", "https://i.rj1.dev/aMNXA.jpg")

    # Start pic
    START_PIC = os.environ.get("START_PIC", "https://i.rj1.dev/aMNXA.jpg")

    # Workers for Pyrogram client
    WORKERS = int(os.environ.get("WORKERS", "20"))

    # Default caption
    DEF_CAP = os.environ.get("DEF_CAP", "<b>{file_name}</b>\n\nBy @Botskingdoms")

    # Messages
    START_MSG = os.environ.get("START_MSG", "Hello {mention}!\n\nI am a fast Telegram Auto Renamer Bot.\n\nSend me any file to rename it.\n\n<b>By @Botskingdoms</b>")
    FORCE_SUB_MSG = os.environ.get("FORCE_SUB_MSG", "<b>Please Join My Update Channel to use this Bot!</b>")
    HELP_MSG = os.environ.get("HELP_MSG", "<b>Help Menu</b>\n\n- Send me any file.\n- Choose rename option.\n- Set your custom format with /autorename.\n\n<b>By @Botskingdoms</b>")
    ABOUT_MSG = os.environ.get("ABOUT_MSG", "<b>About This Bot</b>\n\nA powerful Telegram bot to rename files and change metadata.\n\nDeveloper: @Botskingdoms")

    # Sequence Messages
    S_SEQUENCE_MSG = os.environ.get("S_SEQUENCE_MSG", "<b>File Sequencing Started!</b>\n\nSend me documents, videos, or audio files one by one. Use /esequence when done.")
    E_SEQUENCE_MSG = os.environ.get("E_SEQUENCE_MSG", "<b>File Sequencing Ended!</b>\n\nProcessing your files in order...")
    CANCEL_SEQUENCE_MSG = os.environ.get("CANCEL_SEQUENCE_MSG", "<b>File Sequencing Cancelled!</b>")

    # Credits line
    CREDITS_LINE = os.environ.get("CREDITS_LINE", "By @Botskingdoms")

    # Logs channel
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1003790363380"))

    # Webhook or for keeping it alive
    PORT = os.environ.get("PORT", "8080")
