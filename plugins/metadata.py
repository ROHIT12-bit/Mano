import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
from database.database import db
from config import Config
from helper.utils import quote_text

@Client.on_message(filters.private & filters.command(["meta", "metadata"]))
async def meta_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        text, status = await db.get_metadata(message.from_user.id)
        if text:
            msg = f"<b>Your current metadata:</b>\n\n<code>{text}</code>\nStatus: {'Enabled' if status else 'Disabled'}\n\n{Config.CREDITS_LINE}"
        else:
            msg = f"You don't have any metadata set.\nUsage: /meta [text]\n\n{Config.CREDITS_LINE}"
        await message.reply_text(quote_text(msg), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)
        return
    text = message.text.split(" ", 1)[1]
    await db.set_metadata(message.from_user.id, text)
    await message.reply_text(quote_text(f"Metadata text set to: <code>{text}</code>\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@Client.on_message(filters.private & filters.command("setallmeta"))
async def setallmeta_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text(quote_text(f"Usage: /setallmeta [text]\nExample: /setallmeta {Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)
        return
    text = message.text.split(" ", 1)[1]
    await db.set_metadata(message.from_user.id, text, status=True)
    await message.reply_text(quote_text(f"Metadata text set to: <code>{text}</code> and enabled.\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@Client.on_message(filters.private & filters.command("metaon"))
async def metaon_cmd(client: Client, message: Message):
    await db.set_metadata_status(message.from_user.id, True)
    await message.reply_text(quote_text(f"Metadata enabled.\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@Client.on_message(filters.private & filters.command("metaoff"))
async def metaoff_cmd(client: Client, message: Message):
    await db.set_metadata_status(message.from_user.id, False)
    await message.reply_text(quote_text(f"Metadata disabled.\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)
