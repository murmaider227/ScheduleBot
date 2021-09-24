from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from app.keyboards import faculty_keyboard


async def start_cmd(message: types.Message ):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Розклад занять","Час занять"]
    keyboard.add(*buttons)
    await message.answer("Hi", reply_markup=keyboard)


async def choose_faculty(message: types.Message):
    await message.answer("Выберите факультет", reply_markup=faculty_keyboard())



def register_handlers_common(dp: Dispatcher):
        dp.register_message_handler(start_cmd, commands="start", state="*")
        dp.register_message_handler(choose_faculty, text="Розклад занять", state="*")
