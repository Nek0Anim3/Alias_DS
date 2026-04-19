from enum import Enum
import discord
from bot.views.base import BaseView
from game.game_registry import get_active_session


class RoundView(BaseView):
    def __init__(self, lobby_id: int, role: str, uid: int):
        from bot.connectBot import get_bot
        self.bot = get_bot()
        self.role = role

        self.words = [self.current_word]
        self.menu_text = "-"

        #Initial UI init for HOST!
        self.btn1 = ControlButton(type_btn=ButtonTypes.GREEN, view=self)
        self.btn2 = ControlButton(type_btn=ButtonTypes.RED, view=self)
        self.menu_text = f"---"
        super().__init__(back_view=None)



        if role:
            self.add_item(self.btn1)
            self.add_item(self.btn2)
            self.menu_text = f"{self.current_word} <-"

    #------------------------------------------------------------------------------------ quite a long constructor method...

    def _build_text(self, words_str):

        return f"{words_str} <-\n------------------\nЗалишилось {self.time}с"

    async def update_text(self, word = None):
        if word is not None:
            self.words.append(word)
            self.current_word = word
        if self.role != "leader":
            words_str = "\n".join(f"{w}" for w in self.words[:-1])
        else:
            words_str = "\n".join(f"{w}" for w in self.words)
        text = self._build_text(words_str)
        await self.interaction.edit_original_response(content=text, view=self)


    # def rebase_view_buttons(self, role: RoleTypes):
    #     match role:
    #         case RoleTypes.LEADER:
    #             DebugLogger.Console(f"ROUNDS: Adding buttons to {self.uid}")
    #             self.add_item(self.btn1)
    #             self.add_item(self.btn2)
    #         case RoleTypes.MEMBER:
    #             self.remove_item(self.btn1)
    #             self.remove_item(self.btn2)
    #             DebugLogger.Console(f"ROUNDS: Removing button from {self.uid}")

class ControlButton(discord.ui.Button):
    def __init__(self, type_btn: ButtonTypes, view: RoundView, interaction = discord.Interaction):
        from bot.connectBot import get_bot
        self._view = view
        self.bot = get_bot()
        if type == ButtonTypes.GREEN:

            super().__init__(
                    label="✅ Вгадав",
                    style=discord.ButtonStyle.success,
                    row=0
                )
        else:
            super().__init__(
                    label="❎ Не вгадав",
                    style=discord.ButtonStyle.danger,
                    row=0
                )

    async def callback(self, interaction: discord.Interaction):
        if self.style == discord.ButtonStyle.success:
            self.bot.dispatch("update_text", "yes")
        else:
            self.bot.dispatch("update_text", "no")

class ButtonTypes(Enum):
    GREEN = 1
    RED = 2

class RoleTypes(Enum):
    LEADER = 1
    MEMBER = 2