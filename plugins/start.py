from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import Config
from database.database import db
from helper.utils import quote_text, big_and_nice
import pyrogram
import html

def get_start_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏡", callback_data="start"),
            InlineKeyboardButton("🛡️", callback_data="admin_info"),
            InlineKeyboardButton("💳", callback_data="plan_callback"),
            InlineKeyboardButton("💸", callback_data="premium_callback"),
            InlineKeyboardButton("🖥️", callback_data="source_info")
        ],
        [InlineKeyboardButton("• ᴄᴏᴍᴍᴀɴᴅs •", callback_data="help")],
        [
            InlineKeyboardButton("• ᴜᴘᴅᴀᴛᴇ • ⚡", url="https://t.me/Botskingdoms"),
            InlineKeyboardButton("• sᴜᴘᴘᴏʀᴛ • ⚡", url="https://t.me/Botskingdoms_Support")
        ],
        [
            InlineKeyboardButton("• ᴘʀᴇᴍɪᴜᴍ •", callback_data="plan_callback")
            InlineKeyboardButton("• ᴀʙᴏᴜᴛ •", callback_data="about")
        ]
    ])

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
                await message.reply_text(quote_text("Sorry, you are banned from using me."), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)
                return
        except Exception:
            await message.reply_photo(
                photo=Config.FORCE_SUB_PIC,
                caption=quote_text(Config.FORCE_SUB_MSG),
                parse_mode=pyrogram.enums.ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Join Updates Channel", url=f"https://t.me/{Config.FORCE_SUB}")]]
                )
            )
            return

    mention = f'<a href="tg://user?id={user.id}">{html.escape(user.first_name)}</a>'
    text = quote_text(Config.START_MSG.format(mention=mention))
    buttons = get_start_buttons()

    if Config.START_PIC:
        await message.reply_photo(photo=Config.START_PIC, caption=text, reply_markup=buttons, parse_mode=pyrogram.enums.ParseMode.HTML)
    else:
        await message.reply_text(text=text, reply_markup=buttons, parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

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

    await message.reply_text(quote_text(text), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@Client.on_message(filters.private & filters.command("source"))
async def source_cmd(client: Client, message: Message):
    text = f"This bot is open source. You can find the source code on GitHub.\n\n{Config.CREDITS_LINE}"
    await message.reply_text(quote_text(text), parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@Client.on_callback_query(filters.regex("about"))
async def about(client, query):
    text = quote_text(Config.ABOUT_MSG)
    await query.message.edit_caption(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]), parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_callback_query(filters.regex("help"))
async def help_cmd(client, query):
    text = quote_text(Config.HELP_MSG)
    await query.message.edit_caption(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]), parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_callback_query(filters.regex("start"))
async def start_back(client, query):
    user = query.from_user
    mention = f'<a href="tg://user?id={user.id}">{html.escape(user.first_name)}</a>'
    text = quote_text(Config.START_MSG.format(mention=mention))
    buttons = get_start_buttons()
    await query.message.edit_caption(text, reply_markup=buttons, parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_callback_query(filters.regex("admin_info"))
async def admin_info_cb(client, query):
    text = quote_text(f"Admin: @Botskingdoms\n\n{Config.CREDITS_LINE}")
    await query.answer(big_and_nice("Admin Info"), show_alert=True)

@Client.on_callback_query(filters.regex("plan_callback"))
async def plan_callback(client, query):
    text = quote_text("""ᴜᴘɢʀᴀᴅᴇ ᴛᴏ ᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ sᴇʀᴠɪᴄᴇ ᴀɴᴅ ᴇɴJᴏʏ ᴇxᴄʟᴜsɪᴠᴇ ғᴇᴀᴛᴜʀᴇs:
○ ᴜɴʟɪᴍɪᴛᴇᴅ Rᴇɴᴀᴍɪɴɢ.
> ○ ɴᴏ ᴀᴅꜱ.
> ○ ᴇᴀʀʟʏ Aᴄᴄᴇss.
> ○ ᴍᴏʀᴇ ᴘʀɪᴏʀɪᴛʏ

• ᴜꜱᴇ /plan ᴛᴏ ꜱᴇᴇ ᴀʟʟ ᴏᴜʀ ᴘʟᴀɴꜱ ᴀᴛ ᴏɴᴄᴇ.

➲ ғɪʀsᴛ sᴛᴇᴘ : ᴘᴀʏ ᴛʜᴇ ᴀᴍᴏᴜɴᴛ ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ʏᴏᴜʀ ғᴀᴠᴏʀɪᴛᴇ ᴘʟᴀɴ ᴛᴏ ᴛʜᴇ ᴜᴘɪ ɪᴅ ᴏʀ Qʀ.
➲ secoɴᴅ sᴛᴇᴘ : ᴛᴀᴋᴇ ᴀ sᴄʀᴇᴇɴsʜᴏᴛ ᴏғ ʏᴏᴜʀ ᴘᴀʏᴍᴇɴᴛ ᴀɴᴅ sʜᴀʀᴇ ɪᴛ ᴅɪʀᴇᴄᴛʟʏ ʜᴇʀᴇ: @Rioshin 
➲ ᴀʟᴛᴇʀɴᴀᴛɪᴠᴇ sᴛᴇᴘ : ᴏʀ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ sᴄʀᴇᴇɴsʜᴏᴛ ʜᴇʀᴇ ᴀɴᴅ ʀᴇᴘʟʏ ᴡɪᴛʜ ᴛʜᴇ /bought ᴄᴏᴍᴍᴀɴᴅ. [ᴍᴀʏ ɴᴏᴛ ᴡᴏʀᴋ ᴘʀᴏᴘᴇʀʟʏ]

Yᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴ ᴡɪʟʟ ʙᴇ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ᴀғᴛᴇʀ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ""")
    await query.message.edit_caption(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]), parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_callback_query(filters.regex("premium_callback"))
async def premium_callback(client, query):
    is_premium = await db.is_premium(query.from_user.id)
    if is_premium:
        text = quote_text("You are a Premium User!")
    else:
        text = quote_text("You are a Free User. Upgrade to Premium for more features.")
    await query.answer(text, show_alert=True)

@Client.on_callback_query(filters.regex("source_info"))
async def source_info_cb(client, query):
    text = quote_text(f"Bot Source: https://github.com/Rioshin/AutoRenamerBot\n\n{Config.CREDITS_LINE}")
    await query.message.edit_caption(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="start")]]), parse_mode=pyrogram.enums.ParseMode.HTML)
