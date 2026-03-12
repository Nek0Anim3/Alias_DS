import asyncio

import discord


from bot.views.base import BaseView
from db.lobbyHandle import deleteLobbyDB
from db.userHandle import removePlayerfromDB


class LobbyMenuView(BaseView):
    def __init__(self, uname: str, code: int, playerCount: int):
        super().__init__(back_view=None)
        self.menu_text = f"Лобі {uname} \nКількість гравців в лобі: {playerCount}\nКод приєднання: {code}"
        self.uname = uname
        self.code = code
        self.playerCount = playerCount

    @discord.ui.button(label="Почати Гру", style=discord.ButtonStyle.primary, row=0)
    async def start_game(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label="Вийти", style=discord.ButtonStyle.secondary, row=4)
    async def exit_lobby(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.main_menu import MainMenuView
        from bot.states.lobby_state import unregister_view
        unregister_view(self.code, interaction.user.id)
        await asyncio.gather(
            deleteLobbyDB(interaction.user.id),
            removePlayerfromDB(interaction.user.id),
            self.goto(interaction, MainMenuView())
        )
