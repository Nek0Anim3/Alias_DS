import discord
from discord.ext import commands
from bot.states.states import States, get_state, clear_state
from db.lobbyHandle import joinLobbyDB, findLobbyByCode


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
            lobby = await findLobbyByCode(code)
            #Оновлення менюшки для хоста лобі
            from bot.connectBot import get_bot
            bot = get_bot()
            bot.dispatch("update_lobby", lobby)

            #Оновлення менюшки для гравця який приєднується
            from bot.states.join_state import get_join_view
            view = get_join_view(message.author.id)
            await view.joinLobbySetView(lobby_name=lobby['name'], player_count=len(lobby['players']), players=lobby['player_names'], code=code)

            print("JOINED LOBBY, player ", message.author.name)



def setup(bot):
    bot.add_cog(LobbyJoinCog(bot))