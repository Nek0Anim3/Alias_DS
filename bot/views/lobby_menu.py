import asyncio

import discord


from bot.views.base import BaseView
from db.lobbyHandle import deleteLobbyDB
from db.userHandle import removePlayerfromDB


class LobbyMenuView(BaseView):
    def __init__(self, uname: str, code: int, playerCount: int, players: list):
        self.uname = uname
        self.code = code
        self.playerCount = playerCount
        self.players = players
        self.message: discord.Message = None
        self.menu_text = self._build_text()
        super().__init__(back_view=None)

    def _build_text(self):
        players_str = "\n".join(f"{p}" for p in self.players)
        return (
            f"Лобі {self.uname}\n"
            f"Гравців: {len(self.players)}\n"
            f"{players_str}\n"
            f"Код: {self.code}\n"
        )


    async def refreshLobby(self, playerCount: int):
        self.playerCount = playerCount
        self.menu_text = self._build_text()
        if self.message:
            await self.message.edit(content=self.menu_text, view=self)
        # discord.errors.NotFound: 404 Not Found (error code: 10008): Unknown Message ТВАРИ


    @discord.ui.button(label="Почати Гру", style=discord.ButtonStyle.primary, row=0)
    async def start_game(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label="Вийти", style=discord.ButtonStyle.secondary, row=4)
    async def exit_lobby(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.main_menu import MainMenuView
        from bot.states.lobby_state import unregister_view
        unregister_view(self.code)
        await asyncio.gather(
            deleteLobbyDB(interaction.user.id),
            removePlayerfromDB(interaction.user.id),
            self.goto(interaction, MainMenuView())
        )
