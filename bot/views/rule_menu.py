from bot.views.base import BaseView

class RuleMenuView(BaseView):
    menu_text = (f"Правила Alias\n"
                 f" \n"
                 f"Alias - настільна гра, у якій потрібно вгадати слово.\n"
                 f"Гравці поділяются на команди, та передаючи хід намагаються пояснити слово\n"
                 f"Інші гравці в команді намагаються вгадати\n"
                 f"Перемагає та команда, яка вгадала більше слів\n"
                 f"  \n"
                 f"При описі слова, не можна використовувати синоніми, спільнокореневі\n"
                 f"При пропуску слова, -1 бал команді\n"
                 f"  \n")


    def __init__(self):
        from bot.views.main_menu import MainMenuView
        super().__init__(back_view=MainMenuView())