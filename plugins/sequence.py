from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from database.database import db
from helper.utils import quote_text

@Client.on_message(filters.private & filters.command("ssequence"))
async def start_sequence_cmd(client: Client, message: Message):
    if await db.is_sequencing(message.from_user.id):
        await message.reply_text(quote_text("You are already in a file sequencing session."))
        return
    await db.start_sequence(message.from_user.id)
    await message.reply_text(quote_text(Config.S_SEQUENCE_MSG))

@Client.on_message(filters.private & filters.command("esequence"))
async def end_sequence_cmd(client: Client, message: Message):
    if not await db.is_sequencing(message.from_user.id):
        await message.reply_text(quote_text("You are not in a file sequencing session. Use /ssequence to start one."))
        return

    files = await db.get_sequence(message.from_user.id)
    if not files:
        await db.stop_sequence(message.from_user.id)
        await message.reply_text(quote_text("No files were sent. Sequencing session ended."))
        return

    await message.reply_text(quote_text(Config.E_SEQUENCE_MSG))

    # Send files in order
    for i, file in enumerate(files, 1):
        try:
            caption = quote_text(f"File {i}: {file['file_name']}")
            if file['media_type'] == "video":
                await client.send_video(message.chat.id, video=file['file_id'], caption=caption)
            elif file['media_type'] == "audio":
                await client.send_audio(message.chat.id, audio=file['file_id'], caption=caption)
            else:
                await client.send_document(message.chat.id, document=file['file_id'], caption=caption)
        except Exception as e:
            await message.reply_text(quote_text(f"Error sending file {i}: {e}"))

    await db.stop_sequence(message.from_user.id)
    await message.reply_text(quote_text(f"Successfully sequenced {len(files)} files!\n\n{Config.CREDITS_LINE}"))

@Client.on_message(filters.private & filters.command("stats"))
async def stats_cmd(client: Client, message: Message):
    total_users = await db.total_users_count()
    total_sequences = await db.get_total_sequences()
    user_data = await db.get_user_data(message.from_user.id)

    text = f"<b>Botskingdoms Stats:</b>\n\n" \
           f"Total Users: {total_users}\n" \
           f"Total Sequences: {total_sequences}\n\n" \
           f"<b>Your Stats:</b>\n" \
           f"Renames: {user_data.get('rename_count', 0)}\n" \
           f"Credits: {user_data.get('credits', 0)}\n\n" \
           f"{Config.CREDITS_LINE}"
    await message.reply_text(quote_text(text))

@Client.on_message(filters.private & (filters.document | filters.video | filters.audio), group=-1)
async def collection_handler(client: Client, message: Message):
    if await db.is_sequencing(message.from_user.id):
        file = getattr(message, message.media.value)
        await db.add_to_sequence(message.from_user.id, file.file_id, file.file_name, message.media.value)
        await message.reply_text(quote_text(f"Added to sequence: <code>{file.file_name}</code>"), quote=True)
        # Stop propagation so rename.py doesn't catch it
        message.stop_propagation()
