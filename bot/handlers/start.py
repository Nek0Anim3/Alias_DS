from aiogram import Router, types, F
from aiogram.filters import Command
from bot.keyboards.main_menu import main_menu_kb
from bot.menus.menu import main_menu

router = Router()

@router.message(Command("start"))
async def start_Handler(message: types.Message) -> any:
    await main_menu(message, None)
    # await message.answer(
    #     text="Привіт софійко це зайчик джуді гопс!",
    #     reply_markup=main_menu_kb()
    #     )
    
@router.callback_query(F.data == "start")
async def return_toMenu(callback: types.CallbackQuery):
    await main_menu(None, callback)

@router.message(Command("test"))
async def message_Handler(message: types.Message) -> any:
    await message.answer("Hello from routah!")