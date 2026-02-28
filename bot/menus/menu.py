from aiogram.types import Message, CallbackQuery
from bot.keyboards.main_menu import main_menu_kb

async def main_menu(message: Message, callback: CallbackQuery):
    if message:
        return await message.answer(
            text="Alias menu",
            reply_markup=main_menu_kb()
            )
    if callback:
        return await callback.message.edit_text(
            text="Alias menu",
            reply_markup=main_menu_kb()
            )
