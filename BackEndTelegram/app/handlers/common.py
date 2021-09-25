from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from app.keyboards import faculty_keyboard
from app.db import create_user

async def start_cmd(message: types.Message ):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Розклад занять","Час занять"]
    keyboard.add(*buttons)
    create_user(message.from_user.username, message.from_user.id)
    await message.answer("Hi", reply_markup=keyboard)


def register_handlers_common(dp: Dispatcher):
        dp.register_message_handler(start_cmd, commands="start", state="*")
