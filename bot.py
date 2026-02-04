import os
import logging
import pyrogram
from pyrogram import Client
from pyrogram.types import BotCommand
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Botskingdoms")

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Botskingdoms_Renamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="plugins"),
            workers=Config.WORKERS
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username

        # Set bot commands automatically
        try:
            await self.set_bot_commands([
                BotCommand("start", "Check whether the bot is alive"),
                BotCommand("ssequence", "Start file sequencing"),
                BotCommand("esequence", "End file sequencing"),
                BotCommand("stats", "Check usage statistics"),
                BotCommand("autorename", "Set auto-rename format"),
                BotCommand("showformat", "View your current rename format"),
                BotCommand("source", "Select rename source"),
                BotCommand("cancel", "Clear current queue"),
                BotCommand("queue", "Check current queues"),
                BotCommand("info", "View your account info"),
                BotCommand("leaderboard", "Top 10 renamers"),
                BotCommand("setmedia", "Choose allowed media types"),
                BotCommand("setthumb", "Set thumbnail"),
                BotCommand("viewthumb", "View current thumbnail"),
                BotCommand("delthumb", "Delete thumbnail"),
                BotCommand("get_thumb", "Extract thumbnail from video/file"),
                BotCommand("set_caption", "Set custom caption"),
                BotCommand("see_caption", "View current caption"),
                BotCommand("del_caption", "Delete caption"),
                BotCommand("meta", "Set metadata text"),
                BotCommand("setallmeta", "Apply metadata to all fields"),
                BotCommand("metaon", "Enable metadata"),
                BotCommand("metaoff", "Disable metadata"),
                BotCommand("plan", "View premium plans"),
                BotCommand("premium", "Check pre/plans"),
                BotCommand("premium_users", "List premium users (Admin)"),
                BotCommand("addcredit", "Add credits to user (Admin)"),
                BotCommand("remcredit", "Remove credits (Admin)"),
                BotCommand("add_premium", "Add premium user (Admin)"),
                BotCommand("remove_premium", "Remove premium user (Admin)"),
                BotCommand("restart", "Restart bot (Admin)"),
                BotCommand("status", "Bot status (Admin)"),
                BotCommand("users", "Total users (Admin)"),
                BotCommand("broadcast", "Broadcast message (Admin)"),
                BotCommand("ban", "Ban a user (Admin)"),
                BotCommand("unban", "Unban user (Admin)"),
                BotCommand("admin_mode", "Toggle admin mode (Admin)"),
                BotCommand("add_admin", "Add admin (Owner only)"),
                BotCommand("shortlink", "Set shortlink (Admin)")
            ])
            logger.info("Bot commands set successfully.")
        except Exception as e:
            logger.error(f"Failed to set bot commands: {e}")

        logger.info(f"Botskingdoms Bot started as {me.first_name} (@{me.username})")

    async def stop(self, *args):
        await super().stop()
        logger.info("Botskingdoms Bot stopped.")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
