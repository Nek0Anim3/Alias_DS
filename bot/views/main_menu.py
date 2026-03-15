import discord

import bot.states.lobby_state as lobby_state
from bot.views.base import BaseView
from db.lobbyHandle import createLobbyDB, getLobbyCode
from bot.states.states import set_state, States

class MainMenuView(BaseView):
    menu_text = "Вітаю в Alias"

    def __init__(self):
        super().__init__(back_view=None)

    @discord.ui.button(label="Створити Лобі", style=discord.ButtonStyle.primary, row=0)
    async def open_lobby(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.lobby_menu import LobbyMenuView
        await  createLobbyDB(interaction.user.id, interaction.user.name)
        code = await getLobbyCode(interaction.user.id)
        view = LobbyMenuView(code=code, uname=interaction.user.name, player_count=1, players=[interaction.user.name], interaction=interaction)
        lobby_state.register_view(code, interaction.user.id, view)
        await self.goto(interaction, view)

    @discord.ui.button(label="Приєднатися", style=discord.ButtonStyle.primary, row=0)
    async def open_join(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.join_menu import JoinMenuView
        await self.goto(interaction, JoinMenuView())
        set_state(interaction.user.id, States.CODE_LOBBY_WAIT)

    @discord.ui.button(label="Набори слів", style=discord.ButtonStyle.secondary, row=1)
    async def open_packs(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.packs_menu import PacksMenuView
        await self.goto(interaction, PacksMenuView())

    @discord.ui.button(label="Правила", style=discord.ButtonStyle.secondary, row=1)
    async def open_help(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.rule_menu import RuleMenuView
        await self.goto(interaction, RuleMenuView())

    #DEV
    @discord.ui.button(label="Лобби ивент", style=discord.ButtonStyle.secondary, row=2)
    async def test_btn(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.connectBot import get_bot
        bot = get_bot()
        code = 1234 #temp
        bot.dispatch("custom_e", code)