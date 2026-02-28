from aiogram import Router, types, F, Bot
from db.lobbyHandle import createLobbyDB, fetchLobbiesList
from bot.keyboards.lobbies_list_board import lobbies_list_kb

router = Router()

@router.callback_query(F.data == "create_lobby")
async def createLobby(callback: types.CallbackQuery):

    await createLobbyDB(callback.from_user.id, callback.from_user.first_name)

    await callback.message.edit_text(
        text="да да мгм", 
        reply_markup=types.InlineKeyboardMarkup(
        inline_keyboard=[[
            types.InlineKeyboardButton(text="Почати гру", callback_data="start_game"),
            types.InlineKeyboardButton(text="Налаштування", callback_data="settings")
        ],
        [
            types.InlineKeyboardButton(text="Обрати пак", callback_data="pack"),
            types.InlineKeyboardButton(text="Вийти", callback_data="quit_lobby")
        ]
        ]
    ))

@router.callback_query(F.data == "list_lobby")
async def lobbiesList(callback: types.CallbackQuery):
    lobbies = await fetchLobbiesList()
    keyboard = await lobbies_list_kb(lobbies)
    await callback.message.edit_text(
        text="Список лобі",
        reply_markup=keyboard.as_markup()
        #types.InlineKeyboardMarkup(
        #inline_keyboard=)
    )