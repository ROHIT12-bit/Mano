import time
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from database.database import db
from helper.utils import quote_text

@Client.on_message(filters.private & filters.command("plan"))
async def plan_cmd(client: Client, message: Message):
    text = "<b>Premium Plans:</b>\n\n" \
           "1. Daily: 10 INR\n" \
           "2. Weekly: 50 INR\n" \
           "3. Monthly: 150 INR\n\n" \
           f"Contact @Botskingdoms to buy.\n\n{Config.CREDITS_LINE}"
    await message.reply_text(quote_text(text), parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("trial"))
async def trial_cmd(client, message):
    user_id = message.from_user.id
    if await db.is_premium(user_id):
        await message.reply_text(quote_text("You already have premium!"), parse_mode=pyrogram.enums.ParseMode.HTML)
        return
    if await db.has_used_trial(user_id):
        await message.reply_text(quote_text("You have already used your trial!"), parse_mode=pyrogram.enums.ParseMode.HTML)
        return

    expiry_time = time.time() + (1 * 24 * 60 * 60) # 1 day
    await db.add_premium(user_id, expiry_time)
    await db.set_used_trial(user_id)
    await message.reply_text(quote_text(f"Trial premium activated for 1 day!\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("premium"))
async def premium_info(client: Client, message: Message):
    is_premium = await db.is_premium(message.from_user.id)
    if is_premium:
        user_data = await db.get_user_data(message.from_user.id)
        expiry = user_data.get('premium_expiry', 0)
        readable_expiry = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(expiry))
        await message.reply_text(quote_text(f"You are a premium user. Your plan expires on: <code>{readable_expiry}</code>\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)
    else:
        await message.reply_text(quote_text(f"You are not a premium user. Use /plan to see our plans.\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("leaderboard"))
async def leaderboard_cmd(client: Client, message: Message):
    top_users = await db.get_top_renamers()
    text = "<b>Top 10 Renamers:</b>\n\n"
    i = 1
    async for user in top_users:
        text += f"{i}. User ID: <code>{user['id']}</code> - {user.get('rename_count', 0)} renames\n"
        i += 1
    text += f"\n{Config.CREDITS_LINE}"
    await message.reply_text(quote_text(text), parse_mode=pyrogram.enums.ParseMode.HTML)

# Admin Commands

@Client.on_message(filters.private & filters.command("addcredit"))
async def add_credit_cmd(client, message):
    Botskingdoms = await db.get_admins()
    if message.from_user.id not in Botskingdoms:
        return
    if len(message.command) < 3:
        await message.reply_text(quote_text("Usage: /addcredit [user_id] [amount]"), parse_mode=pyrogram.enums.ParseMode.HTML)
        return
    try:
        user_id = int(message.command[1])
        amount = int(message.command[2])
        await db.add_credits(user_id, amount)
        await message.reply_text(quote_text(f"Added {amount} credits to {user_id}\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)
    except ValueError:
        await message.reply_text(quote_text("Invalid input."), parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("remcredit"))
async def rem_credit_cmd(client, message):
    Botskingdoms = await db.get_admins()
    if message.from_user.id not in Botskingdoms:
        return
    if len(message.command) < 3:
        await message.reply_text(quote_text("Usage: /remcredit [user_id] [amount]"), parse_mode=pyrogram.enums.ParseMode.HTML)
        return
    try:
        user_id = int(message.command[1])
        amount = int(message.command[2])
        await db.add_credits(user_id, -amount)
        await message.reply_text(quote_text(f"Removed {amount} credits from {user_id}\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)
    except ValueError:
        await message.reply_text(quote_text("Invalid input."), parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("add_premium"))
async def add_premium_cmd(client, message):
    Botskingdoms = await db.get_admins()
    if message.from_user.id not in Botskingdoms:
        return
    if len(message.command) < 3:
        await message.reply_text(quote_text("Usage: /add_premium [user_id] [days]"), parse_mode=pyrogram.enums.ParseMode.HTML)
        return
    try:
        user_id = int(message.command[1])
        days = int(message.command[2])
        expiry_time = time.time() + (days * 24 * 60 * 60)
        await db.add_premium(user_id, expiry_time)
        await message.reply_text(quote_text(f"Added premium to {user_id} for {days} days.\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)
    except ValueError:
        await message.reply_text(quote_text("Invalid input."), parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("remove_premium"))
async def remove_premium_cmd(client, message):
    Botskingdoms = await db.get_admins()
    if message.from_user.id not in Botskingdoms:
        return
    if len(message.command) < 2:
        await message.reply_text(quote_text("Usage: /remove_premium [user_id]"), parse_mode=pyrogram.enums.ParseMode.HTML)
        return
    try:
        user_id = int(message.command[1])
        await db.remove_premium(user_id)
        await message.reply_text(quote_text(f"Removed premium from {user_id}\n\n{Config.CREDITS_LINE}"), parse_mode=pyrogram.enums.ParseMode.HTML)
    except ValueError:
        await message.reply_text(quote_text("Invalid input."), parse_mode=pyrogram.enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("premium_users"))
async def premium_users_cmd(client, message):
    Botskingdoms = await db.get_admins()
    if message.from_user.id not in Botskingdoms:
        return
    all_users = await db.get_all_users()
    text = "<b>Premium Users:</b>\n\n"
    async for user in all_users:
        if user.get('is_premium') and user.get('premium_expiry') > time.time():
            text += f"ID: <code>{user['id']}</code> - Exp: {time.strftime('%Y-%m-%d', time.localtime(user['premium_expiry']))}\n"
    text += f"\n{Config.CREDITS_LINE}"
    await message.reply_text(quote_text(text), parse_mode=pyrogram.enums.ParseMode.HTML)
