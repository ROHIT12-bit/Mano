from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import Config
from database.database import db
from helper.utils import quote_text
import pyrogram

@Client.on_message(filters.private & filters.command("start"))
async def start(client: Client, message: Message):
    user = message.from_user
    if not await db.is_user_exist(user.id):
        await db.add_user(user.id)

    # Force Subscribe Logic
    if Config.FORCE_SUB:
        try:
            user_member = await client.get_chat_member(Config.FORCE_SUB, user.id)
            if user_member.status == "kicked":
                await message.reply_text(quote_text("Sorry, you are banned from using me."))
                return
        except Exception:
            await message.reply_photo(
                photo=Config.FORCE_SUB_PIC,
                caption=quote_text(Config.FORCE_SUB_MSG),
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Updates Channel", url=f"https://t.me/{Config.FORCE_SUB}")]]
                )
            )
            return

    text = quote_text(Config.START_MSG.format(mention=user.mention))
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Updates", url="https://t.me/Botskingdoms"),
         InlineKeyboardButton("Support", url="https://t.me/Botskingdoms_Support")],
        [InlineKeyboardButton("About", callback_data="about"),
         InlineKeyboardButton("Help", callback_data="help")]
    ])

    if Config.START_PIC:
        await message.reply_photo(photo=Config.START_PIC, caption=text, reply_markup=buttons)
    else:
        await message.reply_text(text=text, reply_markup=buttons, parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("info"))
async def info(client: Client, message: Message):
    user_id = message.from_user.id
    user_data = await db.get_user_data(user_id)

    text = f"<b>User Info:</b>\n\n" \
           f"Name: {message.from_user.mention}\n" \
           f"ID: <code>{user_id}</code>\n" \
           f"Credits: {user_data.get('credits', 0)}\n" \
           f"Premium: {'Yes' if await db.is_premium(user_id) else 'No'}\n" \
           f"Renames: {user_data.get('rename_count', 0)}\n\n" \
           f"{Config.CREDITS_LINE}"

    await message.reply_text(quote_text(text))

@Client.on_message(filters.private & filters.command("source"))
async def source(client: Client, message: Message):
    text = f"This bot is open source. You can find the source code on GitHub.\n\n{Config.CREDITS_LINE}"
    await message.reply_text(quote_text(text))

@Client.on_callback_query(filters.regex("about"))
async def about(client, query):
    text = quote_text(Config.ABOUT_MSG)
    if query.message.photo:
        await query.message.edit_caption(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))
    else:
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))

@Client.on_callback_query(filters.regex("help"))
async def help_cmd(client, query):
    text = quote_text(Config.HELP_MSG)
    if query.message.photo:
        await query.message.edit_caption(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))
    else:
        await query.message.edit_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]))

@Client.on_callback_query(filters.regex("start"))
async def start_back(client, query):
    user = query.from_user
    text = quote_text(Config.START_MSG.format(mention=user.mention))
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Updates", url="https://t.me/Botskingdoms"),
         InlineKeyboardButton("Support", url="https://t.me/Botskingdoms_Support")],
        [InlineKeyboardButton("About", callback_data="about"),
         InlineKeyboardButton("Help", callback_data="help")]
    ])
    if query.message.photo:
        await query.message.edit_caption(text, reply_markup=buttons)
    else:
        await query.message.edit_text(text, reply_markup=buttons)
