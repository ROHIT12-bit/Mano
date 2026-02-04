import os
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ForceReply
from config import Config
from database.database import db
from helper.utils import progress_for_pyrogram, humanbytes, get_fillings, quote_text
from helper.ffmpeg import add_metadata, get_duration, get_width_height, take_screen_shot

# Dictionary to store ongoing tasks for cancellation
ongoing_tasks = {}

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio))
async def handle_file(client: Client, message: Message):
    user_id = message.from_user.id

    # Skip if sequencing is active
    if await db.is_sequencing(user_id):
        return

    # Check if user is banned
    if await db.is_banned(user_id):
        await message.reply_text(quote_text(f"You are banned from using this bot.\n\n{Config.CREDITS_LINE}"))
        return

    file = getattr(message, message.media.value)
    filename = file.file_name
    fillings = get_fillings(message)

    # Check for autorename
    autorename_format = await db.get_autorename_format(user_id)
    if autorename_format:
        # Auto rename logic
        try:
            new_name = autorename_format.format(**fillings)
        except Exception:
            new_name = autorename_format.replace("{file_name}", os.path.splitext(filename)[0])

        # Add extension if not present in format or just append original extension
        if "." not in new_name:
             new_name += os.path.splitext(filename)[1]

        # Truly automatic: Start processing immediately
        await process_rename(client, message, new_name)
    else:
        await message.reply_text(
            quote_text(f"<b>File Name:</b> <code>{filename}</code>\n\nWhat do you want to do with this file?"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📝 Rename", callback_data="rename_manual")],
                [InlineKeyboardButton("✖️ Cancel", callback_data="cancel_rename")]
            ]),
            reply_to_message_id=message.id
        )

@Client.on_callback_query(filters.regex("rename_manual"))
async def rename_manual_cb(client, query):
    await query.message.delete()
    await query.message.reply_text(
        quote_text("Please enter the new name for the file:"),
        reply_markup=ForceReply(True),
        reply_to_message_id=query.message.reply_to_message.id
    )

@Client.on_message(filters.private & filters.reply & filters.text)
async def manual_rename_handler(client, message):
    if not (message.reply_to_message and isinstance(message.reply_to_message.reply_markup, ForceReply)):
        return

    new_name = message.text
    await process_rename(client, message.reply_to_message.reply_to_message, new_name)

@Client.on_callback_query(filters.regex("^rename_"))
async def rename_cb(client, query):
    new_name = query.data.split("_", 1)[1]
    await query.message.delete()
    await process_rename(client, query.message.reply_to_message, new_name)

@Client.on_callback_query(filters.regex("cancel_rename"))
async def cancel_rename_cb(client, query):
    await query.message.edit_text(quote_text(f"Renaming cancelled.\n\n{Config.CREDITS_LINE}"))

