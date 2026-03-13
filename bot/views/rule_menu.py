from bot.views.base import BaseView

class RuleMenuView(BaseView):
    menu_text = "Правила Alias"

    def __init__(self):
        from bot.views.main_menu import MainMenuView
        super().__init__(back_view=MainMenuView())