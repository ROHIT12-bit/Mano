import os
import re
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
    FORCE_SUB = os.environ.get("FORCE_SUB", "RohitXmax")
    FORCE_SUB_PIC = os.environ.get("FORCE_SUB_PIC", "https://i.rj1.dev/aMNXA.jpg")

    # Start pic
    START_PIC = os.environ.get("START_PIC", "https://i.rj1.dev/aMNXA.jpg")

    # Workers for Pyrogram client
    WORKERS = int(os.environ.get("WORKERS", "20"))



    # Default caption
    DEF_CAP = os.environ.get("DEF_CAP", "<b>{file_name}</b>\n\n<blockquote>[Powered by Botskingdoms](https://t.me/BOTSKINGDOMS)</blockquote>")

    # Messages
    START_MSG = os.environ.get("START_MSG", "›› ʜᴇʏ!!,  『{mention}』\n\n➤ ᴘᴜʀᴘᴏꜱᴇ ᴏꜰ ᴛʜᴇ ʙᴏᴛ:\n\nᴛʜɪꜱ ʙᴏᴛ ᴍᴀᴋᴇꜱ ʀᴇɴᴀᴍɪɴɢ ᴀɴɪᴍᴇ ᴀɴᴅ ꜱᴇʀɪᴇꜱ ꜰɪʟᴇꜱ ᴇᴀꜱʏ ᴀɴᴅ ꜱᴛʀᴇꜱꜱ-ꜰʀᴇᴇ.\n\n‣ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ : <blockquote>[BᴏᴛsKɪɴɢᴅᴏᴍs](https://t.me/BOTSKINGDOMS)</blockquote>\n__________________________________")
    FORCE_SUB_MSG = os.environ.get("FORCE_SUB_MSG", "> ›› ʜᴇʏ 『{mention}』\n\n‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴜʙsᴄʀɪʙᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ʏᴇᴛ, sᴜʙsᴄʀɪʙᴇ ɴᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜᴇ ʙᴏᴛ")
    HELP_MSG = os.environ.get("HELP_MSG", "Send any file and choose option.\nUse /autorename to set format.")
    ABOUT_MSG = os.environ.get("ABOUT_MSG", """<b><blockquote expandable>❍ ᴍʏ ɴᴀᴍᴇ : <a href="https://t.me/AkiraRenameBot">ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ</a>
❍ ᴅᴇᴠᴇʟᴏᴩᴇʀ : <a href="https://t.me/Rioshin">ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>
❍ ʟᴀɴɢᴜᴀɢᴇ : <a href="https://www.python.org/">ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>
❍ ᴅᴀᴛᴀʙᴀꜱᴇ : <a href="https://www.mongodb.com/">ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>
❍ ʜᴏꜱᴛᴇᴅ ᴏɴ : <a href="https://t.me/botskingdoms">ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>
❍ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ : <a href="https://t.me/botskingdoms">ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>

➻ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ғᴏʀ ɢᴇᴛᴛɪɴɢ ʙᴀsɪᴄ ʜᴇʟᴩ ᴀɴᴅ ɪɴғᴏ ᴀʙᴏᴜᴛ ᴍᴇ.</blockquote></b>

 > ➻ ꜰᴇᴀᴛᴜʀᴇꜱ :
 > ➲ ɪ ᴄᴀɴ ᴀᴜᴛᴏ ʀᴇɴᴀᴍᴇ ʏᴏᴜʀ ʙᴀꜱᴇᴅ ᴏɴ ᴄᴜꜱᴛᴏᴍ ꜱᴇᴛᴛɪɴɢꜱ.
 > ➲ ɪ ꜱᴜᴘᴘᴏʀᴛ ꜱᴇᴀꜱᴏɴ, ᴇᴘɪꜱᴏᴅᴇ, ǫᴜᴀʟɪᴛʏ, ᴀɴᴅ ᴏᴛʜᴇʀ ᴍᴇᴛᴀᴅᴀᴛᴀ ᴀᴜᴛᴏ-ᴇxᴛʀᴀᴄᴛɪᴏɴ.
 > ➲ ɪ ᴄᴀɴ ᴀᴅᴅ ᴄᴜꜱᴛᴏᴍ ᴘᴀꜱꜱᴡᴏʀᴅꜱ and ʙᴀɴɴᴇʀꜱ ᴏɴ ғɪʀsᴛ ᴏʀ ʟᴀsᴛ ᴘᴀɢᴇ.
 > ➲ ꜰᴏʀ ᴍᴏʀᴇ ꜰᴇᴀᴛᴜʀᴇꜱ, ᴄʜᴇᴄᴋ ᴄᴏᴍᴍᴀɴᴅs.

➲ ꜰᴏʀ ᴍᴏʀᴇ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴛʜɪꜱ ʙᴏᴛ ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ᴄʀᴇᴀᴛᴏʀ""")

    # Sequence Messages
    S_SEQUENCE_MSG = os.environ.get("S_SEQUENCE_MSG", "Sequence started! Send files.")
    E_SEQUENCE_MSG = os.environ.get("E_SEQUENCE_MSG", "Sequence ended! Processing...")
    CANCEL_SEQUENCE_MSG = os.environ.get("CANCEL_SEQUENCE_MSG", "Sequence cancelled!")

    # Credits line
    CREDITS_LINE = os.environ.get("CREDITS_LINE", "<a href="https://t.me/BOTSKINGDOMS">[ᴘᴏᴡᴇʀᴇᴅ ʙʏ Bᴏᴛskɪɴɢᴅᴏᴍs]</a>")

    # Logs channel
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "0"))

    # Webhook or for keeping it alive
    PORT = os.environ.get("PORT", "8080")
