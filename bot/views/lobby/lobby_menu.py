import asyncio
from collections import Counter
import discord

from bot.states.interactions_state import save_interaction
from bot.states.states import get_state, States
from bot.views.base import BaseView
from bot.views.packs.pack_select_lobby import PacksSelectLobbyView
from bot.views.teams.teams_list_menu import TeamsListView
from db.lobbyHandle import deleteLobbyDB, findLobbyByCode, update_status_lobby
from db.packs import fetchAllPacks, getPackByName
from db.userHandle import removePlayerfromDB
from debug.DebugLogger import DebugLogger
from game.game_manager import GameManager
from game.game_registry import register_active_session, register_game_manager
from game.game_session import GameSession
from game.game_teams import get_lobby_teams, clear_teams


class LobbyMenuView(BaseView):
    def __init__(self, uname: str, code: int, player_count: int, players: list, interaction: discord.Interaction, pack: str):
        self.uname = uname
        self.selected_team = "Не обрана"
        self.code = code
        self.host_id = interaction.user.id
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
            f"Код: {self.code}\n"
            f"------------------\n"
            f"🫂 Ваша команда: {self.selected_team}\n"                        
            f"------------------\n"
            f"👤 Гравців: {len(self.players)}\n"
            f"{players_str}\n"
            f"------------------\n"
            f"📒 Набір слів: {self.pack}\n"
            f"⌚ Таймер раунду: 60с (WIP)"
        )


    async def refresh_lobby(self, player_count: int = None, players: list = None, pack_name: str = None, team_name: str = None):
        if player_count is not None:
            self.player_count = player_count
        if players is not None:
            self.players = players
        if pack_name is not None:
            self.pack = pack_name
        if team_name is not None:
            self.selected_team = team_name
        self.menu_text = self._build_text()
        if get_state(self.host_id) != States.SELECTING_PACK:
            await self.interaction.edit_original_response(content=self.menu_text, view=self)


    @discord.ui.button(label="Почати Гру", style=discord.ButtonStyle.success, row=0)
    async def start_game(self, button: discord.ui.Button, interaction: discord.Interaction):
        save_interaction(interaction.user.id, interaction)

        lobby = await findLobbyByCode(self.code)
        await update_status_lobby(lobby['host'], "ingame")
        pack = await getPackByName(lobby['pack'])
        teams_dict = get_lobby_teams(self.host_id)

        ply_team_list = [item for values in teams_dict.values() for item in values]
        is_teams_equal = True if Counter(ply_team_list) == Counter(lobby['players']) else False

        if pack is None or is_teams_equal is False:
            DebugLogger.Console(f"{lobby['host']} cannot start game: NO PACK / NO TEAM")
            await interaction.response.defer()
            return


        #reg session and manager
        session = GameSession(
            words=pack['words'],
            players=lobby['players'],
            player_scores={},
            teams=teams_dict,
            lobby_id=lobby['host'],
            lobby_time=lobby['timer'])
        register_active_session(interaction.user.id, session)

        game_manager = GameManager(session, self.host_id)
        register_game_manager(self.host_id, game_manager)


        from bot.connectBot import get_bot
        bot = get_bot()
        bot.dispatch("start_game_global", game_manager)


    @discord.ui.button(label="Обрати команду", style=discord.ButtonStyle.primary, row=0)
    async def select_team(self, button: discord.ui.Button, interaction: discord.Interaction):
        view = TeamsListView(interaction, self.host_id, self)
        await self.goto(interaction, view)

    @discord.ui.button(label="Обрати набір", style=discord.ButtonStyle.primary, row=0)
    async def select_pack(self, button: discord.ui.Button, interaction: discord.Interaction):
        packs = await fetchAllPacks()
        from bot.states.states import set_state, States
        set_state(interaction.user.id, States.SELECTING_PACK)
        await self.goto(interaction, PacksSelectLobbyView(packs, interaction, self.code))

    @discord.ui.button(label="Вийти", style=discord.ButtonStyle.secondary, row=4)
    async def exit_lobby(self, button: discord.ui.Button, interaction: discord.Interaction):
        from bot.views.main_menu import MainMenuView
        from bot.states.lobby_state import unregister_hostLobby_view
        unregister_hostLobby_view(interaction.user.id)
        clear_teams(self.host_id)
        from bot.connectBot import get_bot
        bot = get_bot()
        bot.dispatch("destroy_lobby", self.code)
        await asyncio.gather(
            deleteLobbyDB(interaction.user.id),
            removePlayerfromDB(interaction.user.id),
            self.goto(interaction, MainMenuView())
        )
