import discord

import bot.states.lobby_state as lobby_state
from bot.states.interactions_state import save_interaction
from bot.states.join_state import register_join_view
from bot.states.states import set_state, States
from bot.views.base import BaseView
from bot.views.global_leaderboard_menu import get_cache_leaderboard, set_leaderboard_cache
from db.lobbyHandle import createLobbyDB, fetch_leaderboard_db
from debug.DebugLogger import DebugLogger


class MainMenuView(BaseView):
    menu_text = "Вітаю в Alias"

    def __init__(self):
        super().__init__(back_view=None)

    @discord.ui.button(label="Створити Лобі", style=discord.ButtonStyle.primary, row=0)
    async def open_lobby(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.lobby.lobby_menu import LobbyMenuView
        lobby = await createLobbyDB(interaction.user.id, interaction.user.name)
        view = LobbyMenuView(
            code=lobby['code'],
            uname=lobby['name'],
            player_count=len(lobby['players']),
            players=lobby['player_names'],
            interaction=interaction,
            pack=lobby['pack'])
        lobby_state.register_hostLobby_view(interaction.user.id, view)
        await self.goto(interaction, view)
        save_interaction(interaction.user.id, interaction)

    @discord.ui.button(label="Приєднатися", style=discord.ButtonStyle.primary, row=0)
    async def open_join(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.join_menu import JoinMenuView
        view = JoinMenuView(interaction)
        register_join_view(interaction.user.id, view)
        await self.goto(interaction, view)
        set_state(interaction.user.id, States.CODE_LOBBY_WAIT)
        #Save interaction for UI updates | Important!
        save_interaction(interaction.user.id, interaction)

    @discord.ui.button(label="Набори слів", style=discord.ButtonStyle.secondary, row=1)
    async def open_packs(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.packs.packs_menu import PacksMenuView
        await self.goto(interaction, PacksMenuView())

    @discord.ui.button(label="Правила", style=discord.ButtonStyle.secondary, row=1)
    async def open_help(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.rule_menu import RuleMenuView
        await self.goto(interaction, RuleMenuView())

    @discord.ui.button(label="Лідерборд", style=discord.ButtonStyle.secondary, row=1)
    async def open_leaderboard(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.global_leaderboard_menu import GlobalLeaderView
        from bot.states.leaderboard_cache import get_leaderboard_cache, update_leaderboard_cache
        cache = get_leaderboard_cache()
        print(f"Cache: {cache}")
        if cache is []:
            leader_dict = await fetch_leaderboard_db()
            update_leaderboard_cache(leader_dict)
        await self.goto(interaction, GlobalLeaderView(get_leaderboard_cache()))



