from aiogram.utils.keyboard import InlineKeyboardBuilder
from db.lobbyHandle import getLobbyIdList



async def lobbies_list_kb(lobbies_list: list):
    builder = InlineKeyboardBuilder()
    listsize = len(lobbies_list)
    list_id = getLobbyIdList()
    for count in range (0, listsize):
        builder.button(text=f"Lobby {lobbies_list[count]}", callback_data=f"{str(list_id[count])}")
    builder.button(text="Назад", callback_data="start")
    builder.adjust(1)
    return builder