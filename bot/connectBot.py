import discord
import os
from dotenv import load_dotenv
load_dotenv()

bot = None
async def start_bot():
    global bot
    bot = discord.Bot(intents=discord.Intents.default())

    @bot.event
    async def on_ready():
        print(f"Bot online {bot.user}")

    #Реєстрація івентів, команд та іншого.. не загубитись пж(
    bot.load_extension('bot.cogs.main_menu_cog')
    bot.load_extension('bot.cogs.create_packs_cog')
    bot.load_extension('bot.cogs.lobby_update_cog')
    await bot.start(os.getenv("BOT"))

def get_bot() -> discord.Bot:
    if bot is None:
        raise RuntimeError("Бот не ініціалізований")
    return bot
