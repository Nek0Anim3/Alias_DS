import discord
from bot.views.base import BaseView
from bot.views.main_menu import MainMenuView
from debug.DebugLogger import DebugLogger

class GlobalLeaderView(BaseView):
    def __init__(self, leaderboard_list: list):
        self.menu_text = self._build_text(leaderboard_list)
        super().__init__(back_view=MainMenuView())

    def _build_text(self, leaderboard_list: list):
        lines = ["Глобальна таблиця лідерів\n------------------------"]
        for leaderboard in leaderboard_list:
            try:
                del leaderboard["_id"]
                del leaderboard["uid"]
                del leaderboard["lobby_id"]
                del leaderboard["role"]
            except KeyError:
                break
        counter = 0
        for el in leaderboard_list:
            counter += 1
            if el['score'] != 0:
                lines.append(f"[{counter}] {el['name']} —— {el['score']}")
        return "\n".join(lines)

