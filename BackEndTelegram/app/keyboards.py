from aiogram import types
from aiogram.utils.callback_data import CallbackData


callback_days = CallbackData("week","day")

def day_keyboard():


    row_2= types.InlineKeyboardButton('Настройка', callback_data='setting')

    buttons = [
            types.InlineKeyboardButton(text="Пн", callback_data=callback_days.new(day="Понеділок")),
            types.InlineKeyboardButton(text="Вт", callback_data=callback_days.new(day="Вівторок")),
            types.InlineKeyboardButton(text="Ср", callback_data=callback_days.new(day="Середа")),
            types.InlineKeyboardButton(text="Чт", callback_data=callback_days.new(day="Четвер")),
            types.InlineKeyboardButton(text="Пт", callback_data=callback_days.new(day="Пятниця")),
            ]


    keyboard = types.InlineKeyboardMarkup(row_width=5)
    keyboard.add(*buttons)
    keyboard.row(row_2)
    
    return keyboard
