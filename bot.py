import os
import logging
import pyrogram
from pyrogram import Client
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
        logger.info(f"Botskingdoms Bot started as {me.first_name} (@{me.username})")

    async def stop(self, *args):
        await super().stop()
        logger.info("Botskingdoms Bot stopped.")

if __name__ == "__main__":
    bot = Bot()
    bot.run()
