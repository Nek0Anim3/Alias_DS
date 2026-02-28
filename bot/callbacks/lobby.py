from aiogram.filters.callback_data import CallbackData

class LobbyCallback(CallbackData, prefix="lobby"):
    action: str
    lobby_id: str

class PackCallback(CallbackData, prefix="packs"):
    pack_id: str
    action: str