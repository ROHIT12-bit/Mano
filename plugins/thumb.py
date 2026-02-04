import os
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
from database.database import db
from helper.ffmpeg import take_screen_shot
from config import Config
from helper.utils import quote_text

@Client.on_message(filters.private & filters.command("setthumb"))
async def set_thumb_cmd(client: Client, message: Message):
    if not message.reply_to_message or not (message.reply_to_message.photo):
        await message.reply_text(quote_text(f"Please reply to a photo to set it as a thumbnail.\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)
        return

    thumb_id = message.reply_to_message.photo.file_id
    await db.set_thumb(message.from_user.id, thumb_id)
    await message.reply_text(quote_text(f"Thumbnail saved successfully!\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("viewthumb"))
async def view_thumb_cmd(client: Client, message: Message):
    thumb_id = await db.get_thumb(message.from_user.id)
    if thumb_id:
        await message.reply_photo(photo=thumb_id, caption=quote_text(f"Your current thumbnail.\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)
    else:
        await message.reply_text(quote_text(f"You don't have any thumbnail set.\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("delthumb"))
async def del_thumb_cmd(client: Client, message: Message):
    await db.set_thumb(message.from_user.id, None)
    await message.reply_text(quote_text(f"Thumbnail deleted successfully!\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("get_thumb"))
async def get_thumb_cmd(client: Client, message: Message):
    if not message.reply_to_message or not (message.reply_to_message.video or message.reply_to_message.document):
        await message.reply_text(quote_text(f"Please reply to a video or file to extract thumbnail.\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)
        return

    ms = await message.reply_text(quote_text("Extracting thumbnail..."), parse_mode=pyrogram.enums.ParseMode.HTML)
    file = message.reply_to_message

    if file.video:
        file_path = await client.download_media(file)
        thumb_path = await take_screen_shot(file_path, "downloads", 1)
        if thumb_path:
            await message.reply_photo(photo=thumb_path, caption=quote_text(f"Extracted thumbnail.\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)
            os.remove(thumb_path)
        else:
            await ms.edit(quote_text(f"Failed to extract thumbnail.\n\n{Config.CREDITS_LINE}"))
        os.remove(file_path)
    else:
        # If it's a document with a thumbnail
        if file.document.thumbs:
            thumb_id = file.document.thumbs[0].file_id
            await message.reply_photo(photo=thumb_id, caption=quote_text(f"Extracted thumbnail from document.\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)
        else:
            await ms.edit(quote_text(f"This document has no thumbnail.\n\n{Config.CREDITS_LINE}"))
    await ms.delete()
