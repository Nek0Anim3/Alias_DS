import discord
from discord.ext import commands
from bot.states.states import States, get_state, set_state, update_data, get_data, clear_state
from bot.views.packs_creation_menu import CreatePackMenu
from db.lobbyHandle import joinLobbyDB


class LobbyJoinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        if get_state(message.author.id) == States.CODE_LOBBY_WAIT:
            code = 0
            try:
                code = int(message.content)
            except ValueError:
                await message.reply(content="Код повинен бути з 4 цифр")
                return
            isJoined = await joinLobbyDB(code, message.author.id, message.author.name)
            if not isJoined:
                return
            clear_state(message.author.id)
            from bot.connectBot import get_bot
            bot = get_bot()
            bot.dispatch("lobby_join", code)
            print("JOINED LOBBY, player ", message.author.name)

def setup(bot):
    bot.add_cog(LobbyJoinCog(bot))