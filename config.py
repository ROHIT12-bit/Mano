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
    DEF_CAP = os.environ.get("DEF_CAP", "<blockquote><b>{file_name}</b>\n\nBy @Botskingdoms</blockquote>")

    # Messages
    START_MSG = os.environ.get("START_MSG", "<blockquote>Hello {mention}!\n\nI am a fast Telegram Auto Renamer Bot.\n\nSend me any file to rename it.\n\n<b>By @Botskingdoms</b></blockquote>")
    FORCE_SUB_MSG = os.environ.get("FORCE_SUB_MSG", "<blockquote><b>Please Join My Update Channel to use this Bot!</b></blockquote>")
    HELP_MSG = os.environ.get("HELP_MSG", """<blockquote><b>Help Menu</b>

- Send me any file.
- Choose rename option.
- Set your custom format with /autorename.

<b>Available Fillings:</b>
• {filename} - File name
• {filesize} - File size
• {duration} - Duration
• {width} - Width
• {height} - Height
• {resolution} - Resolution
• {ext} - Extension
• {mime_type} - Mime type
• {title} - Audio title
• {artist} - Audio artist
• {caption} - Original caption
• {html_caption} - Original caption (HTML)
• {wish} - Wish (Morning/Evening)
• {year}, {quality}, {language}, {season}, {episode} - Extracted from name

<b>By @Botskingdoms</b></blockquote>""")
    ABOUT_MSG = os.environ.get("ABOUT_MSG", "<blockquote><b>About This Bot</b>\n\nA powerful Telegram bot to rename files and change metadata.\n\nDeveloper: @Botskingdoms</blockquote>")

    # Sequence Messages
    S_SEQUENCE_MSG = os.environ.get("S_SEQUENCE_MSG", "<blockquote><b>File Sequencing Started!</b>\n\nSend me documents, videos, or audio files one by one. Use /esequence when done.</blockquote>")
    E_SEQUENCE_MSG = os.environ.get("E_SEQUENCE_MSG", "<blockquote><b>File Sequencing Ended!</b>\n\nProcessing your files in order...</blockquote>")
    CANCEL_SEQUENCE_MSG = os.environ.get("CANCEL_SEQUENCE_MSG", "<blockquote><b>File Sequencing Cancelled!</b></blockquote>")

    # Credits line
    CREDITS_LINE = os.environ.get("CREDITS_LINE", "By @Botskingdoms")

    # Logs channel
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))

    # Webhook or for keeping it alive
    PORT = os.environ.get("PORT", "8080")
