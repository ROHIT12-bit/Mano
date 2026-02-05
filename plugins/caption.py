import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
from database.database import db
from config import Config
from helper.utils import quote_text

@Client.on_message(filters.private & filters.command(["set_caption", "setcaption"]))
async def set_caption_cmd(client: Client, message: Message):
    if len(message.command) < 2:
        await message.reply_text(quote_text(f"Usage: /set_caption [caption text]\nExample: /set_caption <b>{{file_name}}</b>\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)
        return
    caption = message.text.split(" ", 1)[1]
    # We don't wrap the caption in <blockquote> here, as the user might want their own format
    # but the /see_caption will show it.
    await db.set_caption(message.from_user.id, caption)
    await message.reply_text(quote_text(f"Caption saved successfully!\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@Client.on_message(filters.private & filters.command(["see_caption", "see", "caption"]))
async def see_caption_cmd(client: Client, message: Message):
    caption = await db.get_caption(message.from_user.id)
    if caption:
        await message.reply_text(quote_text(f"<b>Your current caption:</b>\n\n<code>{caption}</code>\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)
    else:
        await message.reply_text(quote_text(f"You don't have any custom caption set.\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@Client.on_message(filters.private & filters.command("del_caption"))
async def del_caption_cmd(client: Client, message: Message):
    await db.set_caption(message.from_user.id, None)
    await message.reply_text(quote_text(f"Caption deleted successfully!\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)
