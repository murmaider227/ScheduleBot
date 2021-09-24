from aiogram import types
from aiogram.utils.callback_data import CallbackData
from app.db import get_faculty, get_major

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


callback_facultys = CallbackData("user","faculty")

def faculty_keyboard():
    faculty = get_faculty()
    buttons = (types.InlineKeyboardButton(item[0], callback_data=callback_facultys.new(faculty=item[0])) for item in faculty)   
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)

    return keyboard

callback_majors = CallbackData("users","major")

def major_keyboard(faculty):
    major = get_major(faculty)
    buttons = (types.InlineKeyboardButton(item[0], callback_data=callback_majors.new(major=item[0])) for item in major)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)

    return keyboard
