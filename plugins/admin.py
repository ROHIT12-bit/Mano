import os
import sys
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config
from database.database import db
from helper.utils import quote_text

@Client.on_message(filters.private & filters.command("status"))
async def status_cmd(client: Client, message: Message):
    Botskingdoms = await db.get_admins()
    if message.from_user.id not in Botskingdoms:
        return
    users_count = await db.total_users_count()
    await message.reply_text(quote_text(f"<b>Bot Status:</b>\n\nTotal Users: {users_count}\n\n{Config.CREDITS_LINE}"))

@Client.on_message(filters.private & filters.command("users"))
async def users_cmd(client: Client, message: Message):
    Botskingdoms = await db.get_admins()
    if message.from_user.id not in Botskingdoms:
        return
    users_count = await db.total_users_count()
    await message.reply_text(quote_text(f"Total Users: {users_count}\n\n{Config.CREDITS_LINE}"))

@Client.on_message(filters.private & filters.command("broadcast"))
async def broadcast_cmd(client: Client, message: Message):
    Botskingdoms = await db.get_admins()
    if message.from_user.id not in Botskingdoms:
        return
    if not message.reply_to_message:
        await message.reply_text(quote_text("Reply to a message to broadcast."))
        return

    ms = await message.reply_text(quote_text("Broadcasting..."))
    all_users = await db.get_all_users()
    success = 0
    failed = 0

    async for user in all_users:
        try:
            await message.reply_to_message.copy(user['id'])
            success += 1
        except:
            failed += 1

    await ms.edit(quote_text(f"<b>Broadcast Completed:</b>\n\nSuccess: {success}\nFailed: {failed}\n\n{Config.CREDITS_LINE}"))

@Client.on_message(filters.private & filters.command("ban"))
async def ban_cmd(client: Client, message: Message):
    Botskingdoms = await db.get_admins()
    if message.from_user.id not in Botskingdoms:
        return
    if len(message.command) < 2:
        await message.reply_text(quote_text("Usage: /ban [user_id]"))
        return
    try:
        user_id = int(message.command[1])
        await db.ban_user(user_id)
        await message.reply_text(quote_text(f"User {user_id} banned.\n\n{Config.CREDITS_LINE}"))
    except ValueError:
        await message.reply_text(quote_text("Invalid User ID."))

@Client.on_message(filters.private & filters.command("unban"))
async def unban_cmd(client: Client, message: Message):
    Botskingdoms = await db.get_admins()
    if message.from_user.id not in Botskingdoms:
        return
    if len(message.command) < 2:
        await message.reply_text(quote_text("Usage: /unban [user_id]"))
        return
    try:
        user_id = int(message.command[1])
        await db.unban_user(user_id)
        await message.reply_text(quote_text(f"User {user_id} unbanned.\n\n{Config.CREDITS_LINE}"))
    except ValueError:
        await message.reply_text(quote_text("Invalid User ID."))

@Client.on_message(filters.private & filters.command("restart"))
async def restart_cmd(client: Client, message: Message):
    Botskingdoms = await db.get_admins()
    if message.from_user.id not in Botskingdoms:
        return
    await message.reply_text(quote_text("Restarting..."))
    os.execl(sys.executable, sys.executable, *sys.argv)

@Client.on_message(filters.private & filters.command("add_admin"))
async def add_admin_cmd(client: Client, message: Message):
    # Only owner (from config) can add admins
    if message.from_user.id not in Config.Botskingdoms:
        return
    if len(message.command) < 2:
        await message.reply_text(quote_text("Usage: /add_admin [user_id]"))
        return
    try:
        user_id = int(message.command[1])
        await db.add_admin(user_id)
        await message.reply_text(quote_text(f"User {user_id} added as admin.\n\n{Config.CREDITS_LINE}"))
    except ValueError:
        await message.reply_text(quote_text("Invalid User ID."))

@Client.on_message(filters.private & filters.command("admin_mode"))
async def admin_mode_cmd(client: Client, message: Message):
    Botskingdoms = await db.get_admins()
    if message.from_user.id not in Botskingdoms:
        return
    await message.reply_text(quote_text(f"Admin mode is active for you.\n\n{Config.CREDITS_LINE}"))

@Client.on_message(filters.private & filters.command("shortlink"))
async def shortlink_cmd(client, message):
    Botskingdoms = await db.get_admins()
    if message.from_user.id not in Botskingdoms:
        return
    if len(message.command) < 3:
        await message.reply_text(quote_text("Usage: /shortlink [url] [api]"))
        return
    url = message.command[1]
    api = message.command[2]
    await db.set_shortlink(url, api)
    await message.reply_text(quote_text(f"Shortlink set to {url} with API {api}.\n\n{Config.CREDITS_LINE}"))
