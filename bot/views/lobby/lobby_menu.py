import asyncio

import discord


from bot.views.base import BaseView
from bot.views.packs.pack_select_lobby import PacksSelectLobbyView
from db.lobbyHandle import deleteLobbyDB, getLobbyCode
from db.packs import fetchAllPacks
from db.userHandle import removePlayerfromDB


class LobbyMenuView(BaseView):
    def __init__(self, uname: str, code: int, player_count: int, players: list, interaction: discord.Interaction, pack: str = "Не обрано"):
        self.uname = uname
        self.code = code
        self.player_count = player_count
        self.players = players
        self.pack = pack
        self.interaction = interaction
        self.menu_text = self._build_text()
        super().__init__(back_view=None)

    def _build_text(self):
        players_str = "\n".join(f"{p}" for p in self.players)
        return (
            f"Лобі {self.uname}\n"
            f"Гравців: {len(self.players)}\n"
            f"{players_str}\n"
            f"Код: {self.code}\n"
            f"Набір слів: {self.pack}\n"
        )


    async def refreshLobby(self, player_count: int = 1, players: list = [], pack_name: str = "Не обрано"): #не забути про те, що тут метод повинен оновлювати ще список гравців
        #ще можна копіпаст цього методу для інших менюшок де це реально буде необхідно в реалтаймі
        self.player_count = player_count
        self.players = players
        self.pack = pack_name
        self.menu_text = self._build_text()
        if self.message:
            await self.interaction.edit_original_response(content=self.menu_text, view=self)


    @discord.ui.button(label="Почати Гру", style=discord.ButtonStyle.primary, row=0)
    async def start_game(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass

    @discord.ui.button(label="Обрати набір", style=discord.ButtonStyle.primary, row=0)
    async def select_pack(self, button: discord.ui.Button, interaction: discord.Interaction):
        packs = await fetchAllPacks()
        await self.goto(interaction, PacksSelectLobbyView(packs, interaction, self.code))

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