async def process_rename(client, message, new_name):
    # Sanitize new_name to prevent path traversal
    new_name = os.path.basename(new_name)
    user_id = message.from_user.id

    # Check credits if not premium
    is_premium = await db.is_premium(user_id)
    if not is_premium:
        credits = await db.get_credits(user_id)
        if credits <= 0:
            await message.reply_text(quote_text(f"You don't have enough credits. Please buy premium or wait for daily credits.\n\n{Config.CREDITS_LINE}"))
            return

    # Download file
    ms = await message.reply_text(quote_text("Trying to Download..."))
    path = os.path.join("downloads", str(user_id), str(time.time()))
    if not os.path.isdir(path):
        os.makedirs(path)

    download_path = os.path.join(path, new_name)

    start_time = time.time()
    try:
        # Store task for cancellation
        task = asyncio.current_task()
        if user_id not in ongoing_tasks:
            ongoing_tasks[user_id] = []
        ongoing_tasks[user_id].append(task)

        file_path = await message.download(
            file_name=download_path,
            progress=progress_for_pyrogram,
            progress_args=(quote_text("Downloading..."), ms, start_time)
        )
    except Exception as e:
        await ms.edit(quote_text(f"Download Error: {e}\n\n{Config.CREDITS_LINE}"))
        return
    finally:
        if user_id in ongoing_tasks and task in ongoing_tasks[user_id]:
            ongoing_tasks[user_id].remove(task)

    if not file_path:
        await ms.edit(quote_text(f"Download failed.\n\n{Config.CREDITS_LINE}"))
        return

    await ms.edit(quote_text("Applying Settings..."))

    # Metadata
    metadata_text, metadata_status = await db.get_metadata(user_id)
    if metadata_status and metadata_text:
        await ms.edit(quote_text("Adding Metadata..."))
        meta_path = os.path.join(path, "meta_" + new_name)
        await add_metadata(file_path, meta_path, metadata_text)
        os.remove(file_path)
        file_path = meta_path

    # Thumbnail
    thumb_id = await db.get_thumb(user_id)
    thumbnail = None
    if thumb_id:
        thumbnail = await client.download_media(thumb_id)
    elif message.video:
        # Extract thumb from video if no custom thumb
        thumbnail = await take_screen_shot(file_path, path, 1)

    # Caption
    fillings = get_fillings(message)
    fillings['file_name'] = new_name # Update with new name
    fillings['file_size'] = humanbytes(os.path.getsize(file_path))

    user_caption = await db.get_caption(user_id)
    if user_caption:
        try:
            caption = user_caption.format(**fillings)
        except Exception:
            caption = user_caption.format(file_name=new_name, file_size=fillings['file_size'])
    else:
        try:
            caption = Config.DEF_CAP.format(**fillings)
        except Exception:
            caption = Config.DEF_CAP.format(file_name=new_name)

    # Apply branding and blockquote to caption if not already present
    if "<blockquote>" not in caption:
        caption = quote_text(caption)

    # Media Type
    media_type = await db.get_media_type(user_id)

    await ms.edit(quote_text("Uploading..."))
    start_time = time.time()

    try:
        if media_type == "video" and (message.video or message.document):
            duration = get_duration(file_path)
            width, height = get_width_height(file_path)
            await client.send_video(
                chat_id=message.chat.id,
                video=file_path,
                caption=caption,
                thumb=thumbnail,
                duration=duration,
                width=width,
                height=height,
                progress=progress_for_pyrogram,
                progress_args=(quote_text("Uploading..."), ms, start_time)
            )
        else:
            await client.send_document(
                chat_id=message.chat.id,
                document=file_path,
                caption=caption,
                thumb=thumbnail,
                progress=progress_for_pyrogram,
                progress_args=(quote_text("Uploading..."), ms, start_time)
            )
    except Exception as e:
        await ms.edit(quote_text(f"Upload Error: {e}\n\n{Config.CREDITS_LINE}"))
    else:
        await ms.delete()
        # Increment rename count and decrease credits
        await db.increment_rename_count(user_id)
        if not is_premium:
            await db.add_credits(user_id, -1)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if thumbnail and os.path.exists(thumbnail):
            os.remove(thumbnail)
        # Clean up directory
        try:
            os.rmdir(path)
        except:
            pass

@Client.on_message(filters.private & filters.command("autorename"))
async def autorename_cmd(client, message):
    if len(message.command) < 2:
        await message.reply_text(quote_text("Usage: /autorename [format]\nExample: /autorename [Prefix] {file_name} [Suffix]"))
        return
    format = message.text.split(" ", 1)[1]
    await db.set_autorename_format(message.from_user.id, format)
    await message.reply_text(quote_text(f"Auto-rename format set to: <code>{format}</code>\n\n{Config.CREDITS_LINE}"))

@Client.on_message(filters.private & filters.command("showformat"))
async def showformat_cmd(client, message):
    format = await db.get_autorename_format(message.from_user.id)
    if format:
        await message.reply_text(quote_text(f"Your current auto-rename format is: <code>{format}</code>\n\n{Config.CREDITS_LINE}"))
    else:
        await message.reply_text(quote_text(f"You haven't set any auto-rename format.\n\n{Config.CREDITS_LINE}"))

@Client.on_message(filters.private & filters.command("setmedia"))
async def setmedia_cmd(client, message):
    await message.reply_text(
        quote_text("Choose allowed media types for upload:"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Document", callback_data="media_document"),
             InlineKeyboardButton("Video", callback_data="media_video")]
        ])
    )

@Client.on_callback_query(filters.regex("^media_"))
async def media_cb(client, query):
    media_type = query.data.split("_")[1]
    await db.set_media_type(query.from_user.id, media_type)
    await query.message.edit_text(quote_text(f"Default upload media type set to: <b>{media_type}</b>\n\n{Config.CREDITS_LINE}"))

@Client.on_message(filters.private & filters.command("cancel"))
async def cancel_task(client, message):
    user_id = message.from_user.id
    cancelled = False

    if await db.is_sequencing(user_id):
        await db.stop_sequence(user_id)
        await message.reply_text(Config.CANCEL_SEQUENCE_MSG)
        cancelled = True

    if user_id in ongoing_tasks and ongoing_tasks[user_id]:
        for task in ongoing_tasks[user_id]:
            task.cancel()
        ongoing_tasks[user_id] = []
        await message.reply_text(quote_text(f"Ongoing tasks cancelled.\n\n{Config.CREDITS_LINE}"))
        cancelled = True

    if not cancelled:
        await message.reply_text(quote_text(f"No ongoing task or sequence found.\n\n{Config.CREDITS_LINE}"))

@Client.on_message(filters.private & filters.command("queue"))
async def queue_cmd(client, message):
    user_id = message.from_user.id
    count = len(ongoing_tasks.get(user_id, []))
    await message.reply_text(quote_text(f"You have {count} tasks in progress.\n\n{Config.CREDITS_LINE}"))
