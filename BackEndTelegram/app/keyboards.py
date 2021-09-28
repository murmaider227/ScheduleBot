from aiogram import types
from aiogram.utils.callback_data import CallbackData
from app.db import DataBase

db = DataBase()

callback_groups = CallbackData("group", "major", "year", "id")

def group_keyboard(user):
    groups = db.get_user_group(user)
    buttons = (types.InlineKeyboardButton(text=str(item[0]) + str(item[1]), callback_data=callback_groups.new(major=item[0], year=item[1], id=item[2])) for item in groups)   
    add = types.InlineKeyboardButton(text="Додати групу", callback_data="add group")
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)
    keyboard.row(add)
    return keyboard

callback_days = CallbackData("week","day")

def day_keyboard():
    row_2=[
        types.InlineKeyboardButton('1 вариант', callback_data="option 1"),
        types.InlineKeyboardButton('2 вариант', callback_data="option 2")
        ]
    row_3=types.InlineKeyboardButton('Видалити групу', callback_data='delete')
    row_4= types.InlineKeyboardButton('Настройка', callback_data='setting')
    buttons = [
            types.InlineKeyboardButton(text="Пн", callback_data=callback_days.new(day="Понеділок")),
            types.InlineKeyboardButton(text="Вт", callback_data=callback_days.new(day="Вівторок")),
            types.InlineKeyboardButton(text="Ср", callback_data=callback_days.new(day="Середа")),
            types.InlineKeyboardButton(text="Чт", callback_data=callback_days.new(day="Четвер")),
            types.InlineKeyboardButton(text="Пт", callback_data=callback_days.new(day="Пятниця")),
            ]


    keyboard = types.InlineKeyboardMarkup(row_width=5)
    keyboard.add(*buttons)
    keyboard.row(*row_2)
    keyboard.row(row_3)
    keyboard.row(row_4)
    
    return keyboard


callback_facultys = CallbackData("user","faculty")

def faculty_keyboard():
    faculty = db.get_faculty()
    buttons = (types.InlineKeyboardButton(item[0], callback_data=callback_facultys.new(faculty=item[0])) for item in faculty)   
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)

    return keyboard

callback_majors = CallbackData("users","major")

def major_keyboard(faculty):
    major = db.get_major(faculty)
    buttons = (types.InlineKeyboardButton(item[0], callback_data=callback_majors.new(major=item[0])) for item in major)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(*buttons)

    return keyboard
callback_years = CallbackData("us","year")

def year_keyboard():
    buttons=(types.InlineKeyboardButton(item, callback_data=callback_years.new(year=item)) for item in range (1,5))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

