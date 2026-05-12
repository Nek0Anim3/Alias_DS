import discord
from discord.ext import commands
from bot.states.states import States, get_state, clear_state
from db.lobbyHandle import joinLobbyDB, findLobbyByCode
from debug.DebugLogger import DebugLogger

class LobbyJoinCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        DebugLogger.Console(f"GOT MESSAGE {message.content}")
        if message.author.bot:
            return
        if get_state(message.author.id) == States.CODE_LOBBY_WAIT:
            try:
                code = int(message.content)
            except ValueError:
                await message.reply(content="Код повинен бути з 4 цифр")
                return
            lobby = await findLobbyByCode(code)
            if lobby['status'] == "ingame":
                await message.reply(content="Гра вже почалась")
                return
            isJoined = await joinLobbyDB(code, message.author.id, message.author.name)
            if not isJoined:
                return
            clear_state(message.author.id)

            new_lobby = await findLobbyByCode(code) #isn't good but okay

            from bot.connectBot import get_bot
            bot = get_bot()
            DebugLogger.Console(f"DISPATCHING UPDATE_LOBBY WITH DATA: {new_lobby['player_names']}, {len(new_lobby['players'])}")
            bot.dispatch("update_lobby", new_lobby)

            #Оновлення менюшки для гравця який приєднується
            from bot.states.join_state import get_join_view
            view = get_join_view(message.author.id)
            await view.joinLobbySetView(lobby_name=new_lobby['name'], player_count=len(new_lobby['players']), players=new_lobby['player_names'], code=code, host_id=new_lobby['host'])

            DebugLogger.Console(f"Player {message.author.name} joined {new_lobby['host']}")



def setup(bot):
    bot.add_cog(LobbyJoinCog(bot))